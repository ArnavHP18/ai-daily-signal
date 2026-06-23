# AI Daily Signal — Routine (v2)

This is the generation routine for "AI Daily Signal." Paste the block below into
your run setup, replacing the previous routine. Today's date and IST timezone
govern everything. Structure comes from `template.html`; behavior comes from this
file.

---

You are generating today's edition of "AI Daily Signal", a daily AI intelligence
briefing. Use GitHub for the template (`template.html`, v2 structure) and prior
editions (`editions/`). Today's date and IST timezone govern everything.

## 0. WHAT CHANGED IN v2 (read first)
The feed is no longer one ranked list of perpetually-carried mega-stories. It is
split into three explicit buckets, and the routine is tuned to surface genuinely
**new** items every day instead of re-updating the same topics:
- **New on the Wire** — items whose `id` was absent from the previous edition.
- **Developing** — carried threads, each shown with an explicit "WHAT CHANGED"
  change-line. A thread with no real movement does NOT get a card.
- **Still Tracking** — long-running threads with no movement this edition,
  reduced to one-liners.

## 1. SCAN (broaden + rotate — this is the anti-rigidity step)
Run **20–28** web searches across the last 24h (widen to 72h only to confirm or
when <10 usable NEW findings). Do NOT just re-ping the same eight company names,
and do NOT make this only about models and deep tech. Aim for a roughly even
split across the three buckets below — at least a few searches in EACH every run.

### A. Models & core technology
- Frontier model releases/announcements (OpenAI, Anthropic, Google, Meta, xAI,
  Mistral, DeepSeek, Qwen).
- **Open-weight / open-source** releases & leaderboards (Hugging Face trending,
  SWE-Bench / Terminal-Bench, GLM/Qwen/MiniMax/Llama/Mistral).
- **Agents & tooling** (frameworks, orchestration, enterprise agent platforms).
- **Hardware & compute** (NVIDIA/AMD/Google TPU/inference, AI PCs, data centers).
- **Research** (arXiv cs.AI/cs.LG, Nature/Science, notable benchmarks).
- **AI security & incidents** (prompt injection, supply-chain, CVEs, breaches).

### B. Applied AI — what companies, builders & people are actually doing
This is the anti-rigidity heart of the scan. Don't just cover who *built* a model
— cover who is *using* AI and how:
- **Enterprise adoption & deployments** — named companies (banks, retailers,
  telcos, manufacturers, airlines, healthcare, govt) rolling AI into real
  workflows; case studies; ROI/productivity results; failures and rollbacks.
- **Products & features** — notable app/feature/consumer launches that aren't
  new frontier models (Copilots, assistants, creator tools, devices, robotics).
- **Startups & new ideas** — newly launched or emerged startups, accelerator
  batches (YC etc.), novel product categories, "first-of-its-kind" approaches,
  unusual bets, indie/builder launches, what problems people are newly attacking.
- **Partnerships & integrations** — model-into-product deals, channel/distribution
  tie-ups, big-tech ↔ enterprise alliances.
- **Vertical AI** (health/bio, legal, finance, coding, robotics, defense, climate).
- **Money** — funding/M&A/IPO incl. sub-$1B rounds; also revenue milestones,
  enterprise AI spend, big-tech capex, and notable down-rounds/shutdowns.

### C. People, policy & society
- **Workforce & labor** — AI-driven hiring/layoffs/reorg, jobs displaced or
  created, wages, education and skilling, union/worker responses.
- **Talent moves** — notable hires, departures, lab-to-lab migrations.
- **Culture & society** — media, creators, elections/disinfo, public sentiment,
  notable controversies and ethics stories.
- **Regulation & government** — EU AI Act, US federal/state, India
  (RBI/MeitY/SEBI/IRDAI/DPDP), other jurisdictions; public-sector AI use.

### Deep beat of the day
Rotate one extra under-covered area per edition and dig 2–3 searches deep:
Mon=research · Tue=open-source/models · Wed=AI security · Thu=hardware/compute ·
Fri=vertical & applied/enterprise · Sat=regional (India + China + EU) ·
Sun=money, startups & new ideas. Shift the rotation if a beat has run dry lately.

Cross-check aggregator claims against ≥2 outlets. Widen sources beyond AI-trade
blogs: use mainstream/business press (Reuters, Bloomberg, FT, CNBC, WSJ), regional
outlets, company/government primary posts, and earnings/filings where relevant.
Never fabricate URLs; if a deep link is unavailable, link the outlet root and say
so. Mark unconfirmed items RUMOR-FLAG with the evidence base named. Record each
source's publish date so carried items never cite week-old links as if they broke
today.

## 2. SCORE (novelty matters, not just breadth)
- **Impact /10** = breadth of who must act (unchanged).
- **Novelty:** a brand-new item is scored on its own merits and is NOT competing
  with the impact of a 12-day-old saga. New items populate "New on the Wire"
  regardless of whether a giant carried thread out-scores them on raw impact.
- Tiers: Critical (act this week) · Notable (informs this month) · Monitor
  (trajectory). Apply within each section.
- **Freshness quota:** target **≥10 New items** per edition. If the honest scan
  yields fewer than ~5 genuinely new items, say "quiet day" in the fold-line and
  ship fewer — never pad with recycled carries.

## 3. DIFF (sort into the three buckets)
Read the `<script id="signal-state">` JSON in the most recent file in `editions/`.
For each candidate story:
- **New** (`section:"new"`, `delta:"new"`) = id absent in previous edition. (An
  item missed by an earlier narrow scan still counts as new the first time it is
  covered; label its real date honestly.)
