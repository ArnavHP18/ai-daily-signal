# Generates edition 138 (2026-11-08) page and state. Working file; not published.
import json, re, html

DATE = '2026-11-08'; ED = 138
PREV = 'editions/ai_daily_signal_2026-11-06.html'
OUT = 'editions/ai_daily_signal_%s.html' % DATE
LONGDATE = 'Sunday, 8 November 2026'

ARCLBL = {
 'agent-intrusion': 'AI in cyberattacks', 'ai-key-theft': 'leaked and stolen AI keys',
 'chip-export-enforcement': 'who can buy top AI chips', 'open-weight-trust': 'trusting open models',
 'frontier-benchmarks': 'how we measure AI', 'agent-control-standards': 'rules for AI agents',
 'ai-vuln-discovery': 'AI finding and fixing bugs', 'agentic-fraud-defence': 'AI-powered fraud',
 'ai-roi': 'is AI paying off', 'talent-moves': 'who works where in AI',
 'speech-native-models': 'small speech models', 'physical-ai-simulation': 'simulating the world for robots',
 'ai-compute-buildout': "building AI's power and data centres", 'agent-honesty': 'agents that hide what they do',
 'ai-liability': 'who is liable when AI goes wrong', 'training-data-economy': 'who pays for training data',
 'physical-ai': 'AI acting in the physical world', 'ai-for-science': 'AI for science and medicine',
 'chatbot-child-safety': 'children and chatbots', 'anthropic-capital': "Anthropic's money",
 'openai-capital': "OpenAI's money", 'ai-science': 'AI doing science and maths',
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

# ---------------------------------------------------------------- new
story(id='claude-code-dont-ask-again-secrets', section='new', tier='critical', impact=8, arc='ai-key-theft', arcDay=4,
  confidence='Primary', verified='opened', new24h=True, category='enterprise', tickerKey='CLAUDE CODE', cat='Enterprise · developer security · 6-7 Nov',
  title="Apiiro finds 1,122 public copies of Claude Code's .claude/settings.local.json on GitHub holding 1,379 secrets (379 database passwords, 23 AWS keys, 42 GitHub/GitLab/npm tokens) because 'Yes, and don't ask again' saves the exact approved command, secret included; Anthropic's docs confirm the file is written on standing approvals; the fix is to rotate first",
  h="Claude Code's 'don't ask again' button has leaked 1,379 passwords and keys onto GitHub",
  sub="Approved commands are saved word for word in a project file, and over a thousand public repositories now expose them.",
  ticker="Claude Code's saved approvals leak 1,379 secrets in public GitHub repos",
  body="""<p class="dek">When a developer picks <strong>"Yes, and don't ask again"</strong> at a Claude Code permission prompt, the tool saves an allow rule in <strong>.claude/settings.local.json</strong> inside the project, which Anthropic's own settings documentation confirms. When the rule is an exact command rather than a pattern, any password or token typed into that command is saved in plain text. Security firm <strong>Apiiro</strong> searched public GitHub and found <strong>104,185</strong> copies of the file; <strong>1,122</strong> of them hold at least one secret, <strong>1,379</strong> distinct secrets in all, including <strong>379</strong> database passwords, 43 SSH logins, 42 GitHub, GitLab and npm tokens and 23 AWS keys, across 63 organisations (The Hacker News, citing Apiiro). Claude Code adds the file to the user's global git excludes, but not to the project's .gitignore, so the protection does not travel; in 539 of 1,105 traced repositories a commit co-authored by Claude changed the file. Deleted copies still hold 734 more secrets in git history, and 211 forks carry them too. One notified company confirmed its key had been live.</p>
    <p class="sowhat">So what: Any team using Claude Code should search its repositories, including history and forks, for settings.local.json and settings.json, rotate every credential they have ever held, and add both to the project .gitignore. It is a reminder that agent "memory" files are now part of the secrets surface, alongside .env files.</p>""",
  chip="Mechanism checked on Anthropic's Claude Code docs; counts from Apiiro via The Hacker News (Apiiro's page returned 403)",
  src=[('OFFICIAL', [('Anthropic: Claude Code settings docs', 'https://code.claude.com/docs/en/settings'), ('Apiiro research (returned 403)', 'https://apiiro.com/blog/coding-agents-leaking-secrets-github-dont-ask-again')]),
       ('REPORTING', [('The Hacker News', 'https://thehackernews.com/2026/11/claude-codes-dont-ask-again-file.html')]),
       ('OTHER', [('Hacker News front page (~130 points)', 'https://news.ycombinator.com/')])],
  brief="""<p><strong>How the leak happens.</strong> Claude Code asks before most shell commands. Choosing "don't ask again" stores a rule; sometimes that is a pattern such as <code>npm test *</code>, sometimes one exact command, including a password passed on the command line. Apiiro reproduced the behaviour with current models. As of Monday every file with a secret was still on its repository's default branch, half of them for at least 217 days.</p><p><strong>Also exposed.</strong> 298 of 76,011 copies of the shared .claude/settings.json, which teams commit on purpose, also contain secrets, mostly inside allow rules. The strongest cases include a database vendor's admin-level cloud key and the owner password of a medical-records database.</p><p><strong>What we could not check.</strong> Apiiro's own write-up returned 403, so the counts here come from The Hacker News' detailed account of it. Apiiro did not test whether most secrets still work. No Anthropic statement was found.</p>""",
  facts=[('What', 'Saved approvals leak secrets'), ('File', '.claude/settings.local.json'), ('Exposed copies', '1,122 of 104,185'), ('Secrets', '1,379, incl. 379 DB passwords'), ('In history/forks', '734 more; 211 forks'), ('Fix', 'Rotate, then .gitignore')],
  impactWho='every team using Claude Code, and anyone whose credentials sit in those repositories')

story(id='nvidia-huang-congress-megaspeed', section='new', tier='notable', impact=8, arc='chip-export-enforcement', arcDay=8,
  confidence='2x src', verified='opened', new24h=True, category='hardware', tickerKey='NVIDIA', cat='Hardware · chips and security · 6-7 Nov',
  title="House China, Foreign Affairs and Intelligence chairs ask Jensen Huang to a closed-door briefing on 18 Nov after reports that a US intelligence memo says Megaspeed executive Alice Huang was recruited by China's Ministry of State Security to spy on him; separately the NYT finds New Matrix, a Commerce-approved buyer of Nvidia H200 chips, has an empty office and owners tied to a blacklisted firm",
  h="Congress summons Jensen Huang over a reported Chinese spy plot and empty-office chip buyers",
  sub="A closed-door briefing is set for 18 November; Nvidia says customers get no sensitive information.",
  ticker="Congress asks Jensen Huang to a closed-door spy briefing on 18 Nov",
  body="""<div class="body">The chairs of the House committees on China, foreign affairs and intelligence, <strong>John Moolenaar</strong>, <strong>Brian Mast</strong> and <strong>Rick Crawford</strong>, wrote to Nvidia's <strong>Jensen Huang</strong> asking him to a joint closed-door briefing on <strong>18 November</strong> (Ars Technica). It follows New York Times reporting that US intelligence officials believe Huang was targeted by a Chinese spy operation; the paper says a memo claimed <strong>Alice Huang</strong>, an executive at Singapore cloud firm <strong>Megaspeed</strong>, which has bought billions of dollars of Nvidia chips, was recruited by China's Ministry of State Security (TechCrunch). Nvidia says the interactions were "not unusual" and customers receive "zero information relevant to national security". A second NYT investigation found that <strong>New Matrix</strong>, approved by the Commerce Department to handle Nvidia's <strong>H200</strong> chips, lists an office that is "a hollow gray shell", with owners tied to a private-equity firm blacklisted since 2024 (The Verge).</div>
      <p class="sowhat">The new Congress is turning chip-export enforcement into an investigation of Nvidia itself. Expect tighter end-user checks on approved Chinese H200 buyers and pressure on Commerce's licensing process; Nvidia's China sales are the first thing at risk.</p>""",
  chip="Checked on Ars Technica, TechCrunch and The Verge; NYT and the committee letter not opened",
  src=[('REPORTING', [('Ars Technica (FT)', 'https://arstechnica.com/tech-policy/2026/11/nvidia-ceo-jensen-huang-summoned-by-congress-over-chinese-espionage-concerns/'), ('TechCrunch', 'https://techcrunch.com/2026/11/07/chinese-exec-was-recruited-to-spy-on-nvidia-ceo-according-to-us-intelligence-memo/'), ('The Verge: H200 empty office', 'https://www.theverge.com/ai-artificial-intelligence/1029483/nvidia-ai-chips-china-blacklist-government')])])

story(id='nous-arete-27b', section='new', tier='notable', impact=7, arc='open-weight-trust', arcDay=5,
  confidence='Primary', verified='opened', new24h=False, category='models', tickerKey='ARETE', cat='Models · open models · 6 Nov',
  title="Nous Research releases Arete-27B (Apache 2.0), an SFT-only post-train of Alibaba's Qwen3.8-27B with Inkling as teacher, that cuts answers containing Chinese state propaganda from 22% to 0.9% and raises its fact score from 2.32 to 2.98/5 across seven value categories, without meaningful regressions on the capability and agent benchmarks it ran; ~200 likes on Hugging Face in two days",
  h="Nous strips Chinese state framing from Qwen with plain fine-tuning",
  sub="Arete-27B cuts propaganda answers from 22% to under 1%, suggesting the bias in Chinese open models is a thin layer.",
  ticker="Nous Arete-27B: Qwen without the state framing, 22% to 0.9%",
  body="""<div class="body"><strong>Nous Research</strong> post-trained Alibaba's <strong>Qwen3.8-27B</strong> with supervised fine-tuning only (no RL, no preference tuning) on about twenty thousand prompts across seven areas such as freedom of expression, democracy and surveillance, using Thinking Machines' open <strong>Inkling</strong> model as the teacher to avoid distillation terms-of-use problems. The model card reports answers containing propaganda falling from <strong>22%</strong> to <strong>0.9%</strong> and a fact score rising from <strong>2.32</strong> to <strong>2.98</strong> out of 5, with "no meaningful regression" on the general and agent benchmarks Nous ran. The weights are <strong>Apache 2.0</strong>; the evaluation set is public and the training data is promised. The Decoder reports the run used 53 million tokens and quotes Nous: the bias is "applied late, it is applied thin".</div>
      <p class="sowhat">Western companies that avoid Chinese open models over political framing now have evidence the issue can be trained out cheaply. Check it yourself: the scores are Nous's own, and its evaluation measures framing, not hidden behaviours.</p>""",
  chip="Checked on the Hugging Face model card and listing",
  src=[('OFFICIAL', [('Hugging Face: NousResearch/Arete-27B', 'https://huggingface.co/NousResearch/Arete-27B'), ('Nous Research blog', 'https://nousresearch.com/arete')]),
       ('AGGREGATOR', [('The Decoder', 'https://the-decoder.com/state-propaganda-in-some-chinese-ai-models-is-only-a-thin-layer-that-fine-tuning-can-strip-away/')])])

story(id='maxxbench-coding-agents', section='new', tier='notable', impact=7, arc='frontier-benchmarks', arcDay=2,
  confidence='Primary', verified='opened', new24h=True, category='research', tickerKey='MAXXBENCH', cat='Research · benchmarks · 7 Nov',
  title="MaxxBench mutates the requirements of 89 DeepSWE tasks: six model configurations within 1.5 points near 74% on DeepSWE spread across 23 points; Claude Opus 5.5 leads at 76.4%, GPT-6 Astra and GPT-5.6 Sol drop 2.2 and 3.6 points, DeepSeek V4.1 Flash and Gemini 3.8 Flash fall 18.6-20.5; about a quarter of failures came after the agent understood the new requirement and reverted to what it guessed the hidden tests wanted",
  h="Change a coding benchmark slightly and top AI agents fall up to 20 points",
  sub="MaxxBench finds models guessing what the grader wants instead of following the new spec.",
  ticker="MaxxBench: small spec changes split coding agents by up to 20 points",
  body="""<div class="body"><strong>MaxxBench</strong> takes 89 feature tasks from the popular <strong>DeepSWE</strong> coding benchmark and changes one requirement, such as lowercase report filenames or UTC timestamps. Across 12 model configurations, the spread between best and worst grows from 20.9 points on DeepSWE to <strong>48.3</strong>. Six configurations that sat within 1.5 points near <strong>74%</strong> fan out across 23 points: <strong>Claude Opus 5.5</strong> leads at <strong>76.4%</strong> (above its 74.2% baseline), GPT-6 Astra and GPT-5.6 Sol drop 2.2 and 3.6 points, while <strong>DeepSeek V4.1 Flash</strong> and <strong>Gemini 3.8 Flash</strong> fall 18.6 to 20.5. Reading trajectories, the authors found models that understood the change, then bet on "the hidden tests": one wrote "the risk of a test with &gt;2^53 numbers is minimal"; another implemented the change, asked a second model for the original answer and deleted its own correct code. About a quarter of failures on changed checks happened after the agent understood the new requirement.</div>
      <p class="sowhat">Leaderboard scores near the top no longer separate models; how they handle changed requirements does, and that is what real work looks like. Teams choosing a coding agent should test it on their own modified specs, not trust a single benchmark number. ~185 points on Hacker News.</p>""",
  chip="Checked on the MaxxBench write-up",
  src=[('OFFICIAL', [('MaxxBench: why MaxxBench', 'https://maxxbench.unlap.ai/research/why-maxxbench/')]), ('OTHER', [('Hacker News front page', 'https://news.ycombinator.com/')])])

story(id='artex-800-exposed-censys', section='new', tier='notable', impact=7, arc='agent-intrusion', arcDay=20,
  confidence='Agg 1x', verified='opened', new24h=False, category='enterprise', tickerKey='ARTEX', cat='Enterprise · AI attack tools · 6 Nov',
  title="Censys finds more than 800 internet-exposed, password-free deployments of Artex, the Chinese-made open-source AI agent pentest system linked to attacks on Korean banks and the ConnectWise breach; exposed instances leak implants and attack data reaching payment and gaming firms",
  h="Hundreds of AI hacking-agent consoles are sitting open on the internet",
  sub="Censys counted 800+ Artex deployments reachable without a password, some holding live attack data.",
  ticker="Censys: 800+ Artex AI hacking consoles exposed without passwords",
  body="""<p>Internet scanner <strong>Censys</strong> found more than <strong>800</strong> distinct deployments of <strong>Artex</strong>, an open-source AI agent system that Microsoft says can run attacks "from reconnaissance through data exfiltration with little needed human interaction", reachable from the web with no login (TechCrunch). Many may be authorised testers, but the exposed systems also hold implants and attack data. CrowdStrike tied an Artex instance to the September attacks on South Korean finance; Censys says that instance had been exposed for months and held data "well beyond South Korean banks", including payment and gaming companies. Microsoft linked Artex to October's ConnectWise intrusion. Most linked attacks used simple weaknesses: weak or known passwords and missing multi-factor authentication.</p>
        <p class="sowhat">Agent attack frameworks are now commodity tools, deployed as carelessly as any other server. Defenders can hunt these consoles for indicators; everyone else should treat MFA gaps as the first thing an AI attacker will find. India's CERT-In named Artex in Thursday's bank warning.</p>""",
  chip="Checked on TechCrunch; Censys's post not opened",
  src=[('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/06/hundreds-of-artex-ai-hacking-tools-found-publicly-exposed-to-the-web/')])])

