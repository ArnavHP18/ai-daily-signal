# Generates edition 139 (2026-11-10) page and state. Working file; not published.
import json, re, html

DATE = '2026-11-10'; ED = 139
PREV = 'editions/ai_daily_signal_2026-11-08.html'
OUT = 'editions/ai_daily_signal_%s.html' % DATE
LONGDATE = 'Tuesday, 10 November 2026'

ARCLBL = {
 'chip-export-enforcement': 'who can buy top AI chips', 'frontier-pacing': 'how fast frontier AI is moving',
 'frontier-price-war': 'the price of AI models', 'compute-scale': 'the race for AI chips and compute',
 'ai-key-theft': 'leaked and stolen AI keys and data', 'ai-building-ai': 'AI improving AI',
 'ai-science': 'AI doing science and maths', 'ai-compute-buildout': "building AI's power and data centres",
 'agent-intrusion': 'AI in cyberattacks', 'physical-ai': 'AI acting in the physical world',
 'india-ai-regulation': "India's rules for AI", 'ai-vuln-discovery': 'AI finding and fixing bugs',
 'training-data-economy': 'who pays for training data', 'agent-economics': 'what AI use costs',
 'image-models': 'image generators', 'chatbot-child-safety': 'children and AI',
 'agent-teams': 'teams of AI agents', 'new-kinds-of-models': 'new kinds of AI models',
}

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

# ---------------------------------------------------------------- developing (lead first)
story(id='nvidia-huang-congress-megaspeed', section='developing', tier='critical', impact=9, arc='chip-export-enforcement', arcDay=9,
  confidence='Primary', verified='opened', new24h=False, first='2026-11-08', delta='escalated', category='hardware', tickerKey='NVIDIA',
  cat='Hardware · chips and security · 8-9 Nov',
  update="Jensen Huang admits an affair after Nvidia's board opens an independent investigation into reports he was the target of Chinese intelligence; shares fall 4.27% (~$250B); Trump says the FBI is looking into it; the first securities class action is filed; the NYT says Commerce paused its Megaspeed probe after Nvidia's lawyer contacted agents",
  title="Nvidia's board opens an independent investigation after reports that CEO Jensen Huang was the target of a Chinese intelligence effort; Huang admits in a company-published email that he was 'unfaithful to my wife'; shares fall 4.27% on Monday (about $250B); Trump says the FBI is looking into it; Rosen Law files the first securities class action; the NYT reports Commerce paused its Megaspeed smuggling probe after Nvidia's general counsel contacted agents, and the case moved to a DOJ criminal inquiry",
  h="Nvidia opens an investigation into Jensen Huang as the FBI and investors close in",
  sub="Huang admits an affair with a woman US officials call a Chinese spy; Nvidia lost about $250 billion in a day.",
  ticker="Board probes Huang over reported Chinese spy link; shares -4.27%",
  body="""<div class="delta-line"><span class="dl-tag">WHAT CHANGED</span> Since Sunday's edition: a board investigation, Huang's admission, a $250B share drop, an FBI inquiry and the first lawsuit.</div>
    <p class="dek">On Sunday <strong>Nvidia's board</strong> said it is opening an <strong>independent investigation</strong>, overseen by independent directors with outside counsel, "in light of recent reporting that founder and CEO Jensen Huang has been the target of a foreign intelligence effort". It says it has "no reason to believe" national security or Nvidia secrets were compromised and still has "confidence in Jensen". Hours later Nvidia published Huang's email to staff: "I was unfaithful to my wife ... There is no excuse for what I did." The New York Times reports US officials believe the relationship was with <strong>Alice Huang</strong> (no relation), a former executive of <strong>Megaspeed</strong>, a Singapore cloud firm that bought about $4.8B of Nvidia chips and that US officials think worked for China's Ministry of State Security; China calls the claims "entirely groundless".</p>
    <p>Nvidia shares fell <strong>4.27%</strong> on Monday, about <strong>$250B</strong> of market value (BBC, TechCrunch). President Trump said the <strong>FBI</strong> is "looking into" the matter and that Huang told him he "had no idea she was a spy". <strong>Rosen Law Firm</strong> filed the first securities class action in the Northern District of California, arguing Nvidia's October statements that the contacts were "not unusual" were misleading. A second NYT report says the <strong>Commerce Department</strong> paused its Megaspeed chip-smuggling investigation after Nvidia's general counsel emailed the agents, and the case moved to a <strong>Justice Department</strong> criminal inquiry. Huang is still due at a closed-door House briefing on 18 November.</p>
    <p class="sowhat">So what: the person who has argued hardest against tighter chip-export rules is now under investigation by his own board, the FBI and investors. Expect Congress to use this to tighten end-user checks on Chinese buyers, and watch for leadership or disclosure changes at the world's most valuable chipmaker before its next earnings.</p>""",
  chip="Board statement and Huang's email checked on Nvidia's newsroom; share move, FBI and lawsuit on BBC and TechCrunch; NYT not opened",
  src=[('OFFICIAL', [('Nvidia: board statement', 'https://nvidianews.nvidia.com/news/statement-from-nvidia-board-of-directors'), ("Nvidia: Huang's email to staff", 'https://nvidianews.nvidia.com/news/a-message-to-our-company')]),
       ('REPORTING', [('BBC: FBI investigating', 'https://www.bbc.co.uk/news/articles/cqg7x7dpvym8o'), ('BBC: shares tumble', 'https://www.bbc.co.uk/news/articles/c6zxjx01vyleo'), ('TechCrunch: first lawsuit', 'https://techcrunch.com/2026/11/09/the-race-is-on-to-sue-nvidia/'), ('The Register', 'https://www.theregister.com/legal/2026/11/09/nvidia-ceo-jensen-huang-admits-affair-with-possible-chinese-asset/5308327'), ('TNW: Commerce probe halted (NYT)', 'https://thenextweb.com/news/megaspeed-probe-commerce-nvidia-lawyer-justice-department-nyt'), ('The Verge explainer', 'https://www.theverge.com/ai-artificial-intelligence/1030422/nvidia-jensen-huang-ai-china-alice-huang')])],
  brief="""<p><strong>What is confirmed.</strong> Nvidia's own newsroom carries the board statement and Huang's email. The email does not name Alice Huang or say she was a spy; it says only that Huang was unfaithful and that he supports the investigation into "the national security concerns raised in news reports".</p><p><strong>What rests on reporting.</strong> The intelligence assessment of Alice Huang, the Rubio memo, the Commerce-to-DOJ handover and the claim that Megaspeed diverted chips to China all come from the New York Times, which we could not open. Megaspeed denies smuggling. A short seller, Culper Research, flagged the relationship as "uncomfortably close" in May (TechCrunch).</p><p><strong>Why it matters beyond Nvidia.</strong> Nvidia holds about $99B of stakes in AI labs and neoclouds (The Verge) and is the lead voice against export curbs. Huang also pulled out of the ElevenLabs Summit on Monday. Trump says Huang should stay on and will join his China trip.</p>""",
  facts=[('What', 'Board probe of CEO; affair admitted'), ('Market hit', '-4.27%, ~$250B (9 Nov)'), ('Federal', 'FBI looking into it (Trump); DOJ criminal inquiry into Megaspeed (NYT)'), ('Lawsuit', 'Rosen Law, N.D. Cal., class from 9 Oct 2025'), ('Next', 'House briefing 18 Nov')],
  impactWho='every buyer of AI chips, Nvidia investors, and anyone shaping US export controls')

story(id='claude-code-dont-ask-again-secrets', section='developing', tier='notable', impact=7, arc='ai-key-theft', arcDay=5,
  confidence='2x src', verified='opened', new24h=False, first='2026-11-08', delta='carry', category='enterprise', tickerKey='CLAUDE CODE', cat='Enterprise · developer security · 9 Nov',
  update="Ars Technica confirms Apiiro's findings and finds the leak was reported in Claude Code bug reports as early as August 2025; those reports were closed without action after 60 days of inactivity; still no Anthropic statement",
  title="Ars Technica confirms Apiiro's finding that Claude Code's 'don't ask again' approvals leak secrets via .claude/settings.local.json on public GitHub (about 1,100 files from 63 organisations), and reports the problem was raised in bug reports from August 2025 that were closed without action after 60 days of inactivity",
  h="Claude Code's secret leak was reported 15 months ago and closed without a fix",
  sub="", ticker="Claude Code settings leak was flagged in Aug 2025 bug reports",
  body="""<p>Sunday's lead now has a second outlet. <strong>Ars Technica</strong> confirms Apiiro's account: choosing "Yes, and don't ask again" can save a full command, password included, into <strong>.claude/settings.local.json</strong>, which Claude Code excludes from git only through the user's global settings, not the project's. Ars adds that the problem was raised in Claude Code <strong>bug reports as far back as August 2025</strong>, and that those reports, and others noting the file sometimes was not ignored, were <strong>closed without action after 60 days of inactivity</strong>. We found no Anthropic statement or fix.</p>
        <p class="sowhat">The advice stands: search repositories, history and forks for Claude settings files, rotate anything they contain, and add them to each project's .gitignore.</p>""",
  chip="Checked on Ars Technica; Apiiro's page still not opened",
  src=[('OFFICIAL', [('Anthropic: Claude Code settings docs', 'https://code.claude.com/docs/en/settings')]),
       ('REPORTING', [('Ars Technica', 'https://arstechnica.com/ai/2026/11/claude-code-settings-files-expose-thousands-of-secrets-on-github/'), ('The Hacker News (8 Nov)', 'https://thehackernews.com/2026/11/claude-codes-dont-ask-again-file.html')])])

