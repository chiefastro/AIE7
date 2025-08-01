# Mental Models for the Intelligence Age - Skillenai

The world is transitioning from the Information Age to the Intelligence Age. We need a new set of mental models to thrive in this new age. Below are a few of the mental models I’ve adopted recently to help guide my work as an AI engineer.


## Engine in a Buggy

> Don’t put an engine in a buggy designed for a horse. Design a new car for the engine.
> 
> Jared Rand

Businesses built before the emergence of LLMs are buggies powered by horses. Business leaders can try to replace the horses with AI, but they will quickly find that they need to redesign the buggy into an automobile.

Maybe you’ve seen this at your company – complex manual processes alongside complex user interfaces alongside complex relational databases… It’s tempting to look at a single step in that complex web and say “hey, we could automate that step with AI!” But doing so misses the forest for the trees. It is cheaper and faster to redesign the entire workflow and rebuild from scratch in an AI-native way.

## Principles of Ideation

Let’s think about ideation from first principles. Where do good ideas come from, and why do people share them?

  * **Meritocracy of ideas** – good ideas can come from anyone
  * **Wisdom of the crowd** – good ideas are rare and require casting a wide net to find
  * **Collisions spark insight** – good ideas are often mergers of two or more concepts that are trivial on their own
  * **Velocity of validation** – the faster you test ideas, the more good ideas you discover
  * **Failure as progress** – failure is success when it narrows the search space
  * **Glory of eureka** – good ideas feel good to discover
  * **Intellectual safety** – ideas are shared when it is psychologically safe to do so
  * **Bias to accept** – ideas are shared when they are likely to be accepted
  * **Bias to action** – ideas are shared when they are likely to be acted on



How many of these principles align with your personal values? What about with your company’s culture?

## R&D as Search

> R&D is a search problem. R&D teams are responsible for exploring and exploiting the search space of profitable solutions to customer needs.
> 
> Jared Rand

I’ve asked AI to help map algorithmic search theory to business tactics:

_Every innovation culture must balance exploration (sampling unfamiliar regions of the state-space) with exploitation (doubling-down on what already works). Demis Hassabis, whose teams turned Monte-Carlo Tree Search and reinforcement learning into AlphaGo and AlphaFold, frames the tension bluntly:_

