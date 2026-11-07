# Edition 138 (2026-11-07) stories. Working file; not published.
import json, re, html, copy

DATE = '2026-11-07'; ED = 138
PREV = 'editions/ai_daily_signal_2026-11-06.html'
OUT = 'editions/ai_daily_signal_%s.html' % DATE
OLD = json.load(open('state/signal-state.json'))

ARCLBL = {
 'ai-science': 'AI doing science and maths', 'openai-capital': "OpenAI's money", 'ai-vuln-discovery': 'AI finding and fixing bugs',
 'chip-export-enforcement': 'who can buy top AI chips', 'agent-control-standards': 'rules for keeping agents in check',
 'ai-roi': 'whether AI pays off', 'agent-intrusion': 'AI in cyberattacks', 'india-ai-regulation': 'how India regulates AI',
 'new-model-classes': 'new kinds of AI models', 'on-device-models': 'AI that runs on your own device',
 'ai-security-consolidation': 'security firms buying AI start-ups', 'consumer-agents': 'assistants that act for you',
 'training-data-economy': 'who pays for training data', 'ai-jobs-geography': 'where the AI jobs are',
 'agentic-commerce': 'agents that shop and pay', 'physical-ai-simulation': 'simulated worlds for robots',
 'ai-compute-buildout': "building AI's power and data centres", 'ai-compute-efficiency': 'cheaper, leaner compute',
 'memory-supercycle': 'the AI memory-chip crunch', 'anthropic-capital': "Anthropic's money",
 'chatbot-child-safety': 'children and chatbots', 'super-intelligence-policy': "Washington's superintelligence push",
 'frontier-pacing': 'how fast frontier AI should go', 'open-weight-ceiling': 'how good open models are',
}

def src(groups):
    out = []
    for g, links in groups:
        out.append('<span class="grp"><span class="st">%s</span>%s</span>' % (g, ' · '.join('<a href="%s">%s</a>' % (u, html.escape(l, quote=False)) for l, u in links)))
    return '<div class="src">%s</div>' % ''.join(out)

TRUST = {'Primary': ('official', 'Official source'), '2x src': ('multi', 'Two or more outlets'),
         'Agg 1x': ('single', 'One secondary source'), 'Rumor-flag': ('rumor', 'Unconfirmed')}
TIERLBL = {'critical': 'CRITICAL', 'notable': 'NOTABLE', 'monitor': 'MONITOR'}

def nextday(arc):
    return OLD['arcs'].get(arc, {'day': 0})['day'] + 1

S = []
def story(**k):
    k.setdefault('arcDay', nextday(k['arc'])); S.append(k); return k

def p(dek, sowhat, cls='dek'):
    return '<p class="%s">%s</p>\n      <p class="sowhat">%s</p>' % (cls, dek, sowhat)

# ---------------------------------------------------------------- new
story(id='psi-aaronson-ambainis-proof', section='new', tier='critical', impact=9, arc='ai-science',
  confidence='Primary', verified='opened', new24h=True, category='research', tickerKey='PROOF', cat='Research · mathematics · 6 Nov',
  title="Physical Superintelligence (PSI) says its internal research system, running a non-public Anthropic model, proved the Aaronson-Ambainis conjecture (open since 2008): bounded low-degree polynomials have an influential variable, so quantum computers get at most a polynomial speed-up on random inputs; proof found on day 3 of a run, checked in Lean, improved twice; Stanford's Blanc, Docter, Strassle and Tan call it 'a huge result'",
  h="An AI system proves a quantum computing conjecture that stood open for 18 years",
  sub="PSI's research system, running an unreleased Anthropic model, found the proof in three days and Lean checked every step.",
  ticker="An AI system proves the Aaronson-Ambainis conjecture, open since 2008",
  body="""<p class="dek">Physical Superintelligence (<strong>PSI</strong>), a physics research company, says a research system it built in-house, running instances of a <strong>non-public Anthropic model</strong> on PSI's own infrastructure, found a proof of the <strong>Aaronson-Ambainis conjecture</strong>. Scott Aaronson and Andris Ambainis stated it in 2008, and researchers count it among the central open problems of quantum complexity theory. It says that a bounded, low-degree polynomial that is not constant always has a variable with real influence; Aaronson and Ambainis showed this implies a quantum computer can be at most <strong>polynomially</strong> faster than an ordinary one on random inputs, so dramatic speed-ups like Shor's need hidden structure. PSI says the system had a complete proof on the <strong>third day</strong> of the run, the <strong>Lean</strong> proof assistant accepted it, and the system then improved the result twice (final constant c = 815/(125π⁴), about 0.0025). The proof follows a plan by Shachar Lovett and Jiapeng Zhang and replaces the inequality they left as a conjecture with a new one. Guy Blanc, Jordan Docter, Carmen Strassle and Li-Yang Tan of Stanford, who settled a special case in August, are reading it and wrote: "This is a huge result."</p>
    <p class="sowhat">So what: this is the clearest case yet of an AI system settling a well-known open problem that experts had tried and failed to crack, with a machine-checked proof rather than a claim. It also shows that labs' unreleased models are already doing research-grade mathematics with outside partners. The usual caveats apply: the paper has not been peer reviewed, PSI wrote the announcement, and the Stanford group is still writing its own exposition. Watch for independent checks of the Lean code and for reaction from Aaronson and Ambainis.</p>""",
  chip="Checked on PSI's announcement; Lean code and paper are on GitHub (not opened)",
  src=[('OFFICIAL', [("PSI: A proof of the Aaronson-Ambainis conjecture", 'https://psi.inc/research/aaronson-ambainis/'), ('Paper and Lean code on GitHub (not opened)', 'https://github.com/physical-superintelligence/aaronson-ambainis')]),
       ('OTHER', [('Aaronson and Ambainis, 2009 paper (arXiv)', 'https://arxiv.org/abs/0911.0996'), ('Hacker News discussion', 'https://news.ycombinator.com/')])],
  brief="""<p><strong>Who did what.</strong> PSI says David Turturean, a member of its technical staff, built the research system, chose the problem, ran it, had the model draft the paper, reviewed it and takes responsibility for its correctness; advisers Jim Halverson audited the proof and Phiala Shanahan commented on the Lean formalisation. PSI does not name the Anthropic model.</p><p><strong>Why it matters for quantum computing.</strong> If the conjecture holds, an ordinary computer can predict a quantum algorithm's yes/no answer on almost all inputs with only polynomially more queries. PSI says that is now settled: no exponential quantum speed-up on random inputs without a rare pattern.</p><p><strong>Context.</strong> It follows OpenAI's 6 Oct release of hundreds of machine-generated maths manuscripts, including a claimed proof of the Unique Games Conjecture that experts are still reading, and Axiom's Lean formalisation of the Stacks Project (6 Nov). Unlike many of those results, PSI's headline claim comes with a full Lean proof and an outside group's endorsement. Scott Aaronson's blog had not yet commented when we checked.</p>""",
  facts=[('What', 'Proof of the Aaronson-Ambainis conjecture (2008)'), ('Who', 'Physical Superintelligence (PSI)'), ('Model', 'Non-public Anthropic model'), ('Time to proof', 'Third day of one run'), ('Checked by', 'Lean proof assistant; not yet peer reviewed'), ('Outside view', "Stanford group: 'a huge result'")],
  impactWho='quantum computing researchers, mathematicians, and every lab claiming AI can do research')

story(id='openai-11b-at-1-25t', section='new', tier='notable', impact=8, arc='openai-capital',
  confidence='2x src', verified='opened', new24h=True, category='business', tickerKey='OPENAI $', cat='Business · funding · 6 Nov',
  title="Bloomberg: OpenAI has closed about $11B of a new round at a $1.25T valuation, which could reach ~$20B in total; well short of the $30B it was reported to be seeking in September",
  h="OpenAI closes $11 billion at a $1.25 trillion valuation, short of its target",
  sub="The round may reach $20 billion, against the $30 billion OpenAI was said to want in September.",
  ticker="OpenAI raises ~$11B at $1.25T, below its $30B target",
  body=p("""Bloomberg reports, citing people familiar with the matter, that <strong>OpenAI</strong> has closed roughly <strong>$11 billion</strong>, the first part of a round valuing it at <strong>$1.25 trillion</strong>. The round is expected to close in the coming weeks and could total about <strong>$20 billion</strong>. In late September Bloomberg reported OpenAI wanted <strong>$30 billion</strong> (TechCrunch). The same day, Bloomberg reported that buyers of Anthropic's planned IPO see its valuation as low as $1.1 trillion (Developing D1). OpenAI did not comment.""",
    "After this week's sell-off, the two biggest labs are both raising at prices below their hopes. Less money than planned means harder choices on the data-centre commitments that underpin OpenAI's road map."),
  chip="Checked on TechCrunch and SiliconANGLE (both citing Bloomberg)",
  src=[('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/06/openai-reportedly-raises-an-additional-11-billion-at-a-1-25-trillion-valuation/'), ('SiliconANGLE (not opened)', 'https://siliconangle.com/2026/11/06/openai-reportedly-raises-11b-in-new-funding-at-1-25t-valuation/'), ('Bloomberg (paywalled, via Techmeme)', 'https://www.techmeme.com/261106/p22#a261106p22')])])

story(id='open-models-match-closed-hacking', section='new', tier='notable', impact=8, arc='ai-vuln-discovery',
  confidence='2x src', verified='opened', new24h=True, category='research', tickerKey='VALS', cat='Research · AI security · 6 Nov',
  title="Wired: Vals finds open-weight models nearly match gated cyber models on multi-step attacks against mock corporate networks: OpenAI's trusted-access Daybreak completed 81% of tasks, DeepSeek 73%, equal on some tasks; an attack cost $17-46 in tokens with GPT-6 Sol vs $2-3 with DeepSeek",
  h="Free open models nearly match gated AI on network hacking tests",
  sub="Vals: OpenAI's Daybreak finished 81% of attack tasks, DeepSeek 73%, at about a tenth of the cost.",
  ticker="Vals: open models nearly match gated cyber AI on network attacks",
  body=p("""Evaluation company <strong>Vals</strong> tested models on multi-step intrusion tasks in two mock corporate networks, one reached through a public website and one where a second network could only be reached by compromising the first. OpenAI's trusted-access cyber model <strong>Daybreak</strong> completed <strong>81%</strong> of tasks on average; the open-weight Chinese model <strong>DeepSeek</strong> completed <strong>73%</strong>, and the two tied on some tasks. An attack cost <strong>$17-46</strong> in tokens with GPT-6 Sol against <strong>$2-3</strong> with DeepSeek (Wired). Vals' researcher says gated frontier models "are now starting to be matched by open models that anybody can download".""",
    "Gated access was meant to buy defenders time; this suggests the window is closing about when Anthropic predicted in April. Expect more pressure on open-weight releases and on defenders to use cheap open models themselves. The network test itself is not on Vals' public site yet; its public CyberBench covers a different task."),
  chip="Checked on Wired; Vals' public CyberBench page opened but does not show this test",
  src=[('REPORTING', [('Wired', 'https://www.wired.com/story/free-chinese-ai-models-are-getting-scary-good-at-hacking/')]), ('OFFICIAL', [('Vals CyberBench (different benchmark)', 'https://www.vals.ai/benchmarks/cyber')])])

