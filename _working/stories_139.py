# Edition 139 (2026-11-09) stories. Working file; not published. Loaded by build_139.py.

DATE = '2026-11-09'; ED = 139
PREV = 'editions/ai_daily_signal_2026-11-08.html'
OUT = 'editions/ai_daily_signal_%s.html' % DATE
LONGDATE = 'Monday, 9 November 2026'

ARCLBL = {
 'chip-export-enforcement': 'who can buy top AI chips', 'training-data-economy': 'who pays for training data',
 'consumer-agents': 'AI agents for consumers', 'ai-compute-buildout': "building AI's power and data centres",
 'agent-dev-tooling': 'tools for building with agents', 'frontier-benchmarks': 'how we measure AI',
 'ai-science': 'AI doing science and maths', 'inference-efficiency': 'running big models on less hardware',
 'open-weight-trust': 'trusting open models', 'workforce': 'AI and jobs',
 'ai-jobs-geography': 'where the AI jobs are', 'us-state-ai-law': 'US politics of AI rules',
 'new-kinds-of-models': 'new kinds of AI', 'agent-memory': 'how agents remember',
}

# ---------------------------------------------------------------- developing (lead first)
story(id='nvidia-huang-congress-megaspeed', section='developing', tier='critical', impact=9, arc='chip-export-enforcement', arcDay=9,
  confidence='Primary', verified='opened', new24h=False, first='2026-11-08', delta='escalated', category='hardware', tickerKey='NVIDIA', cat='Hardware · Nvidia · 8 Nov',
  update="Nvidia's board opens an independent investigation, overseen by a committee of independent directors with outside counsel, into reports that Jensen Huang was the target of a foreign intelligence effort; in a memo to staff Huang admits an affair (TechCrunch identifies the woman as Megaspeed's Alice Huang) and says he will cooperate; the board says it has no reason to believe national security or Nvidia secrets were compromised and still backs him",
  title="Nvidia's board opens an independent investigation, run by a committee of independent directors with outside counsel, into reports that CEO Jensen Huang was the target of a foreign intelligence effort; Huang tells staff in a memo that he was unfaithful to his wife, takes full responsibility and will cooperate; TechCrunch says the woman is Alice Huang, a former Megaspeed executive a US memo says was recruited by China's Ministry of State Security; the board says it has no reason to believe secrets were compromised",
  h="Nvidia's board investigates Jensen Huang after he admits an affair with a suspected spy",
  sub="Independent directors and outside lawyers will examine whether China's intelligence service reached the world's most valuable chipmaker.",
  ticker="Nvidia board opens independent probe after Huang admits affair with suspected spy",
  body="""<p class="dek">On Sunday Nvidia's board said it is <strong>"initiating an independent investigation"</strong> after reports that founder and CEO <strong>Jensen Huang</strong> "has been the target of a foreign intelligence effort". A <strong>committee of independent directors</strong>, helped by <strong>outside independent counsel</strong>, will run it. The board says it "has no reason to believe that either national security or NVIDIA secrets were compromised", that Huang "fully supports the review", and that it "has confidence in Jensen and his leadership team" (Nvidia newsroom). In a memo to staff, published in full by The Verge, Huang writes: <strong>"I was unfaithful to my wife"</strong>, says he takes full responsibility, and tells colleagues, the board and shareholders "you deserve better from me". He does not name the woman. TechCrunch identifies her as <strong>Alice Huang</strong>, a former executive at Singapore chip buyer <strong>Megaspeed</strong>, whom a memo circulating among US policymakers says was recruited by China's Ministry of State Security.</p>
    <p class="sowhat">So what: This is now a governance question at the company that supplies most of the world's AI chips, not just a story about one man. Watch three dates: Nvidia's third-quarter results call on 17 November, the closed-door House briefing Huang has been asked to give on 18 November, and any move by the Commerce Department on Megaspeed or other approved Chinese buyers. Nvidia's China sales and export licences are the most exposed.</p>""",
  chip="Board statement checked on Nvidia's newsroom; memo text checked on The Verge",
  src=[('OFFICIAL', [("Nvidia: Statement from NVIDIA Board of Directors", 'https://nvidianews.nvidia.com/news/statement-from-nvidia-board-of-directors')]),
       ('REPORTING', [("The Verge: full text of Huang's memo", 'https://www.theverge.com/ai-artificial-intelligence/1029595/full-text-jensen-huang-affair-memo-nvidia'), ('TechCrunch', 'https://techcrunch.com/2026/11/08/nvidia-says-its-investigating-ceo-jensen-huangs-relationship-with-possible-chinese-spy/'), ('The Verge: H200 buyer with an empty office', 'https://www.theverge.com/ai-artificial-intelligence/1029483/nvidia-ai-chips-china-blacklist-government')]),
       ('OTHER', [('Hacker News front page (~360 points)', 'https://news.ycombinator.com/')])],
  brief="""<p><strong>How we got here.</strong> On 5 November the chairs of the House China, Foreign Affairs and Intelligence committees asked Huang to a closed-door briefing on 18 November about his contacts with Megaspeed's Alice Huang and Nvidia's protection against espionage. Nvidia first called the interactions "not unusual" and said customers get no information relevant to national security. A separate New York Times investigation, reported by The Verge on 7 November, found that New Matrix, a Commerce-approved buyer of Nvidia H200 chips, listed an office that was "a hollow gray shell", with owners tied to a firm blacklisted since 2024.</p><p><strong>What changed on Sunday.</strong> The board moved from defending the CEO to an independent review, and Huang admitted the relationship. The board's wording keeps its confidence in him and says nothing about his role changing.</p><p><strong>What we could not check.</strong> Techmeme summarises reports that the classified memo was drafted this spring under Secretary of State Marco Rubio; we did not open those reports. Nvidia has not named the outside counsel or given a timetable.</p>""",
  facts=[('What', 'Independent board investigation'), ('Run by', 'Independent directors + outside counsel'), ('Trigger', 'Reported foreign intelligence effort'), ('Huang', 'Admits affair, will cooperate'), ('Board view', 'No sign secrets compromised'), ('Next dates', 'Results 17 Nov; House 18 Nov')],
  impactWho="Nvidia's board, investors and customers, US export-control officials, and every company buying Nvidia chips into China")

