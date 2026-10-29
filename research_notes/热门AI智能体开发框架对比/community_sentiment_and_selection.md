# 开发者社区口碑、生产经验与框架选型指南（截至 2026-10）

> 研究范围：从从业者视角看 AI 智能体框架（LangGraph、CrewAI、OpenAI Agents SDK、Claude Agent SDK、Google ADK、Pydantic AI、Mastra、Microsoft Agent Framework、LlamaIndex、smolagents、Agno、Dify/n8n 等）。功能介绍由其他研究员负责，本文不展开。
> 标注约定：**[证据]** 指实证研究、调查、可复现基准或第一手案例；**[观点]** 指个人或厂商的论述；**[低可信]** 指 SEO/聚合站、单一作者无方法论测试，或只拿到二手转述、未读到原文的内容。厂商发布的材料会另外注明“厂商自述”。
> 研究日期：2026-10-21。HN 数据取自 hn.algolia.com API；news.ycombinator.com 本身无法直连。

---

## 1. 最有影响力的智能体架构/框架文章有哪些，各自主张什么？2025-2026 有哪些新文章改变了主流看法？

### Takeaway
2024-12 到 2025 年中，几篇奠基文章定下了主基调：先用简单、可组合的模式，慎用重框架，慎做多智能体，核心难题是上下文。主要是 Anthropic《Building effective agents》、12-Factor Agents、Cognition《Don't Build Multi-Agents》、Anthropic 多智能体研究系统、context engineering 系列。2025 年末到 2026 年，讨论的重心从“选哪个框架”转向“harness（智能体外壳/运行环境）+ 运行时（持久执行）+ 确定性控制流”。多智能体也得到有条件的“平反”：单写者，其余智能体只读或只出主意。