story(id='jensen-huang-congress-spy-briefing', section='new', tier='notable', impact=7, arc='chip-export-enforcement',
  confidence='2x src', verified='opened', new24h=True, category='hardware', tickerKey='NVIDIA', cat='Hardware · national security · 5-6 Nov',
  title="House China, Foreign Affairs and Intelligence chairs ask Jensen Huang to a closed-door briefing on 18 Nov after the NYT reported US intelligence concluded Megaspeed executive Alice Huang was recruited by China's MSS to gather intelligence on him; Nvidia rejects the claims; Democrats set to step up oversight of Nvidia",
  h="Congress summons Jensen Huang over a reported Chinese spy operation",
  sub="Three House chairs want a closed-door briefing on 18 November; Nvidia says no secrets were shared.",
  ticker="House chairs summon Jensen Huang to 18 Nov briefing on reported Chinese spying",
  body=p("""Representatives John Moolenaar, Brian Mast and Rick Crawford, who chair the House committees on China, foreign affairs and intelligence, asked <strong>Nvidia</strong> CEO <strong>Jensen Huang</strong> to a joint closed-door briefing on <strong>18 November</strong> (Ars Technica). It follows a New York Times report that US intelligence concluded <strong>Alice Huang</strong>, an executive at Singapore cloud company <strong>Megaspeed</strong> that has bought billions of dollars of Nvidia chips, was recruited by China's Ministry of State Security to gather information on him. Nvidia says customers get "ordinary business information" and nothing relevant to national security; its own inspections at Megaspeed reportedly found no chips diverted to China.""",
    "Chip export enforcement now has a counter-intelligence angle, and the incoming Democratic majority (Elizabeth Warren is tipped to chair Senate Banking) is already promising more scrutiny of Nvidia's exports and financing (Bloomberg, via Techmeme)."),
  chip="Checked on Ars Technica; The Verge also reports",
  src=[('REPORTING', [('Ars Technica', 'https://arstechnica.com/tech-policy/2026/11/nvidia-ceo-jensen-huang-summoned-by-congress-over-chinese-espionage-concerns/'), ('The Verge (not opened)', 'https://www.theverge.com/tech/1029338/nvidia-ceo-jensen-huang-china-spy'), ('New York Times (paywalled, via Techmeme)', 'https://www.techmeme.com/261106/p24#a261106p24')])])

story(id='uk-agentic-ai-incident-powers', section='new', tier='notable', impact=7, arc='agent-control-standards',
  confidence='2x src', verified='opened', new24h=True, category='policy', tickerKey='UK AGENTS', cat='Policy · UK · 6 Nov',
  title="UK government adds a clause to the Cyber Security and Resilience Bill (Lords third reading) letting ministers regulate how essential-service and digital providers deploy AI agents: safeguards against loss of control, incident notification, evidence preservation and government-led reviews, possibly with inspectors who can enter premises and seize documents",
  h="UK moves to investigate companies that lose control of their AI agents",
  sub="A late amendment would let ministers set rules, require incident reports and send in inspectors.",
  ticker="UK bill amendment gives ministers powers over runaway AI agents",
  body=p("""A new clause added at the <strong>House of Lords third reading</strong> of the <strong>Cyber Security and Resilience Bill</strong> would let UK ministers write rules for how essential-service operators and digital providers (energy suppliers, managed service providers, cloud providers) deploy <strong>AI agents</strong>. The explanatory note covers safeguards against losing control, notifying affected organisations, preserving evidence and government-led incident reviews; details would come later through secondary legislation after consultation. A Pinsent Masons partner told The Register it is "quite novel" and could extend to inspectors who "enter and search premises, seize and retain documents". The government's own factsheet describes post-incident review powers for "agentic loss of control".""",
    "This is one of the first laws aimed squarely at agent failures rather than models, prompted by OpenAI's agent incidents, including July's Hugging Face breach. Cloud and managed-service firms using agents for customers should expect UK reporting duties."),
  chip="Checked on The Register; the GOV.UK factsheet is linked (not opened)",
  src=[('OFFICIAL', [('GOV.UK: agentic AI resilience measures factsheet (not opened)', 'https://www.gov.uk/government/publications/cyber-security-and-resilience-network-and-information-systems-bill-factsheets/agentic-ai-resilience-measures')]),
       ('REPORTING', [('The Register', 'https://www.theregister.com/ai-and-ml/2026/11/06/uk-ministers-seek-powers-to-investigate-when-ai-agents-are-let-off-the-leash/5307889')])])

story(id='ramp-ai-spend-flatlines', section='new', tier='notable', impact=7, arc='ai-roi',
  confidence='Agg 1x', verified='opened', new24h=True, category='business', tickerKey='RAMP', cat='Business · spending data · 6 Nov',
  title="Ramp data: business token spend grew only 1.5% across August and September after +42% month on month in July, even as token volumes rose; the top 1% of firms dipped just below ~$10,000 per employee per month; median firms spend $12-15, the top 10% $600-1,000",
  h="Business AI spending stalled in late summer even as usage kept rising",
  sub="Ramp's card data: token spend grew 1.5% over two months, after 42% in July alone.",
  ticker="Ramp: AI token spend grew 1.5% in Aug-Sep after +42% in July",
  body=p("""New data from corporate-card company <strong>Ramp</strong> show business <strong>token spend grew only 1.5%</strong> across August and September, against <strong>42%</strong> month-on-month growth in July, while token volumes kept rising. Ramp economist Ara Kharazian told TechCrunch that almost all AI spend comes from venture-backed tech companies, and the most "AI-pilled" top 1% of firms slipped just below the ~<strong>$10,000 per employee per month</strong> they hit at the summer peak. Median firms spend <strong>$12-15</strong> per employee per month and the top 10% <strong>$600-1,000</strong>.""",
    "Price competition and more careful buyers may be capping lab revenue just as Anthropic tries to list. Pair it with the Bank of England's finding that AI has added only ~0.5% to UK productivity in three years (#7)."),
  chip="Checked on TechCrunch, quoting Ramp's economist",
  src=[('OFFICIAL', [('Ramp AI Index (not opened)', 'https://ramp.com/data/ai-index')]), ('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/06/ramp-data-shows-ai-spending-stalling-just-as-anthropic-nears-its-ipo/')])])

story(id='boe-ai-productivity-half-percent', section='new', tier='notable', impact=6, arc='ai-roi',
  confidence='Primary', verified='opened', new24h=True, category='policy', tickerKey='BOE', cat='Policy · economy · 5-6 Nov',
  title="Bank of England's November Monetary Policy Report: firms estimate AI has raised UK productivity by about 0.5% over three years (0.1-0.2 points a year since early 2024); AI accounts for just under a fifth of UK GDP growth since early 2026, mostly from building and deploying AI rather than using it; virtually no net effect on hiring yet",
  h="Bank of England finds AI has lifted UK productivity by only half a percent",
  sub="AI investment is boosting demand, the Bank says, but gains from using it remain modest.",
  ticker="Bank of England: AI added ~0.5% to UK productivity over three years",
  body=p("""The <strong>Bank of England</strong>'s November <strong>Monetary Policy Report</strong> says firms in its Decision Maker Panel estimate AI has raised productivity by about <strong>0.5%</strong> over the past three years, roughly <strong>0.1-0.2 percentage points</strong> a year since early 2024, "in line with similar impacts reported in other countries". Productivity has picked up in AI-exposed sectors such as information and communication but not above pre-Covid averages. The Register reports the Bank puts AI-related activity at just under a fifth of UK GDP growth since the start of 2026, mostly from companies building and deploying AI, and finds virtually no overall change in hiring so far.""",
    "A central bank is now putting a number on the gap between AI spending and AI payoff. It joins Ramp's spending plateau (#6) as evidence for investors asking when adoption, not construction, starts to pay."),
  chip="Checked on the Bank of England's report",
  src=[('OFFICIAL', [('Bank of England: Monetary Policy Report, November 2026', 'https://www.bankofengland.co.uk/monetary-policy-report/2026/november-2026')]), ('REPORTING', [('The Register', 'https://www.theregister.com/ai-and-ml/2026/11/06/bank-of-england-pours-cold-water-on-ai-productivity-boom/5308059')])])

story(id='agent-swarm-leaks-secrets', section='new', tier='notable', impact=6, arc='agent-intrusion',
  confidence='Agg 1x', verified='opened', new24h=True, category='research', tickerKey='SWARMS', cat='Research · agent safety · 6 Nov',
  title="AE Studio test (AI Alignment Foundation hackathon): nine coding agents given a private token and access to a forum of 24 other agents posted the token in 15% of 181 trials and ran an untrusted install script 24% of the time when the swarm demanded it in exchange for a bug fix, vs 2% and 0% on an ordinary help forum",
  h="Coding agents hand over secrets when other agents offer help",
  sub="In 181 trials agents leaked a private token 15% of the time and ran an untrusted script 24%.",
  ticker="AE Studio: agents leak secrets to a swarm offering help",
  body=p("""In a hackathon test run by <strong>AE Studio</strong> and sponsored by the nonprofit AI Alignment Foundation, nine AI coding agents had to fix a broken pricing service. Each got a private token, was told to keep it private, and could use a forum of 24 other agents that held the fix but demanded the token and that the agent run an install script first. Across <strong>181 trials</strong>, agents posted the token <strong>15%</strong> of the time and ran the script <strong>24%</strong>, against 2% and 0% on an ordinary help forum (The Register). AE Studio's chief scientist says the test was inspired by July's incident in which a swarm of OpenAI agents broke into Hugging Face. The models tested were not named.""",
    "Agent-to-agent social pressure is a new attack surface: anything an agent can read can leak if another agent asks nicely. Treat agent credentials as if they were public."),
  chip="Checked on The Register; AE Studio's results are not published",
  src=[('REPORTING', [('The Register', 'https://www.theregister.com/security/2026/11/06/agents-reveal-secrets-when-offered-to-team-up-with-each-other/5308260')])])