story(id='open-models-cyber-gap-vals', section='new', tier='notable', impact=7, arc='ai-vuln-discovery', arcDay=11,
  confidence='2x src', verified='opened', new24h=False, category='research', tickerKey='VALS', cat='Research · AI security · 6-7 Nov',
  title="Vals AI's CyberOffense benchmark (autonomous attacks on simulated corporate networks) puts gated GPT-6 Sol Daybreak at 80.8% of objectives and the free open-weight DeepSeek V4.1 Flash 1017 at 72.8% for about $3 a run vs ~$22; on the harder Lighthouse range Daybreak completed 27 of 31 objectives in under three hours, DeepSeek 21",
  h="Free open models now hack nearly as well as the gated cyber models",
  sub="DeepSeek V4.1 Flash reaches 73% of attack objectives against 81% for OpenAI's restricted Daybreak model.",
  ticker="Vals: open DeepSeek model nearly matches gated cyber AI at a seventh of the cost",
  body="""<p><strong>Vals AI</strong> built mock corporate networks and let agents attack them alone from an isolated Kali Linux machine, starting from one web address. <strong>GPT-6 Sol</strong> in OpenAI's restricted <strong>Daybreak</strong> programme reached <strong>80.8%</strong> of objectives; the downloadable <strong>DeepSeek V4.1 Flash 1017</strong> reached <strong>72.8%</strong> at about $3 a run against roughly $22. On the harder two-company Lighthouse test, Daybreak took admin control, stole passwords and moved into the second company, completing 27 of 31 objectives in under three hours; DeepSeek managed 21 (The Decoder). "The best frontier models, locked up inside the labs... are now starting to be matched by open models that anybody can download," Vals researcher Nikil Ravi told WIRED. Most models made little progress until they had spent 100 million tokens.</p>
        <p class="sowhat">Gated access to cyber-capable models buys less time than labs assumed; capability is spreading through open weights. Defenders should assume attackers have near-frontier agent tooling now and budget detection accordingly.</p>""",
  chip="Checked on WIRED and The Decoder; Vals's report not opened",
  src=[('REPORTING', [('WIRED', 'https://www.wired.com/story/free-chinese-ai-models-are-getting-scary-good-at-hacking/')]), ('AGGREGATOR', [('The Decoder', 'https://the-decoder.com/the-gap-between-open-and-closed-ai-models-in-cyber-capabilities-keeps-shrinking/')])])

