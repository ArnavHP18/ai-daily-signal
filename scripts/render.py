#!/usr/bin/env python3
"""Render an edition page from its data file, and sync the state file.

    python3 scripts/render.py 2026-11-10        # editions/data/2026-11-10.json -> editions/ai_daily_signal_2026-11-10.html

The daily run writes only editions/data/DATE.json (content) and the bookkeeping parts of
state/signal-state.json (tracking, watchlist, retired, resolved, movers, heldBack, noChange,
runNotes). This script then:
  - checks the data file (schema, allowed HTML, categories, storyline labels, lead, links);
  - renders the page with template.html's CSS and script (the design lives there only);
  - writes the edition-level fields of the state file from the data file (edition, date, flags,
    counts, tiers, stories, deadlines, arcs), so page and state can never disagree.
Run scripts/build_site.py afterwards. The data file format is documented in ROUTINE.md (§4 v4).
"""
import datetime as dt
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'editions', 'data')
STATE_FILE = os.path.join(ROOT, 'state', 'signal-state.json')
TEMPLATE = os.path.join(ROOT, 'template.html')

CATEGORIES = ['models', 'research', 'hardware', 'security', 'robotics', 'health', 'energy', 'enterprise', 'business', 'policy']
CAT_LABEL = {'policy': 'POLICY & SOCIETY'}
TRUST = {'Primary': ('official', 'Official source'), '2x src': ('multi', 'Two or more outlets'),
         'Agg 1x': ('single', 'One secondary source'), 'Rumor-flag': ('rumor', 'Unconfirmed')}
TIERLBL = {'critical': 'CRITICAL', 'notable': 'NOTABLE', 'monitor': 'MONITOR'}
SRC_GROUPS = ['OFFICIAL', 'REPORTING', 'OTHER', 'AGGREGATOR']
ALLOWED_TAGS = {'p', 'div', 'strong', 'em', 'b', 'i', 'code', 'a', 'span', 'br', 'ul', 'ol', 'li'}
REACTION_KIND = {'video': 'Video', 'reddit': 'Reddit', 'hn': 'Hacker News', 'news': 'Coverage', 'post': 'Post'}
REQUIRED = ['id', 'section', 'tier', 'impact', 'arc', 'arcDay', 'confidence', 'verified', 'new24h', 'category',
            'title', 'h', 'body', 'chip', 'src', 'cat', 'tickerKey']


def esc(x):
    return html.escape(str(x), quote=False)


def attr(x):
    return html.escape(str(x), quote=True)


class DataError(Exception):
    pass