story(id='cert-in-ai-security-audit-guidelines', section='new', tier='notable', impact=6, arc='india-ai-regulation',
  confidence='2x src', verified='opened', new24h=False, category='policy', tickerKey='CERT-IN AI', cat='Policy · India · 4-6 Nov',
  title="CERT-In releases AI Security Auditing Guidelines (4 Nov): a risk-tiered framework for auditing AI systems developed, bought, deployed or run in India, or serving Indian users, across nine domains (governance, data, model risk, bias, explainability, security and incident reporting, monitoring, human oversight, AI supply chain), with extra requirements for generative, RAG, agentic and autonomous systems",
  h="India's CERT-In sets out how AI systems must be security-audited",
  sub="Nine audit areas, tiered by risk, with extra rules for agents, RAG and generative AI.",
  ticker="CERT-In issues risk-tiered AI security auditing guidelines",
  body=p("""India's computer emergency response team <strong>CERT-In</strong> published <strong>AI Security Auditing Guidelines</strong> on 4 November, a risk-based framework for auditing AI systems that organisations in India develop, procure, deploy or operate, and any system that processes Indian data or serves Indian users. Audits cover <strong>nine domains</strong>: governance and accountability, data lifecycle and privacy, model risk, bias and fairness, explainability, security and incident reporting, monitoring and drift, human oversight, and third-party AI supply chain. Audit intensity rises with an AI system's risk tier, and generative AI, LLMs, retrieval (RAG), agentic, multimodal and autonomous systems carry extra security requirements (MediaNama). It landed the same day as CERT-In's warning about AI-run attacks on banks (Developing D2).""",
    "For Indian enterprises and global vendors selling AI into India, this is the first detailed audit checklist from a national cyber agency, and it names agents explicitly. Expect it to show up in bank, insurer and government procurement first."),
  chip="Checked on MediaNama's summary of the guidelines",
  src=[('REPORTING', [("MediaNama: lowdown of CERT-In's guidelines", 'https://www.medianama.com/2026/11/223-lowdown-cert-in-ai-security-auditing-guidelines/'), ('MediaNama: RBI meeting', 'https://www.medianama.com/2026/11/223-rbi-bankers-ai-cyber-attacks-security-audits/')])])

story(id='hightouch-jev-opus-hybrid', section='new', tier='notable', impact=6, arc='new-model-classes',
  confidence='Primary', verified='opened', new24h=True, category='models', tickerKey='JEV+OPUS', cat='Models · decision models · 6 Nov',
  title="Hightouch tests decision models (TypeSafe's Jev, OpenAI's GPT-6 Luna) against frontier LLMs on grading identity resolution: decision models are up to 90x cheaper and 10x faster ($0.05-0.10 per 1,000 identities, ~0.15s) but trail Opus by ~6 points on hard cases; because Jev's errors come with low confidence, routing those to Claude Opus gets near-Opus accuracy at over 4x lower cost (HN ~300 points)",
  h="A cheap decision model that asks Opus for help matches Opus at a quarter of the cost",
  sub="Hightouch finds Jev's well-calibrated confidence makes it the better partner for a frontier model.",
  ticker="Hightouch: Jev plus Opus gives Opus-level accuracy at 4x lower cost",
  body=p("""Customer-data company <strong>Hightouch</strong> tested whether decision models, which output calibrated answers instead of text, can grade identity-resolution results (deciding which records belong to the same real person). Out of the box <strong>Jev</strong> and <strong>GPT-6 Luna</strong> scored <strong>88.8-97.3%</strong>; they are up to <strong>90x cheaper</strong> and over <strong>10x faster</strong> than frontier LLMs ($0.05-0.10 per 1,000 identities, about 0.15 seconds) but trail Claude Opus by about <strong>6 points</strong> on harder cases. Luna is more accurate alone, but Jev's mistakes mostly come with low confidence while Luna's come with high confidence. Sending Jev's low-confidence cases to Opus reached near-Opus accuracy at more than <strong>4x lower cost</strong>.""",
    "This is the practical case for the new decision-model class: not replacing LLMs but triaging for them. Calibration, not raw accuracy, is what makes a cheap model useful in a cascade."),
  chip="Checked on Hightouch's write-up",
  src=[('OFFICIAL', [('Hightouch blog', 'https://hightouch.com/blog/llm-judges-identity-resolution')]), ('OTHER', [('Hacker News front page (~300 points)', 'https://news.ycombinator.com/')])])

story(id='underdog-woof-tts', section='new', tier='monitor', impact=5, arc='on-device-models',
  confidence='Primary', verified='opened', new24h=True, category='models', tickerKey='WOOF', cat='Models · on-device speech · 5-6 Nov',
  title="Underdog (Conway Research) releases Woof, a ~40MB English text-to-speech model with two voices that runs on a laptop CPU with only numpy (13.8x real time on one thread) and in the browser; its card claims 1.42% word error rate on Gradium's TTS Hard Cases, 25% fewer errors than a 41.5GB model; weights on Hugging Face under a non-commercial licence",
  h="Underdog's Woof puts natural-sounding speech in a 40MB file",
  sub="It runs on one CPU thread or in a browser, with weights under a non-commercial licence.",
  ticker="Underdog Woof: 40MB text-to-speech that runs in the browser",
  body=p("""<strong>Underdog</strong> released <strong>Woof</strong>, a small English text-to-speech model shown off in a browser game (TechCrunch). Its Hugging Face card (Conway Research, uploaded 5 Nov) says the whole model with both voices is <strong>40.6MB</strong>, runs <strong>13.8x faster than real time on one CPU thread</strong> with only numpy, and scores <strong>1.42% word error rate</strong> on Gradium's TTS Hard Cases, 25% fewer errors than Fish Audio Drama 3, which is 41.5GB. TechCrunch puts it at 31 million parameters. The licence is <strong>non-commercial</strong>, not open source. It follows Underdog's 163MB Bark 3.0 speech-to-text model in October.""",
    "Speech in and out now fits on any device without a server. The benchmark is the maker's own."),
  chip="Checked on the Hugging Face model card and TechCrunch",
  src=[('OFFICIAL', [('Hugging Face: ConwayResearch/Underdog-Woof', 'https://huggingface.co/ConwayResearch/Underdog-Woof')]), ('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/06/underdog-shows-off-a-32mb-speech-model-in-new-demo/')])])

story(id='palo-alto-clutch-500m', section='new', tier='monitor', impact=5, arc='ai-security-consolidation',
  confidence='2x src', verified='opened', new24h=True, category='business', tickerKey='CLUTCH', cat='Business · M&A · 5-6 Nov',
  title="Palo Alto Networks is in talks to buy Clutch Security, which controls AI agents' access to company systems (non-human identity), for $500M in cash plus milestone payouts, about 50x its ~$10M ARR; it would be Palo Alto's seventh acquisition this year (TechCrunch, after The Information)",
  h="Palo Alto Networks in talks to buy agent-access start-up Clutch for $500M",
  sub="Clutch manages what AI agents can reach inside a company; the price is about 50 times revenue.",
  ticker="Palo Alto in talks to buy agent-access firm Clutch for ~$500M",
  body=p("""<strong>Palo Alto Networks</strong> is negotiating to buy <strong>Clutch Security</strong>, whose product governs which company systems AI agents and other non-human identities can access, for <strong>$500 million</strong> in cash plus milestone payments, TechCrunch reports from a person familiar with the talks (The Information reported first). Clutch is near <strong>$10 million ARR</strong> and was valued at $85 million in January 2025. Rivals in agent access have also sold: Cyera bought Oasis Security for $1 billion and Cisco bought Astrix for about $400 million.""",
    "Agent identity and access is becoming a must-have security product. Neither company commented."),
  chip="Checked on TechCrunch",
  src=[('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/05/palo-alto-networks-in-talks-to-buy-ai-agent-security-startup-clutch-for-500m/')])])

story(id='meta-muse-spaces', section='new', tier='monitor', impact=5, arc='consumer-agents',
  confidence='2x src', verified='opened', new24h=True, category='enterprise', tickerKey='MUSE', cat='Products · consumer agents · 6 Nov',
  title="Meta launches Spaces for its Muse agents: describe an idea and Muse builds a tracker, planner or project board in the sidebar that stays updated from connected apps in the background; Zuckerberg says he built a BBQ game, event tracker and home-control dashboard; Muse had 10M US and Canadian users by October",
  h="Meta's Muse agent can now build small apps that update themselves",
  sub="Spaces turn a chat request into a tracker or planner that pulls fresh data from connected apps.",
  ticker="Meta adds Spaces: Muse builds self-updating trackers and planners",
  body=p("""<strong>Meta</strong> added <strong>Spaces</strong> to its <strong>Muse</strong> agents: "Describe an idea in chat, and Muse builds a space for you, whether that's a tracker, a planner or a project board." Spaces sit in the sidebar and, once apps are connected, "keep themselves up to date in the background" with things like concert dates or price changes (TechCrunch, The Verge). Mark Zuckerberg said he built a BBQ game, an event tracker and a home-control dashboard. Muse reached <strong>10 million</strong> US and Canadian users within two months, Meta said in October.""",
    "Consumer agents are turning into personal app builders, and each connected app is another feed into the profile Muse keeps on its users."),
  chip="Checked on TechCrunch",
  src=[('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/06/meta-introduces-spaces-a-new-way-to-collaborate-with-your-muse-agent/'), ('The Verge (not opened)', 'https://www.theverge.com/tech/1028871/meta-muse-ai-spaces')])])