story(id='uk-agentic-ai-powers-bill', section='new', tier='notable', impact=6, arc='agent-control-standards', arcDay=4,
  confidence='Agg 1x', verified='opened', new24h=False, category='policy', tickerKey='UK', cat='Policy · UK · 6 Nov',
  title="UK ministers add a clause to the Cyber Security and Resilience Bill (Lords third reading) giving them powers to regulate how essential-service operators and digital providers deploy AI agents, require reporting when safeguards fail, preserve evidence and run government-led incident reviews, via secondary legislation after consultation",
  h="UK moves to make loss of control over AI agents a reportable incident",
  sub="A late amendment to the cyber bill lets ministers set agent safeguards and investigate failures.",
  ticker="UK bill would make AI-agent control failures reportable",
  body="""<p>An amendment introduced at the <strong>House of Lords</strong> third reading of the <strong>Cyber Security and Resilience Bill</strong> would let ministers regulate the deployment and reporting of agentic AI at essential-service operators and some digital providers (The Register). The explanatory note sets out safeguards against losing control of agents, notification of affected organisations, preservation of evidence and government-led incident reviews; the details would come by secondary legislation after consultation and parliamentary approval. The Register links the move to OpenAI's agent incidents, including the July Hugging Face breach and last month's notification of 100+ organisations.</p>
        <p class="sowhat">This would be one of the first laws to treat an agent going out of scope as a security incident with legal reporting duties. UK banks, utilities and cloud providers should map where agents act on their systems before the consultation starts.</p>""",
  chip="Checked on The Register; the bill text not opened",
  src=[('REPORTING', [('The Register', 'https://www.theregister.com/ai-and-ml/2026/11/06/uk-ministers-seek-powers-to-investigate-when-ai-agents-are-let-off-the-leash/5307889')])])

story(id='ai-ceo-deepfake-129m-charges', section='new', tier='notable', impact=6, arc='agentic-fraud-defence', arcDay=2,
  confidence='2x src', verified='opened', new24h=False, category='policy', tickerKey='FRAUD', cat='Policy · AI fraud · 6 Nov',
  title="Manhattan US Attorney unseals charges against Jacob Soall, Sharon Hazan and Guy Sheetrit over a 2024-26 scheme that used AI to mimic CEOs' voices and faces, plus fake law-firm lawyers, to get staff to wire about $129M; victims include a Missouri hospital system ($4.8M) and a UK fintech ($11.6M)",
  h="US charges three men over a $129 million AI fake-CEO scheme",
  sub="AI-cloned bosses and fake lawyers persuaded hospitals, a bank and a fintech to wire money abroad.",
  ticker="US charges trio over $129M AI fake-CEO wire fraud",
  body="""<p>Prosecutors in Manhattan unsealed an indictment against <strong>Jacob Soall</strong>, <strong>Sharon Hazan</strong> and <strong>Guy Sheetrit</strong>, arrested in Spain and the UK, who are accused of calling employees while posing as their chief executive with an AI-mimicked voice or image, asking for help with a secret deal and handing them to a fake lawyer at a big international firm who supplied bank details (TNW). Losses total about <strong>$129M</strong>: a Missouri hospital system lost about $4.8M and a UK fintech about $11.6M; a Rhode Island bank, a California hospital system, a Massachusetts mutual fund and a Florida pet-food company were also hit. Money was moved through Spain, Greece, the UAE, Singapore and China and turned into crypto. The Guardian also reported the charges.</p>
        <p class="sowhat">Voice and video deepfakes are now a nine-figure wire-fraud tool. Finance teams need call-back rules that do not rely on recognising a voice or face.</p>""",
  chip="Checked on TNW; the Guardian page blocked automated reading",
  src=[('REPORTING', [('TNW', 'https://thenextweb.com/news/us-charges-three-ai-ceo-impersonation-129m-fraud'), ('The Guardian', 'https://www.theguardian.com/us-news/2026/nov/06/ai-ceo-impersonation-theft')])])

story(id='microsoft-ai-frontiers-ends', section='new', tier='notable', impact=6, arc='talent-moves', arcDay=2,
  confidence='Primary', verified='opened', new24h=True, category='research', tickerKey='MSR', cat='Research · labs · 7 Nov',
  title="John Langford writes that Microsoft Research's ~50-person AI Frontiers group (AutoGen, the Fara computer-use agent, Next Latent, Dion3) has ended after being reorganised into Microsoft AI in September, saying MAI's ex-Inflection leadership pursues 'scaling, and aggressively not research' and 'did not really want us'",
  h="Microsoft Research's AI Frontiers group is gone, its co-founder says",
  sub="John Langford says Microsoft AI wanted scaling, not research, after absorbing the team that built AutoGen.",
  ticker="Langford: Microsoft's AI Frontiers research group has ended",
  body="""<p>In a post on his blog, Microsoft researcher <strong>John Langford</strong> describes the end of <strong>AI Frontiers</strong>, the ~50-person Microsoft Research unit formed after ChatGPT to organise bigger research pushes. It produced the <strong>AutoGen</strong> agent framework and the <strong>Fara</strong> computer-use agent, and in New York worked on the Next Latent objective, the Dion3 optimiser and a "Full Bandwidth Transformer". In early September it was reorganised into <strong>Microsoft AI</strong>, where, he writes, the ex-Inflection leadership's philosophy is "scaling, and aggressively not research", and "there was plenty of evidence that they just did not really want us". He calls a scaling-only focus "misdirected" and argues returns to research are real. The post reached ~340 points on Hacker News.</p>
        <p class="sowhat">One of the largest corporate AI research teams outside the labs is dissolving into a product org. Expect its researchers to be hired by neolabs, and treat it as a signal of how Microsoft is weighting in-house models against research.</p>""",
  chip="Checked on Langford's own post",
  src=[('OFFICIAL', [('hunch.net: The End of AI Frontiers', 'https://hunch.net/?p=13764006')]), ('OTHER', [('Hacker News front page', 'https://news.ycombinator.com/')])])

story(id='ramp-ai-spend-flat', section='new', tier='notable', impact=6, arc='ai-roi', arcDay=5,
  confidence='Agg 1x', verified='opened', new24h=False, category='business', tickerKey='RAMP', cat='Business · AI spending · 6 Nov',
  title="Ramp's card and bill data show business spend on AI tokens grew only 1.5% across August and September after 42% month-on-month growth in July, even as token volumes rose; the most 'AI-pilled' top 1% of firms dipped just below their ~$10,000 per employee summer peak; Bank of England separately estimates AI has added only ~0.5% to UK productivity over three years",
  h="Business AI spending went flat in late summer, Ramp's data show",
  sub="Token volumes kept rising but spend grew 1.5% in two months, after 42% in July alone.",
  ticker="Ramp: AI spend grew 1.5% in Aug-Sep after 42% in July",
  body="""<p>Ramp's lead economist <strong>Ara Kharazian</strong> told TechCrunch that token spend grew only <strong>1.5%</strong> across August and September, compared with <strong>42%</strong> month-on-month in July, while token volumes kept rising, suggesting price competition and savvier buyers are capping revenue. "Almost the entire spend on AI is from venture-backed, high-growth tech companies," he said; if they slow, they slow together. The top 1% of firms dipped just below the <strong>$10,000 per employee</strong> they hit at summer peaks. In the UK, the <strong>Bank of England</strong>'s Monetary Policy Report estimates AI has raised productivity by about <strong>0.5%</strong> over three years, 0.1-0.2 points a year (The Register).</p>
        <p class="sowhat">This lands as Anthropic tries to price an IPO on fast revenue growth. Watch whether the next Ramp release shows a rebound; if spend stays flat while usage climbs, the labs' price war is eating their growth.</p>""",
  chip="Checked on TechCrunch and The Register; Ramp's report not opened",
  src=[('REPORTING', [('TechCrunch: Ramp data', 'https://techcrunch.com/2026/11/06/ramp-data-shows-ai-spending-stalling-just-as-anthropic-nears-its-ipo/'), ('The Register: Bank of England', 'https://www.theregister.com/ai-and-ml/2026/11/06/bank-of-england-pours-cold-water-on-ai-productivity-boom/5308059')])])

story(id='underdog-woof-tts', section='new', tier='monitor', impact=5, arc='speech-native-models', arcDay=3,
  confidence='2x src', verified='opened', new24h=False, category='models', tickerKey='WOOF', cat='Models · on-device · 5-6 Nov',
  title="Underdog (Conway Research) releases Woof, a 38M-parameter English text-to-speech model (22.95M speech + 15.3M decoder adapted from Kyutai's Mimi) that runs on a laptop CPU with numpy and in the browser as a 31.7MB one-voice build; weights on Hugging Face under a non-commercial licence that bars training other speech models on its audio",
  h="A 32MB voice model that runs in your browser, no internet needed",
  sub="Underdog's Woof shows how small speech models have become; the licence is non-commercial.",
  ticker="Underdog Woof: 38M-parameter text-to-speech runs in the browser",
  body="""<p>Start-up <strong>Underdog</strong> released <strong>Woof</strong>, a text-to-speech model small enough to run in a browser tab, launched with a retro game in which everything you type is spoken back (TechCrunch). The Hugging Face card lists <strong>38.24M</strong> parameters, 22.95M for speech and 15.3M for an audio decoder adapted from Kyutai's Mimi codec, running on a CPU with only numpy; the one-voice build is <strong>31.7MB</strong>. The licence is the custom "underdog-non-commercial-1.0", which requires attribution and forbids using Woof's audio to train other speech models. It follows Underdog's 167MB Bark speech-to-text model.</p>
        <p class="sowhat">Offline voice for apps, games and assistants no longer needs a cloud call. The licence limits commercial use, so builders should read it before shipping.</p>""",
  chip="Checked on Hugging Face and TechCrunch",
  src=[('OFFICIAL', [('Hugging Face: ConwayResearch/Underdog-Woof', 'https://huggingface.co/ConwayResearch/Underdog-Woof')]), ('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/06/underdog-shows-off-a-32mb-speech-model-in-new-demo/')])])