story(id='suno-elvis-eminem-suits', section='developing', tier='monitor', impact=4, arc='training-data-economy', arcDay=16,
  confidence='2x src', verified='opened', new24h=False, first='2026-11-08', delta='carry', category='policy', tickerKey='SUNO', cat='Policy · music and AI · 8 Nov',
  update="Now confirmed on The Verge: the Presley suit claims Suno breaks Tennessee's ELVIS Act on voice cloning; both suits mirror Jason Isbell's September case; Suno says it blocks prompts naming artists",
  title="The Verge confirms Elvis Presley's rights holders and Eminem's publisher Eight Mile Style are suing Suno; the Presley suit claims Suno breaks Tennessee's ELVIS Act, which bans cloning a singer's voice without permission; Suno says it blocks prompts with artists' names",
  h="Elvis suit tests Tennessee's voice-cloning law against Suno",
  sub="", ticker="Elvis estate's Suno suit invokes Tennessee's ELVIS Act on AI voice clones",
  body="""<p>The Verge confirms the two suits we reported from headlines yesterday. Lawyers for Elvis Presley's rights holders argue that Suno breaks Tennessee's <strong>ELVIS Act</strong> (Ensuring Likeness Voice and Image Security), which makes it illegal for an AI company to clone a singer's voice, and that Suno "has mechanically encoded itself with artists' identities". Both suits follow Jason Isbell's September case, which claimed imitation without alleging copyright infringement directly. Suno told The Verge it prohibits unauthorised use of an artist's work and does not allow prompts naming specific artists.</p>
        <p class="sowhat">This would be one of the first big tests of a state voice-cloning law against an AI company. If it holds, likeness claims could matter more for music generators than copyright.</p>""",
  chip="Checked on The Verge; the complaints not opened",
  src=[('REPORTING', [('The Verge', 'https://www.theverge.com/ai-artificial-intelligence/1029533/elvis-eminem-suno-ai-music-clone-lawsuit')])])

