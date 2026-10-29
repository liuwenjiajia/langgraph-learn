# 图/工作流编排类 AI 智能体框架：LangChain + LangGraph、LlamaIndex、Microsoft Agent Framework、Semantic Kernel（及 AutoGen）、Haystack

> 调研日期：2026-10-21。版本号与发布日期优先取自 PyPI JSON API 与 GitHub API（当天实时查询），其次是官方博客与官方文档；第三方来源会单独标注。早于 2026 年的来源一律标为【历史】。
> GitHub Star 数为 2026-10-21 通过 `gh api repos/<owner>/<repo>` 查得的快照。

---

## Q1. LangChain / LangGraph（含 LangSmith、LangSmith Deployment、Deep Agents）：现状、核心抽象、优势、目标场景、弱点、生产用户

### Takeaway
LangChain 与 LangGraph 都在 2025-10 发布 1.0，并承诺"2.0 之前不做破坏性变更"。截至 2026-10，最新版本为 langchain 1.4.6 和 langgraph 1.2.16。生态分成三层：LangGraph 是底层、可控的有状态编排运行时（持久化、中断/HITL、时间旅行、流式）；LangChain `create_agent` 加 middleware 是建在 LangGraph 之上的高层 agent API；Deep Agents 是再往上一层、开箱即用的 agent harness（规划、虚拟文件系统、子代理）。另有商业化的 LangSmith，覆盖可观测、评估和部署。它最适合需要长时间运行、有状态、可人工介入、流程要可控的 agent。主要批评集中在抽象过重、学习曲线，以及早期 API 频繁变动。

### Cited Findings

