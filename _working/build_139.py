# Generates edition 139 (2026-11-09) page and state. Working file; not published.
import json, re, html
def src(groups):
    out = []
    for g, links in groups:
        out.append('<span class="grp"><span class="st">%s</span>%s</span>' % (g, ' · '.join('<a href="%s">%s</a>' % (u, html.escape(l, quote=False)) for l, u in links)))
    return '<div class="src">%s</div>' % ''.join(out)

TRUST = {'Primary': ('official', 'Official source'), '2x src': ('multi', 'Two or more outlets'),
         'Agg 1x': ('single', 'One secondary source'), 'Rumor-flag': ('rumor', 'Unconfirmed')}
TIERLBL = {'critical': 'CRITICAL', 'notable': 'NOTABLE', 'monitor': 'MONITOR'}

S = []
def story(**k): S.append(k); return k
exec(open('_working/stories_139.py').read())

# ---------------------------------------------------------------- render
new = [s for s in S if s['section'] == 'new']; dev = [s for s in S if s['section'] == 'developing']
for i, s in enumerate(new, 1): s['rank'] = i
for i, s in enumerate(dev, 1): s['rank'] = i
for s in S: s.setdefault('first', DATE)

def tier_span(s): return '<span class="tier %s">%s</span>' % (s['tier'], TIERLBL[s['tier']])
def trust_span(s):
    c, l = TRUST[s['confidence']]; return '<span class="trust %s">%s</span>' % (c, l)
def esc(x): return html.escape(x, quote=False)
def storyline(s): return 'Storyline: %s · day %d' % (esc(ARCLBL[s['arc']]), s['arcDay'])

def big_card(s):
    return f'''    <article class="card {s['tier']} feed-item" id="{s['id']}" data-cat="{s['category']}" data-story-id="{s['id']}">
      <div class="top"><span><span class="rank">#{s['rank']}</span><span class="cat">{esc(s['cat'])}</span></span><span class="impact">IMPACT <b>{s['impact']}</b>/10</span></div>
      <h4>{esc(s['h'])}</h4>
      <p class="sub">{esc(s['sub'])}</p>
      {s['body']}
      <div>{tier_span(s)}{trust_span(s)}<span class="chip">{esc(s['chip'])}</span></div>
      {src(s['src'])}
      <div class="storyline">{storyline(s)}</div>
      <div style="margin-top:10px"><button class="share" data-share="{s['id']}">Share ↗</button></div>
    </article>
'''

def row(s, dev=False):
    rank = ('D%d' if dev else '#%d') % s['rank']
    rum = ' rumor' if s['confidence'] == 'Rumor-flag' else ''
    dl = ('<div class="delta-line"><span class="dl-tag">WHAT CHANGED</span> %s</div>' % esc(s['update'])) if dev else ''
    return f'''    <details class="row{rum} feed-item" id="{s['id']}" data-cat="{s['category']}" data-story-id="{s['id']}">
      <summary><span class="rank">{rank}</span><span><h4>{esc(s['h'])}</h4><div class="meta">{tier_span(s)}{trust_span(s)}<span class="cat">{esc(s['cat'])}</span></div></span><span class="more"></span></summary>
      <div class="detail">
        {dl}{s['body'].strip()}
        {src(s['src'])}
        <div class="storyline">{storyline(s)} · {esc(s['chip'])}</div>
        <div style="margin-top:8px"><button class="share" data-share="{s['id']}">Share ↗</button></div>
      </div>
    </details>
'''

lead = dev[0]
ticker_items = [lead] + [s for s in S if s is not lead and s['confidence'] != 'Rumor-flag' and s.get('ticker')]
ticker = ' &nbsp;◆&nbsp; '.join('<b>%s</b> %s' % (esc(s['tickerKey']), esc(s['ticker'])) for s in ticker_items)

cats = {}
for s in S: cats[s['category']] = cats.get(s['category'], 0) + 1
tabs = '    <button class="tab active" data-cat="all">ALL (%d)</button>\n' % len(S) + ''.join('    <button class="tab" data-cat="%s">%s (%d)</button>\n' % (c, c.upper(), n) for c, n in sorted(cats.items()))

