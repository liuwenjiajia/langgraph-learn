# 多智能体协作 / 角色扮演型框架：CrewAI、AutoGen/AG2、MetaGPT(MGX/Atoms)、CAMEL/OWL、AgentScope、Agno（截至 2026-10-21）

> 调研日期：2026-10-21。GitHub 的 star 数、发布版本和最后推送时间都是当天通过 GitHub API（`gh api repos/<org>/<repo>` 和 `/releases`）实时取到的。源链接都指向对应的仓库或 releases 页。
> 标注说明：**[历史]** 表示已不是当前状态的旧信息；**[二手]** 表示来自聚合站、博客或媒体的转述，没有找到官方原始出处；**[未复核]** 表示出自训练知识、本次没有重新核对。

### 速览表（全部为 2026-10-21 的 GitHub API 实测数据）

| 框架 | 仓库 | Stars | 最新版本（日期） | 当前状态 |
|---|---|---|---|---|
| CrewAI | crewAIInc/crewAI | 59,941 | 1.15.28（2026-10-14） | 非常活跃，几乎每周都发版 |
| AutoGen（微软） | microsoft/autogen | 61,504 | python-v0.7.5（2025-09-30） | README 已声明“archived、不再维护”（2026-10-16 修改）。GitHub 的 archived 标志仍是 false |
| Microsoft Agent Framework | microsoft/agent-framework | 14,243 | python-1.22.0（2026-10-15）/ dotnet-1.25.0（2026-10-14） | AutoGen 的官方继任者，1.0 于 2026-04 GA |
| AG2 | ag2ai/ag2 | 5,008 | v1.2.0（2026-10-11） | 活跃。v1.0（2026-07-27）重写为 protocol-driven 框架，旧 API 拆到 ag2-classic |
| MetaGPT | FoundationAgents/MetaGPT | 70,945 | v0.8.2（2025-03-09） | 开源框架基本停滞：最后一次提交在 2026-01-21，团队重心转到商业产品 MGX → Atoms |
| CAMEL | camel-ai/camel | 17,942 | 稳定版 v0.2.90（2026-03-22），预发布 v0.2.91a7（2026-09-03） | 活跃，但仍是 0.x 版本 |
| OWL | camel-ai/owl | 20,154 | 无 GitHub release | 最后一次实质代码提交在 2026-03-18，之后只有自动更新二维码的 commit |
| AgentScope | agentscope-ai/agentscope（原 modelscope/agentscope） | 33,581 | v2.0.10（2026-10-12） | 活跃。2.0 于 2026-05-25 发布（1.0 发布于 2025-08-15） |
| Agno | agno-agi/agno | 42,850 | v3.1.7（2026-10-20） | 非常活跃。3.0 于 2026-08-24 发布（破坏性更新，需要迁移数据库） |