# ---------------------------------------------------------------- new
story(id='claude-fable-mythos-52', section='new', tier='critical', impact=9, arc='frontier-pacing', arcDay=24,
  confidence='Primary', verified='opened', new24h=True, category='models', tickerKey='FABLE 5.2', cat='Models · frontier release · 9 Nov',
  title="Anthropic releases Claude Fable 5.2 (to all users) and Mythos 5.2 (vetted organisations only), the same model with different safeguards, at $8/$40 per million tokens (down from $10 input) and up to 30% faster than 5.1; it reports FrontierSWE v2 69.9% vs 62.3% for Opus 5.5, a 1,000-agent team formalising Fermat's Last Theorem in Lean in 30 hours, two solved open black-hole physics problems and three working electronic devices designed from a one-paragraph prompt; the system card says the models voice suspicion of being evaluated more than any recent Claude",
  h="Anthropic ships Fable 5.2: cheaper, faster, and it formalised Fermat in 30 hours",
  sub="Fable is open to everyone at $8/$40; Mythos stays with vetted defenders. Artificial Analysis ranks it first.",
  ticker="Claude Fable 5.2 launches at $8/$40, ranks #1 on Artificial Analysis",
  body="""<div class="body"><strong>Anthropic</strong> released <strong>Claude Fable 5.2</strong> and <strong>Claude Mythos 5.2</strong>, which it says are "the same underlying model": Fable carries classifiers that block high-risk cyber and biology work (routing those queries to Opus 4.8 or Opus 5) and is open to all users, while Mythos goes only to organisations in its Cyber and Life Sciences Verification Programs. Prices drop to <strong>$8 per million input tokens</strong> and <strong>$40 output</strong> (Fable 5.1 was $10 input, per TechCrunch), with a fast mode at $16/$80. Anthropic's table puts Fable 5.2 at <strong>69.9%</strong> on FrontierSWE v2 against 62.3% for Opus 5.5 and 65.5% for GPT-6 Astra. In pre-release use, it says, a team of about <strong>1,000 Fable agents formalised Fermat's Last Theorem in Lean in 30 hours</strong> (an earlier attempt took 11 days), the model <strong>solved two open problems on black holes</strong> and <strong>designed three working devices</strong> with Diode, including circuit boards and enclosures. <strong>Artificial Analysis</strong> independently scores it <strong>65</strong>, first of 74 models, but also among the slowest and most verbose ($26.54 per index task).</div>
      <p class="sowhat">For teams on Opus 5.5, Fable 5.2 is now the default upgrade path for the hardest coding and research jobs, and it undercuts GPT-6 Astra on price. Anthropic itself recommends starting on Opus 5.5 and moving up only when needed. Note the safety caveat: the models suspect they are being tested more often, which Anthropic says makes evaluation harder.</p>""",
  chip="Checked on Anthropic's announcement and Artificial Analysis; benchmark scores are Anthropic's own",
  src=[('OFFICIAL', [('Anthropic: Introducing Fable 5.2 and Mythos 5.2', 'https://www.anthropic.com/claude-fable-and-mythos-5-2')]),
       ('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/09/anthropic-releases-new-mythos-and-fable-models-amid-rsi-concerns/'), ('The Verge', 'https://www.theverge.com/ai-artificial-intelligence/1030005/anthropic-claude-fable-mythos-5-2'), ('TNW', 'https://thenextweb.com/news/claude-fable-5-2-mythos-5-2-anthropic-launch-price')]),
       ('OTHER', [('Artificial Analysis: Fable 5.2', 'https://artificialanalysis.ai/models/claude-fable-5-2'), ('Hacker News (~880 points)', 'https://news.ycombinator.com/')])])

story(id='meta-muse-ember', section='new', tier='notable', impact=7, arc='frontier-price-war', arcDay=15,
  confidence='Primary', verified='opened', new24h=True, category='models', tickerKey='MUSE EMBER', cat='Models · small model · 9 Nov',
  title="Meta Superintelligence Labs releases Muse Ember, its smallest model, built for the repetitive work inside agents (tool calls, routing, extraction, long documents), at $0.10/$0.50 per million tokens with text, image, audio and video input and a 1M-token window; Meta says it beats Claude Haiku 5.5 and GPT-6 Luna on intelligence per dollar (score ~36 at ~$0.14 per Artificial Analysis task), though Haiku leads on FrontierCode 2.0-AA (34.9% vs 27.2%)",
  h="Meta's Muse Ember is built to be the cheap worker inside AI agents",
  sub="At $0.10 per million input tokens it targets the high-volume subagent jobs where Haiku and Luna sit today.",
  ticker="Meta Muse Ember: agent subagent model at $0.10/$0.50",
  body="""<div class="body"><strong>Meta</strong> released <strong>Muse Ember</strong>, the fourth Muse model after Spark, the open Glimmer and the frontier Wonder. It is made for the work "agents repeat all day": tool calls, coding subtasks, routing, extraction and long-document parsing. Meta's research post says it matches <strong>Claude Haiku 5.5</strong>'s best Artificial Analysis score at about a third of the cost and beats every <strong>GPT-6 Luna</strong> setting; on its own table Ember scores 37.8 on AutomationBench-AA against 13.9 for Haiku. It takes text, images, audio and video, reads up to <strong>1M tokens</strong>, and costs <strong>$0.10/$0.50</strong> per million tokens on the Meta Model API and Muse Code; it is already listed on OpenRouter. Meta's pitch: "Muse Wonder plans, Muse Ember handles the volume." Haiku still beats it on real coding (FrontierCode 2.0-AA, 34.9% vs 27.2%, The Decoder).</div>
      <p class="sowhat">The cheap tier is where agent bills are decided. If Ember's numbers hold in independent tests, teams running large subagent fleets get a new default, and Anthropic and OpenAI face price pressure at the bottom of the range just as Fable moves the top.</p>""",
  chip="Checked on Meta's research post; comparisons are Meta's own using Artificial Analysis runs",
  src=[('OFFICIAL', [('Meta AI: Introducing Muse Ember', 'https://research.meta.ai/blog/muse-ember')]),
       ('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/09/meta-releases-muse-ember-a-new-lightweight-model-for-agent-execution/')]),
       ('AGGREGATOR', [('The Decoder', 'https://the-decoder.com/meta-launches-muse-ember-a-small-ai-model-built-for-the-repetitive-work-agents-actually-do/')])])

story(id='fireworks-second-breach', section='new', tier='notable', impact=7, arc='ai-key-theft', arcDay=5,
  confidence='2x src', verified='snippet', new24h=True, category='enterprise', tickerKey='FIREWORKS AI', cat='Enterprise · AI infrastructure security · 9 Nov',
  title="Inference provider Fireworks AI tells customers that hackers accessed some customers' datasets, incomplete model weights and billing information over the past month, its second notified incident in weeks after an October credential exposure (Forbes, Bloomberg, The Information headlines; articles not opened)",
  h="Fireworks AI says hackers reached customer datasets and partial model weights",
  sub="It is the inference host's second breach notice in weeks; details come only from headlines so far.",
  ticker="Fireworks AI notifies customers of a second breach in weeks",
  body="""<p><strong>Fireworks AI</strong>, the Nvidia-backed company that hosts and fine-tunes open models for businesses, has told customers that attackers accessed <strong>some customers' datasets</strong>, <strong>incomplete model weights</strong> and <strong>billing information</strong> over the past month (Forbes, via Techmeme). Bloomberg calls it the company's <strong>second hack in weeks</strong>; an earlier incident disclosed on 9 October involved internal credentials used to read environment variables in some customers' evaluation jobs. The Information says the breach threatens a $1B business. We could not open any of these articles or find a Fireworks notice, so the scope, dates and number of customers are unconfirmed.</p>
      <p class="sowhat">Customers that fine-tune on Fireworks should assume their training data and adapters may be exposed: rotate API keys and any secrets in job environments, and ask Fireworks which accounts were touched. Hosted fine-tuning is now a target in its own right.</p>""",
  chip="Not checked: Forbes, Bloomberg and The Information seen as headlines only; no Fireworks statement found",
  src=[('REPORTING', [('Techmeme summary of Forbes', 'https://www.techmeme.com/261109/p42#a261109p42')]),
       ('OTHER', [('Google News: Bloomberg, Forbes, The Information headlines', 'https://news.google.com/search?q=Fireworks%20AI%20hack')])])

