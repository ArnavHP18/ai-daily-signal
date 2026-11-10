# AI Daily Signal — Routine (v4)

This is the generation routine for "AI Daily Signal." Today's date and IST timezone
govern everything. Design comes from `template.html` (rendered by `scripts/render.py`);
behavior comes from this file. The scheduled-task prompt is in `ROUTINE_PROMPT.md`.
Where v4 (section 0.00) conflicts with anything below, v4 wins; then v3 (section 0.0).

---

You are generating today's edition of "AI Daily Signal", a daily AI intelligence
briefing. Use GitHub for the template (`template.html`, v2 structure) and prior
editions (`editions/`). Today's date and IST timezone govern everything.

## 0.00 WHAT CHANGED IN v4 (read first; overrides everything below)
Added on 10 Nov 2026 (edition 139). The reader is a tech professional anywhere in the
world, working in banking, who uses this as their main daily news source. The goal:
identify, research and explain new AI advances and what major and niche tech companies
ship, and summarise everything else important that happened, with banking first among
the non-tech areas.

### The daily workflow
1. **Collect.** `python3 scripts/collect.py` (about 1 minute). It pulls every source in
   `config/sources.json` and every company in `config/companies.json`, and writes
   `_working/collect/DATE/digest.md`. **Read the digest first.** It holds top stories by
   topic, product updates per company (new official changelog entries, headline mentions,
   and what people are saying on YouTube, Reddit and Hacker News), developer signals,
   and "What are we missing?". Nothing in it is verified.
2. **Search and check.** Use the 20–40 web searches for verification, the deep beat, the
   10 tracking re-checks and the watchlist (below), not for basic discovery. Open every
   page you cite with curl, as before.
3. **Next-day accuracy check.** Before writing anything new, re-check every Critical and
   Notable story in the previous edition against new reporting. Record one `followups[]`
   entry each: `{id, label, status, note, url?}`, with `status` one of `confirmed`
   (nothing contradicts it), `changed` (moved; say how), `corrected` (we got something
   wrong: also add a plain sentence to `corrections[]`, shown in the footer), `unresolved`
   (still unclear) or `quiet` (no new reporting). A story that moved materially can also
   become a Developing card.
4. **Write the edition as data.** Write `editions/data/DATE.json` (format below) and only
   the bookkeeping parts of `state/signal-state.json`: tracking, watchlist, retired,
   resolved, movers, heldBack, noChange, runNotes (including `runNotes.missing`). Do not
   hand-write HTML pages and do not write per-day builder scripts.
5. **Render.** `python3 scripts/render.py DATE` checks the data file, renders the page from
   `template.html`, and writes the edition-level fields of the state file (edition, date,
   flags, counts, tiers, stories, deadlines, arcs). Fix whatever it reports and re-run.
6. **Build.** `python3 scripts/build_site.py` archives stale tracking items, checks the
   edition (all v3 checks, swipe fields, data file vs page, follow-ups,
   `runNotes.missing`, watchlist size), and rebuilds the archive, search index, share
   card, swipe-app feed, storyline pages and quality log. **Do not commit if it fails.**
7. Commit everything it wrote (including `state/collector-state.json`, which lets the
   collector find only new changelog entries tomorrow), push, report.

### Coverage: everything worth knowing, global, by importance
This is the reader's main daily news source, read each morning: AI and technology first,
plus finance (banking above all), business, health, energy, world affairs, society,
sports and entertainment. It covers what happened since the last edition (wider on
catch-up days), not live news.
- **Region-agnostic.** Rank by importance worldwide; there are no regional quotas. World &
  politics is global. Regional sources exist so important news from anywhere is found.
  This replaces the hotspot list and the daily city-by-city jobs searches in §1.C.
- **As many stories as the day has.** 10, 20, 30, 40 or more: card everything important
  the sources produced, and nothing padded. The minimum is still 10 new (fewer means quiet
  day or catch-up, §0.0.7). Quality over quantity, but nothing important missed.