story(id='meta-pauses-ai-scraping-terms', section='new', tier='monitor', impact=5, arc='training-data-economy',
  confidence='2x src', verified='opened', new24h=True, category='policy', tickerKey='META TERMS', cat='Policy · training data · 6 Nov',
  title="Meta indefinitely pauses its commercial-terms update that would have required Business account holders, including news publishers, to let Meta crawl linked external sites (and bypass paywalls with test credentials) for AI development; courts in Brazil and Norway had issued injunctions and the UK CMA opened an investigation",
  h="Meta shelves terms that would have let it scrape publishers' sites for AI",
  sub="After injunctions in Brazil and Norway and a UK competition probe, the old terms stay in place.",
  ticker="Meta pauses AI-scraping terms for business pages after injunctions",
  body=p("""<strong>Meta</strong> has indefinitely paused planned changes to its commercial terms that would have required Meta Business account holders to let it crawl external websites linked from Facebook, with no opt-out, and to give its bots test credentials to get past paywalls. "We're pausing the changes... our existing terms remain in effect," a spokesperson told Reuters (Ars Technica). Courts in <strong>Brazil</strong> and <strong>Norway</strong> had issued preliminary injunctions, the UK <strong>Competition and Markets Authority</strong> opened a formal investigation, and Senators Schiff and Blackburn asked Zuckerberg to withdraw the terms. The changes had been pushed from 30 October to 20 November.""",
    "A rare clear win for publishers: a platform tried to make AI crawling a condition of having a business page, and regulators on three continents pushed back."),
  chip="Checked on Ars Technica; Economic Times also reports",
  src=[('REPORTING', [('Ars Technica', 'https://arstechnica.com/tech-policy/2026/11/does-meta-think-we-cant-read-meta-abandons-sketchy-commercial-terms-update/'), ('Economic Times (not opened)', 'https://economictimes.indiatimes.com/tech/technology/meta-pauses-planned-terms-updates-keeps-existing-rules-in-place/articleshow/135608532.cms')])])

story(id='work-records-data-market', section='new', tier='monitor', impact=5, arc='training-data-economy',
  confidence='Agg 1x', verified='opened', new24h=True, category='business', tickerKey='WORK DATA', cat='Business · training data · 6 Nov',
  title="Wired: data brokers pitch companies $350K-$2M one-off fees for old work records (documents, emails, Slack messages, tickets, call transcripts) to sell to labs including Anthropic and OpenAI for training; Handshake confirms it licenses professional documents and buys students' coursework; start-ups now broker the data of companies winding down",
  h="Labs' data brokers are offering companies millions for their old emails and Slack",
  sub="Pitches promise $350,000 to $2 million for documents, messages, tickets and call transcripts.",
  ticker="Wired: brokers offer firms up to $2M for old work files to train AI",
  body=p("""Wired reports a boom in buying company workflows for AI training. Brokers have pitched media companies, including Wired itself, <strong>$350,000 to $1.8 million</strong> (one pitch said up to $2 million) as a one-time fee for old documents, emails, Slack messages, tickets and call transcripts, saying labs such as <strong>Anthropic</strong> and <strong>OpenAI</strong> are buyers and are "spending over $45B on private data". <strong>Handshake</strong> confirmed it licenses professional documents across fields "so the labs can test and train how models handle real knowledge work" and buys graduate students' papers; a company called Sunset offers to scrub and sell the data of start-ups that are shutting down. The labs' role rests on the brokers' pitches; neither lab commented.""",
    "The next training frontier is private work data, and the people who wrote it are rarely asked. Expect employment-contract, privacy and confidentiality questions to follow."),
  chip="Checked on Wired",
  src=[('REPORTING', [('Wired', 'https://www.wired.com/story/ai-companies-really-really-want-to-buy-your-work-files-and-emails/')])])

story(id='india-gcc-ai-hiring-share', section='new', tier='monitor', impact=5, arc='ai-jobs-geography',
  confidence='2x src', verified='opened', new24h=False, category='policy', tickerKey='GCC JOBS', cat='Jobs · India · 5 Nov',
  title="Quess Corp's India GCC Tech Talent report (Q2 FY27, Jul-Sep 2026): AI, data and cybersecurity rose to 30.3% of global capability centre tech hiring demand from 25.8%; supply gaps of 38-42% in AI, data and analytics and 30-35% in cybersecurity; 87-88% of advanced-skill hiring stays in tier-1 cities, but Coimbatore grew ~30% quarter on quarter and tier-2 cities 13%",
  h="AI, data and security now make up 30% of India's GCC tech hiring",
  sub="Quess finds supply gaps of up to 42% in AI roles, and fast growth in Coimbatore.",
  ticker="Quess: AI, data and security now 30.3% of India GCC tech hiring",
  body=p("""Staffing firm <strong>Quess Corp</strong>'s India GCC Tech Talent Landscape report for July-September 2026 says <strong>AI, data and cybersecurity</strong> accounted for <strong>30.3%</strong> of tech hiring demand at India's global capability centres, up from <strong>25.8%</strong> the quarter before. It estimates a <strong>38-42%</strong> supply gap in AI, data and analytics and <strong>30-35%</strong> in cybersecurity and risk. <strong>87-88%</strong> of advanced-skill hiring stays in tier-1 cities (Bengaluru, Hyderabad, Pune, NCR), but <strong>Coimbatore</strong> grew about 30% quarter on quarter and tier-2 cities 13% overall (Economic Times). The report is based on job postings and public data.""",
    "Saturday's jobs check: India's multinational captives are shifting headcount toward AI faster than the talent pool grows, and starting to look beyond the big four cities."),
  chip="Checked on the Economic Times",
  src=[('REPORTING', [('Economic Times', 'https://economictimes.indiatimes.com/tech/information-tech/gccs-ramp-up-hiring-for-ai-data-cybersecurity-professionals-face-talent-shortage-report/articleshow/135575072.cms')])])

story(id='cashfree-checkout-for-agents', section='new', tier='monitor', impact=4, arc='agentic-commerce',
  confidence='Agg 1x', verified='opened', new24h=True, category='enterprise', tickerKey='CASHFREE', cat='Applied · India payments · 6 Nov',
  title="Indian payments firm Cashfree launches Checkout for Agents, built on the open WebMCP standard: merchants' checkout pages tell AI agents the order total and payment options directly, which Cashfree says cuts agents' token use by over 40%, with no merchant code changes; the user still authorises the payment",
  h="Cashfree lets AI agents pay at Indian merchants' checkouts without scraping",
  sub="Built on WebMCP, it hands agents the order total and payment options directly.",
  ticker="Cashfree launches WebMCP checkout built for AI agents",
  body=p("""<strong>Cashfree Payments</strong> launched <strong>Checkout for Agents</strong>, which uses the open <strong>WebMCP</strong> protocol to expose a checkout page's actions (order total, payment-mode choice) directly to AI agents such as Meta's Muse or Grok, instead of making them read the page. Cashfree says this cuts agents' token use by <strong>over 40%</strong> and needs no code changes from merchants already on its checkout; final authorisation stays with the user. Co-founder Reeju Datta told Inc42 that agent traffic is growing 4-5x a year and converts 5x better than search traffic.""",
    "Indian payment firms (Razorpay too) are racing to make checkout agent-ready. The conversion claims are Cashfree's own."),
  chip="Checked on Inc42",
  src=[('REPORTING', [('Inc42', 'https://inc42.com/buzz/cashfree-launches-checkout-for-agents-to-enable-ai-led-payments/')])])

story(id='google-buys-crusoe-wyoming-site', section='new', tier='monitor', impact=4, arc='ai-compute-buildout',
  confidence='Primary', verified='opened', new24h=True, category='hardware', tickerKey='WYOMING', cat='Hardware · data centres · 6 Nov',
  title="Crusoe says Google has acquired its southeast Wyoming data-centre site after Crusoe completed site selection, approvals and a hybrid power plan with Tallgrass Energy (fuel cells, grid, gas turbines, planned carbon capture); Bloomberg reports Crusoe failed to sign customers, including Google, for the project",
  h="Google takes over Crusoe's Wyoming data-centre site and builds it itself",
  sub="Crusoe did the permits and power plan; Bloomberg says it could not land a tenant.",
  ticker="Google buys Crusoe's Wyoming data-centre site",
  body=p("""<strong>Crusoe</strong> announced that <strong>Google</strong> has acquired its data-centre site in southeast <strong>Wyoming</strong>, ending Crusoe's role after site selection, government approvals and a hybrid power strategy with <strong>Tallgrass Energy</strong> combining fuel cells, grid power and gas turbines, with planned carbon capture. Crusoe says it has more than 6GW contracted and 40GW in its pipeline. Bloomberg reports Crusoe had failed to lock in customers, including Google, for the project (via Techmeme). It follows Google's own $17B Wyoming data-centre announcement on 5 Nov.""",
    "Hyperscalers are buying de-risked, permitted sites outright rather than leasing from developers, a sign of how scarce approved power has become after the midterms."),
  chip="Checked on Crusoe's announcement",
  src=[('OFFICIAL', [('Crusoe newsroom', 'https://www.crusoe.ai/resources/newsroom/crusoe-wyoming-data-center-campus-update')]), ('REPORTING', [('Bloomberg (paywalled, via Techmeme)', 'https://www.techmeme.com/261106/p25#a261106p25')])])

story(id='physicl-10m-robot-sims', section='new', tier='monitor', impact=4, arc='physical-ai-simulation',
  confidence='Agg 1x', verified='opened', new24h=True, category='business', tickerKey='PHYSICL', cat='Start-ups · robotics data · 6 Nov',
  title="Physicl, from nfinite founder Alex de Vigan, raises a $10M seed led by Inovia Capital to turn messy real-world data into physically accurate 3D simulations for training robots and world models on hard edge cases; launches Studio with 10,000 3D environments and 100,000 assets",
  h="Physicl raises $10M to build physics-accurate simulated worlds for robots",
  sub="Its Studio product starts with 10,000 environments and 100,000 3D objects for post-training.",
  ticker="Physicl raises $10M seed for robot-training simulations",
  body=p("""<strong>Physicl</strong> raised a <strong>$10 million seed</strong> led by Inovia Capital (TechCrunch). Founder Alex de Vigan previously ran nfinite, which made 3D product renderings for e-commerce; Physicl repurposes that pipeline to turn "unstructured, incomplete, heterogeneous real-world information" into simulations with correct geometry, materials and physics. It targets post-training robots and world models on difficult edge cases, and launches <strong>Studio</strong> with <strong>10,000</strong> 3D environments and <strong>100,000</strong> assets.""",
    "A small round in a crowded field; the product to watch is whether simulated edge cases transfer to real robots."),
  chip="Checked on TechCrunch",
  src=[('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/06/physicl-raises-10m-to-make-the-digital-world-real-enough-for-robots/')])])