来源：[crewAI](https://github.com/crewAIInc/crewAI/releases)、[autogen](https://github.com/microsoft/autogen/releases)、[agent-framework](https://github.com/microsoft/agent-framework/releases)、[ag2](https://github.com/ag2ai/ag2/releases)、[MetaGPT](https://github.com/FoundationAgents/MetaGPT/releases)、[camel](https://github.com/camel-ai/camel/releases)、[owl](https://github.com/camel-ai/owl/commits/main)、[agentscope](https://github.com/agentscope-ai/agentscope/releases)、[agno](https://github.com/agno-agi/agno/releases)

---

## Q1. CrewAI：核心概念、版本、AMP 平台、与 LangChain 的关系、融资与采用度、最佳场景与弱点

### Takeaway
CrewAI 目前是 1.15.x 版本，处于高频发版阶段。它的核心是两套抽象：**Crews**（agent 由 role/goal/backstory 定义，强调自主协作）和 **Flows**（事件驱动、有状态、可精确控制）。官方现在的推荐用法是“Flow 搭骨架，需要自主协作的步骤里再嵌 Crew”。商业化产品是 CrewAI AMP Suite。融资公开可查的只有 2024 年的 1,800 万美元。“X% Fortune 500 在用”这类数字都是公司自己的说法，而且口径在变。主要弱点集中在调试、token 成本和版本升级带来的破坏。

### Cited Findings
**定位与核心抽象**
- 官方 README 的自我定位：“an open-source Python framework with high-level abstractions and low-level APIs for building production-ready multi-agent workflows”，通过 Crews 实现 agent 的自主协作，通过 Flows 实现事件驱动的精确控制 — [crewAI README](https://github.com/crewAIInc/crewAI)
- **Crews** 是由 AI agent 组成的团队，agent 有自主性，基于角色协作完成任务。特点是 agent 之间自主决策、动态委派任务、角色专业化。**Flows** 是“production-ready, event-driven workflows”，提供执行路径的细粒度控制、任务间安全一致的状态管理、条件分支，并且能和生产环境的 Python 代码干净地集成 — [crewAI README](https://github.com/crewAIInc/crewAI)
- 官方文档对“Crews 还是 Flows”的回答是两者都用：先用 Flow 定义整体结构、状态和逻辑，某个步骤需要自主协作的 agent 团队时，再在这一步里放一个 Crew。文档给的例子：简单自动化 = 单个 Flow 加 Python 任务；复杂研究 = Flow 管状态、Crew 做研究；应用后端 = Flow 处理 API 请求、Crew 生成内容、再由 Flow 写库 — [CrewAI Docs Introduction](https://docs.crewai.com/en/introduction)
- Agent 用 “Role-Goal-Backstory” 来定义：role 是 agent 的专业职能，backstory 补充人设和工作风格 — [CrewAI Docs: Crafting Effective Agents](https://docs.crewai.com/en/guides/agents/crafting-effective-agents)
- Task + Crew 支持 sequential 进程。README 示例章节的标题是“Example of a simple crew with a sequential process”，hierarchical 进程见社区讨论（下文弱点部分） — [crewAI README](https://github.com/crewAIInc/crewAI)

**版本**
- 1.0.0 于 2025-10-20 发布，1.15.0 于 2026-06-25 发布，最新是 1.15.28（2026-10-14）。2026 年 10 月上旬几乎每天一个补丁版本（1.15.25 到 1.15.27 发布于 10-07 至 10-09） — [crewAI releases](https://github.com/crewAIInc/crewAI/releases)

**与 LangChain 的关系**
- 1.0.0 和 1.10.0 版的 README 写着：“built entirely from scratch—completely **independent of LangChain or other agent frameworks**”，还宣称在某个 QA 任务上“executing 5.76x faster”于 LangGraph — [README @1.10.0](https://github.com/crewAIInc/crewAI/blob/1.10.0/README.md)
- 1.15.0（2026-06）的 README 仍有这句话。当前 main 分支的 README 已经重写，不再提 LangChain。当前 `lib/crewai/pyproject.toml` 的依赖里没有任何 langchain 包，主要依赖是 pydantic、openai、instructor、chromadb、mcp、opentelemetry 等 — [crewAI pyproject.toml](https://github.com/crewAIInc/crewAI/blob/main/lib/crewai/pyproject.toml)

**AMP 平台（企业版）**
- 官方名称是 “CrewAI AMP Suite”，面向“organizations that need a commercial control plane around CrewAI”。提供托管部署、tracing 与可观测性、统一控制面、治理、安全、企业集成、7×24 支持，支持 on-premise 和云端部署 — [crewAI README](https://github.com/crewAIInc/crewAI) / [crewai.com/amp](https://crewai.com/amp)

**融资与采用度**
- 2024-10-22 宣布累计融资 1,800 万美元：inception 轮由 boldstart ventures 领投，Series A 由 Insight Partners 领投。同一份公告称，当时开源版本已被“nearly half of the Fortune 500”使用，每月运行 1,000 万以上个 agent — [TFIR](https://tfir.io/ai-multi-agent-platform-crewai-secures-18-million-in-funding/)；[Insight Partners](https://www.insightpartners.com/ideas/crewai-launches-multi-agentic-platform-to-deliver-on-the-promise-of-generative-ai-for-enterprise/)
- [二手] 2026 年的说法：“used by 63% of the Fortune 500”，过去 12 个月约 20 亿次 agentic 执行（另一来源的数字是 14 亿以上）。这些数字来自聚合站对公司说法的转述，没有找到 CrewAI 官方原文 — [Automation Atlas](https://automationatlas.io/answers/crewai-pricing-explained-2026/)；[Panto](https://www.getpanto.ai/blog/crewai-platform-statistics)
- [二手] 截至 2026 年初没有公开披露过后续融资 — [Panto](https://www.getpanto.ai/blog/crewai-platform-statistics)
- 官方自称有 “over 100,000 developers certified” 通过了 learn.crewai.com 的课程 — [crewAI README](https://github.com/crewAIInc/crewAI)

**弱点（社区与评测）**
- [二手] 调试：框架没有原生手段区分故障出在模型、prompt 还是数据源。深度调试、细粒度状态控制、checkpoint、多租户隔离都被评价为短板。还有一种难以察觉的情况：最终输出看起来没问题，但 crew 中途用错了工具 — [Enterprise DNA](https://enterprisedna.co/resources/blog/practitioner-crewai-production)；[AI Agent Rank](https://aiagentrank.io/blog/crewai-review-2026)；[Automation Atlas](https://automationatlas.io/answers/crewai-review-2026/)（三个来源的具体对应关系来自搜索摘要，没有逐条核对）
- [二手] token 成本：开销主要在委派环节，orchestrator 累积的任务状态会随每次 handoff 一起传递。一个从业者估计 4-agent 工作流每个任务消耗 8,000–25,000 token。agent 还可能陷入反复调用同一工具的循环 — [ActiveWizards](https://activewizards.com/blog/crewai-cost-control-token-budgets-model-routing-and-crew-composition-economics/)
- [二手] hierarchical process 有一个未修复的 bug（GitHub issue #4783）。有 Discord 用户反映小版本升级后生产代码出错 — 同上搜索摘要来源（[AI Agent Rank](https://aiagentrank.io/blog/crewai-review-2026)），没有逐条核对
- 从发版节奏看，2026-10 上旬平均每 1–2 天一个补丁版本（见 releases），客观上增加了需要锁版本的压力 — [crewAI releases](https://github.com/crewAIInc/crewAI/releases)

### Inferences
- **优势**：概念最直观。“角色 + 任务 + 团队”接近业务人员对团队分工的理解，上手快。Crews 加 Flows 的双层设计能兼顾自主性和确定性。有商业控制面（AMP），企业采购路径清晰。核心不依赖 LangChain，依赖链相对轻。
- **重点场景**：业务流程自动化，比如调研 → 撰写 → 审校这种内容流水线、销售/营销资料生成、报告生成、客服后台流程。适合角色分工明确、步骤大体线性的“数字员工团队”类应用。官方示例（落地页生成、旅行规划、股票分析、招聘 JD）也属于这一类。
- **弱点**：纯 Crew 的自主协作不确定性高、难调试、token 开销大。生产环境实际上被引导走向“Flow 为主”，这时它和 LangGraph 这类图编排框架的差异在缩小。发版频繁，需要严格锁定版本。
- **适合的团队**：想快速做出多角色业务自动化 PoC 的应用团队，或者希望有商业支持和托管控制面的企业团队。需要强确定性、复杂状态机或精细调试的团队，应该以 Flows 为主，或者评估其他图编排框架。

### Gaps
- 没有找到 CrewAI 官方原文里的“63% Fortune 500”和“20 亿次执行”。数字在 2024 年（近半数）到 2026 年（63%）之间有变化，口径不明。
- 没有找到 2024-10 之后的融资公告，也没有 AMP 的公开定价（只看到聚合站的说法）。
- 没有找到 Hacker News 上专门讨论 CrewAI 的高质量帖子。社区批评主要来自博客和评测站，可信度一般。

---

## Q2. AutoGen / AG2：AutoGen 发生了什么，AG2 是谁在维护、当前状态如何，适用场景

### Takeaway
微软的 AutoGen 走了四步：0.2 经典版 → 0.4 重写为分层架构（Core / AgentChat / Extensions）→ 2025-10 进入维护模式 → 2026-10-16 在 README 中声明“archived、不再维护、不提供安全修复”。官方继任者是 **Microsoft Agent Framework（MAF）**，它合并了 Semantic Kernel 和 AutoGen 的编排模式，1.0 于 2026-04-03 GA。**AG2** 是 AutoGen 原作者（Chi Wang、Qingyun Wu）在 2024 年 11 月 fork 出来的社区版。2026-07 的 v1.0 又做了一次不兼容的重写：新框架用 `import ag2`，旧的 `ConversableAgent`/`GroupChat` API 拆到 “AG2 Classic”。今天说的 “AutoGen” 实际上指向三条不同的代码线，选型时要分清。

### Cited Findings
**微软 AutoGen**
- 当前 README 的标题带有 “Archived” 徽章，正文写着：“This project has been archived and is no longer actively maintained by Microsoft… Microsoft is not providing bug fixes, security fixes, new features, or support… we continue to advise against production use.” 新用户被引导去用 MAF，老用户按迁移指南迁移 — [microsoft/autogen README](https://github.com/microsoft/autogen)
- README 的修改时间线：2025-10-02 “Update README with maintenance and resource information”（进入维护模式），2026-04-06 “Update maintenance mode banner”，2026-10-16 “docs: clarify AutoGen is archived and no longer maintained”。截至 2026-10-21，GitHub 仓库的 `archived` 标志仍是 false — [README commit history](https://github.com/microsoft/autogen/commits/main/README.md)（GitHub API 实测）
- 最后一个正式版本是 python-v0.7.5（2025-09-30） — [autogen releases](https://github.com/microsoft/autogen/releases)
- 0.4 及以后的版本安装方式是 `pip install -U "autogen-agentchat" "autogen-ext[openai]"`，体现了 AgentChat 和 Extensions 分包的结构 — [microsoft/autogen README](https://github.com/microsoft/autogen)
- [二手] 微软在 v0.4 中把 AutoGen 重建为 event-driven、actor-based 的架构，而 AG2 延续了 0.2 时代基于对话的 API — [blckalpaca: AutoGen vs AG2](https://blckalpaca.at/en/knowledge-base/ai-agents/ai-agent-frameworks-comparison/autogen-vs-ag2)；[aiwiki: AG2](https://aiwiki.ai/wiki/ag2)
- AutoGen 的原始论文是 arXiv 2308.08155，AG2 README 仍引用它作为 “Cite paper” — [ag2 README](https://github.com/ag2ai/ag2)

**Microsoft Agent Framework（继任者）**
- 2026-04-03 宣布 1.0（.NET 与 Python），定位为 production-ready，承诺 API 稳定和长期支持。它把 “Semantic Kernel 的企业级基础” 和 “AutoGen 的创新编排” 合进一个 SDK。1.0 稳定版包括：多模型连接器（Foundry/Azure OpenAI/OpenAI/Claude/Bedrock/Gemini/Ollama）、middleware、可插拔的 memory/context provider、带 checkpoint 的图工作流、多 agent 编排（sequential、concurrent、handoff、group chat、Magentic-One）、YAML 声明式 agent、MCP、A2A。附带 AutoGen 和 SK 的迁移助手 — [MAF 1.0 博客](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- 2026-02-19 发布 RC 版 — [Foundry Blog: MAF RC](https://devblogs.microsoft.com/foundry/microsoft-agent-framework-reaches-release-candidate/)
- 当前版本是 python-1.22.0（2026-10-15）和 dotnet-1.25.0（2026-10-14），14.2k stars — [agent-framework releases](https://github.com/microsoft/agent-framework/releases)
- 官方迁移指南 — [AutoGen → MAF migration guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/)

**AG2**
- [二手] 2024 年 9 月，AutoGen 项目负责人 Chi Wang 和学术合作者 Qingyun Wu 等原作者离开 Microsoft Research。2024 年 11 月成立独立组织 AG2AI，基于 AutoGen 0.2 代码 fork 出 AG2，采用 Apache 2.0 许可，并继承了 `autogen`/`pyautogen` 的 PyPI 包名和 Discord 社区。动机据说是 “move faster… without corporate constraints” 和建立更中立的多组织贡献空间 — [aiwiki: AG2](https://aiwiki.ai/wiki/ag2)；[Atlan: What is AutoGen](https://atlan.com/know/ai-agent/what-is-autogen/)
- 当前 README 称项目由 “a dynamic group of volunteers from several organizations” 维护，项目管理员是 Chi Wang 和 Qingyun Wu。自我定位是 “AG2: Open-Source AgentOS for AI Agents” — [ag2 README](https://github.com/ag2ai/ag2)
- **v1.0.0（2026-07-27）**：在 v0.12 起以 `autogen.beta` 名义开发的 protocol-driven 框架成为主线，导入名改为 `import ag2`，本仓库不再提供 `autogen` 导入名。核心类从 `ConversableAgent` 变为 `Agent`，多 agent 编排从 GroupChat/swarm/nested chat 改为 **Network（hub + channels）**。官方明确说 “v1.0 is **not** a drop-in upgrade”，并提供 group chat 迁移指南。全异步设计（`await agent.ask(...)`） — [AG2 v1.0.0 release](https://github.com/ag2ai/ag2/releases/tag/v1.0.0)；[ag2 README](https://github.com/ag2ai/ag2)
- **AG2 Classic**：旧 API（`ConversableAgent`、`AssistantAgent`、`UserProxyAgent`、`GroupChat`、swarm 等）搬到 [ag2ai/ag2-classic](https://github.com/ag2ai/ag2-classic)，文档在 classic.docs.ag2.ai，通过 `pip install ag2-classic` 或 `pip install autogen` 安装。README 说它 “still maintained… nothing you have built stops working”，release notes 则把它标为 “maintenance mode”，只接收安全修复和关键 bug 修复 — [ag2 README](https://github.com/ag2ai/ag2)；[v1.0.0 release](https://github.com/ag2ai/ag2/releases/tag/v1.0.0)
- ag2-classic 仓库只有 3 个 star，最后推送时间是 2026-07-08（GitHub API 实测）。主仓库 ag2ai/ag2 有 5,008 stars，最新版本 v1.2.0（2026-10-11），v1.0.x 到 v1.2.0 期间大约每 1–2 周发一个版本 — [ag2 releases](https://github.com/ag2ai/ag2/releases)
- AG2 还推出了基于 v1.0 引擎的开源助手 ag2-assistant（聊天、定时任务、工作目录、生成式 UI、语音、实时事件流检查面板） — [v1.0.0 release](https://github.com/ag2ai/ag2/releases/tag/v1.0.0)

### Inferences
- **优势（历史上）**：AutoGen 开创了“多 agent 对话即编程”的范式（ConversableAgent + GroupChat + UserProxy 执行代码），特别适合研究原型、代码生成与执行循环、人在回路的对话式问题求解。Magentic-One 等编排模式已经进入 MAF 1.0。
- **重点场景**：对话式多 agent 研究和实验（辩论、评审、协商）、写代码 + 执行 + 反馈修正的循环、人机混合决策。微软技术栈的企业生产场景应该直接用 MAF，不再用 AutoGen。
- **弱点**：品牌和代码线严重分裂。`pip install autogen` 装到的是 AG2 Classic，`autogen-agentchat` 是微软已归档的 0.4+ 版本，`ag2` 是全新的 v1.0。教程和示例代码很容易混用。微软 AutoGen 已不再提供安全修复，官方不建议用于生产。AG2 两年内经历了两次不兼容的变化（fork 和 v1.0 重写），社区体量（约 5k stars）远小于原仓库。
- **适合的团队**：新项目里，微软/Azure/.NET 生态的企业团队选 MAF。有大量 AutoGen 0.2 老代码、想保持对话式范式的研究型团队，可以锁定 AG2 Classic，或者评估迁移到 AG2 v1.0。不建议新的生产项目再选微软 AutoGen。

### Gaps
- 没有找到 Microsoft 关于 AutoGen 进入维护模式的独立公告原文。时间线依据 README 的 commit 历史。有二手来源称 AutoGen 将 “community-managed”，与当前 README 的 “archived” 说法不一致，以当前 README 为准。
- 没有找到 AG2 的融资、商业主体或大企业用户信息。
- AG2 v1.0 Network（hub + channels）的设计细节和 benchmark 没有深入核对。

---

## Q3. MetaGPT 与 MGX（现更名 Atoms）：SOP 驱动的“软件公司”式多智能体，当前活跃度

### Takeaway
MetaGPT 的核心思想是 `Code = SOP(Team)`：把软件公司的标准作业流程（SOP）固化下来，交给产品经理、架构师、项目经理、工程师等 LLM 角色执行，一句需求就能产出 PRD、设计、API、代码。开源框架基本停在 v0.8.2（2025-03），2026 年只有零星提交。团队（DeepWisdom）把重心放在商业产品 MGX 上，MGX 于 2026-01-13 更名为 **Atoms**，定位是面向非程序员的多 agent “Vibe Coding/Vibe Business” 产品。

### Cited Findings
- README 核心理念：MetaGPT 输入一句需求，输出 user stories、竞品分析、需求、数据结构、API、文档等；内部有产品经理、架构师、项目经理、工程师等角色，“provides the entire process of a software company along with carefully orchestrated SOPs”，`Code = SOP(Team)` 是核心哲学 — [MetaGPT README](https://github.com/FoundationAgents/MetaGPT)
- README 的安装要求是 Python ≥3.9 且 <3.12，示例配置里的默认模型还是 `gpt-4-turbo` — [MetaGPT README](https://github.com/FoundationAgents/MetaGPT)
- README 的 News 停在 2025-03：2025-02-19 发布 MGX（MetaGPT X），称其为 “the world's first AI agent development team”；2025-03 拿到 ProductHunt 日榜和周榜第一；2025-02 发布 SPO、AOT 论文；AFlow 被 ICLR 2025 接收为 oral（top 1.8%） — [MetaGPT README](https://github.com/FoundationAgents/MetaGPT)
- 最后一个 release 是 v0.8.2（2025-03-09），上一个是 v0.8.0（2024-03-29，引入 Data Interpreter 和 RAG）。最近三次提交分别在 2025-10-04（改 README）、2025-11-12（Windows Terminal 支持）、2026-01-21（合并 PR），之后没有新提交。仓库有 70,945 stars，是本组 star 最多的项目 — [MetaGPT releases](https://github.com/FoundationAgents/MetaGPT/releases)（GitHub API 实测）
- [未复核] MetaGPT 论文为 arXiv 2308.00352（ICLR 2024） — [arXiv](https://arxiv.org/abs/2308.00352)
- **MGX → Atoms**：2026-01-13 发布新一代 MGX 并更名为 Atoms，理由是 “MGX” 对英语用户不好发音。Atoms 定位为让非程序员搭建并运营能赚钱的产品的多 agent Vibe Coding 产品，内置登录、数据库、鉴权、部署、Stripe 支付，有专门负责调研（Iris）、SEO（Sarah）的 agent，以及产品经理、架构师、工程师等角色。公司自称效果优于同成本的 Lovable 和 Replit — [36Kr（2026-01-15）](https://eu.36kr.com/zh/p/3640426144812417)
- [公司自述] MGX 上线一个月就有约 50 万注册用户、100 万美元 ARR，没有付费推广。2025-09 月访问量约 120 万，每天生成 1 万多个应用。2025 年上半年 DeepWisdom 完成两轮共约 2.2 亿元人民币融资，投资方有蚂蚁集团、凯辉、锦秋、百度风投、概念资本 — [36Kr](https://eu.36kr.com/zh/p/3640426144812417)；[CB Insights: DeepWisdom](https://www.cbinsights.com/company/deep-wisdom)
- [二手] 2026-06 的报道称 Atoms 开始进入海外科技媒体视野，内置产品经理、设计师、架构师、工程师、营销等 agent，还能做 SEO 和投放广告 — [钛媒体](https://www.tmtpost.com/agent/ai-article?id=18256)
- FoundationAgents 组织在 GitHub 上的总 star 数超过 15 万（2026-01 报道） — [36Kr](https://eu.36kr.com/zh/p/3640426144812417)

### Inferences
- **优势**：SOP 的结构化流程（角色按文档化的中间产物交接，而不是自由聊天）在“需求 → 设计 → 代码”这类流程固定的任务上减少了多 agent 之间的混乱。它是“用组织流程约束 LLM 协作”最早、最有影响力的范式，学术衍生成果（AFlow、SPO、AOT、Data Interpreter）很丰富。
- **重点场景**：从一句需求生成软件项目原型和配套文档、学术研究里的 SOP 化 agent 协作和自动 workflow 搜索（AFlow）。商业产品 Atoms 面向非技术用户“一句话建站并运营”。
- **弱点**：开源框架维护明显放缓。依赖版本陈旧（Python <3.12、默认 gpt-4-turbo），很可能跟不上新模型和新协议（MCP、A2A）。固定的软件公司 SOP 不适合通用业务。生成的代码通常只到原型级别。团队重心已经转向闭源商业产品。
- **适合的团队**：研究多 agent SOP 范式的学术或研究团队，或者想借鉴其设计思路的团队。不建议作为 2026 年新生产系统的底座。想要“AI 软件团队”成品体验的非技术用户可以直接用 Atoms。

### Gaps
- 没有找到 MetaGPT 官方对开源路线的公开说明（比如是否进入维护模式）。
- 没有找到 Atoms 用户数和收入的独立验证，现有数字都是公司说法。
- MetaGPT 论文的录用信息本次没有重新核对。

---

## Q4. CAMEL / OWL：角色扮演 agent 社会、大规模模拟、OWL 通用任务自动化（GAIA），当前状态

### Takeaway
CAMEL 是最早的“角色扮演多 agent”框架之一，自我定位是一个以“寻找 agent 的 scaling law”为目标的研究社区。它的特色是 agent 社会（RolePlaying、Workforce）、百万级 agent 社会模拟（OASIS）、合成数据和环境。OWL 基于 CAMEL Workforce，2025 年在 GAIA 上以 69.09% 拿到开源框架第一，并被 NeurIPS 2025 接收。到 2026 年，OWL 仓库的代码已基本不再更新，CAMEL 主库仍在活跃但还停在 0.2.x。团队的商业化方向是 Eigent（开源的“Cowork 桌面”产品）。

### Cited Findings
**CAMEL**
- 自我定位：“CAMEL is an open-source community dedicated to finding the scaling laws of agents”。他们认为大规模研究 agent 能揭示 agent 的行为、能力和风险 — [CAMEL README](https://github.com/camel-ai/camel)
- 四条设计原则：Evolvability、Scalability（“designed to support systems with millions of agents”）、Statefulness（有状态记忆，支持多步交互）、Code-as-Prompt。宣称可以模拟最多 100 万个 agent 来研究涌现行为和 scaling law — [CAMEL README](https://github.com/camel-ai/camel)
- 关键模块包括 Agent Societies（RolePlaying、Workforce 等多 agent 协作组件）、Workforce（`camel/societies/workforce`），相关项目有 OASIS、CRAB、Loong，商业产品是 Eigent。项目自称是有 100 多名研究者的社区研究团体，联系邮箱是 eigent.ai 域名 — [CAMEL README](https://github.com/camel-ai/camel)
- 原始论文是 “CAMEL: Communicative Agents for ‘Mind’ Exploration of Large Language Model Society”，同时开放了 AI Society 等角色扮演对话数据集 — [CAMEL README](https://github.com/camel-ai/camel)；[未复核：发表于 NeurIPS 2023，arXiv 2303.17760](https://arxiv.org/abs/2303.17760)
- 版本：稳定版 v0.2.90（2026-03-22），之后只有预发布 v0.2.91a4 到 a7（2026-04 至 2026-09-03）。仓库最后推送时间 2026-10-19，17,942 stars — [camel releases](https://github.com/camel-ai/camel/releases)（GitHub API 实测）
- **OASIS**：论文 “OASIS: Open Agent Social Interaction Simulations with One Million Agents”（arXiv 2411.11581，作者来自上海 AI Lab、牛津、KAUST 等）。基于真实社交平台机制（动态关系网络、关注、评论、推荐系统）模拟最多 100 万用户，复现了 X 和 Reddit 上的信息传播、群体极化、从众效应，发现 agent 规模越大，群体动态越强、观点越多样。agent 可执行 23 种动作 — [arXiv 2411.11581](https://arxiv.org/abs/2411.11581)；[OASIS 文档](https://docs.oasis.camel-ai.org/introduction.md)

**OWL**
- 全称 “Optimized Workforce Learning for General Multi-Agent Assistance in Real-World Task Automation” — [OWL README](https://github.com/camel-ai/owl)
- GAIA 成绩：2025-03-03 拿到 58.18 分，开源框架第一；2025-04-18 提升到 69.09%，仍是开源框架第一。复现需要切到 `gaia58.18` 或 `gaia69` 分支，其中包含为 GAIA 定制的 CAMEL 版本（README 原话是 “enhanced toolkits with improved stability specifically optimized for the GAIA benchmark compared to the standard CAMEL installation”） — [OWL README](https://github.com/camel-ai/owl)
- 2025-05-27 发布技术报告（arXiv 2505.23885，讲 workforce 框架和 optimized workforce learning 训练方法），2025-07-21 开源训练数据和模型 checkpoint，2025-09-22 被 NeurIPS 2025 接收 — [OWL README](https://github.com/camel-ai/owl)；[arXiv 2505.23885](https://arxiv.org/abs/2505.23885)
- README 说 “For optimal performance, we strongly recommend using OpenAI models (GPT-4 or later)”，使用其他模型时复杂任务的表现可能明显下降 — [OWL README](https://github.com/camel-ai/owl)
- 2025-03 集中加入了 MCPToolkit、浏览器 toolkit（Chrome/Edge/Chromium）、终端、文件写入、多种搜索（Bing、百度、博查、SearxNG）、Web UI 等 — [OWL README](https://github.com/camel-ai/owl)
- 活跃度：最后一次实质代码提交是 2026-03-18（“Add run_gemini.py”），2026-10 的提交全部是 “Update WeChat QR code via QR Code Updater” 这类自动提交。OWL 没有 GitHub release。20,154 stars — [owl commits](https://github.com/camel-ai/owl/commits/main)（GitHub API 实测）

**Eigent（商业化方向）**
- eigent-ai/eigent 仓库的描述是 “The Open Source Cowork Desktop - Local and Free Alternative to Claude Cowork and Codex”，15,626 stars，2026-10-20 仍在推送。CAMEL README 称 Eigent 为 “The World First Multi-agent Workforce” — [eigent repo](https://github.com/eigent-ai/eigent)；[CAMEL README](https://github.com/camel-ai/camel)

### Inferences
- **优势**：学术基础最深（角色扮演、agent 社会、百万级模拟、合成数据）。模块覆盖 agent、society、环境、数据生成、benchmark。OWL 证明了 Workforce 式多 agent 在通用助理任务（GAIA）上的效果。
- **重点场景**：（1）多 agent 行为研究和社会模拟，比如舆论传播、市场或政策推演（OASIS）；（2）用角色扮演生成指令或对话合成数据；（3）通用任务自动化研究，浏览器、搜索、文件、终端等多工具协作（OWL、Workforce）；（4）agent 方向的教学和论文复现。
- **弱点**：至今仍是 0.2.x，没有 1.0 稳定承诺，2026 年的新版本都是 alpha。OWL 的 GAIA 高分依赖定制分支和 OpenAI 等强模型，标准安装达不到。OWL 仓库已基本停更，精力转向 Eigent 产品。研究导向重于工程化（部署、可观测性、多租户等能力的公开证据较少）。
- **适合的团队**：高校和研究机构、做 agent 社会模拟或合成数据的团队、要复现 GAIA 类通用 agent 的团队。不太适合需要长期 API 稳定性的企业生产团队。

### Gaps
- 没有找到 CAMEL-AI / Eigent 的融资信息。
- 没有找到 CAMEL 在企业生产环境落地的可靠案例。
- 没有核对 OWL 69.09% 之后 GAIA 开源榜单的最新排名（2026 年可能已被超过）。

---

## Q5. AgentScope（阿里通义 / ModelScope）：1.0 特性、2.0 现状、中文生态落地

### Takeaway
AgentScope 由阿里通义实验室团队开发，仓库从 modelscope 迁到 agentscope-ai 组织。**1.0（2025-08）** 的主打是 ReAct agent、异步和并行工具调用、实时介入（real-time steering），再加上配套的 Runtime（沙箱、部署）和 Studio（可视化、评估）。**当前主线是 2.0（2026-05-25 发布，最新 v2.0.10）**，设计理念转为“少约束、靠模型能力”，提供 Agent SDK 和开箱即用的 Agent Service（多租户、IM 渠道、RAG 服务、MCP/Skill Hub、定时任务）。2.0 逐步补齐了 Agent Team、Pipeline、TeamPipeline、SOP、A2A、实时语音。中文生态方面，它和阿里云百炼、ACS 容器服务、钉钉、飞书、DashScope/Qwen 深度集成，还衍生了 CoPaw 个人 agent 工作站、AgentScope Java 等项目。

### Cited Findings
**1.0（历史版本，2025-08 发布）**
- v1.0.0 发布于 2025-08-15 — [agentscope releases](https://github.com/agentscope-ai/agentscope/releases)
- 1.0 论文（arXiv 2508.16279，2025-08-22 提交）：agent 行为以 ReAct 范式为基础，系统性的异步设计提升执行效率，丰富了人-agent 和 agent-agent 的交互模式，内置若干面向实际场景的 agent，提供可扩展的评估模块和可视化 Studio 来追踪长轨迹应用，用 runtime 沙箱保证安全执行并支持快速部署 — [arXiv 2508.16279](https://arxiv.org/abs/2508.16279)
- [二手] 论文正文提到原生支持 “parallel tool calls, asynchronous executions, and real-time steering”。仓库特性表也列出了 agent 层的实时介入中断和自定义处理。AgentScope Runtime（沙箱化工具执行）和 AgentScope Studio（可视化开发与监控、agent 评估）于 2025-09 开源 — [arXiv PDF](https://arxiv.org/pdf/2508.16279)；[ai-bot.cn: AgentScope 1.0](https://ai-bot.cn/agentscope-1-0/)
- 阿里云开发者社区（2025-10-16）称 1.0 用“核心框架 + 运行时 + 可视化工具”三层架构支持构建、部署和监控，具备实时干预、高效工具调用和智能上下文管理 — [阿里云开发者社区](https://developer.aliyun.com/article/1685274)
- 品玩（2025-09-02）援引通义官方的说法：纯 Python 编程、多模型重试与容错、多模态支持、基于 Actor 的分布式机制（集中式编写分布式工作流、自动优化并行）、覆盖开发/部署/监控全生命周期 — [品玩](https://www.pingwest.com/w/307306)
- 早期论文 “AgentScope: A Flexible yet Robust Multi-Agent Platform”（arXiv 2402.14034，2024） — [AgentScope README](https://github.com/agentscope-ai/agentscope)

**2.0（当前版本，2026-05-25 发布）**
- 自我定位：“AgentScope 2.0 is a production-ready, easy-to-use agent framework with essential abstractions that keep up with rising model capability… leverages the models' reasoning and tool use abilities rather than constraining them with strict prompts and opinionated orchestrations.” 仓库描述是 “Build and run agents you can see, understand and trust.” — [AgentScope README](https://github.com/agentscope-ai/agentscope)
- SDK 构件：ReAct（结构化输出、**实时中断与恢复**、顺序或并发的批量工具执行）、Toolkit（Python 工具、MCP、Skills，内置 shell、文件编辑、搜索等 coding 工具和 task/plan 工具）、Model（OpenAI、Anthropic、Gemini、DashScope、DeepSeek、Moonshot、火山引擎、xAI、Ollama）、Context（自动压缩、工具结果 offload、上下文注入）、Event System（统一事件总线，把推理、工具调用、多模态内容流式推给前端）、Permission & HITL、Middleware、Memory（ReMe、Mem0）、Workspace/Sandbox（本地、Docker、Apple Container、Bubblewrap、E2B、OpenSandbox、Daytona、K8s） — [AgentScope README](https://github.com/agentscope-ai/agentscope)
- Agent Service：基于 FastAPI 的后端加预置 Web UI，能力包括多租户和多会话隔离、Agent Team（leader-worker 编排和任务规划）、Channels（飞书、钉钉、Discord）、RAG 服务、MCP & Skill Hub（GitHub MCP Registry、ClawHub）、组织级资源共享、SQL/NoSQL 持久化、定时任务和后台任务 offload — [AgentScope README](https://github.com/agentscope-ai/agentscope)
- 2.0.0 的 release notes 写明 “temporarily deprecate evaluate/module/rag/tts/realtime modules pending refactor”，即 2.0 初版暂时移除了评估、RAG、TTS、实时等模块，并重构了 Msg、tool、MCP（统一为 `MCPClient`）、model、tracing 等核心模块 — [v2.0.0 release](https://github.com/agentscope-ai/agentscope/releases/tag/v2.0.0)
- 2.0 之后的补齐时间线：2026-06 Agent Team、RAG、分布式多租户 RAG 服务、Mem0、Agentic Memory；2026-07 ReMe、K8s/OpenSandbox/Daytona 沙箱；2026-08 Pipeline、Console、飞书/Discord/钉钉渠道、MCP & Skill Hub；2026-09 A2A（`A2AAgent`）、实时语音 agent（DashScope、OpenAI、Gemini、xAI 的 realtime API）、模型路由 middleware、TeamPipeline（leader 委派给成员）、SOP（实验性）；2026-10 Agent Service 支持基于 WebRTC 的实时语音对话（实验性） — [AgentScope NEWS.md](https://github.com/agentscope-ai/agentscope/blob/main/docs/NEWS.md)
- 需要 Python ≥3.11。最新版本 v2.0.10（2026-10-12），33,581 stars — [AgentScope README](https://github.com/agentscope-ai/agentscope)；[releases](https://github.com/agentscope-ai/agentscope/releases)

**中文生态与落地**
- 阿里云帮助中心称，把 AgentScope 部署在百炼应用平台、阿里云容器计算服务（ACS）上“已经成为了主流的部署模式”（阿里云自己的说法） — [阿里云 ACS 文档](https://help.aliyun.com/zh/cs/user-guide/use-agentscope-to-quickly-build-ai-agent-in-acs-cluster)
- 2025-11 通义开源了基于 AgentScope 的 Alias-Agent 和 Data-Juicer Agent，并集成 ReMe 长期记忆 — [格隆汇](https://m.gelonghui.com/live/2154482)
- 2026-03-30 AgentScope 团队发布 CoPaw v1.0.0，这是一个个人 AI agent 工作站，配套 CoPaw-Flash-9B（基于 Qwen3.5-9B 的 agentic 微调小模型）。支持 Mac、Windows、Linux 本地一键安装，安全上做了分层防御（工具守卫、文件防护、技能扫描）。面向企业协作的 HiClaw 也加入了 AgentScope 生态 — [凤凰网/IT之家](https://tech.ifeng.com/c/8rwkr4YnMtr)；[品玩](https://www.pingwest.com/w/312624)；[NYU Shanghai RITS](https://rits.shanghai.nyu.edu/ai/copaw-flash-9b-alibabas-agentic-fine-tune-of-qwen3-5-9b/)
- 另有 AgentScope Java v1.0，面向 Java 开发者构建企业级 agentic 应用 — [阿里云开发者社区](https://developer.aliyun.com/article/1691914)
- 社区渠道是 Discord 和钉钉群，README 提供中文主页（README_zh.md） — [AgentScope README](https://github.com/agentscope-ai/agentscope)

### Inferences
- **优势**：本组里工程化最全面的开源方案之一。从 SDK 到可运行的多租户服务、IM 渠道、沙箱、权限和 HITL 都有现成实现。对国产模型（Qwen/DashScope、DeepSeek、Moonshot、火山引擎、MiniMax）和国内 IM（钉钉、飞书）原生支持，和阿里云（百炼、ACS）结合得好。实时中断与恢复、事件流、权限体系适合做面向终端用户的交互式 agent 产品。同时有 Python 和 Java 两套实现。
- **重点场景**：中国企业落地 agent 应用（客服、内部助理、接入钉钉或飞书的办公 agent）、需要沙箱执行代码或工具的 coding/数据 agent、需要多租户托管的 agent 平台、实时语音 agent、阿里云上的部署。
- **弱点**：1.0 到 2.0 是大规模不兼容重构（Msg、tool、MCP、model 都改了），2.0 初版还暂时砍掉了评估、RAG、实时等模块，说明 API 稳定性有风险。很多新特性仍标为 Experimental（SOP、实时语音）。英文社区的讨论度和第三方案例比 CrewAI、LangGraph 少。2.0 弱化了原先“多 agent 平台”的强编排定位，转向“单 agent 能力 + leader-worker 团队”，想要复杂多 agent 编排的用户需要重新评估。
- **适合的团队**：国内团队，尤其是用通义或阿里云、需要对接钉钉或飞书的团队；需要一套开源 agent 平台（服务、UI、沙箱、多租户）直接改造的团队；需要 Java 实现的企业团队。

### Gaps
- 没有找到 AgentScope Runtime 和 Studio 在 2.0 下的当前状态（是否独立维护、是否适配 2.0）。
- 没有找到具体的企业客户名单和用户规模。阿里云“主流部署模式”的说法缺少第三方数据。
- 知乎、掘金、InfoQ 中文上的开发者评价没有系统检索到。

---

## Q6. Agno（原 Phidata）：性能宣称、多模态、AgentOS 运行时、Teams，当前状态与场景

### Takeaway
Agno 由 Phidata 在 2025 年初更名而来（v1.0.0 于 2025-01-30 发布），现在的定位已经从“轻量高性能 agent 框架”升级为“agent 平台的框架 + 运行时 + 管理 UI”（SDK + AgentOS + AgentOS UI）。当前是 3.x（3.0 于 2026-08-24 发布，需要迁移数据库）。它的“实例化快几百倍、内存小几十倍”宣传是微基准：只测 Python 对象构建，不包括 LLM 调用。独立复测确认实例化确实快几百倍，但内存优势比官方说的小，而且与端到端延迟基本无关。

### Cited Findings
**定位与功能**
- README 的自我定位是 “Agno is a framework and runtime for agent platforms”：用 Agno SDK 构建，用 AgentOS runtime 运行，用 AgentOS UI 管理。强调 “own your agent stack”，数据、记忆、安全（基于 JWT 的 RBAC）都在自己手里，并把使用数据和模拟变成学习闭环 — [Agno README](https://github.com/agno-agi/agno)
- 功能清单：50 多个生产 API 端点（SSE 和 websocket）；session、memory、knowledge、trace 存在自己的数据库里；100 多个集成 toolkit；Context Providers（Slack、Drive、wiki、MCP）；人工审批（暂停 run、拦截需要管理员批准的工具）；OpenTelemetry tracing 和审计日志；JWT RBAC 加多用户多租户隔离；Interfaces（Slack、Telegram、WhatsApp、Discord、AG-UI、A2A）；cron 调度和后台任务；提供 Railway、Docker、AWS、GCP、Azure、Fly、Render、Modal、Helm 部署模板 — [Agno README](https://github.com/agno-agi/agno)
- README 首推的上手方式是把一段 prompt 交给 coding agent（Claude Code、Cursor、Codex），让它克隆 agentos 模板并按指南完成部署。官方文档还提供了 MCP server（docs.agno.com/mcp）和 llms-full.txt — [Agno README](https://github.com/agno-agi/agno)
- 遥测：每次 agent run 发送一个事件（不含 prompt 和输出），可以用 `AGNO_TELEMETRY=false` 关闭 — [Agno README](https://github.com/agno-agi/agno)

**版本**
- v1.0.0（2025-01-30，对应 Phidata 更名为 Agno 的时间段）→ v2.0.0（2025-09-09）→ v3.0.0（2026-08-24）→ 当前 v3.1.7（2026-10-20），几乎每天发版。42,850 stars — [agno releases](https://github.com/agno-agi/agno/releases)（GitHub API 实测）
- v3.0 是破坏性版本，必须先做数据库迁移才能上线：run 从 sessions 表里的 JSON blob 改为独立的 `agno_runs` 表（写放大从 O(N²) 降到 O(N)）。新增工具结果 offload（超过 16,000 字符写入 AgentFS）、媒体 offload 到 S3/GCS、CodeMode（用一个可编程的 IPython kernel 替代大量工具 schema）、AgentOS 持久化后台执行队列（崩溃或重启后不丢失、可多副本执行、支持幂等键）、Studio 3.0 受治理的组件目录（draft 发布后才生效）、更细的按用户隔离（metrics、调度、eval、knowledge、17 种向量库） — [Agno v3.0.0 release](https://github.com/agno-agi/agno/releases/tag/v3.0.0)

**性能宣称与独立复测**
- [二手：搜索摘要转述官方文档] 官方性能页称 agent 实例化约 3μs、内存约 6.6 KiB，2025-10 在 Apple M4 MacBook Pro 上跑 1,000 次测得，并称比 LangGraph 快约 529 倍、比 CrewAI 快约 70 倍 — [Agno Docs: Performance](https://docs.agno.com/get-started/performance)
- [历史] 1.1.x 时期 PyPI README 写的是约 2μs 和约 3.75 KiB — [PyPI agno 1.1.2](https://pypi.org/project/agno/1.1.2)
- 官方文档里的 PerformanceEval 说明：实例化测试只构造对象，不调用模型；涉及响应的测试会调用 OpenAI 模型，延迟包含网络和服务商的波动 — [Agno Docs: performance evals](https://docs.agno.com/performance)
- [二手] 独立复测（2026-07，用 Agno 2.8.2 等当时的最新版本）：实例化仍比 LangGraph 快约 305 倍，但内存差距只有约 5.8 倍，不是文档说的 24 倍。作者指出这是只测 Python 对象构建的微基准，不能说明 agent 响应 prompt 的速度 — [Towards AI](https://pub.towardsai.net/agno-says-it-builds-agents-529-faster-than-langgraph-i-measured-what-that-actually-buys-you-a3c9cb6c198a)
- [二手、可信度低] 另一篇对比文章称在查询（实际运行）阶段，LangGraph 平均反而快约 3.5 倍 — [AI in Plain English](https://ai.plainenglish.io/agno-vs-langgraph-which-ai-framework-wins-on-speed-dc9290a55389)
- [未核实] 搜索摘要提到一篇 2026-08 的官方 benchmark 文章（Agno 2.8.7 中位数 3.2µs / 5.2KiB，LangGraph 1.1ms，CrewAI 18.3ms），但抓取该 URL 只拿到博客索引页，无法确认 — [agno.com articles](https://www.agno.com/articles/benchmarking-agno-against-other-frameworks)

**融资**
- [二手、有冲突] Caplight 记录的最近一轮是 2024-08-29 的种子轮，累计 540 万美元。Startups.fm 的数字是 300 万美元。有来源提到投资方包括 GreatPoint Ventures、Zero Prime Ventures、Surface Ventures — [Caplight](https://www.caplight.com/company/agno)；[CB Insights: Phidata](https://www.cbinsights.com/company/phidata)；[Startups.fm](https://www.startups.fm/startups/agno-dev)

### Inferences
- **优势**：从 SDK 到生产服务的一体化程度最高。AgentOS 自带 API、存储、RBAC、多租户、调度、审批、可观测性和多渠道接入，并且能部署在自己的云上，数据自主。原生支持 Agent、Team、Workflow 三种形态和多模态（媒体存储、视频生成工具等）。对象级开销极低，适合大量并发和短生命周期的 agent 实例。工程团队迭代非常快。
- **重点场景**：要把 agent 做成 SaaS 或内部平台的产品团队（多用户、多租户、需要 API）；对数据驻留和安全有要求、想自托管 agent 平台的企业；需要接入 Slack、WhatsApp 等渠道的助手类产品；高并发、需要大量创建 agent 实例的服务。
- **弱点**：性能卖点和真实瓶颈（LLM 延迟、token）关系不大，营销成分重。2 → 3 大版本需要迁移数据库，发版极其频繁，升级成本不低。多 agent（Team）不是它最鲜明的特色，属于“平台型”框架里的一个能力。默认开启遥测。
- **适合的团队**：重视生产化、自托管和多租户的全栈或平台团队，尤其是想“一套框架包办 agent 后端”的中小团队。只是想研究多 agent 协作范式的团队不必首选它。

### Gaps
- 没有找到 Agno 2025-2026 年的新融资信息，现有数据互相冲突。
- 没有找到 Agno 官方当前（3.x）的性能数字和测试方法原文（docs 性能页没能完整抓取）。
- 没有找到具名的大企业用户案例。

---

## Q7. 跨框架对比：各自优势、重点解决的问题场景、弱点、适合什么团队

### Takeaway
这一组框架可以按“多 agent 协作的哲学”分成三类。第一类是**组织隐喻型**：CrewAI（角色团队）、MetaGPT（SOP 软件公司）。第二类是**对话/社会型**：AutoGen/AG2（对话编程）、CAMEL（角色扮演社会、大规模模拟）。第三类是**平台/运行时型**：AgentScope 2.0、Agno 3.x、MAF，多 agent 只是它们的能力之一，重点在生产服务化。2026 年的明显趋势是：各家都在向“确定性工作流 + 有限的 agent 团队（leader-worker）+ 生产运行时”收敛，纯自由对话式的多 agent 正在边缘化。

### Cited Findings
- CrewAI 官方推荐 Flow 为主、Crew 嵌在其中 — [CrewAI Docs](https://docs.crewai.com/en/introduction)
- AgentScope 2.0 主张 “rather than constraining them with strict prompts and opinionated orchestrations”，多 agent 用 leader-worker 的 Agent Team / TeamPipeline 实现 — [AgentScope README](https://github.com/agentscope-ai/agentscope)
- AG2 v1.0 用 Network（hub + channels）取代 GroupChat，并强调 “AgentOS” — [ag2 README](https://github.com/ag2ai/ag2)
- Agno 定位为 “framework and runtime for agent platforms” — [Agno README](https://github.com/agno-agi/agno)
- MAF 1.0 把 sequential、concurrent、handoff、group chat、Magentic-One 作为标准编排模式，并提供带 checkpoint 的图工作流 — [MAF 1.0 博客](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- AgentScope 2026-09 也加了实验性的 SOP，说明 MetaGPT 的 SOP 思想被其他框架吸收了 — [AgentScope NEWS](https://github.com/agentscope-ai/agentscope/blob/main/docs/NEWS.md)

### Inferences（汇总表，基于前文引用的事实综合得出）

| 框架 | 核心优势 | 重点解决的问题场景 | 主要弱点 | 适合的团队 |
|---|---|---|---|---|
| CrewAI | 角色/任务/团队抽象直观；Crews + Flows 兼顾自主与可控；有商业控制面 AMP；不依赖 LangChain | 业务流程自动化、内容与报告流水线、角色分工明确的“数字员工团队” | 自主模式不确定、难调试、token 开销大；发版频繁 | 想快速落地业务自动化的应用团队，或需要商业支持的企业 |
| AutoGen（微软） | 开创对话式多 agent 编程，代码执行循环成熟 | （历史）研究原型、对话式协作、写代码-执行-修正 | 已归档，无安全修复，官方不建议生产使用 | 只适合维护存量代码，新项目改用 MAF |
| MAF | 合并 SK 与 AutoGen，1.0 GA 且承诺长期支持；同时支持 .NET 和 Python；编排模式标准化 | 微软/Azure 生态的企业生产多 agent | 与 Azure/Foundry 绑定较深（推断） | 微软技术栈的企业团队 |
| AG2 | 原作者社区维护；保留经典对话范式（Classic）；v1.0 异步 + 协议驱动 | 对话式多 agent 研究、AutoGen 0.2 老代码延续 | 两次不兼容变化，包名混乱，社区规模较小 | 有 AutoGen 0.2 老代码或做研究的团队 |
| MetaGPT | SOP 结构化协作范式，学术影响大（AFlow 等） | 一句需求生成软件原型和文档；SOP 化 agent 研究 | 开源基本停更，依赖陈旧；重心转向商业产品 Atoms | 研究人员；借鉴其设计思路的团队 |
| CAMEL / OWL | 角色扮演社会、百万级模拟（OASIS）、合成数据；OWL 曾是 GAIA 开源第一 | 社会模拟、合成数据、通用 agent 研究和 benchmark 复现 | 仍是 0.x；OWL 停更，高分依赖定制分支和强模型 | 高校、研究机构、数据合成团队 |
| AgentScope 2.0 | SDK 到多租户服务全栈；沙箱、权限、实时中断；国产模型和钉钉/飞书原生支持；阿里云集成；有 Java 版 | 国内企业 agent 应用、IM 办公助手、沙箱化 coding/数据 agent、实时语音 | 1→2 大幅不兼容重构，多个特性仍是实验性；英文社区声量较小 | 国内团队、阿里云用户、需要开源 agent 平台的团队 |
| Agno 3.x | AgentOS 一体化运行时（API、存储、RBAC、多租户、调度、审批、可观测性）；自托管；对象开销极低 | 把 agent 做成 SaaS 或内部平台；数据合规下自托管；多渠道助手 | 性能宣传偏微基准；3.0 需要迁移数据库，升级成本高 | 重视生产化和多租户的平台型、全栈团队 |

### Gaps
- 没有找到同一套任务上横向对比这 7 个框架端到端效果、成本、延迟的可信第三方 benchmark。
- MAF“与 Azure 绑定较深”是推断，没有专门核实（1.0 博客列出了 Anthropic、Bedrock、Gemini、Ollama 等非微软的连接器）。

---

## Q8. 社区共识：多智能体架构什么时候值得用，什么时候单 agent 更好（Anthropic vs Cognition）

### Takeaway
两篇代表性文章几乎同时发表（2025-06-12 和 2025-06-13），结论看似对立，其实是一致的。**多 agent 适合可以并行、彼此独立、信息量超过单个上下文窗口、价值高到能承担约 15 倍 token 成本的广度型任务（比如研究）**。**需要共享上下文、子任务之间强依赖的任务（大多数写代码的任务）应该用单线程 agent 加上下文压缩。**

### Cited Findings
**Anthropic《How we built our multi-agent research system》（2025-06-13）**
- 架构是 orchestrator-worker：lead agent 分析查询、做规划，并行派生 subagent 去搜索，再汇总结果，最后由 CitationAgent 标注引用来源 — [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)
- 多 agent 系统（Opus 4 做 lead、Sonnet 4 做 subagent）在内部研究评测上比单 agent 的 Opus 4 高 90.2% — [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)
- agent 交互的 token 用量约是普通聊天的 4 倍，多 agent 系统约是聊天的 15 倍。在 BrowseComp 上，有三个因素解释了 95% 的表现差异，其中 token 用量单独解释了 80%。原文说 “Multi-agent systems work mainly because they help spend enough tokens to solve the problem” — [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)
- 适合的情况：广度优先的开放式研究、高度可并行的任务、信息超出单个上下文窗口、需要大量复杂工具、任务价值足以覆盖 token 成本。不适合的情况：要求所有 agent 共享同一上下文或 agent 之间依赖很多的领域、大多数 coding 任务（真正能并行的部分少）、需要实时协调和委派的场景（LLM agent 目前还不擅长） — [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)
- 工程经验：给 subagent 写清楚任务边界；按查询复杂度决定投入多少；并行工具调用最多可把复杂查询的研究时间缩短 90%；有状态 agent 的错误会累积，所以需要 checkpoint 恢复、完整 tracing 和彩虹部署 — [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)

**Cognition《Don't Build Multi-Agents》（Walden Yan，2025-06-12）**
- 两条原则：（1）Share context，共享完整的 agent 轨迹，而不只是单条消息；（2）Actions carry implicit decisions，每个动作都隐含决策，决策冲突会导致坏结果。作者说默认会排除任何违反这两条的架构，并称 2025 年的多 agent 协作会带来脆弱的系统 — [Cognition](https://cognition.com/blog/dont-build-multi-agents)
- 例子：让两个 subagent 分别做 Flappy Bird 克隆的背景和小鸟，结果一个做成了超级马里奥风格的背景，另一个做的小鸟和游戏不匹配。Claude Code 的 subagent 只回答窄问题，不写代码、不并行，因为它们缺少主 agent 的上下文 — [Cognition](https://cognition.com/blog/dont-build-multi-agents)
- 推荐做法：单线程线性 agent。任务很长时加一个专门的上下文压缩模型，把历史提炼成关键细节、事件和决策（Cognition 为此微调了小模型）。作者对长期的多 agent 协作持乐观态度，但认为 2025 年还不可靠 — [Cognition](https://cognition.com/blog/dont-build-multi-agents)

### Inferences
- 两篇文章的共同点是**上下文工程**：多 agent 的价值在于并行扩展 token 和上下文，风险在于上下文割裂、决策冲突。所以判断标准不是“任务复杂不复杂”，而是“子任务能不能在只共享少量上下文的情况下独立完成”。
- 对这一组框架的启示：
  - CrewAI 的自由委派、AG2 Classic 的 GroupChat、CAMEL 的自由角色扮演都容易违反“共享上下文”原则，适合研究、内容生成这类容错高的任务。
  - MetaGPT 的 SOP（结构化文档交接）、CrewAI Flows、AgentScope/MAF 的 leader-worker 和图工作流，相当于用结构约束来降低决策冲突。
  - Anthropic 式的 orchestrator-worker（lead 规划、worker 并行搜索、lead 汇总）在 AgentScope Agent Team、MAF Magentic-One、CrewAI hierarchical、AG2 Network 中都有对应实现。
- 选型建议：先用单 agent（加工具和上下文压缩）做出基线。只有任务明显可以并行、信息量超出上下文、而且价值能覆盖约 15 倍的 token 成本时，才引入多 agent，并优先选结构化编排（leader-worker 或工作流），而不是自由对话。

### Gaps
- 没有检索 LangChain 等其他厂商对这场争论的回应，也没有检索 2026 年是否有更新的业界共识文章（比如 Cognition 是否发过后续）。Cognition 页面上没有更新说明。
- 没有找到针对本组框架的“多 agent 比单 agent 好多少”的独立量化研究。