- **20 categories in 7 areas** (`config/categories.json`; the page shows area tabs, then
  the categories in that area):
  - Money & finance: `banking` (the reader's main focus) · `payments` (payments & fintech)
    · `insurance` · `markets` (markets & economy) · `crypto` (crypto & digital assets)
  - AI & technology: `models` (AI models & labs) · `products` (products & builders: what
    shipped and what people build with Claude, Cursor, Grok, Gemini and other tools) ·
    `research` (research & science) · `hardware` (hardware & chips) · `security` ·
    `robotics` (robotics & autonomy) · `emerging` (quantum, space, biotech, BCIs, new computing)
  - Business: `business` (business & startups, including enterprise adoption)
  - Health: `health` (health & medicine)
  - Energy & climate: `energy`
  - World & society: `policy` (policy & regulation) · `world` (world & politics) · `society`
    (society & culture: work and jobs, education, media, online life)
  - Sports & entertainment: `sports` · `entertainment`
- **Sources: at least 10 healthy per category** (`config/sources.json`, 282 today).
  `python3 scripts/check_sources.py` tests every source and prints the count per category;
  run it every Sunday and whenever sources change, drop or replace failing ones, and add
  new sources only after they pass. Prefer original reporting and official sources over
  rewrite sites.
- **AI jobs and work** are a global `society` topic: card hiring and layoff data when a real
  release lands, not from daily searches.
- **Builders and ideas.** In `products`, include notable things people built with AI tools
  (Show HN, Product Hunt, r/ClaudeAI, r/LocalLLaMA, specialist blogs) when they are new
  ideas worth copying; say plainly what was built and with what.
- **Deep beat:** Mon research & AI models · Tue products, builders & open source · Wed
  security · Thu hardware, energy & emerging tech · Fri banking, payments & insurance ·
  Sat markets, business & world · Sun week in storylines (and the automatic "This Week in
  Products" roundup; also re-search "weekly" watchlist entries and run check_sources.py).

### Product updates (every edition)
- For each company in `config/companies.json` (mainstream and niche, all of its
  technology, not only AI) that shipped something in the window, add an entry to
  `productUpdates[]`: `{company, updates:[{text, url, date, source}], reactions:[{kind,
  title, url, note?}]}`.
- **updates** are what shipped: one plain line each, linked to the official changelog,
  newsroom or release notes. A report of a launch is acceptable when no official page
  exists (name the outlet in `source`).
- **reactions** are what people are saying: 1–3 of the most useful YouTube videos, Reddit
  threads and Hacker News discussions. Kinds are `video | reddit | hn | news | post`.
  Prefer hands-on tests, comparisons and real problems over hype titles. A reaction is
  never a fact: if it claims something (a bug, a hidden cost, a leak), say "unconfirmed"
  in `note`, or check it and make it a story.
- **Keep each update short:** one line, under about 100 characters. The swipe app shows
  two lines per update and cuts the rest.
- **Blocked or silent changelogs.** Some official changelogs refuse automated fetches (the
  digest shows `(failed: ... 403)` under the company; x.ai's Grok Bot changelog always
  does). For those companies, and for any major company whose products ship weekly but
  show no official entry in the digest (xAI's Grok Bot and Grok Build, for example),
  search the news for the product names over the last 7 days and list what shipped from
  the reports (name the outlet in `source`, e.g. "TeslaNorth, citing the official @bot
  account"). Never conclude "nothing shipped" from a failed or blocked source.
- **Catch-up window for product updates:** an item from the last 7 days that no earlier
  data file listed may be added, with its real date; it is not repeated after that.
- **Leave out** companies with nothing shipped. A big launch is also a story card.
- On Sundays (or with `"weeklyRoundup": true`) the renderer adds "This Week in Products"
  from the last seven data files automatically.

### "What are we missing?" (every edition)
The digest lists unmapped trends (topics in 3+ sources that match no company, storyline,
watchlist entry or recent story), outlets cited often that are not in our sources, and
companies in the news but not in our directory. Act on each one: card it, add it to
`config/companies.json`, `config/sources.json` or the watchlist, or explain why not.
Summarise in `runNotes.missing` (required). Remove sources that keep failing.

### Tracking, watchlist and storylines
- `build_site.py` archives tracking items with no check or movement for 14 days to
  `state/archive/tracking.json`. Re-check the 10 oldest remaining items each run (§0.0.8).
- The watchlist has at most **20 `cadence: "daily"`** entries, re-searched every run;
  the rest are `"weekly"`, re-searched on Sundays. Promote or demote as activity changes.
- Every story belongs to a storyline (`arc`). New storylines need a reader label in
  `arcLabels` (e.g. `"chip-export-enforcement": "who can buy top AI chips"`). Each one
  gets a page in `storylines/`, linked from every card; readers can follow storylines in
  the swipe app.

### Edition data file (`editions/data/DATE.json`)
```jsonc
{
  "format": "edition-v1", "edition": 140, "date": "YYYY-MM-DD",
  "editionType": "daily|catch-up", "degraded": false, "degradedReason": "",
  "sourcesOpened": 30, "scanCount": 28, "shareable": true, "shareBlockers": [],
  "lead": "story-id",                       // a new story, or a Developing one with a major escalation
  "leadRef": "one line for the 'see above' row",
  "description": "meta description, one or two sentences",
  "thirtySecond": [ {"id": "story-id", "h": "3-6 words", "p": "one sentence"} ],   // exactly 3, never the lead or a rumour
  "footerNote": "the deep beat in a sentence or two",
  "arcLabels": { "new-arc-id": "reader label" },
  "deadlines": [ {"date": "YYYY-MM-DD", "label": "...", "severity": "high|medium|low"} ],
  "stories": [ {
    "id": "kebab-id", "section": "new|developing", "tier": "critical|notable|monitor", "impact": 7,
    "delta": "new|escalated|deescalated|carry", "update": "what changed (developing only)",
    "arc": "arc-id", "arcDay": 1, "confidence": "Primary|2x src|Agg 1x|Rumor-flag", "verified": "opened|snippet",
    "new24h": true, "firstSeen": "YYYY-MM-DD", "category": "one of the 20 category ids",
    "title": "one-sentence summary (state file and search)",
    "h": "card headline", "sub": "one sub-line (required for the lead)",
    "cat": "Models · open models · 9 Nov", "tickerKey": "SHORT KEY", "ticker": "ticker line ('' for rumours)",
    "body": "<p class=\"dek\">...</p><p class=\"sowhat\">So what: ...</p>",   // allowed tags: p div strong em b i code a span br ul ol li
    "chip": "what we checked, in plain words",
    "src": [ ["OFFICIAL", [["label", "https://..."]]], ["REPORTING", [...]], ["OTHER", [...]], ["AGGREGATOR", [...]] ],
    "brief": "<p>...</p>", "facts": [["What", "..."]], "impactWho": "...",     // the lead only
    "short": "35-60 word card summary", "stat": {"value": "-4.27%", "label": "..."},
    "image": {"url": "https://official-source/og-image.png", "credit": "Nvidia"}  // swipe fields, §16a
  } ],
  "productUpdates": [ ... ], "followups": [ ... ], "corrections": [ "..." ]
}
```
Order stories with section `new` first (in rank order), then `developing`. The renderer
numbers them, places the lead in the hero, gives the next two new stories large cards and
everything else compact rows, and omits Developing when there is none.

## 0.0 WHAT CHANGED IN v3 (read first; overrides everything below)
Added after edition 127, where no source page could be opened, the first build led
with company-only claims and listed a real Node.js CVE as a rumour.

### Where things live
- `state/signal-state.json` is the single source of truth for bookkeeping: stories,
  tracking (with `since` / `lastChecked`), watchlist, arcs, deadlines, movers, resolved,
  retired, `heldBack[]`, `noChange[]` and `runNotes{}`. Read it at the start of every run
  (it replaces "the signal-state JSON in the most recent edition") and overwrite it at
  the end. Git history is the archive of past states.
- `state/REVIEW.md` is generated from it by the build script, for human review. Never
  edit it by hand.
- Each edition page shows reader content only and embeds a small
  `<script id="page-data">` (fields listed in `template.html`). Tracking, watchlist,
  movers, resolved/retired, held-back notes, scan stats and method notes are NOT
  rendered on the page.

### Trust
1. **Open sources, don't just search.** Fetch the pages you cite with `curl -sSL
   --max-time 30 URL` in Bash (it uses the session proxy). The WebFetch tool has failed
   with DNS errors in every run so far. Pick at least the lead's primary source and
   one source for each Critical or Notable item. Record the number you opened as
   `sourcesOpened`, and mark each story `verified: "opened"` or `"snippet"`.
2. **Degraded editions.** If fewer than half of the Critical and Notable stories
   could be checked against an opened page, set `degraded: true` with a plain
   `degradedReason`. The page then shows a yellow DEGRADED EDITION banner. If
   *nothing* could be opened, ship only stories confirmed by an official source you
   did open; if there are none, skip the day and say why in the run report.
3. **Status line.** It renders from state above the headline, e.g. "Catch-up edition ·
   Quiet day: 5 stories, none in the last 24 hours, 2 sources opened". Keep
   `editionType`, `counts`, `new24h` and `sourcesOpened` accurate; nothing else needed.
4. **Check the easy facts before shipping.** CVEs on the vendor's security page or
   NVD; model names, sizes and licences on the Hugging Face model card; prices on the
   vendor's pricing page; funding on the company's own post. If you cannot check one,
   say so on the card, and do not lead with it.
5. **Rumours.** A `Rumor-flag` story gets the `rumor` class (dashed, muted card), an
   "Unconfirmed" trust marker, and never appears in the ticker, hero, 30-Second Read
   or movers.
6. **Sharing gate.** Set `shareable: true` only when the edition is not degraded and
   the lead's main claim was checked on an opened primary source; otherwise
   `shareable: false` with `shareBlockers[]`. Anything that posts to X or elsewhere
   must read this flag (in `state/signal-state.json` or the page's `page-data`) and
   must not post when it is false.

### Content
7. **Searches: 20–40.** If the first 28 yield fewer than 5 items dated within 48h,
   spend up to 12 more on dated queries before calling it a catch-up day.
   `editionType: "catch-up"` when fewer than 5 stories broke in the last 48h; a
   catch-up edition carries nothing older than 30 days. If fewer than 3 checkable
   stories exist at all, skip the day and report it.
8. **Tracking hygiene, every run.** Re-search the 10 tracking items with the oldest
   `lastChecked` (missing counts as oldest; ties go to the oldest `since`). Each one
   is updated (`lastChecked` = today), moved to `resolved[]` if it has an outcome, or
   moved to `retired[]` with a reason if the re-search finds nothing new. These
   searches count toward the 40. Every tracking item carries `since` (the date it
   entered tracking) and, once checked, `lastChecked`. `state/REVIEW.md` lists the next
   10 due.
9. **Rank sources by type** on every card, in this order: OFFICIAL (the company,
   regulator, project or paper), REPORTING (outlets doing original reporting: Reuters,
   Bloomberg, WSJ, FT, TechCrunch, The Verge, trade press), OTHER (law firms, filings,
   analysts), AGGREGATOR (roundups, AI-news digests, rewrite sites). A story whose only
   sources are aggregators is "One secondary source" at best.
10. **Research, dev-attention and policy.** Use these when the network allows
    (`curl`): arXiv `https://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&sortBy=submittedDate&max_results=50`,
    Hacker News `https://hn.algolia.com/api/v1/search?tags=front_page`, GitHub
    trending `https://github.com/trending`, Hugging Face
    `https://huggingface.co/api/models?sort=createdAt&limit=50`, and the regulator
    pages for policy. arXiv rate-limits (HTTP 429): make one request, and if refused
    wait 5 seconds and retry once. If a source is blocked, say so in `runNotes.blocked`. No research
    story is better than an unchecked one: drop the category instead of padding it.

### Design (template.html v3)
11. Headline 12–15 words, plus one sub-line (`.subhead`). The masthead holds only the
    name, edition number, date and byline; stats and the beat note go in the footer.
12. The lead appears once (hero). The 30-Second Read sits right under it and shows
    the *next* three. The lead's slot in the feed is a one-line "see above" row.
13. The two highest-scoring stories after the lead get large cards; the rest go in
    the compact tap-to-expand list.
14. Plain words on the page: "Storyline: … · day N" (not "ARC … D1"), trust markers
    "Official source / Two or more outlets / One secondary source / Unconfirmed" (not
    "PRIMARY / 2x SRC / AGG 1x"). No routine jargon ("rev 2.1", "v2") in reader text.
15. Keep writing `movers[]` (`up` = rose or raised money, `down` = fell or a risk) to
    the state file; it is not shown on the page. Record items you could not check in
    `heldBack[]` and carried stories re-checked without movement in `noChange[]`.
    Search counts, pages opened, blocked hosts, gaps and corrections go in `runNotes{}`.
    A short public correction line goes in the page footer only when an edition is
    republished with a changed claim.
16. Omit the Developing section when no carried story moved.
16a. **Swipe view (`app/`).** Phones can read each edition one story per screen. The deck is
    the lead, then every Critical and Notable story; Monitor stories and all rumours go in an
    "Also today" list. For every deck story, write in the data file (v4; `render.py` copies them to the state file and `page-data`):
    - `short`: a plain-text summary of at most 60 words, written for the card (the key fact,
      the number that matters, and what is unconfirmed). Without it the build cuts the
      card's first paragraph, which reads worse.
    - `stat`: `{ "value": "-4.27%", "label": "Nvidia shares on Monday" }`, the one number
      the generated cover shows (keep the value to about 7 characters).
    - `image` (optional): `{ "url": "https://…", "credit": "Anthropic" }`, only the share
      image (og:image) of the story's OFFICIAL source page you opened. Never use news
      outlets' or agencies' photos, and never guess a URL. With no image, the card shows
      the generated `stat` cover. Rumours never carry an image.
    `build_site.py` fails the edition if a deck story lacks `short` (35-60 words, plain
    text) or `stat`, if a `stat` value is over 9 characters, if an image is not https or
    has no credit, if a rumour has an image, or if these fields differ between the page and
    the state file.

### Ship
17. (v4: run `python3 scripts/render.py DATE` first; see §0.00.) Then run `python3 scripts/build_site.py`. It checks the
    newest edition (JSON, tags, cards vs state, counts, tiers, headline length, rumour
    and sharing rules, swipe-card fields; page and state file describe the same edition) and rebuilds
    `state/REVIEW.md`, the archive (months, missed dates, search), the
    search index, the root redirect, the 1200×630 share card, and the swipe-view feeds
    (`app/feed.json` and `editions/feeds/DATE.json`). **Do not commit if
    it fails.** Commit everything it wrote together with the edition.

## 0. WHAT CHANGED IN v2
The feed is no longer one ranked list of perpetually-carried mega-stories. It is
split into three explicit buckets, and the routine is tuned to surface genuinely
**new** items every day instead of re-updating the same topics:
- **New on the Wire** — items whose `id` was absent from the previous edition.
- **Developing** — carried threads, each shown with an explicit "WHAT CHANGED"
  change-line. A thread with no real movement does NOT get a card.
- **Still Tracking** — long-running threads with no movement this edition,
  reduced to one-liners.

## 0.1 WHAT CHANGED IN rev 2.1
Added after edition 100 found that **Jev** (TypeSafe AI's decision-only "System One"
model, launched 15 Sep 2026) was missed for two weeks while it went viral: edition 097
carried only the company's seed round, and edition 099 retired it as "single-source"
although TechCrunch, The Register and Bloomberg had covered it. Four fixes, all
mandatory:
1. **Emerging-tech beat (1.E)** — every run searches for new *kinds* of AI, not just
   new releases from named labs.
2. **Re-search before downgrading** — nothing is labelled single-source, demoted or
   retired without first re-searching its entity name AND its flagship product name.
3. **Product-first scoring of money items** — a funding round is scored on the
   technology it funds, and the product is named in the card.
4. **Watchlist** — a standing `watchlist[]` of emerging approaches in the state JSON,
   re-checked every edition.
The user's primary objective for this briefing: **identify, research and give
insight on new and upcoming AI advancements.** When in doubt, favour the new
technique over the incremental release.

## 1. SCAN (broaden + rotate — this is the anti-rigidity step)
Run **20–40** web searches (see 0.0 §7) across the last 24h (widen to 72h only to confirm or
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

### E. Emerging tech & new paradigms (MANDATORY — at least 3 searches every run; counts toward A's share of the 20–28)
The lab list in A is how new *releases* are found; it is not how new *kinds* of AI
are found. A model from an unknown company, or one that isn't an LLM at all, will
match none of the named-lab queries. So every run also:
- Searches **without lab names**: "new AI model" / "new type of AI model" / "not an
  LLM" / "alternative to LLMs" / "new architecture" / "AI startup launches model",
  scoped to the last 7 days.
- Searches **new approaches by class**: decision / classification models (e.g. Jev),
  world models & JEPA, diffusion and other non-autoregressive LMs, state-space and
  hybrid architectures, small specialised models, neuro-symbolic, on-device models.
- Checks **developer-attention signals**, which lead the press by days: newly listed
  models on OpenRouter / Vercel AI Gateway / Cloudflare AI Gateway, Hacker News front
  page, GitHub trending, viral launch posts on X, and Hugging Face clones or
  "open-source X" re-implementations appearing (a burst of clones = real traction).
- Re-searches every entry in `watchlist[]` by name.
An emerging-tech item with measurable developer adoption (gateway listings, clones,
widely-covered launch) is **Notable at minimum**, even pre-revenue.

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
- **AI jobs market & hiring hotspots** — where AI roles are booming, by geography:
  **India** (Bengaluru, Hyderabad, Pune, NCR; GCCs/IT services), **US** (Bay Area,
  NYC, Seattle, Austin), **UK** (London), **UAE/Dubai & Abu Dhabi**, plus EU
  (Berlin/Paris), Singapore, Canada, Saudi. Track: hiring surges and freezes,
  in-demand roles (ML/AI eng, prompt/agent eng, AI product, data, AI safety),
  salary benchmarks, visa/immigration shifts, GCC and big-tech hiring drives,
  and which sectors/cities are adding vs cutting AI headcount. Sources: LinkedIn
  Economic Graph, Indeed/Naukri/Hired reports, Levels.fyi, Robert Half/Michael
  Page, government labor data, and regional business press.
- **Talent moves** — notable hires, departures, lab-to-lab migrations.
- **Culture & society** — media, creators, elections/disinfo, public sentiment,
  notable controversies and ethics stories.
- **Regulation & government** — EU AI Act, US federal/state, India
  (RBI/MeitY/SEBI/IRDAI/DPDP), other jurisdictions; public-sector AI use.

### Deep beat of the day
Rotate one extra under-covered area per edition and dig 2–3 searches deep:
Mon=research · Tue=open-source/models · Wed=AI security · Thu=hardware/compute ·
Fri=vertical & applied/enterprise · Sat=regional + AI jobs hotspots (India · US ·
UK · UAE/Dubai · EU · Singapore) · Sun=money, startups & new ideas. Shift the
rotation if a beat has run dry lately.

**Re-search before downgrading (rev 2.1).** Before any item is labelled
single-source / Agg 1x, demoted, or retired, run one search on the entity name AND
one on its flagship product or model name. If either returns new coverage, update
the item instead of downgrading it. "Single-source" means "one source after
re-searching", never "one source found by today's topic queries".

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
- **Product-first for money items (rev 2.1):** for any funding / M&A / valuation
  item, name the product or technology in the title and card, and score the
  technology's significance, not the round size. A small seed behind a genuinely
  new kind of model outranks a large round for an incremental one.
- **Novel approach bonus:** a new technique or model class (not a version bump)
  scores at least Notable when it has independent coverage or measurable developer
  adoption.
- **Freshness quota:** target **≥10 New items** per edition. If the honest scan
  yields fewer than ~5 genuinely new items, say "quiet day" in the fold-line and
  ship fewer — never pad with recycled carries.

## 3. DIFF (sort into the three buckets)
Read `state/signal-state.json` (v3; see 0.0).
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
  outcome moves to `resolved[]`; unresolved drops are silently retired —
  **but only after the re-search in §1 finds nothing new** (rev 2.1). An item
  whose topic moved into `watchlist[]` is retired from Tracking, not from view.
- **Movers** (`movers[]`) = anything that escalated/deescalated or had a notable
  price move today (1 line each, ▲/▼).
- Yesterday's stories with a known outcome → one-line `resolved[]` entries.

## 4. BUILD (copy `template.html` structure EXACTLY)
Follow `template.html` v3 (section order is in its header comment; v3 rules in 0.0
override the v2 list below). Replace only content:
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
- Write the complete new state to `state/signal-state.json` (schema below) and embed
  only the `page-data` subset in the page.

## 5. SHIP
Save as `editions/ai_daily_signal_YYYY-MM-DD.html`, then run
`python3 scripts/build_site.py` (it regenerates `editions/index.html`, the root
`index.html` redirect, `editions/search-index.json` and `editions/cards/DATE.png`; never
edit those by hand). Working files go in `_working/`, which is not published. Commit to main with
message `AI Daily Signal: edition NNN (YYYY-MM-DD)` and push. Report: edition
number; new/developing/tracking + tier counts; what's new/escalated/resolved vs
yesterday; auto-retirements; **what's new on the emerging-tech beat and any
watchlist movement**; scan gaps. Thin-news days: fewer beats filler.
Never invent stories, quotes, numbers, or links.

## State schema (`state/signal-state.json`)
```jsonc
{
  "edition": 14, "date": "YYYY-MM-DD", "tz": "Asia/Kolkata", "format": "v3",
  "editionType": "daily|catch-up",
  "degraded": false, "degradedReason": "plain sentence, shown in the banner",
  "sourcesOpened": 6,
  "shareable": true, "shareBlockers": [ "why not shareable (when false)" ],
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
      "verified": "opened|snippet",
      "new24h": true,
      "update": "what changed (developing only)",
      "firstSeen": "YYYY-MM-DD", "lastUpdate": "YYYY-MM-DD",
      "category": "models|business|policy|enterprise|research|hardware",
      // swipe view (§16a), deck stories only:
      "short": "<=60-word card summary", "stat": { "value": "65", "label": "..." },
      "image": { "url": "https://official-source/og-image.png", "credit": "Anthropic" }
    }
  ],
  "tracking": [ { "id": "...", "label": "one-liner (no movement)", "arc": "...", "arcDay": 4,
                  "since": "YYYY-MM-DD", "lastChecked": "YYYY-MM-DD" } ],
  "retired":  [ { "id": "...", "date": "YYYY-MM-DD", "reason": "what the re-search found" } ],
  "movers":   [ { "dir": "up|down", "text": "what moved" } ],
  "arcs":     { "arc-id": { "day": 1, "note": "..." } },
  "resolved": [ "one-line closure" ],
  "heldBack": [ { "item": "...", "why": "why it could not be checked", "next": "how to check it" } ],
  "noChange": [ "carried story re-checked: what was found" ],
  "runNotes": { "searches": "...", "pagesOpened": "...", "blocked": "...", "notCovered": "...",
                "trackingCleanup": "...", "corrections": "..." },
  "deadlines":[ { "date": "YYYY-MM-DD", "label": "...", "severity": "high|medium|low" } ],
  // rev 2.1: emerging approaches re-searched every edition (state-only; not rendered)
  "watchlist":[ { "id": "jev-decision-models", "label": "what it is + why it matters",
                  "query": "names/terms to re-search", "firstSeen": "YYYY-MM-DD",
                  "lastChecked": "YYYY-MM-DD", "status": "watching|carded|faded" } ]
}
```
The renderer keys off `section`, `delta`, `new24h`, `movers`, `tracking`,
`deadlines`, `resolved`, `retired`, `degraded`, `editionType`, `sourcesOpened`. Cards are authored in HTML and matched by
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
- **models** — frontier + open-weight model releases, and new model classes /
  architectures from the emerging-tech beat (1.E), e.g. decision models like Jev.

If applied/startup/society coverage becomes a large recurring share, promote a
dedicated tab (e.g. `applied` or `society`) and update the renderer's tab list.