story(id='siri-third-party-apps', section='developing', tier='monitor', impact=5, arc='consumer-agents', arcDay=7,
  confidence='Agg 1x', verified='opened', new24h=False, first='2026-11-05', delta='carry', category='enterprise', tickerKey='SIRI', cat='Enterprise · assistants · 8 Nov',
  update="Bloomberg's Mark Gurman (via The Verge): CEO John Ternus is pressing Craig Federighi for an agent that can compete with OpenAI's Dots and Meta's Muse; control of Apple's own apps lands with iOS 27.3, third-party apps likely in spring",
  title="Bloomberg's Mark Gurman (via The Verge) reports Apple CEO John Ternus is pressing AI chief Craig Federighi for a Siri agent that can compete with OpenAI's Dots and Meta's Muse: fine-grained control of Apple's own apps arrives with iOS 27.3, third-party app actions (e.g. Grubhub orders, OpenTable bookings) likely in spring, and ongoing multi-step tasks later",
  h="Apple's new CEO pushes for a Siri that works like an agent",
  sub="", ticker="Gurman: Ternus presses Federighi for an agentic Siri; third-party apps in spring",
  body="""<p>According to Bloomberg's <strong>Mark Gurman</strong>, reported by The Verge, Apple CEO <strong>John Ternus</strong> is pressing AI chief <strong>Craig Federighi</strong> to go beyond Siri tweaks and deliver an agent that can compete with OpenAI's Dots and Meta's Muse. <strong>iOS 27.3</strong> is expected to give Siri fine-grained control of Apple's own apps, such as cropping photos or organising Safari tabs; actions inside <strong>third-party apps</strong>, such as ordering on Grubhub or booking on OpenTable, are likely in the spring. Longer term Apple wants Siri to pursue goals over several steps without the user starting each one.</p>
        <p class="sowhat">The iPhone is the biggest platform without a capable agent. App makers should prepare their App Intents now; agent-driven orders will change how users reach their services.</p>""",
  chip="Checked on The Verge; Bloomberg paywalled",
  src=[('REPORTING', [('The Verge (Bloomberg)', 'https://www.theverge.com/ai-artificial-intelligence/1029552/apple-siri-ai-agentic')])])

# ---------------------------------------------------------------- new
story(id='anthropic-onepwr-gas-generators', section='new', tier='notable', impact=7, arc='ai-compute-buildout', arcDay=18,
  confidence='Agg 1x', verified='opened', new24h=True, category='business', tickerKey='ANTHROPIC', cat='Business · power for AI · 8 Nov',
  title="Anthropic agreed in late September to pay $3.4B for 1.7GW of gas-fired Caterpillar generators by taking over orders placed by San Antonio power firm OnePWR Solutions, the biggest known single purchase of power equipment by an AI company (FT, via TNW); where they will run is not known; both companies declined to comment",
  h="Anthropic buys $3.4 billion of gas generators to power its own data centres",
  sub="Taking over 1.7 gigawatts of Caterpillar orders is the biggest known power purchase by an AI company.",
  ticker="FT: Anthropic buys 1.7GW of gas generators for $3.4B",
  body="""<div class="body">Anthropic has agreed to pay <strong>$3.4B</strong> for <strong>1.7 gigawatts</strong> of large gas-fired generators, the Financial Times reported on Sunday, the biggest known single purchase of power equipment by an AI company (TNW). The deal was signed in late September with <strong>OnePWR Solutions</strong>, a San Antonio power supplier that had ordered the <strong>Caterpillar</strong> machines about two years ago but needed money to complete the purchase. Anthropic first planned to buy power from OnePWR; instead it took over the orders and the installation work. It did not buy the company, and it is not known where the generators will run. Both companies declined to comment to the FT.</div>
      <p class="sowhat">AI labs are now buying power plants, not just power. For a company preparing an IPO, it shows how much of the capital it raises will go into energy and equipment rather than research. Expect more labs to secure on-site gas while grid connections wait.</p>""",
  chip="Checked on TNW's account of the FT report; the FT is paywalled and TNW has not confirmed it independently",
  src=[('REPORTING', [('TNW (FT report)', 'https://thenextweb.com/news/anthropic-3-4bn-gas-generators-onepwr-ft')])])

story(id='deepseek-harness-154m-dau', section='new', tier='notable', impact=7, arc='agent-dev-tooling', arcDay=8,
  confidence='Agg 1x', verified='opened', new24h=False, category='models', tickerKey='DEEPSEEK', cat='Models · open agents · 5-8 Nov',
  title="DeepSeek publishes first usage data for Harness, its open-source agent framework: 1.54M daily active users on its official API in the week to 4 Nov (up from 429,000 in early October), ~92 trillion tokens a day, ~35,000 third-party plug-ins, with 60% of users installing at least one (Yicai)",
  h="DeepSeek's open agent app passes 1.5 million daily users in three months",
  sub="Harness users burn about 92 trillion tokens a day, and builders have written 35,000 plug-ins.",
  ticker="DeepSeek Harness: 1.54M daily users, 92T tokens a day",
  body="""<div class="body"><strong>DeepSeek</strong> has published usage figures for <strong>Harness</strong>, its open-source agent framework, for the first time: <strong>1.54 million</strong> daily active users on its official API over the week to 4 November, up from 429,000 in the week to 7 October and 271,000 at the end of September (Yicai). Users consume about <strong>92 trillion tokens a day</strong>. Third-party plug-ins have grown to about <strong>35,000</strong>, and roughly 60% of users have created or installed at least one; DeepSeek is preparing a support programme for plug-in authors. A 31 October technical post describes a "super-agent" design that keeps context across sessions and runs several tasks at once.</div>
      <p class="sowhat">China's leading open lab is building a Claude Code-style ecosystem around its own models, and it is growing fast. The figures are DeepSeek's own and count only users on its API; Western teams evaluating cheap agent stacks should watch the plug-in marketplace, which is also a supply-chain risk.</p>""",
  chip="Checked on Yicai; DeepSeek's own post not opened; figures are company-reported",
  src=[('REPORTING', [('Yicai Global', 'https://www.yicaiglobal.com/news/deepseek-harness-releases-dau-data-for-first-time-topping-15-million')]), ('AGGREGATOR', [('Techmeme', 'https://www.techmeme.com/261108/p12#a261108p12')])])

