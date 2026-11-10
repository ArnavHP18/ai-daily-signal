#!/usr/bin/env python3
"""Collect today's raw material for an AI Daily Signal edition.

Run from the repo root at the start of every run, before any web search:

    python3 scripts/collect.py                 # last 48 hours
    python3 scripts/collect.py --hours 72      # wider window (catch-up days)
    python3 scripts/collect.py --no-reactions  # skip YouTube/Reddit/HN reaction lookups

It reads config/sources.json and config/companies.json, fetches everything with curl
(through the session proxy) in parallel, and writes to _working/collect/DATE/ (not committed):

  digest.md        start here: stats, top candidates by topic, product updates per company
                   (official changelog entries + news mentions + what people are saying),
                   developer signals, "what are we missing" (unmapped trends, suggested
                   sources, companies not in our directory) and failed sources
  candidates.json  every dated item in the window, deduplicated, with sources and topic hints
  companies.json   per company: new official updates, headline mentions, reactions
  trends.json      unmapped trends, suggested sources and companies
  stats.json       counts and per-source status

It also updates state/collector-state.json (fingerprints of changelog lines seen before),
which is how only *new* changelog entries surface. Commit that file with the edition.
Nothing here is verified: the collector finds, the run checks.
"""
import concurrent.futures as cf
import datetime as dt
import email.utils
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG_SOURCES = os.path.join(ROOT, 'config', 'sources.json')
CFG_COMPANIES = os.path.join(ROOT, 'config', 'companies.json')
COLLECT_STATE = os.path.join(ROOT, 'state', 'collector-state.json')
SIGNAL_STATE = os.path.join(ROOT, 'state', 'signal-state.json')
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
NOW = dt.datetime.now(dt.timezone.utc)

CATEGORIES = json.load(open(os.path.join(ROOT, 'config', 'categories.json')))['categories']
TOPIC_WORDS = {c['id']: c['hint'] for c in CATEGORIES}     # sorting hints only; the run decides the category
STOP = set('''the a an and or of to in on for with by at from as is are was were be been it its this that these those how why what when where who which
new news report reports says said say will can could would should may might more most over into after before about than up out off not no yes just
ai artificial intelligence update updates today week year years day days time first last next big top best you your our we they he she his her their
inc ltd llc corp co mr ms dr us uk eu one two three four five ceo cto cfo exclusive opinion analysis video watch live breaking explained here there
january february march april may june july august september october november december monday tuesday wednesday thursday friday saturday sunday
nov oct dec jan feb mar apr jun jul aug sep sept'''.split())


GENERIC = set('''future billion million trillion ai-driven ai-powered data centers data center u.s china america american
global world report study survey market markets stocks stock shares investors deal deals jobs workers startup startups
government congress democrats republicans state states city cities company companies industry tech technology
generative agentic agents agent models model chips chip power energy health security robots robot india indian'''.split())


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def fetch(url, timeout=25):
    """GET with curl (uses the session proxy and CA bundle). Returns (status, text)."""
    try:
        p = subprocess.run(['curl', '-gsSL', '--compressed', '-A', UA, '--max-time', str(timeout),
                            '-w', '\n__STATUS__%{http_code}', url], capture_output=True, timeout=timeout + 10)
        out = p.stdout.decode('utf-8', 'replace')
        i = out.rfind('\n__STATUS__')
        return (int(out[i + 11:] or 0) if i >= 0 else 0), (out[:i] if i >= 0 else out)
    except Exception as e:  # noqa: BLE001 - any failure is just a failed source
        return 0, str(e)


def strip(s):
    s = re.sub(r'<!\[CDATA\[|\]\]>', '', s or '')
    s = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def parse_date(s):
    s = (s or '').strip()
    if not s:
        return None
    try:
        d = email.utils.parsedate_to_datetime(s)
    except (TypeError, ValueError, IndexError):
        try:
            d = dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
        except ValueError:
            # loose formats: "Friday, November 6, 2026 - 10:02", "Nov 9, 2026 11:35am", "9 November 2026"
            m = re.search(r'([A-Z][a-z]{2})[a-z]*\.? (\d{1,2}),? (20\d\d)', s) or re.search(r'(\d{1,2}) ([A-Z][a-z]{2})[a-z]* (20\d\d)', s)
            if not m:
                return None
            a, b, y = m.groups()
            mon, day = (a, b) if a[0].isalpha() else (b, a)
            try:
                d = dt.datetime(int(y), dt.datetime.strptime(mon[:3], '%b').month, int(day))
            except ValueError:
                return None
    return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)


