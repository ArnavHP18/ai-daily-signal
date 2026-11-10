"""Pipeline v4 pieces used by build_site.py: state upkeep, data-file checks (including the
next-day accuracy check), storyline pages and the quality log."""
import datetime as dt
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ED = os.path.join(ROOT, 'editions')
DATA = os.path.join(ED, 'data')
STATE_FILE = os.path.join(ROOT, 'state', 'signal-state.json')
ARCHIVE_DIR = os.path.join(ROOT, 'state', 'archive')
QUALITY_FILE = os.path.join(ROOT, 'state', 'quality.json')
DATA_SINCE = '2026-11-10'          # first edition written as editions/data/DATE.json
TRACKING_DAYS = 14                 # tracked items with no check or movement for this long are archived
WATCHLIST_DAILY_MAX = 20
FOLLOWUP_STATUSES = ('confirmed', 'changed', 'corrected', 'unresolved', 'quiet')


def esc(s):
    return html.escape(str(s), quote=False)


def load_data(date):
    p = os.path.join(DATA, date + '.json')
    return json.load(open(p)) if os.path.exists(p) else None


def prev_data_date(date):
    if not os.path.isdir(DATA):
        return None
    ds = sorted(f[:-5] for f in os.listdir(DATA) if re.match(r'\d{4}-\d{2}-\d{2}\.json$', f) and f[:-5] < date)
    return ds[-1] if ds else None


# ---------------------------------------------------------------- state upkeep
def maintain_state(date):
    """Archive stale tracking items, keep the watchlist to <=20 daily entries, compact long labels.
    Returns a one-line summary. Idempotent."""
    st = json.load(open(STATE_FILE))
    cutoff = (dt.date.fromisoformat(date) - dt.timedelta(days=TRACKING_DAYS)).isoformat()
    keep, gone = [], []
    for t in st.get('tracking', []):
        last = max(t.get('since') or '0', t.get('lastChecked') or '0')
        (keep if last >= cutoff else gone).append(t)
    if gone:
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        ap = os.path.join(ARCHIVE_DIR, 'tracking.json')
        arch = json.load(open(ap)) if os.path.exists(ap) else []
        for t in gone:
            t['archived'] = date
            t['archiveReason'] = 'no check or movement for %d days' % TRACKING_DAYS
        json.dump(arch + gone, open(ap, 'w'), indent=0, ensure_ascii=False)
    st['tracking'] = keep
    st.setdefault('counts', {})['tracking'] = len(keep)

    wl = st.get('watchlist', [])
    for w in wl:
        lab = w.get('label', '')
        if len(lab) > 1600:   # labels grow by one note per run: keep the definition and the latest notes
            w['label'] = lab[:450].rsplit(' ', 1)[0] + ' … ' + lab[-900:].split(' ', 1)[-1]
    if any('cadence' not in w for w in wl):
        def activity(w):
            tail = w.get('label', '')[-900:]
            carded = [m for m in re.findall(r'(\d{1,2}) (Oct|Nov|Dec) [^.]{0,40}?CARDED', tail)]
            last = max([(('10' if m[1] == 'Oct' else '11' if m[1] == 'Nov' else '12'), int(m[0])) for m in carded], default=('00', 0))
            return (last, w.get('firstSeen', ''))
        ranked = sorted(wl, key=activity, reverse=True)
        daily = {id(w) for w in ranked[:WATCHLIST_DAILY_MAX]}
        for w in wl:
            w.setdefault('cadence', 'daily' if id(w) in daily else 'weekly')
    json.dump(st, open(STATE_FILE, 'w'), indent=1, ensure_ascii=False)
    n_daily = sum(1 for w in wl if w.get('cadence') == 'daily')
    return 'tracking %d (archived %d older than %d days); watchlist %d daily, %d weekly' % (
        len(keep), len(gone), TRACKING_DAYS, n_daily, len(wl) - n_daily)