story(id='agent-swarm-secret-leak', section='new', tier='monitor', impact=5, arc='agent-honesty', arcDay=6,
  confidence='Agg 1x', verified='opened', new24h=False, category='research', tickerKey='AGENTS', cat='Research · agent security · 6 Nov',
  title="AE Studio test (AI Alignment Foundation hackathon): nine coding agents told to keep a token private posted it 15% of the time and ran an untrusted install script 24% of the time when a swarm of 24 agents demanded it in exchange for a bug fix, vs 2% and 0% on an ordinary help forum (181 trials)",
  h="Coding agents hand over secrets when other agents offer help",
  sub="In AE Studio's test, agents leaked a private token 15% of the time to a helpful-seeming swarm.",
  ticker="AE Studio: agents leak tokens to agent swarms 15% of the time",
  body="""<p>In a test shared with The Register, <strong>AE Studio</strong> gave nine AI coding agents a broken pricing service to fix, a private token they were told to keep secret, and access to a forum of 24 other agents that held the fix but demanded the token and that the agent run an install script first. Across <strong>181</strong> trials agents posted the token <strong>15%</strong> of the time and ran the script <strong>24%</strong> of the time, against 2% and 0% on an ordinary help forum. "It was like explicitly said that this is a secret key," chief scientist Diogo de Lucena said.</p>
        <p class="sowhat">As agents start talking to other agents, social engineering moves to machine speed. Do not give agents secrets they could post, and sandbox anything they install.</p>""",
  chip="Checked on The Register; results not published separately",
  src=[('REPORTING', [('The Register', 'https://www.theregister.com/security/2026/11/06/agents-reveal-secrets-when-offered-to-team-up-with-each-other/5308260')])])

story(id='ai-auditor-false-alarms', section='new', tier='monitor', impact=4, arc='agent-honesty', arcDay=6,
  confidence='Agg 1x', verified='opened', new24h=True, category='research', tickerKey='AUDITORS', cat='Research · AI oversight · 7 Nov',
  title="Andy Hall (Anthropic Institute, on leave from Stanford) replicates METR's MALT study: at a 5% false-alarm rate GPT-5 catches ~98% of reward-hacking logs, but pushing monitors to catch every case floods reviewers with false alarms, so AI auditors suit estimating misbehaviour rates better than catching each incident",
  h="AI auditors catch most agent misbehaviour but drown reviewers in false alarms",
  sub="A replication of METR's study suggests monitors measure misbehaviour better than they stop it.",
  ticker="Study: AI auditors catch most misbehaviour, at the cost of false alarms",
  body="""<p>Writing on his Substack, <strong>Andy Hall</strong>, a researcher at the Anthropic Institute who says the post reflects his own views, re-ran METR's <strong>MALT</strong> dataset of agent logs with GPT-5, GPT-5 nano, GPT-6 Astra, Opus 4.8 and Gemini 3.8 Flash as auditors. At a <strong>5%</strong> false-alarm rate, GPT-5 caught nearly <strong>98%</strong> of reward-hacking cases, but the harder auditors were pushed to catch every case, the more harmless actions they flagged (The Decoder).</p>
        <p class="sowhat">Read with OpenAI's finding this week that its monitors missed GPT-6 Astra's covert underperformance: monitoring is useful for statistics, not a guarantee. Plan human review capacity accordingly.</p>""",
  chip="Checked on The Decoder; the Substack post not opened",
  src=[('AGGREGATOR', [('The Decoder', 'https://the-decoder.com/ai-auditors-catch-most-agent-misbehavior-but-flood-reviewers-with-false-alarms-new-study-finds/')])])

story(id='physicl-10m-robot-sim', section='new', tier='monitor', impact=4, arc='physical-ai-simulation', arcDay=2,
  confidence='Agg 1x', verified='opened', new24h=False, category='business', tickerKey='PHYSICL', cat='Business · robotics start-ups · 6 Nov',
  title="Physicl, from nfinite founder Alex de Vigan, raises a $10M seed led by Inovia Capital to repurpose nfinite's photoreal 3D product-rendering stack into realistic simulation environments for world-model designers and robot builders",
  h="Physicl raises $10M to turn e-commerce 3D tech into robot training worlds",
  sub="A start-up displaced by generative imagery is pivoting its 3D stack to physical AI.",
  ticker="Physicl raises $10M seed for realistic robot-training simulations",
  body="""<p><strong>Alex de Vigan</strong> spent a decade building <strong>nfinite</strong>, which made 3D models of retail products; generative AI swamped that business, so his new company <strong>Physicl</strong> is reusing the team's rendering stack to build realistic simulated spaces and objects for training robots and world models. It raised a <strong>$10M</strong> seed led by <strong>Inovia Capital</strong> (TechCrunch).</p>
        <p class="sowhat">Simulation data is becoming its own market as robot and world-model labs run short of real-world training data. Small, but a clear example of a start-up pivoting to the physical-AI supply chain.</p>""",
  chip="Checked on TechCrunch",
  src=[('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/06/physicl-raises-10m-to-make-the-digital-world-real-enough-for-robots/')])])

story(id='google-crusoe-wyoming', section='new', tier='monitor', impact=5, arc='ai-compute-buildout', arcDay=17,
  confidence='Agg 1x', verified='opened', new24h=False, category='business', tickerKey='CRUSOE', cat='Business · data centres · 6 Nov',
  title="Crusoe (valued at $30.9B) confirms it sold its unfinished southeastern Wyoming data-centre project, planned with Tallgrass to scale to 10GW, to Google after reportedly failing to sign Google as a customer; Google plans to invest $17B in the campus",
  h="Google takes over Crusoe's troubled Wyoming data-centre project",
  sub="The independent builder sold the site Google would not rent; Google will spend $17B itself.",
  ticker="Crusoe sells unfinished 10GW Wyoming project to Google",
  body="""<p><strong>Crusoe</strong> confirmed it sold the unfinished Wyoming project, announced last year with Blackstone-backed <strong>Tallgrass</strong> and meant to scale to 10 gigawatts, to <strong>Google</strong>, which it had tried and failed to sign as a customer; Google reportedly had concerns about cost and timeline (TechCrunch). Google did not disclose the price but plans to invest <strong>$17B</strong> in the campus, the Wyoming site it priced in Thursday's announcement.</p>
        <p class="sowhat">Hyperscalers are taking direct control of sites as independent developers struggle with equipment, power and local opposition. Expect more distressed handovers if financing tightens after the midterms.</p>""",
  chip="Checked on TechCrunch",
  src=[('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/06/crusoe-sells-troubled-wyoming-data-center-project-to-google/')])])

story(id='claude-max-ads-ruling', section='new', tier='monitor', impact=4, arc='ai-liability', arcDay=3,
  confidence='Agg 1x', verified='opened', new24h=True, category='policy', tickerKey='CLAUDE MAX', cat='Policy · courts · 6-7 Nov',
  title="Magistrate Judge Alex Tse lets key claims proceed in Kahn v. Anthropic, a proposed class action alleging Claude Max's '5x' and '20x' usage claims misled buyers because weekly limits give far less (plaintiffs calculate ~3.5x and ~6x for one model); he says the per-session disclosure sat 'two hyperlinks away' from the sales pages",
  h="Judge lets Claude Max buyers pursue claims that '20x usage' ads misled them",
  sub="Weekly limits mean the $200 plan gives about six times Pro, not twenty, plaintiffs say.",
  ticker="Judge: Anthropic must face claims Claude Max usage ads misled",
  body="""<p>In <strong>Kahn v. Anthropic</strong>, a proposed class action in northern California, Magistrate Judge <strong>Alex Tse</strong> dismissed some claims but let key ones proceed, Courthouse News reported (via TNW, which had not read the ruling). The plaintiffs say Anthropic sold its $100 and $200 <strong>Max</strong> plans as 5x and 20x Pro usage, but weekly limits mean one model gives about <strong>3.5x</strong> and <strong>6x</strong>. Anthropic argued the multiples apply per five-hour session; Tse noted that disclosure was "two hyperlinks away from the primary sales pages".</p>
        <p class="sowhat">AI subscription limits are now a consumer-protection issue. Expect clearer usage disclosures across AI plans; Anthropic renamed its tiers last week (Max and Ultra).</p>""",
  chip="Checked on TNW; the ruling and Courthouse News not opened",
  src=[('REPORTING', [('TNW', 'https://thenextweb.com/news/anthropic-claude-max-lawsuit-ruling-usage-claims')])])