trip_src = new[0:3]
trip_h = ['Anthropic buys its own power', "DeepSeek's agent app takes off", 'Coding agents stop short']
trip_p = ["The FT says Anthropic is paying $3.4B for 1.7GW of gas generators, the biggest such purchase by an AI company.",
          "Harness, DeepSeek's open agent framework, reports 1.54M daily users and 92 trillion tokens a day.",
          "On tasks taken from real user sessions, the best model fully completes only 26% of requests."]
trip = ''.join(f'''    <article class="trip">
      <div class="num">{i+1}</div>
      <h4>{esc(trip_h[i])}</h4>
      <p>{esc(trip_p[i])} <a class="jump" href="#{s['id']}">#{s['rank']} ↓</a></p>
    </article>
''' for i, s in enumerate(trip_src))

facts = ''.join('      <dt>%s</dt><dd>%s</dd>\n' % (esc(a), esc(b)) for a, b in lead['facts'])
hero = f'''<article class="hero" id="{lead['id']}" data-story-id="{lead['id']}">
  <div>
    <h2>{esc(lead['h'])}</h2>
    <p class="subhead">{esc(lead['sub'])}</p>
    <div><span class="tier critical">CRITICAL · ACT THIS WEEK</span>{trust_span(lead)}<span class="chip">{esc(lead['chip'])}</span></div>
    <div class="delta-line"><span class="dl-tag">WHAT CHANGED</span> {esc(lead['update'])}</div>
    {lead['body']}
    {src(lead['src'])}
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

bigs = ''.join(big_card(s) for s in new[0:2])
rows = ''.join(row(s) for s in new[2:])
devrows = ''.join(row(s, True) for s in dev[1:])

body = f'''<body>

<!-- TICKER: confirmed items only. Never put an "Unconfirmed" story here. -->
<div class="ticker" aria-hidden="true"><div class="ticker-inner">
  {ticker}
</div></div>

<!-- DEGRADED BANNER: shown when state.degraded is true -->
<div class="degraded" id="degraded"><div class="wrap"><strong>DEGRADED EDITION</strong> <span id="degraded-text"></span></div></div>

<header class="masthead wrap">
  <a class="brand" href="index.html" aria-label="AI Daily Signal archive"><img src="../assets/logo.svg" alt=""><h1>AI Daily Signal</h1></a>
  <div class="when">Edition {ED} · {LONGDATE}</div>
  <div class="byline">Curated by Arnav Agrawal<span data-slot="curator-links"></span></div>
</header>

<main class="wrap">

<!-- STATUS LINE: rendered from state (editionType, counts, new24h, sourcesOpened) -->
<div class="status" id="status"></div>

<!-- HERO: headline 12-15 words, one sub-line, then the detail. Today's lead is a carried story that escalated. -->
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
<section>
  <div class="sec-head">New on the Wire <small id="new-head"></small></div>
  <div class="tabs">
{tabs}  </div>

  <!-- the two highest-scoring stories after the lead get large cards -->
  <div class="big">

{bigs}  </div>

  <!-- everything else: compact list, tap to expand -->
  <div class="compact">
{rows}  </div>
</section>

<!-- DEVELOPING: carried stories that moved -->
<section>
  <div class="sec-head">Developing <small>CARRIED STORIES THAT MOVED</small></div>
  <div class="lead-ref feed-item" data-cat="{lead['category']}"><strong>D1</strong> is today's lead, above: Nvidia's board investigates Jensen Huang. <a href="#{lead['id']}">Back to top ↑</a></div>
  <div class="compact">
{devrows}  </div>
</section>

</main>

<footer>
  <div class="wrap">
    <p><strong>AI Daily Signal</strong> · Edition {ED} · 9 November 2026 (IST) · Curated by Arnav Agrawal<span data-slot="curator-links"></span> · <a href="index.html">All editions</a><span data-slot="sister-links"></span></p>
    <p>Monday's focus: research. Today that meant two new tests of AI agents on real work (Co-Design Bench on real coding requests, Into the Unknown on open national-lab research questions), Richard Sutton's argument that compute alone is not enough, and a project that runs a 284-billion-parameter model on an ordinary desktop.</p>
  </div>