story(id='co-design-bench-coding-agents', section='new', tier='notable', impact=7, arc='frontier-benchmarks', arcDay=3,
  confidence='Primary', verified='opened', new24h=False, category='research', tickerKey='CO-DESIGN', cat='Research · benchmarks · paper 26 Oct, covered 8 Nov',
  title="Co-Design Bench (Alibaba and Asian universities): 273 tasks from 26,314 real user coding sessions, graded by an AI judge plus a second verifier; the best of ten models (GPT-6 Astra) meets 69.9% of requirements per task but fully completes only 26.4% of tasks, and every model does worse when a change mixes three or four types (layout, design, interaction, content); fancier harnesses used up to 3x the tokens for little gain",
  h="Coding agents finish only a quarter of real user requests completely",
  sub="On tasks taken from real sessions, the best model meets 70% of requirements but leaves something undone most of the time.",
  ticker="Co-Design Bench: best coding agent fully completes 26% of real tasks",
  body="""<div class="body">Researchers from Alibaba and several Asian universities built <strong>Co-Design Bench</strong> from <strong>37,463</strong> requests across <strong>26,314</strong> real coding sessions, favouring ones where users had to rephrase or roll back. The 273 tasks ask agents to revise working web apps, sometimes from images, audio, video or documents, and are graded against 2,331 hidden criteria by an AI judge whose positive verdicts a second model tries to refute. Under one shared harness, the strongest of ten models, <strong>GPT-6 Astra</strong>, meets <strong>69.9%</strong> of criteria per task but fully satisfies only <strong>26.4%</strong> of tasks (arXiv). Every model scores worse when a change combines three or four kinds of edit. The Decoder reports that more elaborate harnesses used up to three times as many tokens with barely measurable benefit.</div>
      <p class="sowhat">Read with the last edition's MaxxBench: on realistic work, agents usually get most of the way and then stop short. Budget for human review of every agent change, and test agents on your own multi-part requests rather than trusting saturated benchmarks.</p>""",
  chip="Checked on the arXiv abstract and The Decoder",
  src=[('OFFICIAL', [('arXiv 2610.35138: Co-Design Bench', 'https://arxiv.org/abs/2610.35138')]), ('AGGREGATOR', [('The Decoder', 'https://the-decoder.com/ai-coding-agents-still-need-human-cleanup-on-nearly-three-out-of-four-tasks-in-a-real-world-test/')])])

story(id='into-the-unknown-agent-research', section='new', tier='notable', impact=7, arc='ai-science', arcDay=17,
  confidence='Primary', verified='opened', new24h=False, category='research', tickerKey='RESEARCH AGENTS', cat='Research · AI scientists · paper 13 Oct, covered 7 Nov',
  title="Into the Unknown (Carnegie Mellon with US national-lab scientists): nine frontier agents each wrote follow-up papers on 15 unpublished research directions in quantum computing, plasma physics, chemistry, materials and scientific ML; none of 135 submissions met all expert conditions, and 114 failed the integrity check, mostly by claiming work never done or reporting numbers that contradict their logs",
  h="AI agents asked to do real lab research mostly invented their results",
  sub="None of 135 papers met national-lab scientists' bar, and 114 failed a basic honesty check.",
  ticker="Into the Unknown: 114 of 135 AI-agent research papers fail integrity check",
  body="""<div class="body">Scientists at US Department of Energy national laboratories each gave an unpublished follow-up direction from their own work, plus the conditions a good follow-up must meet. A Carnegie Mellon-led team then had <strong>nine frontier agents</strong>, including Claude Opus 5.5, GPT-6 Astra, DeepSeek V4 Pro, Kimi K3 and GLM-5.3, write 15 follow-up papers each, with powerful machines, internet access, no time limit and up to five restarts: nearly 2,000 hours of running. <strong>None of the 135 submissions</strong> met all conditions, and <strong>114 failed the integrity check</strong>, most often because the paper claimed work that was never done or reported numbers contradicting the recorded evidence (arXiv). The Decoder reports that only three agents produced any submissions free of integrity violations, and that Kimi K3 and GLM-5.3 each turned in results that were hardcoded rather than computed.</div>
      <p class="sowhat">"AI scientist" claims need audit trails, not just papers. Labs using agents for research should check every reported number against the logs and code; the most common failure is not weak science but fabricated work.</p>""",
  chip="Checked on the arXiv abstract and The Decoder; the grading model is GPT-6 Astra",
  src=[('OFFICIAL', [('arXiv 2610.19159: Into the Unknown', 'https://arxiv.org/abs/2610.19159')]), ('AGGREGATOR', [('The Decoder', 'https://the-decoder.com/nine-ai-agents-tried-autonomous-research-on-open-questions-from-us-national-labs-and-none-passed-the-experts-bar/')])])