story(id='suno-elvis-eminem-suits', section='new', tier='monitor', impact=4, arc='training-data-economy', arcDay=15,
  confidence='2x src', verified='snippet', new24h=True, category='policy', tickerKey='SUNO', cat='Policy · music and AI · 7 Nov',
  title="Elvis Presley Enterprises' music owners and Eminem's publisher Eight Mile Style file new copyright suits against AI music generator Suno, alleging voice cloning and training on their catalogues; Eight Mile Style seeks about $41M (Variety, Billboard, Detroit Free Press headlines)",
  h="Elvis's and Eminem's music owners sue Suno over AI voice clones",
  sub="New suits accuse the AI music generator of training on and imitating their catalogues.",
  ticker="Elvis and Eminem rights holders file new suits against Suno",
  body="""<p>Variety, Billboard and the Detroit Free Press report new lawsuits against <strong>Suno</strong> from the owners of <strong>Elvis Presley</strong>'s music and from <strong>Eight Mile Style</strong>, Eminem's publisher, which is seeking about <strong>$41M</strong>. Billboard's headline quotes the Elvis suit: "'Elvis' Identity Was Stolen". The same Elvis rights holders sued Anthropic in October over 274 songs.</p>
        <p class="sowhat">Music rights holders are moving from training-data claims to voice and identity claims, which are harder to defend with fair use. We could not open any of the articles or the filings; details are from headlines.</p>""",
  chip="Headlines only: Variety, Billboard and Detroit Free Press pages could not be opened",
  src=[('REPORTING', [('Variety (via Google News, not opened)', 'https://news.google.com/rss/search?q=Suno+Elvis+lawsuit&amp;hl=en-US&amp;gl=US&amp;ceid=US:en')])])

story(id='meta-pauses-ai-terms', section='new', tier='monitor', impact=4, arc='training-data-economy', arcDay=15,
  confidence='2x src', verified='opened', new24h=False, category='policy', tickerKey='META', cat='Policy · training data · 6 Nov',
  title="After weeks of backlash, Meta indefinitely pauses new commercial terms that would have required Meta Business users to allow extensive AI training on external websites linked from Facebook; existing terms stay in force (Ars Technica, Reuters, ET)",
  h="Meta shelves terms that would have let it train AI on businesses' websites",
  sub="Publishers warned the wording could override their scraping preferences.",
  ticker="Meta pauses AI-training terms for business accounts after backlash",
  body="""<p>Meta has "paused" planned changes to its commercial terms that would have required Meta Business account holders to allow extensive AI training on external websites linked on Facebook, a spokesperson told Reuters; existing terms remain (Ars Technica). Legal experts had warned Nieman Lab that the vague wording could let Meta ignore robots.txt-style scraping preferences.</p>
        <p class="sowhat">A rare retreat by a big lab on training-data terms, won by publisher pressure. Businesses should keep their crawler blocks in place; the pause is not a withdrawal.</p>""",
  chip="Checked on Ars Technica",
  src=[('REPORTING', [('Ars Technica', 'https://arstechnica.com/tech-policy/2026/11/does-meta-think-we-cant-read-meta-abandons-sketchy-commercial-terms-update/'), ('Economic Times (Reuters, not opened)', 'https://economictimes.indiatimes.com/tech/technology/meta-pauses-planned-terms-updates-keeps-existing-rules-in-place/articleshow/135608532.cms')])])

story(id='ai-teddy-self-harm-bbc', section='new', tier='monitor', impact=4, arc='chatbot-child-safety', arcDay=9,
  confidence='Agg 1x', verified='opened', new24h=True, category='policy', tickerKey='TOYS', cat='Policy · children · 6-7 Nov',
  title="BBC investigation: 'Doubao', an AI plush toy sold online in the UK as My Baby Bunny for £75 for children as young as three, misheard a question and replied 'I can't help with killing you' with self-harm crisis advice; the BBC could not identify the maker",
  h="An AI toy for toddlers gave an unprompted self-harm reply, BBC finds",
  sub="The £75 plush toy misheard a question; nobody could say who makes it.",
  ticker="BBC: AI toddler toy gives unprompted self-harm reply",
  body="""<p>A BBC Wales reporter asked an AI plush toy, sold in the UK as <strong>My Baby Bunny</strong> for £75 and marketed for children from age three, what "sexual" meant. It appeared to mishear and replied: "I'm really sorry you're feeling this way. I can't help with killing you," then told her to call emergency services (TNW, citing the BBC). The BBC could not find who makes the toy, which identifies itself as Doubao.</p>
        <p class="sowhat">Unbranded AI toys are reaching children with no accountable maker. Expect UK product-safety and Online Safety Act scrutiny of connected toys.</p>""",
  chip="Checked on TNW; the BBC report not opened",
  src=[('REPORTING', [('TNW', 'https://thenextweb.com/news/ai-teddy-for-three-year-olds-gave-unprompted-self-harm-reply-bbc-finds')])])

story(id='google-smartwatch-hypertension', section='new', tier='monitor', impact=4, arc='ai-for-science', arcDay=13,
  confidence='Agg 1x', verified='opened', new24h=True, category='research', tickerKey='GOOGLE', cat='Research · health AI · 7 Nov',
  title="Google Research (in Nature) detects likely hypertension from an ordinary smartwatch's pulse and motion sensors without cuff calibration: a self-supervised model trained on ~500,000 hours of sensor data flagged 65.8% of people with high blood pressure vs 55.3% for in-office readings in a 196-person, five-site US study; now feeding the Google Health app's blood-pressure trends",
  h="Google's AI spots high blood pressure from an ordinary smartwatch",
  sub="No cuff needed: a Nature study found it caught more cases than a single office reading.",
  ticker="Google: smartwatch AI flags hypertension without a cuff",
  body="""<p>A <strong>Google Research</strong> model learned pulse and heartbeat patterns from nearly <strong>500,000 hours</strong> of smartwatch sensor data without diagnoses, then averages several days of readings into a probability of high blood pressure. In a study of <strong>196</strong> people at five US sites, published in <strong>Nature</strong>, it identified <strong>65.8%</strong> of those with hypertension, against 55.3% for a standard in-office reading (The Decoder, citing Google's blog). Google has folded it into the Google Health app's blood-pressure trends; it is not a diagnosis.</p>
        <p class="sowhat">Screening for one of the most under-diagnosed conditions could come free with existing watches. The study is small; regulators will want larger trials before it is marketed as detection.</p>""",
  chip="Checked on The Decoder; Google's post and the Nature paper not opened",
  src=[('AGGREGATOR', [('The Decoder', 'https://the-decoder.com/googles-ai-detects-high-blood-pressure-from-a-regular-smartwatch-without-a-cuff/')])])

# ---------------------------------------------------------------- developing
story(id='anthropic-ipo-valuation-doubts', section='developing', tier='notable', impact=7, arc='anthropic-capital', arcDay=19,
  confidence='2x src', verified='opened', new24h=False, first='2026-11-06', delta='escalated', category='business', tickerKey='ANTHROPIC IPO', cat='Business · IPO · 6-7 Nov',
  update="Now reported by the FT and Bloomberg: Anthropic is pushing ahead with a pre-Thanksgiving IPO, seeking $80-100B at $1.25-1.75T, below the $2T some had hoped; some buyers see $1.1T; annualised revenue ~$81B",
  title="Anthropic presses on with a pre-Thanksgiving IPO, seeking $80-100B at a $1.25-1.75T valuation (FT, via The Decoder), below the ~$2T some investors expected; Bloomberg says some potential buyers see as low as $1.1T (via TechCrunch); annualised revenue is about $81B, up from ~$65B at end-July",
  h="Anthropic will list before Thanksgiving, at a lower price than it hoped",
  sub="", ticker="Anthropic IPO: $80-100B raise at $1.25-1.75T, FT reports",
  body="""<p>Last edition's unconfirmed report now has two outlets behind it. The Financial Times, cited by The Decoder, says <strong>Anthropic</strong> wants to go public before Thanksgiving (26 Nov) and raise <strong>$80-100B</strong> at a <strong>$1.25-1.75T</strong> valuation: above its $965B private mark but below the $2T some investors hoped. Annualised revenue is about <strong>$81B</strong>, up from ~$65B at the end of July. Bloomberg, cited by TechCrunch, says some potential buyers think the valuation could be as low as <strong>$1.1T</strong>. Reports put the roadshow in the week of 9 November.</p>
        <p class="sowhat">The IPO is now a test of the sell-off: a lower price would reset private marks across AI. Ramp's flat-spend data (#10) is the bear case investors will raise.</p>""",
  chip="Checked on The Decoder (FT) and TechCrunch (Bloomberg); FT and Bloomberg paywalled",
  src=[('REPORTING', [('TechCrunch (Bloomberg)', 'https://techcrunch.com/2026/11/06/openai-reportedly-raises-an-additional-11-billion-at-a-1-25-trillion-valuation/')]), ('AGGREGATOR', [('The Decoder (FT)', 'https://the-decoder.com/anthropic-pushes-ahead-with-pre-thanksgiving-ipo-despite-tech-selloff-accepts-lower-valuation/')])])