# ---------------------------------------------------------------- data-file checks
def check_data(date, page_state):
    """Problems with the edition's data file, the next-day accuracy check and v4 bookkeeping."""
    if date < DATA_SINCE:
        return []
    d = load_data(date)
    if d is None:
        return ['editions/data/%s.json is missing (write the data file, then run scripts/render.py)' % date]
    p = []
    if {s['id']: s['title'] for s in d['stories']} != {s['id']: s['title'] for s in page_state.get('stories', [])}:
        p.append('the page does not match editions/data/%s.json: run python3 scripts/render.py %s' % (date, date))
    # next-day accuracy check: every Critical/Notable story of the previous edition gets a follow-up
    prev = prev_data_date(date)
    if prev:
        pd = load_data(prev)
        due = [s['id'] for s in pd['stories'] if s['tier'] in ('critical', 'notable')]
        got = {f.get('id'): f for f in d.get('followups', [])}
        for sid in due:
            f = got.get(sid)
            if not f:
                p.append('followups: no entry for %s (a %s story on %s)' % (sid, 'Critical/Notable', prev))
            elif f.get('status') not in FOLLOWUP_STATUSES:
                p.append('followups: %s status must be one of %s' % (sid, ', '.join(FOLLOWUP_STATUSES)))
            elif not f.get('note'):
                p.append('followups: %s needs a note saying what the re-check found' % sid)
        if any(f.get('status') == 'corrected' for f in d.get('followups', [])) and not d.get('corrections'):
            p.append('a follow-up is "corrected" but corrections[] is empty (the footer must say what changed)')
    st = json.load(open(STATE_FILE))
    if 'missing' not in st.get('runNotes', {}):
        p.append('runNotes.missing is required: what the run did with the collector\'s "what are we missing" list')
    n_daily = sum(1 for w in st.get('watchlist', []) if w.get('cadence') == 'daily')
    if n_daily > WATCHLIST_DAILY_MAX:
        p.append('watchlist has %d daily entries (max %d): set the quietest to "weekly"' % (n_daily, WATCHLIST_DAILY_MAX))
    return p


# ---------------------------------------------------------------- storylines
def headline_of(text, sid):
    m = re.search(r'<(article|details)\b[^>]*data-story-id="%s"[^>]*>.*?<h[24]>(.*?)</h[24]>' % re.escape(sid), text, re.S)
    return html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip() if m else ''


def build_storylines(eds, read_state):
    st = json.load(open(STATE_FILE))
    arcs = st.get('arcs', {})
    entries = {}
    for date, f in eds:
        text = open(os.path.join(ED, f)).read()
        ps = read_state(text) or {}
        for s in ps.get('stories', []):
            if not s.get('arc'):
                continue
            entries.setdefault(s['arc'], []).append({
                'date': date, 'file': f, 'id': s['id'], 'tier': s.get('tier', ''), 'day': s.get('arcDay', ''),
                'section': s.get('section', ''), 'h': headline_of(text, s['id']) or s.get('title', '')[:140]})
    out_dir = os.path.join(ROOT, 'storylines')
    os.makedirs(out_dir, exist_ok=True)
    latest = eds[-1][0]
    cutoff = (dt.date.fromisoformat(latest) - dt.timedelta(days=TRACKING_DAYS)).isoformat()

    def label(a):
        lab = arcs.get(a, {}).get('label') or a.replace('-', ' ')
        return lab[:1].upper() + lab[1:]
    rows = []
    for a, es in entries.items():
        es.sort(key=lambda e: (e['date'], e['id']), reverse=True)
        items = ''.join('<li class="%s"><span class="d">%s</span><a href="../editions/%s#%s">%s</a><span class="t">%s%s</span></li>' % (
            e['tier'], esc(e['date']), e['file'], e['id'], esc(e['h']), esc(e['tier'].upper()),
            (' · day %s' % e['day']) if e['day'] else '') for e in es)
        page = STORY_PAGE % {'title': esc(label(a)), 'n': len(es), 'first': es[-1]['date'], 'last': es[0]['date'],
                             'items': items, 'note': esc(es[0]['h']), 'arc': a}
        open(os.path.join(out_dir, a + '.html'), 'w').write(page)
        rows.append((es[0]['date'] >= cutoff, es[0]['date'], len(es), a))
    rows.sort(key=lambda r: (r[0], r[1], r[2]), reverse=True)
    lis = []
    for active, last, n, a in rows:
        lis.append('<li class="%s"><a href="%s.html">%s</a><span class="t">%d stories · last %s</span></li>' % (
            'active' if active else 'quiet', a, esc(label(a)), n, last))
    n_active = sum(1 for r in rows if r[0])
    open(os.path.join(out_dir, 'index.html'), 'w').write(STORY_INDEX % {'items': ''.join(lis), 'active': n_active, 'total': len(rows)})
    return len(rows), n_active