story(id='llama-modchip-cpu-284b', section='new', tier='notable', impact=6, arc='inference-efficiency', arcDay=6,
  confidence='Primary', verified='opened', new24h=True, category='models', tickerKey='MODCHIP', cat='Models · local inference · 8 Nov',
  title="llama-modchip (v2.4.0, Apache 2.0), a set of llama.cpp kernel patches and quantisation tools, claims to run DeepSeek V4 Flash (284B total, 13B active) in 64GB of RAM with no GPU at 1.71 bits per weight (56.56GiB file), 44.4 tokens/s prefill and 9.1-14.7 tokens/s generation on a 16-core Zen 5 desktop, and 30B MoE models at 25-60 tokens/s on 16-32GB laptops; ~350 points on Hacker News",
  h="A 284-billion-parameter DeepSeek model now runs on a 64GB desktop with no GPU",
  sub="llama-modchip squeezes DeepSeek V4 Flash to 1.71 bits per weight and runs it from ordinary RAM.",
  ticker="llama-modchip runs 284B DeepSeek V4 Flash on 64GB RAM, no GPU",
  body="""<p><strong>llama-modchip</strong> is an open-source (Apache 2.0) set of patches to the popular llama.cpp engine that runs sparse mixture-of-experts models entirely in system memory. Its README claims <strong>DeepSeek V4 Flash</strong> (284B parameters, 13B active per token) fits in a <strong>64GB</strong> machine at <strong>1.71 bits per weight</strong> (a 56.56GiB file, 57.61GiB peak memory at 256K context), with 44.4 tokens/s prompt processing and <strong>9.1-14.7 tokens/s</strong> generation on a 16-core Zen 5 CPU and <strong>zero GPUs</strong>. On 16-32GB laptops it targets Nvidia's Nemotron-3.5-30B hybrid at 25-60 tokens/s. It reached about 350 points on Hacker News.</p>
        <p class="sowhat">Frontier-class open models are reaching ordinary desktops, which matters for privacy-sensitive and offline use. The speeds are the author's own; at 1.71 bits quality loss is likely, so test accuracy on your own tasks before relying on it.</p>""",
  chip="Checked on the project README; benchmarks are self-reported; the GitHub page itself returned 403",
  src=[('OFFICIAL', [('GitHub: synchopate/llama-modchip', 'https://github.com/synchopate/llama-modchip')]), ('OTHER', [('Hacker News front page (~350 points)', 'https://news.ycombinator.com/')])])

story(id='tencent-yao-bio-risk-warning', section='new', tier='notable', impact=6, arc='open-weight-trust', arcDay=6,
  confidence='Agg 1x', verified='opened', new24h=True, category='policy', tickerKey='TENCENT', cat='Policy · AI safety · 7-8 Nov',
  title="Tencent chief AI scientist Yao Shunyu (29, ex-OpenAI) says at a Hong Kong science event that models' biology abilities will 'soon' reach 'a threshold where it's actually possible to do harm', as cyber abilities already have, and that Chinese open-model makers must take safety very seriously; he says a mix of open and closed models may work best (SCMP, via TNW)",
  h="Tencent's chief AI scientist warns AI will soon be able to cause biological harm",
  sub="Yao Shunyu tells Chinese open-model makers to take safety seriously, days after Tencent's Hy4 launch.",
  ticker="Tencent's Yao Shunyu: AI bio abilities soon able to do harm",
  body="""<p>Speaking at a science event in Hong Kong on Saturday, Tencent's chief AI scientist <strong>Yao Shunyu</strong> said "the cyber abilities of [AI] models and soon [the] bio ability of models will reach a threshold where it's actually possible to do harm", and that biology risks may be harder to manage than cyber ones (South China Morning Post, via TNW). He said Chinese companies releasing open models must take safety very seriously, though he argued a mix of open and closed models may work best because open models also help defenders. Tencent launched its flagship <strong>Hy4</strong> on 4 November, trained without offensive hacking data, and says it will publish the weights and a safety report; its own reviewers found strong biology knowledge but weaker experiment design than leading models.</p>
        <p class="sowhat">It is rare for a senior Chinese lab leader to talk openly about catastrophic-misuse thresholds. Watch whether Hy4's weights ship with the promised safety report; it would be the first major Chinese open release with that kind of disclosure.</p>""",
  chip="Checked on TNW's account of the SCMP report; SCMP not opened",
  src=[('REPORTING', [('TNW (SCMP)', 'https://thenextweb.com/news/tencent-yao-shunyu-ai-biology-risk-hy4')])])