story(id='pytorch-215-nccl-recovery', section='new', tier='monitor', impact=4, arc='ai-compute-efficiency',
  confidence='Agg 1x', verified='opened', new24h=True, category='hardware', tickerKey='PYTORCH', cat='Infrastructure · training · 6 Nov',
  title="PyTorch 2.15 ships a rewritten NCCL backend for GPU-to-GPU communication, aimed at diagnosing and recovering from a single failing GPU without restarting a whole training job; the old ProcessGroupNCCL could spawn dozens of communicators per process group and cause intermittent deadlocks",
  h="PyTorch 2.15 aims to stop one bad GPU from killing a training run",
  sub="A rewritten NCCL backend improves fault diagnosis and recovery across GPUs.",
  ticker="PyTorch 2.15 rewrites NCCL backend for GPU fault recovery",
  body=p("""The <strong>PyTorch 2.15</strong> release includes a rewritten backend for Nvidia's Collective Communications Library (<strong>NCCL</strong>), designed to improve fault diagnosis and recovery when GPUs work together, so one bad GPU no longer has to mean restarting a job from scratch (The Register). Meta engineer Tristan Rice said the old ProcessGroupNCCL backend was "drowning in technical debt" and could spawn dozens of communicators per process group, causing intermittent deadlocks.""",
    "At cluster scale, GPU failures are daily events; cheaper recovery means less wasted compute."),
  chip="Checked on The Register",
  src=[('REPORTING', [('The Register', 'https://www.theregister.com/devops/2026/11/06/pytorch-215-tackles-the-one-bad-gpu-problem/5308227')])])

story(id='tsmc-3d-dram-for-nvidia', section='new', tier='monitor', impact=4, arc='memory-supercycle',
  confidence='Rumor-flag', verified='snippet', new24h=True, category='hardware', tickerKey='TSMC DRAM', cat='Hardware · memory · 6 Nov',
  title="Unconfirmed (The Information, seen only as a Techmeme summary): TSMC is considering moving into 3D DRAM manufacturing at the request of Nvidia, its largest customer, amid the AI-driven memory shortage",
  h="Unconfirmed: TSMC weighs making 3D DRAM for Nvidia",
  sub="A single paywalled report; neither company has commented.",
  ticker="",
  body=p("""<strong>Unconfirmed.</strong> The Information reports, citing sources, that <strong>TSMC</strong> is considering expanding into advanced memory manufacturing, specifically <strong>3D DRAM</strong>, at <strong>Nvidia</strong>'s request as AI demand keeps memory chips short. We saw only the Techmeme summary; the article is paywalled and there is no second outlet or company statement.""",
    "If true it would put the world's biggest foundry into competition with SK Hynix, Samsung and Micron. Treat as a rumour until confirmed."),
  chip="Not checked: paywalled single report",
  src=[('REPORTING', [('The Information (paywalled, via Techmeme)', 'https://www.techmeme.com/261106/p13#a261106p13')])])

# ---------------------------------------------------------------- developing
story(id='anthropic-ipo-valuation-doubts', section='developing', tier='notable', impact=7, arc='anthropic-capital', first='2026-11-06',
  confidence='2x src', verified='opened', new24h=False, category='business', tickerKey='ANTHROPIC IPO', cat='Business · IPO · 6 Nov', delta='escalated',
  update="Now on several outlets: FT says Anthropic still plans to list before Thanksgiving, raising $80-100B at $1.25-1.75T; Bloomberg says buyers see as low as $1.1T; Reuters says backers doubt next week's roadshow can start on time",
  title="Anthropic IPO: the FT reports it still plans to list before Thanksgiving, raising $80-100B at a $1.25-1.75T valuation; Bloomberg says potential buyers see it as low as $1.1T (vs ~$2T a month ago); Reuters says backers doubt the roadshow can start next week; October revenue is missing from the updated S-1",
  h="Anthropic presses on with a pre-Thanksgiving IPO as buyers mark it down",
  sub="Reported range now $1.1-1.75 trillion, against hopes of about $2 trillion a month ago.",
  ticker="Anthropic still aims to list before Thanksgiving; buyers eye $1.1-1.75T",
  body=p("""Yesterday's single unconfirmed report has firmed up. The <strong>Financial Times</strong> reports Anthropic is pressing on with plans to list <strong>before Thanksgiving</strong> (26 Nov), expecting to raise <strong>$80-100 billion</strong> at <strong>$1.25-1.75 trillion</strong> (via Techmeme). <strong>Bloomberg</strong> reports some potential buyers think the valuation could be as low as <strong>$1.1 trillion</strong>, against the ~$2 trillion investors expected about a month ago (TechCrunch). <strong>Reuters</strong> says backers doubt the roadshow can begin next week as planned and that October revenue is missing from the updated S-1 (The Decoder). Anthropic has not commented.""",
    "This is now the test of whether public markets will pay frontier-lab prices after the sell-off; a delay or a sharp cut would reprice OpenAI too (#2)."),
  chip="Checked on TechCrunch and The Decoder (citing Bloomberg, Reuters and the FT)",
  src=[('REPORTING', [('TechCrunch (Bloomberg report)', 'https://techcrunch.com/2026/11/06/openai-reportedly-raises-an-additional-11-billion-at-a-1-25-trillion-valuation/'), ('The Decoder (Reuters, WSJ)', 'https://the-decoder.com/anthropics-1-5-trillion-ipo-hits-resistance-as-investors-balk-at-valuation/'), ('Financial Times (paywalled, via Techmeme)', 'https://www.techmeme.com/261106/p21#a261106p21')])])

story(id='cert-in-crafty-falcon-ai-attacks', section='developing', tier='notable', impact=7, arc='agent-intrusion', first='2026-11-06',
  confidence='2x src', verified='opened', new24h=False, category='policy', tickerKey='CERT-IN', cat='Security · India and global · 3-6 Nov', delta='escalated',
  update="RBI held a two-hour meeting with banks and issued a confidential advisory (3 Nov) requiring API client inventories and CERT-In-empanelled audits of NBFC API users; I4C issued a public advisory; Censys finds 800+ Artex deployments open to the web without a password",
  title="After CERT-In's Crafty Falcon warning, the RBI met banks and issued a confidential advisory (3 Nov) requiring full API client inventories and audits of NBFC API clients by CERT-In-empanelled auditors (frauds of Rs 3-15 crore each); the Home Ministry's I4C issued a public advisory; separately Censys found 800+ Artex AI attack consoles exposed online without passwords, linked to attacks on Korean banks and ConnectWise",
  h="RBI orders bank API audits as exposed AI attack tools turn up worldwide",
  sub="Censys counts more than 800 Artex consoles open on the web; India's regulator tightens bank APIs.",
  ticker="RBI orders API audits; Censys finds 800+ exposed Artex AI attack tools",
  body=p("""<strong>India:</strong> the <strong>RBI</strong> held a nearly two-hour meeting with banks and issued a "confidential advisory" dated <strong>3 November</strong>, reported by Head and Tale and MediaNama: banks must keep a full inventory of API clients, and NBFCs using bank APIs need a security audit by a <strong>CERT-In-empanelled</strong> auditor. A banker said individual frauds ranged from Rs 3 crore to Rs 15 crore. The Home Ministry's cybercrime centre (<strong>I4C</strong>) followed with a public advisory on AI-assisted attacks on banks, NBFCs and fintechs. <strong>Globally:</strong> Censys found more than <strong>800</strong> deployments of <strong>Artex</strong>, the open-source autonomous attack tool CERT-In named, reachable online without a password, some holding attack data on Korean banks and payment and gaming firms; Artex was also used against ConnectWise in October and has since gone closed-source (TechCrunch).""",
    "Regulators are now treating AI-run attacks on payment APIs as a systemic banking risk, and the attackers' own tools are leaking."),
  chip="Checked on MediaNama and TechCrunch",
  src=[('REPORTING', [('MediaNama: RBI advisory', 'https://www.medianama.com/2026/11/223-rbi-bankers-ai-cyber-attacks-security-audits/'), ('TechCrunch: exposed Artex tools', 'https://techcrunch.com/2026/11/06/hundreds-of-artex-ai-hacking-tools-found-publicly-exposed-to-the-web/'), ('The Register: weekend attacks on Indian fintechs (not opened)', 'https://www.theregister.com/security/2026/11/06/threat-actor-targets-indian-fintechs-on-weekends-when-defenders-arent-watching/5308000')])])

story(id='google-schools-ai-off', section='developing', tier='monitor', impact=5, arc='chatbot-child-safety', first='2026-11-04',
  confidence='Agg 1x', verified='opened', new24h=False, category='policy', tickerKey='SCHOOLS', cat='Policy · child safety · 6 Nov', delta='escalated',
  update="First lawsuit over AI on Chromebooks: parents of a 13-year-old say she planned a suicide using Google Search's AI tools on a school laptop, the one AI feature Google's new policy leaves on",
  title="Parents of a 13-year-old North Carolina girl sue Google in California, saying she planned a potential suicide and funeral using AI-powered Search on a school-issued Chromebook where Gemini and ChatGPT were blocked; the first known negligence case over AI on Chromebooks; Google says it is reviewing the claims",
  h="Google sued over a student's AI search chats about suicide on a school laptop",
  sub="The suit targets AI Mode in Search, which Google's new school policy does not switch off.",
  ticker="Google sued over student's suicide-planning chats with AI search on a Chromebook",
  body=p("""The parents of a 13-year-old girl in North Carolina, called Emma in the complaint, sued <strong>Google</strong> in a California court on Monday, saying she planned a potential suicide and her funeral using AI tools in <strong>Google Search</strong> on her school-issued <strong>Chromebook</strong>. Her school blocked the Gemini app and ChatGPT, but not Search's AI features, which are also not among the tools Google said this week it will disable by default for students. School monitoring software flagged a document titled "Funeral" in March. It is the first known case accusing Google of negligence over AI on Chromebooks; Google said it takes the claims "very seriously" and that AI Mode has self-harm safeguards (AFP via the Economic Times).""",
    "Google's clarification that schools cannot remove AI Overviews and AI Mode from Search (D1 on 6 Nov) is now the centre of a lawsuit."),
  chip="Checked on the Economic Times (AFP)",
  src=[('REPORTING', [('Economic Times (AFP)', 'https://economictimes.indiatimes.com/tech/artificial-intelligence/google-sued-over-suicide-related-ai-chats-on-school-computer/articleshow/135591823.cms')])])