### Cited Findings
**奠基文章（2024-12 至 2025）**
- [观点] Anthropic《Building effective agents》，2024-12-19，作者 Erik S. 与 Barry Zhang。文章区分 workflows 和 agents：workflows 是“LLM 与工具按预定义代码路径编排”，agents 是“LLM 动态主导自身流程与工具使用”。文中给出 5 种工作流模式：prompt chaining、routing、parallelization、orchestrator-workers、evaluator-optimizer。关于框架，文章说它们 "often create extra layers of abstraction that can obscure the underlying prompts and responses"，并建议先直接用 LLM API，因为 "many patterns can be implemented in a few lines of code"，还提醒 "incorrect assumptions about what's under the hood are a common source of customer error"。现行页面列出的框架是 Claude Agent SDK、AWS Strands、Rivet、Vellum，并注明工具生态已变化，指向 Anthropic 新的 Managed Agents。由此看，页面发布后被修订过。— [Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- [观点] Harrison Chase（LangChain）《How to think about agent frameworks》，2025-04-20。这是对 OpenAI《A practical guide to building agents》的回应。主要论点：
  - 构建可靠智能体的难点是“确保 LLM 在每一步都有合适的上下文”。
  - “声明式 vs 命令式”是个弱维度。Agent 抽象类似 Keras，前提是能下沉到底层。
  - 用 floor/ceiling 比喻：workflow 框架门槛高、上限高，agent 抽象门槛低、上限低，LangGraph 想做到门槛低、上限高。
  - 框架真正的价值在短期/长期记忆、HITL、human-on-the-loop、流式输出、可观测性、容错（durable execution），并承认“如果你能自己构建这些，就可能不需要框架”。
  - 他称 OpenAI 指南的框架划分 "misguided"。作者是厂商一方，立场有偏。
  - 来源：[LangChain Blog](https://www.langchain.com/blog/how-to-think-about-agent-frameworks)
- [观点] 12-Factor Agents（HumanLayer，Dex Horthy）：
  - 核心论断：多数号称 "AI Agents" 的产品其实是 "mostly deterministic code, with LLM steps sprinkled in"。“循环直到达成目标”的模式不够可靠。用框架通常能做到 70-80% 质量，但 "80% isn't good enough for most customer-facing features"。
  - 12 条原则包括：Own your prompts、Own your context window、Own your control flow、Contact humans with tool calls、Make your agent a stateless reducer、Small, Focused Agents 等。
  - GitHub 约 26.8k stars。
  - 来源：[GitHub](https://github.com/humanlayer/12-factor-agents)。HN 首发于 2025-04-15，475 分、78 条评论：[HN Algolia](https://hn.algolia.com/api/v1/search?query=agent%20framework&tags=story&numericFilters=points%3E150,created_at_i%3E1735689600)
- [观点] Cognition（Walden Yan）《Don't Build Multi-Agents》，2025-06-12。两条原则：其一，"Share context, and share full agent traces, not just individual messages"；其二，行动携带隐含决策，冲突的决策会导致坏结果。文章用 Flappy Bird 例子说明子智能体风格冲突，点名 OpenAI Swarm 和 Microsoft AutoGen "actively push concepts which I believe to be the wrong way of building agents"。它推荐单线程线性智能体，并把 context engineering 称为 "the #1 job of engineers building AI agents"。— [Cognition](https://cognition.com/blog/dont-build-multi-agents)
- [证据，厂商自述] Anthropic《How we built our multi-agent research system》，2025-06-13：
  - Opus 4 主导、Sonnet 4 子智能体的多智能体系统，在内部研究评测上比单智能体 Opus 4 高 90.2%。
  - 在 BrowseComp 上，token 用量单独解释约 80% 的性能方差；加上工具调用次数与模型选择，合计解释 95%。
  - 智能体的 token 用量约为聊天的 4 倍，多智能体约 15 倍。
  - 不适合多智能体的场景：需要共享同一上下文、依赖多的任务，以及大多数编码任务。
  - 生产经验：需要从检查点恢复，不能从头重启；用 rainbow deployment 避免打断运行中的智能体。
  - 来源：[Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
- [观点] Anthropic《Effective context engineering for AI agents》，2025-09-29，Applied AI 团队。把 context engineering 定义为 "curating and maintaining the optimal set of tokens" during inference。提出 context rot：上下文越满，召回越差。技术手段有 just-in-time 检索、compaction、结构化笔记、子智能体。总原则是 "do the simplest thing that works"。— [Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [观点] Anthropic《Building agents with the Claude Agent SDK》，2025-09-29，Thariq Shihipar。Claude Code SDK 更名为 Claude Agent SDK，理由是 Claude Code 的 harness 可以驱动非编码智能体，例如金融、个人助理、客服、深度研究。核心循环是 "gather context -> take action -> verify work -> repeat"，并提出 "the folder and file structure of an agent becomes a form of context engineering"。— [Claude Blog](https://claude.com/blog/building-agents-with-the-claude-agent-sdk)
- [观点] Harrison Chase《Agent Frameworks, Runtimes, and Harnesses - oh my!》，2025-10-25。三分法：LangChain 是 framework（抽象），LangGraph 是 runtime（durable execution、流式、HITL、持久化），DeepAgents 是 harness。作者承认三者边界仍然模糊。全文未读到，以下信息来自搜索摘要和文档页。— [LangChain Blog](https://www.langchain.com/blog/agent-frameworks-runtimes-and-harnesses-oh-my)；[LangChain Docs concepts](https://docs.langchain.com/oss/python/concepts/)
- [观点] fly.io《You should write an agent》，HN 2025-11-06，1070 分、395 条评论。主张智能体就是“循环里的 LLM 调用加工具”，约 15 行即可写出。作者称 "context engineering is a straightforwardly legible programming problem"，认为 "MCP is just a plugin interface for Claude Code and Cursor"，主张 "Deal in APIs, not plugins"。抓取到的正文未署名，作者自述是漏洞研究员。— [fly.io](https://fly.io/blog/everyone-write-an-agent/)；[HN Algolia](https://hn.algolia.com/api/v1/search?query=agents&tags=story&hitsPerPage=40&numericFilters=points%3E250,created_at_i%3E1759276800)
- [观点] Karpathy 在 Dwarkesh 播客中说“需要十年才能解决智能体的问题”，HN 2025-10-17，1212 分、1115 条评论，可视为对智能体炒作的一次降温。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=agents&tags=story&hitsPerPage=40&numericFilters=points%3E250,created_at_i%3E1759276800)；[Dwarkesh](https://www.dwarkesh.com/p/andrej-karpathy)

**2026 年的新文章与观点变化**
- [观点] Philipp Schmid《The importance of Agent Harness in 2026》，2026-01-05：
  - 比喻：模型是 CPU，上下文是 RAM，harness 是操作系统，agent 是应用。
  - 框架提供积木；harness 是 "batteries included"，带预置提示、工具处理、生命周期钩子、规划/文件系统/子智能体。
  - 引用 Bitter Lesson，主张 harness 要轻、要 "Build to delete"。
  - 引用的案例：Manus 6 个月内重构 harness 5 次；LangChain Open Deep Research 一年重构 3 次；Vercel 删掉 80% 工具后步数更少、token 更少、速度更快。
  - 来源：[philschmid.de](https://www.philschmid.de/agent-harness-2026)
- [观点+厂商自述数据] Cognition（Walden Yan）《Multi-Agents: What's Actually Working》，2026-04-22，是对 2025 年文章的修正。新论点是：多智能体 "work best today when writes stay single-threaded and the additional agents contribute intelligence rather than actions"。
  - 有效的模式：单写者加辅助智能体；不共享上下文的 clean-context 审查者；"smart friend"，即便宜模型向强模型求助，主模型太弱时不成立；manager-child 拆分；只读检索子智能体。
  - 仍然无效：并行写入的 swarm、无结构的智能体互相协商，后者被称为 "mostly a distraction"。
  - 数据：Devin Review 平均每个 PR 抓到约 2 个 bug，其中约 58% 是严重 bug；最大企业客户群的用量 6 个月增长约 8 倍。
  - 来源：[Cognition](https://cognition.com/blog/multi-agents-working)
- [观点] 《Agents need control flow, not more prompts》（bsuh.bearblog.dev），2026-05-07，HN 590 分、296 条评论。主张用 "deterministic control flow encoded in software, not increasingly elaborate prompt chains"。文章把全大写的 "MANDATORY / DO NOT SKIP" 视为提示词已到天花板的信号，并说没有程序化校验时，只剩 "Babysitter / Auditor / Prayer" 三种选择。— [bearblog](https://bsuh.bearblog.dev/agents-need-control-flow/)；[HN](https://hn.algolia.com/api/v1/items/48051562)
- [观点] InfoWorld（Karthik Karunanithi，IBM 解决方案架构师），2026-07-24。Microsoft Agent Framework 于 2026-04 GA，AutoGen 与 Semantic Kernel 进入维护模式，“选 SDK 之争”因此结束。真正的架构决策是：是否需要 agent、上下文管理（"context beats model choice"）、失败恢复（"no framework makes for you"）、身份与权限、为变化而设计（与框架抽象紧耦合的团队迁移很痛苦）。— [InfoWorld](https://www.infoworld.com/article/4199575/the-microsoft-agent-framework-wars-are-over-the-real-architecture-decision-starts-now.html)
- [低可信] “loop engineering”一词据称在 2026-06 出现，指设计提示智能体的自主循环，Boris Cherny、Addy Osmani、Andrew Ng 有过讨论。只有二手来源。— [agentconn](https://agentconn.com/blog/loop-engineering/)；[Simon Willison 2025-05-22 "tools in a loop"](https://feeds.simonwillison.net/2025/May/22/tools-in-a-loop/)

### Inferences
- 观点演变大致分三段：2024-12 至 2025-06“少用框架，少做多智能体，先把上下文做好”；2025-09 至 2025-12“harness 和上下文工程成为一等公民，编码智能体的 harness 被泛化”；2026“在 harness/运行时之上用确定性控制流约束模型，多智能体只在单写者模式下回归”。
- LangChain 的回应路线也在变：先辩护框架的价值（2025-04），再把产品重新定位成 framework/runtime/harness 三层（2025-10），并推出 1.0 稳定承诺（见第 3 节）。这说明社区批评确实推动了产品调整。

### Gaps
- 《Building effective agents》2024 年原版列出了哪些框架，没能直接核实。我印象中包括 LangGraph、Bedrock Agents，但未验证，不应引用。现行页面已修订。
- 《Agent Frameworks, Runtimes, and Harnesses》全文、OpenAI《A practical guide to building agents》原文均未直接读取。
- Simon Willison、Hamel Husain、Eugene Yan、Chip Huyen 对“框架”的直接表态没有检索到可靠一手出处。Hamel 的相关观点主要是“通用 eval 框架是谬误”，来自二手转述：[antoinebuteau](https://www.antoinebuteau.com/lessons-from-hamel-husain/)。

---

## 2. “到底需不需要框架？”之争

### Takeaway
最强的实证数据来自 UC Berkeley 等机构的 MAP 研究：深访的 20 个生产团队中，85% 自研、直接调 API，只有 3 个用了框架；但更大样本的问卷里 61% 用框架。这说明“大规模、高要求的生产系统偏向自研，大众开发者偏向框架”。共识正在收敛为：不需要“智能体抽象”框架，但很可能需要“运行时能力”，包括持久化、HITL、durable execution 和可观测性。这些能力可以来自 LangGraph 一类框架，也可以来自 Temporal/DBOS 加薄封装，或来自托管 harness。

### Cited Findings
- [证据] 《Measuring Agents in Production》（MAP），arXiv 2512.04123v3，UC Berkeley 牵头，2026-02 修订。数据收集于 2025-04 至 2025-11，包括 20 个深度案例访谈和 306 份有效问卷。
  - 框架使用："Production agents favor custom implementations (85%) over frameworks for flexibility, simplicity, and control at scale"。20 个案例中 17 个自研、直接调 API；只有 3 个用框架（LangChain/LangGraph、DSPy）。问卷中 61% 用框架，其中 LangChain/LangGraph 占 25%。
  - 自主程度：68% 的已部署智能体在人工介入前执行不到 10 步，47% 不到 5 步；80% 的案例采用结构化 workflow，而非开放式自主规划。
  - 模型与评测：70% 的案例直接用现成模型，不做 SFT/RL；74% 依赖人工评估，52% 用 LLM-as-judge；75% 的案例没有正式基准集。
  - 痛点与结论：可靠性是首要瓶颈，38% 的受访者把它列为第一优先级。作者结论是 "Teams deliberately constrain autonomy for production stability"。
  - 来源：[arXiv](https://arxiv.org/html/2512.04123v3)
- [证据] LangChain《State of Agent Engineering》问卷，2025-11-18 至 12-02，1,340 份回答。57.3% 已有生产智能体（上年为 51%），30.4% 在开发中；万人以上企业 67% 已上生产。厂商调查，样本偏向 LangChain 用户。— [LangChain](https://www.langchain.com/state-of-agent-engineering)
- [观点] Anthropic：先直接用 LLM API，很多模式几行代码即可实现。— [Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- [观点] Harrison Chase 的反方论点：框架的价值不在 agent 抽象，而在记忆、HITL、流式、可观测、容错；"you may not need a framework if you can build these yourself"。— [LangChain Blog](https://www.langchain.com/blog/how-to-think-about-agent-frameworks)
- [观点] HN 上 LangChain CVE-2025-68664 的讨论（2025-12-25，131 分、91 条评论）：
  - baobabKoodaa 认为 LangChain "does not solve any actual problem"。
  - hhh 认为在快速变化的领域，自写编排反而容易。
  - prodigycorp 说很多人后悔，但 "in too deep"。
  - 推荐的替代方案有 Pydantic/PydanticAI、BAML、Spring AI、Mastra（TS）、原生 SDK 手写。
  - 也有反例：stbenjam 用 LangChain 做的内部 CI 聊天机器人已上线、够用，但正在转向 Claude Code 式工具。
  - 来源：[HN item 46386009](https://hn.algolia.com/api/v1/items/46386009)
- [低可信，二手] Crail 编辑部（2026-07-27）把 "agent framework fatigue" 视为主流情绪。它引用 Ask HN《Sick of AI Agent Frameworks》中的说法：框架 "work, just barely"，多数是 "workflow builders with LLMs as a node"；另有评论者称在律所做了约 900 个智能体却没用框架。文章没有量化数据，原帖也未能直接读取。— [Crail](https://www.crail.ai/blog/agent-framework-fatigue-and-the-langchain-cve/)；原帖 [HN 42691946](https://news.ycombinator.com/item?id=42691946)
- [观点] HN《Claude Managed Agents》讨论（2026-04-08，169 分、87 条评论）中有两种声音：
  - 认可托管：bnchrch 说它省去了为啤酒厂内部订单/开票智能体搭生产基础设施的工作；suncemoje 用过 OpenAI Agents SDK，认为难点在基础设施、可观测性和扩展，正是托管方案解决的部分。
  - 反对框架：gck1 认为框架对非确定性模型太僵化，tmux 就能做很多编排；jameslk 认为框架仍不成熟、每周都在变。
  - 来源：[HN item 47693047](https://hn.algolia.com/api/v1/items/47693047)
- [观点] 掘金（2026-10-20）认为分类、抽取、总结类任务直接调模型即可，不需要框架。— [掘金](https://juejin.cn/post/7698533148759408681)
- [观点] InfoWorld：先问是否需要 agent；固定步骤的流程应写成测试充分的函数工作流。— [InfoWorld](https://www.infoworld.com/article/4199575/the-microsoft-agent-framework-wars-are-over-the-real-architecture-decision-starts-now.html)
- [观点] 《Show HN: Axe – A 12MB binary that replaces your AI framework》（2026-03-12，227 分、128 条评论）反映出“去框架化”工具的热度。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=agent%20framework&tags=story&numericFilters=points%3E150,created_at_i%3E1735689600)
- [观点，中文] Datawhale 的 Hello-Agents 教程带读者用原生 API 自己实现一套框架，“不被 LangChain 等框架局限”。但推荐它的作者也承认，LangChain 在容错等方面很成熟，工作中仍在用。— [知乎](https://zhuanlan.zhihu.com/p/2047724163847156731)

### Inferences
- “要不要框架”其实是“要不要外包运行时能力”。纯 agent 循环几十行代码就能写；真正贵的是 durable execution、断点恢复、HITL 暂停/恢复、追踪和评测。MAP 的“85% 自研”和 LangChain 调查的“89% 有可观测性”并不矛盾：自研团队同样要自建或采购这些能力。
- 团队越资深、系统越关键，越倾向自研或薄封装；团队越大众化，越需要框架提供心智模型。这与 Harrison Chase 说的“抽象帮助入门”一致，也与 12-Factor 的“框架让你到 70-80%”一致。

### Gaps
- 没有找到区分“生产成功率 × 是否用框架”的对照研究。MAP 只做了描述性统计。
- Ask HN《Sick of AI Agent Frameworks》原帖无法直接访问，900 个智能体的律所案例只有二手转述。

---

## 3. 各主流框架反复出现的批评与好评

### Takeaway
LangChain 长期背负“抽象过深、API 频繁变动、依赖冲突”的口碑，2025-10 的 1.0 稳定承诺是对此的正面回应。LangGraph 被普遍视为“生产级状态编排的默认选项”，代价是学习曲线和样板代码。CrewAI 上手快，但几乎所有基准都显示它 token 开销最高，生产化能力需要自补。Pydantic AI 在 HN 上口碑持续上升，被当作“薄而类型安全”的选择。各厂商 SDK 起步最简单，最大顾虑是厂商锁定。AutoGen 已被 Microsoft Agent Framework 取代。低代码平台（Dify/n8n/Coze）的定位是“快速验证”，复杂逻辑仍要回到代码。

### Cited Findings
**跨框架实证（GitHub 讨论挖掘）**
- [证据] arXiv 2512.01939《An Empirical Study of Agent Developer Practices in AI Agent Frameworks》（中山大学等，2025-12-01）。数据：1,575 个仓库、8,710 条讨论；RQ3 分析 10 个框架的 11,910 条讨论，其中 LangChain 6,006 条、LlamaIndex 1,691 条、LangGraph 978 条、AutoGen 988 条、CrewAI 224 条。
  - 问题分布：版本/兼容性问题约占 23%-25% 以上，例如 LangChain 的 Pydantic v1→v2、AutoGen 的 v0.2→v0.4 重写；任务终止问题约 21.6%-25.6%；性能问题 16.03%。
  - 开发者关注维度：开发效率 28.4%、功能抽象 21.1%、学习成本 18.7%、可维护性 14.5%、性能 12.3%。
  - LangChain：约 42% 的开发者认为深度嵌套的抽象拖慢了进度；破坏性变更和 pydantic 冲突使其维护复杂度最高。
  - AutoGen：约 31% 的项目在自定义工具上出现适配或调用失败；v0.4 重构带来很重的维护负担。
  - CrewAI：声明式编排对新手友好，但文档薄，对 LiteLLM/Pydantic 的严格版本锁定会引发冲突。
  - LangGraph：breakpoint 机制支持人工审查，但与 LangChain 耦合过紧。
  - LlamaIndex：检索强，但缺少历史管理和冲突解决，内存占用高。
  - Semantic Kernel：没有内置缓存，存在内存泄漏，示例过时。
  - 跨框架：96% 的高星项目组合使用两个以上框架；缓存普遍缺失；MCP 的提示开销约 11.7k tokens，其中 40% 是 MCP 指令。
  - 来源：[arXiv](https://arxiv.org/html/2512.01939v1)

**LangChain / LangGraph**
- [证据，第一手] Octomind《Why we no longer use LangChain for building our AI agents》，HN 2024-06-20，480 分、297 条评论，是最有代表性的“弃用”文章，核心批评是不必要的抽象层。原文域名无法解析，未读到全文。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=langchain&tags=story&numericFilters=points%3E80,created_at_i%3E1704067200)
- [证据] CVE-2025-68664（langchain-core 序列化对象混淆，可能泄露密钥）由 Cyata 于 2025-12 披露。根因是 `dumps()/dumpd()` 没有转义含保留键 `lc` 的用户字典。— [Cyata](https://cyata.ai/blog/langgrinch-langchain-core-cve-2025-68664/)；[HN item 46386009](https://hn.algolia.com/api/v1/items/46386009)
- [证据] LangChain 与 LangGraph 1.0 于 2025-10-22 发布，承诺 "no breaking changes until 2.0"。新增 `create_agent`（基于 LangGraph runtime）和 middleware（HITL、摘要、PII 脱敏）；旧 chains/AgentExecutor 移入 `langchain-classic`。— [LangChain Blog](https://www.langchain.com/blog/langchain-langgraph-1dot0)
- [观点] HN 用户 persedes（2026-09）批评 LangChain 的 "version-branching mess"，转用 Pydantic AI。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=%22pydantic%20ai%22&tags=comment&hitsPerPage=25&numericFilters=created_at_i%3E1735689600)
- [低可信] 多篇 2026 年对比文章称 LangGraph 是生产状态化工作流的最安全选择，代价是学习曲线陡、要定义 state schema/节点/边，简单工具型智能体用它显得过度设计。— [letsdatascience](https://letsdatascience.com/blog/ai-agent-frameworks-compared)；[the-agent-report](https://the-agent-report.com/2026/07/ai-agent-frameworks-comparison-2026-langgraph-crewai-autogen/)
- [观点，中文] 掘金把 LangGraph 定为 Python 团队、复杂长流程、需要断点恢复和人工审批时的“默认答案”。— [掘金](https://juejin.cn/post/7698533148759408681)

**CrewAI**
- [证据] 两个独立基准都显示 CrewAI token 开销最高，见第 5 节：AIMultiple 中 travel planner 输出 5,339 tokens，LangGraph 为 2,589；DEV Grochal 中每次运行 27,684 tokens，约为 MAF 的 4 倍。— [AIMultiple](https://aimultiple.com/agentic-orchestration)；[DEV](https://dev.to/lukaszgrochal/i-benchmarked-5-ai-agent-frameworks-heres-what-actually-matters-3ela)
- [观点] HN 用户的说法：thienzz（2026-01）认为 CrewAI 等框架偏重，启动慢、资源占用高、缺少防循环/失败保护；Shanmugaraj-1（2026-03）说生产中安全、可观测、RBAC 都得自己补；matbanik（2026-06）的做法是先用 OpenCode 原型，再移植到 LangGraph 或 CrewAI 上线。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=crewai%20production&tags=comment&hitsPerPage=25&numericFilters=created_at_i%3E1735689600)
- [低可信，中文] CSDN/掘金类文章称 CrewAI 无法从崩溃点恢复，团队需要生产级状态管理时常迁移到 LangGraph。— [CSDN](https://blog.csdn.net/weixin_32050773/article/details/164522126)

**AutoGen / Semantic Kernel → Microsoft Agent Framework**
- [证据] Microsoft Agent Framework 于 2026-04 达到 1.0/GA，覆盖 .NET 与 Python；Semantic Kernel 和 AutoGen 进入维护模式。— [InfoWorld](https://www.infoworld.com/article/4199575/the-microsoft-agent-framework-wars-are-over-the-real-architecture-decision-starts-now.html)
- [观点] BUILD 2026 上，MAF 把 harness 作为核心概念，并宣布了长工具链自动 compaction、Hosted Agents、CodeAct 等能力。— [Microsoft DevBlogs](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/)
- [观点，中文] 掘金提醒新项目不要再用 AutoGen。— [掘金](https://juejin.cn/post/7698533148759408681)

**Pydantic AI**
- [观点] HN 好评较多：
  - persedes（2026-09）称其为 "go-to"。
  - gorkaerana（2026-05）称其 "a superb addition"。
  - corv（2026-09）用一个薄 Pydantic AI 封装替换了 OpenCode，看重访问控制、表面积小、代码易懂。
  - benlm（2026-04）在其上构建了生产文档助手的虚拟文件系统。
  - rick1290（2026-04）选择 Pydantic AI + DBOS/Temporal/Celery，以避免厂商锁定。
  - eleventen（2026-04）因为 Claude API 定价，把应用从 Claude SDK 迁到了 Pydantic AI。
  - 来源：[HN Algolia](https://hn.algolia.com/api/v1/search?query=%22pydantic%20ai%22&tags=comment&hitsPerPage=25&numericFilters=created_at_i%3E1735689600)
- [观点] 批评：Show HN《I tested 11 AI frameworks for basic security – none passed》（2026-04）指出 Pydantic AI 等缺少内置的运行时安全能力，如注入检测和 PII 脱敏。— 同上
- [证据，官方文档] Pydantic AI 官方支持 4 种 durable 后端：Temporal、DBOS、Prefect、Restate。— [Pydantic Docs](https://pydantic.dev/docs/ai/integrations/durable_execution/overview/index.md)
- [低可信] Pydantic AI 据称于 2025-09 发布 V1，承诺 V2 之前不做破坏性变更。— [myengineeringpath](https://myengineeringpath.dev/tools/pydantic-ai/)

**OpenAI Agents SDK**
- [证据] HN 上《OpenAI adds MCP support to Agents SDK》（2025-03-26）获得 807 分、267 条评论，说明社区高度关注。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=agents%20SDK&tags=story&numericFilters=points%3E80,created_at_i%3E1735689600)
- [证据，厂商] Temporal 与 OpenAI Agents SDK 的集成于 2026-03-23 GA，用来应对限流、网络失败和崩溃。— [Temporal](https://temporal.io/blog/announcing-openai-agents-sdk-integration)
- [低可信] 对比类文章普遍认为它上手最简单、handoff 模式直观，但锁定集中在托管 tracing 和服务端工具上；也有人指出它能接任意 OpenAI 兼容端点。— [silverthreadlabs](https://www.silverthreadlabs.com/blog/ai-agent-sdks-compared)；[kanopylabs](https://kanopylabs.com/blog/claude-agent-sdk-vs-openai-agents-sdk-vs-google-adk)
- [低可信，单作者测试] 有人测试发现，朴素重试时 OpenAI Agents SDK 会重复执行动作，而 ADK 在一次调用内不会重复已成功的工具调用。— [Medium](https://medium.com/@Micheal-Lanham/adk-typescript-vs-openai-agents-sdk-which-one-survives-retries-timeouts-and-human-approvals-808903d65a61)

**Claude Agent SDK / Claude Managed Agents**
- [观点] 被认为是“通用 harness”的代表，Phil Schmid 和 LangChain 文档都把它归为 harness。— [philschmid.de](https://www.philschmid.de/agent-harness-2026)；[LangChain Docs](https://docs.langchain.com/oss/python/concepts/)
- [观点] 主要顾虑是锁定和定价。在 HN Managed Agents 讨论中，JLO64 和 dakolli 认为单一供应商锁定不可接受；mccoyb 认为 Anthropic 不会让竞争模型进入它的 harness；mrbungie 认为可用性的“9”还不够。— [HN item 47693047](https://hn.algolia.com/api/v1/items/47693047)

**Google ADK**
- [低可信] 有报告称 Cloud Run 容器重启后内存中的会话状态会丢失，持久存储配置不当曾导致用户看到他人会话；LoopAgent 不设 max_iterations 会导致成本失控。— [aimakers](https://www.aimakers.co/blog/ai-agents-landscape-2026/)；[vertexfrontier](https://vertexfrontier.com/google-agent-development-kit-adk/)

**Mastra（TypeScript）**
- [证据] HN 热度：Show HN（2025-02-19）442 分、154 条评论；Mastra 1.0（2026-01-20）213 分、70 条评论。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=agent%20framework&tags=story&numericFilters=points%3E150,created_at_i%3E1735689600)
- [低可信] 好评集中在 TS 优先、类型安全（编译期能发现缺失的工具参数）、可自托管；批评是检查点/durable resume 不如 LangGraph 成熟、生态较新。据称用户包括 Replit、PayPal、Brex 等。— [openaitoolshub](https://www.openaitoolshub.org/en/blog/mastra-ai-framework-review)；[makerstack](https://makerstack.co/reviews/mastra-review/)

**smolagents / Agno**
- [观点] HN 用户 Imanari 提到 smolagents 以 Python 代码作为唯一工具（CodeAct 思路），并把它当作“少工具更可靠”的例证。— [HN item 48051562](https://hn.algolia.com/api/v1/items/48051562)
- 2025 年后 HN 评论中检索不到对 smolagents 或 Agno 的实质性评价（返回 0 条），见 Gaps。

**低代码：Dify / n8n / Coze**
- [观点] Jimmy Song（2025-08）的评级：Dify 五星，n8n、Coze、LangGraph、RAGFlow 各四星。他提醒 Dify、FastGPT、n8n 限制未经授权的 SaaS 化使用（n8n 是 fair-code 许可），而 Coze、LangGraph、RAGFlow 是宽松许可；企业团队适合 Coze/Dify/n8n，强技术团队适合 LangGraph。— [jimmysong.io](https://jimmysong.io/blog/open-source-ai-agent-workflow-comparison/)
- [低可信] 有评测认为可视化工具存在天花板，复杂定制逻辑应放进代码；竞品称，需要在业务系统中“行动”的智能体，团队会离开 Dify。— [chatforest](https://chatforest.com/reviews/dify-open-source-ai-workflow-agent-platform-review/)；[activepieces](https://www.activepieces.com/blog/dify-alternatives-4-options-compared-2026-guide.md)
- [观点，中文] 掘金的说法是“GUI 验证，代码上线”，全拖拽或全写代码都很难走远。— [掘金](https://juejin.cn/post/7698533148759408681)

### Inferences
- 批评的焦点在迁移：2023-2024 年是“抽象太深/太黑盒”，主要针对 LangChain；2025 年是“版本变动和依赖冲突”，加上一次 CVE；2026 年是“厂商锁定”和“生产化能力（安全、durable、可观测）要自补”。
- “薄、类型化、可换模型”成为 HN 社区偏好的方向，Pydantic AI、Mastra、自研薄 harness 都属此类。重抽象、角色扮演式的多智能体框架（CrewAI、早期 AutoGen）在资深开发者中口碑下滑，但在原型和新手场景仍有市场。

### Gaps
- smolagents、Agno、LlamaIndex Workflows 在 2026 年缺少可靠的社区评价样本。
- 没能直接访问 Reddit（r/LangChain、r/AI_Agents、r/LocalLLaMA），搜索引擎也没返回相关帖子，因此 Reddit 情绪未覆盖。
- Google ADK 的生产反馈只有低可信来源。

---

## 4. 生产案例与迁移故事

### Takeaway
公开的迁移故事几乎都朝一个方向走：从重抽象框架迁到“更薄、更可控”的方案，原因集中在可控性、可调试性和工程师可维护性。具体去向有 LangChain → Pydantic AI 或自研，原型框架 → LangGraph。大型 AI 原生公司（Anthropic、Cognition、Manus、Vercel）的经验是：harness 要不断删减重构，多智能体只在特定形态下有效。

### Cited Findings
- [证据，厂商自述] MindsDB 从 LangChain 迁到 Pydantic AI，2025-01-27 发布。
  - 迁移前：用 LangChain 约两年，CEO Jorge Torres 形容排障过程是 "whack-a-mole game"，智能体像黑盒，只有少数人能改。
  - 迁移过程：周末做出 POC，一个月内智能体性能提升 10 倍，并因此拿下一个企业单。
  - 迁移后：依赖大幅减少，后端工程师都能参与，实验从数周缩短到数小时。
  - Torres 的原话："The more we let the LLM figure things out in loops, the more mistakes it tends to make."
  - 来源：[Pydantic](https://pydantic.dev/case-studies/mindsdb)
- [证据，二手] Octomind 弃用 LangChain，2024-06，HN 480 分，见第 3 节。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=langchain&tags=story&numericFilters=points%3E80,created_at_i%3E1704067200)
- [证据] MAP 的 20 个生产案例：17 个自研，16 个用结构化 workflow，14 个不做微调，17 个用闭源模型（Claude Sonnet 4/Opus 4.1、GPT o3 等），15 个可异步运行。— [arXiv](https://arxiv.org/html/2512.04123v3)
- [证据，厂商自述] Cognition Devin：多智能体只保留单写者、clean-context 审查者、smart friend 和 manager-child；Devin Review 平均每个 PR 约 2 个 bug、58% 为严重 bug。— [Cognition](https://cognition.com/blog/multi-agents-working)
- [证据，厂商自述] Anthropic Research：多智能体 +90.2%，代价是约 15 倍 token；工具描述改写智能体让后续任务耗时减少 40%。— [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
- [证据，二手] Manus 6 个月内重构 harness 5 次；LangChain Open Deep Research 一年重构 3 次；Vercel 删掉 80% 工具后步数、token、延迟都下降。— [philschmid.de](https://www.philschmid.de/agent-harness-2026)
- [证据，HN 第一手轶事]
  - evilelectron：用确定性的解析器和生成器做 spec-to-code，只在校验失败时调用 Claude，总花费不到 350 美元。
  - marcus_holmes：禁止 LLM 执行任何资金操作，必须走经校验的 API 加人工审核。
  - scrappyjoe：花一周扩充提示词，效果变差；花一周精确定义对象和操作，效果变好。
  - 来源：[HN item 48051562](https://hn.algolia.com/api/v1/items/48051562)
- [证据，HN 轶事] nostrebored 用 LangChain 在约 5 万条记录上做结构化抽取，错误率高、schema 理解差；jmogly 说 Gemini 2.5 Pro 不加封装就能处理复杂结构化输出。— [HN item 46386009](https://hn.algolia.com/api/v1/items/46386009)
- [证据，二手] 据称 OpenAI（Codex web）、Replit、Lovable 采用 Temporal 一类 durable execution。— [ZenML LLMOps DB](https://www.zenml.io/llmops-database/building-reliable-production-ai-agents-with-durable-execution-infrastructure)
- [证据，中文，自愿提报样本] InfoQ 年终榜单征集到 200 多家企业的 300 多个 AI 案例（2025-12-26）。所有成功案例都在关键节点保留人工干预；普遍融合领域知识（语义图谱、本体）来抑制幻觉。文中没有统计框架使用情况。— [InfoQ 中文](https://www.infoq.cn/article/GXuY8mpKHgWpeIFOoPtd)
- [观点，中文] QCon 北京 2026 Agentic Engineering 专题描述的现状是“PoC 满天飞，生产级系统寥寥无几”。— [QCon 北京 2026](https://qcon.infoq.cn/2026/beijing)
- [证据，HN 事故类] 《An AI agent deleted our production database》（2026-04-26，860 分、1032 条评论）、《AI agent bankrupted their operator…》（2026-06，1467 分）等事故帖热度很高，推动了沙箱和权限方面的讨论。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=agents&tags=story&hitsPerPage=40&numericFilters=points%3E250,created_at_i%3E1759276800)

### Inferences
- 迁移的主要驱动是可控性和可维护性，不是性能或成本。MindsDB 所说的“10 倍”多半来自控制流显式化，而不是框架本身更快。这与 12-Factor 的“Own your control flow”和 2026 年“control flow, not more prompts”一致。
- 反向迁移（自研 → 框架）的公开故事很少。迁向托管 harness（如 Managed Agents）的动机是“省掉基础设施”，属于新出现的第三条路。

### Gaps
- 没有找到独立第三方的 CrewAI → LangGraph、OpenAI Agents SDK 生产复盘，只有中文低可信文章提到这一模式。
- 字节 Eino、阿里 AgentScope/Spring AI Alibaba 的生产案例未深入检索。已知 InfoQ 有 Eino 实践文章：[InfoQ](https://www.infoq.cn/article/g1owAQLkxG5Ehg52mfGf)，但未读。

---

## 5. 独立对比文章与基准测试的结论

### Takeaway
现有“框架基准”样本都很小、任务单一，排名彼此矛盾，目前没有覆盖所有主流框架、可复现的权威基准。唯一稳定的信号是 CrewAI 的 token 开销偏高。同一模型下各框架的输出质量差异很小，质量主要由模型和上下文决定；框架影响的是延迟、token 和一致性，而且受实现方式影响很大。不要把单篇基准当作选型依据，应该在自己的任务上固定模型和提示词做 bake-off。

### Cited Findings
- [证据] AIMultiple，Hazal Şimşek，页面同时标注 2026-06-04 与 2026-10-12 两个更新日期。
  - 方法：5 智能体串行旅行规划，Claude Haiku 4.5，temperature 0.1，每个框架跑 100 次，测试 LangGraph、LangChain、CrewAI、AutoGen。
  - token：travel planner 输出 CrewAI 5,339、AutoGen 3,316、LangChain 3,187、LangGraph 2,589。
  - 延迟：CrewAI 的 agent-to-tool 间隔达 5,010 ms（Flight Finder），其他框架低于 0.1 ms；LangGraph 比 CrewAI 快 2.2 倍。
  - 不足：没有给出总耗时绝对值。
  - 来源：[AIMultiple](https://aimultiple.com/agentic-orchestration)
- [证据，开源可复现] DEV（Łukasz Grochal，2026-02-16）。
  - 方法：3 智能体公司研究流水线，Qwen 3 14B 本地运行，temperature 0，每个框架 9 次；Kruskal-Wallis 加 Bonferroni 校正；代码已开源。
  - 结果：

    | 框架 | 平均延迟 | 平均 tokens | 质量 |
    |---|---|---|---|
    | MS Agent Framework（1.0.0b） | 93s | 7,006 | 9.87 |
    | CrewAI | 246s | 27,684 | 9.66 |
    | AutoGen | 572s | 10,793 | 9.63 |
    | LangGraph（1.0.x） | 506s | 8,823 | 9.42 |
    | OpenAI Agents SDK | 448s | 8,676 | 9.31 |

  - 结论：质量总差距只有 0.56 分，校正后只有 Agents SDK 与 MAF 的差异显著；作者结论是 "all five frameworks produce excellent output"，选型应看速度、成本和一致性。
  - 局限：样本小，用的是本地 14B 模型。
  - 来源：[DEV](https://dev.to/lukaszgrochal/i-benchmarked-5-ai-agent-frameworks-heres-what-actually-matters-3ela)
- [低可信，仅搜索摘要] 以下几项结论与上面相互矛盾：
  - DEV《107 Task Bakeoff》：AutoGen 延迟和 token 最低，CrewAI 最高；作者承认无法确认模型、提示和重试是否一致。— [DEV](https://dev.to/priyeshdave6/agent-frameworks-in-the-real-world-107-task-bakeoff-of-langgraph-crewai-and-autogen-13e7)
  - AgentMail 测了 9 个框架，LangGraph token 开销最低，CrewAI 单智能体高约 11%。这是厂商博客。— [AgentMail](https://www.agentmail.to/blog/best-ai-agent-frameworks-2026)
  - arXiv《Open Agent Specification》：CrewAI F1 最高但响应慢，LangGraph 快但 F1 低。— [arXiv 2510.04173](https://arxiv.org/pdf/2510.04173)
- [证据] arXiv 2512.01939：检索增强智能体平均每次查询 3.2-5.6 秒，比直接生成慢约 1.8 倍；MCP 提示开销约 11.7k tokens。— [arXiv](https://arxiv.org/html/2512.01939v1)
- [证据，HN] HarnessTax（2026-09-16，233 分、99 条评论）评测编码智能体 harness 带来的 token/成本开销，主要来自系统提示和工具描述。评论有几种看法：
  - nojs 认为 harness 主要是防止工具调用失败，对“智能”影响不大。
  - lukax 指出模型会被特定 harness 的工具名“训练绑定”，例如 DeepSeek 会套用 Claude Code 的 `old_string`。
  - big-chungus4 认为小模型更需要精简的 harness。
  - 原页面无法加载，具体数字未获取。
  - 来源：[HN item 49733726](https://hn.algolia.com/api/v1/items/49733726)
- [观点] Berkeley RDI《Exploiting the most prominent AI agent benchmarks》（2026-04-11，HN 588 分）指出主流智能体基准存在可被利用的漏洞。只看了标题，正文未读。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=agents&tags=story&hitsPerPage=40&numericFilters=points%3E250,created_at_i%3E1759276800)
- [低可信] 多数 “Top N frameworks 2026” 文章（uvik、bovo-digital、agentlist、qubittool 等）的基准表方法论不明、数字相互冲突，不建议引用。— [letsdatascience](https://letsdatascience.com/blog/ai-agent-frameworks-compared)；[qubittool](https://qubittool.com/blog/ai-agent-framework-comparison-2026)

### Inferences
- 框架的 token 开销主要来自框架注入的系统提示、角色描述和中间推理（CrewAI 的 role/goal/backstory 模式），以及工具描述（MCP、harness）。这与 HarnessTax 讨论和 MAP 的“提示开销”发现一致。成本敏感的场景应关注“框架默认注入了多少 token”。
- 延迟排名会随实现方式翻转（MAF 和 AutoGen 在两项研究中排位相反），说明框架本身不是主要变量，模型、并发策略和工具实现更重要。

### Gaps
- 没有覆盖 Claude Agent SDK、Google ADK、Pydantic AI、Mastra、Agno、smolagents 的公开可复现对比基准。
- 没有任务成功率在复杂长任务（如 50 步以上）上的跨框架对比。

---

## 6. 实践者推荐的选型标准，以及“场景 → 推荐框架”映射

### Takeaway
从业者共识是先回答几个问题：是否需要 agent，自主程度需要多高，是否需要持久化/HITL/断点恢复，团队语言栈，是否允许单一模型锁定，谁来维护。框架排名是次要的。多数生产场景是“结构化 workflow + 有限自主 + 人工节点”，所以运行时能力比 agent 抽象更重要。

### Cited Findings
**选型标准（来源支撑）**
- [观点] 先问是否需要 agent：固定步骤的流程用函数工作流，需要选工具、适应、规划时才用 agent。然后看上下文管理、失败恢复（重试、回滚、升级到人工、带着部分结果继续）、身份与权限、为变化设计（业务逻辑、提示、编排松耦合）。— [InfoWorld](https://www.infoworld.com/article/4199575/the-microsoft-agent-framework-wars-are-over-the-real-architecture-decision-starts-now.html)
- [证据] 生产现实：68% 的智能体不到 10 步就需要人工介入；80% 的案例用结构化 workflow；66% 能容忍分钟级以上的响应；可靠性是第一瓶颈。— [MAP arXiv](https://arxiv.org/html/2512.04123v3)
- [证据] 质量是最大障碍（32%），其次是延迟（20%）；2000 人以上企业把安全排第二（24.9%）。可观测性覆盖 89%，生产组织中达 94%，但离线评测只有 52.4%。超过四分之三的组织使用多个模型。— [LangChain 调查](https://www.langchain.com/state-of-agent-engineering)
- [观点] 多智能体只在宽度优先、可并行、上下文依赖低的任务（如研究）上值得做，且 token 成本约为聊天的 15 倍；大多数编码任务不适合。— [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)。写操作保持单线程。— [Cognition](https://cognition.com/blog/multi-agents-working)
- [观点] 中文社区的五个坑：
  1. 把 demo 当生产。应事先定好成功率、延迟、转人工率和成本上限。
  2. 只看 GitHub stars。应结合下载量、生产案例和最近提交。
  3. 工具路线一刀切。
  4. 没有 eval。
  5. 忽视协议锁定。工具用 MCP，智能体间用 A2A。
  - 来源：[掘金](https://juejin.cn/post/7698533148759408681)
- [证据] 超过 80% 的开发者表示难以找到满足需求的框架；GitHub 上开源智能体框架超过 100 个。— [arXiv 2512.01939](https://arxiv.org/abs/2512.01939v1)
- [观点] 许可证也是选型维度：Dify、n8n、FastGPT 限制 SaaS 化，Coze、LangGraph、RAGFlow 是宽松许可。— [jimmysong.io](https://jimmysong.io/blog/open-source-ai-agent-workflow-comparison/)
- [观点] 锁定的分布：智能体逻辑可移植，周边脚手架（托管工具、tracing、权限模型）不可移植，切换成本集中在后者。— [kanopylabs](https://kanopylabs.com/blog/claude-agent-sdk-vs-openai-agents-sdk-vs-google-adk)（低可信）；HN 上的多模型路由诉求见 [HN 47693047](https://hn.algolia.com/api/v1/items/47693047)

**场景 → 推荐映射（综合上述来源；推荐属于综合判断）**

| 场景 | 推荐方向 | 依据 |
|---|---|---|
| 单步/少步 LLM 任务（分类、抽取、总结、简单工具调用） | 不用框架：原生 SDK + 结构化输出（可选 Pydantic AI / BAML） | [掘金](https://juejin.cn/post/7698533148759408681)；[Anthropic](https://www.anthropic.com/engineering/building-effective-agents)；HN 评论 [46386009](https://hn.algolia.com/api/v1/items/46386009) |
| Python、复杂长流程、需要断点恢复和人工审批 | LangGraph（或 LangChain 1.0 `create_agent` 起步） | [掘金](https://juejin.cn/post/7698533148759408681)；[LangChain 1.0](https://www.langchain.com/blog/langchain-langgraph-1dot0) |
| Python，重视类型安全、可换模型、想要薄封装 | Pydantic AI + Temporal/DBOS 等 durable 后端 | [HN 评论](https://hn.algolia.com/api/v1/search?query=%22pydantic%20ai%22&tags=comment&hitsPerPage=25&numericFilters=created_at_i%3E1735689600)；[Pydantic docs](https://pydantic.dev/docs/ai/integrations/durable_execution/overview/index.md)；[MindsDB](https://pydantic.dev/case-studies/mindsdb) |
| TypeScript 全栈团队 | Mastra / Vercel AI SDK | [掘金](https://juejin.cn/post/7698533148759408681)；[HN Mastra 1.0](https://hn.algolia.com/api/v1/search?query=agent%20framework&tags=story&numericFilters=points%3E150,created_at_i%3E1735689600) |
| .NET / 微软生态 | Microsoft Agent Framework（不要再用 AutoGen） | [InfoWorld](https://www.infoworld.com/article/4199575/the-microsoft-agent-framework-wars-are-over-the-real-architecture-decision-starts-now.html)；[掘金](https://juejin.cn/post/7698533148759408681) |
| 深度绑定单一云/模型厂商 | 对应官方 SDK：OpenAI Agents SDK / Claude Agent SDK / Google ADK / AWS Strands | [掘金](https://juejin.cn/post/7698533148759408681) |
| 长时间、开放式、需要“电脑”（文件系统、bash、浏览）的通用智能体 | Harness：Claude Agent SDK / LangChain Deep Agents / 托管方案（Claude Managed Agents） | [philschmid.de](https://www.philschmid.de/agent-harness-2026)；[Claude Blog](https://claude.com/blog/building-agents-with-the-claude-agent-sdk) |
| 宽度优先、可并行的研究型任务 | Orchestrator-workers 多智能体（只读子智能体） | [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)；[Cognition](https://cognition.com/blog/multi-agents-working) |
| 角色化多智能体快速原型、Demo | CrewAI（注意 token 开销，上生产时需评估迁移） | [DEV](https://dev.to/lukaszgrochal/i-benchmarked-5-ai-agent-frameworks-heres-what-actually-matters-3ela)；[掘金](https://juejin.cn/post/7698533148759408681) |
| 文档密集型 RAG | LlamaIndex / Haystack / RAGFlow | [掘金](https://juejin.cn/post/7698533148759408681)；[jimmysong.io](https://jimmysong.io/blog/open-source-ai-agent-workflow-comparison/) |
| 业务团队自助、快速验证、带 UI | Dify / Coze（扣子）/ n8n（注意许可证与可视化天花板） | [jimmysong.io](https://jimmysong.io/blog/open-source-ai-agent-workflow-comparison/)；[掘金](https://juejin.cn/post/7698533148759408681) |
| 涉及资金或不可逆操作的生产系统 | 不论用什么框架：确定性控制流 + 校验 + 人工审批 | [HN 48051562](https://hn.algolia.com/api/v1/items/48051562)；[MAP](https://arxiv.org/html/2512.04123v3) |

### Inferences
- 选型更像是“分层组合”，不是挑一个框架：模型 SDK 一层，可选的 agent 抽象一层，运行时（durable、HITL、持久化）一层，可观测与评测一层，协议（MCP/A2A）一层。arXiv 研究里“96% 的高星项目组合使用多个框架”也支持这个判断。
- 对正在学 LangGraph 的团队来说，LangGraph 在“Python + 状态化长流程 + HITL”这个象限仍是社区公认的默认选项。但应同时理解 12-Factor 的原则，避免与框架抽象过度耦合（InfoWorld 的“为变化而设计”）。

### Gaps
- 没有找到基于实证数据的“团队规模/技能 × 框架成功率”研究，映射表属于综合判断，不是统计结论。

---

## 7. 2026 年的关键趋势

### Takeaway
2026 年的主线有六条：
- harness 成为新的抽象层级，“框架/运行时/harness”三分法流行开来；
- 托管智能体（agents-as-a-service）兴起；
- durable execution 成为生产标配；
- MCP、AGENTS.md、A2A 进入 Linux Foundation 的中立治理；
- 可观测性普及，评测仍然滞后；
- 编码智能体的 harness 被泛化为通用智能体底座，多智能体以“单写者”形态有条件回归。

框架层同时在收敛：AutoGen 和 Semantic Kernel 并入 MAF，LangChain 推出 1.0。

### Cited Findings
- **Harness 化**
  - [观点] Phil Schmid（2026-01）。— [philschmid.de](https://www.philschmid.de/agent-harness-2026)
  - [观点] LangChain 的三分法（2025-10）。— [LangChain](https://www.langchain.com/blog/agent-frameworks-runtimes-and-harnesses-oh-my)
  - [证据] BUILD 2026 上 MAF 把 harness 作为核心概念。— [Microsoft DevBlogs](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/)
  - [观点] Anthropic 的长时运行 harness 模式：initializer agent 加增量编码智能体，用笔记和 commit 跨会话传递状态。— [GitHub anthropics/cwc-long-running-agents](https://github.com/anthropics/cwc-long-running-agents)；[Addy Osmani](https://addyosmani.com/blog/long-running-agents/)
- **托管智能体**
  - [证据] Claude Managed Agents 于 2026-04-08 公测，由 Anthropic 托管容器、编排、上下文管理、错误恢复和 tracing；多智能体协作处于 research preview。— [IT Brief](https://itbrief.com.au/story/anthropic-launches-claude-managed-agents-in-public-beta)；[HN 47693047](https://hn.algolia.com/api/v1/items/47693047)
  - [证据，仅标题] OpenAI《Dots: Always-on agents》（2026-09-29，HN 770 分）和《Cloudflare OS: an open platform for agents》（2026-08-05，HN 668 分）表明各平台都在做托管/常驻智能体。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=agents&tags=story&hitsPerPage=40&numericFilters=points%3E250,created_at_i%3E1759276800)
- **Durable execution**
  - [证据，厂商] Temporal 与 OpenAI Agents SDK 的集成于 2026-03-23 GA。— [Temporal](https://temporal.io/blog/announcing-openai-agents-sdk-integration)
  - [证据，官方文档] Pydantic AI 支持 Temporal、DBOS、Prefect、Restate。— [Pydantic](https://pydantic.dev/docs/ai/integrations/durable_execution/overview/index.md)
  - [观点] LangChain 认为 durable execution 是 runtime 的首要能力。— [LangChain](https://www.langchain.com/blog/agent-frameworks-runtimes-and-harnesses-oh-my)
  - [观点] HN 用户 druhinbala（2026-09）认为检查点已基本解决，但崩溃后防止重复副作用仍是难题。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=crewai%20production&tags=comment&hitsPerPage=25&numericFilters=created_at_i%3E1735689600)
- **标准化**
  - [证据] Linux Foundation 于 2025-12-09 成立 Agentic AI Foundation（AAIF），首批项目是 Anthropic MCP、Block goose、OpenAI AGENTS.md。— [InfoQ](https://infoq.com/news/2025/12/agentic-ai-foundation/)
  - [低可信，日期冲突] 有来源称 Google 于 2026-08-20 把 A2A 捐给 AAIF；另有来源称 A2A 在 2026-04 已到 v1.0、有 150 多个支持组织。来源之间无法对齐。— [FlowHunt](https://www.flowhunt.io/blog/agentic-ai-foundation-a2a-mcp-standards/)；[IntuitionLabs](https://intuitionlabs.ai/articles/agentic-ai-foundation-open-standards)
  - [低可信] MCP SDK 月下载量超过 1.1 亿，AGENTS.md 被 6 万多个开源项目使用，数据截至 2026-04。— [IntuitionLabs](https://intuitionlabs.ai/articles/agentic-ai-foundation-open-standards)
  - [证据，仅标题] 《Claude Code now reads AGENTS.md if there is no Claude.md》（2026-09-18，HN 741 分）。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=agents&tags=story&hitsPerPage=40&numericFilters=points%3E250,created_at_i%3E1759276800)
- **评测与可观测性**
  - [证据] 可观测性覆盖 89%，离线评测 52.4%，在线评测 37.3%；人工评审 59.8%，LLM-as-judge 53.3%。— [LangChain 调查](https://www.langchain.com/state-of-agent-engineering)
  - [证据] 75% 的案例没有正式基准集。— [MAP](https://arxiv.org/html/2512.04123v3)
  - [观点] 观测只说明发生了什么，评估才能判断做得对不对。— [掘金](https://juejin.cn/post/7698533148759408681)
- **编码智能体走向通用智能体**
  - [观点] Claude Code SDK 更名为 Agent SDK，理由是给智能体一台电脑。— [Claude Blog](https://claude.com/blog/building-agents-with-the-claude-agent-sdk)
  - [证据] 受访者日常使用的智能体中，编码助手占主导（Claude Code、Cursor、Copilot）。— [LangChain 调查](https://www.langchain.com/state-of-agent-engineering)
  - [证据，仅标题] 《Coding agents have replaced every framework I used》（2026-02-07，HN 375 分、593 条评论），讨论的是编码智能体对一般软件框架的替代，不专指智能体框架。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=agent%20framework&tags=story&numericFilters=points%3E150,created_at_i%3E1735689600)
- **多智能体有条件回归**
  - [观点] Cognition 2026-04 的修正文章。— [Cognition](https://cognition.com/blog/multi-agents-working)
  - [证据，仅标题] Anthropic《We tasked Opus 4.6 using agent teams to build a C Compiler》（2026-02-05，HN 735 分）。— [Anthropic](https://www.anthropic.com/engineering/building-c-compiler)
- **框架收敛与稳定化**
  - [证据] MAF 于 2026-04 GA。— [InfoWorld](https://www.infoworld.com/article/4199575/the-microsoft-agent-framework-wars-are-over-the-real-architecture-decision-starts-now.html)
  - [证据] LangChain/LangGraph 1.0 于 2025-10 发布。— [LangChain](https://www.langchain.com/blog/langchain-langgraph-1dot0)
  - [证据，仅标题] Mastra 1.0 于 2026-01 发布。— [HN Algolia](https://hn.algolia.com/api/v1/search?query=agent%20framework&tags=story&numericFilters=points%3E150,created_at_i%3E1735689600)
- **安全与沙箱**
  - [证据，HN 热度，仅标题] Docker Sandboxes（2026-08，694 分）、Agent Safehouse（2026-03，823 分）。
  - [证据，HN 热度，仅标题] 事故帖：删除生产库（2026-04，860 分）。
  - [证据，HN 热度，仅标题] Show HN《I tested 11 AI frameworks for basic security – none passed》（2026-04）。
  - 来源：[HN Algolia](https://hn.algolia.com/api/v1/search?query=agents&tags=story&hitsPerPage=40&numericFilters=points%3E250,created_at_i%3E1759276800)；[HN 评论检索](https://hn.algolia.com/api/v1/search?query=%22pydantic%20ai%22&tags=comment&hitsPerPage=25&numericFilters=created_at_i%3E1735689600)
- **“Build to delete”与 Bitter Lesson**
  - [观点] 模型变强会淘汰手工控制逻辑，2024 年的复杂流水线如今一个提示就能完成。— [philschmid.de](https://www.philschmid.de/agent-harness-2026)
  - [观点] 与之相对，2026-05 的《control flow》文章主张用更多确定性代码。两者张力仍然存在。— [bearblog](https://bsuh.bearblog.dev/agents-need-control-flow/)

### Inferences
- 2026 年存在两股相反的力量：
  - Bitter Lesson 派主张 harness 尽量轻，把规划交给模型，随模型升级删代码，代表是 Phil Schmid、Vercel 删工具。
  - 确定性派主张控制流写进代码，LLM 只做有界决策，代表是 12-Factor、《control flow》、MAP 的“刻意约束自主性”。
  - 从业者的实际折中是：确定性外层编排加 durable 运行时，内层用轻 harness 让模型自主完成有界子任务，写操作保持单线程。
- 托管 harness（Managed Agents、Dots）可能把“框架之争”进一步变成“自建 vs 托管 vs 锁定”之争。HN 上对锁定的强烈反应显示，开源可换模型的方案（Pydantic AI、LangGraph、Mastra）仍有稳固需求。

### Gaps
- A2A 并入 AAIF 的确切日期与版本状态，各来源说法冲突，需以 Linux Foundation 官方公告为准。
- OpenAI “Dots”、Cloudflare OS 的具体能力只看到标题，未核实细节。
- HarnessTax 的具体数据未获取（页面依赖 JS 加载）。
- 知乎问题《Multi-Agent 是否真的必要？》的高赞回答返回 403，未能读取：[知乎](https://www.zhihu.com/question/2030332404074858123/answer/2033206371584300792)。