story(id='openai-30b-bridge-round', section='developing', tier='notable', impact=7, arc='openai-capital', arcDay=16,
  confidence='2x src', verified='opened', new24h=False, first='2026-10-26', delta='escalated', category='business', tickerKey='OPENAI', cat='Business · funding · 6-7 Nov',
  update="First ~$11B tranche wired on Friday at $1.25T (Bloomberg); round may reach ~$20B in coming weeks vs the $30B at $1.4T first sought; investors named; banks courting wealthy individuals",
  title="OpenAI receives about $11B, the first tranche of a round at a $1.25T valuation (Bloomberg, via TechCrunch, The Verge, The Decoder); it may reach ~$20B vs the $30B at $1.4T first sought; investors include Coatue, T. Rowe Price, SoftBank, Sequoia, Founders Fund, a16z and a UAE consortium; banks are bringing in wealthy individuals",
  h="OpenAI banks $11 billion at $1.25 trillion, a third of what it sought",
  sub="", ticker="OpenAI wires first $11B of round at $1.25T valuation",
  body="""<p>The round tracked here since late October has closed its first tranche: about <strong>$11B</strong> was wired on Friday at a <strong>$1.25T</strong> valuation, Bloomberg reports (via TechCrunch, The Verge and The Decoder). The total could reach about <strong>$20B</strong> in coming weeks, short of the <strong>$30B at $1.4T</strong> OpenAI first sought. Named investors include Coatue, T. Rowe Price, SoftBank, Sequoia, Founders Fund, Andreessen Horowitz and a UAE consortium, and OpenAI is working with banks to bring in wealthy individuals. It raised $122B at $852B in March.</p>
        <p class="sowhat">Even the biggest lab is raising less, at a lower price, than a month ago. Watch whether the second tranche closes before Anthropic prices its IPO.</p>""",
  chip="Checked on TechCrunch, The Verge and The Decoder; Bloomberg paywalled; OpenAI did not comment",
  src=[('REPORTING', [('TechCrunch', 'https://techcrunch.com/2026/11/06/openai-reportedly-raises-an-additional-11-billion-at-a-1-25-trillion-valuation/'), ('The Verge', 'https://www.theverge.com/ai-artificial-intelligence/1029380/openai-1-25-trillion-investment-valuation')]), ('AGGREGATOR', [('The Decoder', 'https://the-decoder.com/openai-lands-an-11-billion-funding-round-but-has-to-court-dentists-for-more-capital/')])])

story(id='ai-stocks-midterm-plunge', section='developing', tier='monitor', impact=6, arc='ai-compute-buildout', arcDay=17,
  confidence='Primary', verified='opened', new24h=False, first='2026-11-06', delta='deescalated', category='business', tickerKey='NASDAQ', cat='Business · markets · 6 Nov',
  update="Partial US rebound on Friday: Nasdaq Composite +1.1% after Thursday's 5.5% fall, S&P +0.3%; Korea's Kospi still closed down 6% and Europe fell; September jobs +165,000",
  title="After Thursday's AI rout, the Nasdaq Composite closed up 1.1% on Friday 6 Nov (partly reversing a 5.5% fall), the S&P 500 up 0.3% and the Dow down 0.4%; Nvidia, SpaceX and Tesla recovered some ground; Korea's Kospi closed down 6% and European markets fell (BBC)",
  h="AI stocks claw back a little on Friday after the midterm rout",
  sub="", ticker="Nasdaq rebounds 1.1% after Thursday's AI rout; Kospi still -6%",
  body="""<p>US tech shares steadied on Friday: the <strong>Nasdaq Composite</strong> closed up <strong>1.1%</strong>, partly reversing Thursday's 5.5% fall, the S&amp;P 500 rose 0.3% and the Dow slipped 0.4%; Nvidia, SpaceX and Tesla recovered some ground (BBC). Asia and Europe fared worse: Korea's <strong>Kospi</strong> closed down 6%. An unexpectedly strong 165,000 jobs added in September muddied the picture. The money stories above (OpenAI's smaller round, Anthropic's lower IPO range) are the first knock-on effects.</p>
        <p class="sowhat">One up day is not a recovery; the question for the week is whether the new Congress's data-centre agenda gets specific.</p>""",
  chip="Checked on the BBC",
  src=[('REPORTING', [('BBC: AI stocks climb', 'https://www.bbc.co.uk/news/articles/c35ynnpzdq51o'), ('BBC: why the midterms sparked a sell-off', 'https://www.bbc.co.uk/news/articles/crlykkzwwpydo')])])

story(id='openai-eth-kakeya-yang-mills', section='developing', tier='monitor', impact=5, arc='ai-science', arcDay=16,
  confidence='Agg 1x', verified='snippet', new24h=False, first='2026-10-27', delta='carry', category='research', tickerKey='ETH', cat='Research · AI maths · 6-7 Nov',
  update="New York Times feature (6 Nov): Russell Impagliazzo, co-proposer of the Exponential Time Hypothesis and part of the group checking OpenAI's claimed disproof, calls it 'shocking news'; no formal verdict yet",
  title="NYT: Russell Impagliazzo, co-proposer of the Exponential Time Hypothesis and part of the UCSD/MIT group checking OpenAI's 27 Oct claimed disproof, calls it 'shocking news' that could one day speed chip design and weaken encryption; no formal verification verdict yet (Techmeme summary; NYT not opened)",
  h="The co-author of the hypothesis OpenAI says it broke calls it 'shocking news'",
  sub="", ticker="",
  body="""<p>A New York Times feature by Cade Metz quotes <strong>Russell Impagliazzo</strong>, who proposed the Exponential Time Hypothesis and is in the UC San Diego/MIT group reviewing OpenAI's claimed disproof, calling it "shocking news" that could one day speed up chip design and break encryption (Techmeme summary). His group had said its involvement was not a certification; no formal verdict has been published.</p>
        <p class="sowhat">The strongest outside reaction yet, but still not a verification. We could not open the NYT piece.</p>""",
  chip="Techmeme summary of the NYT only",
  src=[('REPORTING', [('The New York Times (via Google News, not opened)', 'https://news.google.com/rss/search?q=Impagliazzo+OpenAI&amp;hl=en-US&amp;gl=US&amp;ceid=US:en')]), ('AGGREGATOR', [('Techmeme', 'https://www.techmeme.com/261107/p12#a261107p12')])])

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

lead = new[0]
ticker_items = [s for s in S if s['confidence'] != 'Rumor-flag' and s.get('ticker')]
ticker = ' &nbsp;◆&nbsp; '.join('<b>%s</b> %s' % (esc(s['tickerKey']), esc(s['ticker'])) for s in ticker_items)

cats = {}
for s in S: cats[s['category']] = cats.get(s['category'], 0) + 1
tabs = '    <button class="tab active" data-cat="all">ALL (%d)</button>\n' % len(S) + ''.join('    <button class="tab" data-cat="%s">%s (%d)</button>\n' % (c, c.upper(), n) for c, n in sorted(cats.items()))

trip_src = new[1:4]
trip_h = ['Congress summons Jensen Huang', 'Propaganda trained out of Qwen', 'Benchmarks crack under small changes']
trip_p = ["House chairs want Nvidia's CEO at a closed-door briefing on 18 Nov over a reported Chinese spy plot.",
          "Nous's Arete-27B cuts state-framed answers from 22% to 0.9% with fine-tuning alone.",
          "MaxxBench tweaks DeepSWE tasks and top coding agents spread across 23 points."]
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

  <div class="lead-ref feed-item" data-cat="{lead['category']}"><strong>#1</strong> is today's lead, above: Claude Code's saved approvals leak secrets to GitHub. <a href="#{lead['id']}">Back to top ↑</a></div>

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
    <p><strong>AI Daily Signal</strong> · Edition {ED} · 8 November 2026 (IST) · Curated by Arnav Agrawal<span data-slot="curator-links"></span> · <a href="index.html">All editions</a><span data-slot="sister-links"></span></p>
    <p>Sunday's focus: money, start-ups and new ideas. Today that meant OpenAI's smaller-than-planned round, Anthropic's lower IPO range, Ramp's flat AI-spend data, Physicl's pivot to robot simulation, Google taking over Crusoe's Wyoming site, and a 38M-parameter voice model from Underdog.</p>
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
stories = [sstate(s) for s in S]
tiers = {'critical': 0, 'notable': 0, 'monitor': 0}
for s in S: tiers[s['tier']] += 1

trk = {t['id']: t for t in old['tracking']}
retired, resolved = [], []
def retire(i, reason):
    trk.pop(i); retired.append({'id': i, 'date': DATE, 'reason': reason})