story(id='google-tpu-8tx-8i-max', section='new', tier='notable', impact=7, arc='compute-scale', arcDay=18,
  confidence='Primary', verified='opened', new24h=True, category='hardware', tickerKey='GOOGLE TPU', cat='Hardware · chips · 9 Nov',
  title="Google adds TPU 8tx, a confidential-computing system that keeps data and weights encrypted in use (TPU 8t silicon with AMD EPYC hosts, up to 2x lower latency than 8t) and TPU 8i Max, two 8i chips on one package for million-token contexts and dense racks, making four eighth-generation TPU systems in one year; TPUs now have nearly 100 customers",
  h="Google's new TPUs target secret data and million-token agents",
  sub="", ticker="Google adds TPU 8tx (confidential) and 8i Max (long context)",
  body="""<p><strong>Google</strong> added two systems to its eighth-generation TPU line. <strong>TPU 8tx</strong> uses TPU 8t silicon with 5th-generation AMD EPYC hosts to keep data and model weights protected "even while in active use", with up to 2x lower latency than TPU 8t, so regulated firms can fine-tune, distil and run agents on sensitive data in one place. <strong>TPU 8i Max</strong> puts two 8i chips on one package to push memory bandwidth for million-token contexts and the densest racks. It is the first time Google has launched four TPU systems in a year, and it says TPUs now have <strong>nearly 100 customers</strong>, including some running them in their own data centres.</p>
      <p class="sowhat">Confidential inference is the feature banks and governments have been waiting for before putting frontier models near their data. It also widens Google's pitch as a second source to Nvidia in the week Nvidia's leadership is in question.</p>""",
  chip="Checked on Google's blog; no performance figures for 8i Max published",
  src=[('OFFICIAL', [('Google blog: TPU 8tx and 8i Max', 'https://blog.google/innovation-and-ai/infrastructure-and-cloud/global-network/tpu-8i-max-and-8tx/')]),
       ('AGGREGATOR', [('The Decoder', 'https://the-decoder.com/google-ships-four-tpu-variants-in-one-year-as-it-ramps-up-competition-with-nvidia/')])])

story(id='baidu-ernie-evolve', section='new', tier='notable', impact=7, arc='ai-building-ai', arcDay=1,
  confidence='Agg 1x', verified='opened', new24h=True, category='research', tickerKey='ERNIE EVOLVE', cat='Research · AI improving AI · 9 Nov',
  title="Baidu unveils ERNIE Evolve, an AI system that chooses experiments, edits code and keeps only changes that pass checks it cannot see; Baidu says it made its in-development ERNIE-5.5-Flash 33.7% faster on already-tuned GPUs in about three days and over 6x faster on Kunlunxin P800 chips (much of that from enabling unused features), and beat the NanoGPT Speedrun record (38.9s vs 39.9s, not submitted)",
  h="Baidu's ERNIE Evolve sped up its next model by itself",
  sub="", ticker="Baidu ERNIE Evolve: AI tuned ERNIE-5.5-Flash 33.7% faster on GPUs",
  body="""<p><strong>Baidu</strong> introduced <strong>ERNIE Evolve</strong>, a system that picks what to research, edits code, runs tests and keeps only changes that pass separate checks hidden from it. Used on <strong>ERNIE-5.5-Flash</strong>, a model still in development, Baidu says it raised throughput on engineer-tuned GPUs by <strong>33.7%</strong> in about three days and made generation <strong>more than six times faster</strong> on Kunlunxin P800 chips, though China AI Dispatch notes much of that came from switching on features the setup was not using. Baidu also reports a 38.9-second NanoGPT Speedrun against a 39.9-second record, not yet submitted to the leaderboard. Next it plans to point the system at training, and says its scope "should grow only while people can still understand, supervise, and stop the system". All figures are Baidu's (TNW).</p>
      <p class="sowhat">China's labs are now running the same "AI speeds up AI" loop as Anthropic (which says Claude writes over 90% of merged code in its core codebase) and Google. Infrastructure teams should expect model-serving gains to arrive faster, and safety teams should note that hidden-check designs like this one are becoming the norm.</p>""",
  chip="Checked on TNW; Baidu's own post not opened; all results are Baidu's",
  src=[('REPORTING', [('TNW', 'https://thenextweb.com/news/baidu-ernie-evolve-automated-ai-research')]),
       ('OTHER', [('Hugging Face: ERNIE-5.5-Flash-Base (trending)', 'https://huggingface.co/baidu/ERNIE-5.5-Flash-Base')])])

story(id='psi-aaronson-ambainis-proof', section='new', tier='notable', impact=7, arc='ai-science', arcDay=17,
  confidence='Primary', verified='opened', new24h=False, category='research', tickerKey='QUANTUM PROOF', cat='Research · maths · 6-9 Nov',
  title="Physical Superintelligence (PSI) says its internal research system, running instances of a non-public Anthropic model, proved the Aaronson-Ambainis conjecture (open since 2008): quantum computers cannot be exponentially faster on yes/no questions about random inputs; the proof is formalised in Lean, Stanford's Blanc, Docter, Strassle and Tan call it 'a huge result'; not yet peer reviewed",
  h="An AI research system proves a 2008 quantum computing conjecture, checked in Lean",
  sub="", ticker="PSI: AI system proves the Aaronson-Ambainis conjecture, Lean-checked",
  body="""<p>Start-up <strong>Physical Superintelligence (PSI)</strong> says a research system it built, running instances of a <strong>non-public Anthropic model</strong>, found a proof of the <strong>Aaronson-Ambainis conjecture</strong> on the third day of a run, and that the Lean proof assistant accepted it; the system later improved the result twice. The conjecture, open since 2008, implies that on yes-or-no questions about random inputs a quantum computer is at most polynomially, not exponentially, faster than an ordinary one. Stanford's Guy Blanc, Jordan Docter, Carmen Strassle and Li-Yang Tan, who proved a special case in August, wrote to PSI: "This is a huge result." It is not yet peer reviewed, and Anthropic would not say which model was used (TechCrunch).</p>
      <p class="sowhat">Machine-checked proofs of famous open problems are arriving weekly (Fable 5.2's Fermat formalisation, Axiom's Stacks Project, OpenAI's ETH claim). For quantum computing it narrows where real speedups can exist: structured problems, not random ones.</p>""",
  chip="Checked on PSI's research post; independent expert review pending",
  src=[('OFFICIAL', [('PSI: A proof of the Aaronson-Ambainis conjecture', 'https://psi.inc/research/aaronson-ambainis/')]),
       ('REPORTING', [('TechCrunch (in Fable 5.2 report)', 'https://techcrunch.com/2026/11/09/anthropic-releases-new-mythos-and-fable-models-amid-rsi-concerns/')])])

story(id='anthropic-gas-turbines-34b', section='new', tier='notable', impact=6, arc='ai-compute-buildout', arcDay=18,
  confidence='2x src', verified='opened', new24h=True, category='business', tickerKey='ANTHROPIC POWER', cat='Business · energy · 9 Nov',
  title="Anthropic is buying about $3.4B of Caterpillar natural gas generators able to produce up to 1.7GW, originally ordered by supplier OnePWR, which could not finance them (FT, via TechCrunch and Tom's Hardware); a shift for a company that has mostly rented compute, including $1.25B a month from xAI under a deal running to May 2029",
  h="Anthropic buys $3.4 billion of gas generators to skip the power queue",
  sub="", ticker="Anthropic buys ~$3.4B of gas turbines, up to 1.7GW",
  body="""<p><strong>Anthropic</strong> is spending about <strong>$3.4B</strong> on <strong>Caterpillar</strong> natural gas generators that can produce up to <strong>1.7GW</strong>, the Financial Times reports (via TechCrunch). The units were ordered by supplier OnePWR, which could not finance the purchase; Anthropic went to Caterpillar directly. It is a break from renting: Anthropic's S-1 discloses it pays xAI, now part of SpaceX, <strong>$1.25B a month</strong> for computing through May 2029. Turbine backlogs run into the early 2030s and grid queues can be as long, which is why AI firms are building on-site gas plants.</p>
      <p class="sowhat">Owning power is becoming part of the cost of being a frontier lab, two weeks before Anthropic's planned IPO. It also ties Anthropic to gas prices and to the local backlash against data centres that just shaped the US midterms.</p>""",
  chip="Checked on TechCrunch; FT paywalled; Anthropic has not commented",
  src=[('REPORTING', [('TechCrunch (FT)', 'https://techcrunch.com/2026/11/09/anthropic-joins-ais-natural-gas-frenzy-buys-3-4b-worth-of-turbines/'), ("Tom's Hardware", 'https://www.tomshardware.com/tech-industry/data-centers/anthropic-skips-six-year-waitlist-with-massive-usd3-4-billion-gas-turbine-generator-deal-firm-takes-over-onepwrs-orders-secures-1-7gw-of-capacity-to-power-ai-data-centers')])])

