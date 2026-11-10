#!/usr/bin/env python3
"""Check that sources work and every category has enough of them.

    python3 scripts/check_sources.py                 # check config/sources.json
    python3 scripts/check_sources.py FILE.json       # check a candidate list (same format)
    python3 scripts/check_sources.py --write-status  # also record status in config/sources.json

A source is healthy when it answers 200, parses into items, and its newest item is at most
7 days old (Google News queries and developer APIs only need to answer). Prints failures and
the number of healthy sources per category from config/categories.json; exits 1 if any
category has fewer than 10. Run it weekly (Sundays) and whenever sources change.
"""
import concurrent.futures as cf
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import collect  # noqa: E402

ROOT = collect.ROOT
MIN_PER_CATEGORY = 10
FRESH_DAYS = 7


def check(src):
    st, text = collect.fetch(src['url'] if src['kind'] != 'gnews' else
                             'https://news.google.com/rss/search?q=%s+when:2d&hl=en-US&gl=US&ceid=US:en' % collect.urllib.parse.quote_plus(src['query']))
    if st != 200:
        return src, st, 0, None
    if src['kind'] in ('rss', 'gnews'):
        items = collect.parse_feed(text)
        dates = [i['date'] for i in items if i['date']]
        newest = max(dates) if dates else (collect.NOW if items else None)   # undated feeds: answering with items is enough
        return src, st, len(items), newest
    return src, st, 1, collect.NOW          # APIs and pages: answering is enough


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    path = args[0] if args else os.path.join(ROOT, 'config', 'sources.json')
    cfg = json.load(open(path))
    cats = json.load(open(os.path.join(ROOT, 'config', 'categories.json')))
    cat_ids = [c['id'] for c in cats['categories']]
    srcs = [s for s in cfg['sources'] if s['kind'] != 'page']
    healthy, bad = {c: [] for c in cat_ids}, []
    results = {}
    with cf.ThreadPoolExecutor(16) as ex:
        for src, st, n, newest in ex.map(check, srcs):
            age = (collect.NOW - newest).days if newest else None
            ok = st == 200 and n > 0 and (src['kind'] != 'rss' or (age is not None and age <= FRESH_DAYS))
            results[src['id']] = {'status': st, 'items': n, 'newestDays': age, 'ok': ok}
            if not ok:
                bad.append((src, st, n, age))
            for t in src.get('topics', []):
                if ok and t in healthy:
                    healthy[t].append(src['name'])
    print('%d sources checked, %d healthy, %d failing' % (len(srcs), len(srcs) - len(bad), len(bad)))
    for src, st, n, age in sorted(bad, key=lambda b: b[0]['id']):
        print('  FAIL %-28s status %s, %d items, newest %s days' % (src['id'], st, n, age))
    short = []
    print('\nHealthy sources per category (minimum %d):' % MIN_PER_CATEGORY)
    for c in cats['categories']:
        n = len(healthy[c['id']])
        flag = '' if n >= MIN_PER_CATEGORY else '   <-- below minimum'
        if n < MIN_PER_CATEGORY:
            short.append(c['id'])
        print('  %-14s %3d%s' % (c['id'], n, flag))
    if '--write-status' in sys.argv and path.endswith('sources.json'):
        for s in cfg['sources']:
            if s['id'] in results:
                s['lastCheck'] = {'date': collect.NOW.date().isoformat(), **results[s['id']]}
        json.dump(cfg, open(path, 'w'), indent=1, ensure_ascii=False)
    if '--json' in sys.argv:
        print(json.dumps({'results': results, 'healthy': healthy}))
    sys.exit(1 if short else 0)


if __name__ == '__main__':
    main()