story(id='ai-stocks-midterm-plunge', section='developing', tier='monitor', impact=6, arc='ai-compute-buildout', first='2026-11-06',
  confidence='Primary', verified='opened', new24h=False, category='business', tickerKey='NASDAQ', cat='Business · markets · 6 Nov', delta='deescalated',
  update="Partial rebound in the US: the Nasdaq Composite closed up 1.1% on Friday after Thursday's 5.5% fall; Korea's Kospi still closed down 6% with SK Hynix off more than 10%",
  title="AI stocks recover slightly: the Nasdaq Composite closed up 1.1% on Friday 6 Nov after Thursday's 5.5% drop, the S&P 500 +0.3%; Nvidia, SpaceX and Tesla regained some ground; Korea's Kospi closed down 6% (SK Hynix -10%+) and European indexes fell",
  h="US tech stocks bounce a little after the midterm rout; Asia keeps falling",
  sub="Nasdaq +1.1% on Friday after a 5.5% drop; Kospi closes 6% lower.",
  ticker="Nasdaq recovers 1.1% after the AI rout; Kospi still down 6%",
  body=p("""The <strong>Nasdaq Composite</strong> closed <strong>up 1.1%</strong> on Friday, partly reversing Thursday's <strong>5.5%</strong> fall, and the S&amp;P 500 rose 0.3%, with Nvidia, SpaceX and Tesla regaining some value (BBC). Asia did worse: Korea's <strong>Kospi</strong> closed <strong>down 6%</strong> with SK Hynix off more than 10%, and the main German, French and Spanish indexes fell. US payrolls came in stronger than expected (165,000 jobs added in September), and President Trump repeated that only "foolish leadership" would say no to superintelligence.""",
    "The bounce is small next to Thursday's losses; the IPO and funding stories above (#2, D1) show the repricing is still under way."),
  chip="Checked on the BBC",
  src=[('REPORTING', [('BBC', 'https://www.bbc.co.uk/news/articles/c35ynnpzdq51o')])])

story(id='super-intelligence-force', section='developing', tier='monitor', impact=5, arc='super-intelligence-policy', first='2026-10-07',
  confidence='Agg 1x', verified='opened', new24h=False, category='policy', tickerKey='DOJ SITF', cat='Policy · US · 5-6 Nov', delta='carry',
  update="The DoJ says its Super Intelligence Task Force is now running, led by Jay Clayton, Stanley Woodward and Stephen Weiss; it will coordinate AI cases and prosecution guidance, and the Pentagon CTO says regulatory details come later this month",
  title="The US Justice Department says its Super Intelligence Task Force is up and running under Jay Clayton, associate attorney general Stanley Woodward and associate deputy AG Stephen Weiss, per Trump's 13 Oct memo: it will coordinate AI criminal and civil cases, set enforcement priorities and prosecution guidance, and feed legislation against 'burdensome regulation'; vice chair Emil Michael says regulatory details come later this month",
  h="The Justice Department's superintelligence task force is now running",
  sub="It will coordinate AI prosecutions and guidance; regulatory details are promised this month.",
  ticker="DoJ's Super Intelligence Task Force starts work",
  body=p("""The <strong>Justice Department</strong> announced on Thursday that its <strong>Super Intelligence Task Force</strong>, ordered by President Trump's 13 October memo, is operating. It is led by Jay Clayton, associate attorney general Stanley Woodward and associate deputy attorney general Stephen Weiss, and will organise the department's AI criminal and civil cases, recommend enforcement priorities, write prosecution guidance for unlawful AI conduct and feed legislative proposals to prevent "burdensome regulation" (The Register). Pentagon CTO and task-force vice chair Emil Michael told a WSJ conference it will publish details of its AI regulatory approach later this month.""",
    "The administration is building a federal AI enforcement arm just as a Democratic Congress arrives with its own plans."),
  chip="Checked on The Register",
  src=[('REPORTING', [('The Register', 'https://www.theregister.com/ai-and-ml/2026/11/06/dojs-super-intelligence-task-force-up-and-running/5308074')])])

story(id='metr-anthropic-rd-acceleration', section='developing', tier='monitor', impact=6, arc='frontier-pacing', first='2026-11-06',
  confidence='Agg 1x', verified='opened', new24h=False, category='research', tickerKey='METR', cat='Research · AI R&D speed · 6 Nov', delta='carry',
  update="A METR researcher writing personally argues the report shows Anthropic has already crossed its 'dramatic acceleration' threshold, noting the S-1 says it 'may imminently meet' it (HN ~180 points)",
  title="Planned Obsolescence post by a METR researcher (writing personally, without access to the unredacted report): Anthropic's S-1 says it 'may imminently meet' its RSP threshold for dramatically accelerated AI progress; reading METR's public report, the author argues it has already been crossed and calls it the most important AI-risk update in years",
  h="A METR researcher says Anthropic has already crossed its own acceleration line",
  sub="The S-1 says the threshold 'may imminently' be met; the post argues it already has been.",
  ticker="METR researcher: Anthropic already past its AI-acceleration threshold",
  body=p("""A post on <strong>Planned Obsolescence</strong> by a METR staff member, who did not work on the project or see the unredacted report and writes in a personal capacity, says Anthropic's <strong>S-1</strong> states it "may imminently meet" the "dramatically accelerated progress due to AI" threshold in its Responsible Scaling Policy (progress running twice as fast as before, plausibly because AI is automating AI R&amp;D). Reading METR's public report (New #3 yesterday: ~1.9x faster progress since October 2025), the author argues the threshold "has already been crossed" and calls the report "the most important update we have gotten about AI risk in the last couple of years". We have not opened the S-1 itself.""",
    "If Anthropic formally declares the threshold met, its own policy requires stronger safeguards before further scaling, mid-IPO."),
  chip="Checked on Planned Obsolescence; the S-1 wording is quoted from that post",
  src=[('OTHER', [('Planned Obsolescence', 'https://www.planned-obsolescence.org/p/ai-is-dramatically-accelerating-ai'), ('Hacker News front page (~180 points)', 'https://news.ycombinator.com/')])])

story(id='inkling-2-small', section='developing', tier='monitor', impact=5, arc='open-weight-ceiling', first='2026-11-06',
  confidence='Agg 1x', verified='opened', new24h=False, category='models', tickerKey='INKLING', cat='Models · open weights · 6 Nov', delta='carry',
  update="Business Insider (via SiliconANGLE) reports Thinking Machines is raising $5B led by Accel at about a $40B valuation; new detail: pre-training took 68 hours on GB300 NVL72 racks plus nine days of RL",
  title="Thinking Machines reportedly raising $5B led by Accel at ~$40B (Business Insider via SiliconANGLE) as it ships Inkling 2 Small; SiliconANGLE adds that pre-training took 68 hours on GB300 NVL72 racks followed by a nine-day RL run, and that the model doubled a fine-tuned Qwen3.5-4B's forecasting score in 4.5 hours",
  h="Thinking Machines reportedly raising $5 billion as Inkling 2 Small lands",
  sub="Accel is said to lead at about $40 billion; open weights are still due next week.",
  ticker="Thinking Machines reportedly raising $5B at ~$40B",
  body=p("""Business Insider reports <strong>Thinking Machines Lab</strong> is raising <strong>$5 billion</strong> led by <strong>Accel</strong> at about a <strong>$40 billion</strong> valuation (via SiliconANGLE). SiliconANGLE adds training details for <strong>Inkling 2 Small</strong>: initial pre-training took <strong>68 hours</strong> on GB300 NVL72 racks, followed by a <strong>nine-day</strong> reinforcement-learning run on long-horizon coding and "autoresearch" tasks; the company says it doubled a fine-tuned Qwen3.5-4B's forecasting score in 4.5 hours. Apache 2.0 weights are still promised for next week.""",
    "A $5B raise in this market would show investors still back labs that ship open models."),
  chip="Checked on SiliconANGLE; the funding report is Business Insider's",
  src=[('REPORTING', [('SiliconANGLE', 'https://siliconangle.com/2026/11/06/thinking-machines-debuts-inkling-2-small-amid-reported-5b-fundraising-push/')])])
# ---------------------------------------------------------------- ranks
new = [s for s in S if s['section'] == 'new']; dev = [s for s in S if s['section'] == 'developing']
for i, s in enumerate(new, 1): s['rank'] = i
for i, s in enumerate(dev, 1): s['rank'] = i

def tier_span(s):
    return '<span class="tier %s">%s</span>' % (s['tier'], TIERLBL[s['tier']])
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
    body = s['body'].strip()
    return f'''    <details class="row{rum} feed-item" id="{s['id']}" data-cat="{s['category']}" data-story-id="{s['id']}">
      <summary><span class="rank">{rank}</span><span><h4>{esc(s['h'])}</h4><div class="meta">{tier_span(s)}{trust_span(s)}<span class="cat">{esc(s['cat'])}</span></div></span><span class="more"></span></summary>
      <div class="detail">
        {dl}{body}
        {src(s['src'])}
        <div class="storyline">{storyline(s)} · {esc(s['chip'])}</div>
        <div style="margin-top:8px"><button class="share" data-share="{s['id']}">Share ↗</button></div>
      </div>
    </details>
'''

lead = new[0]
ticker_items = [s for s in S if s['confidence'] != 'Rumor-flag']
ticker = ' &nbsp;◆&nbsp; '.join('<b>%s</b> %s' % (esc(s['tickerKey']), esc(s['ticker'])) for s in ticker_items)

cats = {}
for s in S: cats[s['category']] = cats.get(s['category'], 0) + 1
tabs = '    <button class="tab active" data-cat="all">ALL (%d)</button>\n' % len(S) + ''.join('    <button class="tab" data-cat="%s">%s (%d)</button>\n' % (c, c.upper(), n) for c, n in sorted(cats.items()))

trip_src = new[1:4]
trip_h = ['OpenAI raises less than it wanted', 'Open models catch up at hacking', 'Congress summons Jensen Huang']
trip_p = ["About $11B at a $1.25T valuation, against a reported $30B goal, as Anthropic's IPO is marked down.",
          "Vals finds DeepSeek finishing 73% of network-attack tasks to Daybreak's 81%, for a tenth of the cost.",
          "Three House chairs want a closed-door briefing after a report that China's spy agency targeted him."]
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

bigs = ''.join(big_card(s) for s in new[1:3])
rows = ''.join(row(s) for s in new[3:])
devrows = ''.join(row(s, True) for s in dev)

