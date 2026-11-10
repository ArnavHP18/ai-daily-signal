# Scheduled-task prompt for AI Daily Signal

Paste the block below into the scheduled task. It replaces the previous prompt.
The detailed rules live in `ROUTINE.md`; this prompt points the run at them.

```
Generate today's edition of "AI Daily Signal". Follow ROUTINE.md (v4) in the
arnavhp18/ai-daily-signal repo exactly; section 0.00 (v4) overrides 0.0 (v3),
which overrides older sections. Today's date and IST govern. The reader is a
tech professional in banking who uses this as their main daily news source:
AI and tech first, then finance (banking above all), business, health,
energy, world, society, sports and entertainment. Rank by importance, not
region.

Workflow (ROUTINE.md §0.00):
1. Run python3 scripts/collect.py and read _working/collect/DATE/digest.md
   first: top stories by topic, product updates per company (official
   changelog entries, mentions, and what people are saying on YouTube, Reddit
   and Hacker News), developer signals, and "What are we missing?".
2. Read state/signal-state.json (prior state) and state/REVIEW.md (the next 10
   tracked items due for re-check).
3. Next-day accuracy check: re-check every Critical and Notable story from the
   previous edition; write one followups[] entry each (confirmed / changed /
   corrected / unresolved / quiet, with a note). Anything corrected also goes
   in corrections[] (shown in the footer).
4. 20–40 web searches for verification, the day's deep beat, the 10 tracking
   re-checks and the watchlist (the 20 "daily" entries every run; "weekly"
   ones on Sundays). Include emerging-tech searches (new model types, non-LLM
   approaches, OpenRouter, Hacker News, Hugging Face).
5. Open sources with curl: at minimum the lead's primary source and one source
   per Critical/Notable story. Count them in sourcesOpened. Check the easy
   facts (CVEs on the vendor page or NVD, model details on the Hugging Face
   card, funding on the company's post). Never fabricate URLs, quotes,
   numbers or image links.
6. Write editions/data/DATE.json (format in ROUTINE.md §0.00) and only the
   bookkeeping parts of state/signal-state.json (tracking, watchlist, retired,
   resolved, movers, heldBack, noChange, runNotes including runNotes.missing).
   Do not hand-write HTML.
7. python3 scripts/render.py DATE, then python3 scripts/build_site.py. Fix
   anything either reports and run them again. Do not commit if the build
   fails.
8. Commit everything (including state/collector-state.json) to main as
   "AI Daily Signal: edition NNN (YYYY-MM-DD)" and push.

Content rules:
- As many stories as the day has (10, 20, 30, 40+), nothing padded, nothing
  important missed. At least 10 new; if fewer than 5 broke in the last 48h,
  mark it a catch-up edition (nothing older than 30 days); never pad with old
  carries. NEW IN 24H only for stories that broke within 24h.
- Categories (config/categories.json, 20 in 7 areas): banking, payments,
  insurance, markets, crypto · models, products, research, hardware,
  security, robotics, emerging · business · health · energy · policy, world,
  society · sports, entertainment. In products, include notable things
  people built with AI tools (Show HN, Product Hunt, Reddit, specialist
  blogs) as ideas worth copying.
- Sources: every category keeps at least 10 healthy sources. On Sundays run
  python3 scripts/check_sources.py, replace failing sources, and add new ones
  only after they pass.
- If fewer than half of Critical/Notable stories could be checked on an opened
  page, mark the edition degraded. If nothing could be opened, ship only
  officially confirmed stories, or skip the day and say why.
- Before labelling anything single-source or retiring it, re-search its name
  and its flagship product. Score funding items on the product, not the round.
- Rumours: Rumor-flag (dashed card, "Unconfirmed"); never the lead, ticker,
  30-second read, swipe deck or an image. shareable=true only if the edition
  is not degraded and the lead was checked on an opened primary source.
- Product updates: for every company in config/companies.json (mainstream and
  niche, all of its technology) that shipped something, list what shipped
  (linked to the official changelog or newsroom) and 1–3 of the most useful
  reactions (videos, Reddit, Hacker News), labelled as reactions, never as
  facts. Leave out companies with nothing shipped. Keep each update line under
  about 100 characters. If a company's official changelog failed or is blocked
  (x.ai's Grok Bot changelog always is), or a weekly-shipping product (Grok Bot,
  Grok Build) shows nothing, search the news for it over the last 7 days and list
  what shipped from the reports; never treat a blocked source as "nothing
  shipped". Items from the last 7 days not listed in an earlier edition may be
  added with their real date.
- What are we missing: act on every unmapped trend, suggested source and
  missing company in the digest (card it, add it to config/companies.json,
  config/sources.json or the watchlist, or say why not) and summarise in
  runNotes.missing.
- Swipe view: for the lead and every Critical and Notable story that is not a
  rumour, write "short" (35–60 plain words), "stat" {value ≤ 9 characters,
  label} and, only from the story's opened OFFICIAL source page, an optional
  "image" {url, credit}.
- New storylines need a reader label in arcLabels.

Report: edition number, counts and tiers, sources opened, degraded or
catch-up status, shareable, swipe deck size, product-update companies,
follow-up results (confirmed / changed / corrected), what's new / escalated /
resolved / retired, what the "what are we missing" check found and what you
did, emerging-tech and watchlist movement, and scan gaps.
```
