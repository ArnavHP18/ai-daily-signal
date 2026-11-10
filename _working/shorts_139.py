# Adds purpose-written swipe-card summaries ("short", <=60 words) to edition 139's state and page-data.
import json, re
SHORT = {
 'nvidia-huang-congress-megaspeed': "Nvidia's board has opened an independent investigation after reports that Jensen Huang was targeted by Chinese intelligence, and Huang admitted an affair in an email Nvidia published. Shares fell 4.27%, about $250 billion. Trump says the FBI is looking into it, the first investor lawsuit is filed, and Huang faces a closed-door House briefing on 18 November.",
 'claude-fable-mythos-52': "Anthropic released Claude Fable 5.2 for everyone and Mythos 5.2 for vetted security and biology teams. It is up to 30% faster and cheaper, at $8 per million input tokens. Artificial Analysis ranks it first of 74 models. Anthropic says 1,000 of its agents formalised Fermat's Last Theorem in 30 hours.",
 'meta-muse-ember': "Meta's new Muse Ember is a small, cheap model built for the repetitive jobs inside AI agents: tool calls, routing, extraction and long documents. At $0.10 per million input tokens, Meta says it beats Claude Haiku 5.5 and GPT-6 Luna on intelligence per dollar. Haiku still wins on real coding tests.",
 'fireworks-second-breach': "Fireworks AI, which hosts and fine-tunes open models for businesses, told customers that hackers reached some customers' datasets, partial model weights and billing data over the past month. It is the company's second breach notice in weeks. Details come from Forbes and Bloomberg headlines; Fireworks has published no notice we could find.",
 'google-tpu-8tx-8i-max': "Google added two AI chip systems. TPU 8tx keeps data and model weights encrypted even while in use, aimed at banks and governments. TPU 8i Max puts two chips on one package for million-token contexts. It is Google's fourth TPU system this year, and TPUs now have nearly 100 customers.",
 'baidu-ernie-evolve': "Baidu's ERNIE Evolve runs its own experiments to improve AI code, keeping only changes that pass checks it cannot see. Baidu says it made its next model, ERNIE-5.5-Flash, 33.7% faster on GPUs in about three days, and beat a public speed record. All figures are Baidu's own.",
 'psi-aaronson-ambainis-proof': "Start-up PSI says its research system, running an unreleased Anthropic model, proved the Aaronson-Ambainis conjecture, open since 2008, and the Lean proof checker accepted it. The result shows quantum computers cannot be exponentially faster on random inputs. Stanford researchers called it \"a huge result\". It is not yet peer reviewed.",
 'anthropic-gas-turbines-34b': "Anthropic is buying about $3.4 billion of Caterpillar gas generators, enough for up to 1.7 gigawatts, to avoid waiting years for grid power and new turbines, the Financial Times reports. It is a shift for a company that mostly rents its computing, and it lands two weeks before Anthropic's planned stock market listing.",
 'bossai-taipei-dispatch-agents': "One attacker in Taiwan used AI agents he called BOSSAI against hundreds of organisations in 11 countries, Acronis researchers say. The agents pulled emergency dispatch records for seven Taipei districts. Because commercial AI refused, they ran on open models with their safety training removed. His own exposed server gave the operation away.",
 'cert-in-ai-audit-guidelines': "India's cyber agency CERT-In has issued AI security audit guidelines with four risk levels and specific tests for AI agents: whether they exceed permissions, misuse tools or fall for prompt injection. Reports say high-risk agents need a kill switch and AI incidents must be reported within six hours. We could not open CERT-In's own site.",
 'claude-code-dont-ask-again-secrets': "Ars Technica confirms that Claude Code's \"don't ask again\" approvals can save passwords into a settings file that ends up on public GitHub, about 1,100 files from 63 organisations. It adds that the problem was raised in bug reports in August 2025, which were closed without a fix. Rotate any exposed secrets.",
}
for k, v in SHORT.items():
    n = len(v.split()); assert n <= 60, (k, n)
st = json.load(open('state/signal-state.json'))
for s in st['stories']:
    if s['id'] in SHORT: s['short'] = SHORT[s['id']]
json.dump(st, open('state/signal-state.json', 'w'), indent=1, ensure_ascii=False)
p = 'editions/ai_daily_signal_2026-11-10.html'; t = open(p).read()
m = re.search(r'(<script id="page-data" type="application/json">\n)(.*?)(\n</script>)', t, re.S)
pd = json.loads(m.group(2))
for s in pd['stories']:
    if s['id'] in SHORT: s['short'] = SHORT[s['id']]
t = t[:m.start(2)] + json.dumps(pd, indent=1, ensure_ascii=False) + t[m.end(2):]
open(p, 'w').write(t)
print('shorts added:', len(SHORT))