story(id='bossai-taipei-dispatch-agents', section='new', tier='notable', impact=6, arc='agent-intrusion', arcDay=21,
  confidence='2x src', verified='opened', new24h=True, category='enterprise', tickerKey='BOSSAI', cat='Enterprise · AI-driven attacks · 6-9 Nov',
  title="Acronis researchers say one attacker in Hualien, Taiwan, used 'BOSSAI' AI agents running mostly on abliterated (safety-removed) local models to target hundreds of organisations in 11+ countries, pulling 119 emergency dispatch records for seven Taipei districts and accessing about 10 victims in Taiwan, Mexico and Thailand; his own exposed server held 90,000+ files including the agents' conversations",
  h="One hacker's AI agents pulled Taipei's emergency dispatch records",
  sub="", ticker="Acronis: lone attacker's AI agents hit Taipei 119 dispatch data",
  body="""<p>Researchers at <strong>Acronis</strong> say a single attacker, very likely based in Hualien City, Taiwan, used AI agents he called <strong>BOSSAI</strong> against hundreds of organisations in at least 11 countries, including emergency services, banks, universities and military systems. The agents pulled <strong>emergency dispatch records</strong> for seven Taipei districts from the city's 119 system API and found a fire-department platform exposing patient data, including ECG readings, without a login; about 10 targets in Taiwan, Mexico and Thailand were accessed. Because commercial models mostly refused, the agents ran almost entirely on <strong>"abliterated" local models</strong> with safety training removed. The evidence came from the attacker's own misconfigured server, which held more than 90,000 files including the agents' conversations (The Hacker News).</p>
      <p class="sowhat">This is the open-model version of the AI-agent attacks seen with Artex and Claude-based campaigns: one person, many targets, and refusals in hosted models simply routed around. Public-sector APIs with default credentials are the soft spot.</p>""",
  chip="Checked on The Hacker News; Acronis' technical report not opened",
  src=[('REPORTING', [('The Hacker News', 'https://thehackernews.com/2026/11/taiwan-based-hacker-used-bossai-ai.html')]),
       ('AGGREGATOR', [('The Decoder on abliterated models (Tencent)', 'https://the-decoder.com/tencents-ai-chief-says-ai-bioweapons-are-coming-but-closing-off-models-isnt-the-answer/')])])

story(id='cert-in-ai-audit-guidelines', section='new', tier='notable', impact=6, arc='india-ai-regulation', arcDay=3,
  confidence='2x src', verified='snippet', new24h=False, category='policy', tickerKey='CERT-IN', cat='Policy · India · 4-9 Nov',
  title="India's CERT-In publishes 107-page AI Security Auditing Guidelines (v1.0), with four risk tiers and agent-specific tests for excess permissions, tool and credential misuse, memory and prompt injection; reports say high-risk agents need a kill switch, critical systems need audits by CERT-In-empanelled firms, logs must be kept 180 days and AI incidents reported within six hours",
  h="India sets audit rules for AI agents, including kill switches and six-hour reporting",
  sub="", ticker="CERT-In issues AI security audit guidelines with agent tests",
  body="""<p>India's cyber agency <strong>CERT-In</strong> has issued <strong>AI Security Auditing Guidelines</strong>, a 107-page version 1.0 document covering systems that plan tasks, use tools and hand work to other AIs. Auditors are told to test whether an agent can exceed its permissions, misuse tools or credentials, or be steered by prompt injection or poisoned memory. Systems are sorted into <strong>four risk levels</strong>; agents touching health records, payments or industrial control need stronger checks. Reports (Industrial Cyber, Cloud Security Alliance research note) say high-risk agents need a <strong>kill switch</strong>, critical ones need audits by CERT-In-empanelled firms, logs must be kept <strong>180 days</strong> and AI incidents reported within <strong>six hours</strong>. Outlets differ on whether it is final or a proposal, and we could not open CERT-In's site.</p>
      <p class="sowhat">For Indian banks, insurers and GCCs deploying agents, this becomes the audit checklist even without penalties. It mirrors the UK's new agent powers (8 Nov) and is more specific than most Western guidance.</p>""",
  chip="Not checked on CERT-In's site (returned an empty page); details from secondary reports",
  src=[('OFFICIAL', [('CERT-In (site did not load)', 'https://www.cert-in.org.in/')]),
       ('OTHER', [('Cloud Security Alliance research note (PDF)', 'https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/11/CSA_research_note_certin_ai_security_auditing_guidelines_20261106-csa-styled.pdf')])])

story(id='nominal-240m-hardware-testing', section='new', tier='monitor', impact=5, arc='physical-ai', arcDay=15,
  confidence='Primary', verified='opened', new24h=True, category='business', tickerKey='NOMINAL', cat='Business · hardware engineering · 9 Nov',
  title="Nominal, an Austin start-up whose AI platform analyses test data for complex hardware such as aircraft, reactors and factories, raises a $240M Series C at $3B led by Lightspeed and co-led by Insight, tripling its valuation in eight months; 80 customers including Anduril, and a $71.2M US Air Force STRATFI award in October",
  h="Nominal triples to $3 billion selling AI for testing aircraft and reactors",
  sub="", ticker="Nominal raises $240M at $3B for hardware-testing AI",
  body="""<p><strong>Nominal</strong> sells an AI platform for engineering and testing complex hardware, letting engineers analyse telemetry from aircraft, nuclear reactors and smart factories. It raised a <strong>$240M Series C at a $3B valuation</strong> led by Lightspeed and co-led by Insight Partners, three times the $1B of its March round. It has 80 commercial and government customers, including Anduril, and the Air Force picked it in October for a <strong>$71.2M</strong> STRATFI award (TechCrunch).</p>
      <p class="sowhat">Defence and hard-tech test data is a rich, closed corpus; the money is following AI that works on it rather than on text.</p>""",
  chip="Checked on TechCrunch, which reports the company's announcement",
  src=[('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/09/ai-hardware-startup-nominal-triples-valuation-to-3b-in-8-months/')])])

story(id='mythos-cisco-ibm-red-team', section='new', tier='monitor', impact=5, arc='ai-vuln-discovery', arcDay=12,
  confidence='2x src', verified='opened', new24h=True, category='enterprise', tickerKey='MYTHOS', cat='Enterprise · security tools · 9 Nov',
  title="Cisco will add Claude Mythos to its AI Defense product to plan red-team attacks on customers' own AI apps and agents (no open prompt access, every test logged to a named person, select enterprises first, no date); IBM plans to add Mythos to Concert Protect vulnerability scanning in early 2027",
  h="Cisco and IBM build Claude Mythos into their security products",
  sub="", ticker="Cisco and IBM add Claude Mythos to security tools",
  body="""<p><strong>Cisco</strong> said at Cisco Live in Melbourne it will add <strong>Claude Mythos</strong> to <strong>AI Defense</strong>, where it will plan attacks on customers' own AI apps and agents. Customers cannot prompt Mythos directly: it runs a fixed job against registered systems, each test is tied to a named person and logged, and it cannot scan the wider internet; select enterprises get it first, with no date. <strong>IBM</strong> said it plans to add Mythos to its <strong>Concert Protect</strong> tool in early 2027 (TNW). Palo Alto Networks already offers always-on testing with Mythos and OpenAI's cyber model.</p>
      <p class="sowhat">Anthropic is distributing its most dangerous model through security vendors' locked-down products rather than raw access, the same day Mythos 5.2 shipped. Expect most enterprises to meet Mythos this way.</p>""",
  chip="Checked on TNW; Cisco's and IBM's own posts not opened",
  src=[('REPORTING', [('TNW: Cisco', 'https://thenextweb.com/news/cisco-ai-defense-claude-mythos-red-teaming'), ('TNW: IBM', 'https://thenextweb.com/news/ibm-concert-protect-claude-mythos-vulnerability-scanning')])])