def check(d, arc_labels):
    p = []
    for k in ['edition', 'date', 'editionType', 'degraded', 'sourcesOpened', 'scanCount', 'shareable', 'lead', 'stories', 'thirtySecond', 'deadlines', 'footerNote', 'description']:
        if k not in d:
            p.append('missing top-level field "%s"' % k)
    if p:
        raise DataError('\n  - '.join(p))
    ids = [s.get('id') for s in d['stories']]
    if len(ids) != len(set(ids)):
        p.append('duplicate story ids')
    for s in d['stories']:
        sid = s.get('id', '?')
        for k in REQUIRED:
            if k not in s:
                p.append('%s: missing "%s"' % (sid, k))
        if s.get('section') not in ('new', 'developing'):
            p.append('%s: section must be new or developing' % sid)
        if s.get('section') == 'developing' and not s.get('update'):
            p.append('%s: developing story needs "update"' % sid)
        if s.get('tier') not in TIERLBL:
            p.append('%s: bad tier' % sid)
        if s.get('confidence') not in TRUST:
            p.append('%s: bad confidence' % sid)
        if s.get('category') not in CATEGORIES:
            p.append('%s: category "%s" not in %s' % (sid, s.get('category'), CATEGORIES))
        if s.get('arc') and s['arc'] not in arc_labels:
            p.append('%s: storyline "%s" has no label (add it to arcLabels)' % (sid, s['arc']))
        for f in ('body', 'brief'):
            for tag in re.findall(r'</?([a-zA-Z0-9]+)', s.get(f, '')):
                if tag.lower() not in ALLOWED_TAGS:
                    p.append('%s: <%s> not allowed in %s' % (sid, tag, f))
        for g in s.get('src', []):
            if g[0] not in SRC_GROUPS:
                p.append('%s: source group %s not in %s' % (sid, g[0], SRC_GROUPS))
            for label, url in g[1]:
                if not re.match(r'https?://[^/\s]+\.[^/\s]+', url):
                    p.append('%s: bad link %s' % (sid, url))
        if s.get('confidence') == 'Rumor-flag' and s.get('ticker'):
            p.append('%s: unconfirmed stories cannot have ticker text' % sid)
    by = {s['id']: s for s in d['stories']}
    lead = by.get(d['lead'])
    if not lead:
        p.append('lead "%s" is not a story' % d['lead'])
    else:
        if lead['confidence'] == 'Rumor-flag':
            p.append('the lead cannot be unconfirmed')
        for k in ('sub', 'brief', 'facts', 'impactWho'):
            if not lead.get(k):
                p.append('lead needs "%s"' % k)
        if len(lead['h'].split()) > 16:
            p.append('lead headline is %d words (12-15)' % len(lead['h'].split()))
    for t in d['thirtySecond']:
        if t.get('id') == d['lead']:
            p.append('the 30-second read must not repeat the lead')
        if t.get('id') not in by:
            p.append('30-second read item %s is not a story' % t.get('id'))
        elif by[t['id']]['confidence'] == 'Rumor-flag':
            p.append('30-second read cannot include an unconfirmed story')
    if len(d['thirtySecond']) != 3:
        p.append('the 30-second read needs exactly 3 items')
    for c in d.get('productUpdates', []):
        if not c.get('updates'):
            p.append('product updates for %s: leave a company out when it has no updates' % c.get('company'))
        for u in c.get('updates', []) + c.get('reactions', []):
            if not re.match(r'https?://', u.get('url', '')):
                p.append('product updates for %s: every line needs a link' % c.get('company'))
    if p:
        raise DataError('\n  - '.join(p))


def src_html(groups):
    out = []
    for g, links in groups:
        out.append('<span class="grp"><span class="st">%s</span>%s</span>' % (
            g, ' · '.join('<a href="%s">%s</a>' % (attr(u), esc(l)) for l, u in links)))
    return '<div class="src">%s</div>' % ''.join(out)