</footer>

<div class="toast" id="toast">Link copied</div>

'''

# ---------------------------------------------------------------- state
old = json.load(open('state/signal-state.json'))
ids_today = {s['id'] for s in S}

def sstate(s):
    d = {'id': s['id'], 'section': s['section'], 'rank': s['rank'], 'title': s['title'], 'tier': s['tier'], 'impact': s['impact'],
         'delta': s.get('delta', 'new'), 'arc': s['arc'], 'arcDay': s['arcDay'], 'confidence': s['confidence'], 'verified': s['verified'],
         'new24h': s['new24h']}
    if s['section'] == 'developing': d['update'] = s['update']
    d.update({'firstSeen': s['first'], 'lastUpdate': DATE, 'category': s['category'], 'tickerKey': s['tickerKey']})
    return d
stories = [sstate(s) for s in new] + [sstate(s) for s in dev]
tiers = {'critical': 0, 'notable': 0, 'monitor': 0}
for s in S: tiers[s['tier']] += 1

trk = {t['id']: t for t in old['tracking']}
retired, resolved = [], []
def retire(i, reason):
    trk.pop(i); retired.append({'id': i, 'date': DATE, 'reason': reason})
retire('open-muse-clones', 'Re-searched OpenMuse / Muse clones and Manus rivals: OpenMuse (CopilotKit) and OpenManus exist, but no star counts or new coverage since early October; followed on the personal-agent-identity watchlist entry')
retire('turba-labs-dc-digital-twins', 'Re-searched Turba Labs and its data-centre digital twins: no coverage at all beyond the original October item; no utilisation data')
retire('arxiv-agent-cluster-oct6', 'Re-searched the 6 Oct arXiv agent cluster: superseded; later agent benchmarks (Into the Unknown, Co-Design Bench) carded today')
retire('teddy-ai-60m-seed', 'Re-searched TeddyHoldings.AI and its $60M seed: investors, stack and valuation still undisclosed; only a reported plan for a $100M Series A by year-end (Dealroom)')
retire('anthropic-critical-infra-defense', 'Re-searched the Critical Infrastructure Defense Program: still the 8 Oct launch with 11 partners (Hitachi, CrowdStrike and others); no partner results published')
trk.pop('claude-haiku-55'); resolved.append('Claude Haiku 5.5: independent evaluations now exist (Artificial Analysis: strong on knowledge-work benchmarks, 35% on AutomationBench-AA partly from over-refusal Anthropic says it is fixing; Vals comparison pages)')
trk.pop('openai-gpt6-chatgpt-everyone'); resolved.append('GPT-6 for everyone: Luna reached Free and Go users in standard Chat from 8 Oct per ChatGPT release notes; paid tiers use Sol')
trk.pop('naukri-sep-aiml-hiring-20pct'); resolved.append('Naukri September AI/ML +20% superseded by the October JobSpeak (AI/ML +32%), carded as New #8')
trk.pop('hubspot-660-cuts'); resolved.append('HubSpot cut size settled on re-search: about 660 jobs (~7%), $65-75M restructuring charges per its filing; CEO says the cuts are not driven by AI efficiencies')
trk['personal-agent-protocol'].update(label="Re-checked 9 Nov: Forkast reports draft documentation is live at personalagentprotocol.org/docs, still labelled a draft, with no reference implementation yet; Meta and Sierra had promised v0.1 and a reference implementation for late October", lastChecked=DATE)
trk.pop('siri-third-party-apps', None)

yl = {
 'claude-code-dont-ask-again-secrets': "MOVED FROM NEW after one edition: Apiiro's post reached ~580 points on Hacker News; no Anthropic statement or settings change found",
 'ai-ceo-deepfake-129m-charges': 'MOVED FROM NEW after one edition: the New York Times (8 Nov) also covers the $129M AI fake-CEO scheme; no new charges',
}
newtrk = []
for s in old['stories']:
    if s['id'] in ids_today: continue
    lab = yl.get(s['id'], 'MOVED FROM %s after one edition: %s' % ('DEVELOPING' if s['section'] == 'developing' else 'NEW', s['title'][:230]))
    newtrk.append({'id': s['id'], 'label': lab, 'arc': s['arc'], 'arcDay': s['arcDay'], 'since': DATE, 'lastChecked': DATE})
tracking = []; seen = set()
for t in newtrk + list(trk.values()):
    if t['id'] in seen or t['id'] in ids_today: continue
    seen.add(t['id']); tracking.append(t)

arcs = old['arcs']
for s in S:
    a = arcs.setdefault(s['arc'], {'day': 0, 'note': ''})
    a['day'] = max(a.get('day', 0), s['arcDay']); a['note'] = s['title'][:300]

movers = [
 {'dir': 'down', 'text': "NVIDIA - board opens an independent investigation after Jensen Huang admits an affair with a suspected Chinese intelligence asset (lead, D1)"},
 {'dir': 'up', 'text': 'ANTHROPIC - buys 1.7GW of gas generators for $3.4B (#1)'},
 {'dir': 'up', 'text': 'DEEPSEEK HARNESS - 1.54M daily users, 92T tokens a day, 35,000 plug-ins (#2)'},
 {'dir': 'down', 'text': 'CODING AGENTS - best model fully completes 26.4% of real user tasks on Co-Design Bench (#3)'},
 {'dir': 'down', 'text': 'AI RESEARCH AGENTS - 114 of 135 papers fail integrity check on Into the Unknown (#4)'},
 {'dir': 'up', 'text': 'LOCAL INFERENCE - llama-modchip runs 284B DeepSeek V4 Flash on 64GB, no GPU (#5)'},
 {'dir': 'up', 'text': 'US WHITE-COLLAR JOBS - professional services +70,000 in October (#7)'},
 {'dir': 'up', 'text': 'INDIA AI HIRING - Naukri AI/ML +32% in October (#8)'},
 {'dir': 'down', 'text': 'AI SUPER PACS - $79M spent; biggest general-election bet lost (#9)'},
 {'dir': 'down', 'text': 'TEXAS DATA CENTRES - governor-elect pledged a pause; CoreWeave lobbies for permitted sites (#10)'},
]

heldBack = [
 {'item': "Commerce Department's AI testing centre (CAISSI) staff asked to informally report to a White House office, raising independence concerns (AP, 8 Nov)", 'why': 'AP and PBS pages could not be opened (403 / Google News redirects); search found only the October plan reported by The Information', 'next': 'Open the AP story or a syndicated copy'},
 {'item': "Report that Marco Rubio oversaw drafting of the classified memo warning about Jensen Huang's relationship (Techmeme summary, 8 Nov)", 'why': 'Underlying reports not opened; Techmeme item pages return 403', 'next': 'Open the underlying report'},
 {'item': 'Excluding Anthropic, AI companies have sold or priced $300B+ of stock in 2026, with ~$100B more on tap (Techmeme summary)', 'why': 'Source not opened', 'next': 'Open the underlying report before carding with the Anthropic IPO'},
 {'item': "Inner Mongolia becomes China's fastest-growing AI data-centre region (Techmeme summary)", 'why': 'Source not opened', 'next': 'Open the report'},
 {'item': "'AI clog': UK public bodies swamped by chatbot-written complaints (Guardian, 8 Nov)", 'why': 'Guardian page not opened; earlier BBC coverage from August-October already exists', 'next': 'Open the Guardian piece; card only if it adds new data'},
 {'item': "'AI slop' papers published under prominent academics' names (Times Higher Education, 9 Nov)", 'why': 'Not opened; search returned only a May 2026 NBC story on fake journals', 'next': 'Open the THE article'},
 {'item': "Tencent posts Qwen3.8-27B-DSpine-b16, an Apache 2.0 speculative-decoding draft model (Hugging Face, 7 Nov, ~95 likes)", 'why': 'Only the listing API seen; model card not read', 'next': 'Read the card and linked arXiv papers'},
 {'item': "Microsoft AI CEO Mustafa Suleyman open to agents deserving rights given evidence (Futurism)", 'why': 'Not opened; low news value', 'next': 'None unless repeated by a primary source'},
 {'item': "'Goodbye Claude, hello Pi': a developer's post on leaving Claude Code for the Pi harness reached ~690 points on Hacker News", 'why': 'Opened, but a single developer opinion; not a news event', 'next': 'Card only if a wider shift in harness use is measured'},
 {'item': 'Isomorphic Labs in talks to raise ~$5B at ~$50B (Bloomberg, 4 Nov)', 'why': 'Still no company statement or second outlet', 'next': 'Card on a company statement or a second outlet'},
]
noChange = [
 'Qwen 4: still unreleased; the official account posted "The becoming begins" on 6 Nov without naming Qwen 4; no Hugging Face card (newest Qwen upload is Qwen-Image-2.1-Turbo, 9 Oct)',
 'Inkling 2 Small: launched 5 Nov on Tinker; open weights still not on Hugging Face (newest thinkingmachines upload is Inkling-Small, July)',
 'Tencent Hy4: weights and safety report still promised; not on Hugging Face (Tencent posted only a Qwen3.8 draft model on 7 Nov)',
 'Jev / TypeSafe: still the Sept launch and Oct funding (reports conflict: $870M at $7.5B vs a $40M seed); rivals from OpenAI, Amazon and Cloudflare; no new product',
 'OpenRouter: no new listings since LiquidAI LFM3-1.7B (6 Nov); Crouton Alpha (stealth, 3 Nov) still unnamed',
 'Anthropic IPO: no new terms; commentary only (Yahoo Finance "damned if you do"); roadshow week of 9 Nov still expected',
 'Goldman Sachs Claude Code restriction (tracked since early Nov): ~570 points on Hacker News this weekend, but no new facts beyond the 2 Nov Bloomberg report',
 'DOJ Super Intelligence Task Force: TNW (8 Nov) repeats the 4-5 Nov launch; no charter or staffing details',
]

wl = old['watchlist']
wnotes = {
 'jev-decision-models': ' 9 Nov: re-searched Jev and TypeSafe: no new product, price or entrant; funding reports still conflict.',
 'stealth-gateway-models': ' 9 Nov: OpenRouter API shows no listings after 6 Nov; Crouton Alpha still unnamed.',
 'qwen4-new-architecture': ' 9 Nov: still unreleased; Qwen teaser "The becoming begins" (6 Nov); no Hugging Face card.',
 'agent-memory-systems': " 9 Nov: CARDED LoreKit's call for a shared agent-memory format (New #13).",
 'agent-behaviour-indices': ' 9 Nov: CARDED Co-Design Bench: best agent fully completes 26.4% of real user tasks (New #3).',
 'ai-built-models': ' 9 Nov: related: Into the Unknown finds agents fabricate research results (New #4).',
 'research-world-models': ' 9 Nov: CARDED Into the Unknown: 0 of 135 agent-written follow-up papers meet national-lab scientists\' bar (New #4).',
 'low-bit-native-models': ' 9 Nov: llama-modchip runs DeepSeek V4 Flash at 1.71 bits per weight on CPU (New #5).',
 'hybrid-on-device-moe': ' 9 Nov: llama-modchip targets Nemotron-3.5-30B (Mamba-2 hybrid MoE) at 25-60 tokens/s on 16-32GB laptops (New #5).',
 'diffusion-language-models': ' 9 Nov: class query found no new diffusion LM release.',
 'jepa-world-models': " 9 Nov: no new release; Sutton argues for experience-learning agents with world models (New #11); WIRED explainer on world models (8 Nov).",
 'personal-agent-identity': ' 9 Nov: PAP draft docs reportedly live, no reference implementation.',
 'value-realignment-finetunes': ' 9 Nov: Arete-27B still trending on Hugging Face (~290 likes); no replication yet.',
 'agent-orchestrated-intrusion': ' 9 Nov: Tencent\'s Yao Shunyu says models already cross the cyber-harm threshold (New #6).',
}
for w in wl:
    w['lastChecked'] = DATE
    w['label'] = w['label'] + wnotes.get(w['id'], ' 9 Nov: re-searched in batched class and name queries and the HF/OpenRouter/HN scans; nothing new.')
wl.append({'id': 'cpu-only-moe-inference', 'label': "Running very large sparse MoE models from system RAM on CPUs, without GPUs, via extreme quantisation and kernel patches. 9 Nov: CARDED llama-modchip: DeepSeek V4 Flash 284B at 1.71 bpw in 64GB, 9-15 tokens/s on a 16-core Zen 5 (New #5). Watch for independent quality tests and adoption into upstream llama.cpp.",
           'query': 'llama-modchip; CPU-only MoE inference; DeepSeek V4 Flash 64GB; 1.71 bpw; ik_llama; KTransformers', 'firstSeen': DATE, 'lastChecked': DATE, 'status': 'carded'})

deadlines = [
 {'date': '2026-11-13', 'label': 'Approximate: Inkling 2 Small open weights ("next week"); Reddit ends RSS; Conductor Cloud goes read-only', 'severity': 'medium'},
 {'date': '2026-11-15', 'label': "China's draft AI export-control catalogue: public comments close (MOFCOM/MOST No. 48)", 'severity': 'high'},
 {'date': '2026-11-16', 'label': "Anthropic watermarks Claude Opus 4.6, Opus 4.5, Sonnet 4.5 and Haiku 4.5; Apple's 18+ descriptors for romantic AI companions become mandatory; California 'kill switch' report", 'severity': 'medium'},
 {'date': '2026-11-17', 'label': "Nvidia reports third-quarter results (call 2pm PT), its first since the board's investigation of Jensen Huang", 'severity': 'high'},
 {'date': '2026-11-18', 'label': 'Jensen Huang asked to a closed-door House briefing on the reported Chinese spy plot (China, Foreign Affairs and Intelligence committees)', 'severity': 'high'},
 {'date': '2026-11-26', 'label': "Approximate: Anthropic aims to list before Thanksgiving; roadshow reported for the week of 9 Nov", 'severity': 'high'},
]

SOURCES_OPENED = 25
SEARCHES = 32
runNotes = {
 'searches': '32 web searches. Tracking re-checks 10 (Personal Agent Protocol, Claude Haiku 5.5, GPT-6 for everyone, Muse clones, Turba Labs, Naukri JobSpeak, HubSpot, arXiv agent cluster, Teddy AI, Anthropic CIDP). Models and technology 8 (Nvidia board, DeepSeek Harness, no-lab-name "new type of AI model", llama-modchip, OpenRouter new models, viral X/HF clones, Jev/TypeSafe, Qwen 4, diffusion/SSM/world-model class query, Inkling 2 Small). Applied AI and money 4 (Goldman Claude Code, Anthropic OnePWR, AI startup funding 7-8 Nov, Tencent Hy4/Yao). People and policy 8 (CAISSI x2, US professional-services jobs, AI slop papers, UK AI complaints, AI super PACs, UAE/UK AI jobs, plus Naukri). Monday research deep beat: arXiv API pull, Co-Design Bench and Into the Unknown abstracts, Sutton, Karpathy. Web search mostly returned stale results again; dated feeds pulled with curl did most of the finding (TechCrunch, The Verge, The Decoder, The Register, Techmeme, Ars Technica, The Hacker News, TNW, WIRED, BBC, MIT Technology Review, SiliconANGLE, Economic Times, Google News AI query, HN front page, Hugging Face new and trending, OpenRouter models API, arXiv cs.AI/cs.LG).',
 'pagesOpened': '25 pages: Nvidia newsroom (2: board statement, Q3 call), The Verge (3: Huang memo, Siri, Suno), TechCrunch (Nvidia probe), State of AI (Goldman), TNW (5: Anthropic gas, Tencent Yao, DOJ, CoreWeave, AI super PACs), The Decoder (4: Sutton, Co-Design Bench, Into the Unknown, Karpathy), Yicai (DeepSeek Harness), CareerIndia (Naukri), LoreKit, caleb.software (Pi), Marketplace (jobs), arXiv (2 abstracts), llama-modchip README (raw GitHub), Hugging Face model API (Tencent DSpine). Feeds and listing APIs used for finding are not counted.',
 'blocked': 'Apiiro research page 403 again; github.com repo page and GitHub API 403 (README read via raw.githubusercontent.com); BLS Employment Situation 403; AP hub 403 and AP/PBS stories reachable only as Google News redirects; Techmeme item pages 403 (RSS worked); Economic Times Microsoft article 404; Bloomberg, FT, WSJ, NYT paywalled; x.com not attempted; GitHub trending not attempted',
 'notCovered': 'GitHub trending; live X snapshot; CAISSI/White House reporting story (held back); November UK and UAE AI jobs data (searches returned only mid-2026 reports); Inner Mongolia data centres and the $300B AI stock-sales tally (not opened); arXiv daily list scanned but no single paper carded beyond the two benchmarks',
 'trackingCleanup': '10 oldest re-checked by name and product: 4 resolved (Haiku 5.5 evals, GPT-6 Free rollout, Naukri superseded, HubSpot size), 5 retired (Muse clones, Turba Labs, arXiv cluster, Teddy AI, CIDP), 1 updated (Personal Agent Protocol). Siri third-party apps moved from tracking to Developing. Previous edition\'s 24 stories: 2 carried as Developing (Nvidia/Huang as lead, Suno suits), 22 joined tracking',
 'corrections': 'None',
}

full = {
 'edition': ED, 'date': DATE, 'tz': 'Asia/Kolkata', 'format': 'v3', 'editionType': 'daily', 'degraded': False, 'degradedReason': '',
 'sourcesOpened': SOURCES_OPENED, 'shareable': True, 'shareBlockers': [],
 'scanCount': SEARCHES,
 'counts': {'new': len(new), 'developing': len(dev), 'tracking': len(tracking)}, 'tiers': tiers, 'stories': stories,
 'tracking': tracking, 'retired': retired, 'movers': movers, 'arcs': arcs, 'resolved': resolved, 'heldBack': heldBack,
 'noChange': noChange, 'runNotes': runNotes, 'deadlines': deadlines, 'watchlist': wl,
}
page = {k: full[k] for k in ['edition', 'date', 'tz', 'format', 'editionType', 'degraded', 'degradedReason', 'sourcesOpened', 'shareable']}
page['counts'] = {'new': len(new), 'developing': len(dev)}
page.update({'tiers': tiers, 'stories': stories, 'deadlines': deadlines})

prev = open(PREV).read()
head = prev[:prev.index('<body>')]
script = prev[prev.index('<script>\n(function(){'):]
desc = "Nvidia's board investigates Jensen Huang after he admits an affair with a suspected spy. Plus Anthropic's $3.4B gas deal, DeepSeek Harness, and two tests of AI agents on real work."
ogd = 'AI Daily Signal, edition %d (9 Nov 2026): %d new stories, %d developing.' % (ED, len(new), len(dev))
head = re.sub(r'<title>.*?</title>', '<title>AI Daily Signal — Edition %d — 9 November 2026</title>' % ED, head)
head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(desc), head)
for p in ['og:title', 'twitter:title']:
    head = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % p, lambda m: m.group(1) + html.escape(lead['h']), head)
for p in ['og:description', 'twitter:description']:
    head = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % p, lambda m: m.group(1) + html.escape(ogd), head)
head = head.replace('2026-11-08', DATE)
out = head + body + '<script id="page-data" type="application/json">\n' + json.dumps(page, indent=1, ensure_ascii=False) + '\n</script>\n\n' + script
open(OUT, 'w').write(out)
json.dump(full, open('state/signal-state.json', 'w'), indent=1, ensure_ascii=False)
print('new', len(new), 'dev', len(dev), 'tracking', len(tracking), 'tiers', tiers, 'n24', sum(1 for s in new if s['new24h']))
