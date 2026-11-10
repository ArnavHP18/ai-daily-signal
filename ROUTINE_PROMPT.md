# Scheduled-task prompt for AI Daily Signal

Paste the block below into the scheduled task. It replaces the previous prompt.
The detailed rules live in `ROUTINE.md`; this prompt points the run at them.

```
Generate today's edition of "AI Daily Signal". Follow ROUTINE.md (v3) in the
arnavhp18/ai-daily-signal repo exactly; where section 0.0 conflicts with older
sections, 0.0 wins. Today's date and IST govern.

Start: read state/signal-state.json (the prior state; not the edition pages) and
state/REVIEW.md (the next 10 tracked items due for re-check). Use template.html
(v3) for structure.

Hard requirements:
- 20–40 web searches, split evenly across Models & tech / Applied AI / People &
  policy, with the day's deep beat. Include the mandatory emerging-tech searches
  (new model types, non-LLM approaches, OpenRouter, Hacker News, X, new Hugging
  Face uploads) and re-search every watchlist entry.
- Open sources with curl in Bash: at minimum the lead's primary source and one
  source per Critical/Notable story. Count them in sourcesOpened. Check the easy
  facts (CVEs on the vendor page or NVD, model details on the Hugging Face card,
  funding on the company's post). Never fabricate URLs, quotes or numbers.
- If fewer than half of Critical/Notable stories could be checked, mark the
  edition degraded. If nothing could be opened, ship only officially confirmed
  stories, or skip the day and say why.
- Re-search the 10 tracked items with the oldest lastChecked; update, resolve or
  retire each one.
- Before labelling anything single-source or retiring it, re-search its name and
  its flagship product. Score funding items on the product, not the round.
- Target ≥10 new stories; if fewer than 5 broke in the last 48h, mark it a
  catch-up edition (nothing older than 30 days); never pad with old carries.
  NEW IN 24H only for stories that broke within 24h.
- Rumours: dashed, muted card; "Unconfirmed" marker; never in the ticker, hero
  or 30-second read. Set shareable=true only if the edition is not degraded and
  the lead was checked on an opened primary source.
- Swipe view (ROUTINE.md §16a): for the lead and every Critical and Notable
  story that is not a rumour, write in BOTH state/signal-state.json and the
  page's page-data:
    - "short": a plain-text card summary, 35–60 words, written for the card
      (the key fact, the number that matters, what is unconfirmed);
    - "stat": {"value", "label"} — the one key number for the card cover,
      value at most 9 characters (e.g. "-4.27%", "$0.10", "1.7 GW");
    - "image" (optional): {"url", "credit"} — only the og:image of the story's
      OFFICIAL source page you opened, credited to that source. Never use news
      outlets' or agencies' photos, never guess an image URL, and never give a
      rumour an image.
  Monitor stories and rumours need none of these; they go in the app's
  "Also today" list.
- Write the full state (tracking, watchlist, movers, resolved, retired,
  heldBack, noChange, runNotes) to state/signal-state.json. The page embeds
  only the page-data subset and shows reader content only.
- Save editions/ai_daily_signal_YYYY-MM-DD.html, then run
  python3 scripts/build_site.py. It checks the edition (including the swipe
  fields above) and writes the archive, share card and swipe-view feeds
  (app/feed.json, editions/feeds/DATE.json). Do not commit if it fails; fix
  what it reports and run it again. Commit everything to main as
  "AI Daily Signal: edition NNN (YYYY-MM-DD)" and push.
- Report: edition number, counts and tiers, sources opened, degraded or
  catch-up status, shareable, swipe deck size (cards and "Also today" items),
  what's new / escalated / resolved / retired, emerging-tech and watchlist
  movement, and scan gaps.
```
