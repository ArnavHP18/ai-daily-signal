# Adds swipe-card cover data to edition 139: "stat" (key number for the generated cover) and,
# where the story's OFFICIAL source publishes a share image, "image" {url, credit}.
import json, re
STAT = {
 'nvidia-huang-congress-megaspeed': ('-4.27%', 'Nvidia shares on Monday, about $250B'),
 'claude-fable-mythos-52': ('65', 'Artificial Analysis score, #1 of 74 models'),
 'meta-muse-ember': ('$0.10', 'per million input tokens'),
 'fireworks-second-breach': ('2nd', 'breach notice in weeks'),
 'google-tpu-8tx-8i-max': ('4', 'new TPU systems in one year'),
 'baidu-ernie-evolve': ('+33.7%', 'GPU speed-up found by the AI itself'),
 'psi-aaronson-ambainis-proof': ('2008', 'year the conjecture was posed'),
 'anthropic-gas-turbines-34b': ('1.7 GW', 'of gas generators, about $3.4B'),
 'bossai-taipei-dispatch-agents': ('11+', 'countries targeted by one attacker'),
 'cert-in-ai-audit-guidelines': ('6 hrs', 'to report an AI security incident'),
 'claude-code-dont-ask-again-secrets': ('15 mo', 'since the leak was first reported'),
}
IMAGE = {
 'claude-fable-mythos-52': ('https://www-cdn.anthropic.com/images/4zrzovbb/website/b2dab182c77b4ccfd36423470106915b20f676ae-1200x630.jpg', 'Anthropic'),
 'nvidia-huang-congress-megaspeed': ('https://iprsoftwaremedia.com/219/files/202512/692f56983d6332f89cbbc58b_nvidia-logo-horiz-wht-16x9/nvidia-logo-horiz-wht-16x9_44a60e3f-c4e5-4d8a-879f-ec5121ad6f4b-prv.png?v=44a60e3f-c4e5-4d8a-879f-ec5121ad6f4b', 'Nvidia'),
 'google-tpu-8tx-8i-max': ('https://storage.googleapis.com/gweb-uniblog-publish-prod/images/TPU-8tx_and_8i-Max.width-1300.png', 'Google'),
 'psi-aaronson-ambainis-proof': ('https://psi.inc/og/ring-arch-2.png', 'PSI'),
 'idol-image-to-3d-splat': ('https://cdn-thumbnails.huggingface.co/social-thumbnails/models/speridlabs/idol.png', 'Hugging Face'),
}
def patch(stories):
    for s in stories:
        if s['id'] in STAT: s['stat'] = {'value': STAT[s['id']][0], 'label': STAT[s['id']][1]}
        if s['id'] in IMAGE: s['image'] = {'url': IMAGE[s['id']][0], 'credit': IMAGE[s['id']][1]}
st = json.load(open('state/signal-state.json')); patch(st['stories'])
json.dump(st, open('state/signal-state.json', 'w'), indent=1, ensure_ascii=False)
p = 'editions/ai_daily_signal_2026-11-10.html'; t = open(p).read()
m = re.search(r'(<script id="page-data" type="application/json">\n)(.*?)(\n</script>)', t, re.S)
pd = json.loads(m.group(2)); patch(pd['stories'])
open(p, 'w').write(t[:m.start(2)] + json.dumps(pd, indent=1, ensure_ascii=False) + t[m.end(2):])
print('stat', len(STAT), 'image', len(IMAGE))