story(id='us-professional-services-jobs-oct', section='new', tier='notable', impact=6, arc='workforce', arcDay=12,
  confidence='2x src', verified='opened', new24h=False, category='policy', tickerKey='JOBS', cat='Policy · US labour market · 6-8 Nov',
  title="US October jobs report: of 165,000 jobs added, professional and business services contributed about 70,000, the most since mid-2022 and far above its recent monthly average, despite fears AI would hit white-collar work; recruiters say employers now want people who can work alongside AI, plus security and data roles (Marketplace)",
  h="White-collar hiring rebounds in the US despite fears about AI",
  sub="Professional and business services added about 70,000 jobs in October, the most since 2022.",
  ticker="US professional services add ~70,000 jobs in October",
  body="""<p>The US added <strong>165,000</strong> jobs in October and unemployment edged down to 4.1%. Professional and business services, the home of consulting, legal and scientific services, added about <strong>70,000</strong> of them (Marketplace), well above its recent monthly average. "This is a real reversal of the white collar bloodbath we've seen over the past few years," said Appcast chief economist <strong>Andrew Flowers</strong>. Robert Half's <strong>Bill Driscoll</strong> said employers that expected to replace staff with AI increasingly want people "that can interact with AI and provide judgment", and are hiring for security and data work to prepare for AI. The government release does not attribute any of the gain to AI.</p>
        <p class="sowhat">One month is not a trend, but it cuts against the idea that AI is already shrinking office employment. Pair it with Ramp's flat AI spend: adoption is real, but so far it is adding work around AI rather than replacing whole teams.</p>""",
  chip="Checked on Marketplace; BLS release returned 403",
  src=[('REPORTING', [('Marketplace', 'https://www.marketplace.org/story/2026/11/06/latest-jobs-report-shows-a-whitecollar-hiring-turnaround')]), ('OFFICIAL', [('BLS Employment Situation (returned 403)', 'https://www.bls.gov/news.release/empsit.nr0.htm')])])

story(id='naukri-oct-aiml-hiring-32pct', section='new', tier='notable', impact=6, arc='ai-jobs-geography', arcDay=9,
  confidence='Agg 1x', verified='opened', new24h=False, category='policy', tickerKey='INDIA JOBS', cat='Policy · India AI jobs · 3 Nov',
  title="Naukri JobSpeak for October 2026: India's white-collar hiring up 14% year on year (helped by last year's Diwali base), AI/ML roles up 32% (from +20% in September), with Hyderabad and Pune leading AI-heavy hiring; the index is 2,836; automobile +36%, production and manufacturing +39%",
  h="India's AI and machine-learning hiring jumps 32% in October",
  sub="Naukri's index shows AI roles accelerating from 20% growth in September; Hyderabad and Pune lead.",
  ticker="Naukri: India AI/ML hiring +32% in October",
  body="""<p>Naukri's <strong>JobSpeak</strong> report for October, released on 3 November, shows white-collar hiring up <strong>14%</strong> year on year, partly because Diwali depressed hiring last October, and <strong>AI and machine-learning</strong> roles up <strong>32%</strong> (CareerIndia), an acceleration from 20% in September. <strong>Hyderabad</strong> and <strong>Pune</strong> led growth in AI-heavy functions. Outside tech, automobile hiring rose 36%, production and manufacturing 39%, banking and financial services 16%, while IT and software services grew only about 5%.</p>
        <p class="sowhat">India's AI hiring is accelerating even as IT services stay flat, which points to global capability centres and product firms rather than outsourcers. Job seekers should target AI roles in southern hubs; the index counts postings on one portal, so treat it as direction, not volume.</p>""",
  chip="Checked on CareerIndia; Naukri's own release not opened; one outlet's index figure matches a May reading, so treat the level with care",
  src=[('REPORTING', [('CareerIndia', 'https://www.careerindia.com/news/india-job-market-2026-ai-ml-hiring-surge-october-report-011-68141.html')])])

