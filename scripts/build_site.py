#!/usr/bin/env python3
"""Rebuild the site around the editions and check the newest one before it ships.

Run from the repo root after saving an edition:

    python3 scripts/build_site.py            # check the newest edition, rebuild everything
    python3 scripts/build_site.py --no-card  # skip the 1200x630 share image (needs Playwright)

It writes:
  index.html                 root page that redirects to the newest edition
  editions/index.html        archive: by month, missed dates, search, tap to expand
  editions/search-index.json every edition's stories, for archive search
  editions/cards/DATE.png    share image for the newest edition
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
STATE_RE = re.compile(r'<script id="signal-state"[^>]*>(.*?)</script>', re.S)
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
    if st.get('counts', {}).get('tracking') != len(st.get('tracking', [])):
        problems.append('counts.tracking does not match tracking[]')
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
    return problems


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
        print('checks passed: %s' % f)
    latest = build_archive(eds)
    build_root(latest)
    print('archive, search index and root redirect rebuilt (latest: %s)' % latest)
    if '--no-card' not in sys.argv and st.get('format') == 'v3':
        print('share card: %s' % build_card(date, f))


if __name__ == '__main__':
    main()
