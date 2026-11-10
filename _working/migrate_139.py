# One-off: converts edition 139 (built by _working/build_139.py) into editions/data/2026-11-10.json.
import json, re
src = open('_working/build_139.py').read()
ns = {}
exec(src[:src.index('# ---------------------------------------------------------------- render')], ns)
S, ARCLBL = ns['S'], ns['ARCLBL']
state = json.load(open('state/signal-state.json'))
extra = {s['id']: s for s in state['stories']}
stories = []
for s in S:
    o = {k: s[k] for k in ('id', 'section', 'tier', 'impact', 'arc', 'arcDay', 'confidence', 'verified', 'new24h', 'category',
                           'title', 'h', 'sub', 'body', 'chip', 'src', 'cat', 'tickerKey', 'ticker') if k in s}
    o['firstSeen'] = s.get('first', '2026-11-10')
    if s['section'] == 'developing':
        o['update'], o['delta'] = s['update'], s['delta']
    for k in ('brief', 'facts', 'impactWho'):
        if s.get(k):
            o[k] = s[k]
    o['body'] = re.sub(r'<div class="delta-line">.*?</div>\s*', '', o['body'], flags=re.S)
    o['src'] = [[g, [list(x) for x in links]] for g, links in s['src']]
    if 'facts' in o:
        o['facts'] = [list(x) for x in o['facts']]
    for k in ('short', 'stat', 'image'):
        if extra.get(s['id'], {}).get(k):
            o[k] = extra[s['id']][k]
    stories.append(o)
data = {
 'format': 'edition-v1', 'edition': 139, 'date': '2026-11-10', 'editionType': 'daily', 'degraded': False, 'degradedReason': '',
 'sourcesOpened': state['sourcesOpened'], 'scanCount': state['scanCount'], 'shareable': state['shareable'], 'shareBlockers': state.get('shareBlockers', []),
 'lead': 'nvidia-huang-congress-megaspeed', 'leadRef': "Nvidia's board investigates Jensen Huang.",
 'description': "Nvidia's board investigates Jensen Huang as the FBI looks in and shares drop 4%. Plus Anthropic's Fable 5.2, Meta's Muse Ember, a Fireworks AI breach and Google's new TPUs.",
 'thirtySecond': [
   {'id': 'claude-fable-mythos-52', 'h': 'Anthropic ships Fable 5.2', 'p': "Cheaper and faster, first on Artificial Analysis, and its agent teams formalised Fermat's Last Theorem in 30 hours."},
   {'id': 'meta-muse-ember', 'h': "Meta's cheap agent worker", 'p': 'Muse Ember undercuts Haiku and Luna at $0.10 per million input tokens for subagent work.'},
   {'id': 'fireworks-second-breach', 'h': 'Fireworks AI breached again', 'p': "Hackers reached some customers' datasets and partial model weights; details still unconfirmed."}],
 'footerNote': "Tuesday's focus: open source and models. Today that meant Anthropic's Fable 5.2, Meta's Muse Ember, ByteDance's Seedream 5.5, the open Idol 3D model topping Hugging Face, and a check on the open weights still missing from Thinking Machines (Inkling 2 Small is on OpenRouter for free) and Alibaba (Qwen 4).",
 'arcLabels': {s['arc']: ARCLBL[s['arc']] for s in S},
 'deadlines': state['deadlines'],
 'stories': stories,
 'productUpdates': [],
 'followups': [],
 'corrections': [],
}
json.dump(data, open('editions/data/2026-11-10.json', 'w'), indent=1, ensure_ascii=False)
print('stories', len(stories))
