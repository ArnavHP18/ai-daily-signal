#!/usr/bin/env python3
"""Rebuild the site around the editions and check the newest one before it ships.

Run from the repo root after saving an edition:

    python3 scripts/build_site.py            # check the newest edition, rebuild everything
    python3 scripts/build_site.py --no-card  # skip the 1200x630 share image (needs Playwright)

Bookkeeping lives in state/signal-state.json (tracking, watchlist, retired,
resolved, movers, held-back and no-change notes, run notes). Each edition page
embeds only what it renders (<script id="page-data">).

It writes:
  state/REVIEW.md            readable view of state/signal-state.json, for review
  index.html                 root page that redirects to the newest edition
  editions/index.html        archive: by month, missed dates, search, tap to expand
  editions/search-index.json every edition's stories, for archive search
  editions/cards/DATE.png    share image for the newest edition
  app/feed.json              swipe-view data for the newest edition (and editions/feeds/DATE.json)
and fills the byline / sister-site link slots from scripts/site_config.json.

It exits non-zero if the newest edition fails a check, so the routine must not
commit until this passes.
"""
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ED = os.path.join(ROOT, 'editions')
CFG = json.load(open(os.path.join(ROOT, 'scripts', 'site_config.json')))
NAME_RE = re.compile(r'^ai_daily_signal_(\d{4}-\d{2}-\d{2})\.html$')
STATE_RE = re.compile(r'<script id="(?:page-data|signal-state)"[^>]*>(.*?)</script>', re.S)
STATE_FILE = os.path.join(ROOT, 'state', 'signal-state.json')
VOID = {'meta', 'link', 'br', 'img', 'input', 'hr', 'wbr', 'source', 'col', 'area', 'base'}


def read_state(text):
    m = STATE_RE.search(text)
    return json.loads(m.group(1)) if m else None