def parse_feed(text):
    items = []
    for b in re.findall(r'<(?:item|entry)\b.*?</(?:item|entry)>', text, re.S):
        t = re.search(r'<title[^>]*>(.*?)</title>', b, re.S)
        d = re.search(r'<(pubDate|published|updated|dc:date)>(.*?)</\1>', b, re.S)
        l = re.search(r'<link>(.*?)</link>', b, re.S) or re.search(r'<link[^>]*href="([^"]+)"', b)
        desc = re.search(r'<(description|summary|content)[^>]*>(.*?)</\1>', b, re.S)
        if not t:
            continue
        items.append({'title': strip(t.group(1)), 'url': strip(l.group(1)) if l else '',
                      'date': parse_date(strip(d.group(2))) if d else None,
                      'summary': strip(desc.group(2))[:400] if desc else ''})
    return items


def page_lines(text):
    """Visible text of a page (or markdown), one meaningful line each, newest content usually first."""
    if '<html' in text[:2000].lower() or '<body' in text.lower():
        text = re.sub(r'(?is)<(script|style|noscript|svg|nav|footer|header)[^>]*>.*?</\1>', ' ', text)
        text = re.sub(r'(?i)<br\s*/?>|</(p|div|li|h\d|tr|section|article)>', '\n', text)
        text = html.unescape(re.sub(r'<[^>]+>', ' ', text))
    out = []
    for ln in text.split('\n'):
        ln = re.sub(r'\s+', ' ', ln).strip(' #*-|')
        if 20 <= len(ln) <= 500 and not re.search(r'\b\d+\s*(seconds?|minutes?|hours?|days?)\s+ago\b|cookie|subscribe|sign in|log in', ln, re.I):
            out.append(ln)
    return out[:600]


def h(s):
    return hashlib.sha1(re.sub(r'\W+', ' ', s.lower()).strip().encode()).hexdigest()[:10]


def in_window(d, since):
    return d is None or d >= since


def norm_title(t):
    return ' '.join(re.findall(r'[a-z0-9]+', t.lower())[:9])


def topics_for(text, source_topics=()):
    hits = [k for k, rx in TOPIC_WORDS.items() if re.search(rx, text, re.I)]
    both = [k for k in source_topics if k in hits]
    return (both or list(source_topics)[:1] or hits[:1] or ['business'])[:3]