def render(date):
    d = json.load(open(os.path.join(DATA, date + '.json')))
    state = json.load(open(STATE_FILE))
    arcs = state.setdefault('arcs', {})
    arc_labels = {k: v.get('label') for k, v in arcs.items() if v.get('label')}
    arc_labels.update(d.get('arcLabels', {}))
    check(d, arc_labels)
    D = dt.date.fromisoformat(date)
    longdate = D.strftime('%A, ') + str(D.day) + D.strftime(' %B %Y')
    shortdate = str(D.day) + D.strftime(' %B %Y')

    S = d['stories']
    new = [s for s in S if s['section'] == 'new']
    dev = [s for s in S if s['section'] == 'developing']
    for i, s in enumerate(new, 1):
        s['rank'] = i
    for i, s in enumerate(dev, 1):
        s['rank'] = i
    by = {s['id']: s for s in S}
    lead = by[d['lead']]

    def tier_span(s):
        return '<span class="tier %s">%s</span>' % (s['tier'], TIERLBL[s['tier']])

    def trust_span(s):
        c, l = TRUST[s['confidence']]
        return '<span class="trust %s">%s</span>' % (c, l)

    def storyline(s):
        return '<a href="../storylines/%s.html">Storyline: %s · day %d</a>' % (attr(s['arc']), esc(arc_labels[s['arc']]), s['arcDay'])

    def rank_of(s):
        return ('D%d' if s['section'] == 'developing' else '#%d') % s['rank']

    def delta_line(s):
        return '<div class="delta-line"><span class="dl-tag">WHAT CHANGED</span> %s</div>' % esc(s['update']) if s['section'] == 'developing' else ''

    def big_card(s):
        return f'''    <article class="card {s['tier']}{' rumor' if s['confidence'] == 'Rumor-flag' else ''} feed-item" id="{s['id']}" data-cat="{s['category']}" data-story-id="{s['id']}">
      <div class="top"><span><span class="rank">{rank_of(s)}</span><span class="cat">{esc(s['cat'])}</span></span><span class="impact">IMPACT <b>{s['impact']}</b>/10</span></div>
      <h4>{esc(s['h'])}</h4>
      <p class="sub">{esc(s.get('sub', ''))}</p>
      {delta_line(s)}{s['body']}
      <div>{tier_span(s)}{trust_span(s)}<span class="chip">{esc(s['chip'])}</span></div>
      {src_html(s['src'])}
      <div class="storyline">{storyline(s)}</div>
      <div style="margin-top:10px"><button class="share" data-share="{s['id']}">Share ↗</button></div>
    </article>
'''

    def row(s):
        rum = ' rumor' if s['confidence'] == 'Rumor-flag' else ''
        return f'''    <details class="row{rum} feed-item" id="{s['id']}" data-cat="{s['category']}" data-story-id="{s['id']}">
      <summary><span class="rank">{rank_of(s)}</span><span><h4>{esc(s['h'])}</h4><div class="meta">{tier_span(s)}{trust_span(s)}<span class="cat">{esc(s['cat'])}</span></div></span><span class="more"></span></summary>
      <div class="detail">
        {delta_line(s)}{s['body'].strip()}
        {src_html(s['src'])}
        <div class="storyline">{storyline(s)} · {esc(s['chip'])}</div>
        <div style="margin-top:8px"><button class="share" data-share="{s['id']}">Share ↗</button></div>
      </div>
    </details>
'''

    ticker_items = [lead] + [s for s in S if s is not lead and s['confidence'] != 'Rumor-flag' and s.get('ticker')]
    ticker = ' &nbsp;◆&nbsp; '.join('<b>%s</b> %s' % (esc(s['tickerKey']), esc(s.get('ticker') or s['h'])) for s in ticker_items)

    cats = {}
    for s in S:
        cats[s['category']] = cats.get(s['category'], 0) + 1
    tabs = '    <button class="tab active" data-cat="all">ALL (%d)</button>\n' % len(S) + ''.join(
        '    <button class="tab" data-cat="%s">%s (%d)</button>\n' % (c, CAT_LABEL.get(c, c.upper()), cats[c]) for c in CATEGORIES if c in cats)

    trip = ''.join(f'''    <article class="trip">
      <div class="num">{i + 1}</div>
      <h4>{esc(t['h'])}</h4>
      <p>{esc(t['p'])} <a class="jump" href="#{t['id']}">{rank_of(by[t['id']])} ↓</a></p>
    </article>
''' for i, t in enumerate(d['thirtySecond']))

    facts = ''.join('      <dt>%s</dt><dd>%s</dd>\n' % (esc(a), esc(b)) for a, b in lead['facts'])
    lead_tier = {'critical': 'CRITICAL · ACT THIS WEEK', 'notable': 'NOTABLE · THIS MONTH', 'monitor': 'MONITOR'}[lead['tier']]
    hero = f'''<article class="hero" id="{lead['id']}" data-story-id="{lead['id']}">
  <div>
    <h2>{esc(lead['h'])}</h2>
    <p class="subhead">{esc(lead['sub'])}</p>
    <div><span class="tier {lead['tier']}">{lead_tier}</span>{trust_span(lead)}<span class="chip">{esc(lead['chip'])}</span></div>
    {delta_line(lead)}{lead['body']}
    {src_html(lead['src'])}
    <div class="storyline">{storyline(lead)}</div>
    <button class="brief-toggle" onclick="document.getElementById('hero-brief').classList.toggle('open')">READ FULL BRIEF ▾</button>
    <div class="full-brief" id="hero-brief">
      {lead['brief']}
    </div>
  </div>
  <aside class="facts">
    <h3>Facts</h3>
    <dl>
{facts}      <dt>Impact</dt><dd><b style="font-size:18px">{lead['impact']}</b>/10 — {esc(lead['impactWho'])}</dd>
    </dl>
  </aside>
</article>'''

    lead_ref = '  <div class="lead-ref feed-item" data-cat="%s"><strong>%s</strong> is today\'s lead, above: %s <a href="#%s">Back to top ↑</a></div>\n' % (
        lead['category'], rank_of(lead), esc(d.get('leadRef') or lead['h']), lead['id'])
    new_rest = [s for s in new if s is not lead]
    dev_rest = [s for s in dev if s is not lead]
    new_sec = f'''<section>
  <div class="sec-head">New on the Wire <small id="new-head"></small></div>
  <div class="tabs">
{tabs}  </div>
{lead_ref if lead['section'] == 'new' else ''}
  <!-- the two highest-scoring new stories get large cards -->
  <div class="big">

{''.join(big_card(s) for s in new_rest[:2])}  </div>

  <!-- everything else: compact list, tap to expand -->
  <div class="compact">
{''.join(row(s) for s in new_rest[2:])}  </div>
</section>'''
    dev_sec = ''
    if dev:
        dev_sec = f'''
<!-- DEVELOPING: carried stories that moved -->
<section>
  <div class="sec-head">Developing <small>CARRIED STORIES THAT MOVED</small></div>
{lead_ref if lead['section'] == 'developing' else ''}  <div class="compact">
{''.join(row(s) for s in dev_rest)}  </div>
</section>'''

    pu_sec = product_updates_html(d.get('productUpdates', []), 'Product Updates', 'WHAT SHIPPED · WHAT PEOPLE ARE SAYING', '')
    if D.weekday() == 6 or d.get('weeklyRoundup'):
        pu_sec += product_updates_html(weekly_updates(date), 'This Week in Products', 'THE LAST SEVEN DAYS, BY COMPANY', ' pu-week')

    fu = d.get('followups', [])
    corrections = d.get('corrections', [])
    footer_extra = ''
    if corrections:
        footer_extra += '    <p><strong>Corrections:</strong> %s</p>\n' % ' '.join(esc(c) for c in corrections)
    changed = [f for f in fu if f.get('status') in ('changed', 'corrected')]
    if changed:
        footer_extra += '    <p class="followup"><strong>Since the last edition:</strong> %s</p>\n' % ' · '.join(
            '%s — %s' % (esc(f['label'] if f.get('label') else f['id']), esc(f['note'])) for f in changed)

    body = f'''<body>

<!-- TICKER: confirmed items only. Never put an "Unconfirmed" story here. -->
<div class="ticker" aria-hidden="true"><div class="ticker-inner">
  {ticker}
</div></div>

<!-- DEGRADED BANNER: shown when state.degraded is true -->
<div class="degraded" id="degraded"><div class="wrap"><strong>DEGRADED EDITION</strong> <span id="degraded-text"></span></div></div>

<header class="masthead wrap">
  <a class="brand" href="index.html" aria-label="AI Daily Signal archive"><img src="../assets/logo.svg" alt=""><h1>AI Daily Signal</h1></a>
  <div class="when">Edition {d['edition']} · {longdate}</div>
  <div class="byline">Curated by Arnav Agrawal<span data-slot="curator-links"></span></div>
  <a class="swipe-link" href="../app/">📱 SWIPE VIEW</a>
</header>

<main class="wrap">

<!-- STATUS LINE: rendered from state (editionType, counts, new24h, sourcesOpened) -->
<div class="status" id="status"></div>

<!-- HERO: headline 12-15 words, one sub-line, then the detail -->
{hero}

<!-- 30-SECOND READ: right under the headline; never repeats the lead -->
<section>
  <div class="sec-head">The 30-Second Read <small>THE NEXT THREE AFTER THE LEAD</small></div>
  <div class="triptych">
{trip}  </div>
</section>

<!-- DEADLINES: timeline with days-left counters, rendered from state.deadlines -->
<section>
  <div class="sec-head">Coming Up <small>DATES THAT MATTER · DAYS LEFT</small></div>
  <div class="timeline" id="timeline"></div>
</section>

<!-- FEED -->
{new_sec}
{dev_sec}
{pu_sec}
</main>

<footer>
  <div class="wrap">
    <p><strong>AI Daily Signal</strong> · Edition {d['edition']} · {shortdate} (IST) · Curated by Arnav Agrawal<span data-slot="curator-links"></span> · <a href="index.html">All editions</a> · <a href="../storylines/index.html">Storylines</a><span data-slot="sister-links"></span></p>
    <p>{esc(d['footerNote'])}</p>
{footer_extra}  </div>
</footer>

<div class="toast" id="toast">Link copied</div>

'''

    # ---- state sync (edition-level fields only; bookkeeping stays as the run wrote it)
    def sstate(s):
        o = {k: s[k] for k in ('id', 'section', 'rank', 'title', 'tier', 'impact') if k in s}
        o['delta'] = s.get('delta', 'new' if s['section'] == 'new' else 'carry')
        o.update({k: s[k] for k in ('arc', 'arcDay', 'confidence', 'verified', 'new24h')})
        if s['section'] == 'developing':
            o['update'] = s['update']
        o.update({'firstSeen': s.get('firstSeen', date), 'lastUpdate': date, 'category': s['category'], 'tickerKey': s['tickerKey']})
        for k in ('short', 'stat', 'image'):
            if s.get(k):
                o[k] = s[k]
        return o
    order = new + dev
    stories = [sstate(s) for s in order]
    tiers = {'critical': 0, 'notable': 0, 'monitor': 0}
    for s in S:
        tiers[s['tier']] += 1
    for k in ('edition', 'date', 'editionType', 'degraded', 'sourcesOpened', 'shareable', 'scanCount', 'deadlines'):
        state[k] = d[k]
    state.update({'tz': 'Asia/Kolkata', 'format': 'v3', 'degradedReason': d.get('degradedReason', ''),
                  'shareBlockers': d.get('shareBlockers', []), 'stories': stories, 'tiers': tiers})
    state['counts'] = {'new': len(new), 'developing': len(dev), 'tracking': len(state.get('tracking', []))}
    for s in S:
        a = arcs.setdefault(s['arc'], {'day': 0, 'note': ''})
        a['day'] = max(a.get('day', 0), s['arcDay'])
        a['note'] = s['title'][:300]
        a['label'] = arc_labels[s['arc']]
        a['last'] = date
    page = {k: state[k] for k in ['edition', 'date', 'tz', 'format', 'editionType', 'degraded', 'degradedReason', 'sourcesOpened', 'shareable']}
    page['counts'] = {'new': len(new), 'developing': len(dev)}
    page.update({'tiers': tiers, 'stories': stories, 'deadlines': d['deadlines']})

    tpl = open(TEMPLATE).read()
    head = tpl[:tpl.index('<body>')]
    head = re.sub(r'(?s)<!--.*?-->\n', '', head, count=1)    # the template's explanatory comment
    script = tpl[tpl.index('<script>\n(function(){'):]
    ogd = 'AI Daily Signal, edition %d (%s): %s%d new stories, %d developing.' % (
        d['edition'], D.strftime('%d %b %Y').lstrip('0'), 'a catch-up edition, ' if d['editionType'] == 'catch-up' else '', len(new), len(dev))
    head = re.sub(r'<title>.*?</title>', '<title>AI Daily Signal — Edition %d — %s</title>' % (d['edition'], shortdate), head)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + attr(d['description']), head)
    for p_ in ['og:title', 'twitter:title']:
        head = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % p_, lambda m: m.group(1) + attr(lead['h']), head)
    for p_ in ['og:description', 'twitter:description']:
        head = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % p_, lambda m: m.group(1) + attr(ogd), head)
    head = re.sub(r'ai_daily_signal_\d{4}-\d{2}-\d{2}\.html', 'ai_daily_signal_%s.html' % date, head)
    head = re.sub(r'cards/\d{4}-\d{2}-\d{2}\.png', 'cards/%s.png' % date, head)
    out = head + body + '<script id="page-data" type="application/json">\n' + json.dumps(page, indent=1, ensure_ascii=False) + '\n</script>\n\n' + script
    path = os.path.join(ROOT, 'editions', 'ai_daily_signal_%s.html' % date)
    open(path, 'w').write(out)
    json.dump(state, open(STATE_FILE, 'w'), indent=1, ensure_ascii=False)
    return path, len(new), len(dev), tiers