def strip_tags(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


class TagCheck(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append('unexpected </%s> at line %d' % (tag, self.getpos()[0]))


def check_edition(path):
    """Return a list of problems with a v3 edition (empty list = ok)."""
    text = open(path).read()
    problems = []
    try:
        st = read_state(text)
    except json.JSONDecodeError as e:
        return ['signal-state JSON does not parse: %s' % e]
    if not st:
        return ['no signal-state JSON']
    tc = TagCheck()
    tc.feed(text)
    problems += tc.errors[:5]
    if tc.stack:
        problems.append('unclosed tags: %s' % tc.stack[-5:])

    stories = st.get('stories', [])
    ids = {s['id'] for s in stories}
    markup = re.sub(r'<script\b.*?</script>', '', text, flags=re.S)
    on_page = set(re.findall(r'data-story-id="([^"]+)"', markup))
    if ids - on_page:
        problems.append('stories with no card: %s' % sorted(ids - on_page))
    if on_page - ids:
        problems.append('cards with no story in state: %s' % sorted(on_page - ids))

    new = [s for s in stories if s.get('section') == 'new']
    if st.get('counts', {}).get('new') != len(new):
        problems.append('counts.new is %s but %d new stories' % (st.get('counts', {}).get('new'), len(new)))
    # the page and the state file must describe the same edition
    try:
        full = json.load(open(STATE_FILE))
    except (OSError, json.JSONDecodeError) as e:
        return problems + ['state/signal-state.json missing or invalid: %s' % e]
    if (full.get('edition'), full.get('date')) != (st.get('edition'), st.get('date')):
        problems.append('state file is edition %s (%s), page is %s (%s)' % (full.get('edition'), full.get('date'), st.get('edition'), st.get('date')))
    if {x['id'] for x in full.get('stories', [])} != ids:
        problems.append('stories in state file and page differ')
    if full.get('counts', {}).get('tracking') != len(full.get('tracking', [])):
        problems.append('counts.tracking does not match tracking[] in the state file')
    if 'tracking' in st or 'watchlist' in st:
        problems.append('page embeds tracking/watchlist; keep those in state/signal-state.json only')
    tiers = {'critical': 0, 'notable': 0, 'monitor': 0}
    for s in stories:
        tiers[s['tier']] += 1
    if st.get('tiers') != tiers:
        problems.append('tiers %s do not match stories %s' % (st.get('tiers'), tiers))

    # trust rules
    if not st.get('sourcesOpened') and not st.get('degraded'):
        problems.append('no sources opened but degraded is not set')
    ticker = re.search(r'<div class="ticker-inner">(.*?)</div>', text, re.S)
    for s in stories:
        if s.get('confidence') == 'Rumor-flag':
            el = re.search(r'<[^>]+data-story-id="%s"[^>]*>' % re.escape(s['id']), text)
            if el and 'rumor' not in el.group(0):
                problems.append('%s is unconfirmed but its card lacks the rumor style' % s['id'])
            if ticker and s.get('tickerKey') and s['tickerKey'].lower() in ticker.group(1).lower():
                problems.append('%s is unconfirmed but appears in the ticker' % s['id'])
        if s.get('new24h') and s.get('firstSeen') != st.get('date'):
            problems.append('%s has new24h but firstSeen is not today' % s['id'])
    if st.get('shareable') and (st.get('degraded') or not st.get('sourcesOpened')):
        problems.append('shareable is true on a degraded edition')

    # headline length
    h2 = re.search(r'<article class="hero"[^>]*>.*?<h2>(.*?)</h2>', text, re.S)
    if h2:
        words = len(strip_tags(h2.group(1)).split())
        if words > 16:
            problems.append('headline is %d words (limit about 15)' % words)
    else:
        problems.append('no hero headline')

    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith('http') and not re.match(r'https?://[^/\s]+\.[^/\s]+', href):
            problems.append('suspicious link: %s' % href)

    if st.get('date', '') >= SWIPE_SINCE:
        lead_id = h2 and re.search(r'<article class="hero"[^>]*data-story-id="([^"]+)"', text)
        problems += check_swipe_fields(stories, lead_id.group(1) if lead_id else None,
                                       {x['id']: x for x in full.get('stories', [])})
    return problems


SWIPE_SINCE = '2026-11-10'   # first edition written with swipe-card fields (ROUTINE.md §16a)


def check_swipe_fields(stories, lead_id, state_by_id):
    """Every swipe-deck story (the lead, plus Critical and Notable non-rumours) needs a card
    summary and a key number, in the page and in the state file; images must be credited https."""
    problems = []
    for s in stories:
        if s.get('confidence') == 'Rumor-flag':
            if s.get('image'):
                problems.append('%s is unconfirmed and must not carry a swipe image' % s['id'])
            continue
        on_deck = s['id'] == lead_id or s.get('tier') in ('critical', 'notable')
        if not on_deck:
            continue
        sid, short, stat, img = s['id'], s.get('short', ''), s.get('stat') or {}, s.get('image')
        if not short.strip():
            problems.append('%s is a swipe card but has no "short" summary' % sid)
        else:
            n = len(short.split())
            if n > 60:
                problems.append('%s "short" is %d words (limit 60)' % (sid, n))
            if n < 20:
                problems.append('%s "short" is only %d words (write 35-60)' % (sid, n))
            if '<' in short:
                problems.append('%s "short" must be plain text, not HTML' % sid)
        if not str(stat.get('value', '')).strip() or not str(stat.get('label', '')).strip():
            problems.append('%s is a swipe card but has no "stat" {value, label}' % sid)
        elif len(str(stat['value'])) > 9:
            problems.append('%s "stat" value "%s" is too long for the cover (9 characters max)' % (sid, stat['value']))
        if img is not None:
            if not str(img.get('url', '')).startswith('https://'):
                problems.append('%s "image" url must be https' % sid)
            if not str(img.get('credit', '')).strip():
                problems.append('%s "image" needs a credit (the official source)' % sid)
        st_s = state_by_id.get(sid, {})
        if (st_s.get('short'), st_s.get('stat'), st_s.get('image')) != (s.get('short'), s.get('stat'), s.get('image')):
            problems.append('%s swipe fields (short/stat/image) differ between page-data and state file' % sid)
    return problems


def build_review():
    """Write state/REVIEW.md: the bookkeeping from the state file, in reading order."""
    st = json.load(open(STATE_FILE))
    L = ['# AI Daily Signal — state review', '',
         'Generated by `scripts/build_site.py` from `state/signal-state.json` (edition %s, %s). Do not edit by hand.' % (st.get('edition'), st.get('date')), '']
    rn = st.get('runNotes', {})
    if rn:
        L += ['## Run notes', ''] + ['- **%s:** %s' % (k, v) for k, v in rn.items()] + ['']
    L += ['## Stories this edition', '']
    for x in st.get('stories', []):
        L.append('- #%s **%s** (%s, %s, %s): %s' % (x.get('rank'), x['id'], x['section'], x['tier'], x.get('verified', '?'), x['title']))
    for title, key in (('Held back (could not be checked)', 'heldBack'),):
        if st.get(key):
            L += ['', '## ' + title, ''] + ['- %s. Why: %s. Next: %s' % (h['item'], h['why'], h.get('next', '')) for h in st[key]]
    if st.get('noChange'):
        L += ['', '## Re-checked, no change', ''] + ['- ' + n for n in st['noChange']]
    if st.get('movers'):
        L += ['', '## Movers', ''] + ['- %s %s' % ('▲' if m['dir'] == 'up' else '▼', m['text']) for m in st['movers']]
    tr = st.get('tracking', [])
    due = sorted(tr, key=lambda t: (t.get('lastChecked', '0000'), t.get('since', '')))[:10]
    L += ['', '## Next to re-check (10 oldest lastChecked)', ''] + ['- %s (since %s, checked %s): %s' % (t['id'], t.get('since', '?'), t.get('lastChecked', 'never'), t['label']) for t in due]
    L += ['', '## Watchlist', ''] + ['- **%s** [%s, checked %s]: %s' % (w['id'], w.get('status'), w.get('lastChecked'), w['label'][-300:]) for w in st.get('watchlist', [])]
    if st.get('resolved'):
        L += ['', '## Resolved this edition', ''] + ['- ' + r for r in st['resolved']]
    if st.get('retired'):
        L += ['', '## Retired this edition', ''] + ['- %s: %s' % (r['id'], r['reason']) for r in st['retired']]
    L += ['', '## Still tracking (%d, newest first)' % len(tr), '']
    for t in sorted(tr, key=lambda t: (t.get('since', ''), t.get('lastChecked', '')), reverse=True):
        L.append('- %s (since %s%s): %s' % (t['id'], t.get('since', '?'), (', checked ' + t['lastChecked']) if t.get('lastChecked') else '', t['label']))
    open(os.path.join(ROOT, 'state', 'REVIEW.md'), 'w').write('\n'.join(L) + '\n')


def editions():
    out = []
    for f in sorted(os.listdir(ED)):
        m = NAME_RE.match(f)
        if m:
            out.append((m.group(1), f))
    return out


def lead_of(text):
    h2 = re.search(r'<article class="hero"[^>]*>.*?<h2>(.*?)</h2>', text, re.S)
    sub = re.search(r'<p class="subhead">(.*?)</p>', text, re.S)
    return (strip_tags(h2.group(1)) if h2 else ''), (strip_tags(sub.group(1)) if sub else '')


def old_index_entries():
    """Keep the hand-written lead/summary lines from the existing archive page."""
    p = os.path.join(ED, 'index.html')
    if not os.path.exists(p):
        return {}
    keep = {}
    for li in re.findall(r'<li[^>]*>(.*?)</li>', open(p).read(), re.S):
        href = re.search(r'href="(ai_daily_signal_[^"]+\.html)"', li)
        if not href:
            continue
        lead = re.search(r'<span class="lead">\s*<a[^>]*>(.*?)</a>', li, re.S)
        sub = re.search(r'<(?:span|div) class="sub">(.*?)</(?:span|div)>', li, re.S)
        crit = re.search(r'class="crit">([^<]*)<', li)
        keep[href.group(1)] = {'lead': lead.group(1).strip() if lead else '',
                               'sub': sub.group(1).strip() if sub else '',
                               'crit': crit.group(1).strip() if crit else ''}
    return keep


def fill_slots(path):
    text = open(path).read()
    links = CFG.get('curator_links', {})
    parts = [' · <a href="%s">%s</a>' % (html.escape(u), n) for n, u in (('LinkedIn', links.get('linkedin')), ('X', links.get('x'))) if u]
    sisters = [' · <a href="%s">%s</a>' % (html.escape(s['url']), html.escape(s['name'])) for s in CFG.get('sister_sites', []) if s.get('url')]
    new = re.sub(r'<span data-slot="curator-links">.*?</span>', '<span data-slot="curator-links">%s</span>' % ''.join(parts), text)
    new = re.sub(r'<span data-slot="sister-links">.*?</span>', '<span data-slot="sister-links">%s</span>' % ''.join(sisters), new)
    if new != text:
        open(path, 'w').write(new)


def build_archive(eds):
    keep = old_index_entries()
    rows, search = {}, []
    for date, f in eds:
        text = open(os.path.join(ED, f)).read()
        try:
            st = read_state(text) or {}
        except json.JSONDecodeError:
            st = {}
        lead, sub = lead_of(text)
        k = keep.get(f, {})
        lead = lead or k.get('lead', '') or f
        sub = sub or k.get('sub', '')  # a v3 page's own sub-line wins over the old hand-written one
        crit = st.get('tiers', {}).get('critical')
        crit_txt = ('%d CRITICAL' % crit) if crit is not None else k.get('crit', '')
        num = st.get('edition')
        rows.setdefault(date, []).append({'file': f, 'lead': lead, 'sub': sub, 'crit': crit_txt,
                                          'num': ('%03d' % num) if isinstance(num, int) else '',
                                          'catchup': st.get('editionType') == 'catch-up',
                                          'degraded': bool(st.get('degraded'))})
        search.append({'date': date, 'file': f, 'edition': num, 'lead': strip_tags(lead),
                       'stories': [s.get('title', '')[:160] for s in st.get('stories', [])]})
    json.dump(search, open(os.path.join(ED, 'search-index.json'), 'w'), ensure_ascii=False, separators=(',', ':'))

    first = dt.date.fromisoformat(CFG.get('first_edition_date', eds[0][0]))
    last = dt.date.fromisoformat(eds[-1][0])
    months, d = {}, last
    while d >= first:
        key = d.strftime('%Y-%m')
        ds = d.isoformat()
        if ds in rows:
            for r in sorted(rows[ds], key=lambda r: r['num'], reverse=True):
                months.setdefault(key, []).append((ds, r))
        else:
            months.setdefault(key, []).append((ds, None))
        d -= dt.timedelta(days=1)

    out = []
    for i, (key, items) in enumerate(months.items()):
        label = dt.date.fromisoformat(key + '-01').strftime('%B %Y')
        n_ed = sum(1 for _, r in items if r)
        n_miss = sum(1 for _, r in items if not r)
        out.append('<details class="month"%s><summary><span>%s</span><small>%d editions%s</small></summary><ol>' %
                   (' open' if i == 0 else '', label, n_ed, (' · %d missed' % n_miss) if n_miss else ''))
        for ds, r in items:
            day = dt.date.fromisoformat(ds).strftime('%a %d %b')
            if not r:
                out.append('<li class="missing"><span class="date">%s</span><span class="lead">No edition</span></li>' % day)
                continue
            flags = ''.join(f for f, on in (('<span class="flag">CATCH-UP</span>', r['catchup']), ('<span class="flag deg">DEGRADED</span>', r['degraded'])) if on)
            sub = '<div class="sub">%s</div>' % r['sub'] if r['sub'] else ''
            out.append('<li><span class="date">%s%s</span><span class="crit">%s</span>%s<span class="lead"><a href="%s">%s</a></span>%s</li>' %
                       (day, (' · #' + r['num']) if r['num'] else '', html.escape(r['crit']), flags, r['file'], r['lead'], sub))
        out.append('</ol></details>')

    latest = eds[-1][1]
    page = ARCHIVE % {'months': '\n'.join(out), 'latest': latest, 'count': len(eds),
                      'site': html.escape(CFG['site_url']), 'curator': html.escape(CFG['curator'])}
    open(os.path.join(ED, 'index.html'), 'w').write(page)
    return latest


TRUST_LABEL = {'Primary': ('official', 'Official source'), '2x src': ('multi', 'Two or more outlets'),
               'Agg 1x': ('single', 'One secondary source'), 'Rumor-flag': ('rumor', 'Unconfirmed')}
TIER_RANK = {'critical': 0, 'notable': 1, 'monitor': 2}


def element_html(text, sid):
    """Inner HTML of the article/details element carrying data-story-id=sid (first match outside scripts)."""
    m = re.search(r'<(article|details)\b[^>]*data-story-id="%s"[^>]*>' % re.escape(sid), text)
    if not m:
        return ''
    tag, depth, i = m.group(1), 1, m.end()
    for t in re.finditer(r'<(/?)%s\b[^>]*>' % tag, text[i:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return text[i:i + t.start()]
    return ''


def first_words(s, lo=35, hi=62):
    """Plain-text summary: whole sentences up to about hi words, else a cut at hi words."""
    words, out = s.split(), []
    for w in words:
        out.append(w)
        if len(out) >= lo and re.search(r'[.!?]["”’)]?$', w):
            break
        if len(out) >= hi:
            return ' '.join(out).rstrip(',;:') + '…'
    return ' '.join(out)


def story_feed_item(text, s, date):
    """One story as plain data for the swipe app, read from its card on the edition page."""
    el = element_html(text, s['id'])
    head = re.search(r'<h[24]>(.*?)</h[24]>', el, re.S)
    sub = re.search(r'<p class="sub(?:head)?">(.*?)</p>', el, re.S)
    sowhat = re.search(r'<p class="sowhat">(.*?)</p>', el, re.S)
    chip = re.search(r'<span class="chip">(.*?)</span>', el, re.S)
    srcs = re.search(r'<div class="src">.*?</div>(?=\s*<div class="storyline"|\s*$)', el, re.S)
    storyline = re.search(r'<div class="storyline">(.*?)</div>', el, re.S)
    # detail = the card's prose (dek/body/paragraphs), minus the so-what line and chrome
    detail = ''.join(re.findall(r'<(?:p|div) class="(?:dek|body)">.*?</(?:p|div)>|<p>.*?</p>', el, re.S))
    if not detail:
        detail = ''.join(re.findall(r'<p(?: class="dek")?>.*?</p>', el, re.S))
    prose = strip_tags(re.sub(r'<div class="delta-line">.*?</div>', '', detail, flags=re.S))
    kind, label = TRUST_LABEL.get(s.get('confidence'), ('single', 'One secondary source'))
    sw = strip_tags(sowhat.group(1)) if sowhat else ''
    sw = re.sub(r'^So what:\s*', '', sw)
    sw = sw[:1].upper() + sw[1:]
    return {
        'id': s['id'], 'section': s['section'], 'rank': s.get('rank'), 'tier': s['tier'], 'impact': s.get('impact'),
        'category': s.get('category', ''), 'delta': s.get('delta', 'new'), 'new24h': bool(s.get('new24h')),
        'trust': kind, 'trustLabel': label, 'rumor': s.get('confidence') == 'Rumor-flag', 'verified': s.get('verified', ''),
        'headline': strip_tags(head.group(1)) if head else s['title'][:120],
        'sub': strip_tags(sub.group(1)) if sub else '',
        'summary': s.get('short') or first_words(prose or s['title']),
        'whyItMatters': sw,
        'update': s.get('update', ''),
        'checked': strip_tags(chip.group(1)) if chip else '',
        'storyline': ' · '.join(strip_tags(storyline.group(1)).split(' · ')[:2]) if storyline else '',
        'detailHtml': re.sub(r'<p class="sowhat">.*?</p>', '', detail, flags=re.S).strip(),
        'sourcesHtml': srcs.group(0) if srcs else '',
        'url': '../editions/ai_daily_signal_%s.html#%s' % (date, s['id']),
        'stat': s.get('stat') or None,     # {value, label}: key number for the generated cover
        'image': s.get('image') if (s.get('image') or {}).get('url', '').startswith('https://') else None,  # {url, credit}: official source image
    }


def build_feed(date, f):
    """Write editions/feeds/DATE.json and app/feed.json (newest) for the swipe app."""
    text = open(os.path.join(ED, f)).read()
    st = read_state(text)
    if not st or st.get('format') != 'v3':
        return None
    hero = re.search(r'<article class="hero"[^>]*data-story-id="([^"]+)"', text)
    lead_id = hero.group(1) if hero else None
    items = [story_feed_item(text, s, date) for s in st.get('stories', [])]
    by_id = {i['id']: i for i in items}
    lead = by_id.get(lead_id)
    rest = [i for i in items if i is not lead]
    full = [i for i in rest if i['tier'] in ('critical', 'notable') and not i['rumor']]
    full.sort(key=lambda i: (TIER_RANK[i['tier']], i['section'] != 'new', i.get('rank') or 99))
    also = [i for i in rest if i not in full]
    also.sort(key=lambda i: (i['rumor'], i['section'] != 'new', i.get('rank') or 99))
    d = dt.date.fromisoformat(date)
    feed = {
        'format': 'feed-v1', 'site': CFG['site_name'], 'edition': st.get('edition'), 'date': date,
        'longDate': d.strftime('%A, ') + str(d.day) + d.strftime(' %B %Y'),
        'editionType': st.get('editionType', 'daily'), 'degraded': bool(st.get('degraded')),
        'degradedReason': st.get('degradedReason', ''), 'shareable': bool(st.get('shareable')),
        'counts': st.get('counts', {}), 'sourcesOpened': st.get('sourcesOpened'),
        'editionUrl': '../editions/' + f, 'archiveUrl': '../editions/index.html',
        'shareUrl': '%s/editions/%s' % (CFG['site_url'], f),
        'deck': ([lead] if lead else []) + full, 'alsoToday': also,
    }
    os.makedirs(os.path.join(ED, 'feeds'), exist_ok=True)
    data = json.dumps(feed, ensure_ascii=False, indent=1)
    open(os.path.join(ED, 'feeds', date + '.json'), 'w').write(data)
    os.makedirs(os.path.join(ROOT, 'app'), exist_ok=True)
    open(os.path.join(ROOT, 'app', 'feed.json'), 'w').write(data)
    return feed


SWIPE_LINK = '<a class="swipe-link" href="../app/" style="display:inline-block;margin-top:8px;font-family:var(--mono);font-size:12px;letter-spacing:1px;border:1px solid var(--rule);border-radius:999px;padding:4px 12px">📱 SWIPE VIEW</a>'


def add_swipe_link(path):
    """Put a link to the swipe app under the masthead byline (idempotent)."""
    text = open(path).read()
    if 'class="swipe-link"' in text:
        return
    new = re.sub(r'(<div class="byline">.*?</div>)', lambda m: m.group(1) + '\n  ' + SWIPE_LINK, text, count=1, flags=re.S)
    if new != text:
        open(path, 'w').write(new)


def build_root(latest):
    page = ROOT_PAGE % {'latest': latest, 'site': html.escape(CFG['site_url'])}
    open(os.path.join(ROOT, 'index.html'), 'w').write(page)


def build_card(date, f):
    text = open(os.path.join(ED, f)).read()
    st = read_state(text)
    lead, sub = lead_of(text)
    os.makedirs(os.path.join(ED, 'cards'), exist_ok=True)
    out = os.path.join(ED, 'cards', date + '.png')
    when = dt.date.fromisoformat(date).strftime('%A %d %B %Y')
    card = CARD % {'lead': html.escape(lead), 'sub': html.escape(sub), 'when': when, 'ed': st.get('edition', ''),
                   'logo': open(os.path.join(ROOT, 'assets', 'logo.svg')).read(),
                   'status': html.escape('%d stories' % st['counts']['new'])}
    tmp = os.path.join(ED, 'cards', '.card.html')
    open(tmp, 'w').write(card)
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();"
          "const p=await b.newPage({viewport:{width:1200,height:630}});await p.goto('file://'+process.argv[1]);"
          "await p.waitForTimeout(600);await p.screenshot({path:process.argv[2]});await b.close();})()"
          ".catch(e=>{console.error(e);process.exit(1)})")
    try:
        subprocess.run(['node', '-e', js, tmp, out], check=True, cwd='/tmp')
    finally:
        os.remove(tmp)
    return out


ARCHIVE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Daily Signal — All Editions</title>
<meta name="description" content="Every edition of AI Daily Signal, a daily briefing on new AI advances, curated by %(curator)s.">
<meta property="og:title" content="AI Daily Signal — All Editions">
<meta property="og:type" content="website">
<meta property="og:url" content="%(site)s/editions/index.html">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Inter:wght@400;600&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root{--ink:#16140f;--paper:#f5f1e8;--paper2:#ece6d8;--rule:#c9c0ac;--crit:#b3261e;--accent:#1f3a93;--muted:#6b6353}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--paper);color:var(--ink);font-family:'Inter',sans-serif;max-width:860px;margin:0 auto;padding:32px 16px 60px}
  a{color:var(--accent);text-decoration:none}
  header{border-bottom:4px double var(--ink);padding-bottom:12px;display:flex;align-items:center;gap:14px}
  header img{width:46px;height:46px}
  h1{font-family:'Fraunces',serif;font-weight:800;font-size:clamp(30px,6vw,42px);text-transform:uppercase;letter-spacing:-1px;line-height:1}
  .tag{font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:1px;color:var(--muted);margin:10px 0 18px}
  .latest{display:inline-block;margin-bottom:18px;font-weight:600}
  #q{width:100%%;font:inherit;font-size:16px;padding:10px 12px;border:1px solid var(--rule);background:#fffdf7;margin-bottom:6px}
  #qinfo{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--muted);min-height:16px;margin-bottom:12px}
  details.month{border-bottom:1px solid var(--rule)}
  details.month > summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:baseline;padding:14px 0;font-family:'Fraunces',serif;font-size:22px;font-weight:600}
  details.month > summary::-webkit-details-marker{display:none}
  details.month > summary small{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--muted);font-weight:400}
  details.month > summary::after{content:"▾";font-size:14px;color:var(--muted);margin-left:10px}
  details.month[open] > summary::after{content:"▴"}
  ol{list-style:none}
  li{border-top:1px solid var(--rule);padding:14px 0;display:flex;gap:6px 16px;align-items:baseline;flex-wrap:wrap;cursor:pointer}
  li.missing{cursor:default;color:var(--muted);padding:8px 0}
  li.missing .lead{font-style:italic;font-size:14px}
  .date{font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:600;min-width:130px}
  .crit{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--crit);min-width:84px}
  .flag{font-family:'IBM Plex Mono',monospace;font-size:10px;background:#d99a00;color:var(--ink);padding:1px 6px}
  .flag.deg{background:#fff1c7;border:1px solid #d99a00}
  .lead{flex:1 1 380px;min-width:0}
  .lead a{font-family:'Fraunces',serif;font-size:18px;font-weight:600;line-height:1.3}
  .sub{flex:1 1 100%%;font-size:14px;line-height:1.55;color:#4a4436;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  li.open .sub{-webkit-line-clamp:unset;overflow:visible}
  li .hit{flex:1 1 100%%;font-size:13px;color:var(--muted)}
  mark{background:#ffd166}
  footer{margin-top:30px;font-size:13px;color:var(--muted)}
</style>
</head>
<body>
<header><img src="../assets/logo.svg" alt=""><div><h1>AI Daily Signal</h1></div></header>
<div class="tag">ALL %(count)s EDITIONS · NEWEST FIRST · IST · CURATED BY %(curator)s</div>
<a class="latest" href="%(latest)s">Read the latest edition →</a>
<input id="q" type="search" placeholder="Search every edition (company, model, topic…)" aria-label="Search every edition">
<div id="qinfo"></div>
<div id="months">
%(months)s
</div>
<footer>Tap an entry to see its full summary. Dates with no edition are listed so gaps are visible.</footer>
<script>
(function(){
  // tap to expand (works on phones; hover does not)
  document.querySelectorAll('li:not(.missing)').forEach(function(li){
    li.addEventListener('click', function(e){ if(e.target.tagName !== 'A') li.classList.toggle('open'); });
  });
  var idx = null, q = document.getElementById('q'), info = document.getElementById('qinfo');
  var rows = Array.prototype.slice.call(document.querySelectorAll('li:not(.missing)'));
  var byFile = {}; rows.forEach(function(li){ var a = li.querySelector('.lead a'); if(a) byFile[a.getAttribute('href')] = li; });
  fetch('search-index.json').then(function(r){ return r.json(); }).then(function(j){ idx = j; }).catch(function(){});
  var esc = function(s){ return s.replace(/[&<>]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]; }); };
  q.addEventListener('input', function(){
    var term = q.value.trim().toLowerCase();
    document.querySelectorAll('li .hit').forEach(function(h){ h.remove(); });
    if(!term){ document.querySelectorAll('li').forEach(function(li){ li.style.display = ''; }); info.textContent = ''; return; }
    var n = 0;
    document.querySelectorAll('li.missing').forEach(function(li){ li.style.display = 'none'; });
    rows.forEach(function(li){
      var a = li.querySelector('.lead a'), file = a ? a.getAttribute('href') : '';
      var text = li.textContent.toLowerCase(), hits = [];
      if(idx){ idx.forEach(function(e){ if(e.file === file){ e.stories.forEach(function(s){ if(s.toLowerCase().indexOf(term) > -1) hits.push(s); }); } }); }
      var show = text.indexOf(term) > -1 || hits.length > 0;
      li.style.display = show ? '' : 'none';
      if(show){
        n++;
        var d = li.closest('details'); if(d) d.open = true;
        if(hits.length){ var h = document.createElement('div'); h.className = 'hit'; h.innerHTML = '↳ ' + hits.slice(0,3).map(esc).join(' · '); li.appendChild(h); }
      }
    });
    info.textContent = n + (n === 1 ? ' edition matches' : ' editions match') + (idx ? '' : ' (headlines only; full-text index not loaded)');
  });
})();
</script>
</body>
</html>
'''

ROOT_PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Daily Signal</title>
<meta http-equiv="refresh" content="0; url=editions/%(latest)s">
<link rel="canonical" href="%(site)s/editions/%(latest)s">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<meta property="og:title" content="AI Daily Signal">
<meta property="og:description" content="A daily briefing on new AI advances.">
<meta property="og:url" content="%(site)s/">
<style>body{font-family:system-ui,sans-serif;background:#f5f1e8;color:#16140f;padding:40px 16px;text-align:center}a{color:#1f3a93}</style>
</head>
<body>
<p>Opening the latest edition… <a href="editions/%(latest)s">Continue</a> · <a href="editions/index.html">All editions</a></p>
<script>location.replace('editions/%(latest)s');</script>
</body>
</html>
'''

CARD = '''<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,800&family=Inter:wght@400;600&family=IBM+Plex+Mono:wght@600&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#f5f1e8;color:#16140f;font-family:Inter,sans-serif;padding:56px 64px;display:flex;flex-direction:column;border-bottom:18px solid #16140f}
.top{display:flex;align-items:center;gap:18px;font-family:'IBM Plex Mono',monospace;font-size:22px;letter-spacing:3px;text-transform:uppercase}
.top svg{width:64px;height:64px}
.top b{font-family:Fraunces,serif;font-size:34px;letter-spacing:-0.5px}
h1{font-family:Fraunces,serif;font-weight:800;font-size:60px;line-height:1.07;margin-top:44px;flex:1}
p{font-size:26px;line-height:1.4;color:#3a352a;margin-top:18px;max-height:110px;overflow:hidden}
.foot{font-family:'IBM Plex Mono',monospace;font-size:20px;color:#6b6353;margin-top:24px;letter-spacing:1px}
</style></head><body>
<div class="top">%(logo)s<b>AI DAILY SIGNAL</b></div>
<h1>%(lead)s</h1>
<p>%(sub)s</p>
<div class="foot">EDITION %(ed)s · %(when)s</div>
</body></html>'''


def main():
    eds = editions()
    if not eds:
        sys.exit('no editions found')
    date, f = eds[-1]
    path = os.path.join(ED, f)
    st = read_state(open(path).read()) or {}
    if st.get('format') == 'v3':
        problems = check_edition(path)
        if problems:
            print('NEWEST EDITION FAILS CHECKS:', *problems, sep='\n  - ')
            sys.exit(1)
        fill_slots(path)
        add_swipe_link(path)
        print('checks passed: %s' % f)
        feed = build_feed(date, f)
        print('swipe feed: app/feed.json and editions/feeds/%s.json (%d cards, %d also today)' % (date, len(feed['deck']), len(feed['alsoToday'])))
    if os.path.exists(STATE_FILE):
        build_review()
        print('state/REVIEW.md rebuilt')
    latest = build_archive(eds)
    build_root(latest)
    print('archive, search index and root redirect rebuilt (latest: %s)' % latest)
    if '--no-card' not in sys.argv and st.get('format') == 'v3':
        print('share card: %s' % build_card(date, f))


if __name__ == '__main__':
    main()