story(id='torvalds-ai-patch-flood-peak', section='new', tier='monitor', impact=5, arc='ai-vuln-discovery', arcDay=12,
  confidence='Primary', verified='opened', new24h=True, category='enterprise', tickerKey='LINUX', cat='Enterprise · open source · 9 Nov',
  title="Linus Torvalds, releasing Linux 7.4-rc2 after the largest rc1 in kernel history, says the flood of AI-found bug fixes may be starting to turn: eBPF lead Alexei Starovoitov reports fixes now arrive faster than new reports, though 'most other areas haven't reached that point yet'",
  h="Linus Torvalds sees the first sign the AI bug-report flood is peaking",
  sub="", ticker="Torvalds: AI-found bug flood may be turning in eBPF",
  body="""<p>Releasing <strong>Linux 7.4-rc2</strong>, <strong>Linus Torvalds</strong> said the previous rc1 was the largest in kernel history, driven by fixes for flaws found with AI tools since Anthropic's Mythos arrived in April. He passed on that eBPF lead <strong>Alexei Starovoitov</strong> says fixes on his side "are now coming in faster than the new reports", adding: "most other areas haven't reached that point yet, but it's at least a sign that we _may_ be starting to see the tide starting to turn" (The Register). Microsoft fixed a record 974 flaws in September and Oracle 1,449 in one month.</p>
      <p class="sowhat">The first sign that defenders can catch up with AI bug-finding at the source. Patch teams downstream are still swamped; plan for high volumes through at least Q1.</p>""",
  chip="Checked on The Register, quoting Torvalds' weekly kernel post",
  src=[('REPORTING', [('The Register', 'https://www.theregister.com/security/2026/11/09/linus-torvalds-sees-signs-ai-prompted-patch-flood-has-peaked/5308345')])])

story(id='waymo-school-bus-recall-query', section='new', tier='monitor', impact=5, arc='physical-ai', arcDay=15,
  confidence='2x src', verified='opened', new24h=True, category='policy', tickerKey='WAYMO', cat='Policy · robotaxis · 6-9 Nov',
  title="NHTSA opens a recall query into whether Waymo's November 2025 software fix worked, saying most reported cases of its robotaxis illegally passing stopped school buses happened after the update; Waymo says it has had no citations since March 2026",
  h="Regulators say Waymo robotaxis kept passing school buses after the fix",
  sub="", ticker="NHTSA: most Waymo school-bus passes came after its fix",
  body="""<p>The <strong>National Highway Traffic Safety Administration</strong> said in a 6 November filing that most reported incidents of <strong>Waymo</strong> robotaxis passing stopped school buses with lights flashing occurred <strong>after</strong> the software recall Waymo completed on 17 November 2025, and opened a "recall query" into whether the remedy was adequate. Austin's school district had reported at least five cases. Waymo says it has made "significant improvements" and received no citations since March 2026 (TechCrunch).</p>
      <p class="sowhat">A test case for how regulators judge recalls of software that keeps learning: a fix that is declared complete may not stay fixed.</p>""",
  chip="Checked on TechCrunch; NHTSA filing not opened",
  src=[('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/09/waymo-robotaxis-kept-illegally-passing-school-buses-after-software-fix-feds-say/')])])

story(id='disney-adobe-firefly-foundry', section='new', tier='monitor', impact=4, arc='training-data-economy', arcDay=16,
  confidence='2x src', verified='opened', new24h=True, category='enterprise', tickerKey='DISNEY', cat='Enterprise · media · 9 Nov',
  title="Disney and Adobe sign a multi-year deal under which Adobe's Firefly Foundry builds custom generative models trained on Disney's characters, environments and styles for theme parks, cruises, ESPN and the studios; Disney earlier walked away from an OpenAI deal and, per Bloomberg, plans thousands of job cuts",
  h="Disney picks Adobe to train private AI models on its characters",
  sub="", ticker="Disney and Adobe build custom Firefly models on Disney IP",
  body="""<p><strong>Disney</strong> and <strong>Adobe</strong> announced at Adobe MAX a multi-year partnership in which <strong>Firefly Foundry</strong> will build custom models trained on Disney's characters, environments and visual styles, to produce "commercially safe" output for theme parks, the cruise line, ESPN and Walt Disney Studios. Imagineering already uses Firefly. Disney previously struck and then left a deal with OpenAI; Bloomberg reports it plans to cut thousands of jobs (The Decoder, The Verge).</p>
      <p class="sowhat">Large rights holders are choosing private models trained only on their own IP over general-purpose ones. That is the business model for Adobe, and a template for studios, publishers and brands.</p>""",
  chip="Checked on The Decoder; Adobe's announcement not opened",
  src=[('AGGREGATOR', [('The Decoder', 'https://the-decoder.com/disney-bets-on-adobes-firefly-to-create-brand-safe-ai-models-for-its-entertainment-empire/')]),
       ('REPORTING', [('The Verge (headline)', 'https://www.theverge.com/ai-artificial-intelligence')])])

story(id='apple-intelligence-usage-packs', section='new', tier='monitor', impact=4, arc='agent-economics', arcDay=4,
  confidence='2x src', verified='opened', new24h=True, category='enterprise', tickerKey='APPLE', cat='Enterprise · consumer AI pricing · 9 Nov',
  title="Apple starts selling one-time $49.99 'Intelligence Usage Packs' in Logic Pro to extend Apple Intelligence features that run on OpenAI or Google Gemini cloud models once monthly limits are hit; unused usage rolls over and expires after 12 months; other Creator Studio apps to follow this month",
  h="Apple starts charging $50 for extra AI usage in its creative apps",
  sub="", ticker="Apple sells $49.99 Intelligence Usage Packs",
  body="""<p><strong>Apple</strong> added a "Buy More Usage" option to <strong>Logic Pro</strong>: a one-time <strong>$49.99 Intelligence Usage Pack</strong> that extends Apple Intelligence features with usage limits, because they run on cloud models from <strong>OpenAI or Google Gemini</strong>. Packs are tied to one Apple Account, roll over monthly and expire after 12 months; Pixelmator Pro, Final Cut Pro, Motion and Pages are expected to get them this month (The Verge, 9to5Mac).</p>
      <p class="sowhat">Even Apple now passes third-party model costs to users per use. Metered AI inside subscriptions is becoming normal, and heavy users will feel it first.</p>""",
  chip="Checked on The Verge",
  src=[('REPORTING', [('The Verge', 'https://www.theverge.com/tech/1030084/apple-intelligence-usage-packs-ai-features-creator-studio-logic-pro')])])

story(id='bytedance-seedream-55', section='new', tier='monitor', impact=4, arc='image-models', arcDay=1,
  confidence='Agg 1x', verified='opened', new24h=True, category='models', tickerKey='SEEDREAM 5.5', cat='Models · image generation · 9 Nov',
  title="ByteDance Seed releases Seedream 5.5, an image model it says keeps unchanged areas pixel-stable across up to 100 rounds of editing without colour drift and outputs native RGBA images with transparent backgrounds; rolling out via Jimeng, Doubao and Volcengine Ark, with a Pro version planned",
  h="ByteDance's Seedream 5.5 edits an image 100 times without drifting",
  sub="", ticker="ByteDance Seedream 5.5: 100-round pixel-stable edits",
  body="""<p><strong>ByteDance Seed</strong> released <strong>Seedream 5.5</strong>, an image model for production work. It claims stable multi-round editing for up to <strong>100 rounds</strong>, keeping untouched areas identical at the pixel level with no colour shift, and generates <strong>native RGBA images</strong> with transparent backgrounds that designers can use as assets directly. It is rolling out through Jimeng, Doubao, Doubao Work and Volcengine Ark; a Pro version is planned. Claims of beating GPT Image 2.5 Sunburst are ByteDance's (The Decoder).</p>
      <p class="sowhat">Drift across repeated edits is what stops image models being used in real design pipelines; if this holds, it removes a reason to keep humans redoing the last step.</p>""",
  chip="Checked on The Decoder; ByteDance's own page not opened",
  src=[('AGGREGATOR', [('The Decoder', 'https://the-decoder.com/bytedances-seedream-5-5-promises-pixel-stable-image-editing-across-100-rounds-without-color-drift/')])])