**版本与状态（截至 2026-10-21）**
- `langchain` 最新版 1.4.6，2026-10-14 上传；1.0.0 于 2025-10-17 上传到 PyPI。来源：[PyPI langchain](https://pypi.org/project/langchain/)
- `langchain-core` 最新版 1.6.12（2026-10-16）；1.0.0 上传于 2025-10-17。来源：[PyPI langchain-core](https://pypi.org/project/langchain-core/)
- `langgraph` 最新版 1.2.16（2026-10-16）；1.0.0 上传于 2025-10-17。来源：[PyPI langgraph](https://pypi.org/project/langgraph/)
- GitHub 上 langgraph 1.2.0 的 release 发布于 2026-05-12，langchain==1.4.0 发布于 2026-09-03。来源：[GitHub langgraph releases](https://github.com/langchain-ai/langgraph/releases)、[GitHub langchain releases](https://github.com/langchain-ai/langchain/releases)
- `deepagents` 最新版 0.7.29（2026-10-20），仍处于 0.x。PyPI 简介原文："Production-ready, extensible agent harness with a built-in filesystem and context management, sub-agent delegation, skills, and long-term memory." 来源：[PyPI deepagents](https://pypi.org/project/deepagents/)
- `langsmith` SDK 最新版 0.14.11（2026-10-16）。来源：[PyPI langsmith](https://pypi.org/project/langsmith/)
- GitHub Star（2026-10-21）：langchain 约 148k，仓库描述 "The agent engineering platform."；langgraph 约 43.6k，描述 "Build resilient agents."；deepagents 约 30.5k，描述 "The batteries-included agent harness."。来源：[GitHub langchain](https://github.com/langchain-ai/langchain)、[GitHub langgraph](https://github.com/langchain-ai/langgraph)、[GitHub deepagents](https://github.com/langchain-ai/deepagents)

**LangChain 1.0 / LangGraph 1.0 改了什么（官方博客，2025-10-22）**
- 两者同时达到 1.0，官方承诺 "no breaking changes until 2.0"。来源：[LangChain 官方博客：LangChain and LangGraph 1.0](https://www.langchain.com/blog/langchain-langgraph-1dot0)
- `create_agent`：用任意模型提供商构建 agent 的新入口，运行在 LangGraph runtime 上，取代 `langgraph.prebuilt` 里的 `create_react_agent`（后者已废弃）。来源同上。
- Middleware：在 agent 循环中插入钩子。内置人工审批（HITL）、接近上下文上限时自动摘要、PII 脱敏三种，也支持自定义。来源同上。
- 结构化输出并入主循环（model→tools 循环），省掉一次额外的 LLM 调用。可选工具调用或提供商原生结构化输出。来源同上。
- 标准内容块：消息新增 `.content_blocks` 属性，用与提供商无关的格式表示推理轨迹、引用、服务端工具调用；核心接口位于 `langchain-core` 1.0。来源同上。
- 旧功能（legacy chains、旧 AgentExecutor 等）移入 `langchain-classic` 包，以精简核心包；1.0 起要求 Python 3.10+。来源同上；legacy chains 与 AgentExecutor 的具体归属见二手报道 [ClickIT](https://www.clickittech.com/ai/langchain-1-0-vs-langgraph-1-0/)
- LangGraph 1.0 主打三点：持久化状态（服务重启或流程中断后可从断点恢复）、内置持久化（支持跨多天的审批和后台任务）、一等的人在回路 API。唯一显著的破坏性变更是废弃 `langgraph.prebuilt`，其功能迁到 `langchain.agents`。来源：[LangChain 官方博客](https://www.langchain.com/blog/langchain-langgraph-1dot0)
- 博客自报月下载量 9000 万。来源同上。

**LangGraph 核心概念（官方文档）**
- 自我定位：底层编排框架与运行时，"very low-level, and focused entirely on agent orchestration"；面向长时间运行、有状态的 agent，可在一张图里混合写死的步骤和 LLM 驱动的步骤；不依赖 LangChain 也能单独使用。来源：[LangGraph overview（docs.langchain.com）](https://docs.langchain.com/oss/python/langgraph/overview)
- 核心能力：durable execution（故障后可恢复、可长时间运行）、streaming、human-in-the-loop（运行中任意时刻查看和修改状态）、短期工作记忆 + 跨会话长期记忆、借助 LangSmith 调试与可视化、面向有状态长任务的部署基础设施。来源同上。
- 编程模型：用 `StateGraph` 添加节点（node），用边（edge）连接 `START`/`END`，然后 `compile()`。来源同上。
- 持久化：Checkpointer 把每个 thread（以 `thread_id` 区分）的图状态存成 checkpoint，提供线程级短期记忆；Store 存放跨线程的长期数据（用户偏好、事实等）。持久化支撑四类能力：对话连续性、HITL、time travel、容错。实现包括 `InMemorySaver`（重启即丢）、`SqliteSaver`（适合开发）、`PostgresSaver`/`AsyncPostgresSaver`（适合生产）。来源：[LangGraph persistence 文档](https://docs.langchain.com/oss/python/langgraph/persistence)
- 子图（subgraph）是正式特性：1.2.6 修复了 "nested subgraph inherits parent checkpoint_ns"。1.2 alpha 系列加入了优雅停机/drain、定时器、流式 transformer、节点级错误处理器、`stream_events(version='v3')`（以上来自 release 聚合站，非官方说明页）。来源：[newreleases.io langgraph 1.2.x](https://newreleases.io/project/pypi/langgraph/release/1.2.10)、[1.2.0a6](https://newreleases.io/project/pypi/langgraph/release/1.2.0a6)

**LangSmith / LangSmith Deployment（原 LangGraph Platform）**
- 据 LangChain changelog（检索摘要），LangGraph Platform 已更名为 LangSmith Deployment，LangGraph Studio 更名为 LangSmith Studio；官方说这只是改名，现有部署、API、工作流不受影响。来源：[LangChain changelog](https://changelog.langchain.com/)（检索摘要，未逐条打开）
- LangSmith Deployment 的官方定位是在生产中规模化运行 agent 的托管服务；FAQ 称可部署"任意框架"构建的 agent。来源：[LangSmith Deployment 产品页](https://www.langchain.com/langsmith/deployment)
- 【历史，2025】LangGraph Platform 曾以"部署和管理长时间运行、有状态的 agent"为卖点 GA。来源：[LangGraph Platform GA 博客](https://www.langchain.com/blog/langgraph-platform-ga)
- 【历史，2024-09】Replit Agent 构建在 LangGraph 上，用 LangSmith 追踪；Replit 的复杂度倒逼 LangSmith 补齐了三项能力：大 trace 的性能与规模、trace 内搜索过滤、面向 HITL 的 thread 视图。来源：[LangChain 客户案例：Replit](https://www.langchain.com/blog/customers-replit)

**Deep Agents（deepagents）**
- 定位为 "batteries-included agent harness"，是独立的 `deepagents` 库，基于 LangChain 构建，以 LangGraph 为运行时，获得 durable execution、streaming、HITL 等能力。来源：[Deep Agents overview](https://docs.langchain.com/oss/python/deepagents/overview)
- 能力：opt-in 的 `write_todos` 规划工具（"Starting in v0.7 task planning is opt-in only"，通过 `TodoListMiddleware` 开启）；虚拟文件系统（`ls`/`read_file`/`write_file`/`edit_file`/`glob`/`grep`），后端可插拔（内存状态、本地磁盘、LangGraph store），shell `execute` 只在沙箱后端可用；`task` 工具派生隔离的子代理（默认同步，也可异步并行，且能中途转向）；上下文管理（摘要、卸载大段历史和工具结果，对 Anthropic/Bedrock 做 prompt caching）；从 `AGENTS.md` 加载长期记忆；遵循 Agent Skills 标准的渐进加载 skills；用 `interrupt_on` 在敏感工具调用前暂停审批。来源同上。
- 选型建议：复杂、多步、需要规划、文件化上下文和任务委派的场景用 Deep Agents；想自己搭、不要内置能力时用 `create_agent` 或自定义 LangGraph 工作流。来源同上。
- 公开发布时间各来源不一致：多数说 2026-03，也有说 2025-07 的。来源：[ascii.co.uk 2026-03 报道](https://ascii.co.uk/news/article/news-20260317-3e7156d1/langchain-releases-deep-agents-open-source-llm-agent-framewo)（二手；时间冲突见 Gaps）
- 二手来源称 NVIDIA AI-Q Blueprint 基于 Deep Agents 构建（未经一手确认）。来源：[levelup.gitconnected 生态综述](https://levelup.gitconnected.com/the-langchain-ecosystem-in-2026-a-practitioners-map-884257892374)（通过检索摘要）

**生产用户（官方案例页，偏营销）**
- Klarna：基于 LangGraph + LangSmith 的 AI 助手服务 8500 万活跃用户的客服，客户问题解决时间下降 80%。来源：[Built with LangGraph](https://www.langchain.com/built-with-langgraph)
- AppFolio：物业管理 copilot Realm-X 切到 LangGraph 后回答准确率提升 2 倍，每周节省 10 小时以上。来源同上。
- LinkedIn：用对话式搜索、候选人匹配和分层 agent 系统构建 AI 招聘助手（无数据）。来源同上。
- Uber：开发者平台团队用 LangGraph 构建 agent 网络，做大规模代码迁移和单元测试自动生成（无数据）。来源同上。
- Elastic：编排 AI agent 做威胁检测，减少人力密集的 SecOps 工作（无数据）。来源同上。
- 案例页还有 Lyft、Cisco、GitLab、Rippling、monday.com、Workday、Coinbase、Rakuten 的 logo，未附细节。来源同上。
- 1.0 博客另列 Uber、JP Morgan、BlackRock、Cisco 在生产使用；Rippling 评价："the new agent prebuilt and middleware in LangChain 1.0 makes it far more flexible than before."。来源：[LangChain 1.0 博客](https://www.langchain.com/blog/langchain-langgraph-1dot0)
- LangGraph 文档首页点名 Klarna、Uber、J.P. Morgan。来源：[LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)

**弱点与批评**
- 【历史，2024】Octomind 在生产中用了 LangChain 12 个多月后弃用。原因是要改底层行为时得钻进框架内部，高层抽象让底层代码"很难甚至无法"实现；换成模块化的小组件后代码更简单。文中也承认，在快速变化的技术上设计经得起时间的抽象本来就很难。来源：[Octomind: Why we no longer use LangChain](https://octomind.dev/blog/why-we-no-longer-use-langchain-for-building-our-ai-agents)
- 【二手】据二手汇总，LangChain CEO Harrison Chase 承认早期版本 "abstracted away too much"，1.0 被视为一次纠偏，但也有人认为纠得不够。来源：检索摘要汇总自 [Designveloper](https://www.designveloper.com/blog/is-langchain-bad/) 等（二手，未见 Chase 原话一手出处）
- 【二手，2026】对简单的一问一答任务，图模型是多余的抽象；定义 state、节点、边、checkpointer 的成本，对小团队可能超过收益；带条件路由和环的图比顺序代码更难追踪，LangSmith 能缓解。正面评价：它逼你显式思考 state，做出来的 agent 更好调试。来源：[rentierdigital](https://rentierdigital.xyz/blog/langgraph-for-agentic-ai)、[fme.safe.com LangGraph alternatives](https://fme.safe.com/guides/ai-agent-architecture/langgraph-alternatives/)（二手，后者属竞品方）
- 1.0 把大批旧功能迁到 `langchain-classic` 并废弃 `langgraph.prebuilt`，本身就说明 1.0 之前 API 动荡较大。来源：[LangChain 1.0 博客](https://www.langchain.com/blog/langchain-langgraph-1dot0)

### Inferences
- **优势（综合）**：(1) 底层可控：显式的 state + 节点 + 边，能混合写死的流程和 LLM 自主决策；(2) 生产级运行时原语齐全：checkpointer 持久化、断点恢复、interrupt/HITL、time travel、流式、子图；(3) 分层产品线：从 Deep Agents（开箱即用）到 `create_agent` + middleware（中层）再到 LangGraph（底层），同一 runtime 可以逐层下沉；(4) 生态与集成最大，Star 和下载量领先；(5) LangSmith 提供 tracing、评估和托管部署闭环；(6) 头部企业案例最多（Klarna、Uber、LinkedIn、Elastic、AppFolio、Replit）。
- **重点解决的问题场景**：长时间运行、多步骤、有状态的 agent（客服、招聘、代码迁移、安全运营）；需要人工审批、可暂停可恢复的流程（多天审批、后台任务）；业务流程要严格可控、可审计的"半确定性" agent；多 agent 分层协作；研究和编码类深度任务（Deep Agents）。
- **适合的团队**：以 Python/TS 为主、要在生产上精细控制 agent 行为的工程团队，能接受学习图模型的成本，并愿意（或已经）使用 LangSmith。简单的问答或单次工具调用不必上 LangGraph。
- LangGraph 1.0 之后的 1.1 和 1.2 仍有新运行时特性（节点级错误处理、v3 事件流等），patch 发布非常频繁（1.2.0 在 2026-05，到 2026-10 已到 1.2.16）。这说明"API 稳定"与"高频迭代"并存，用户的升级成本主要变成跟进新特性，而不是被迫重写。

### Gaps
- 没找到 LangGraph 1.1/1.2 和 LangChain 1.1–1.4 的官方汇总 release blog，只看到 release 聚合站条目；每个小版本的具体新特性需查官方 changelog。
- Deep Agents 首次公开发布日期有冲突（2025-07 还是 2026-03），未找到一手发布博客确认。现在 PyPI 仍是 0.x，"production-ready" 是其自述。
- LangGraph Server / Agent Server 在 LangSmith Deployment 改名后是否也改了名，未确认。
- 没有拿到 Reddit r/LangChain 或 HN 的一手社区讨论，批评主要来自博客与二手汇总。
- LangSmith Deployment 当前的定价和自托管选项未核实。

---

## Q2. LlamaIndex（Workflows / AgentWorkflow / LlamaParse / LlamaCloud / LlamaAgents）：从 RAG 框架到 agent 框架的演进、优势、场景、弱点

### Takeaway
LlamaIndex 已从"RAG 数据框架"转型为"文档处理平台加文档 agent"：商业重心是 LlamaParse/LlamaCloud（解析、抽取、分类、切分、索引），开源编排层是事件驱动的 Workflows（2025-06 发布 1.0，2025-08 发布 2.0，2026-10 为 2.26.0），以及在其上的 AgentWorkflow（多 agent handoff）。截至 2026-10，`llama-index-core` 仍是 0.14.x。它最适合文档密集、知识密集的 agent（合同、财报、发票、PE/投行尽调等）。

### Cited Findings

**版本与状态**
- `llama-index-core` 最新版 0.14.25（2026-09-21），仍为 0.x。来源：[PyPI llama-index-core](https://pypi.org/project/llama-index-core/)
- `llama-index-workflows` 最新版 2.26.0（2026-10-11）；1.0.0 上传于 2025-06-25，2.0.0 上传于 2025-08-29。PyPI 简介："An event-driven, async-first, step-based way to control the execution flow of AI applications like Agents." 来源：[PyPI llama-index-workflows](https://pypi.org/project/llama-index-workflows/)
- GitHub run-llama/llama_index 约 52.6k Star，仓库描述已改为 "LlamaIndex is the document processing platform for AI."；Workflows 源码所在的 run-llama/llama-agents 约 460 Star。来源：[GitHub llama_index](https://github.com/run-llama/llama_index)、[GitHub llama-agents](https://github.com/run-llama/llama-agents)

**定位演进（官网，2026-10）**
- 官网标题 "Turn Any Document Into AI-Ready Context"，自称 "an applied AI lab building frontier models for document parsing and extraction"；LlamaParse 的口号是 "Agentic document processing at the frontier of cost and accuracy"；另有 "Build document agents that understand, reason, and act" 和 "Build durable agents that automate knowledge work"。来源：[llamaindex.ai 官网](https://www.llamaindex.ai/)
- LlamaParse（页面上也叫 LlamaCloud）的子产品：Parse（50+ 文件类型，含手写）、Extract（基于 schema 的 LLM 抽取 agent，横幅宣传 "Extract v2.5"）、Split、Classify、Index（RAG 的切分与嵌入流水线）。来源同上。
- LiteParse：开源本地解析器，"VLM-free fast and local OSS parsing"。来源同上。
- 官网自报：处理文档 10 亿+、包月下载 2500 万+、LlamaParse 用户 30 万+、可用性 99.9%；免费档每月 10,000 credits（约 1,000 页）。来源同上（自报数据）。
- 【二手，2026-10-17】LlamaIndex 文档称公司为 "the company behind LlamaParse"，框架为 "original open-source Python toolkit for RAG and agents"。开源编排层重组到 LlamaAgents 品牌下（Workflows + `llamactl` + server/client + LlamaCloud 文档原语 + `@llamaindex/ui` React hooks）。LlamaIndex.TS 于 2026-03 被废弃，2026-04-30 归档。来源：[DevelopersDigest: LlamaIndex in 2026](https://www.developersdigest.tech/blog/llamaindex-workflows-agents-whats-new-2026)（第三方，引用了 llms.txt、GitHub、PyPI）

**Workflows**
- 【历史，2025-06-30】Workflows 1.0 定位为 "a lightweight framework for building complex, multi-step agentic AI applications in Python and Typescript"，async-first、事件驱动。它拆成独立包（Python `llama-index-workflows`，TS `@llamaindex/workflow-core`），旧包继续 re-export；支持 typed state、资源注入（Python）、通过 `llama-index-instrumentation` 接 OpenTelemetry/Arize Phoenix。来源：[LlamaIndex 博客：Announcing Workflows 1.0](https://www.llamaindex.ai/blog/announcing-workflows-1-0-a-lightweight-framework-for-agentic-systems)
- 【二手】2.24.0（2026-09-16）支持配置 serializer；2.25.0（09-25）把超时改为跨 resume 累计存活时间（行为变更）；2.26.0（10-11）新增 journal/restore API、`state_checkpoint`、resume 时 exactly-once 投递；默认 Workflow 超时 45 秒。`llama-agents-server` 0.8.0、`llama-agents-dbos` 0.7.0、`llamactl` 0.10.4 于 09-16 发布。来源：[DevelopersDigest](https://www.developersdigest.tech/blog/llamaindex-workflows-agents-whats-new-2026)

**AgentWorkflow 与 agent 类型**
- 【历史，2025-01-22】AgentWorkflow 是建在 Workflow 抽象上的多 agent 编排系统，负责 agent 间协调和状态维护。agent 类型有 `FunctionAgent`（原生函数调用模型）、`ReActAgent`（任意 LLM），也可自定义；`can_handoff_to` 声明可移交的对象；工具可访问全局 workflow Context 读写共享 state；支持事件流监控；工具可以发出 input-request 事件、等人工响应再继续（HITL）。来源：[LlamaIndex 博客：Introducing AgentWorkflow](https://www.llamaindex.ai/blog/introducing-agentworkflow-a-powerful-system-for-building-ai-agent-systems)
- 【二手】另有 `CodeActAgent`（写代码并执行作为动作）；三种多 agent 模式：handoff、编排者把 agent 当工具、自定义 planner；MCP 双向支持；0.14.24（2026-08-19）修复 AgentWorkflow 对 `structured_output_fn`/`output_cls` 的支持；Retrieval Harness（付费档 beta）给 agent 提供基于已索引文档的文件系统式工具。来源：[DevelopersDigest](https://www.developersdigest.tech/blog/llamaindex-workflows-agents-whats-new-2026)

**客户**
- 官网 logo：Lovable、Carlyle、KPMG、PepsiCo、Lazard、Guidehouse、Michelin、ManpowerGroup、Intel、Sandisk、Cemex、Delphi 等；推荐语来自 NTT DATA、Delphi、Carlyle；案例研究有 Delphi、Carlyle、KPMG、Cemex。来源：[llamaindex.ai](https://www.llamaindex.ai/)
- 【二手】Salesforce Agentforce、Jeppesen（波音旗下）也被列为用户。来源：检索摘要引自 [futureagi / rywalker 等](https://rywalker.com/research/llamaindex)（未经一手确认）
- 【官方，2026-02】newsletter 展示了用 LlamaAgents + LlamaParse SDK 构建的 Private Equity Assistant。来源：[LlamaIndex newsletter 2026-02-03](https://llamaindex.ai/blog/llamaidnex-newsletter-2026-02-03)（检索摘要）

**弱点**
- 【二手，作者自评】编排层只剩 Python（TS 已废弃）；step 要求幂等；持久化需显式开启；事件流只能单读者消费；拆成很多小包；core 在 2026 年基本只有维护性发布。来源：[DevelopersDigest](https://www.developersdigest.tech/blog/llamaindex-workflows-agents-whats-new-2026)
- 2.25.0 的超时语义变更属于小版本里的行为变化。来源同上。

### Inferences
- **优势（综合）**：(1) 文档理解能力业界领先，且与框架深度整合：从 LlamaParse/Extract/Classify/Split 到 Index 再到 agent，一条链路打通；(2) RAG 积淀深（检索、索引、数据连接器）；(3) Workflows 是轻量的事件驱动 step 模型，比显式图更贴近普通 Python 异步代码，又支持 checkpoint/恢复/HITL；(4) AgentWorkflow 让多 agent handoff 上手门槛低；(5) 有开源本地解析（LiteParse），适合数据不能出域的场景。
- **重点解决的问题场景**：文档密集型 agent，例如合同/财报/发票/保单处理、尽调与投研助手（PE、投行、咨询，客户 logo 印证）、知识库问答与企业搜索、表格和 PDF 结构化抽取、"文档进、结构化数据出、agent 后续行动"的自动化流程。
- **适合的团队**：核心难点是"读懂复杂文档"而不是"复杂控制流"的团队；以 Python 为主；愿意为高质量解析付费，或用 LiteParse 本地化。TS 团队不宜再选 LlamaIndex 做编排（LlamaIndex.TS 已归档，二手来源）。
- Workflows 从 1.0（2025-06）到 2.0（2025-08）只隔两个月，此后 2.x 小版本里仍有行为变更，API 稳定性不如 LangGraph 1.x 的"2.0 前不破坏"承诺明确。core 仍为 0.x，说明框架本体不再是公司重心。

### Gaps
- LlamaIndex.TS 废弃和归档的日期只有第三方来源，未打开官方 GitHub 归档声明。
- 官方 LlamaAgents 发布博客未直接打开，具体发布日期和是否 GA 不确定（二手称 2026 年进入 open preview）。
- LlamaCloud 当前定价（Starter/Pro 档）只有第三方数据（Starter $50/月、Pro $500/月），未在官方定价页核实。
- 没找到 r/LocalLLaMA 或 HN 对 2026 版 LlamaIndex 的一手社区批评。

---

## Q3. Microsoft Agent Framework（MAF）：发布时间、融合了 AutoGen 与 Semantic Kernel 的什么、语言支持、图工作流、企业特性、MCP/A2A

### Takeaway
MAF 于 2025-10 推出预览，2026-02-19 发布 RC，2026-04-03 宣布 1.0 GA（.NET + Python，MIT 协议，承诺 API 稳定与长期支持）。它是 Semantic Kernel 与 AutoGen 的"直接继任者"，由同一批团队打造：把 AutoGen 简洁的单/多 agent 抽象，与 SK 的企业特性（会话状态、类型安全、filters/middleware、遥测、广泛的模型支持）合并，再加上基于图的 Workflows（类型化 executor、边、superstep 检查点、HITL）。截至 2026-10，Python 版 1.22.0、.NET 版 1.25.0，Go 版处于公开预览。它最适合 .NET/Azure 技术栈的企业、需要合规、可观测、多 agent 编排的场景。

### Cited Findings

**时间线与版本**
- 2026-04-03 官方宣布 1.0，覆盖 .NET（NuGet `Microsoft.Agents.AI`）和 Python（PyPI `agent-framework`）；2025-10 首次推出，2026-02 进入 RC；"stable APIs, and a commitment to long-term support"；从 RC 升级只需改包版本号；微软员工在评论中确认 MIT 协议。来源：[Microsoft devblog：Agent Framework Version 1.0](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- RC 公告日期为 2026-02-19。来源：[Microsoft Foundry devblog：MAF reaches Release Candidate](https://devblogs.microsoft.com/foundry/microsoft-agent-framework-reaches-release-candidate/)
- PyPI 上 `agent-framework` 1.0.0 上传于 2026-04-02（比博客早一天，可能是时区或预发布所致）；最新版 1.22.0（2026-10-15）。来源：[PyPI agent-framework](https://pypi.org/project/agent-framework/)
- GitHub release 显示 python-1.22.0（2026-10-15）、dotnet-1.25.0（2026-10-14），2026-09 到 10 月大约每周一个小版本。来源：[GitHub microsoft/agent-framework releases](https://github.com/microsoft/agent-framework/releases)
- GitHub 约 14.2k Star。仓库描述："A framework for building, orchestrating and deploying AI agents and multi-agent workflows with support for Python and .NET." 来源：[GitHub microsoft/agent-framework](https://github.com/microsoft/agent-framework)
- 官方文档（2026-07/08 更新）已列出 Go SDK，状态为 public preview，暂不支持 declarative agents、RAG、CodeAct 和 functional workflows。来源：[MAF Overview（Microsoft Learn）](https://learn.microsoft.com/en-us/agent-framework/overview/)

**融合了什么**
- 官方原文："Agent Framework combines AutoGen's simple agent abstractions with Semantic Kernel's enterprise features — session-based state management, type safety, middleware, telemetry — and adds graph-based workflows for explicit multi-agent orchestration." 同页称其为 SK 与 AutoGen 的 "direct successor, created by the same teams" 和 "the next generation of both Semantic Kernel and AutoGen"。来源：[MAF Overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- 四大组成：Agents（调用工具和 MCP server）、Harness Agent（"opinionated agent with batteries-included capabilities for long, multi-step tasks"：规划/todo、上下文压缩、文件访问与记忆、工具审批、可观测）、Workflows（函数式和图式）、Integrations。底层构件：model clients（chat completions 和 responses）、agent session（状态管理）、context providers（记忆）、middleware、MCP clients。来源同上。
- 官方选型原则：开放式或对话式任务、需要自主用工具和规划时用 agent；步骤明确、需要显式控制执行顺序、多 agent 或函数需协同时用 workflow；"If you can write a function to handle the task, do that instead of using an AI agent." 来源同上。

**1.0 稳定特性（GA 博客）**
- 一方连接器：Microsoft Foundry、Azure OpenAI、OpenAI、Anthropic Claude、Amazon Bedrock、Google Gemini、Ollama。来源：[MAF 1.0 博客](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- Middleware 钩子：不改 prompt 就能做内容安全、日志、合规。来源同上。
- 记忆与 context providers：会话历史、持久化 KV 状态、向量检索；后端可选 Foundry Agent Service memory、Mem0、Redis、Neo4j 或自定义。来源同上。
- 图式 Workflows：agent 与函数组合，支持分支、并行 fan-out、汇聚；checkpointing 和 hydration 支撑长时间运行的流程。来源同上。
- 多 agent 编排模式：sequential、concurrent、handoff、group chat、Magentic-One，均支持流式、检查点、HITL 审批、暂停/恢复。来源同上。
- 声明式 YAML：agent 指令、工具、记忆配置、编排拓扑都可放进版本控制的 YAML，一次 API 调用加载。来源同上。
- MCP：发现并调用 MCP server 上的工具。A2A：跨运行时 agent 协作，A2A 1.0 支持 "coming soon"（截至 GA 博客）。来源同上。
- 迁移助手：分析 SK/AutoGen 代码并生成迁移计划。来源同上。

**1.0 时仍为 Preview 的特性**
- DevUI（浏览器本地调试器）；Foundry hosted agents（以托管服务或 Azure Durable Functions 运行）；Foundry 集成（工具、记忆、基于 OpenTelemetry 的可观测与评估面板）；AG-UI/CopilotKit/ChatKit 前端适配；Skills；把 GitHub Copilot SDK 和 Claude Code SDK 当作 agent harness 嵌入 workflow；本地 Agent Harness（shell、文件系统、消息）。来源：[MAF 1.0 博客](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)

**Workflows 概念模型（Microsoft Learn）**
- 定义："explicit, inspectable execution paths for coordinating code, agents, state, events, and human input"。所有 SDK 都支持图式 API，Python 另有实验性的函数式 API（`@workflow`）。来源：[MAF Workflow concepts](https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/)
- .NET 用 `WorkflowBuilder` 连接类型化的 executor（通过 edge 和 condition），支持 fan-out/fan-in，发出 workflow/executor 事件，在 superstep 边界做 checkpoint；可用 `AsAIAgent()` 把 workflow 暴露成标准 agent 接口。来源同上。
- Python 两种 API 对比：函数式用原生 if/循环/`asyncio.gather`，HITL 用 `ctx.request_info()`，按 `@step` 缓存结果；图式用边与条件，靠并行边组和 superstep 实现并行，HITL 用 `RequestInfoExecutor`，在 superstep 边界做 checkpoint；两者都可 `.as_agent()`。还支持 Sub-Workflows（把 workflow 当 executor 嵌套）和 Agent Executor（把 agent 放进图）。来源同上。

**弱点**
- RC 期间的 Python release notes 标了多处破坏性变更，例如把 OpenAI/Azure OpenAI 提供商拆到新包、移除废弃的 kwargs 兼容路径。来源：[newreleases.io python-1.0.0rc6](https://newreleases.io/project/github/microsoft/agent-framework/release/python-1.0.0rc6)（GitHub release 镜像）
- 【二手】从 SK/AutoGen 迁移有重构成本；"Azure 锁定"的说法有争议：有博客认为与 Azure 耦合紧，也有评测指出它支持 OpenAI、Anthropic、Ollama 等多家。来源：检索摘要，[promptquorum MAF review](https://www.promptquorum.com/power-local-llm/microsoft-agent-framework-review)、[Medium first look](https://medium.com/@info_90506/microsoft-agent-framework-a-comprehensive-first-look-d1319c0d72fd)（二手）
- GA 博客只说与 "customers and partners" 一起验证，未点名任何客户。来源：[MAF 1.0 博客](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- 不少企业级能力（Foundry hosted agents、OTel 评估面板、DevUI、Skills）在 1.0 时仍是 preview。来源同上。

### Inferences
- **优势（综合）**：(1) 一流的 .NET 支持，加上 Python 平价（以及预览中的 Go），这是其他几个框架都没有的；(2) 企业基因：类型安全、middleware/filters、会话状态、OpenTelemetry、声明式 YAML（便于版本管理与审计）、与 Microsoft Foundry/Azure 深度打通；(3) agent 与 workflow 两种范式并存，官方选型原则清晰；图式 workflow 的类型化 executor、superstep checkpoint、HITL 和 LangGraph 的 Pregel 风格接近；(4) 内置多种多 agent 模式（含源自 AutoGen 研究的 Magentic-One）；(5) 开放标准：MCP、A2A、AG-UI；(6) 微软官方背书，并承诺 LTS。
- **重点解决的问题场景**：微软技术栈企业（.NET 后端、Azure/Foundry、M365）里的生产级 agent；有合规、审计、遥测要求的流程自动化；多 agent 协作（顺序、并发、handoff、群聊、Magentic）；需要检查点和人工审批的长流程；跨组织或跨运行时的 agent 互通（A2A）；从 SK/AutoGen 的存量迁移。
- **适合的团队**：.NET/C# 团队或深度使用 Azure 的企业、需要微软支持与长期稳定承诺的团队、正在用 SK/AutoGen 的团队。不在微软生态、追求社区生态规模和第三方案例的团队，LangGraph 的选择面更大。
- GA 后约 6 个月 Python 就到了 1.22、.NET 到了 1.25，迭代很快；按语义化版本应不含破坏性变更，但小版本节奏快意味着要持续跟进。

### Gaps
- 没找到任何公开点名的 MAF 生产客户案例（GA 博客未点名），需要关注 Microsoft 客户案例或 Ignite/Build 演讲。
- A2A 1.0 支持在 GA 后是否已落地，未核实。
- 1.0 时为 preview 的特性（DevUI、Foundry hosted agents 等）截至 2026-10 是否已 GA，未逐项核实。
- 二手的"Azure 锁定"批评没有实测依据。

---

## Q4. Semantic Kernel 与 AutoGen 的现状（被 MAF 取代后的状态）

### Takeaway
Semantic Kernel 的 README 已改为 "Semantic Kernel is now Microsoft Agent Framework!"：SK v1.x 仍在维护，只修关键 bug 和安全问题，承诺至少支持到 MAF GA 后一年（即至少到 2027-04 前后），新功能都进 MAF。截至 2026-10 仍有发布（Python 1.45.0，2026-10-06）。AutoGen 的 README 已标为 "archived and no longer maintained"，微软不再提供 bug 修复、安全修复和支持，并建议不要用于生产。新项目不应再选这两个。

### Cited Findings
- SK README 当前提示："Semantic Kernel is now Microsoft Agent Framework! Microsoft Agent Framework (MAF) is the enterprise‑ready successor to Semantic Kernel." 并附迁移指南链接。来源：[GitHub microsoft/semantic-kernel README](https://github.com/microsoft/semantic-kernel)
- 【官方，2025-10-07】"we will continue to support Semantic Kernel v1.x for the foreseeable future"，持续修复 "critical bugs, security issues"；支持期至少到 "one year after Microsoft Agent Framework leaves Preview and is Generally Available"；大部分新功能进 MAF；既有项目或赶工期的项目 "it is perfectly fine to use Semantic Kernel"，新项目推荐从 MAF 起步。来源：[devblog：Semantic Kernel and Microsoft Agent Framework](https://devblogs.microsoft.com/agent-framework/semantic-kernel-and-microsoft-agent-framework/)
- PyPI `semantic-kernel` 最新版 1.45.0（2026-10-06）；1.0.0 于 2024-05-21 发布。来源：[PyPI semantic-kernel](https://pypi.org/project/semantic-kernel/)
- SK GitHub 约 28.7k Star，仍在活跃提交（pushed 2026-10-21）。来源：[GitHub semantic-kernel](https://github.com/microsoft/semantic-kernel)
- SK 的历史价值：MAF 文档称 SK 和 AutoGen "pioneered the concepts of AI agents and multi-agent orchestration"，MAF 继承了 SK 的 session 状态管理、类型安全、filters、遥测和广泛的模型/嵌入支持。来源：[MAF Overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- AutoGen README（2026-10-21 读取）标题带 "status-archived" 徽章，并写明："This project has been archived and is no longer actively maintained by Microsoft. Microsoft is not providing bug fixes, security fixes, new features, or support for this project." 以及 "AutoGen was developed for research and experimentation and as it transitions to archived, we continue to advise against production use."；新用户请转 MAF，存量用户按迁移指南迁移。来源：[GitHub microsoft/autogen README](https://github.com/microsoft/autogen)
- 但 GitHub API 显示该仓库 `archived=false`（尚未在 GitHub 层面设为只读），最后推送 2026-10-16；`autogen-agentchat` 最新版仍是 0.7.5（2025-09-30）。来源：[GitHub API repos/microsoft/autogen](https://github.com/microsoft/autogen)、[PyPI autogen-agentchat](https://pypi.org/project/autogen-agentchat/)
- 【二手】2025-10 时 AutoGen 处于 maintenance mode（只修 bug 和安全问题）；由原作者 Chi Wang、Qingyun Wu 主导的社区分叉 AG2 独立存在、仍然活跃。来源：[atlan: What is AutoGen](https://atlan.com/know/ai-agent/what-is-autogen/)（二手）

### Inferences
- **Semantic Kernel 的优势与场景（历史定位）**：SK 曾是 .NET 企业接入 LLM 的首选 SDK（Kernel、plugins、filters、planner、广泛的连接器），适合把 LLM 能力嵌进既有企业应用。现在它的价值主要是给存量系统提供稳定维护。存量 SK 项目可继续运行，但应规划在 2027 年前后支持期结束前迁到 MAF。
- **AutoGen**：其多 agent 对话与 Magentic-One 等研究成果已被 MAF 吸收。官方 README 从"维护模式"进一步升级为"已归档、不再维护、不建议生产"，新项目应避开。坚持 AutoGen 风格 API 的用户可以考虑社区分叉 AG2（二手来源，需另行核实其现状）。
- 状态冲突说明：AutoGen README 写"已归档"，GitHub 仓库标志位尚未设为 archived，可理解为"正在归档过程中"（README 原文也有 "as it transitions to archived"）。

### Gaps
- SK 支持期的确切截止日期官方未给出（只说"至少 GA 后一年"），按 GA 日期 2026-04-03 推算约为 2027-04，属推断。
- AutoGen 从 maintenance 改为 archived 的官方公告博客没找到，只有 README 文本为证。
- AG2 当前（2026-10）的版本与活跃度未核实。

---

## Q5. Haystack（deepset）：当前版本、Pipelines、Agent 支持、生产/企业定位

### Takeaway
Haystack 于 2026-07-20 发布 3.0（主打 "production-grade agents with full control and flexibility"），2026-10-15 发布 3.4.0（最低 Python 3.11）。核心抽象是可序列化、可在 Kubernetes 上运行的组件化 Pipeline，以及作为组件的 Agent。3.0 给 Agent 加了六点 hooks 系统（HITL 和压缩都做成了 hook），并把 Pipeline 与 AsyncPipeline 合并为一个类。它最适合注重透明、可控、可部署（含私有化/主权 AI）的 RAG 加 agent 生产系统，在欧洲企业中较常见。

### Cited Findings

**版本**
- `haystack-ai` 最新版 3.4.0（2026-10-15）；3.0.0 于 2026-07-20 上传；2.0.0 于 2024-03-11。来源：[PyPI haystack-ai](https://pypi.org/project/haystack-ai/)、[GitHub release v3.0.0](https://github.com/deepset-ai/haystack/releases/tag/v3.0.0)
- 3.4.0 亮点：支持 Python 3.15，放弃 3.10（3.10 于 2026-10 EOL），最低 3.11；新增实验性的 `ToolResultOffloadCompactor`：触发压缩时不丢弃也不摘要旧工具结果，而是写入 `ToolResultStore` 并留下引用，agent 需要时可读回。来源：[GitHub release v3.4.0](https://github.com/deepset-ai/haystack/releases/tag/v3.4.0)
- 【二手】2.31.0 被称为 3.0 前最后一个 2.x 版本，开始把重型组件迁到独立集成包。来源：[Haystack LinkedIn 展示页](https://linkedin.com/showcase/haystack-ai-framework)（检索摘要）
- GitHub 约 26.8k Star，仓库描述："Open-source AI orchestration framework for building context-engineered, production-ready LLM applications. Design modular pipelines and agent workflows with explicit control over retrieval, routing, memory, and generation." 来源：[GitHub deepset-ai/haystack](https://github.com/deepset-ai/haystack)

**Haystack 3.0 变化（官方 release notes）**
- 定位："Haystack 3.0 is a major release for building production-grade agents with full control and flexibility." 来源：[Haystack 3.0.0 release notes](https://haystack.deepset.ai/release-notes/3.0.0)
- Agent hooks 六个挂载点：before_run、before_llm、before_tool、after_tool、on_exit、after_run。Agent 自己负责工具执行（移除独立的 ToolInvoker）；HITL 改为 `before_tool` hook（`ConfirmationHook`）；`ToolResultOffloadHook` 存储大结果，对话中只保留短指针。来源同上。
- `SkillToolset` 渐进披露 skills；`run`/`run_async` 时可传入工具（运行时选工具，一个 Agent 可服务不同团队）；`@tool` 支持 `async def`；Agent 内置 `step_count`、`token_usage`、`tool_call_counts` 状态，tracing 输出 step 级 span。来源同上。
- "`Pipeline` and `AsyncPipeline` are now one class"，提供 `run`、`run_async`、`run_async_generator`、`stream`；`Pipeline.stream()` 逐个产出 `StreamingChunk`。来源同上。
- 组件和 pipeline 新增 `warm_up`/`close` 生命周期，避免长时间运行的服务泄漏连接、GPU 显存和文件句柄。来源同上。
- 精简核心：移除旧 Generators，30 个组件迁到独立发布的集成包；pipeline 反序列化启用可信模块白名单并屏蔽危险 builtins；提供 Mock 组件（`MockChatGenerator` 等），无需 API key 也能测试。来源同上。
- 破坏性变更（官方称 "a few small, intentional breaking changes"）：移除 `AsyncPipeline`、Jinja2 模板变量默认必填、不再按名称隐式注入 `State`、`Document.id` 生成方式改变、tracing 需显式开启、多个组件移出核心。来源同上。

**企业定位与用户**
- 官网口号 "Open-Source AI Orchestration for Production-Grade Agents"；"Haystack Pipelines are serializable, cloud-agnostic, and Kubernetes-ready"；强调透明、可检查和调试每一步（检索、推理、记忆、工具使用），无厂商锁定（OpenAI、Anthropic、Mistral、Hugging Face、Weaviate、Pinecone、Elasticsearch 等）；用例包括高级 RAG、agent、多模态、对话式 AI、内容生成。来源：[haystack.deepset.ai](https://haystack.deepset.ai/)
- 企业产品：Haystack Enterprise Support（私有工程支持、模板、部署指南）；Haystack Enterprise Platform，定位为 "Sovereign AI toolset built on Haystack"，提供可视化且与代码对齐的 pipeline 设计、数据与测试工作流、访问控制，可云上或本地部署。来源同上。
- 【二手】该平台在 2026 年初由 "deepset AI Platform" 更名为 "Haystack Enterprise Platform"。来源：[idp-software.com deepset 厂商页](https://idp-software.com/vendors/deepset/)（二手）
- 官网 logo（无案例细节）：Telus、Lufthansa Industry Solutions、Accenture、NVIDIA、Airbus、AWS、Comcast、Zeit Online。来源：[haystack.deepset.ai](https://haystack.deepset.ai/)

**弱点**
- 3.0 有一批破坏性变更（见上），2.x 用户需按迁移指南升级。来源：[Haystack 3.0.0 release notes](https://haystack.deepset.ai/release-notes/3.0.0)
- 【竞品方观点】有文章认为 Haystack 中 Agent、Tool、StructuredOutput、Evaluator 是 "second-class"（相对于 pipeline）。该文作者是竞品，3.0 的 agent 升级可能已部分回应了这一点。来源：[futureagi: best haystack alternatives 2026](https://futureagi.com/blog/best-haystack-alternatives-2026/)
- 官网只有 logo，没有给出客户案例或性能指标。来源：[Haystack 3.0.0 release notes 页](https://haystack.deepset.ai/release-notes/3.0.0)、[haystack.deepset.ai](https://haystack.deepset.ai/)

### Inferences
- **优势（综合）**：(1) Pipeline 是显式的有向图，组件化、可序列化（YAML）、云无关、可在 K8s 上部署，便于审计和版本管理；(2) RAG 能力成熟（检索、路由、文档存储集成广），并提出了"context engineering"的定位；(3) 3.0 后 agent 能力补齐：六点 hooks、HITL、工具结果卸载和压缩、skills、并发工具、流式、内置运行指标；(4) 工程化细节到位：生命周期管理、安全反序列化、Mock 组件测试；(5) 厂商中立，并有面向主权和私有化部署的企业平台（对欧洲和受监管行业有吸引力，属推断）。
- **重点解决的问题场景**：生产级 RAG、企业搜索与问答；对数据主权和私有化有要求的组织；检索、路由、生成每一步都要透明、可调试的系统；"pipeline 为主、agent 为辅"的混合应用；多模态内容处理。
- **适合的团队**：重视可维护性和可部署性、偏好显式 pipeline 而非高度自治 agent、需要本地或私有云部署、可能想要商业支持的 Python 团队。如果主要需求是复杂的多 agent 协作或超长时间运行的有状态 agent，LangGraph/MAF 的运行时原语更完整（推断）。

### Gaps
- Haystack 3.0 是否内置像 LangGraph checkpointer 那样的 durable execution / 断点恢复，release notes 未提及，需查文档。
- Hayhooks（REST/MCP 部署工具）的当前状态未核实。
- 没找到 Haystack 的一手生产案例（logo 以外的细节）。
- 3.1–3.3 各版本的主要变化只有 RC 片段（如 3.1 新增 `HAYSTACK_UNSAFE_DESERIALIZATION` 环境变量，3.3 改了 BM25 行为），来源为 [newreleases.io](https://newreleases.io/project/github/deepset-ai/haystack/release/v3.3.0-rc1)。

---

## Q6. 横向对比：各框架的优势、重点场景、弱点与团队画像（供报告写作者综合）

### Takeaway
五个框架都汇聚到"图/工作流编排 + agent + HITL + 可观测"这一共同形态，但重心不同：LangGraph 侧重通用、可控、有状态的 agent 运行时，生态最大；LlamaIndex 侧重文档智能；MAF 面向微软生态的企业级统一框架；Haystack 是透明、可部署的 pipeline 与主权 AI；SK 和 AutoGen 已进入维护或归档阶段，由 MAF 接替。

### Cited Findings
- LangGraph 1.0 的 durable state、内置持久化、HITL，以及 "no breaking changes until 2.0" 的承诺。来源：[LangChain 1.0 博客](https://www.langchain.com/blog/langchain-langgraph-1dot0)
- MAF 1.0 的图式 workflow（分支、fan-out、汇聚、checkpointing/hydration）与多 agent 模式。来源：[MAF 1.0 博客](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- LlamaIndex 自我定位为 "document processing platform for AI"。来源：[GitHub llama_index](https://github.com/run-llama/llama_index)
- Haystack 3.0 定位 "production-grade agents with full control and flexibility"，Pipeline 可序列化并能在 K8s 上部署。来源：[Haystack 3.0 release notes](https://haystack.deepset.ai/release-notes/3.0.0)、[haystack.deepset.ai](https://haystack.deepset.ai/)
- "开箱即用 harness"已成趋势：LangChain 有 Deep Agents，MAF 有 Harness Agent（规划、上下文压缩、文件和记忆、工具审批），Haystack 3.x 有 SkillToolset、工具结果卸载和压缩 hook，LlamaIndex 有 Retrieval Harness（beta）。来源：[Deep Agents overview](https://docs.langchain.com/oss/python/deepagents/overview)、[MAF Overview](https://learn.microsoft.com/en-us/agent-framework/overview/)、[Haystack 3.0 notes](https://haystack.deepset.ai/release-notes/3.0.0)、[DevelopersDigest](https://www.developersdigest.tech/blog/llamaindex-workflows-agents-whats-new-2026)

### Inferences

**对比表（所有条目均可追溯到上文 Q1–Q5 的引用；"推断"列为综合判断）**

| 维度 | LangChain + LangGraph | LlamaIndex | Microsoft Agent Framework | Semantic Kernel / AutoGen | Haystack |
|---|---|---|---|---|---|
| 当前版本（2026-10） | langchain 1.4.6 / langgraph 1.2.16 / deepagents 0.7.29 | core 0.14.25 / workflows 2.26.0 | Python 1.22.0 / .NET 1.25.0 / Go 预览 | SK 1.45.0（维护中）/ AutoGen 0.7.5（已归档） | 3.4.0 |
| 1.0/大版本时间 | 2025-10 双 1.0 | Workflows 1.0 于 2025-06，2.0 于 2025-08 | 1.0 GA 于 2026-04-03 | SK 1.0 于 2024-05 | 3.0 于 2026-07-20 |
| 语言 | Python（JS/TS 版本本次未核实） | Python（TS 已废弃，二手） | .NET、Python、Go（预览） | .NET、Python（其他语言 SDK 本次未核实） | Python |
| 核心编排抽象 | StateGraph（节点/边/state）+ checkpointer；create_agent + middleware；Deep Agents harness | 事件驱动 Workflow（step/event/Context）；AgentWorkflow handoff | Agent + 图式 Workflow（executor/edge/superstep）+ 函数式 workflow；Harness Agent | Kernel/plugins（SK）；多 agent 对话（AutoGen） | 组件化 Pipeline（DAG/可序列化）+ Agent 组件（hooks） |
| HITL / 持久化 | interrupt、checkpointer、time travel，一等支持 | input-request 事件；2.26 有 journal/restore、state_checkpoint | RequestInfoExecutor / request_info；superstep checkpoint | — | ConfirmationHook（before_tool）；持久化未确认 |
| 核心优势 | 可控性、运行时原语、生态与案例最多、LangSmith 闭环 | 文档解析/抽取领先、RAG 积淀 | .NET 一流、企业特性、微软背书 LTS、MCP/A2A | 存量稳定 | 透明、可序列化、K8s、厂商中立、主权 AI |
| 重点场景 | 长时间运行的有状态 agent、可控流程、HITL、多 agent、深度研究和编码 | 文档密集型/知识型 agent、投研尽调、抽取自动化 | 微软栈企业、合规流程、多 agent 编排、SK/AutoGen 迁移 | 仅存量维护 | 生产级 RAG、企业搜索、私有化部署 |
| 主要弱点 | 抽象与学习曲线、简单任务过重、历史 API 变动 | core 仍 0.x、Workflows 版本跳得快、编排只剩 Python | 新（GA 约 6 个月）、部分企业能力仍 preview、无公开客户案例、迁移成本 | 不再获得新功能 / 不再维护 | 3.0 破坏性变更、社区规模较小、案例细节少 |
| 公开生产用户 | Klarna、Uber、LinkedIn、Elastic、AppFolio、Replit、JP Morgan 等 | Carlyle、KPMG、Cemex、Delphi 等（logo/案例） | 未公开点名 | — | Airbus、NVIDIA、Telus、Comcast 等（仅 logo） |
| GitHub Star（2026-10-21） | 148k / 43.6k / 30.5k | 52.6k | 14.2k | 28.7k / 61.5k | 26.8k |

- **选型画像（推断）**：
  - 要通用、可控、能长时间运行的 agent，且团队愿意投入学习，选 LangGraph（需要快速做出深度任务 agent 时用 Deep Agents，标准工具调用 agent 用 `create_agent`）。
  - 核心难点是"把复杂文档变成可用上下文"，选 LlamaIndex（LlamaParse + Workflows）；也可以只把 LlamaParse 当解析服务，搭配其他编排框架使用。
  - .NET 或 Azure 企业、存量 SK/AutoGen，选 MAF。
  - 生产 RAG、透明 pipeline、私有化或主权部署，选 Haystack。
- 共同趋势：五家都在补齐 checkpoint 与恢复、HITL、MCP、OpenTelemetry/tracing、开箱即用 harness（规划、文件系统、上下文压缩、skills），差异化正从"有没有"转向"运行时可靠性、生态和商业平台"。

### Gaps
- 没有找到独立、可复现的跨框架性能或可靠性基准，对比只能基于特性和官方说法。
- Star 数只能大致反映社区热度，不能代表生产采用率；PyPI 下载量除 LangChain 自报的 9000 万/月、LlamaIndex 自报的 2500 万+/月外，没有统一的第三方数据。
- LangChain JS/TS（LangGraph.js）的版本状态本次未单独核实。
