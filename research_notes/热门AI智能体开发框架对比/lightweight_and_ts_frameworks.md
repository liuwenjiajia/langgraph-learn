# 轻量级 / 类型安全 / Code-first / TypeScript 生态 AI 智能体框架（截至 2026-10-21）

> 说明：版本号、Star 数、下载量为 2026-10-21 通过 GitHub API、npm 下载 API（统计窗口 2026-10-12 ~ 2026-10-18）和 pypistats（近 30 天）实测，链接给到对应公开页面。标注"历史"的数据是旧时间点的数据，仅作趋势参考。厂商自述（如客户名单、成本降低倍数）一律标注为"官方自述"，未经独立核实。

## Q1. Pydantic AI：现状、核心抽象、优势、重点场景、弱点

### Takeaway
Pydantic AI 的 V1 于 2025-09-05 发布，V2 于 2026-06-23 转正。V2 的核心是 "harness-first" 设计：新增 **Capability** 原语，把指令、工具、hooks、模型设置打包成可组合的单元。框架把 "端到端类型安全 + 类型化依赖注入 + OTel/Logfire 可观测 + 8 种持久化执行引擎 + AG-UI/Vercel AI/ACP/A2A/MCP 多协议" 做成了一套 FastAPI 风格的 Python 生产栈。最适合重视类型、测试和可观测性的 Python 后端团队。