> _“The exploitation–exploration problem is the crux of AI and of running an R & D organisation… We run a loose **70-20-10 portfolio** : 70 % on core bets, 20 % on adjacent ideas, 10 % on wild, orthogonal experiments.” _
> 
> [Demis Hassabis](https://hbr.org/podcast/2023/05/azeems-picks-demis-hassabis-on-deepminds-journey-from-games-to-fundamental-science)

_Algorithmic search theory (multi-armed bandits, UCB, Bayesian optimisation) shows that shortening evaluation cycles and widening information flow raise the effective learning rate. Below, each cultural tactic maps to a concrete search-algorithm idea that speeds learning while keeping risk bounded._

**Search principle**| **Cultural tactic**| **What it does & why it works**  
---|---|---  
**Wide random playouts**  
Monte-Carlo rollouts sample unexpected branches.| **Company-wide hackathons** (Microsoft’s 70 k-person event; Pinterest’s “Makeathon”) | Generates many low-cost probes of distant solution space; the few high-value “Move 37s” drive returns.  
**High-bandwidth reward signal**  
RL agents learn fastest when reward comes quickly.| **Dedicated Discord / Slack communities that mix customers with builders** | Converts real-time user chatter into near-instant reward/penalty signals, collapsing cycle time from quarters to hours.  
**Upper-Confidence Bound (UCB)**  
Favour actions with high mean _and_ high uncertainty.| **70-20-10 resourcing rule** (Hassabis) | Guarantees constant budget for “high-uncertainty, high-potential” bets while sustaining the core.  
**Evolutionary mutation & crossover**  
Generate variants, keep the fittest.| **Build-in-public transparency** and open design logs | External contributors suggest small “mutations”; social proof surfaces the fittest ideas.  
**Rapid rollout / back-prop**  
Short step-size = faster convergence.| **Vibe-coding & no-code rapid prototyping** (Replit, Vercel v0) | Non-technical staff ship testable artifacts in hours, shrinking the explore→measure→learn loop.  
**Stochastic gradient descent**  
Take many tiny updates instead of rare big ones.| **Kaizen & Toyota Way continuous improvement** | Front-line teams ship micro-optimisations daily; variance averages out, trend points forward.  
**Distributed sensing**  
Bandit algorithms need many arms.| **Idea-Driven Organization** — frontline suggestion systems | Every employee becomes a sampling arm; aggregate ideas reveal gradients undetectable from the C-suite.  
**Credit assignment**  
Reinforce behaviours that improved reward.| **Explicit ownership of outcomes** | Teams that see the scoreboard (KPIs, OKRs) learn which behaviours raise reward and iterate faster.  
**Avoid long, open-loop simulations**| **Lean-Startup “build-measure-learn” over 12-month plans** | Frequent checkpoints keep the value function up-to-date and prevent runaway wasted compute (budget).  
**Low‐latency observation noise control**| **Scrum sprints & short feedback loops** | Tight iterations dampen noise, enabling finer gradient steps and surer convergence.  
  
**Putting it to work**

  1. _**Audit your portfolio.** Classify spend into explore / exploit buckets; re-balance toward a 70-20-10 (or 60-30-10) mix._
  2. _**Instrument the loop.** For each tactic, define a quantifiable reward (e.g., time-to-prototype, idea-to-production throughput)._
  3. _**Lower activation energy.** Provide no-code tools, protected hackathon time, and persistent community channels so anyone can “pull the bandit arm.”_
  4. _**Broadcast learning.** Ship demo videos, internal podcasts, or discord AMAs after every sprint so knowledge diffuses like back-prop updates across the org._
  5. _**Reward novelty × impact.** Use a simple 2-D matrix: business value vs. novelty. Celebrate the upper-right quadrant publicly._



**Why it matters**

_Search theory tells us that the faster an organisation can cycle through hypothesis-generation, real-world testing, and reward propagation, the steeper its learning curve. Embedding these tactics turns your company into a live reinforcement-learning system — one whose**global optimum is ever-moving customer value** , and whose search policy gets smarter every day._

## Avoid the AI Steamroller

> Treat frontier models like rapidly-improving public infrastructure—great to ride on, fatal to stand under. Build the parts of the value chain that infrastructure can’t, or won’t, absorb.
> 
> o3

What this means in July 2025 is this: avoid chat interfaces within your web app. Frontier labs are now shipping AI-native browsers (like Comet from Perplexity) and agents that can use browsers (like OpenAI’s ChatGPT Agent). With browser agents, users will have a chat interface built into their browser, so you don’t need to build one in your app. And their browser agent can operate across multiple tabs of the browser, which your in-app chat interface can never do. 

The play becomes building MCP tools that connect your data to those browser agents, or creating custom web pages meant to be accessed by an agent instead of a human. And building browser extensions that can solve vertical workflows across multiple apps may be another path forward for AI builders.

But let’s zoom out a bit on this concept of avoiding the AI steamroller. Here’s AI’s take on it:

_Sam Altman’s blunt warning to founders—“we’re going to steam-roll you” if your product is just a thin wrapper on today’s GPT-4-style APIs—captures the new platform risk of the intelligence age . In the same spirit that Apple sherlocked single-feature iOS apps and Google subsumed SEO point-solutions, the frontier-model labs (OpenAI, Anthropic, Google, Meta, Microsoft, et al.) will keep folding the “obvious” point features into ever-more capable base models._

_**The lesson:** if your value proposition disappears the moment GPT-5 ships, you’re standing on the tracks._

**_Where the steamroller can’t reach — nine strategic “safe-zones”_**

**Safe-zone**| **Why it resists commoditisation**| **Practical moves & examples**  
---|---|---  
**Proprietary or hard-to-get data**|  Foundational models train on public corpora; your private telemetry, labelled edge-data or regulated records stay out of reach.| Build data-network effects (usage ⇒ new data ⇒ better model). Venture VCs now rank “unique data” the strongest moat for Gen-AI startups .  
**Deep domain expertise**|  Frontier labs optimise for _general_ intelligence; niche science, legal or biotech workflows need domain context humans spent years acquiring.| Anthropic’s Mike Krieger points to specialised verticals—“I don’t see us solving lab-automation any time soon” . Hire/prioritise operators who lived the pain.  
**Workflow lock-in & systems-of-record**| If you own the daily operating system (docs, tickets, supply-chain, EMR), models become replaceable modules behind the scenes.| Move “up-stack” from insight → action → transaction; integrate approvals, compliance, billing.  
**Real-time or edge context**|  Latency, privacy or offline constraints force local inference or hybrid architectures Big Tech won’t customise.| Combine on-device small models with cloud LLM calls; add physical sensors or custom hardware.  
**Regulatory & compliance shields**| Heavily regulated verticals (health, finance, defense) impose certifications cloud labs won’t chase.| Secure SOC-2/ISO, embed audit trails, offer private-cloud or on-prem fine-tuning.  
**Human-in-the-loop services**|  Models supply 80 % of the answer; you monetise the last-mile QA, curation, relationship, liability.| Examples: AI-augmented legal review, clinical scribing with licensed physicians, AI plus expert forums.  
**New interfaces & UX innovation**| Labs expose APIs, not magical product experiences. Unconventional interfaces can become defensible habits.| Krieger urges “weird, power-user” UI bets that mature into mass adoption —think Figma’s multiplayer canvas or Midjourney’s Discord chat.  
**Distribution & community moats**| An owned audience or network effect survives model competition.| Build ecosystems (plugins, marketplaces), cultivate creator communities, embed in incumbents’ workflows.  
**Orchestration across many models**|  As open-source accelerates, enterprises will need routers, guardrails and cost/performance tuning.| Provide LLMOps, policy engines, retrieval pipelines, heterogeneous agent frameworks.  
  
**_Tactics for builders today_**

  1. _**Design for step-function upgrades.** Assume GPT-6/7 will trivialise today’s “wow” features. Architect your product so each model leap improves unit economics rather than nukes your margin._
  2. _**Own the feedback loop.** Capture proprietary usage data the big labs can’t see—then fine-tune small internal models or retrieval pipelines on it._
  3. _**Marry atoms & bits.** Edge devices, proprietary sensors, robotics or custom silicon create hardware switching-costs the cloud giants won’t replicate quickly._
  4. _**Compete on trust.** Compliance guarantees, white-box explanations and liability coverage beat a generic API reply when careers (or patient lives) are at stake._
  5. _**Invest in community as distribution.** A loyal Discord, Slack or LinkedIn following that loves your workflow is harder to “sherlock” than a prompt template. The moment OpenAI adds your feature, the community should still pick you for support, templates and social capital ._
  6. _**Partner, don’t fight, on commodities.** Let frontier labs pay the GPU bill; differentiate on vertical data, UX and last-mile integrations._