def product_updates_html(companies, title, small, extra_cls):
    if not companies:
        return ''
    blocks = []
    for c in companies:
        ups = ''.join('<li><a href="%s">%s</a>%s</li>' % (attr(u['url']), esc(u['text']), (' <span class="kind">%s</span>' % esc(u['date'])) if u.get('date') else '')
                      for u in c['updates'])
        says = ''
        if c.get('reactions'):
            says = '<div class="say"><b>WHAT PEOPLE ARE SAYING</b><ul>%s</ul></div>' % ''.join(
                '<li><span class="kind">%s</span><a href="%s">%s</a>%s</li>' % (
                    esc(REACTION_KIND.get(r.get('kind'), r.get('kind', ''))), attr(r['url']), esc(r['title']), (' — ' + esc(r['note'])) if r.get('note') else '')
                for r in c['reactions'])
        blocks.append('    <div class="pu-co"><h4>%s</h4><ul>%s</ul>%s</div>\n' % (esc(c['company']), ups, says))
    return f'''
<!-- PRODUCT UPDATES: what each company shipped (official changelogs) and what people are saying -->
<section>
  <div class="sec-head">{title} <small>{small}</small></div>
  <div class="pu{extra_cls}">
{''.join(blocks)}  </div>
</section>
'''


def weekly_updates(date):
    """Merge the last seven data files' product updates by company (for Sunday editions)."""
    D = dt.date.fromisoformat(date)
    merged = {}
    for i in range(7):
        f = os.path.join(DATA, (D - dt.timedelta(days=i)).isoformat() + '.json')
        if not os.path.exists(f):
            continue
        for c in json.load(open(f)).get('productUpdates', []):
            m = merged.setdefault(c['company'], {'company': c['company'], 'updates': [], 'reactions': []})
            seen = {u['url'] + u['text'] for u in m['updates']}
            m['updates'] += [u for u in c['updates'] if u['url'] + u['text'] not in seen]
    out = sorted(merged.values(), key=lambda c: -len(c['updates']))
    for c in out:
        c['updates'] = c['updates'][:8]
    return out


def main():
    if len(sys.argv) < 2 or not re.match(r'^\d{4}-\d{2}-\d{2}$', sys.argv[1]):
        sys.exit('usage: python3 scripts/render.py YYYY-MM-DD')
    try:
        path, n, dv, tiers = render(sys.argv[1])
    except DataError as e:
        print('DATA FILE FAILS CHECKS:\n  - %s' % e)
        sys.exit(1)
    print('rendered %s (%d new, %d developing, tiers %s); state synced' % (os.path.relpath(path, ROOT), n, dv, tiers))


if __name__ == '__main__':
    main()