# ---------------------------------------------------------------- sources
def collect_source(src, since):
    k = src['kind']
    url = src.get('url')
    if k == 'gnews':
        url = 'https://news.google.com/rss/search?q=%s+when:2d&hl=en-US&gl=US&ceid=US:en' % urllib.parse.quote_plus(src['query'])
    if k == 'page':
        return src, 0, []          # pages are handled as company updates (diffs)
    st, text = fetch(url)
    items = []
    if st != 200:
        return src, st, items
    try:
        if k in ('rss', 'gnews'):
            for n_item, it in enumerate(parse_feed(text)):
                if it['date'] is None and n_item >= 10:
                    continue          # undated feed: trust only the first (newest) items
                if not in_window(it['date'], since):
                    continue
                if k == 'gnews':
                    m = re.match(r'(.*) - ([^-]{2,60})$', it['title'])
                    if m:
                        it['title'], it['outlet'] = m.group(1).strip(), m.group(2).strip()
                if src.get('filter') == 'ai' and not re.search(r'\bAI\b|artificial intelligence|IndiaAI|machine learning|semiconductor', it['title'] + ' ' + it['summary'], re.I):
                    continue
                items.append(it)
        elif k == 'hn_front':
            for x in json.loads(text)['hits']:
                d = parse_date(x.get('created_at'))
                if in_window(d, since - dt.timedelta(hours=24)):
                    items.append({'title': x.get('title', ''), 'url': x.get('url') or 'https://news.ycombinator.com/item?id=%s' % x['objectID'],
                                  'date': d, 'summary': '', 'points': x.get('points') or 0, 'comments': x.get('num_comments') or 0,
                                  'discussion': 'https://news.ycombinator.com/item?id=%s' % x['objectID']})
        elif k in ('hf_new', 'hf_trending'):
            for m in json.loads(text):
                d = parse_date(m.get('createdAt'))
                likes = m.get('likes') or 0
                if k == 'hf_new' and likes < 3:
                    continue
                if k == 'hf_trending' and d and d < NOW - dt.timedelta(days=21):
                    continue
                items.append({'title': 'Hugging Face: %s (%d likes)' % (m['id'], likes), 'url': 'https://huggingface.co/' + m['id'],
                              'date': d, 'summary': m.get('pipeline_tag') or '', 'likes': likes})
        elif k == 'hf_papers':
            for p in json.loads(text)[:40]:
                pp = p.get('paper', p)
                items.append({'title': 'Paper: ' + strip(pp.get('title', '')), 'url': 'https://huggingface.co/papers/%s' % pp.get('id', ''),
                              'date': parse_date(pp.get('publishedAt')), 'summary': strip(pp.get('summary', ''))[:300], 'upvotes': pp.get('upvotes', 0)})
        elif k == 'openrouter':
            for m in json.loads(text)['data']:
                d = dt.datetime.fromtimestamp(m.get('created', 0), dt.timezone.utc)
                if d >= since - dt.timedelta(hours=24):
                    items.append({'title': 'OpenRouter lists %s (%s)' % (m.get('name', m['id']), m['id']), 'url': 'https://openrouter.ai/' + m['id'],
                                  'date': d, 'summary': strip(m.get('description', ''))[:300]})
        elif k == 'arxiv':
            for e in re.findall(r'<entry>(.*?)</entry>', text, re.S):
                t = strip(re.search(r'<title>(.*?)</title>', e, re.S).group(1))
                items.append({'title': 'arXiv: ' + t, 'url': strip(re.search(r'<id>(.*?)</id>', e).group(1)),
                              'date': parse_date(strip(re.search(r'<published>(.*?)</published>', e).group(1))),
                              'summary': strip(re.search(r'<summary>(.*?)</summary>', e, re.S).group(1))[:400]})
    except (ValueError, KeyError, AttributeError, TypeError) as e:
        return src, -1, []
    return src, st, items


# ---------------------------------------------------------------- company updates (changelog diffs)
def collect_update(company, upd, since, seen):
    key = '%s|%s' % (company['id'], upd['url'])
    st, text = fetch(upd['url'])
    if st != 200:
        return company['id'], upd, st, [], key, None
    if upd['kind'] == 'rss':
        new = [{'text': it['title'], 'url': it['url'], 'date': it['date'].date().isoformat() if it['date'] else ''}
               for it in parse_feed(text) if it['date'] and it['date'] >= since]
        return company['id'], upd, st, new[:12], key, None
    lines = page_lines(text)
    hashes = [h(x) for x in lines]
    old = seen.get(key)
    dated = dated_entries(lines, since)
    if old is None:   # first time we see this page: only entries dated inside the window count
        if dated:
            return company['id'], upd, st, [{'text': x[:300], 'url': upd['url'], 'date': d} for x, d in dated][:25], key, hashes
        return company['id'], upd, st, 'baseline', key, hashes
    oldset = set(old)
    dmap = {x: d for x, d in dated}
    new = [{'text': x[:300], 'url': upd['url'], 'date': dmap.get(x, '')} for x, hh in zip(lines, hashes) if hh not in oldset]
    return company['id'], upd, st, new[:25], key, hashes


MONTHS = 'jan feb mar apr may jun jul aug sep oct nov dec'.split()
DATE_RXS = [r'\b(?P<m>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.? (?P<d>\d{1,2}),? (?P<y>20\d\d)\b',
            r'\b(?P<d>\d{1,2}) (?P<m>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]* (?P<y>20\d\d)\b',
            r'\b(?P<y>20\d\d)[-./](?P<mn>\d{2})[-./](?P<d>\d{2})\b']