### Cited Findings
**版本与状态**
- v1.0.0 发布于 2025-09-05。这一版加入了人机协同（human-in-the-loop）工具调用审批、`tool_calls_limit` 用量限制、默认附带 `logfire`，并升级了 `temporalio` 依赖（说明发版前已有 Temporal 集成）— [GitHub Release v1.0.0](https://github.com/pydantic/pydantic-ai/releases/tag/v1.0.0)
- v2.0.0 发布于 2026-06-23，经过 7 个 beta 后转正。官方原话是 "V2 leans into a harness-first design with capabilities as a core primitive"— [GitHub Release v2.0.0](https://github.com/pydantic/pydantic-ai/releases/tag/v2.0.0)
- 2026-10-21 同一天发布了 v2.59.0，同时 v1 维护线发布 v1.107.9，两条线并行维护。仓库约 20,763 Star，MIT 许可，GitHub 描述为 "How Python does AI… typed end to end"— [GitHub releases](https://github.com/pydantic/pydantic-ai/releases)（GitHub API 实测 2026-10-21）
- V2 官方文章（Douwe Maan，2026-06-23）要点如下 — [Pydantic AI v2 文章](https://pydantic.dev/articles/pydantic-ai-v2.md)
  - V1 发布后已有"一百多个版本"。官方判断 agent loop 本身已经定型，剩下的提升空间在外围：中途改写模型输入的 hooks、上下文管理、steering、工具按需加载。
  - Capability 把 instructions、tools、lifecycle hooks、model settings 合成一个单元。示例有 `Thinking`、`CodeMode`、`WebSearch`、`ToolSearch`，以及 `defer_loading=True` 的延迟加载 capability。Capability 可序列化，因此 agent 可以从 spec 文件加载。
  - Core 保持小而稳：loop、providers、capability/hooks API。记忆、guardrails、上下文管理、文件系统、code mode 等放到一方的 **Pydantic AI Harness** 包里。官方正在 Pydantic 自己的仓库里内部试用（dogfood）一个基于它的无界面（headless）coding agent。
  - 默认安装只带 OpenAI、Anthropic、Google，`bedrock`、`groq`、`mistral` 等长尾 provider 改为可选安装。`openai:` 前缀默认走 Responses API。
  - 版本策略：大版本之间的"无破坏性变更窗口"从 6 个月缩短到 3 个月；同一大版本内不做破坏性变更。
  - 持久化执行正在"迁移到 capability 层"，文中写的是进行中。
- 第三方博客称 Harness 仍是 0.x，API 可能变动（二手来源，未核实）— [developersdigest](https://www.developersdigest.tech/blog/pydantic-ai-whats-new-2026)

**核心抽象与能力（官方文档）**
- 官方首页列出的卖点 — [Pydantic AI Overview](https://pydantic.dev/docs/ai/overview/)
  - "Typed end to end"：结构化输出和类型化工具，让 IDE 和类型检查器在编写阶段就能发现错误。
  - "typed dependency injection"：把类型化的上下文注入到 instructions 和 tools。
  - "Virtually every model and provider"，也可以通过 Pydantic AI Gateway 实现 failover 和成本监控。
  - "one line lights up Pydantic Logfire"，基于 OpenTelemetry 原生插桩。
  - Pydantic Graph 提供类型化的控制流。
  - Pydantic Evals 可以给最终输出和工具调用轨迹打分。
- 持久化执行官方支持 8 个引擎：Temporal、DBOS、Prefect、Restate、AWS Lambda、Absurd、pgtask、Apache Airflow，另有 builder 可以接入其他引擎。其中 Temporal、DBOS、Prefect、Restate、AWS Lambda 由 Pydantic 与引擎厂商共同维护。每个 agent 只能挂一个引擎。保存、恢复和分叉运行不需要引擎，用 Harness 的 `StepPersistence` 即可 — [docs/durable_execution/overview.md](https://github.com/pydantic/pydantic-ai/blob/main/docs/durable_execution/overview.md)
- 同一个 agent 可以挂到多种界面上：代码调用、终端（`clai`）、Web chat（`agent.to_web()`）、自建前端（AG-UI 或 Vercel AI 协议，含 Vercel `useChat` hooks）、编辑器（Agent Client Protocol，比如 Zed）、其他 agent（A2A，通过独立的 `fasta2a` 包）、实时语音、GitHub Agentic Workflows — [docs/interfaces.md](https://github.com/pydantic/pydantic-ai/blob/main/docs/interfaces.md)
- 官方自述：Pydantic Validation 是 OpenAI SDK、Anthropic SDK、Google ADK、LangChain 等的校验层，FastAPI 也构建在 Pydantic 之上 — [Pydantic AI Overview](https://pydantic.dev/docs/ai/overview/)

**采用度**
- PyPI 近 30 天下载：`pydantic-ai` 5,383,780；`pydantic-ai-slim` 23,908,854。slim 被很多下游包依赖，所以数字偏大 — [pypistats pydantic-ai](https://pypistats.org/packages/pydantic-ai)、[pypistats pydantic-ai-slim](https://pypistats.org/packages/pydantic-ai-slim)

### Inferences
- **优势**
  - 以类型为一等公民：输出、工具参数和依赖都用 Pydantic 模型约束，可以用 mypy/pyright 静态检查。依赖注入让单元测试替换外部依赖很自然（`deps` 加测试模型）。
  - 协议覆盖面很广：AG-UI、Vercel AI、ACP、A2A、MCP 都有。持久化执行可选的引擎数量在同类框架里少见。
- **重点场景**
  - 已有 FastAPI/Pydantic 技术栈的 Python 团队，要构建生产级、强结构化输出的 agent，比如抽取、分类、表单填写、业务流程编排。
  - 需要长时运行或人工审批的流程（接 Temporal/DBOS）。
  - Python 后端配 React `useChat` 前端的组合。
- **弱点**
  - 发版很频繁，近乎每天一版，还有两条线并行。V2 刚出不久，Harness 还处在早期，生态文章和示例可能滞后。
  - 只支持 Python。
  - 深度可观测体验与自家商业产品 Logfire 绑定较深（OTel 原生在一定程度上缓解了锁定）。
  - 复杂多 agent 图编排的成熟度和社区案例仍不如 LangGraph（推断，没有找到直接对比数据）。

### Gaps
- 没有找到 Pydantic AI 官方公布的知名生产用户名单或案例。官方页面只强调 Pydantic Validation 的生态地位。
- V2 文章没有提 Pydantic Graph 和 A2A 的具体演进。A2A 仍通过第三方维护的 `fasta2a`（datalayer）提供，长期维护状态未核实。

## Q2. Hugging Face smolagents：现状、Code Agent、优势、重点场景、弱点

### Takeaway
smolagents 是"用 Python 代码而非 JSON 表达动作"的极简 agent 库，核心逻辑约 1,000 行，主打 CodeAgent、Hub 共享和沙箱执行。它在研究、教学、快速原型和开源模型实验方面很有价值。不过最新版 v1.26.0 发布于 2026-05-29，之后的提交基本只有 CI 和安全加固，**功能开发明显放缓**，生产选型要谨慎。

### Cited Findings
- 2024-12-31 发布博客，定位是 `transformers.agents` 的继任者。博客列出 code action 的四点优势：可组合性、对象管理、通用性、在 LLM 训练数据中出现得多。引用论文为 arXiv 2402.01030（Executable Code Actions Elicit Better LLM Agents）、2411.01747（DynaSaur）、2401.00812 — [HF Blog: smolagents](https://huggingface.co/blog/smolagents)
- README 原话："uses 30% fewer steps (thus 30% fewer LLM calls)"，并且在困难基准上表现更好。这两个数字引用自上述论文，并非 smolagents 自测 — [smolagents README](https://github.com/huggingface/smolagents)
- 自测基准 `m-ric/agents_medium_benchmark_2`：结论是 code agent 优于 vanilla，图注称开源模型 DeepSeek-R1 超过闭源模型。正文没有给出具体分数 — [smolagents README](https://github.com/huggingface/smolagents)、[HF Blog](https://huggingface.co/blog/smolagents)
- 核心特性 — [smolagents docs](https://huggingface.co/docs/smolagents/index)
  - agent 逻辑约 1,000 行。
  - 两种 agent：`CodeAgent` 和 `ToolCallingAgent`（JSON 工具调用）。
  - 沙箱：Modal、Blaxel、E2B、Docker。
  - 可以与 Hub 互相推拉 agent 和工具（作为 Gradio Spaces）。
  - 模型不限：HF Inference Providers、通过 LiteLLM 接 OpenAI/Anthropic、本地 Transformers 或 Ollama。
  - 支持视觉、视频、音频多模态，可用 MCP、LangChain 工具和 Hub Space 作为工具，附带 `smolagent`、`webagent` CLI。
- 安全警告：内置 `LocalPythonExecutor` 被明确标注为"not a security boundary"，必须使用沙箱 — [smolagents README](https://github.com/huggingface/smolagents)
- v1.25.0（2026-05-14）修复了"High impact vulnerability on remote executors"，并移除了旧的无前缀 pickle 支持 — [Release v1.25.0](https://github.com/huggingface/smolagents/releases/tag/v1.25.0)
- v1.26.0（2026-05-29）移除了远程 WasmExecutor，新增 Exa 搜索 — [Release v1.26.0](https://github.com/huggingface/smolagents/releases/tag/v1.26.0)
- 发布节奏：v1.22.0（2025-09-25）、v1.23.0（2025-11-17）、v1.24.0（2026-01-16）、v1.25.0（2026-05-14）、v1.26.0（2026-05-29）。2026-07 到 2026-10-06 的提交全部是安全策略、GitHub Actions 加固和文档修订，没有功能提交 — [smolagents commits](https://github.com/huggingface/smolagents/commits/main)（GitHub API 实测）
- 约 29,955 Star，Apache-2.0。PyPI 近 30 天下载 425,605 — [GitHub](https://github.com/huggingface/smolagents)、[pypistats smolagents](https://pypistats.org/packages/smolagents)
- 官方概念文档给出了 agency 分级（从 Simple processor 到 Code Agents），并主张在确定性工作流能覆盖需求时不要用 agent — [smolagents: What are agents?](https://huggingface.co/docs/smolagents/conceptual_guides/intro_agents)
- 第三方指出它缺少原生的 checkpoint 断点续跑能力（二手来源）— [developersdigest smolagents](https://www.developersdigest.tech/agent-frameworks/smolagents)

### Inferences
- **优势**
  - 代码量极小，可以通读源码，适合学习 agent loop 原理。
  - CodeAgent 天然支持循环、嵌套调用、变量复用，对多步计算和数据处理类任务调用次数更少。
  - 与 HF 生态（Hub、Inference Providers、开源模型）深度集成。
- **重点场景**
  - 研究和基准实验（例如 GAIA 类 deep research）、教学、开源模型 agent 能力评估。
  - 数据分析或计算密集型的多步任务。
  - 想用"代码即动作"范式快速做原型。
- **弱点**
  - 执行任意代码带来固有安全风险，必须额外部署沙箱，2025-2026 年也确实修过高危漏洞。
  - 缺少持久化、状态管理、类型化结构输出等生产级能力。
  - 2026 年中以后功能开发几乎停滞，下载量比 Pydantic AI 和 DSPy 低一个数量级以上。
- 适合的团队：研究、算法团队，以及以 HF 开源模型为主的团队。不建议作为企业生产主框架。

### Gaps
- 没有找到 Hugging Face 官方关于 smolagents 路线图、维护模式或弃用的声明。"放缓"是根据发版和提交记录推断的。
- 没有在官方文本里找到自测基准的具体数值（只有图片）。

## Q3. DSPy（Stanford）：现状、核心抽象、优化器、Agent 用法、重点场景、弱点

### Takeaway
DSPy 的口号是 "Program, don't prompt"。它用 Signature（类型化 I/O 声明）+ Module（策略）+ Optimizer（按指标自动调 prompt 或权重）来替代手写 prompt。当前版本 3.4.1（2026-10-12）。核心价值在于**对复合 AI 系统做可度量的自动优化**（MIPROv2、GEPA 等），agent 是它的一种 Module（`dspy.ReAct`），并非它的主卖点。

### Cited Findings
- 当前版本 3.4.1（2026-10-12），3.4.0 发布于 2026-09-25。仓库约 38,712 Star，MIT — [DSPy releases](https://github.com/stanfordnlp/dspy/releases)（GitHub API 实测）
- 3.0.0（2025-08-12）的重点 — [DSPy 3.0.0 release](https://github.com/stanfordnlp/dspy/releases/tag/3.0.0)
  - 新优化器：RL 方向的 `dspy.GRPO`（基于 Arbor 库），反思式 prompt 演化方向的 `dspy.GEPA` 和 `dspy.SIMBA`。
  - 扩展性：`dspy.Adapter`（Chat/JSON/XML/BAML 适配器）、`dspy.Type`（Image、Audio、History、ToolCalls 等）。
  - 内置支持 MCP 和 LangChain 工具，与 MLflow 3.0 深度集成，提供 async、batch、流式和稳定的 save/load。
- 官方首页 — [dspy.ai](https://dspy.ai/current/)
  - 主张 "Express your tasks as structured signatures, not prompts"，得到 "maintainable, modular, and optimizable programs"。
  - Module 有 `dspy.Predict`、`dspy.ChainOfThought`、`dspy.ReAct`。Agent 用 `dspy.ReAct` 加上普通 Python 函数作为工具，文档有 MCP 专页。
  - 优化器包括 MIPROv2、GEPA、SIMBA、BootstrapFewShot、BetterTogether、BootstrapFinetune、COPRO、KNNFewShot 等。
- 官方自述的采用度：5.3M+ 月下载、39k Star、476+ 贡献者。生产用户有 Databricks、Shopify、Dropbox、AWS、JetBlue、Replit、Nous Research。Shopify 元数据抽取成本降低约 550 倍（官方自述）— [dspy.ai](https://dspy.ai/current/)
- 月下载数和 pypistats 实测基本吻合：`dspy` 近 30 天 5,312,050 — [pypistats dspy](https://pypistats.org/packages/dspy)
- GEPA 论文（arXiv 2507.19457）的数据在两个版本间有变化 — [arXiv v1](https://arxiv.org/html/2507.19457v1)、[arXiv v2](https://arxiv.org/pdf/2507.19457v2)、[alphaXiv v2](https://www.alphaxiv.org/abs/2507.19457v2)
  - v1：在 4 个任务上平均比 GRPO 高 10%、最高高 20%，rollout 少至多 35 倍；比 MIPROv2 高 10% 以上。
  - v2：在 6 个任务上平均比 GRPO 高 6%、最高高 20%；比 MIPROv2 高 10% 以上；AIME-2025 准确率 +12%。
  - 这些都是作者自己的基准，主要是 HotpotQA、HoVer 等，模型为 Qwen3 8B 和 GPT-4.1 Mini。
- 社区批评（多数来自竞品厂商，需打折看）— [futureagi](https://futureagi.com/blog/best-dspy-alternatives-2026/)、[trilogyai](https://trilogyai.substack.com/p/useful-or-not-dspy)
  - 学习曲线陡。
  - 偏离线、notebook 形态，没有 gateway、可观测运行时和内联 guardrails。
  - 优化器跑一批实验成本高，有一个未核实的说法是每批 200 到 400 美元。
  - 无法弥补数据质量或需求不清的问题。

### Inferences
- **优势**
  - 把 prompt 变成可编译、可优化的程序，换模型时重新编译即可，不用重写 prompt。
  - 有评测指标驱动的系统化优化（GEPA、MIPROv2），也可以走微调路线（BootstrapFinetune、GRPO）。
  - Signature 让 I/O 结构化，适配器负责与各模型的结构化输出对接。
- **重点场景**
  - 有标注数据或可定义指标的复合 AI 系统：RAG 管线、多跳 QA、信息抽取、分类。
  - 需要在不同模型之间迁移并保持质量。
  - 想把小模型优化到接近大模型效果、从而降本（例如 Shopify 案例）。
  - 已有 agent 框架的系统中，作为"prompt 优化层"使用。
- **弱点**
  - 不是完整的 agent 应用框架，没有一方的 UI 流式、持久化执行和部署平台。
  - 范式与常规开发差异大。
  - 优化需要评测集和算力成本。
  - 只支持 Python。
- 适合的团队：有 ML、评测文化，追求可度量质量提升的团队。

### Gaps
- 没有找到 DSPy 在"agent 场景"下（而非 QA、抽取场景）的独立大规模生产案例数据。
- GEPA 是否为 ICLR 2026 oral 只见于二手博客，未核实。

## Q4. Mastra（TypeScript）：现状、融资、核心组件、优势、重点场景、弱点

### Takeaway
Mastra 由 Gatsby 原班人马创立（YC W25）。1.0 于 2026-01-20 发布到 npm，当前 @mastra/core 1.78.0，周下载约 133 万，是增长最快的 TS 原生 agent 框架。它提供 agents、workflows、memory、RAG、evals、MCP、Studio 全家桶。2026-04 完成 Spark Capital 领投的 2,200 万美元 A 轮（累计 3,500 万美元），并转型为"框架 + 平台"。主要风险：2026-06 发生 npm 供应链攻击；部分企业功能（`ee/` 目录）不是 Apache 许可。

### Cited Findings
**融资与团队**
- 2025-10-08 宣布 1,300 万美元种子轮 — [Mastra Blog: seed round](https://mastra.ai/blog/seed-round)
  - 投资方包括 YC、Paul Graham、Gradient Ventures、Guillermo Rauch（Vercel）、Amjad Masad（Replit）、Shay Banon（Elastic）等 120 余人。
  - CEO Sam Bhagwat 是 Gatsby 联合创始人，Abhi 是 Gatsby principal engineer，Shane 是 staff engineer 兼产品负责人。
  - 自称"有史以来增长第三快的 JavaScript 框架"（基于对 100 个 npm 包的自行分析）。上线一年时周下载约 19 万，Gatsby 用了四年才到这个数（历史数据，2025-10）。
- 种子轮领投方说法不一：一说 YC 领投，Seedtable 把 YC 列为参投 — [Teten](https://teten.com/?p=24661)、[Seedtable](https://seedtable.com/companies/mastra/funding-rounds/seed-2025-10)
- 2026-04-09 宣布 2,200 万美元 A 轮 — [Mastra Blog: Series A](https://mastra.ai/blog/series-a)
  - Spark Capital 领投，累计融资 3,500 万美元。
  - 同日宣布 "Starting today, Mastra is a platform, too"，推出 Mastra Studio（云端或自托管：evals、logs、traces、datasets、annotations）、Mastra Server（部署 agents 和 workflows）、Memory Gateway（可供其他框架使用的 agent 记忆）。
  - 点名客户：Brex、Sanity、Factorial、Indeed、Marsh McLennan、MongoDB、Workday、Salesforce、Replit（官方自述）。
- 种子轮文章中的点名用户：Replit Agent 3 大规模生成 Mastra agents；SoftBank；Marsh McLennan（75,000 名员工使用基于 Mastra 的 agentic 搜索）；Elastic、Docker 发文介绍了使用情况；PayPal、Adobe 正在走向生产（官方自述）— [Mastra Blog: seed round](https://mastra.ai/blog/seed-round)
- YC W25 批次 — [YC Mastra](https://www.ycombinator.com/companies/mastra/jobs)

**版本与采用度**
- npm 上 @mastra/core 1.0.0 的发布时间是 2026-01-20。官方升级指南称 v1 于 2026-01 发布，主要破坏性变更有：`createTool` 签名、`@mastra/core` 子路径导入、分页改为 page/perPage、配置项 `telemetry:` 改为 `observability:`；提供 codemod `npx @mastra/codemod@latest v1` — [npm registry @mastra/core](https://www.npmjs.com/package/@mastra/core)、[Mastra v1 升级指南](https://mastra.ai/guides/migrations/upgrade-to-v1/overview.md)
- 最新 @mastra/core 1.78.0（GitHub release 2026-10-16），2026-10 上半月几乎每 1 到 3 天一个 minor 版本 — [Mastra releases](https://github.com/mastra-ai/mastra/releases)
- 约 28,971 Star。npm @mastra/core 周下载 1,329,534（2026-10-12 ~ 10-18）— [GitHub](https://github.com/mastra-ai/mastra)、[npm @mastra/core](https://www.npmjs.com/package/@mastra/core)
- 第三方称 1.0 发布前后周下载约 30 万（历史数据，2026-01，二手来源）— [byteiota](https://byteiota.com/mastra-1-0-typescript-ai-framework-reaches-production/)
- 许可证：仓库整体为 Apache 2.0，但所有 `ee/` 目录（如 `@mastra/core/auth/ee`、`agent-builder/ee`、`@mastra/editor/ee`）适用单独的 `ee/LICENSE` — [Mastra LICENSE.md](https://github.com/mastra-ai/mastra/blob/main/LICENSE.md)
- 2026-10 官方博客节奏：Mastra Launch（10-20）、Studio-scoped SSO、Trace Queries、Metrics API、Thread View、Mastra Connect（10-07）、Agent Controller GA（10-06）、VPC 隔离 Postgres（10-01）、Mastra Factory 接入 Jira/GitLab/incident.io（09-30）、Agency Program — [Mastra Blog](https://mastra.ai/blog)
- 第三方 release 跟踪显示 1.x 期间加入了 observational memory、多 agent 的 supervisor 模式、Okta 认证与 RBAC — [releases.sh](https://releases.sh/mastra/mastra-github-releases/highlights)

**安全事件（弱点）**
- 2026-06-17 发生 npm scope 被接管事件 — [Socket](https://www.socket.dev/blog/mastra-npm-packages-compromised)、[Wiz](https://threats.wiz.io/all-incidents/mastra-packages-trojanized-with-malicious-dependency)、[CSA Research Note](https://labs.cloudsecurityalliance.org/research/csa-research-note-mastra-npm-supply-chain-easy-day-js-202606/)、[Hexnode](https://www.hexnode.com/blogs/mastra-npm-supply-chain-attack-compromises-144-ai-framework-packages)
  - 攻击者向 116 到 144 个 `@mastra/*` 包（各来源数字不同）注入仿冒 dayjs 的 `easy-day-js` 依赖，通过 postinstall 投放窃密程序。Mastra 自身代码未被篡改。
  - 入口是被劫持的 npm 账号，现任还是前任贡献者说法不一。
  - Socket 建议：装过受影响版本的主机或 CI 一律视为已失陷。

### Inferences
- **优势**
  - TS 原生的一站式框架：agent、workflow（图状、可暂停恢复）、memory、RAG、evals、MCP、本地 Studio 调试器。对 Next.js/Node 全栈团队来说，"不用切到 Python 就能把 agent 做到生产"。
  - 商业公司全职维护，迭代很快，客户背书强。
  - 和 Vercel AI SDK 兼容互通，Mastra 文档有 AI SDK v5 集成专页（[mastra.ai/docs/frameworks/ai-sdk-v5](https://mastra.ai/docs/frameworks/ai-sdk-v5)）。
- **重点场景**
  - JS/TS 全栈团队构建带记忆、工作流和 RAG 的业务 agent，比如企业搜索、客服、内部 copilot。
  - 需要可观测、评测、部署一体化平台（Mastra Platform/Studio）的团队。
  - 需要多 agent supervisor 的场景。
- **弱点**
  - 版本迭代极快（近乎日更 minor），1.0 刚满 9 个月，API 面广，升级成本和学习成本较高。
  - 出过严重的供应链安全事件，需要锁版本并审计依赖。
  - 部分企业功能是 `ee` 许可，有商业化导向。
  - 平台化后存在一定程度的绑定风险。

### Gaps
- "Mastra Cloud" 是 2025 年时的产品名（历史），本次没有找到它与现在 "Mastra Platform" 的官方对应说明。
- 官方博客没有给出 2026 年的 npm 下载数字，下载数据以 npm API 实测为准。
- 没有找到 Mastra 官方对 2026-06 供应链事件的事后复盘原文（本次只看了第三方安全厂商的报告）。

## Q5. Vercel AI SDK（v5 / v6 / v7）：现状、Agent 抽象、UI 流式、Provider 抽象、AI Gateway、重点场景、弱点

### Takeaway
AI SDK 是 TS 生态下载量最大的 LLM 工具包（npm 周下载约 1,835 万）。主线已经到 **v7**（2026-06-25 发布，当前 ai@7.0.148），v6、v5 线仍在打补丁。演进路线：v5 重做了 UIMessage 和类型化工具部件（2025-07），v6 把 `Agent` 改为接口并提供 `ToolLoopAgent`（2025-12），v7 推出持久化 `WorkflowAgent`、实验性 `HarnessAgent`，并改为 ESM-only（2026-06）。最适合需要流式聊天 UI、多 provider 切换的 Web 应用。

### Cited Findings
**版本线**
- ai@5.0.0 发布于 2025-07-31 — [Release ai@5.0.0](https://github.com/vercel/ai/releases/tag/ai%405.0.0)
  - typed tool parts in UI messages。
  - 工具字段从 args/result 改为 input/output。
  - 自动处理工具执行错误。
  - 去掉 UI 消息到模型消息的自动转换。
  - RSC 拆成独立包。
- ai@6.0.0 发布于 2025-12-22 — [Vercel Blog: AI SDK 6](https://vercel.com/blog/ai-sdk-6)
  - `Agent` 变为接口，可以自定义实现；`ToolLoopAgent` 是现成实现，默认最多 20 步。
  - 工具设 `needsApproval: true` 即开启人机审批。
  - MCP 在 `@ai-sdk/mcp` 中转为稳定，支持 OAuth、resources、prompts、elicitation。
  - DevTools（`npx @ai-sdk/devtools`）。
  - 新增 `rerank`。
  - `generateObject` 与 `generateText` 统一，多步工具循环可以以结构化输出结束。
  - 当时自称"over 20 million monthly downloads"（历史数据）。
  - 案例：Thomson Reuters 用 3 名开发者、2 个月做出 CoCounsel，服务 1,300 家会计事务所；Clay 做了 Claygent。
- ai@7.0.0 发布于 2026-06-25 — [Vercel Blog: AI SDK 7](https://vercel.com/blog/ai-sdk-7)、[Release ai@7.0.0](https://github.com/vercel/ai/releases/tag/ai%407.0.0)
  - `WorkflowAgent`（`@ai-sdk/workflow`）：持久化、可恢复，能扛住进程重启、部署和延迟审批。
  - `ToolLoopAgent` 支持 `toolsContext`、`runtimeContext`、`prepareStep`、`toolApproval`。
  - 实验性 `HarnessAgent`：用统一接口运行 Claude Code、Codex、Pi、Deep Agents、OpenCode 等外部 harness。
  - `registerTelemetry`，支持 OTel 和 Node tracing channel；`experimental_telemetry` 转稳定。
  - 实验性实时语音，支持 OpenAI、Google、xAI，React hook 返回 `UIMessage[]`。
  - `uploadFile`、`uploadSkill`；工具审批（可选 HMAC 签名）；sandbox sessions；MCP Apps；终端 UI；实验性 `generateVideo`。
  - 自称"over 16 million weekly downloads"。
  - 所有包改为 ESM-only，移除 CommonJS 导出；`stepCountIs` 改名为 `isStepCount`。升级 codemod：`npx @ai-sdk/codemod v7`。
- 第三方称 7.0 之后陆续加了 tool search、`toolCallConcurrency`、`streamRetries`，HarnessAgent、batch、code mode 等仍是实验性（二手来源）— [developersdigest](https://www.developersdigest.tech/blog/vercel-ai-sdk-whats-new-2026)
- 2026-10-21 同日发布 ai@7.0.148、ai@6.0.312、ai@5.0.279，三条线都在维护。仓库约 27,428 Star，Apache-2.0 — [vercel/ai releases](https://github.com/vercel/ai/releases)、[LICENSE](https://github.com/vercel/ai/blob/main/LICENSE)
- npm `ai` 周下载 18,352,661（2026-10-12 ~ 10-18）— [npm ai](https://www.npmjs.com/package/ai)

**Provider 抽象与 AI Gateway**
- README 描述为 "provider-agnostic TypeScript toolkit"，支持 Next.js、React、Svelte、Vue、Angular、Node.js，要求 Node.js 22+ — [vercel/ai README](https://github.com/vercel/ai)
  - 直接传模型字符串（如 `'anthropic/...'`）时**默认走 Vercel AI Gateway**；也可以安装 `@ai-sdk/openai` 等 provider 包直连。
  - 结构化输出用 `Output.object({ schema: z.object(...) })`（Zod）。
- AI SDK 7 的 `gateway.experimental_realtime()` 提供归一化的实时会话 — [Vercel Blog: AI SDK 7](https://vercel.com/blog/ai-sdk-7)
- 跨生态的事实：Pydantic AI 官方支持 Vercel AI UI 协议和 `useChat` hooks，所以 `useChat` 前端可以接 Python 后端 — [Pydantic AI docs/interfaces.md](https://github.com/pydantic/pydantic-ai/blob/main/docs/interfaces.md)

**弱点（迁移成本）**
- v4→v5 迁移是重大变更：`Message` 改为 `UIMessage`、parts 成为唯一事实来源、`maxTokens` 改为 `maxOutputTokens`、工具 `parameters` 改为 `inputSchema`，流式协议改为标准 SSE。atypica.AI 的迁移涉及约 200 个文件、耗时约 3 天，codemod 留下大量 FIXME — [atypica.AI 迁移记录](https://atypica.ai/engineering/ai-sdk-v5-migration)、[官方 v5 迁移指南](https://ai-sdk.dev/v5/docs/migration-guides/migration-guide-5-0)

### Inferences
- **优势**
  - Provider 抽象统一，几十个 provider 加上 Gateway 一行切换。
  - React、Vue、Svelte、Angular 都有 UI hooks（`useChat`），流式和类型化 tool parts 做聊天 UI 是事实标准。
  - 下载量和社区规模在 TS 生态领先，Mastra、VoltAgent 等上层框架也构建在它的 provider 层上。
  - 从 v6 起有轻量 Agent 抽象，v7 起有持久化工作流。
- **重点场景**
  - Next.js、React 等 Web 应用中的流式聊天 UI、生成式 UI、带工具调用的助手。
  - 需要在多家模型之间切换或做 failover（配合 AI Gateway）。
  - 部署在 Vercel 上、搭配 Vercel Sandbox 或 Workflow 的产品。
- **弱点**
  - 大约每 6 个月一个大版本（2025-07、2025-12、2026-06），每次都有破坏性变更，v7 还改成了 ESM-only 并要求 Node 22+。
  - 它是"工具包"而非完整的 agent 平台：记忆、RAG、评测需要自己组装或借助 Mastra 之类的框架。
  - 默认 Gateway 与 Vercel 平台有一定的商业耦合。
- 适合的团队：前端或全栈 TS 团队，先做好 AI 产品的 UI 和交互，再逐步加 agent 能力。

### Gaps
- 没有找到 Hacker News 上关于 v5/v6/v7 迁移的代表性讨论（搜索没有返回 HN 结果）。
- AI Gateway 的 GA 日期和定价本次未核实。

## Q6. 其他值得关注的 code-first 框架（VoltAgent、BeeAI、Atomic Agents、Genkit、LangChain.js/LangGraph.js、OpenAI Agents SDK JS）

### Takeaway
TS 生态的格局是：AI SDK（底层工具包）+ Mastra（全家桶）+ LangGraph.js（图编排、跨语言对齐）+ OpenAI Agents SDK JS（轻量多 agent 和语音）为主力，VoltAgent、Genkit 作为补充。Python 轻量派里，Atomic Agents（基于 Instructor 的 schema 链）和 BeeAI（IBM 发起、LF AI & Data 托管、Python 与 TS 双栈）属于小众，采用度低一到两个数量级。

### Cited Findings
**VoltAgent（TS）**
- 定位为 "AI Agent Engineering Platform"：开源 TS 框架加 VoltOps Console（云端或自托管：可观测、自动化、部署、evals、guardrails、prompts）— [VoltAgent README](https://github.com/VoltAgent/voltagent)
- 框架特性：类型化角色和工具（Zod）、工作流引擎、supervisor 与 sub-agent、MCP、记忆适配器、可恢复流式、RAG 与托管知识库、语音、guardrails、evals。示例直接使用 `@ai-sdk/openai` 作为模型 provider — [VoltAgent README](https://github.com/VoltAgent/voltagent)
- @voltagent/core 2.11.0（2026-09-28），1.0.0 于 2025-09-12 发布到 npm。约 10,854 Star，MIT。npm 周下载 23,812 — [VoltAgent releases](https://github.com/VoltAgent/voltagent/releases)、[npm @voltagent/core](https://www.npmjs.com/package/@voltagent/core)

**BeeAI Framework（Python 和 TS，IBM 发起）**
- 定位为 "Build production-ready multi-agent systems in Python or TypeScript"，属于 Linux Foundation AI & Data 项目；README 声明代码由 IBM 以开源形式提供，不是 IBM 产品 — [BeeAI README](https://github.com/i-am-bee/beeai-framework)
- 特性：`RequirementAgent`（用规则约束 agent 行为，让不同 LLM 下表现一致）、`HandoffTool` 多 agent、Backend 统一接口、RAG、Memory、Cache、Serialization、Workflows，可以用 A2A 或 MCP 对外服务。2025-08-25 其 ACP 协议并入 Linux Foundation 下的 A2A — [BeeAI README](https://github.com/i-am-bee/beeai-framework)
- python_v0.1.85、typescript_v0.1.31（2026-09-28），仍是 0.x。约 3,438 Star。PyPI 近 30 天 27,773；npm 周下载 872 — [BeeAI releases](https://github.com/i-am-bee/beeai-framework/releases)、[pypistats beeai-framework](https://pypistats.org/packages/beeai-framework)

**Atomic Agents（Python）**
- 基于 Instructor 和 Pydantic，强调原子化：每个组件单一职责、可复用、可组合、输出可预测。用输入输出 schema（`BaseIOSchema`）把 agent 和工具串成管线，提供 `SystemPromptGenerator`、Context Providers 和 Atomic Assembler CLI — [Atomic Agents README](https://github.com/BrainBlend-AI/atomic-agents)
- v2.14.0（2026-10-20），README 标注 v2.0 已发布并附升级指南。约 6,289 Star，MIT。PyPI 近 30 天 11,711 — [Atomic Agents releases](https://github.com/BrainBlend-AI/atomic-agents/releases)、[pypistats atomic-agents](https://pypistats.org/packages/atomic-agents)

**Google Genkit（JS/TS、Go、Python、Dart）**
- 官方称 "built and used in production by Google's Firebase"。JS/TS 与 Go 已可用于生产，Python 为 Beta，Dart 为 Preview。插件式接入 Google、OpenAI、Anthropic、Ollama 等 — [Genkit README](https://github.com/firebase/genkit)
- Genkit for Node.js 1.0 于 2025-02-12 宣布可用于生产（历史）；2024-05 在 Google I/O 首发 — [Firebase Blog](https://firebase.blog/posts/2025/02/announcing-genkit/)
- 近期版本：go/v1.14.0（2026-10-20）、py/v0.12.0（2026-09-24）、genkit-cli 1.44.0；npm `genkit` 1.42.0（2026-09-01），周下载 130,233。约 6,535 Star，Apache-2.0 — [Genkit releases](https://github.com/firebase/genkit/releases)、[npm genkit](https://www.npmjs.com/package/genkit)

**LangChain.js / LangGraph.js（TS 对照组）**
- @langchain/langgraph 1.0.0 于 2025-10-18 发布到 npm，当前 1.5.1（2026-10-16），周下载 2,065,793。`langchain` 1.5.18，周下载 1,734,370；`@langchain/core` 周下载 3,551,272 — [npm @langchain/langgraph](https://www.npmjs.com/package/@langchain/langgraph)、[npm langchain](https://www.npmjs.com/package/langchain)
- langgraphjs 仓库约 3,370 Star，描述为 "Framework to build resilient language agents as graphs"。近期发布了 `@langchain/react`、`@langchain/vue`、`@langchain/svelte`、`@langchain/angular` 等前端集成包 — [langgraphjs releases](https://github.com/langchain-ai/langgraphjs/releases)
- langchainjs 仓库约 18,285 Star，GitHub 描述改为 "The agent engineering platform" — [langchainjs](https://github.com/langchain-ai/langchainjs)

**OpenAI Agents SDK JS（TS）**
- 描述为 "A lightweight, powerful framework for multi-agent workflows and voice agents"。@openai/agents 0.21.0（2026-10-20），仍是 0.x。npm 周下载 1,155,073，约 3,933 Star — [openai-agents-js](https://github.com/openai/openai-agents-js)、[npm @openai/agents](https://www.npmjs.com/package/@openai/agents)

### Inferences
- **VoltAgent**：适合想要"Mastra 式全家桶"、但偏好 MIT 许可和自托管 VoltOps 的 TS 团队。采用度约为 Mastra 的 1/50，社区和长期可持续性有待观察。
- **Genkit**：适合 Firebase、Google Cloud 和 Gemini 技术栈，或需要 Go 后端的团队。Go SDK 已到生产级，这在同类框架中少见。
- **LangGraph.js**：适合需要显式状态图、checkpoint 和人机协同，并且希望和 Python 版 LangGraph 概念对齐的团队（例如本仓库所学的 LangGraph）。周下载约 200 万，在 TS 编排层仍是主流。
- **OpenAI Agents SDK JS**：轻量，用 handoff 做多 agent，有语音和 realtime，适合深度使用 OpenAI 模型的团队。仍是 0.x，API 可能变化。
- **Atomic Agents**：适合偏好"每一步都是显式 schema 函数"、反感黑盒 agent loop 的 Python 开发者，属于小众。
- **BeeAI**：适合需要 IBM、watsonx、Granite 生态，以及 A2A 开放治理的企业。0.x 加上低下载量，生产采用度有限。

### Gaps
- 没有找到 VoltAgent、Atomic Agents 的融资信息和具名生产客户。
- 没有核实 LangChain.js v1 的 `createAgent` 等新抽象的官方说明（本次只拿到 npm、GitHub 元数据）。
- Genkit 在 Google 内部（Firebase 之外）的生产使用规模没有公开数据。

## Q7. 横向对比：优势、重点场景、弱点、什么团队该选（汇总）

### Takeaway
选型的关键分界线有三条：语言栈（Python 还是 TS）、对"类型安全和生产可靠性"与"极简和实验性"的取舍、是否需要一站式平台。Python 生产选 Pydantic AI，Python 质量优化选 DSPy，研究或原型选 smolagents。TS 的 UI 驱动应用选 AI SDK，TS 全栈 agent 平台选 Mastra，TS 复杂状态编排选 LangGraph.js。

### Cited Findings
- 采用度实测（2026-10，npm 为周下载，PyPI 为近 30 天下载）— [npm API](https://api.npmjs.org/downloads/point/last-week/ai)、[pypistats](https://pypistats.org/)
  - TS：`ai` 18.35M/周、`@langchain/core` 3.55M/周、`@langchain/langgraph` 2.07M/周、`@mastra/core` 1.33M/周、`@openai/agents` 1.16M/周、`genkit` 130k/周、`@voltagent/core` 23.8k/周。
  - Python：`langgraph` 44.8M/月（对照）、`pydantic-ai` 5.38M/月（slim 23.9M/月）、`dspy` 5.31M/月、`smolagents` 426k/月、`beeai-framework` 27.8k/月、`atomic-agents` 11.7k/月。
- GitHub Star（2026-10-21）：DSPy 38.7k、smolagents 30.0k、Mastra 29.0k、AI SDK 27.4k、Pydantic AI 20.8k、LangChain.js 18.3k、VoltAgent 10.9k、Genkit 6.5k、Atomic Agents 6.3k、OpenAI Agents JS 3.9k、BeeAI 3.4k、LangGraph.js 3.4k — 各仓库 GitHub 页面（见上文各节链接）
- 最近发版日期（2026-10-21 查询）：Pydantic AI 2026-10-21、AI SDK 2026-10-21、Mastra 2026-10-16、DSPy 2026-10-12、Atomic Agents 2026-10-20、Genkit Go 2026-10-20、OpenAI Agents JS 2026-10-20、VoltAgent 2026-09-28、BeeAI 2026-09-28、**smolagents 2026-05-29（最旧）** — 各仓库 releases 页（见上文各节链接）

### Inferences
| 框架 | 语言 | 当前版本（2026-10） | 核心优势 | 重点解决的问题场景 | 主要弱点 | 适合团队 |
|---|---|---|---|---|---|---|
| Pydantic AI | Python | v2.59.0（V2 于 2026-06 转正） | 端到端类型安全、DI、Logfire/OTel、8 种持久化引擎、AG-UI/Vercel AI/ACP/A2A/MCP、Evals、Graph | 生产级 Python agent、结构化输出、长时或审批流程、Python 后端加 useChat 前端 | 发版极频繁、V2/Harness 较新、只支持 Python | FastAPI/Pydantic 技术栈的后端团队 |
| smolagents | Python | v1.26.0（2026-05 后停滞） | 约 1,000 行、CodeAgent（引用论文称步数少约 30%）、HF Hub、开源模型 | 研究和基准、教学、数据计算类多步任务原型 | 代码执行安全风险、缺生产能力、开发放缓 | 研究或算法团队、HF 生态用户 |
| DSPy | Python | 3.4.1 | Signature/Module/Optimizer，GEPA、MIPROv2 自动优化，换模型重新编译 | 有指标的复合 AI 系统（RAG、抽取、多跳 QA）、降本、模型迁移 | 学习曲线陡、不是完整应用框架、优化有成本 | 有评测文化的 ML 团队 |
| Mastra | TS | @mastra/core 1.78.0 | TS 一站式：agent、workflow、memory、RAG、evals、Studio、平台，客户背书强 | JS/TS 全栈团队做生产 agent，需要可观测、部署一体化 | 迭代过快、2026-06 供应链事件、`ee` 许可 | Next.js/Node 全栈团队 |
| Vercel AI SDK | TS | ai@7.0.148 | Provider 统一、AI Gateway、`useChat` 流式 UI、ToolLoopAgent/WorkflowAgent | Web 应用流式聊天和生成式 UI、多模型切换 | 每约 6 个月一次破坏性大版本、ESM-only、不是全家桶 | 前端或全栈 TS 团队 |
| LangGraph.js | TS | 1.5.1 | 显式状态图、checkpoint、与 Python 版对齐 | 复杂状态编排、人机协同 | 抽象较重（推断） | 跨 Python/TS 的 LangGraph 用户 |
| VoltAgent | TS | core 2.11.0 | MIT、框架加 VoltOps 自托管 | 想要 Mastra 式能力但偏好 MIT 和自托管 | 采用度低 | 小型 TS 团队 |
| Genkit | JS/TS、Go、Py、Dart | JS 1.42 / Go 1.14 | Google 生产背书、Go SDK 生产级 | Firebase/GCP/Gemini 应用、Go 后端 | 非 Google 生态吸引力弱（推断） | Firebase/GCP 团队 |
| OpenAI Agents JS | TS | 0.21.0 | 轻量 handoff、多 agent、语音 | OpenAI 模型为主的多 agent 和语音 | 0.x | OpenAI 重度用户 |
| Atomic Agents | Python | v2.14.0 | Instructor + Pydantic 的 schema 链，可预测 | 偏确定性的 LLM 管线 | 小众 | 反感黑盒 loop 的 Python 开发者 |
| BeeAI | Python、TS | py 0.1.85 / ts 0.1.31 | RequirementAgent 规则约束、A2A/MCP、LF 治理 | IBM/Granite 生态多 agent | 0.x、采用度低 | IBM 生态企业 |

- 2025 到 2026 年的共同趋势：
  - 框架都在向"harness/capability"层收敛：Pydantic AI V2 的 capabilities，AI SDK 7 的 HarnessAgent，Mastra A 轮文章中的 "harnesses have become bigger, not smaller"。
  - 持久化执行成为标配：Pydantic AI 接 8 个引擎，AI SDK 7 有 WorkflowAgent，Mastra 有可暂停恢复的 workflow。
  - 协议互通：MCP 几乎全员支持；A2A 有 Pydantic AI（经 fasta2a）和 BeeAI；AG-UI 和 Vercel AI UI 协议有 Pydantic AI。
  - 这三点是根据上文各节的引用归纳的。

### Gaps
- 没有找到这些框架之间权威的独立性能或可靠性基准（同一任务、同一模型），只能从特性和采用度上比较。
- 社区讨论（HN、Reddit）的代表性观点本次检索有限，只找到 DSPy 和 AI SDK 迁移相关的零散博客，没有覆盖 Pydantic AI 和 Mastra 的社区口碑。