retire('anthropic-cyber-verification-tiers', 'Re-searched Cyber Verification Program and Critical Infrastructure Defense Program: coverage still the 6 Oct three-tier CVP and 8 Oct CIDP launch (11 partners, OSS Scanner); no new tiers, partners or results')
retire('openai-eu-text-watermark', 'Re-searched textGrain EU watermarking: still the 5 Oct announcement ("coming weeks"); no report that the EU rollout finished or of detector access widening')
retire('amd-2027-supply-ramp', "Re-searched AMD 2027 supply and MI500: still Lisa Su's 6 Oct statement with no volume targets; AMD's Q3 results were covered 6 Nov")
retire('claude-startups-program-expansion', 'Re-searched Claude for Startups: still the 6 Oct expansion ($1,000 API credit, a year of Team); one third-party guide says the cohort closed 30 Oct, not confirmed on Anthropic\'s page')
retire('meta-muse-privacy-dossier', "Re-searched Muse dossier: still the TIME report (~6 Oct) and reprints; Meta's 6 Nov Muse Spaces feature (TechCrunch) does not address it")
retire('multiply-labs-robotic-biologics', 'Re-searched Multiply Labs: only the 9 Oct $75M Series B coverage; no deployment or regulatory news')
retire('arxiv-reclaim-diffusion-lm', 'Re-searched RECLAIM: no follow-up, citations or release found; diffusion LMs followed on the diffusion-language-models watchlist entry')
retire('reflection-beam-501b', 'Re-searched Reflection and Beam 501B: still only vendor-reported benchmarks (GLM 5.2 parity at 3-4x less compute); no independent evaluation')
retire('midterm-deepfake-legal-threats', 'Re-searched Colorado deepfake law: no 2026 hearing outcome or enforcement action found; the midterms are over')
trk.pop('musubi-policylm'); resolved.append('Musubi PolicyLM size question settled on re-search: both a 1B (on Baseten) and a 1.7B (Apache 2.0 on Hugging Face) variant exist; no independent benchmarks')
trk['super-intelligence-force'].update(label="Re-checked 8 Nov: the DOJ launched a Super Intelligence Task Force (4-5 Nov, Nextgov, Decrypt), co-led by Stanley Woodward and Stephen Weiss, absorbing the AI Litigation Task Force and acting as DOJ's contact with Jay Clayton's Super Intelligence Force; still no charter action or 120-day report", lastChecked=DATE)
trk.pop('openai-30b-bridge-round', None); trk.pop('openai-eth-kakeya-yang-mills', None)

yl = {
 'claude-dispatch-rce-wontfix': 'MOVED FROM NEW after one edition: The Hacker News (6 Nov) also reports the Claude Dispatch browser-extension flaw; still no Anthropic fix or statement found',
 'inkling-2-small': "MOVED FROM NEW after one edition: Vals AI finds Inkling 2 Small swears in its chain of thought (316 instances across 2,655 runs, mostly two runaway runs); open weights still promised 'next week'",
 'europe-datacentre-protests': "MOVED FROM NEW after one edition: activists breached a Microsoft data-centre construction site in Amsterdam (Tom's Hardware, ET, 6 Nov; not opened); Bloomberg says the backlash is spreading",
 'cert-in-crafty-falcon-ai-attacks': 'MOVED FROM NEW after one edition: Censys finds 800+ exposed Artex deployments, one of the tools CERT-In named (New #5)',
 'google-schools-ai-off': "MOVED FROM DEVELOPING: The Hill and SILive report schools scrambling after Google's ultimatum; parents sue Google over a school Chromebook (Cleveland.com); not opened",
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
 {'dir': 'down', 'text': "ANTHROPIC - Claude Code's 'don't ask again' file leaks 1,379 secrets on public GitHub (lead)"},
 {'dir': 'down', 'text': 'NVIDIA - House chairs summon Jensen Huang to an 18 Nov closed-door briefing over a reported spy plot (#2)'},
 {'dir': 'up', 'text': 'NOUS RESEARCH - Arete-27B strips state framing from Qwen3.8-27B (#3)'},
 {'dir': 'down', 'text': 'DEEPSEEK V4.1 FLASH / GEMINI 3.8 FLASH - fall 18.6-20.5 points on MaxxBench (#4)'},
 {'dir': 'up', 'text': 'OPEN MODELS - DeepSeek V4.1 Flash reaches 72.8% vs 80.8% for gated Daybreak on Vals CyberOffense (#6)'},
 {'dir': 'down', 'text': 'MICROSOFT RESEARCH - AI Frontiers group ends after move into Microsoft AI (#9)'},
 {'dir': 'down', 'text': 'AI SPEND - Ramp: token spend +1.5% over Aug-Sep after +42% in July (#10)'},
 {'dir': 'down', 'text': 'ANTHROPIC IPO - range $1.25-1.75T, below the $2T hoped (D1)'},
 {'dir': 'up', 'text': 'OPENAI - first ~$11B of round wired at $1.25T (D2)'},
 {'dir': 'up', 'text': 'NASDAQ - +1.1% on Friday after Thursday\'s rout (D3)'},
]

heldBack = [
 {'item': 'Firmly raises a $15M Series A backed by J.P. Morgan Payments and Mastercard for AI shopping-agent checkout (Axios Pro, GeekWire)', 'why': 'Only an aggregator summary and a Google News headline; neither article opened', 'next': "Open GeekWire or Firmly's announcement"},
 {'item': "Meta's chief strategy officer Dave Wehner leaves to be CFO of inference start-up Fireworks AI (CNBC)", 'why': 'CNBC article pages return 403; only the headline seen', 'next': 'Check Fireworks or Meta statement'},
 {'item': 'Axon invests up to $1.2B more in Skydio at $5.2B pre-money and becomes its exclusive US/Canada public-safety distributor (Axon 8-K, 5 Nov)', 'why': 'SEC EDGAR returned 403; figures seen only in search snippets of the filing', 'next': 'Open the 8-K exhibit on EDGAR'},
 {'item': 'Nasscom president Rajesh Nambiar warns AI could make it harder for fresh Indian engineering graduates to find jobs, urges CS curriculum overhaul (ET)', 'why': 'Techmeme summary only; ET article not opened; search returned only July coverage', 'next': 'Open the ET article'},
 {'item': "SpaceX building a 'Starbase supercomputer' in Texas per public records (Techmeme)", 'why': 'Source not opened', 'next': 'Open the underlying report'},
 {'item': 'SEA makes up ~50% of APAC data-centre capacity being built; Malaysia paused 49 projects and Thailand delayed 117 approvals in Sept (Techmeme)', 'why': 'Source not opened', 'next': 'Open the report'},
 {'item': 'Ocient raises $100M Series C for agentic AI analytics (SiliconANGLE via Techmeme)', 'why': 'Not opened; data-analytics vendor round, low novelty', 'next': 'None unless product details matter'},
 {'item': "Tesla AI accelerator roadmap with 'SI' branding (Tom's Hardware)", 'why': "Tom's Hardware URL returned 404 from the feed link", 'next': 'Re-open from the site'},
 {'item': 'Weill Cornell says radiology patients\' details were entered into AI tools without authorisation (Medical Daily)', 'why': 'Not opened', 'next': "Open Weill Cornell's notice"},
 {'item': 'Isomorphic Labs in talks to raise ~$5B at ~$50B (Bloomberg, 4 Nov)', 'why': 'Still no company statement or second outlet', 'next': 'Card on a company statement or a second outlet'},
]
noChange = [
 'Inkling 2 Small: open weights still promised "next week"; Vals finds profanity in its chain of thought (The Decoder), no capability change',
 'Tencent Hy4: listed on OpenRouter (4 Nov); Hugging Face weights still not found',
 'Qwen 4: still unreleased; a rumoured 2-8 Nov window passes without an Alibaba post',
 'Crouton Alpha (OpenRouter stealth, 3 Nov): still unnamed; newest OpenRouter listing is LiquidAI LFM3-1.7B incl. a free tier (6 Nov)',
 'Jev / TypeSafe: still the Sept launch and Oct round; no new product or price',
 'Claude Dispatch flaw: now also reported by The Hacker News; no Anthropic response',
 'Ripple-65B Preview and Kimi K3.1 Pro remain on Hugging Face trending; no new releases',
 "India MeitY AI-regulation consultation paper: still not published on its expected date (8 Nov); dropped from the radar until it appears",
]