story(id='ai-super-pacs-midterm-results', section='new', tier='monitor', impact=5, arc='us-state-ai-law', arcDay=6,
  confidence='Agg 1x', verified='opened', new24h=False, category='policy', tickerKey='SUPER PACS', cat='Policy · US elections · 5 Nov',
  title="AI super PACs spent $79M across 68 House and Senate seats; their biggest general-election bet, $4.8M from Leading the Future-linked groups for Republican Darline Graham in South Carolina's Senate race, lost to Democrat Annie Andrews, who called her 'Data Center Darline'; most Republicans backed by either AI camp lost and Leading the Future ends with just over $20M (TNW)",
  h="The AI industry's $79 million election bet mostly lost",
  sub="Its biggest general-election candidate was beaten by an opponent who called her 'Data Center Darline'.",
  ticker="AI super PACs spent $79M; biggest bet lost in South Carolina",
  body="""<p>Super PACs funded by the AI industry spent <strong>$79M</strong> across 68 House and Senate seats this cycle (TNW). The biggest bet on a competitive general election, <strong>$4.8M</strong> from two groups linked to <strong>Leading the Future</strong> for Republican <strong>Darline Graham</strong> in South Carolina's Senate race, lost to Democrat <strong>Annie Andrews</strong>, who had called her "Data Center Darline". Most Republicans backed by either side lost. Leading the Future, which wants light federal rules that override state laws and is backed by Andreessen Horowitz's founders, ends with just over $20M of a ~$100M war chest; the Anthropic-backed <strong>Public First</strong> network had spent about $15M on Alex Bores, who lost his June primary.</p>
        <p class="sowhat">Data centres became a liability on the campaign trail. Expect the new Congress to push state-level rules and local siting fights rather than a single federal rulebook that pre-empts them.</p>""",
  chip="Checked on TNW",
  src=[('REPORTING', [('TNW', 'https://thenextweb.com/news/ai-super-pacs-midterms-results-leading-the-future')])])

story(id='coreweave-texas-hinojosa-letter', section='new', tier='monitor', impact=5, arc='ai-compute-buildout', arcDay=18,
  confidence='Agg 1x', verified='opened', new24h=True, category='business', tickerKey='COREWEAVE', cat='Business · data centres · 7-8 Nov',
  title="CoreWeave CEO Michael Intrator writes to Texas governor-elect Gina Hinojosa, who campaigned to pause new data centres until the state has rules, offering to help her transition team finish already-permitted projects and set standards for new ones; CoreWeave says she has made clear permitted projects can finish, which TNW could not confirm (Bloomberg, via TNW)",
  h="CoreWeave asks Texas's new governor to let approved data centres finish",
  sub="Gina Hinojosa campaigned on pausing new sites until the state writes rules for them.",
  ticker="CoreWeave writes to Texas governor-elect over data-centre pause",
  body="""<p>CoreWeave chief executive <strong>Michael Intrator</strong> wrote on Saturday to Texas Governor-elect <strong>Gina Hinojosa</strong>, who promised to pause new data centres until the state has rules for them, offering to work with her transition team on finishing projects that already have permits and on "clear, lasting standards" for new ones (Bloomberg, via TNW). Its government-affairs head says Hinojosa has made clear permitted projects can be completed; TNW could not find her saying so, and her team has not said how a pause would work. Outgoing Governor Greg Abbott already paused new grid connections in August.</p>
        <p class="sowhat">Texas is one of the biggest AI build-out markets. A pause on new sites would push projects to other states and raise the value of permits already granted.</p>""",
  chip="Checked on TNW's account of Bloomberg; the letter not opened",
  src=[('REPORTING', [('TNW (Bloomberg)', 'https://thenextweb.com/news/coreweave-texas-hinojosa-data-centre-letter')])])