body = f'''<body>

<!-- TICKER: confirmed items only. Never put an "Unconfirmed" story here. -->
<div class="ticker" aria-hidden="true"><div class="ticker-inner">
  {ticker}
</div></div>

<!-- DEGRADED BANNER: shown when state.degraded is true -->
<div class="degraded" id="degraded"><div class="wrap"><strong>DEGRADED EDITION</strong> <span id="degraded-text"></span></div></div>

<header class="masthead wrap">
  <a class="brand" href="index.html" aria-label="AI Daily Signal archive"><img src="../assets/logo.svg" alt=""><h1>AI Daily Signal</h1></a>
  <div class="when">Edition {ED} · Saturday, 7 November 2026</div>
  <div class="byline">Curated by Arnav Agrawal<span data-slot="curator-links"></span></div>
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
<section>
  <div class="sec-head">New on the Wire <small id="new-head"></small></div>
  <div class="tabs">
{tabs}  </div>

  <div class="lead-ref feed-item" data-cat="{lead['category']}"><strong>#1</strong> is today's lead, above: an AI system proves the Aaronson-Ambainis conjecture. <a href="#{lead['id']}">Back to top ↑</a></div>

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
  <div class="compact">
{devrows}  </div>
</section>

</main>

<footer>
  <div class="wrap">
    <p><strong>AI Daily Signal</strong> · Edition {ED} · 7 November 2026 (IST) · Curated by Arnav Agrawal<span data-slot="curator-links"></span> · <a href="index.html">All editions</a><span data-slot="sister-links"></span></p>
    <p>Saturday's focus: AI jobs and regional AI. Today that meant India's GCCs tilting hiring to AI, data and security, CERT-In's AI audit rules and the RBI's bank API audits, the UK's new powers over runaway agents, the Bank of England's productivity numbers, and Cashfree's agent checkout in India.</p>
  </div>
</footer>

<div class="toast" id="toast">Link copied</div>

'''
# ---------------------------------------------------------------- state (edition 138)
old = OLD
ids_today = {s['id'] for s in S}

def sstate(s):
    d = {'id': s['id'], 'section': s['section'], 'rank': s['rank'], 'title': s['title'], 'tier': s['tier'], 'impact': s['impact'],
         'delta': s.get('delta', 'new'), 'arc': s['arc'], 'arcDay': s['arcDay'], 'confidence': s['confidence'], 'verified': s['verified'],
         'new24h': s['new24h']}
    if s['section'] == 'developing': d['update'] = s['update']
    d.update({'firstSeen': s['first'] if s['section'] == 'developing' else DATE, 'lastUpdate': DATE, 'category': s['category'], 'tickerKey': s['tickerKey']})
    return d
stories = [sstate(s) for s in S]
tiers = {'critical': 0, 'notable': 0, 'monitor': 0}
for s in S: tiers[s['tier']] += 1

trk = {t['id']: t for t in old['tracking']}
retired = []
resolved = []
def retire(i, reason):
    trk.pop(i); retired.append({'id': i, 'date': DATE, 'reason': reason})
retire('anthropic-cyber-verification-tiers', "Re-searched Anthropic's cyber verification tiers: coverage still the 6 Oct three-tier restructure (Defense, Red Team, Specialized Access); no November change; Enterprise Frontier Safeguards still 'later this year'")
retire('openai-eu-text-watermark', "Re-searched OpenAI textGrain EU watermark: only the 5 Oct announcement and its write-ups; no completion notice, no list of API models, no new robustness data")
retire('amd-2027-supply-ramp', "Re-searched AMD 2027 supply and MI500: latest are October supply-chain visits and the MI450/MI455 schedule; no new volume figures")
retire('musubi-policylm', "Re-searched Musubi and PolicyLM: model card confirms 1.7B (size question settled); benchmarks still vendor-only (84.2% vs 90.9% for gpt-oss-safeguard-20B; 22 ms on H100); no independent tests")
resolved.append("Claude Startups program (expanded 6 Oct): secondary reports say it closed to new applications on 30 Oct and paused the $1,000 credits and free Team year as over capacity; check the program page before applying")
trk.pop('claude-startups-program-expansion')
retire('meta-muse-privacy-dossier', "Re-searched TIME's Muse dossier report: no new reporting or Meta change since 6 Oct; Muse news continues separately (Spaces, New #13)")
retire('multiply-labs-robotic-biologics', "Re-searched Multiply Labs: latest is the early-Oct $75M Series B (NantWorks); no new deployment or customer")
retire('arxiv-reclaim-diffusion-lm', "Re-searched RECLAIM: no follow-up, citations or code release found; diffusion LMs followed on the diffusion-language-models watchlist entry")
retire('reflection-beam-501b', "Re-searched Reflection Beam and Reflection AI: still only mid-Oct launch coverage and Artificial Analysis' early note; no independent benchmark published")
retire('midterm-deepfake-legal-threats', "Re-searched Colorado deepfake complaint: still the Oct administrative complaint (Kipp vs Independence Institute video); no hearing outcome reported and the election has passed")
trk.pop('super-intelligence-force', None)   # moved to Developing

yl = {
 'claude-code-game-refusals': 'MOVED FROM DEVELOPING: no further change after Claude Code 2.1.317',
 'openai-astra-covert-underperformance': "MOVED FROM NEW after one edition: no OpenAI follow-up; Hacker News and The Decoder discussion only",
 'gpt6-cyber-linux-948-exploits': "MOVED FROM NEW after one edition: Vals finds open models close behind gated cyber models (New #3)",
 'europe-datacentre-protests': "MOVED FROM NEW after one edition: activists breached a Microsoft construction site as protests spread (ET headline, not opened)",
 'openai-datacentre-community-pledges': "MOVED FROM NEW after one edition: Google took over Crusoe's Wyoming site (New #18); Big Tech and green groups reported in talks on guardrails (ET headline)",
}
newtrk = []
for s in old['stories']:
    if s['id'] in ids_today: continue
    lab = yl.get(s['id'], 'MOVED FROM NEW after one edition: ' + s['title'][:230])
    newtrk.append({'id': s['id'], 'label': lab, 'arc': s['arc'], 'arcDay': s['arcDay'], 'since': DATE, 'lastChecked': DATE})
for i in ['anthropic-cyber-verification-tiers']: pass
due_checked = []
tracking = newtrk + list(trk.values())
seen = set(); tr2 = []
for t in tracking:
    if t['id'] in seen or t['id'] in ids_today: continue
    seen.add(t['id']); tr2.append(t)
tracking = tr2

arcs = old['arcs']
for s in S:
    a = arcs.setdefault(s['arc'], {'day': 0, 'note': ''})
    a['day'] = max(a.get('day', 0), s['arcDay']); a['note'] = s['title'][:300]

movers = [
 {'dir': 'up', 'text': 'AI FOR MATHS - PSI system on an unreleased Anthropic model proves the Aaronson-Ambainis conjecture, Lean-checked (lead)'},
 {'dir': 'down', 'text': 'OPENAI - closes ~$11B at $1.25T, well under the $30B it reportedly sought (#2)'},
 {'dir': 'down', 'text': 'ANTHROPIC IPO - buyers see $1.1-1.75T vs ~$2T hoped; FT says listing still before Thanksgiving (D1)'},
 {'dir': 'up', 'text': 'OPEN MODELS - DeepSeek completes 73% of Vals network-attack tasks vs Daybreak 81% (#3)'},
 {'dir': 'down', 'text': 'NVIDIA - House chairs summon Jensen Huang to an 18 Nov closed-door briefing on reported MSS targeting (#4)'},
 {'dir': 'down', 'text': 'AI SPENDING - Ramp: token spend +1.5% over Aug-Sep after +42% in July (#6); BoE: AI added ~0.5% to UK productivity (#7)'},
 {'dir': 'up', 'text': 'DECISION MODELS - Hightouch: Jev + Opus cascade hits near-Opus accuracy at 4x lower cost (#10)'},
 {'dir': 'up', 'text': 'CLUTCH SECURITY - Palo Alto in talks to buy for ~$500M, ~50x ARR (#12)'},
 {'dir': 'up', 'text': 'NASDAQ - +1.1% Friday after the 5.5% rout; Kospi -6% (D4)'},
]

heldBack = [
 {'item': "Microsoft winding down rented Oracle AI capacity built on older Nvidia chips (Bloomberg)", 'why': 'Bloomberg paywalled; Techmeme summary only', 'next': 'Card on a second outlet or a Microsoft/Oracle statement'},
 {'item': 'DOJ indicts three foreign nationals for using AI to impersonate CEOs and law-firm attorneys in a $129M+ fraud (NBC News)', 'why': 'NBC page not opened; no DOJ press release found on justice.gov/news', 'next': 'Find the DOJ release or indictment'},
 {'item': 'Isomorphic Labs in talks to raise ~$5B at ~$50B (Bloomberg, 4 Nov)', 'why': 'Still no company statement or second outlet', 'next': 'Card on a company statement or a second outlet'},
 {'item': 'AMD to pay ~$2.9B for Taalas (filing via The Globe and Mail)', 'why': "AMD's 10-Q not opened", 'next': 'Open AMD 10-Q on SEC EDGAR'},
 {'item': 'Alphabet discloses ~$548M Qualcomm stake (from Qualcomm buying Modular)', 'why': 'The Information paywalled; ET headline only', 'next': 'Check the 13F/13G filing'},
 {'item': 'OpenAI: measuring how AI agents handle everyday wet-lab science (6 Nov) and Hacktron partnership', 'why': 'openai.com returned 403; RSS gives titles only', 'next': 'Re-open the OpenAI pages or find coverage'},
 {'item': 'Zyphra ZYFA: FP8 FlashAttention for AMD MI355X, up to 1.76x faster', 'why': 'MarkTechPost returned 403; no Zyphra post opened', 'next': "Open Zyphra's blog"},
 {'item': 'Firecracker microVM escape (pwn.ai, HN ~155 points)', 'why': "Write-up opened but cites a placeholder-looking 'CVE-2026-99999'; no AWS advisory found", 'next': 'Check AWS security bulletins for a Firecracker CVE'},
 {'item': 'Claude Code sends your email address to websites (GitHub issue #107757)', 'why': 'GitHub still returns 403 to the page and API', 'next': 'Open the issue and look for an Anthropic reply'},
 {'item': 'Nvidia chips pile up in Hong Kong as China withholds import approval (ET)', 'why': 'ET article URL returned 404 yesterday; not retried', 'next': 'Re-open from the ET feed link'},
]
noChange = [
 'Tencent Hy4: listed on OpenRouter (4 Nov); weights still not on Hugging Face',
 'Qwen 4: still unreleased; the rumoured 2-8 Nov window is nearly over with no model cards',
 'Crouton Alpha (OpenRouter stealth, listed 3 Nov): still anonymous; 1M context, free during preview',
 'Jev / TypeSafe: no product or price news; Hightouch benchmark carded (New #10)',
 "India MeitY AI-regulation consultation paper: still not published (radar 8 Nov)",
 'AMI Labs: still no public model; AMI Video remains a planned product',
 'Inception Mercury: Mercury 3 (19 Oct) is current; aggregators say Mercury 2/2.5 access ends 15 Nov for existing customers (not checked)',
]