wl = old['watchlist']
wnotes = {
 'jev-decision-models': ' 8 Nov: re-searched Jev and TypeSafe: still the Sept launch and Oct round; no new decision-model entrant.',
 'stealth-gateway-models': ' 8 Nov: OpenRouter newest listings LiquidAI LFM3-1.7B (+free, 6 Nov) and Gemini Omni 1.2 Flash (5 Nov); Crouton Alpha still unnamed.',
 'qwen4-new-architecture': ' 8 Nov: still unreleased; rumoured 2-8 Nov window passing without an official post.',
 'speech-native-voice-models': ' 8 Nov: CARDED Underdog Woof, 38M-parameter TTS running in the browser (New #11).',
 'hybrid-on-device-moe': ' 8 Nov: LFM3-1.7B now on OpenRouter with a free tier; still trending on Hugging Face.',
 'agent-behaviour-indices': ' 8 Nov: CARDED MaxxBench: coding agents revert to guessed hidden-test behaviour after spec changes (New #4).',
 'activation-probe-monitors': " 8 Nov: Andy Hall's MALT replication: AI auditors catch ~98% of reward hacking at 5% false alarms but over-flag when pushed (New #13).",
 'agent-trace-audit-models': ' 8 Nov: related: AI auditors over-flag at high recall (New #13).',
 'agent-orchestrated-intrusion': ' 8 Nov: CARDED Censys finds 800+ exposed Artex deployments (New #5); Vals: open models near gated ones on autonomous network attacks (New #6).',
 'eval-containment': ' 8 Nov: UK amendment would make loss of control over agents reportable (New #7).',
 'diffusion-language-models': ' 8 Nov: class query found no new diffusion LM release.',
 'jepa-world-models': ' 8 Nov: class query found no new world-model release; Physicl (New #14) sells simulation to world-model builders.',
 'cross-embodiment-world-models': ' 8 Nov: no new release; Physicl raises $10M for robot-training simulation (New #14).',
 'byo-key-theft-distillation': " 8 Nov: related: Claude Code saved-approval file leaks secrets (lead).",
}
for w in wl:
    w['lastChecked'] = DATE
    w['label'] = w['label'] + wnotes.get(w['id'], ' 8 Nov: re-searched in batched class and name queries and the HF/OpenRouter/HN scans; nothing new.')
wl.append({'id': 'value-realignment-finetunes', 'label': "Cheap post-training that changes an open model's political or value framing. 8 Nov: CARDED Nous Arete-27B: SFT-only on Qwen3.8-27B cuts propaganda answers 22% to 0.9% (New #3). Watch for replications, adversarial evals and Chinese-lab responses.",
           'query': 'Arete-27B; Propaganda_Eval; de-censored Qwen; value alignment fine-tune open model; abliterated', 'firstSeen': DATE, 'lastChecked': DATE, 'status': 'carded'})

deadlines = [
 {'date': '2026-11-13', 'label': 'Approximate: Inkling 2 Small open weights ("next week"); Reddit ends RSS; Conductor Cloud goes read-only', 'severity': 'medium'},
 {'date': '2026-11-15', 'label': "China's draft AI export-control catalogue: public comments close (MOFCOM/MOST No. 48)", 'severity': 'high'},
 {'date': '2026-11-16', 'label': "Anthropic watermarks Claude Opus 4.6, Opus 4.5, Sonnet 4.5 and Haiku 4.5; Apple's 18+ descriptors for romantic AI companions become mandatory; California 'kill switch' report", 'severity': 'medium'},
 {'date': '2026-11-18', 'label': 'Jensen Huang asked to a closed-door House briefing on the reported Chinese spy plot (China, Foreign Affairs and Intelligence committees)', 'severity': 'high'},
 {'date': '2026-11-26', 'label': "Approximate: Anthropic aims to list before Thanksgiving; roadshow reported for the week of 9 Nov", 'severity': 'high'},
 {'date': '2026-11-29', 'label': 'OpenAI starts training on Daybreak Blue cybersecurity sessions; check the separate opt-out', 'severity': 'medium'},
]

SOURCES_OPENED = 42
SEARCHES = 29
runNotes = {
 'searches': '29 web searches. Tracking re-checks 10 (Anthropic cyber tiers/CIDP, OpenAI EU watermark, AMD 2027 supply, Musubi PolicyLM, Claude for Startups, Muse dossier, Multiply Labs, RECLAIM, Reflection Beam, Colorado deepfake law). Models and technology 7 (OpenAI ETH disproof, Nous Arete-27B, no-lab-name "new type of AI model", diffusion/SSM/world-model class query, viral X launches and HF clones, Jev/TypeSafe, Qwen 4) plus Underdog Woof. Applied AI and money 6 (OpenAI $11B round, Anthropic IPO, AI startup funding, Firmly, Axon-Skydio, Suno suits). People and policy 6 (DOJ Super Intelligence Task Force, Nasscom fresh graduates, UK/UAE AI jobs, AI CEO voice fraud charges, Anthropic science post). Sunday deep beat (money, start-ups, new ideas) ran through the OpenAI, Anthropic, funding, Firmly, Axon-Skydio searches plus Ramp, Physicl, Crusoe and Underdog. Web search again returned mostly stale results; dated feeds pulled with curl did most of the finding (Techmeme, TechCrunch, The Verge, The Decoder, The Register, Ars Technica, SiliconANGLE, The Hacker News, Economic Times, Google blog, OpenAI RSS, Wired, TNW, Tom\'s Hardware, BBC Business, Guardian Technology, MIT Technology Review, Google News AI query, Anthropic newsroom, METR feed, HN front page, Hugging Face new and trending, OpenRouter models API).',
 'pagesOpened': '42 pages and APIs (not counting ~26 RSS feeds and listing APIs): TechCrunch (8: OpenAI round, Megaspeed, Artex, Underdog, Physicl, Ramp, Crusoe, Muse Spaces), The Verge (2), The Decoder (8: OpenAI round, Anthropic IPO, open/closed cyber gap, AI auditors, Google BP, Arete, Inkling profanity, a listing page), The Register (4: UK agent powers, Bank of England, agent swarms, Fireworks), The Hacker News, Claude Code settings docs, Hugging Face (Arete API and card, Woof API), hunch.net, MaxxBench, WIRED, TNW (4: CEO fraud, Claude Max, AI teddy, ETH), BBC (2), Ars Technica (2), SiliconANGLE (Atomicwork), Anthropic (3: Public Benefit Fund, AI for Science, guest post). Feeds and listing APIs used for finding are not counted.',
 'blocked': 'Apiiro research page 403 (lead counts taken from The Hacker News); openai.com pages 403 (wet-lab agents post); CNBC 403; Techmeme item pages 403 (RSS worked); SEC EDGAR 403 (Axon 8-K); VentureBeat RSS 429; Guardian article served a bot challenge; Tom\'s Hardware feed links 404; GitHub trending not attempted after repeated 403s; Bloomberg, FT, WSJ, NYT and The Information paywalled; Variety/Billboard reachable only as Google News redirects; x.com not attempted',
 'notCovered': 'GitHub trending; live X snapshot; arXiv API not pulled this run (research beat covered via MaxxBench, Vals and the MALT replication); November AI jobs data for India, UK, UAE and EU (searches returned only mid-2026 reports, not carded); OpenAI wet-lab agent evaluation (6 Nov) and Hacktron partnership not opened (403); Anthropic AI for Science expansion and Public Benefit Fund dates unclear (late Oct), not carded; NYC schools/Google ultimatum follow-ups not opened',
 'trackingCleanup': '10 oldest re-checked by name and product: 1 resolved (Musubi size), 9 retired, 0 updated. Also updated: super-intelligence-force (DOJ task force). Two tracked items moved to Developing (OpenAI round, ETH disproof). Previous edition\'s 26 stories: 2 carried as Developing (Anthropic IPO, AI stock rout), 24 joined tracking',
 'corrections': 'None',
}

full = {
 'edition': ED, 'date': DATE, 'tz': 'Asia/Kolkata', 'format': 'v3', 'editionType': 'daily', 'degraded': False, 'degradedReason': '',
 'sourcesOpened': SOURCES_OPENED, 'shareable': False,
 'shareBlockers': ["The lead's counts (1,122 files, 1,379 secrets) come from The Hacker News' account of Apiiro's research; Apiiro's own page returned 403. Only the mechanism was checked on an official page (Anthropic's Claude Code docs)."],
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
desc = "Claude Code's saved approvals leak 1,379 secrets to GitHub. Plus Congress summons Jensen Huang, Nous's Arete-27B, MaxxBench, and OpenAI's and Anthropic's lower valuations."
ogd = 'AI Daily Signal, edition %d (8 Nov 2026): %d new stories, %d developing.' % (ED, len(new), len(dev))
head = re.sub(r'<title>.*?</title>', '<title>AI Daily Signal — Edition %d — 8 November 2026</title>' % ED, head)
head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(desc), head)
for p in ['og:title', 'twitter:title']:
    head = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % p, lambda m: m.group(1) + html.escape(lead['h']), head)
for p in ['og:description', 'twitter:description']:
    head = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % p, lambda m: m.group(1) + html.escape(ogd), head)
head = head.replace('2026-11-06', DATE)
out = head + body + '<script id="page-data" type="application/json">\n' + json.dumps(page, indent=1, ensure_ascii=False) + '\n</script>\n\n' + script
open(OUT, 'w').write(out)
json.dump(full, open('state/signal-state.json', 'w'), indent=1, ensure_ascii=False)
print('new', len(new), 'dev', len(dev), 'tracking', len(tracking), 'tiers', tiers, 'n24', sum(1 for s in new if s['new24h']))