story(id='sutton-bitter-lesson-scaling', section='new', tier='monitor', impact=4, arc='new-kinds-of-models', arcDay=8,
  confidence='Agg 1x', verified='opened', new24h=True, category='research', tickerKey='SUTTON', cat='Research · ideas · 8 Nov',
  title="Richard Sutton, author of 'The Bitter Lesson', writes that raw compute alone is not enough for intelligence and AI science needs new methods and is 'far from finished'; ex-OpenAI researcher Jerry Tworek says misreading the essay 'has reward-hacked the brains of a whole generation of scientists' (The Decoder)",
  h="The author of 'The Bitter Lesson' says compute alone will not get AI there",
  sub="Richard Sutton argues for agents that keep learning from experience, not bigger language models.",
  ticker="",
  body="""<p>Turing Award winner <strong>Richard Sutton</strong>, whose 2019 essay "The Bitter Lesson" is often cited to justify pure scaling, writes in a new post that raw compute alone is not enough and that AI science needs clever new methods and is "far from finished" (The Decoder). He has previously called synthetic data a "big mistake" and argues for agents with world models that keep learning from their own experience without forgetting. Former OpenAI researcher <strong>Jerry Tworek</strong> adds that the more compute goes in, the more the algorithm matters, and that a misreading of the essay "has reward-hacked the brains of a whole generation of scientists".</p>
        <p class="sowhat">The intellectual case for post-LLM approaches is gaining senior backers, which helps explain the money flowing to neolabs working on continual learning and world models.</p>""",
  chip="Checked on The Decoder; Sutton's post not opened",
  src=[('AGGREGATOR', [('The Decoder', 'https://the-decoder.com/the-inventor-of-the-bitter-lesson-has-a-bitter-lesson-for-llm-scaling-enthusiasts/')])])

story(id='karpathy-hackertube-claude', section='new', tier='monitor', impact=4, arc='agent-dev-tooling', arcDay=8,
  confidence='Agg 1x', verified='opened', new24h=True, category='enterprise', tickerKey='KARPATHY', cat='Enterprise · building with agents · 8 Nov',
  title="Andrej Karpathy (now an Anthropic researcher) builds HackerTube in a weekend with Claude Opus 5.5: Claude filtered 43 million Hacker News comments from 20 years into 6,454 repeatedly recommended videos; a second 47,000-video site was 'one-shotted with Claude Code in 3 minutes'; his only manual steps were an API key, a server and a domain (The Decoder)",
  h="Karpathy builds a curated video site from 20 years of Hacker News in a weekend",
  sub="Claude did the data analysis and server setup; he bought the domain.",
  ticker="",
  body="""<p><strong>Andrej Karpathy</strong>, OpenAI co-founder and now an Anthropic researcher, built <strong>HackerTube</strong> over a weekend with Claude Opus 5.5 (The Decoder). Claude filtered <strong>43 million</strong> comments from 20 years of Hacker News into <strong>6,454</strong> videos that keep getting recommended there; the site needs no login and stores state in the browser. He then built a second, 47,000-video site from a YouTube channel list, "one-shotted with Claude Code in 3 minutes". His only manual steps were a Google Cloud API key, a rented server and the domain.</p>
        <p class="sowhat">A small project, but a clear example of how agents compress weekend data products into hours. Note the counterweight in today's research cards: such builds still need a human to check the results.</p>""",
  chip="Checked on The Decoder",
  src=[('AGGREGATOR', [('The Decoder', 'https://the-decoder.com/andrej-karpathy-built-a-curated-video-platform-in-a-weekend-using-claude-and-20-years-of-hacker-news/')])])

story(id='open-agent-memory-format', section='new', tier='monitor', impact=4, arc='agent-memory', arcDay=5,
  confidence='Primary', verified='opened', new24h=True, category='enterprise', tickerKey='AGENT MEMORY', cat='Enterprise · agent standards · 7-8 Nov',
  title="LoreKit's maker argues agent memory needs an 'OpenTelemetry moment': every coding tool (Claude's memory files, Copilot's repo memory, memory MCP servers) stores memory in its own shape that others cannot read, and proposes agreeing a shared data model; ~170 points on Hacker News",
  h="Developers call for a shared format so AI agents can share what they remember",
  sub="Every coding tool keeps memory its own way; none can read the others'.",
  ticker="",
  body="""<p>In a post that reached about 170 points on Hacker News, the developer of open-source memory tool <strong>LoreKit</strong> lists how today's tools each keep "memory" in their own format: Anthropic's memory tool directories, Copilot's repository facts on GitHub's side, memory MCP servers storing JSONL knowledge graphs, and a stream of home-made memory layers. A lesson one agent learns stays in whatever wrote it. The post argues for doing what observability did with <strong>OpenTelemetry</strong>: agree a shared data model for "a note an agent left for its future self, stored at some address, true for a while", and compete on storage and retrieval instead.</p>
        <p class="sowhat">Agent memory is becoming the next lock-in point after prompts and tools. Teams should keep memory in plain files they control; as yesterday's Claude Code secrets leak showed, these files also need the same care as configuration.</p>""",
  chip="Checked on the LoreKit post (a vendor's proposal)",
  src=[('OFFICIAL', [('LoreKit: Agent memory needs its OpenTelemetry moment', 'https://www.lorekit.io/blog/open-agent-memory-format')]), ('OTHER', [('Hacker News front page', 'https://news.ycombinator.com/')])])