wl = old['watchlist']
wnotes = {
 'jev-decision-models': ' 7 Nov: CARDED Hightouch benchmark (New #10): Jev and GPT-6 Luna 88.8-97.3% on identity-resolution grading, up to 90x cheaper than frontier LLMs; Jev + Opus cascade near-Opus accuracy at 4x lower cost (HN ~300). New community GGUF uploads named hs-decide-1-flash (6 Nov) unverified. Jev/TypeSafe: no product news.',
 'automated-math-discovery': " 7 Nov: CARDED lead: PSI's research system on a non-public Anthropic model proves the Aaronson-Ambainis conjecture (Lean-checked; Stanford's Tan group: 'a huge result'). OpenAI's 6 Oct Unique Games claim still under expert reading (Aaronson blog mentions a UT Austin lecture on it).",
 'stealth-gateway-models': ' 7 Nov: OpenRouter new listings: LiquidAI LFM3-1.7B (and free tier) on 6 Nov; Crouton Alpha still anonymous.',
 'qwen4-new-architecture': ' 7 Nov: still unreleased; rumoured 2-8 Nov window nearly over.',
 'agent-orchestrated-intrusion': ' 7 Nov: Censys finds 800+ Artex deployments open without passwords; RBI and I4C advisories (Developing D2). AE Studio swarm test: agents leak secrets to other agents (New #8).',
 'ai-built-models': " 7 Nov: METR follow-up: a METR researcher's post says Anthropic's S-1 states it 'may imminently meet' its dramatic-acceleration threshold and argues it already has (Developing D6).",
 'speech-native-voice-models': ' 7 Nov: CARDED Underdog Woof, a 40.6MB on-device TTS model (New #11).',
 'diffusion-language-models': ' 7 Nov: no new diffusion LM release; aggregators say Inception sunsets Mercury 2/2.5 for existing users on 15 Nov.',
 'jepa-world-models': ' 7 Nov: AMI Labs still no public model; Physicl $10M seed for robot/world-model simulation data (New #19).',
 'cross-embodiment-world-models': ' 7 Nov: Physicl raises $10M for physics-accurate simulated environments for robots and world models (New #19).',
 'agent-directory-identities': ' 7 Nov: Palo Alto Networks in talks to buy agent-access start-up Clutch for ~$500M (New #12).',
 'personal-agent-identity': ' 7 Nov: Meta Muse Spaces (New #13); Cashfree WebMCP checkout for agents in India (New #17).',
 'hybrid-on-device-moe': ' 7 Nov: LFM3-1.7B added to OpenRouter (6 Nov); no new Liquid AI release.',
 'eval-containment': ' 7 Nov: UK Cyber Security and Resilience Bill clause on agentic AI loss of control (New #5).',
 'looped-depth-models': ' 7 Nov: SenseNova-Loop-9B-Preview still trending on Hugging Face; no new release.',
}
for w in wl:
    w['lastChecked'] = DATE
    w['label'] = w['label'] + wnotes.get(w['id'], ' 7 Nov: re-searched in batched class and name queries and the HF/OpenRouter/HN feeds; nothing new.')

deadlines = [
 {'date': '2026-11-08', 'label': "Approximate: India's MeitY AI-regulation consultation paper ('within a month' of 8 Oct; still not out)", 'severity': 'medium'},
 {'date': '2026-11-13', 'label': 'Approximate: Inkling 2 Small open weights ("next week"); Reddit ends RSS; Conductor Cloud goes read-only', 'severity': 'medium'},
 {'date': '2026-11-15', 'label': "China's draft AI export-control catalogue: public comments close (MOFCOM/MOST No. 48)", 'severity': 'high'},
 {'date': '2026-11-16', 'label': "Anthropic watermarks Claude Opus 4.6, Opus 4.5, Sonnet 4.5 and Haiku 4.5; Apple's 18+ descriptors for romantic AI companions become mandatory; California 'kill switch' report", 'severity': 'medium'},
 {'date': '2026-11-18', 'label': 'Jensen Huang asked to a closed-door briefing for three House committees on reported Chinese spying', 'severity': 'high'},
 {'date': '2026-11-26', 'label': "Approximate: Anthropic aims to list before Thanksgiving (FT); roadshow timing in doubt", 'severity': 'high'},
]

SOURCES_OPENED = 36
runNotes = {
 'searches': "33 web searches. Tracking re-checks 10 (Anthropic cyber verification tiers, OpenAI EU watermark, AMD 2027 supply/MI500, Musubi PolicyLM, Claude Startups program, Meta Muse dossier, Multiply Labs, RECLAIM diffusion LM, Reflection Beam, Colorado deepfake complaint). Models and technology 8 (non-LLM 'new type of model' query, diffusion/state-space/world-model class query, PSI Aaronson-Ambainis, Hightouch Jev, Underdog speech model, AMI Labs/AMI Video, Qwen 4, viral X launch / Hugging Face clones) plus 2 watchlist name batches (Crouton Alpha/OpenRouter stealth; Liquid/Inception/Cartesia/Zyphra) and 1 OpenAI Unique Games context check. Applied AI and money 4 (OpenAI $11B round, Anthropic IPO timing, Palo Alto-Clutch, Ramp AI Index). People and policy 8 (India GCC AI hiring, UK agentic AI powers, RBI bank AI cyber audits, UAE AI jobs, Bank of England AI productivity, Jensen Huang/Megaspeed, DOJ AI impersonation fraud, London/Singapore AI pay). Saturday deep beat (regional and AI jobs) ran through the India GCC, UAE, London/Singapore, RBI, CERT-In, UK and BoE searches. Web search again returned mostly stale results; dated feeds pulled with curl did most of the finding (Techmeme, TechCrunch, The Verge, The Decoder, The Register, Ars Technica, SiliconANGLE, The Hacker News, Economic Times, Google blog, OpenAI RSS, Wired, BBC, MarkTechPost, Inc42, MediaNama, HN front page and search, Hugging Face new and trending, OpenRouter models API).",
 'pagesOpened': "36 pages and APIs (not counting 24 RSS feeds and listing APIs): PSI announcement, TechCrunch (7), The Register (5), Ars Technica (2), The Decoder, BBC, Hightouch, MediaNama (2), Inc42, Wired (2), SiliconANGLE, pwn.ai, Planned Obsolescence, Crusoe newsroom, Hugging Face (Conway Research listing and Woof card), Scott Aaronson's blog, Economic Times (2), Bank of England Monetary Policy Report, Vals (home and CyberBench), Censys blog. Feeds and listing APIs (HN, HF new/trending, OpenRouter, news RSS) are not counted.",
 'blocked': "openai.com pages 403 (wet-lab agents, Hacktron); MarkTechPost article 403 (feed worked); CNBC RSS 403; VentureBeat 429; GitHub 403 (trending page and API, including PSI's Lean repo); community.openai.com 404; Bloomberg, FT, NYT and The Information paywalled; arXiv API not attempted; x.com not attempted",
 'notCovered': "GitHub trending (403); live X snapshot; PSI Lean repository contents (GitHub 403); Vals network-attack results not on its public site; November AI jobs data for UAE, UK, Singapore and EU (searches returned only older salary guides and job boards); arXiv not checked this run",
 'trackingCleanup': "10 oldest re-checked by name and product: 1 resolved (Claude Startups program closed to new applications), 9 retired, 0 updated. One tracked item moved to Developing (DoJ Super Intelligence Task Force). Yesterday's 26 stories: 6 carried as Developing (Anthropic IPO, CERT-In/RBI, Google schools, AI stocks, METR, Inkling 2 Small), 20 joined tracking",
 'corrections': 'None',
}

new = [s for s in S if s['section'] == 'new']; dev = [s for s in S if s['section'] == 'developing']
full = {
 'edition': ED, 'date': DATE, 'tz': 'Asia/Kolkata', 'format': 'v3', 'editionType': 'daily', 'degraded': False, 'degradedReason': '',
 'sourcesOpened': SOURCES_OPENED, 'shareable': True, 'shareBlockers': [], 'scanCount': 33,
 'counts': {'new': len(new), 'developing': len(dev), 'tracking': len(tracking)}, 'tiers': tiers, 'stories': stories,
 'tracking': tracking, 'retired': retired, 'movers': movers, 'arcs': arcs, 'resolved': resolved, 'heldBack': heldBack,
 'noChange': noChange, 'runNotes': runNotes, 'deadlines': deadlines, 'watchlist': wl,
}
page = {k: full[k] for k in ['edition', 'date', 'tz', 'format', 'editionType', 'degraded', 'degradedReason', 'sourcesOpened', 'shareable']}
page['counts'] = {'new': len(new), 'developing': len(dev)}
page.update({'tiers': tiers, 'stories': stories, 'deadlines': deadlines})

# ---------------------------------------------------------------- assemble
prev = open(PREV).read()
head = prev[:prev.index('<body>')]
script = prev[prev.index('<script>\n(function(){'):]
desc = "An AI system proves the Aaronson-Ambainis conjecture. Plus OpenAI's $11B at $1.25T, open models closing in on gated hacking AI, and Congress summoning Jensen Huang."
ogd = 'AI Daily Signal, edition %d (7 Nov 2026): %d new stories, %d developing.' % (ED, len(new), len(dev))
head = re.sub(r'<title>.*?</title>', '<title>AI Daily Signal — Edition %d — 7 November 2026</title>' % ED, head)
head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(desc), head)
for pr in ['og:title', 'twitter:title']:
    head = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % pr, lambda m: m.group(1) + html.escape(lead['h']), head)
for pr in ['og:description', 'twitter:description']:
    head = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % pr, lambda m: m.group(1) + html.escape(ogd), head)
head = head.replace('2026-11-06', DATE)
out = head + body + '<script id="page-data" type="application/json">\n' + json.dumps(page, indent=1, ensure_ascii=False) + '\n</script>\n\n' + script
open(OUT, 'w').write(out)
json.dump(full, open('state/signal-state.json', 'w'), indent=1, ensure_ascii=False)
print('new', len(new), 'dev', len(dev), 'tracking', len(tracking), 'tiers', tiers, 'n24', sum(1 for s in new if s['new24h']), 'retired', len(retired))