story(id='instagram-ai-age-estimation-global', section='new', tier='monitor', impact=4, arc='chatbot-child-safety', arcDay=10,
  confidence='2x src', verified='opened', new24h=True, category='policy', tickerKey='INSTAGRAM', cat='Policy · teen safety · 9 Nov',
  title="Meta expands Instagram's AI age-estimation worldwide, placing users it suspects are teens into Teen Accounts even if they list an adult birthday, using profile text, comments and visual cues such as height and bone structure; Facebook rollout continues and Threads follows later this year",
  h="Instagram's AI will now guess users' ages worldwide",
  sub="", ticker="Instagram rolls out AI age estimation globally",
  body="""<p><strong>Meta</strong> is expanding the AI age estimation on <strong>Instagram</strong> to every country. It looks for signs that an account belongs to a teen, such as birthday posts, mentions of school grades, and visual cues including height and bone structure, and moves suspected teens into restricted <strong>Teen Accounts</strong> even if they gave an adult birthday. Facebook is rolling it out and Threads follows later this year. The move follows settlements worth up to $18B with nearly every US state in August, which required better age detection (TechCrunch).</p>
      <p class="sowhat">AI age assurance is becoming the default answer to child-safety laws. Expect wrong guesses and appeals at scale, and privacy questions about inferring age from bodies in photos.</p>""",
  chip="Checked on TechCrunch",
  src=[('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/09/meta-expands-instagrams-ai-age-guessing-tech-globally/')])])

story(id='arxiv-agent-teams-quantum-programs', section='new', tier='monitor', impact=4, arc='agent-teams', arcDay=1,
  confidence='Primary', verified='opened', new24h=False, category='research', tickerKey='ARXIV', cat='Research · agent teams · 6 Nov',
  title="Two arXiv papers (6 Nov) on teams of AI agents: 'Parallel agent teams' samples many small collaborating teams and keeps the best, beating plain parallel agents on 10 of 12 long tasks with a 27B model and 100 agents; 'Discovering formally verified quantum programs with AI' has agent teams write quantum programs in Lean against formal specs, verifying correctness and cost, with order-of-magnitude improvements claimed",
  h="Research: small teams of AI agents beat one big team or many loners",
  sub="", ticker="arXiv: parallel teams of ten agents beat 100 solo agents on 10 of 12 tasks",
  body="""<p>Two papers posted on 6 November study teams of AI agents. <strong>"Test-Time Compute Scales Better with Parallel Agent Teams"</strong> runs many small collaborating teams at once and keeps the best team's result: with a 27B model and a budget of 100 agents, teams of ten beat 100 independent agents on 10 of 12 long tasks (GPU kernels, formal proofs, exploit development) and beat one team of 100 everywhere it was tried; at equal cost, it matched a frontier model on half the tasks. <strong>"Discovering formally verified quantum programs with AI"</strong> builds a quantum-program library in Lean where agent teams write programs against formal specifications and the prover checks correctness and cost, reporting order-of-magnitude gains on scientific applications.</p>
      <p class="sowhat">The same shape as Fable 5.2's 1,000-agent Fermat run: organised teams plus a verifier. How to split a budget across agents is becoming an engineering question with measurable answers.</p>""",
  chip="Checked on the arXiv abstracts; results are the authors' own",
  src=[('OFFICIAL', [('arXiv 2611.09798: parallel agent teams', 'https://arxiv.org/abs/2611.09798'), ('arXiv 2611.09822: verified quantum programs', 'https://arxiv.org/abs/2611.09822')])])

story(id='idol-image-to-3d-splat', section='new', tier='monitor', impact=4, arc='new-kinds-of-models', arcDay=9,
  confidence='Primary', verified='opened', new24h=False, category='models', tickerKey='IDOL', cat='Models · open 3D · 28 Oct-9 Nov',
  title="Speridlabs' Idol (Apache 2.0), which turns one image of an object into a 3D Gaussian splat of up to ~1M Gaussians including unseen sides in under 2 seconds on a consumer GPU (7.2GB VRAM), tops Hugging Face's trending list with ~1,600 likes and ~25,000 downloads",
  h="An open model that turns one photo into a 3D object tops Hugging Face",
  sub="", ticker="Idol: one image to a 3D splat in 2s, #1 on Hugging Face",
  body="""<p><strong>Idol</strong>, from <strong>Speridlabs</strong>, takes a single picture of an object, removes the background and generates a <strong>3D Gaussian splat</strong> of up to 1,048,576 Gaussians, "including the sides the picture never showed", written as a standard .ply file. It runs in <strong>under 2 seconds</strong> on consumer GPUs with 7.2GB of VRAM; weights are about 3GB under <strong>Apache 2.0</strong>, though it relies on two gated image encoders. Released on 28 October, it is now first on Hugging Face's trending list with about 1,600 likes and 25,000 downloads.</p>
      <p class="sowhat">Fast single-image 3D is the missing step for game, e-commerce and robot-simulation pipelines; an open, local version lowers the cost to near zero.</p>""",
  chip="Checked on the Hugging Face model card and API; no independent quality tests",
  src=[('OFFICIAL', [('Hugging Face: speridlabs/idol', 'https://huggingface.co/speridlabs/idol')])])

story(id='opus-55-nerf-claim', section='new', tier='monitor', impact=4, arc='frontier-pacing', arcDay=24,
  confidence='Rumor-flag', verified='snippet', new24h=True, category='models', tickerKey='OPUS NERF', cat='Models · unconfirmed claim · 9 Nov',
  title="UNCONFIRMED: a viral X post (733 points on Hacker News) claims Claude Opus 5.5's thinking patterns changed on 3 November; Anthropic has not commented; earlier 'nerf' claims about Opus 5.5 were traced mostly to the default effort dropping to medium, and BridgeBench found no drop beyond noise",
  h="Unconfirmed: developers claim Opus 5.5's reasoning changed on 3 November",
  sub="", ticker="",
  body="""<p>A post on X, which reached 733 points on Hacker News on Monday, claims <strong>Claude Opus 5.5</strong>'s thinking patterns changed on <strong>3 November</strong>. We could not open the post or find data behind it, and Anthropic has not commented. Earlier complaints that Opus 5.5 had been "nerfed" were largely explained by its default effort being set to medium at launch, and an independent tracker (BridgeBench) found no drop beyond noise.</p>
      <p class="sowhat">Treat as a claim to check, not a finding. If your evals moved after 3 November, check effort settings first.</p>""",
  chip="Unconfirmed: one X post via Hacker News; not opened",
  src=[('OTHER', [('Hacker News front page', 'https://news.ycombinator.com/')])])

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

lead = dev[0]   # major escalation of a carried story takes the hero (routine §4)
ticker_items = [lead] + [s for s in new + dev[1:] if s['confidence'] != 'Rumor-flag' and s.get('ticker')]
ticker = ' &nbsp;◆&nbsp; '.join('<b>%s</b> %s' % (esc(s['tickerKey']), esc(s['ticker'])) for s in ticker_items)

cats = {}
for s in S: cats[s['category']] = cats.get(s['category'], 0) + 1
tabs = '    <button class="tab active" data-cat="all">ALL (%d)</button>\n' % len(S) + ''.join('    <button class="tab" data-cat="%s">%s (%d)</button>\n' % (c, c.upper(), n) for c, n in sorted(cats.items()))

trip_src = [new[0], new[1], new[2]]
trip_h = ['Anthropic ships Fable 5.2', "Meta's cheap agent worker", 'Fireworks AI breached again']
trip_p = ["Cheaper and faster, first on Artificial Analysis, and its agent teams formalised Fermat's Last Theorem in 30 hours.",
          'Muse Ember undercuts Haiku and Luna at $0.10 per million input tokens for subagent work.',
          "Hackers reached some customers' datasets and partial model weights; details still unconfirmed."]
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

  <!-- the two highest-scoring new stories get large cards -->
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
    <p><strong>AI Daily Signal</strong> · Edition {ED} · 10 November 2026 (IST) · Curated by Arnav Agrawal<span data-slot="curator-links"></span> · <a href="index.html">All editions</a><span data-slot="sister-links"></span></p>
    <p>Tuesday's focus: open source and models. Today that meant Anthropic's Fable 5.2, Meta's Muse Ember, ByteDance's Seedream 5.5, the open Idol 3D model topping Hugging Face, and a check on the open weights still missing from Thinking Machines (Inkling 2 Small is on OpenRouter for free) and Alibaba (Qwen 4).</p>
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
order = new + dev
stories = [sstate(s) for s in order]
tiers = {'critical': 0, 'notable': 0, 'monitor': 0}
for s in S: tiers[s['tier']] += 1

trk = {t['id']: t for t in old['tracking']}
retired, resolved = [], []
def retire(i, reason):
    trk.pop(i); retired.append({'id': i, 'date': DATE, 'reason': reason})