def dated_entries(lines, since):
    """Lines under a date heading that falls inside the window: (line, 'YYYY-MM-DD')."""
    out, cur, budget = [], None, 0
    for ln in lines:
        found = None
        for rx in DATE_RXS:
            m = re.search(rx, ln)
            if m:
                g = m.groupdict()
                mon = int(g['mn']) if g.get('mn') else MONTHS.index(g['m'][:3].lower()) + 1
                try:
                    found = dt.datetime(int(g['y']), mon, int(g['d']), 23, 59, tzinfo=dt.timezone.utc)
                except ValueError:
                    found = None
                break
        if found and found > NOW + dt.timedelta(days=1):
            found = None          # a future date inside an entry ("removal on Nov 30") is not the entry's date
        if found:
            cur, budget = (found if found >= since else None), 8
            if cur and len(ln) > 40:
                out.append((ln, cur.date().isoformat()))
            continue
        if cur and budget > 0:
            out.append((ln, cur.date().isoformat()))
            budget -= 1
    return out


# ---------------------------------------------------------------- reactions
def yt_search(query):
    # sp=EgIIAw== : uploaded this week; we then keep the last ~2 days
    st, text = fetch('https://www.youtube.com/results?search_query=%s&sp=EgIIAw%%3D%%3D' % urllib.parse.quote_plus(query))
    if st != 200:
        return st, []
    m = re.search(r'var ytInitialData = (\{.*?\});</script>', text, re.S)
    if not m:
        return st, []
    try:
        data = json.loads(m.group(1))
    except ValueError:
        return st, []
    vids = []

    def walk(o):
        if isinstance(o, dict):
            if 'videoRenderer' in o:
                v = o['videoRenderer']
                try:
                    vids.append({'title': v['title']['runs'][0]['text'], 'url': 'https://www.youtube.com/watch?v=' + v['videoId'],
                                 'channel': v.get('ownerText', {}).get('runs', [{}])[0].get('text', ''),
                                 'published': v.get('publishedTimeText', {}).get('simpleText', ''),
                                 'views': v.get('viewCountText', {}).get('simpleText', '')})
                except (KeyError, IndexError):
                    pass
            for x in o.values():
                walk(x)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(data)
    def age_hours(s):
        m = re.search(r'(\d+)\s*(s|sec|second|m|min|minute|h|hr|hour|d|day|w|wk|week|mo|month|y|yr|year)s?\b', s)
        if not m:
            return 1e9
        n, u = int(m.group(1)), m.group(2)
        return n * {'s': 0, 'sec': 0, 'second': 0, 'm': 1 / 60, 'min': 1 / 60, 'minute': 1 / 60, 'h': 1, 'hr': 1, 'hour': 1,
                    'd': 24, 'day': 24}.get(u, 1e6)
    recent = [v for v in vids if age_hours(v['published']) <= 48]

    def views(v):
        n = re.sub(r'[^\d]', '', v['views'])
        return int(n) if n else 0
    return st, sorted(recent, key=views, reverse=True)[:5]


REDDIT_LOCK = __import__('threading').Lock()


def reddit_top(sub):
    with REDDIT_LOCK:            # Reddit rate-limits parallel requests: one at a time, gently
        time.sleep(1.2)
        st, text = fetch('https://www.reddit.com/r/%s/top/.rss?t=day' % sub)
    if st != 200:
        return st, []
    return st, [{'title': it['title'], 'url': it['url'], 'sub': sub} for it in parse_feed(text)[:5]]


def hn_search(q, since):
    url = 'https://hn.algolia.com/api/v1/search?query=%s&tags=story&numericFilters=%s&hitsPerPage=8' % (
        urllib.parse.quote_plus(q), urllib.parse.quote('created_at_i>%d,points>10' % int(since.timestamp())))
    st, text = fetch(url)
    if st != 200:
        return st, []
    try:
        hits = json.loads(text)['hits']
    except (ValueError, KeyError):
        return st, []
    # Algolia also matches URLs, authors and story text; keep only stories whose title names the query,
    # otherwise unrelated front-page posts show up as "reactions" (e.g. paper airplanes under xAI)
    rx = re.compile(r'\b%s\b' % re.escape(q), re.I)
    hits = [x for x in hits if rx.search(x.get('title') or '')]
    return st, [{'title': x['title'], 'url': 'https://news.ycombinator.com/item?id=%s' % x['objectID'], 'points': x.get('points', 0),
                 'comments': x.get('num_comments', 0)} for x in sorted(hits, key=lambda x: -(x.get('points') or 0))[:4]]