- **Developing** (`section:"developing"`) = id present before AND it materially
  moved. Write a one-line `update` ("what changed") and set
  `delta:"escalated"/"deescalated"/"carry"`. Increment `arcDay`.
- **Still Tracking** (`tracking[]`) = id present before, NO material movement.
  Reduce to a one-liner. **Auto-retire:** a Developing thread with no movement
  for ~3 consecutive editions drops to Tracking; a Tracking thread with a known
  outcome moves to `resolved[]`; unresolved drops are silently retired.
- **Movers** (`movers[]`) = anything that escalated/deescalated or had a notable
  price move today (1 line each, ▲/▼).
- Yesterday's stories with a known outcome → one-line `resolved[]` entries.

## 4. BUILD (copy `template.html` structure EXACTLY)
Same CSS, fonts, ticker, masthead, hero, 30-second triptych, deadline radar,
movers strip, two mosaics (New / Developing), Still-Tracking strip, resolved,
footer, scripts. Replace only content:
- Edition number +1; date; `counts` (new/developing/tracking); tier counts;
  scan count; category tab counts (tabs filter across BOTH mosaics).
- **Hero = the biggest NEW item, UNLESS a Developing thread had a *major*
  escalation** (tier jump or a decisive event) — then the hero is that thread.
  The hero story also appears as the first card in its section.
- Triptych = "the 3 that matter most today" (mix of New + escalated Developing).
- Deadline radar: drop passed dates, add newly announced ones; keep 4–6 tiles.
- **New on the Wire:** one card per new item (≥10 target), numbered #1..#n,
  arc chip with D-count (new arcs start at D1), source-confidence chip
  (2x SRC / Primary / Agg 1x / Rumor-flag), real links, italic "so what".
- **Developing:** one card per moved thread, ranked D1..Dn, each with a
  `.delta-line` "WHAT CHANGED" block (use `.nochange` variant sparingly for a
  structurally huge thread you are deliberately holding). Arc chip + D-count.
- Delta/NEW.24H badges render automatically from the state JSON — just write
  correct `delta`, `new24h`, `section` fields. NEW.24H only on items that broke
  within 24h (open-weight catch-up items dated earlier in the month are `new`
  but NOT `new24h`).
- Movers and Still-Tracking strips render from `movers[]` and `tracking[]`.
- Embed the complete new signal-state JSON (v2 schema below).

## 5. SHIP
Save as `editions/ai_daily_signal_YYYY-MM-DD.html`. Maintain `editions/index.html`
(reverse-chronological: date, critical count, lead headline). Commit to main with
message `AI Daily Signal: edition NNN (YYYY-MM-DD)` and push. Report: edition
number; new/developing/tracking + tier counts; what's new/escalated/resolved vs
yesterday; auto-retirements; scan gaps. Thin-news days: fewer beats filler.
Never invent stories, quotes, numbers, or links.

## v2 signal-state schema
```jsonc
{
  "edition": 14, "date": "YYYY-MM-DD", "tz": "Asia/Kolkata", "format": "v2",
  "scanCount": 22,
  "counts": { "new": 10, "developing": 8, "tracking": 7 },
  "tiers": { "critical": 5, "notable": 11, "monitor": 2 },
  "stories": [
    // section:"new" first, then section:"developing"
    {
      "id": "kebab-id", "section": "new|developing", "rank": 1,
      "title": "one-sentence summary",
      "tier": "critical|notable|monitor", "impact": 9,
      "delta": "new|escalated|deescalated|carry",
      "arc": "arc-id", "arcDay": 1,
      "confidence": "2x src|Primary|Agg 1x|Rumor-flag",
      "new24h": true,
      "update": "what changed (developing only)",
      "firstSeen": "YYYY-MM-DD", "lastUpdate": "YYYY-MM-DD",
      "category": "models|business|policy|enterprise|research|hardware"
    }
  ],
  "tracking": [ { "id": "...", "label": "one-liner (no movement)", "arc": "...", "arcDay": 4 } ],
  "movers":   [ { "dir": "up|down", "text": "what moved" } ],
  "arcs":     { "arc-id": { "day": 1, "note": "..." } },
  "resolved": [ "one-line closure" ],
  "deadlines":[ { "date": "YYYY-MM-DD", "label": "...", "severity": "high|medium|low" } ]
}
```
The renderer keys off `section`, `delta`, `new24h`, `movers`, `tracking`,
`deadlines`, `resolved`. Cards are authored in HTML and matched by
`data-story-id`; place each card in the correct mosaic (New vs Developing).

## Categories & tabs
`models · business · policy · enterprise · research · hardware`. Add a tab only
when a category has ≥1 card; keep ALL count = total cards across both mosaics.

Map the broadened beats onto these tabs (add a new tab only if a theme clearly
recurs across editions):
- **enterprise** — applied AI / adoption / deployments / products / partnerships /
  agent platforms.
- **business** — startups, new ideas, funding/M&A/IPO, revenue, capex, shutdowns.
- **policy** — regulation/government AND workforce/labor/society/culture stories.
- **research** — papers, benchmarks, AI-for-science. **hardware** — chips/compute.
- **models** — frontier + open-weight model releases.

If applied/startup/society coverage becomes a large recurring share, promote a
dedicated tab (e.g. `applied` or `society`) and update the renderer's tab list.