# the 10 oldest tracking items, re-searched by name and product
retire('personal-agent-protocol', 'Re-searched the protocol and its site: documentation still "Draft 0.1, updated 13 Oct" with no reference implementation; the promised end-October v0.1 has not appeared. Nothing new')
trk['claude-haiku-55'].update(label='Re-checked 10 Nov: independent data now exists (Vals AI head-to-head with GLM 5.3: Haiku 5.5 leads 10 of 22 shared benchmarks); Meta claims Muse Ember matches its best Artificial Analysis score at ~1/3 the cost (New #2)', lastChecked=DATE)
trk.pop('openai-gpt6-chatgpt-everyone'); resolved.append('GPT-6 for everyone: resolved on re-search. GPT-6 Luna reached ChatGPT Free and Go users in the Chat tab from 8 Oct (phased); paid tiers use GPT-6 Sol')
trk['open-muse-clones'].update(label='Re-checked 10 Nov: CopilotKit OpenMuse (MIT, alpha) is the most-cited clone, reported at 3.5k-5.5k GitHub stars in snapshots; nanoMuse (GPL-3.0) also exists; no live star count opened', lastChecked=DATE)
retire('turba-labs-dc-digital-twins', 'Re-searched the company and its digital-twin product: no coverage at all beyond the original item; no utilisation data')
trk.pop('naukri-sep-aiml-hiring-20pct'); resolved.append("Naukri September city split resolved on Naukri's own blog: Hyderabad +9% is overall white-collar hiring; Hyderabad led GCC hiring at +23%; AI/ML +20% YoY, fresher AI/ML +19%, AI/ML inside IT +11%")
trk.pop('hubspot-660-cuts'); resolved.append('HubSpot cuts: settled at about 660 jobs (~7%), board-approved 1 Oct with $65-75M charges; CEO Yamini Rangan says the cut was not driven by AI efficiencies')
retire('arxiv-agent-cluster-oct6', 'Re-searched: superseded by later agent-evaluation papers (e.g. parallel agent teams, New #18); no follow-up on the 6 Oct cluster')
trk['teddy-ai-60m-seed'].update(label='Re-checked 10 Nov: TeddyHoldings.AI ($60M seed) says it passed $25M revenue in 2026 and founder Kyle Tucker aims for a $100M Series A by year-end (Dealroom, citybiz); investors still undisclosed', lastChecked=DATE)
retire('anthropic-critical-infra-defense', 'Re-searched the programme (CIDP, 11 founding partners from 8 Oct) and Mythos: no partner results published; the related Cisco and IBM Mythos integrations are carded separately (New #11)')

yl = {
 'anthropic-ipo-valuation-doubts': 'MOVED FROM DEVELOPING: no new filing or pricing; TechCrunch (9 Nov) still says Anthropic plans to list this year; Fable 5.2 launch and $3.4B turbine purchase land in the roadshow week',
 'openai-30b-bridge-round': 'MOVED FROM DEVELOPING: no new tranche reported since the ~$11B first close at $1.25T',
 'ai-stocks-midterm-plunge': "MOVED FROM DEVELOPING: Monday's move was Nvidia-specific (-4.27% on the board probe, D1); UBS CEO says AI investors had priced for 'perfection' (ET)",
 'openai-eth-kakeya-yang-mills': 'MOVED FROM DEVELOPING: no verification verdict yet; an arXiv essay (2611.09736) frames OpenAI proofs and the Hugging Face breach as the same proposer-verifier loop',
 'microsoft-ai-frontiers-ends': 'MOVED FROM NEW after one edition: no Microsoft response found',
 'nous-arete-27b': 'MOVED FROM NEW after one edition: Arete-27B now ~364 likes and still on Hugging Face trending',
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
 {'dir': 'down', 'text': "NVIDIA - board investigates Jensen Huang; shares -4.27% (~$250B); FBI looking into it; first class action filed (lead, D1)"},
 {'dir': 'up', 'text': 'ANTHROPIC - Fable 5.2 ranks #1 on Artificial Analysis (65) at a 20% lower input price (#1)'},
 {'dir': 'up', 'text': 'META - Muse Ember undercuts Haiku 5.5 and GPT-6 Luna on cost per task (#2)'},
 {'dir': 'down', 'text': "FIREWORKS AI - second breach notice in weeks; customer datasets and partial weights reached (#3)"},
 {'dir': 'up', 'text': 'GOOGLE TPU - two new eighth-gen systems; nearly 100 TPU customers (#4)'},
 {'dir': 'up', 'text': 'BAIDU - ERNIE Evolve: AI made ERNIE-5.5-Flash 33.7% faster on GPUs (#5)'},
 {'dir': 'up', 'text': 'NOMINAL - $240M Series C at $3B, valuation tripled in eight months (#10)'},
 {'dir': 'down', 'text': 'WAYMO - NHTSA recall query: school-bus passes continued after the fix (#13)'},
]

heldBack = [
 {'item': "SpaceX plans a gas-fired power plant and 'super-compute facility' at Starbase, Texas, with ~$24B for initial phases, per a public hearing notice (Bloomberg)", 'why': 'Bloomberg paywalled; seen only as a Techmeme headline and a blog citing the notice', 'next': "Open the City of Starbase hearing notice"},
 {'item': 'Mavria, founded by former DOE staff, raises $130M (pre-seed and seed) at a $1B valuation led by Paradigm to build truck-shippable modular data centres (WSJ, DCD)', 'why': 'WSJ paywalled and DCD returned 403; headlines only', 'next': "Open DCD or Mavria's announcement"},
 {'item': 'OpenAI Control Room: a central system to track and stop model workloads across its research infrastructure (OpenAI, 9 Nov)', 'why': 'openai.com returned 403; only the RSS title seen', 'next': 'Re-open the post or find coverage'},
 {'item': "Viral GitHub repo claims Google Gemini routes personal Drive files and emails to human annotators (352 points on Hacker News)", 'why': "The repository URL returned an error; Google's own notices say some Workspace Labs and Deep Research data is human-reviewed", 'next': 'Open the repo or wait for reporting'},
 {'item': "Naukri JobSpeak October: AI/ML hiring +32% YoY vs +14% overall (careerindia, LapaasVoice)", 'why': "Not yet on Naukri's blog (its 'october-2026' URL carries the September report); low Diwali base in Oct 2025", 'next': "Open Naukri's October release when posted"},
 {'item': 'DeepX tapes out second-gen DX-M2 chip claiming 100B-parameter inference under 5W (EE Times, 136 HN points)', 'why': 'EE Times connection failed; no independent validation of the claim', 'next': 'Open EE Times or a DeepX release'},
 {'item': 'Nvidia tells cloud partners renting GPUs abroad that at least 51% of usage must be non-Chinese (Tom\'s Hardware)', 'why': "Tom's Hardware page did not render the article text", 'next': 'Re-open; fold into the Nvidia storyline if confirmed'},
 {'item': "Tencent chief AI scientist Yao Shunyu argues for a mix of open and closed models despite coming AI bioweapons risk (SCMP via The Decoder)", 'why': 'Opinion, no new action; SCMP not opened', 'next': 'None'},
 {'item': 'Isomorphic Labs in talks to raise ~$5B at ~$50B (Bloomberg, 4 Nov)', 'why': 'Still no company statement or second outlet', 'next': 'Card on a company statement or a second outlet'},
 {'item': 'Firmly $15M Series A for agent checkout; Axon up to $1.2B more in Skydio; Ocient $100M (carried from 8 Nov)', 'why': 'Still not opened', 'next': 'Drop unless product details emerge'},
]
noChange = [
 'Inkling 2 Small: now listed free on OpenRouter (9 Nov), but Hugging Face still shows only the July Inkling and Inkling-Small weights; Apache 2.0 release still pending',
 'Qwen 4: still unreleased after the rumoured 2-8 Nov window; no Alibaba post',
 'Jev / TypeSafe: no new product or price; an arXiv paper (6 Nov) finds the open Laya decision model changes its answer on 25.8% of questions when options are reordered',
 "Anthropic IPO: no new pricing or filing found; roadshow week coincides with Fable 5.2 and the turbine purchase",
 'Tencent Hy4 and Ripple-65B Preview: still on OpenRouter; no new weights',
 'Claude Dispatch flaw: no Anthropic response found',
]