# ---------------------------------------------------------------- trends
def phrases(title):
    out = set()
    for m in re.finditer(r"\b([A-Z][\w.\-']*(?:\s+(?:[A-Z][\w.\-']*|\d[\w.]*)){0,3})", title):
        p = m.group(1).strip(" .'-")
        words = p.split()
        while words and words[0].lower() in STOP:
            words = words[1:]
        while words and words[-1].lower() in STOP:
            words = words[:-1]
        if not words:
            continue
        p = re.sub(r"['’]s$", '', ' '.join(words))
        if len(p) >= 3 and p.lower() not in STOP and p.lower() not in GENERIC:
            out.add(p)
    for m in re.finditer(r'\b[A-Za-z][\w\-]*[ -]?\d+(?:\.\d+)+\b', title):   # versioned products: "Fable 5.2"
        out.add(m.group(0))
    return out


def domain(u):
    try:
        d = urllib.parse.urlparse(u).netloc.lower()
        return d[4:] if d.startswith('www.') else d
    except ValueError:
        return ''


# ---------------------------------------------------------------- main
def main():
    hours = 48
    if '--hours' in sys.argv:
        hours = int(sys.argv[sys.argv.index('--hours') + 1])
    since = NOW - dt.timedelta(hours=hours)
    date = (NOW + dt.timedelta(hours=5, minutes=30)).date().isoformat()   # IST
    out_dir = os.path.join(ROOT, '_working', 'collect', date)
    os.makedirs(out_dir, exist_ok=True)
    sources = json.load(open(CFG_SOURCES))['sources']
    cconf = json.load(open(CFG_COMPANIES))
    companies = cconf['companies']
    seen = json.load(open(COLLECT_STATE)) if os.path.exists(COLLECT_STATE) else {}
    t0 = time.time()

    # 1. sources
    stats, raw = {}, []
    with cf.ThreadPoolExecutor(16) as ex:
        for src, st, items in ex.map(lambda s: collect_source(s, since), sources):
            if src['kind'] == 'page':
                continue
            stats[src['id']] = {'name': src['name'], 'status': st, 'items': len(items)}
            for it in items:
                it['source'] = it.get('outlet') or src['name'] if src['kind'] == 'gnews' else src['name']
                it['sourceId'] = src['id']
                it['sourceTopics'] = src.get('topics', [])
                it['kind'] = src['kind']
                raw.append(it)
    log('sources: %d fetched, %d items, %.0fs' % (len(stats), len(raw), time.time() - t0))

    # dedupe by normalised title; merge sources
    cands = {}
    for it in raw:
        k = norm_title(it['title'])
        if not k:
            continue
        c = cands.get(k)
        if c is None:
            c = cands[k] = {'kind': it['kind'], 'title': it['title'], 'url': it['url'], 'date': it['date'], 'summary': it.get('summary', ''),
                            'sources': [], 'outlets': [], 'topics': topics_for(it['title'] + ' ' + it.get('summary', ''), it.get('sourceTopics', []))}
            for x in ('points', 'comments', 'discussion', 'likes', 'upvotes'):
                if x in it:
                    c[x] = it[x]
        if it['source'] not in c['sources']:
            c['sources'].append(it['source'])
        if it.get('outlet') and it['outlet'] not in c['outlets'] and it['outlet'] != it['source']:
            c['outlets'].append(it['outlet'])
        if it['kind'] == 'gnews':
            c.setdefault('queries', []).append(it['sourceId'])
        if it['date'] and (c['date'] is None or it['date'] > c['date']):
            c['date'] = it['date']
    cand = sorted(cands.values(), key=lambda c: (-(len(c['sources']) + len(c['outlets'])), -(c['date'].timestamp() if c['date'] else 0)))

    # 2. company updates (official) + mentions
    comp = {c['id']: {'name': c['name'], 'updates': [], 'mentions': [], 'reactions': [], 'baseline': [], 'failed': []} for c in companies}
    jobs = [(c, u) for c in companies for u in c.get('updates', [])]
    new_seen = dict(seen)
    with cf.ThreadPoolExecutor(12) as ex:
        for cid, upd, st, new, key, hashes in ex.map(lambda cu: collect_update(cu[0], cu[1], since, seen), jobs):
            if st != 200:
                comp[cid]['failed'].append('%s (%s)' % (upd['name'], st))
                continue
            if hashes is not None:
                new_seen[key] = hashes
            if new == 'baseline':
                comp[cid]['baseline'].append(upd['name'])
                continue
            for n in new:
                n['source'] = upd['name']
            comp[cid]['updates'] += new
    for c in companies:
        rx = [re.compile(r'(?<![\w-])%s(?![\w-])' % re.escape(a)) for a in c.get('aliases', [])]
        for x in cand:
            if any(r.search(x['title']) for r in rx):
                comp[c['id']]['mentions'].append({'title': x['title'], 'url': x['url'], 'sources': x['sources'] + x['outlets']})
    log('company updates: %d pages/feeds, %.0fs' % (len(jobs), time.time() - t0))

    # 3. reactions, for companies with something happening (plus the core set)
    core = {'anthropic', 'openai', 'google', 'meta', 'xai', 'x', 'tesla', 'spacex'}
    active = [c for c in companies if c['id'] in core or comp[c['id']]['updates'] or len(comp[c['id']]['mentions']) >= 2]
    reaction_status = {}
    if '--no-reactions' not in sys.argv:
        def react(c):
            r, got = c.get('reactions', {}), []
            if r.get('youtube'):
                st, vids = yt_search(r['youtube'])
                reaction_status['youtube'] = st
                got += [dict(v, kind='video') for v in vids[:3]]
                time.sleep(0.4)
            for sub in r.get('reddit', [])[:1]:
                st, posts = reddit_top(sub)
                reaction_status['reddit'] = st
                got += [dict(p, kind='reddit') for p in posts[:3]]
            for q in [q.strip().strip('"') for q in r.get('hn', '').split(' OR ')][:2]:
                if q:
                    st, hits = hn_search(q, since)
                    reaction_status['hn'] = st
                    got += [dict(x, kind='hn') for x in hits[:2]]
            return c['id'], got
        with cf.ThreadPoolExecutor(4) as ex:
            for cid, got in ex.map(react, active):
                seen_urls = set()
                comp[cid]['reactions'] = [g for g in got if not (g['url'] in seen_urls or seen_urls.add(g['url']))]
        for sub in cconf.get('reddit_global', []):
            st, posts = reddit_top(sub)
            comp.setdefault('_community', {'name': 'Community (global)', 'updates': [], 'mentions': [], 'reactions': [], 'baseline': [], 'failed': []})
            comp['_community']['reactions'] += [dict(p, kind='reddit') for p in posts[:4]]
    log('reactions: %d companies, %.0fs' % (len(active), time.time() - t0))

    # 4. what are we missing?
    known = []
    for c in companies:
        known += [c['name'], c['id']] + c.get('aliases', [])
    for s in sources:
        known.append(s['name'])
    if os.path.exists(SIGNAL_STATE):
        st_all = json.load(open(SIGNAL_STATE))
        for a, v in st_all.get('arcs', {}).items():
            known += [a.replace('-', ' '), v.get('label', ''), v.get('note', '')[:120]]
        for w in st_all.get('watchlist', []):
            known += [w.get('id', '').replace('-', ' '), w.get('query', '')]
        for s in st_all.get('stories', []):
            known.append(s.get('title', ''))
    known_blob = ' '.join(known).lower()
    counts = {}
    for x in cand:
        srcs = set(x['sources'] + x['outlets'])
        for p in phrases(x['title']):
            d = counts.setdefault(p, {'sources': set(), 'titles': []})
            d['sources'] |= srcs
            if len(d['titles']) < 3:
                d['titles'].append(x['title'])
    trends = [{'phrase': p, 'sources': len(d['sources']), 'examples': d['titles']}
              for p, d in counts.items() if len(d['sources']) >= 3 and p.lower() not in known_blob]
    trends.sort(key=lambda t: -t['sources'])
    known_out = set(s['name'].lower() for s in sources) | set(domain(s.get('url', '')) for s in sources)
    outlets = {}
    for x in cand:
        for o in x['outlets']:
            outlets[o] = outlets.get(o, 0) + 1
        if x.get('discussion'):
            d = domain(x['url'])
            if d and 'ycombinator' not in d:
                outlets[d] = outlets.get(d, 0) + 1
    for x in raw:
        if x.get('sourceId') == 'techmeme':
            m = re.search(r'\(([^()/]+)/([^()]+)\)\s*$', x['title'])
            if m:
                outlets[m.group(2).strip()] = outlets.get(m.group(2).strip(), 0) + 1
    suggested = sorted([(o, n) for o, n in outlets.items() if n >= 2 and o.lower() not in known_out
                        and not any(o.lower() in k for k in known_out) and o.lower() not in known_blob], key=lambda x: -x[1])[:20]
    # companies in the news but not in config/companies.json: named next to a launch/funding verb in 2+ outlets
    verbs = re.compile(r'\b(raises|raised|launch|launches|unveil|unveils|releases|debuts|acquires|acquired|startup|valuation|IPO|ships)\b', re.I)
    possible = []
    for ph, d in counts.items():
        if len(d['sources']) < 2 or ph.lower() in known_blob or len(ph) < 3:
            continue
        ex = [x for x in d['titles'] if verbs.search(x) and x.find(ph) <= 25]
        if ex:
            possible.append({'name': ph, 'sources': len(d['sources']), 'examples': ex[:2]})
    possible.sort(key=lambda c: -c['sources'])
    trend_out = {'unmapped': trends[:30], 'suggestedSources': [{'outlet': o, 'mentions': n} for o, n in suggested],
                 'possibleCompanies': possible[:25]}

    # 5. write
    def ser(o):
        if isinstance(o, dt.datetime):
            return o.astimezone(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
        if isinstance(o, set):
            return sorted(o)
        raise TypeError(type(o))
    json.dump(cand, open(os.path.join(out_dir, 'candidates.json'), 'w'), default=ser, indent=1, ensure_ascii=False)
    json.dump(comp, open(os.path.join(out_dir, 'companies.json'), 'w'), default=ser, indent=1, ensure_ascii=False)
    json.dump(trend_out, open(os.path.join(out_dir, 'trends.json'), 'w'), indent=1, ensure_ascii=False)
    failed = {k: v for k, v in stats.items() if v['status'] != 200}
    stat_out = {'generated': ser(NOW), 'windowHours': hours, 'sources': len(stats), 'sourcesOk': len(stats) - len(failed),
                'items': len(raw), 'candidates': len(cand), 'companiesActive': len(active), 'reactionStatus': reaction_status,
                'failed': failed, 'perSource': stats, 'seconds': round(time.time() - t0)}
    json.dump(stat_out, open(os.path.join(out_dir, 'stats.json'), 'w'), indent=1)
    json.dump(new_seen, open(COLLECT_STATE, 'w'), indent=0, sort_keys=True)
    write_digest(out_dir, date, stat_out, cand, comp, companies, trend_out, ser)
    print('collect: %s (%d sources ok of %d, %d candidates, %d companies active) in %ds' % (
        os.path.relpath(out_dir, ROOT), stat_out['sourcesOk'], len(stats), len(cand), len(active), stat_out['seconds']))


def write_digest(out_dir, date, stats, cand, comp, companies, trends, ser):
    L = ['# Collector digest — %s' % date, '',
         'Window: last %d hours. %d of %d sources answered; %d unique items. Nothing here is verified: open the source before carding.' % (
             stats['windowHours'], stats['sourcesOk'], stats['sources'], stats['candidates']), '']
    L += ['## Top stories by topic (most sources first)', '']
    for cat in CATEGORIES:
        topic = cat['id']
        rows = [c for c in cand if c['topics'][0] == topic and c['kind'] in ('rss', 'gnews')][:20]
        if rows:
            L += ['### %s (%s)' % (cat['label'], topic), '']
            for c in rows:
                n = len(set(c['sources'] + c['outlets']))
                L.append('- [%d src] %s — %s · %s %s' % (n, c['title'][:160], ', '.join((c['sources'] + c['outlets'])[:4]),
                                                        ser(c['date']) if c['date'] else 'undated', c['url']))
            L.append('')
    L += ['## Product updates by company', '',
          'Official = new since the last run on the company\'s changelog/newsroom. Mentions = headlines naming it. Reactions = what people are saying (not facts).', '']
    order = sorted([c for c in companies], key=lambda c: -(len(comp[c['id']]['updates']) * 3 + len(comp[c['id']]['mentions'])))
    for c in order:
        d = comp[c['id']]
        if not (d['updates'] or d['mentions'] or d['reactions']):
            continue
        L.append('### %s' % d['name'])
        for u in d['updates'][:12]:
            L.append('- OFFICIAL (%s) %s %s' % (u['source'], u['text'][:220], u['url']))
        for m in d['mentions'][:6]:
            L.append('- news: %s — %s' % (m['title'][:160], ', '.join(m['sources'][:3])))
        for r in d['reactions'][:8]:
            extra = ' · '.join(x for x in [r.get('channel', ''), r.get('views', ''), r.get('published', ''), ('%s pts' % r['points']) if r.get('points') else '', ('r/' + r['sub']) if r.get('sub') else ''] if x)
            L.append('- %s: %s (%s) %s' % (r['kind'], r['title'][:140], extra, r['url']))
        if d['baseline']:
            L.append('- (first run for: %s — recorded, nothing reported)' % ', '.join(d['baseline']))
        if d['failed']:
            L.append('- (failed: %s)' % ', '.join(d['failed']))
        L.append('')
    if comp.get('_community', {}).get('reactions'):
        L += ['### Community (global subreddits)'] + ['- reddit r/%s: %s %s' % (r['sub'], r['title'][:140], r['url']) for r in comp['_community']['reactions']] + ['']
    L += ['## Developer signals', '']
    for label, pref in [('Hacker News front page', None), ('Hugging Face', 'Hugging Face:'), ('OpenRouter', 'OpenRouter lists'), ('Papers', 'Paper:')]:
        if pref is None:
            rows = sorted([c for c in cand if 'points' in c], key=lambda c: -c['points'])[:15]
            L += ['### ' + label] + ['- %d pts: %s %s (discussion %s)' % (c['points'], c['title'][:140], c['url'], c.get('discussion', '')) for c in rows]
        else:
            rows = [c for c in cand if c['title'].startswith(pref)][:15]
            L += ['### ' + label] + ['- %s %s' % (c['title'][:160], c['url']) for c in rows]
        L.append('')
    L += ['## What are we missing?', '', 'Act on each: card it, add it to a category/watchlist/companies.json, add the source to sources.json, or say why not in runNotes.missing.', '',
          '### Unmapped trends (3+ sources, not matching any company, storyline, watchlist entry or recent story)']
    L += ['- %s (%d sources): e.g. %s' % (t['phrase'], t['sources'], ' | '.join(t['examples'][:2])[:220]) for t in trends['unmapped'][:25]] or ['- none']
    L += ['', '### Possibly missing from config/companies.json (named next to a launch, funding or acquisition)']
    L += ['- %s (%d sources): %s' % (c['name'], c['sources'], ' | '.join(c['examples'])[:220]) for c in trends.get('possibleCompanies', [])] or ['- none']
    L += ['', '### Outlets cited often but not in config/sources.json'] + (['- %s (%d)' % (s['outlet'], s['mentions']) for s in trends['suggestedSources']] or ['- none'])
    L += ['', '## Failed sources', ''] + (['- %s: %s' % (v['name'], v['status']) for v in stats['failed'].values()] or ['- none'])
    open(os.path.join(out_dir, 'digest.md'), 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