STYLE = '''<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Inter:wght@400;600&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root{--ink:#16140f;--paper:#f5f1e8;--paper2:#ece6d8;--rule:#c9c0ac;--crit:#b3261e;--note:#8a6d00;--mon:#3d5a4c;--accent:#1f3a93;--muted:#6b6353}
  @media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--ink:#efe9dc;--paper:#15130f;--paper2:#211e18;--rule:#3a352b;--accent:#8fa8f0;--muted:#a49a86}}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--paper);color:var(--ink);font-family:'Inter',sans-serif;line-height:1.5}
  .wrap{max-width:860px;margin:0 auto;padding:24px 16px 60px}
  a{color:var(--accent);text-decoration:none}
  .top{font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:1px;color:var(--muted);text-transform:uppercase}
  h1{font-family:'Fraunces',serif;font-weight:800;font-size:clamp(28px,6vw,42px);line-height:1.1;margin:10px 0 6px}
  .sub{color:var(--muted);margin-bottom:18px}
  ul{list-style:none;border-top:3px solid var(--ink)}
  li{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;padding:12px 0;border-bottom:1px solid var(--rule)}
  li a{font-family:'Fraunces',serif;font-weight:600;font-size:18px;line-height:1.3;flex:1 1 320px}
  .d,.t{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--muted)}
  .d{flex:0 0 90px}
  li.critical{border-left:4px solid var(--crit);padding-left:10px} li.notable{border-left:4px solid var(--note);padding-left:10px} li.monitor{border-left:4px solid var(--mon);padding-left:10px}
  li.quiet a{color:var(--muted)}
  table{border-collapse:collapse;width:100%;font-size:13px}
  th,td{border-bottom:1px solid var(--rule);padding:6px 6px;text-align:right;font-family:'IBM Plex Mono',monospace}
  th:first-child,td:first-child{text-align:left}
  th{font-size:11px;color:var(--muted);font-weight:600}
  .bar{display:inline-block;height:8px;background:var(--mon);vertical-align:middle;margin-left:4px}
  .bad{color:var(--crit);font-weight:600}
</style>'''

STORY_PAGE = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s — AI Daily Signal storyline</title>
<meta name="description" content="Every AI Daily Signal story on %(title)s, newest first.">
''' + STYLE.replace('%', '%%') + '''
</head><body><div class="wrap">
<div class="top"><a href="index.html">← All storylines</a> · <a href="../editions/index.html">All editions</a> · <a href="../app/">Swipe view</a></div>
<h1>%(title)s</h1>
<p class="sub">%(n)d stories from %(first)s to %(last)s. Latest: %(note)s</p>
<ul>%(items)s</ul>
</div></body></html>
'''

STORY_INDEX = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Storylines — AI Daily Signal</title>
<meta name="description" content="The running storylines AI Daily Signal follows, with every story in each.">
''' + STYLE.replace('%', '%%') + '''
</head><body><div class="wrap">
<div class="top"><a href="../editions/index.html">All editions</a> · <a href="../app/">Swipe view</a> · <a href="../editions/quality.html">Quality log</a></div>
<h1>Storylines</h1>
<p class="sub">%(active)d active in the last two weeks, %(total)d in all. Each one lists every story we ran on it, newest first.</p>
<ul>%(items)s</ul>
</div></body></html>
'''