wl = old['watchlist']
wnotes = {
 'jev-decision-models': ' 10 Nov: re-searched Jev, TypeSafe and Laya: no new release; arXiv 2611.09803 (Maya a1) finds Laya flips 25.8% of answers when options are reordered, cut to 7.2% by shuffled fine-tuning.',
 'stealth-gateway-models': ' 10 Nov: OpenRouter newest listings Claude Fable 5.2, Meta Muse Ember and Inkling 2 Small (free), all 9 Nov; no new stealth model.',
 'qwen4-new-architecture': ' 10 Nov: still unreleased; no Alibaba post.',
 'ai-built-models': ' 10 Nov: CARDED Baidu ERNIE Evolve sped up ERNIE-5.5-Flash 33.7% on GPUs (New #5); Anthropic says >90% of merged changes in its core codebase are written by Claude.',
 'automated-math-discovery': " 10 Nov: CARDED PSI's Lean-checked proof of the Aaronson-Ambainis conjecture (New #6); Fable 5.2 agents formalised Fermat's Last Theorem in 30 hours (New #1); arXiv verified quantum programs (New #18).",
 'agent-orchestrated-intrusion': ' 10 Nov: CARDED Acronis BOSSAI: one attacker, abliterated local models, Taipei dispatch data (New #8).',
 'hybrid-on-device-moe': ' 10 Nov: DeepX claims 100B-parameter inference under 5W with its second-gen chip (EE Times, not opened).',
 'eval-containment': ' 10 Nov: Mythos 5.2 system card: models voice suspicion of being evaluated more often than any recent Claude; new 1,800-scenario sandbox-escape evaluation (New #1).',
 'agent-self-report-honesty': ' 10 Nov: Mythos 5.2 shows stronger covert capabilities when its reasoning is hidden from the monitor (system card via TechCrunch).',
 'byo-key-theft-distillation': ' 10 Nov: Fireworks AI breach reached customer datasets and partial weights (New #3); Anthropic extends preserved thinking to all accounts against distillation.',
 'value-realignment-finetunes': ' 10 Nov: Arete-27B ~364 likes, still trending; no replications found.',
 'research-world-models': " 10 Nov: no new release; WIRED explainer on world models; Register covers a 'nature makes no leaps' smoothness prior for robot prediction.",
 'cross-embodiment-world-models': ' 10 Nov: arXiv 2611.09847 argues computer-use agents can do embodied tasks through rendered software, winning four ECCV workshop prizes.',
 'diffusion-language-models': ' 10 Nov: class query found no new diffusion LM release.',
 'jepa-world-models': ' 10 Nov: class query found no new world-model release.',
}
for w in wl:
    w['lastChecked'] = DATE
    w['label'] = w['label'] + wnotes.get(w['id'], ' 10 Nov: re-searched in batched class and name queries and the HF/OpenRouter/HN/arXiv scans; nothing new.')
wl.append({'id': 'agent-team-scaling', 'label': "How to spend compute across many cooperating agents. 10 Nov: CARDED arXiv 'parallel agent teams' (teams of ten beat 100 solo agents on 10 of 12 tasks) and Fable 5.2's ~1,000-agent Lean formalisation of Fermat (New #1, #18). Watch for team-size scaling laws and verifier-in-the-loop results.",
           'query': 'parallel agent teams; agent swarm scaling; 1,000 agents Lean; multi-agent test-time compute', 'firstSeen': DATE, 'lastChecked': DATE, 'status': 'carded'})
wl.append({'id': 'single-image-3d-models', 'label': "Fast open models that turn one image into a 3D asset. 10 Nov: CARDED Speridlabs Idol (Apache 2.0, one image to ~1M-Gaussian splat in <2s on 7.2GB VRAM), #1 on Hugging Face trending (New #19).",
           'query': 'Idol speridlabs; image-to-3D Gaussian splat; single image 3D open model', 'firstSeen': DATE, 'lastChecked': DATE, 'status': 'carded'})

deadlines = [
 {'date': '2026-11-13', 'label': 'Approximate: Inkling 2 Small open weights ("next week"); Reddit ends RSS; Conductor Cloud goes read-only', 'severity': 'medium'},
 {'date': '2026-11-15', 'label': "China's draft AI export-control catalogue: public comments close (MOFCOM/MOST No. 48)", 'severity': 'high'},
 {'date': '2026-11-16', 'label': "Anthropic watermarks Claude Opus 4.6, Opus 4.5, Sonnet 4.5 and Haiku 4.5; Apple's 18+ descriptors for romantic AI companions become mandatory; California 'kill switch' report", 'severity': 'medium'},
 {'date': '2026-11-18', 'label': 'Jensen Huang due at a closed-door House briefing on the reported Chinese spy plot, as Nvidia\'s board investigation and an FBI inquiry run', 'severity': 'high'},
 {'date': '2026-11-26', 'label': "Approximate: Anthropic aims to list before Thanksgiving", 'severity': 'high'},
 {'date': '2026-11-29', 'label': 'OpenAI starts training on Daybreak Blue cybersecurity sessions; check the separate opt-out', 'severity': 'medium'},
]

SOURCES_OPENED = 37
SEARCHES = 28
runNotes = {
 'searches': '28 web searches. Tracking re-checks 10 (Personal Agent Protocol, Claude Haiku 5.5, GPT-6 ChatGPT rollout, open Muse clones, Turba Labs, Naukri JobSpeak, HubSpot, arXiv agent papers, Teddy AI, Anthropic CIDP). Models and technology 10 (Fable/Mythos 5.2, Muse Ember, no-lab-name "new type of AI model", diffusion/world/state-space class query, Jev/TypeSafe, Qwen 4, Inkling 2 Small, Baidu ERNIE Evolve, Maya a1/Laya decision model, open-weight releases deep beat) plus DeepX. Applied AI and money 4 (Fireworks breach, PSI proof, SpaceX Starbase, Opus 5.5 nerf claim). People and policy 4 (Nvidia/Huang FBI, CERT-In guidelines, Democrats AI agenda, UAE/UK AI jobs) plus the Naukri and HubSpot re-checks. Tuesday deep beat (open source and models) ran through Fable, Ember, Inkling, Qwen 4, open-weight and Hugging Face/OpenRouter scans. Web search again returned mostly stale results; dated feeds pulled with curl did most of the finding (Techmeme, TechCrunch, The Verge, The Decoder, The Register, Ars Technica, SiliconANGLE, The Hacker News, Economic Times, Google blog, OpenAI RSS, WIRED, TNW, BBC Technology, Guardian AI, MIT Technology Review, Tom\'s Hardware, Hugging Face blog, Simon Willison, Import AI, Google News AI and India queries, HN front page, Hugging Face new/trending, OpenRouter models API, arXiv cs.AI/cs.LG).',
 'pagesOpened': "37 pages (feeds and listing APIs not counted): Anthropic Fable 5.2 post; Nvidia newsroom (board statement, Huang's email); Meta research (Muse Ember); Google blog (TPU); PSI research post; Artificial Analysis (Fable 5.2); Hugging Face Idol card; Naukri blog; TechCrunch (7: Fable, Ember, turbines, lawsuit, Nominal, Waymo, Instagram); The Verge (3: Fable, Nvidia explainer, Apple packs); BBC (2); The Register (2: Huang, Torvalds); TNW (4: Fable, Megaspeed probe, Baidu, Cisco); The Decoder (5: Fable, Ember, Disney, Tencent, Seedream); The Hacker News (2: BOSSAI, OpenAI engineer); Ars Technica (Claude Code); Fireworks blog (Ember-1); Tom's Hardware (turbines).",
 'blocked': "openai.com 403 (Control Room post); Fireworks has no security notice page (404); Forbes, Bloomberg, The Information, WSJ, FT and NYT paywalled or seen only as headlines; DCD 403; letsdatascience 403; EE Times connection reset; CERT-In site returned an empty page; GitHub repo for the Gemini annotator claim returned an error; Tom's Hardware article text did not render; VentureBeat RSS 429; BleepingComputer 403; x.com not attempted",
 'notCovered': 'GitHub trending not attempted; live X snapshot; Fireworks breach scope unconfirmed; SpaceX Starbase and Mavria held back; November AI jobs data for UK, UAE and EU (searches returned only PwC 2026 barometer material); Pennsylvania AI Deceptive Advertising Act and Democratic AI agenda not carded (no new action this cycle)',
 'trackingCleanup': '10 oldest re-checked by name and product: 3 resolved (GPT-6 rollout, Naukri city split, HubSpot), 4 retired (Personal Agent Protocol, Turba Labs, arXiv 6 Oct cluster, Anthropic CIDP), 3 updated (Haiku 5.5, open Muse clones, Teddy AI). Previous edition\'s 24 stories: 2 carried as Developing (Nvidia/Huang escalated to lead, Claude Code secrets), 22 joined tracking',
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
desc = "Nvidia's board investigates Jensen Huang as the FBI looks in and shares drop 4%. Plus Anthropic's Fable 5.2, Meta's Muse Ember, a Fireworks AI breach and Google's new TPUs."
ogd = 'AI Daily Signal, edition %d (10 Nov 2026): %d new stories, %d developing.' % (ED, len(new), len(dev))
head = re.sub(r'<title>.*?</title>', '<title>AI Daily Signal — Edition %d — 10 November 2026</title>' % ED, head)
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