# ---------------------------------------------------------------- quality log
def update_quality(eds, read_state):
    """Recompute the quality log from every v3 edition (page-data), plus data-file extras."""
    q = json.load(open(QUALITY_FILE)) if os.path.exists(QUALITY_FILE) else {}
    for date, f in eds:
        ps = read_state(open(os.path.join(ED, f)).read()) or {}
        if ps.get('format') != 'v3':
            continue
        ss = ps.get('stories', [])
        cn = [s for s in ss if s.get('tier') in ('critical', 'notable')]
        row = {
            'edition': ps.get('edition'), 'type': ps.get('editionType', 'daily'), 'degraded': bool(ps.get('degraded')),
            'stories': len(ss), 'new': sum(1 for s in ss if s.get('section') == 'new'),
            'criticalNotable': len(cn),
            'checkedShare': round(sum(1 for s in cn if s.get('verified') == 'opened') / len(cn), 2) if cn else None,
            'singleSourceShare': round(sum(1 for s in ss if s.get('confidence') == 'Agg 1x') / len(ss), 2) if ss else None,
            'rumours': sum(1 for s in ss if s.get('confidence') == 'Rumor-flag'),
            'sourcesOpened': ps.get('sourcesOpened'), 'shareable': bool(ps.get('shareable')),
        }
        d = load_data(date)
        if d:
            fu = d.get('followups', [])
            row.update({'followups': {k: sum(1 for x in fu if x.get('status') == k) for k in FOLLOWUP_STATUSES if any(x.get('status') == k for x in fu)},
                        'corrections': len(d.get('corrections', [])), 'productCompanies': len(d.get('productUpdates', [])),
                        'scanCount': d.get('scanCount')})
        q[date] = row
    json.dump(dict(sorted(q.items())), open(QUALITY_FILE, 'w'), indent=1)
    rows = []
    for date, r in sorted(q.items(), reverse=True)[:120]:
        cs = r.get('checkedShare')
        rows.append('<tr><td><a href="ai_daily_signal_%s.html">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td%s>%s<span class="bar" style="width:%dpx"></span></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            date, date, r.get('edition', ''), r['stories'], r['criticalNotable'],
            ' class="bad"' if cs is not None and cs < 0.5 else '', '' if cs is None else '%d%%' % (cs * 100), int((cs or 0) * 60),
            '' if r.get('singleSourceShare') is None else '%d%%' % (r['singleSourceShare'] * 100), r.get('rumours', 0),
            r.get('sourcesOpened', ''), ('catch-up' if r.get('type') == 'catch-up' else '') + (' degraded' if r.get('degraded') else ''),
            ', '.join('%s %d' % kv for kv in r.get('followups', {}).items()) + ((' · %d corrected' % r['corrections']) if r.get('corrections') else '')))
    page = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Quality log — AI Daily Signal</title>
<meta name="description" content="How well each AI Daily Signal edition was checked.">
''' + STYLE.replace('%', '%%') + '''
</head><body><div class="wrap">
<div class="top"><a href="index.html">All editions</a> · <a href="../storylines/index.html">Storylines</a></div>
<h1>Quality log</h1>
<p class="sub">Per edition: Critical and Notable stories checked on an opened page (aim for 100%%; under 50%% makes an edition degraded), share of single-source stories, rumours shown, pages opened, and the next-day re-check of the previous edition's Critical and Notable stories.</p>
<div style="overflow-x:auto"><table><tr><th>Date</th><th>Ed.</th><th>Stories</th><th>Crit+Not.</th><th>Checked</th><th>Single-src</th><th>Rumours</th><th>Opened</th><th>Flags</th><th>Next-day re-check</th></tr>
%s</table></div>
</div></body></html>
''' % ''.join(rows)
    open(os.path.join(ED, 'quality.html'), 'w').write(page)
    return len(q)
