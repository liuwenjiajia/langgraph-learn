# 模型厂商 / 云厂商 AI Agent SDK 与互操作协议（截至 2026-10-21）

> 调研时间：2026-10-21。版本号均取自官方 GitHub Releases / PyPI / 官方 changelog 当日页面。凡标注"历史"的条目是 2025 年的背景信息，已被后续变化覆盖或部分覆盖。二手来源（博客、聚合站）的结论单独标注可信度。

## Q1. OpenAI Agents SDK（Python & TypeScript）+ Responses API / AgentKit / Agents API：是什么、现状、优势、重点场景

### Takeaway
OpenAI Agents SDK 是 Swarm 的"生产级升级版"，以 Agents / Handoffs（及 agents-as-tools）/ Guardrails / Sessions / Tracing 少量原语为核心，2026 年 4 月起加入沙箱执行与"模型原生 harness"，已成为仅次于 LangChain 的第二大 agent 框架（Stack Overflow 2026 调查 23.8%）。AgentKit（DevDay 2025）中的可视化 Agent Builder 与 Evals 已在 2026-06-03 宣布下线（2026-11-30 关停），OpenAI 把重心转向"代码优先的 Agents SDK + 全托管的 Agents API（Codex harness）+ ChatKit 前端"。

### Cited Findings
**定位与起源**
- 官方定义：轻量级 Python 包，用于构建 agentic AI 应用，是 OpenAI 早期实验项目 Swarm 的 "production-ready upgrade" — [OpenAI Agents SDK 文档](https://openai.github.io/openai-agents-python/)
- 首发时间：Responses API 与 Agents SDK 于 2025 年 3 月发布（AgentKit 博客原文回顾 "Since releasing the Responses API and Agents SDK in March"）— [OpenAI: Introducing AgentKit](https://openai.com/index/introducing-agentkit/)
- 设计原则：功能够用但原语足够少、开箱即用且可定制、"Python-first" 用语言原生特性做编排而非引入新抽象 — [OpenAI Agents SDK 文档](https://openai.github.io/openai-agents-python/)

**核心原语（当前文档）**
- Agents（带指令和工具的 LLM）、Handoffs 与 agents-as-tools（代理间委派）、Guardrails（输入/输出校验）、Sessions（agent loop 内的持久化记忆层）、Tracing（内置可视化调试，可对接 OpenAI 的评估/微调/蒸馏工具）、Sandbox agents（在隔离工作区中运行、由 manifest 定义文件、可恢复会话）、Realtime 与 voice agents（低延迟语音 agent，以及 STT→agent→TTS 管线）、MCP（内置远程 MCP 工具调用）— [OpenAI Agents SDK 文档](https://openai.github.io/openai-agents-python/)

**版本与 2026 年演进（时间线）**
- 2026-04-15：Agents SDK 增加 sandboxed agent execution、harness inspection/customization 与 memory controls — [OpenAI API Changelog](https://developers.openai.com/api/docs/changelog)
- TechCrunch 报道该版本：引入原生沙箱（agent 只能在工作区内访问特定文件/代码）与 "in-distribution" harness，用于长时程（long-horizon）任务；OpenAI 的 Karan Sharma 称 SDK 兼容"all of these sandbox providers"；新功能先上 Python，TypeScript 后续；路线图包含 code mode 与 subagents；按标准 API 价格提供 — [TechCrunch 2026-04-15](https://techcrunch.com/2026/04/15/openai-updates-its-agents-sdk-to-help-enterprises-build-safer-more-capable-agents/)
- 2026-05-06：TypeScript Agents SDK 增加 sandbox agents 与内置开源 harness — [OpenAI API Changelog](https://developers.openai.com/api/docs/changelog)
- Python 最新版 openai-agents **0.24.0（2026-10-15）**：MCP annotations 暴露到转换后的工具、run 级工具异常格式化、会话写入批处理修复等；0.23.0（10-02）：可配置 MCP 列表分页、Docker 删除保护、记忆整合轮数、approvals 限定到所属 agent；0.21.1 提到 Docker 网络开关、Modal 沙箱资源选项；0.21.0 增加"provider-neutral testing utilities"；0.20.0（08-11）默认模型改为 gpt-5.6-luna、同时支持 MCP Python SDK v1 与 v2 — [openai-agents-python Releases](https://github.com/openai/openai-agents-python/releases)
- TypeScript 最新版 @openai/agents **0.21.0（2026-10-20）**，分为 agents / agents-core / agents-openai / agents-realtime / agents-extensions 五个包；0.21.0 移除了 Runloop 沙箱 provider；agents-realtime 支持 WebRTC、Twilio 音频 — [openai-agents-js Releases](https://github.com/openai/openai-agents-js/releases)

**模型无关性**
- 默认对 OpenAI 模型走 Responses API；文档记录了非 OpenAI provider，提供 Any-LLM 与 LiteLLM 第三方适配器，API 参考中含 Chat Completions 模型接口；官方文档页面并未自称 "provider-agnostic" — [OpenAI Agents SDK 文档](https://openai.github.io/openai-agents-python/)

**AgentKit（DevDay 2025，历史 + 现状）**
- 2025-10-06 DevDay 发布 Agent Builder（可视化多 agent 工作流画布）与 ChatKit（可嵌入聊天界面）— [OpenAI API Changelog](https://developers.openai.com/api/docs/changelog)
- AgentKit 组成：Agent Builder（拖拽节点、版本化、预览运行、内联 eval）、Connector Registry（跨 ChatGPT 与 API 统一管理数据源与第三方 MCP）、ChatKit、开源 Guardrails 库（PII 掩码、越狱检测）、Evals 新功能（datasets、trace grading、自动 prompt 优化、第三方模型评估）、RFT；"AgentKit builds on the Responses API" — [OpenAI: Introducing AgentKit](https://openai.com/index/introducing-agentkit/)
- 当时的客户背书：Klarna 支持 agent 处理三分之二工单、Clay 销售 agent 增长 10 倍（基于 Responses API + Agents SDK）；Ramp 用 Agent Builder 几小时做出采购 agent、"迭代周期缩短 70%"；LY Corporation 两小时内做出工作助理 agent；Canva 用 ChatKit 节省两周以上；Carlyle 称 Evals 缩短 50% 开发时间 — [OpenAI: Introducing AgentKit](https://openai.com/index/introducing-agentkit/)
- **2026-06-03 更新**：OpenAI 宣布逐步关闭 Agent Builder 与 Evals，2026-11-30 起不再可用；代码化工作流建议迁移到 Agents SDK，自然语言场景建议用 ChatGPT Workspace Agents — [OpenAI: Introducing AgentKit（页首更新）](https://openai.com/index/introducing-agentkit/)
- 官方 Deprecations 页：Agent Builder 2026-11-30 关停（替代：Agents SDK 或 ChatGPT Workspace Agents）；Evals 平台 2026-10-31 只读、11-30 关停（替代：Promptfoo）；可复用 prompt 对象 11-30 关停；ChatKit 继续可用；Assistants API 已于 2026-08-26 关停（迁移到 Responses + Conversations API）— [OpenAI Deprecations](https://developers.openai.com/api/docs/deprecations)

**Responses API 与托管 Agents API（2026）**
- Responses API 2026 年持续加码 agent 能力：2026-01-15 发布开源规范 Open Responses；02-10 服务端 compaction、Skills、Hosted Shell；03-05 GPT-5.4 引入 tool search 与内置 computer use；04-24 GPT-5.5 支持 computer use、hosted shell、tool search、Skills、MCP；05-19 Secure MCP Tunnel（让 ChatGPT、Codex、Responses API 和 AgentKit 访问私有 MCP 服务器）；07-09 多 agent 编排在 Responses API 中进入 beta — [OpenAI API Changelog](https://developers.openai.com/api/docs/changelog)
- 2026-09-10：**Agents API 公测**，提供托管的 Codex harness、持久会话与沙箱，可接入自有工具和 MCP 服务器；09-29 增加 computer use（OpenAI 托管浏览器）；10-09 沙箱可预热、只在活跃轮次计费；10-16 托管沙箱获得 Artifact SDK 及表格/演示/文档技能 — [OpenAI API Changelog](https://developers.openai.com/api/docs/changelog)
- 二手报道称 Agents API 无平台费（只付 token 与工具费，沙箱另计）、数据仅限美国、不支持 ZDR（可信度中等，未在官方文档核对）— [MarkTechPost 2026-09-10](https://www.marktechpost.com/2026/09/10/openai-launches-the-agents-api-in-public-beta-putting-the-codex-harness-behind-one-api-call/)；[AI Weekly](https://aiweekly.co/alerts/openai-ships-agents-api-in-public-beta-exposing-managed-codex-harness-with)
- DevDay 2026（InfoQ 2026-10-02 报道）：Agents API 支持 computer use，并纳入 Codex 的多 agent 能力、tool search、tool calling、context compaction，由 OpenAI 管理执行基础设施；另发布 Decisions API（有限预览，用小模型 Luna 从预定义选项中选择，用于分类/路由/选择 agent 下一步）；ChatGPT 插件可通过提议中的 MCP Events 规范响应事件 — [InfoQ: OpenAI DevDay 2026 Recap](https://www.infoq.com/news/2026/10/openai-devday-2026/)

**采用度**
- Stack Overflow 2026 开发者调查"过去一年用过的 agent 编排/框架"：OpenAI Agents SDK 23.8%（1,048 人），仅次于 LangChain 30.2%（n=4,400）— [Stack Overflow Survey 2026 AI data](https://survey.stackoverflow.co/2026/ai/data)

### Inferences
- **优势**：原语少、上手快（Python-first、无 DSL）；与 OpenAI 模型/Responses API 新能力（computer use、hosted shell、compaction、tool search）同步最快；内置 tracing 与 guardrails；语音/实时 agent 是其他厂商 SDK 少有的一等公民；2026 起有沙箱 + harness，可做长时程任务；如不想自管基础设施，可升级到托管的 Agents API。
- **重点场景**：基于 OpenAI 模型的客服/销售/分诊类多 agent（handoff 模式天然匹配客服转接）、语音 agent（呼叫中心、Twilio 电话）、需要 guardrails 的企业流程、在沙箱里读写文件/跑代码的长时程任务，以及前端用 ChatKit 嵌入的 agent 产品。
- **锁定程度**：SDK 本身开源且可通过 LiteLLM/Any-LLM 接其他模型，属"轻度锁定"；但最新功能（hosted tools、computer use、托管沙箱、Agents API、tracing 后端）都依赖 OpenAI 平台。Agent Builder 下线一年即退场的事实说明：依赖厂商托管的无代码层存在产品退役风险，代码层（SDK）更稳。
- **弱点**：0.x 版本号、迭代极快（Python 两个月从 0.20 到 0.24，含"migration-relevant behavior changes"），升级成本不低；非 OpenAI 模型走适配器，能力不对等（推断：hosted tools 等无法跨厂商使用）；Agents API 仍是公测且有数据驻留限制。

### Gaps
- 没有找到 OpenAI 官方公布的 Agents SDK 下载量/星标或专门使用 Agents SDK（而非 Responses API）的客户名单；Klarna/Clay 案例是 "Responses API + Agents SDK" 合并表述。
- Agents API 定价与数据驻留细节只来自二手报道，未在官方文档核实。
- 未核实 OpenAI Agents SDK 是否原生支持 A2A 协议。

## Q2. Claude Agent SDK（原 Claude Code SDK）+ Claude Managed Agents：是什么、现状、优势、重点场景、弱点

### Takeaway
Claude Agent SDK 把 Claude Code 背后的 agent harness（内置文件/命令/搜索工具、agent loop、上下文管理、权限、会话、hooks、subagents、skills、plugins、MCP）以 Python/TypeScript 库形式开放，核心理念是"给 Claude 一台电脑"。它最适合编码 agent 与需要操作文件系统/终端的长时程自主 agent；主要代价是只能用 Claude 模型（可走 Bedrock/Vertex/Foundry 等渠道），且架构上是驱动一个打包的 Claude Code 原生二进制。2026 年 Anthropic 又推出托管版 Claude Managed Agents（beta）。

### Cited Findings
**定位、起源与命名**
- 2025-09-29 Anthropic 将 Claude Code SDK 更名为 Claude Agent SDK，原因是 Claude Code 背后的 harness 能驱动编码之外的多种 agent（内部已用于研究、视频制作、笔记）— [Claude Blog: Building agents with the Claude Agent SDK](https://claude.com/blog/building-agents-with-the-claude-agent-sdk)
- 核心设计原则：给 Claude 访问计算机的能力（终端、文件编辑、搜索），像人一样工作；agent loop 为 "gather context → take action → verify work → repeat" — [Claude Blog](https://claude.com/blog/building-agents-with-the-claude-agent-sdk)
- 官方定义："Build production AI agents with Claude Code as a library"，提供与 Claude Code 相同的工具、agent loop 和上下文管理，支持 Python 与 TypeScript — [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)

**核心能力**
- 内置工具（读/写/编辑文件、运行命令、网页搜索）、Hooks（生命周期关键点执行自定义代码）、Subagents、MCP、Permissions（哪些工具自动运行/需审批）、Sessions（跨轮次保持上下文，可 resume/fork）、Skills/commands/memory（从 `.claude/` 与 `~/.claude/` 自动加载）、Plugins（打包 skills、agents、hooks、MCP 服务器）— [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- 关键上下文工程手段：agentic search（grep/tail 拉取文件片段，文件夹结构即上下文工程）、subagents（并行 + 隔离上下文窗口，只回传相关结果）、compaction（接近上下文上限时自动摘要旧消息，支撑长时程运行）、代码生成作为动作、MCP 集成外部服务；验证手段：规则/lint、视觉反馈（截图）、LLM-as-judge — [Claude Blog](https://claude.com/blog/building-agents-with-the-claude-agent-sdk)
- 官方给出的用例：金融 agent、个人助理 agent、客服 agent（处理模糊工单、必要时升级人工）、深度研究 agent — [Claude Blog](https://claude.com/blog/building-agents-with-the-claude-agent-sdk)
- 与其他 Claude 工具的分工：Agent SDK = 在自己运营的进程里嵌入 Claude Code 的 agent；CLI = 交互式开发；Client SDK = 直接调 API、自己写工具循环（或用 beta tool runner）；Managed Agents = Anthropic 托管 harness；其他语言可用 `claude -p --output-format json` 子进程方式驱动 — [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)

**架构、安装与模型渠道**
- 运行要求 Node.js 18+ 或 Python 3.10+；包名 `@anthropic-ai/claude-agent-sdk` / `claude-agent-sdk`；两种 SDK 都打包了原生 Claude Code 二进制（某些安装方式如 `npm ci --omit=optional` 或 ARM64 Windows 源码包不含二进制，需单独安装 Claude Code）— [Agent SDK Quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart)
- 认证渠道：Anthropic API key，或 Amazon Bedrock（`CLAUDE_CODE_USE_BEDROCK=1`）、Claude Platform on AWS（`CLAUDE_CODE_USE_ANTHROPIC_AWS=1`）、Google Cloud's Agent Platform（`CLAUDE_CODE_USE_VERTEX=1`）、Microsoft Foundry（`CLAUDE_CODE_USE_FOUNDRY=1`）— [Agent SDK Quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart)
- 条款限制：未经批准，第三方不得在基于 Agent SDK 的产品中提供 claude.ai 登录或其速率额度；产品不得命名为 "Claude Code" 或模仿其视觉；使用受 Anthropic Commercial Terms 约束 — [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)

**版本（2026-10-21）**
- Python 最新 **v0.2.170（10-21）**，打包 CLI 2.1.306；v0.2.166（10-14）新增类型化 hook 输出类与 `SystemInitData`；多数版本仅更新打包的 CLI — [claude-agent-sdk-python Releases](https://github.com/anthropics/claude-agent-sdk-python/releases)
- TypeScript 最新 **v0.3.306（10-21）**，与 Claude Code v2.1.306 对齐；v0.3.304 为浏览器 SDK 增加 `suspendSseStream`/`resumeSseStream`；v0.3.302 起 fork subagents 在 SDK 会话中默认开启、第三方 provider 上默认 `permissionMode` 改为 `default` — [claude-agent-sdk-typescript Releases](https://github.com/anthropics/claude-agent-sdk-typescript/releases)

**Claude Managed Agents（托管版）**
- 定义：预构建、可配置的 agent harness，运行在托管基础设施上，适合长时程与异步任务；四个核心概念 Agent / Environment（Anthropic 托管云沙箱或自托管沙箱）/ Session / Events；SSE 流式返回，事件历史服务端持久化，可中途 steer/interrupt；支持 cron 定时部署；内置 Bash、文件操作、Web 搜索/抓取、MCP；处于 beta（beta header `managed-agents-2026-04-01`），也可在 Claude Platform on AWS 使用；因有状态设计，目前不符合 ZDR 与 HIPAA BAA — [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)

**知名用户/集成**
- Apple Xcode 26.3 原生集成 Claude Agent SDK（2026-02-03 宣布），开发者在 IDE 内获得 subagents、后台任务、plugins，Claude 可截取 Xcode Previews 迭代 SwiftUI 界面 — [Anthropic: Apple Xcode × Claude Agent SDK](https://anthropic.com/news/apple-xcode-claude-agent-sdk)；[Anthropic on X](https://x.com/AnthropicAI/status/2018771170938724682)
- Microsoft Agent Framework 在 Build 2026 推出到 Claude Agent SDK 与 GitHub Copilot SDK 的 connector，可把这些编码 agent 作为编排中的一员，并沿用同一身份/内容安全/OTel 观测策略 — [InfoQ 2026-08-03](https://www.infoq.com/news/2026/08/agent-framework-harness-ga/)
- AWS AgentCore Harness 提供导出到 Strands 代码，"Claude Agent SDK coming soon" 作为导出目标 — [AWS What's New 2026-06-17](https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-agentcore-harness-generally-available/)
- 二手聚合来源称 Intuit 用 SDK 为中型企业构建定制 agent（未核实）— [genaipm wiki](https://genaipm.com/wiki/tools/claude-agent-sdk)

**弱点/批评（多为社区观点）**
- 架构上是 Python/TS 包装器以子进程方式驱动 Claude Code CLI 并经 stdio 交换消息；包管理器跳过可选依赖会导致缺少原生二进制 — [ksred.com](https://www.ksred.com/the-claude-agent-sdk-what-it-is-and-why-its-worth-understanding/)；[Agent SDK Quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart)
- 有作者认为它把你耦合到 Anthropic 模型、MCP 工具与托管设施，换模型需重写 agent 逻辑；另一作者认为选多厂商框架就要放弃 CLAUDE.md、hooks、skills 这些 Claude 特有能力 — [Towards AI (Medium)](https://pub.towardsai.net/i-built-the-same-agent-in-cursor-claude-and-openais-new-sdks-one-shouldn-t-win-with-9-lines-bb3f9b671729)；[ksred.com](https://www.ksred.com/the-claude-agent-sdk-what-it-is-and-why-its-worth-understanding/)
- 计费：二手来源对"Agent SDK 与 `claude -p` 用量从 2026-06-15 起改为独立月度额度"说法不一，有的称当天即暂停 — [Totalum Blog](https://www.totalum.app/blog/claude-agent-sdk-credits-2026)；[developersdigest](https://www.developersdigest.tech/blog/claude-agent-sdk-whats-new-2026)（低可信度，需以官方为准）
- Stack Overflow 2026 的"agent 编排/框架"题目选项中没有 Claude Agent SDK，但在编码 agent 题中 Claude Code 使用率 66% 居首 — [Stack Overflow Survey 2026 AI data](https://survey.stackoverflow.co/2026/ai/data)；[Stack Overflow Survey 2026 AI](https://survey.stackoverflow.co/2026/ai)

### Inferences
- **优势**：最"重"也最完整的开箱 harness——文件系统、bash、搜索、compaction、subagents、hooks、权限、skills、plugins 全部内置且经过 Claude Code 大规模实战打磨；开发者只写 prompt/工具/策略，不用自己写 agent loop 与上下文管理；与 Claude Code 生态（`.claude/` 配置、skills、plugins、MCP）同构，复用成本低。
- **重点场景**：编码 agent（代码审查、修 bug、IDE 集成如 Xcode）、需要"一台电脑"的长时程自主 agent（研究报告、数据处理、文档生成、运维脚本）、CI/CD 中的无人值守任务、需要细粒度权限与 hook 审计的企业 agent；不想自管运行时可用 Managed Agents。
- **锁定程度**：模型层强锁定（仅 Claude，但云渠道多元：Anthropic API / Bedrock / Google Agent Platform / Foundry）；工具层通过 MCP 可移植；编排层（hooks、skills、subagents 语义）与 Claude Code 绑定。
- **弱点**：Claude-only；依赖打包的原生二进制与子进程通信，部署形态比纯库重（容器镜像、平台兼容性）；品牌与登录方式受条款限制；Managed Agents 仍 beta 且不支持 ZDR/HIPAA。

### Gaps
- 未找到官方公布的 Agent SDK 下载量或客户名单（除 Apple Xcode 外）。
- 未核实 Claude Agent SDK 是否原生支持 A2A。
- Managed Agents 首发日期与定价未在本次调研中确认（仅见 beta header 日期 2026-04-01）。
- 2026 年 6 月计费调整的最终状态未能用官方来源确认。

## Q3. Google Agent Development Kit（ADK）+ Vertex AI Agent Engine（现 Gemini Enterprise Agent Platform / Agent Runtime）：现状、优势、重点场景

### Takeaway
ADK 是 Google 开源的"代码优先"agent 框架，覆盖 Python、TypeScript、Go、Java、Kotlin 五种语言，内建多 agent 层级、工作流 agent、评估工具与 A2A/MCP 支持；2026 年的 ADK 2.0 把执行模型从"层级 agent 执行器"改为"图式 Workflow Runtime"（Python 5-19、Go 6-30、TS 8-21 GA）。它"模型与部署无关但为 Gemini 优化"，最适合 Google Cloud 上需要确定性工作流 + LLM 推理混合、多语言团队、以及跨组织 A2A 互通的企业 agent。Vertex AI 已在 Cloud Next 2026 更名为 Gemini Enterprise Agent Platform，托管运行时在 ADK 文档中称为 "Agent Runtime"。

### Cited Findings
**定位与语言**
- 官方定义：开源 agent 开发框架，"build, debug, and deploy reliable AI agents at enterprise scale"；支持 Python（`google-adk`）、TypeScript（`@google/adk`，2.0 GA）、Go（`google.golang.org/adk/v2`）、Java（`com.google.adk:google-adk`）、Kotlin（`google-adk-kotlin-core`）— [adk.dev](https://adk.dev/)
- PyPI 描述："open-source, code-first Python framework for building, evaluating, and deploying AI agents… model-agnostic and deployment-agnostic, though optimized for Gemini"；最新 **google-adk 2.12.0（2026-10-13）**，Apache 2.0 — [PyPI google-adk](https://pypi.org/project/google-adk/)
- 首发（历史）：ADK 于 Google Cloud Next 2025（2025 年 4 月）随 Vertex AI 多系统 agent 能力一起发布，Revionics 当时展示了基于 ADK 的多 agent 定价系统 alpha — [Google Cloud Blog（日文版）](https://cloud.google.com/blog/ja/products/ai-machine-learning/build-and-manage-multi-system-agents-with-vertex-ai)；[Chain Drug Review](https://chaindrugreview.com/revionics-unveils-futuristic-pricing-solution-at-google-cloud-next)
- Java 1.0.0 于 2026-03-30 发布（新增 Google Maps grounding、HITL 确认流）；Go 1.0 于 2026-03-31 发布（原生 OpenTelemetry tracing、插件系统）（根据搜索摘要，未逐页核实）— [Google Developers Blog: ADK for Java 1.0.0](https://developers.googleblog.com/announcing-adk-for-java-100-building-the-future-of-ai-agents-in-java/)；[Google Developers Blog: ADK Go 1.0](https://developers.googleblog.com/adk-go-10-arrives/)

**ADK 2.0（2026）**
- GA 日期：Python 2.0 于 2026-05-19、Go 2.0 于 2026-06-30、TypeScript 2.0 于 2026-08-21；页面称 2.0 "is available for Python, TypeScript, and Go"，未列 Java/Kotlin — [ADK 2.0](https://adk.dev/2.0/)
- 新特性：Workflow Runtime 把 ADK 从层级 agent 执行器改为图引擎，agents、tools、functions 都作为节点运行；支持图式确定性工作流、代码化动态工作流（循环/分支）、协调者 + 多子 agent 的协作工作流；`RetryConfig` 自动重试、HITL 暂停 — [ADK 2.0](https://adk.dev/2.0/)
- 破坏性变更：Python 中 `BaseAgent` 改为继承 `BaseNode`，不应再覆写 `_run_async_impl()`，新增事件字段可能需要改数据库 schema；TypeScript 中 `SequentialAgent`、`ParallelAgent`、`LoopAgent` 已标记 deprecated；Go 导入路径改为 `/v2` — [ADK 2.0](https://adk.dev/2.0/)
- PyPI 列出的 2.x 特性：Workflow Runtime（路由、循环、重试、状态、HITL、嵌套工作流）、Task API（结构化 agent 间委派）、多 agent 层级、丰富工具生态（预置工具、函数、OpenAPI、MCP）、Agent Config（无代码定义 agent）、Tool Confirmation、部署到 Cloud Run 或 Vertex AI Agent Engine — [PyPI google-adk](https://pypi.org/project/google-adk/)

**评估、部署、互操作、模型**
- 评估：criteria、用户模拟、环境模拟、自定义指标与优化；部署：Agent Runtime（Agent Platform）、Cloud Run、GKE 及容器化自托管；A2A：提供 Python/Go/Java/Kotlin 的暴露与消费 A2A agent 快速入门；MCP 工具（含将 agent 作为 MCP server）；模型适配：OpenAI、Claude、Ollama、vLLM、LiteLLM；首页称可用 Gemini 及其他主流模型，"can work with almost any generative AI model" — [adk.dev](https://adk.dev/)

**托管平台更名**
- Cloud Next 2026：Google 把 Vertex AI 更名为 Gemini Enterprise Agent Platform，增加构建、编排、治理 agent 的工具；Agentspace 并入 Gemini Enterprise 应用 — [HPCwire/AIwire 2026-04-23](https://www.hpcwire.com/aiwire/2026/04/23/google-unveils-gemini-enterprise-agent-platform/)；[The Next Web](https://thenextweb.com/news/google-cloud-next-ai-agents-agentic-era)
- 单一博客称 Agent Engine 更名为 Agent Runtime（Vertex AI Search→Agent Search 等）— [workspaceblog.in](https://www.workspaceblog.in/blog/vertex-ai-to-gemini-enterprise-agent-platform-migration-guide/)；ADK 官网部署栏目写作 "Agent Runtime (Agent Platform)"，Anthropic 文档也称 "Google Cloud's Agent Platform"，间接印证 — [adk.dev](https://adk.dev/)；[Claude Agent SDK Quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart)

**知名用户与采用度**
- Google Cloud 博客引述 Renault Group 用 ADK 开发帮助选址 EV 充电桩的 agent；Revionics 用 ADK 构建零售多 agent 定价系统（发布时为 alpha）— [Google Cloud Blog](https://cloud.google.com/blog/ja/products/ai-machine-learning/build-and-manage-multi-system-agents-with-vertex-ai)；[Martechvibe](https://martechvibe.com/?p=47624)
- Stack Overflow 2026 调查：Google ADK 14.0%（617 人），排在 LangChain、OpenAI Agents SDK、LangGraph、Llama Stack 之后 — [Stack Overflow Survey 2026 AI data](https://survey.stackoverflow.co/2026/ai/data)

### Inferences
- **优势**：语言覆盖最广（五种语言，Java/Kotlin/Go 对企业后端团队友好）；2.0 图式 Workflow Runtime 把"确定性代码 + LLM 推理"统一为节点，兼顾可控性与灵活性；评估工具（用户/环境模拟）在厂商 SDK 中最完整之一；A2A 由 Google 发起，ADK 的 A2A 支持最成熟；与 Google Cloud 托管运行时、Cloud Run、GKE 一条龙部署。
- **重点场景**：Google Cloud / Gemini 上的企业级多 agent 系统（定价、客服、数据分析）、需要确定性流程编排（审批、ETL 式多步骤）的场景、多语言微服务团队、需要通过 A2A 与其他组织/框架的 agent 互通的场景。
- **锁定程度**：中低——框架开源且模型适配广，但"为 Gemini 优化"，托管运行时与 Google Cloud 绑定。
- **弱点**：2.0 破坏性变更较多（事件 schema、基类变化、Go 导入路径），1.x 时代的 Sequential/Parallel/LoopAgent 在 TS 中已 deprecated，旧教程大量失效；Java/Kotlin 尚未进入 2.0；平台更名（Vertex AI → Agent Platform、Agent Engine → Agent Runtime）造成文档与品牌混乱。

### Gaps
- Agent Engine → Agent Runtime 更名缺少 Google 官方公告的直接核实。
- 未找到 ADK 官方下载量数据；Renault/Revionics 的生产状态未确认。
- Java 1.0 / Go 1.0 的发布细节来自搜索摘要，未逐页抓取核对。

## Q4. AWS Strands Agents + Amazon Bedrock AgentCore：现状、优势、重点场景

### Takeaway
Strands Agents 是 AWS 开源的"模型驱动（model-driven）"agent SDK：几行代码定义模型 + 工具 + 提示，由模型自主规划，而非开发者硬编码工作流；1.0（2025-07-15）引入 agents-as-tools、handoffs、swarm、graph 四种多 agent 原语与 A2A，截至 2026-10 已到 Python v1.61.1 / TS v1.21.0，并新增 Strands Harness、Strands Box（策略沙箱）、Strands Decider 2B（决策小模型）。配套的 Bedrock AgentCore（2025-10-13 GA）是框架与模型均无关的托管运行时（Runtime/Memory/Gateway/Identity 等），2026-06-17 又推出托管 AgentCore Harness。

### Cited Findings
**Strands Agents SDK**
- README：开源 SDK，Python（3.10+）与 TypeScript（Node.js 22+），"runs in your process with no hosted control plane"；"A model-driven approach to building AI agents in just a few lines of code"；一等支持 Amazon Bedrock、Anthropic、OpenAI、Gemini，文档覆盖 Ollama 等，可自定义 provider；TS 默认模型为 Bedrock；内置多 agent 与 MCP；Python 支持双向流；Apache 2.0；约 8.9k stars；提供 Strands Harness（`create_harness()`/`createHarness()`，带基准化默认的模型/工具/记忆/会话/上下文管理） — [strands-agents/sdk-python](https://github.com/strands-agents/sdk-python)
- 1.0 发布（2025-07-15）：四个多 agent 原语——Agents-as-Tools、Handoffs（含 `handoff_to_user` 交还人类）、Swarms（共享记忆的自治团队）、Graphs（带条件路由的显式工作流）；支持 A2A（任意 Strands agent 可包装为网络可访问，外部 A2A agent 可加入 Strands 多 agent 模式）；`SessionManager`（本地文件 / S3 后端）；`stream_async` 异步流与取消；合作伙伴贡献 Anthropic、Meta、OpenAI、Cohere、Mistral、Stability、Writer、Baseten 等 provider；预览期已支持 Bedrock 全部模型及经 LiteLLM 的 OpenAI 兼容端点 — [AWS Open Source Blog](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-1-0-production-ready-multi-agent-orchestration-made-simple/)
- 1.0 时的采用数据：自 2025 年 5 月预览以来 2,000+ GitHub stars、150K+ PyPI 下载，0.1.0→1.0 合并 150+ PR（22% 来自社区）；Amazon Q Developer、AWS Glue 等团队在生产中使用 — [AWS Open Source Blog](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-1-0-production-ready-multi-agent-orchestration-made-simple/)
- 当前版本：python/v1.61.1（10-15，修复类）、typescript/v1.21.0（10-14：面向 Claude/Codex/Cursor 的 Strands 打包、DecisionModel 原语、MCP 进度回调、python_repl 工具、TS subagent 工具）、python/v1.60.0（10-12：OTel baggage 传播、MCP SEP-2663 任务执行、auxModel）、harness-python v0.3.x / harness-cli v0.2.1 — [strands-agents/sdk-python Releases](https://github.com/strands-agents/sdk-python/releases)
- 2026-10：AWS 开源 Strands Decider 2B（基于 Qwen3.5-2B、指针头打分候选项的决策模型，用于路由/工具选择/分类/guardrails，RTX 3090 中位延迟约 115ms）与 Strands Box（开发者预览，内核级隔离 + Dogwood 策略语言，按工具参数与历史动作放行/拒绝，可与不同模型和框架配合）— [InfoQ 2026-10-16](https://www.infoq.com/news/2026/10/aws-strands-agents/)
- 2026-03 AWS 推出 Strands Labs 承载实验项目（仅见 InfoQ 标题）— [InfoQ 2026-03](https://www.infoq.com/news/2026/03/aws-strands-agents/)

**Amazon Bedrock AgentCore**
- 2025-10-13 GA：Runtime 保留 8 小时执行窗口与会话隔离并新增 A2A 支持；Memory 新增自管理策略；Gateway 可连接现有 MCP 服务器并支持 IAM 授权；Identity 增加身份感知授权与 refresh token 保险库；全面支持 VPC、PrivateLink、CloudFormation — [AWS What's New 2025-10](https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-bedrock-agentcore-available)
- FAQ：可与任意框架（LangChain、Strands Agents、CrewAI 等）及任意模型（Bedrock 内外）集成 — [AgentCore FAQ](https://aws.amazon.com/bedrock/agentcore/faqs/)
- 2026-06-17 AgentCore Harness GA：声明式配置模型、工具、skills、指令，由 AWS 运行编排循环、工具执行、上下文窗口管理、状态持久化、失败恢复与会话隔离；模型解耦、可在会话中途切换 provider 不丢上下文；一条 CLI 命令导出为 Strands 代码（Claude Agent SDK 导出"coming soon"）；含每 agent 隔离文件系统与 shell、跨会话记忆、AWS 精选 skills 目录、网页浏览/搜索、经策略网关访问工具、内置身份/记忆/观测 — [AWS What's New 2026-06-17](https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-agentcore-harness-generally-available/)
- 二手来源称 2026-07-30 起 Amazon Bedrock Agents 更名为 "Bedrock Agents Classic" 并停止接受新客户（单一来源，未核实）— [cipherprojects.com](https://www.cipherprojects.com/blog/posts/bedrock-agents-vs-agentcore-strands/)

**采用度**
- Stack Overflow 2026 调查：Strands 4.0%（178 人）— [Stack Overflow Survey 2026 AI data](https://survey.stackoverflow.co/2026/ai/data)

### Inferences
- **优势**："模型驱动"让简单 agent 代码量极少，复杂度交给模型推理；多 agent 原语齐全（agents-as-tools / handoffs / swarm / graph）且原生 A2A；provider 广泛（Bedrock、Anthropic、OpenAI、Gemini、Ollama、LiteLLM）；从本地进程到 AgentCore 托管运行时有平滑路径（AgentCore Harness 可导出为 Strands 代码，即"先托管、后掌控"）；AWS 在执行安全（Strands Box 策略沙箱）上投入明显。
- **重点场景**：AWS 上的企业 agent（需要 IAM、VPC、PrivateLink、合规）、需长时间运行（8 小时）与会话隔离的任务、要接入大量既有 API/Lambda/MCP 的工具集成型 agent、对执行策略有硬性要求的场景；AgentCore 本身也适合托管非 Strands 框架（LangGraph、CrewAI）的 agent。
- **锁定程度**：SDK 层低（开源、多 provider、"any cloud"）；运行时层若用 AgentCore 则与 AWS 绑定，但 AgentCore 框架无关，降低了"框架锁定"。
- **弱点**：社区规模明显小于 LangChain/OpenAI/ADK（调查仅 4.0%）；默认与示例偏 Bedrock/AWS；版本号增长极快（1.0→1.61 约 15 个月），API 面持续扩张（harness、decider、box、labs），学习面变宽。

### Gaps
- 未找到 Strands 2026 年最新下载量官方数据（只有 1.0 时的 150K）。
- Bedrock Agents "Classic" 更名信息仅有单一二手来源。
- AgentCore Harness 定价未核实。

## Q5. 2025–2026 新出现的其他主要厂商 SDK

### Takeaway
最重要的新增是 Microsoft Agent Framework（Semantic Kernel + AutoGen 合并，2026-04-02 1.0 GA，.NET/Python），它在 2026 年把 harness 与 Foundry Hosted Agents 推到 GA，并可直接编排 Claude Agent SDK 与 GitHub Copilot SDK。Google 还有基于 Antigravity IDE 同源基础设施的 Antigravity SDK（2026-10 新增本地模型）。整体趋势是各厂商从"SDK"走向"托管 harness + 沙箱 + 治理"：OpenAI Agents API、Claude Managed Agents、AgentCore Harness、Foundry Hosted Agents 在 2026 年相继推出。

### Cited Findings
**Microsoft Agent Framework**
- 作为 Semantic Kernel 与 AutoGen 的开源整合于 2025-10 发布（InfoQ 2025-10 报道）；1.0 GA 于 2026-04-02，Build 2026（6 月 2–3 日）将 Agent Harness、GitHub Copilot SDK 与 Claude Agent SDK connectors、多 agent 编排模式推到 stable；之后 harness 与 Foundry Hosted Agents GA；1.0 让两个前身进入维护模式 — [InfoQ 2026-08-03](https://www.infoq.com/news/2026/08/agent-framework-harness-ga/)
- 其他来源称 1.0 为 2026-04-03，覆盖 .NET 与 Python，稳定 API + 长期支持承诺；2026-02 发布 RC — [Visual Studio Magazine 2026-04-06](https://visualstudiomagazine.com/articles/2026/04/06/microsoft-ships-production-ready-agent-framework-1-0-for-net-and-python.aspx)；[InfoQ 2026-02 RC](https://www.infoq.com/news/2026/02/ms-agent-framework-rc/)；[Microsoft Tech Community](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/the-future-of-agentic-ai-inside-microsoft-agent-framework-1-0/4510698)
- Harness 内容：函数调用、按调用持久化历史、context compaction、带 plan/execute 模式的 todo list、文件记忆、skills、web search、工具审批、内置 OpenTelemetry（默认开启可移除）；shell、文件访问、后台子 agent、自动循环需显式开启；`create_harness_agent(...)` 一次调用接线；Foundry Hosted Agents 按消耗计费；编排模式含 sequential、parallel、Magentic（源自 Magentic-One）且共用一个 API — [InfoQ 2026-08-03](https://www.infoq.com/news/2026/08/agent-framework-harness-ga/)
- InfoQ 引用 MBZUAI 论文"Dive into Claude Code"：泄露的 Claude Code v2.1.88 约 51.2 万行代码中约 98.4% 属于 harness 基础设施（权限、上下文管理、沙箱、工具路由、恢复），仅约 1.6% 是 AI 决策逻辑（作者自承是基于泄露包的行数分类）— [InfoQ 2026-08-03](https://www.infoq.com/news/2026/08/agent-framework-harness-ga/)

**Google Antigravity SDK**
- Antigravity SDK 与 Antigravity IDE 共享底层 agent 基础设施，SDK 用于以编程方式构建自有 agent；2026-10 新增本地模型支持（首发 Gemma 4 26B A4B via LiteRT，并支持 Ollama、LM Studio、vLLM 等 OpenAI 兼容本地服务器），主打 Architect-Builder 混合编排（云端架构师规划、本地 builder 执行，演示中 97.2% token 在本地、源码不上云）— [InfoQ 2026-10-14](https://www.infoq.com/news/2026/10/antigravity-sdk-local-models/)；[Google Developers Blog](https://developers.googleblog.com/introducing-support-for-local-ai-models-in-the-antigravity-sdk/)

**托管 harness 的同质化趋势**
- OpenAI Agents API（2026-09-10 公测，托管 Codex harness）— [OpenAI API Changelog](https://developers.openai.com/api/docs/changelog)
- Claude Managed Agents（beta）— [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)
- AgentCore Harness（2026-06-17 GA）— [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-agentcore-harness-generally-available/)
- DigitalOcean Managed Agents（2026-10，仅见 InfoQ 标题）— [InfoQ](https://www.infoq.com/news/2026/10/digitalocean-managed-agents/)

**其他出现在调查中的厂商栈**
- Stack Overflow 2026 调查中 Meta 的 Llama Stack 达 17.4%（767 人），Semantic Kernel 5.0%、AutoGen 4.5%（Microsoft Agent Framework 未作为单独选项列出）— [Stack Overflow Survey 2026 AI data](https://survey.stackoverflow.co/2026/ai/data)

### Inferences
- **Microsoft Agent Framework 优势**：.NET 一等支持（其他厂商 SDK 均无），企业治理（身份、内容安全、OTel、Foundry）完整，且能把 Claude/Copilot 编码 agent 作为受治理成员编排——适合 Azure/.NET 企业与"多厂商 agent 统一治理"场景。
- **行业共性**：2026 年厂商竞争焦点从"SDK 原语"转向"harness 质量 + 托管沙箱 + 治理/观测"。四家（OpenAI、Anthropic、AWS、Microsoft）都已提供托管 harness；harness 形态趋同（文件系统 + shell + compaction + skills + subagents + 审批 + MCP）。
- Antigravity SDK 代表"IDE agent 能力 SDK 化 + 本地/云混合"的新方向，与 Claude Agent SDK（Claude Code 的库化）路线相似。

### Gaps
- Microsoft Agent Framework 的 A2A / MCP / AG-UI 支持细节未在本次调研中逐项核实。
- Antigravity SDK 首发日期、语言支持未核实。
- 未调研 Mistral Agents API、xAI、阿里（Qwen-Agent/AgentScope）等其他厂商 SDK。

## Q6. MCP、A2A（及 AG-UI）：治理与采用现状、哪些框架支持、如何影响框架选择与锁定

### Takeaway
MCP（agent↔工具/数据，"纵向"）与 A2A（agent↔agent，"横向"）在 2026 年都已进入 Linux Foundation 旗下的 Agentic AI Foundation（AAIF）：MCP 是 2025-12-09 AAIF 的创始项目，A2A 于 2026-08-17 加入；MCP 发布了迄今最大的 2026-07-28 版规范（无状态化），月 SDK 下载近 5 亿；A2A 在 2026 年 3–4 月发布 v1.0。所有主要厂商 SDK 都原生支持 MCP，ADK、Strands、AgentCore 原生支持 A2A。协议把"工具集成"和"跨框架协作"从框架中剥离出来，显著降低集成层锁定，但编排代码、harness 语义与托管运行时状态仍是锁定来源。AG-UI（CopilotKit）是 agent↔前端 UI 的事实标准候选，但治理仍在单一公司。

### Cited Findings
**AAIF 治理**
- 2025-12-09 Linux Foundation 宣布成立 Agentic AI Foundation，以 Anthropic 的 MCP、Block 的 goose、OpenAI 的 AGENTS.md 为首批项目；白金会员包括 AWS、Anthropic、Block、Bloomberg、Cloudflare、Google、Microsoft、OpenAI — [Linux Foundation 新闻稿](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)；[SD Times](https://sdtimes.com/ai/linux-foundation-forms-agentic-ai-foundation-to-be-new-home-for-mcp-goose-and-agents-md/)
- A2A 于 2026-08-17 成为 AAIF 托管项目（Axios 独家报道；部分媒体写 8-20）；A2A 自 2025-06 已是 LF 项目，这次是 LF 内部转入 AAIF；AAIF 会员从不足 40 家增至 250+；与 MCP、goose、AGENTS.md、agentgateway 并列 — [Axios 2026-08-17](https://www.axios.com/2026/08/17/a2a-agentic-ai-foundation-open-ai-standards)（经搜索摘要，原文抓取失败）；[Forbes 2026-08-19](https://www.forbes.com/sites/janakirammsv/2026/08/19/agent2agent-joins-the-agentic-ai-foundation-alongside-mcp/)；[FlowHunt](https://www.flowhunt.io/blog/agentic-ai-foundation-a2a-mcp-standards/)
- 各协议保留各自维护者、规范流程与发布节奏 — [practicallogix](https://www.practicallogix.com/the-2026-agent-interoperability-reset-a2a-mcp-under-aaif/)（二手）

**MCP 现状**
- 2026-07-28 版规范：从有状态双向协议改为无状态请求/响应（废除 `initialize` 握手与 `Mcp-Session-Id`，可选 `server/discover`）；Multi Round-Trip Requests 取代服务器发起的 sampling/elicitation/roots；Streamable HTTP 需带 `Mcp-Method`/`Mcp-Name` 头便于路由；list 结果可缓存（`ttlMs`）；正式扩展框架——Tasks、MCP Apps、Enterprise Managed Authorization；授权加强（RFC 9207、弃用 DCR 改用 CIMD）；Roots、Sampling、Logging 与 HTTP+SSE 传输弃用（至少 12 个月过渡）— [MCP Blog: The 2026-07-28 Specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- 采用数据：Tier 1 SDK 合计每月近 5 亿次下载，TypeScript 与 Python SDK 各自累计超 10 亿；Tier 1 = TypeScript、Python、Go、C#，Rust beta；首席维护者 David Soria Parra 称这是"自远程 MCP 首发以来最重要的版本" — [MCP Blog](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- AAIF 也发布了该版本迁移指南 — [AAIF Blog](https://aaif.io/blog/mcp-2026-07-28-whats-changing-and-how-to-migrate)；Google、AWS 撰文支持无状态 MCP（AWS 称可去除会话亲和性要求）— [Google Developers Blog](https://developers.googleblog.com/scaling-ai-agent-infrastructure-with-the-mcp-stateless-updates/)；[InfoQ 2026-09](https://www.infoq.com/news/2026/09/aws-stateless-mcp/)

**A2A 现状**
- 历史：A2A 由 Google 于 2025-04 发起；2025-06-23 Linux Foundation 宣布托管 A2A，创始成员 AWS、Cisco、Google、Microsoft、Salesforce、SAP、ServiceNow，当时已有 100+ 公司支持 — [Linux Foundation 新闻稿](https://linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)；[Google Developers Blog](https://developers.googleblog.com/google-cloud-donates-a2a-to-linux-foundation/)
- v1.0：一源称 v1.0.0 于 2026-03-12 发布，另有来源称 2026-04；2026-05 的 v1.0.1 为当前补丁版；三种绑定 JSON-RPC 2.0 over HTTPS、gRPC、HTTP+JSON/REST；v1.0.0 有 16 项破坏性变更（如移除 part 的 `kind` 字段）— [testmuai](https://www.testmuai.com/blog/a2a-protocol-v1/)；[packetnebula](https://packetnebula.com/articles/a2a-joins-aaif-v1-migration/)（二手，日期存在冲突）

**框架支持情况（本次核实到的）**
- MCP：OpenAI Agents SDK 内置 MCP（Python 0.20.0 起兼容 MCP Python SDK v1 与 v2）— [OpenAI Agents SDK 文档](https://openai.github.io/openai-agents-python/)；[Releases](https://github.com/openai/openai-agents-python/releases)；Responses API / Agents API 支持 MCP 与 Secure MCP Tunnel — [OpenAI API Changelog](https://developers.openai.com/api/docs/changelog)；Claude Agent SDK 与 Managed Agents 支持 MCP — [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)；ADK 支持 MCP 工具及作为 MCP server — [adk.dev](https://adk.dev/)；Strands 内置 MCP（并已实现 MCP SEP-2663 任务执行）— [sdk-python](https://github.com/strands-agents/sdk-python)；AgentCore Gateway 连接现有 MCP 服务器 — [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-bedrock-agentcore-available)；官方 MCP C# SDK v2.0 — [.NET Blog](https://devblogs.microsoft.com/dotnet/announcing-v20-of-the-official-mcp-csharp-sdk/)
- A2A：ADK 提供 Python/Go/Java/Kotlin 的 A2A 快速入门 — [adk.dev](https://adk.dev/)；Strands 1.0 起支持 A2A — [AWS Open Source Blog](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-1-0-production-ready-multi-agent-orchestration-made-simple/)；AgentCore Runtime GA 时加入 A2A — [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-bedrock-agentcore-available)

**AG-UI**
- AG-UI 标准化 agent 与用户界面的连接（流式聊天、前端工具调用、状态共享、HITL）；获 Google、Microsoft、Amazon、Oracle 及 LangChain、Mastra、PydanticAI、Agno 等框架支持；背后公司 CopilotKit 于 2026-05 融资 2700 万美元 — [TechCrunch 2026-05-05](https://techcrunch.com/2026/05/05/copilotkit-raises-27m-to-help-devs-deploy-app-native-ai-agents/)；[GeekWire](https://www.geekwire.com/2026/seattles-copilotkit-raises-27m-as-some-of-the-biggest-names-in-tech-adopt-its-ai-agent-protocol/)；使用量数字多为厂商自报 — [CopilotKit Blog](https://www.copilotkit.ai/blog/ag-ui-is-redefining-the-agent-user-interaction-layer)
- OpenAI 的 ChatKit 是其自有的 agent 聊天前端方案，与 AG-UI 定位相近 — [OpenAI: Introducing AgentKit](https://openai.com/index/introducing-agentkit/)

### Inferences
- **MCP 降低工具层锁定**：五大厂商 SDK + AgentCore Gateway 都原生支持 MCP，一个 MCP server 可被任何框架复用，"为某框架写工具适配"的沉没成本基本消失，框架切换成本下降。
- **A2A 降低多 agent 层锁定**：不同团队可分别用 ADK、Strands、LangGraph 等构建 agent，再经 A2A 互通，框架选择可以"按团队/按 agent"局部化，而不必全公司统一。A2A 的原生支持目前在 Google/AWS 阵营最成熟；OpenAI 与 Anthropic SDK 是否原生支持 A2A 本次未能确认。
- **未被协议解决的锁定**：编排代码（handoff/graph/workflow 语义）、harness 行为（compaction、权限、skills 语义）、托管运行时的服务端状态（会话、沙箱文件系统、事件历史）仍是迁移成本；托管 agent 服务（Agents API、Managed Agents）的不支持 ZDR、数据驻留限制等是新的锁定维度。
- **对选型的含义**：在 2026 年，"是否支持 MCP"已是门槛项而非差异项；差异化在于 harness 质量、模型能力、托管运行时与治理。选型时应把工具实现为 MCP server、跨团队协作走 A2A，把框架当作可替换的"编排胶水"。
- MCP 2026-07-28 是大改（无状态化 + 弃用 sampling/roots），短期内各 SDK 的协议版本兼容性会成为实际问题（例如 OpenAI Python SDK 需同时兼容 MCP SDK v1/v2）。

### Gaps
- AAIF 关于 A2A 加入的官方新闻稿原文未能抓取（依赖 Axios/Forbes 摘要）；A2A v1.0 精确发布日期存在 3 月 12 日与 4 月的冲突。
- 未找到 A2A 的权威生产采用数据（组织数、部署数）。
- 未核实 AG-UI 是否已进入 AAIF 或其他中立基金会。
- 未核实 OpenAI Agents SDK、Claude Agent SDK、Microsoft Agent Framework 的 A2A 原生支持情况。

## Q7. 总体趋势：厂商 SDK 是否在蚕食 LangChain / CrewAI 等第三方框架？分析师与社区怎么说

### Takeaway
有可靠数据显示厂商 SDK 已占据显著份额但未取代第三方框架：Stack Overflow 2026 调查中 LangChain 30.2% 仍居首，OpenAI Agents SDK 23.8% 紧随其后，LangGraph 18.8%、Llama Stack 17.4%、Google ADK 14.0%，CrewAI 仅 5.5%、Strands 4.0%；同时"Terminal Use"（直接轻量编排）达 18.9%，68% 的开发者偏好可预测的单 agent。社区存在持续的"直接用 SDK、去框架化"情绪，但未见 LangChain 被大规模放弃的证据；也未找到 Gartner/Forrester 类分析师的市场份额数据。

### Cited Findings
- Stack Overflow 2026"过去一年用过的 agent 编排/框架"（n=4,400）：LangChain 30.2%（1,329）、OpenAI Agents SDK 23.8%（1,048）、Terminal Use 18.9%、LangGraph 18.8%、Llama Stack 17.4%、Google ADK 14.0%、Hermes Agent 10.2%、Vercel AI SDK 9.0%、Pydantic AI 8.9%、CrewAI 5.5%、Semantic Kernel 5.0%、AutoGen 4.5%、Strands 4.0%、DSPy 3.6%、Mastra 3.0%、Dify 2.9%、Smolagents 2.6%、Agno 2.4% 等；调查评论称 "Terminal Use" 19% 说明许多开发者偏好直接、轻量的编排 — [Stack Overflow Survey 2026 AI data](https://survey.stackoverflow.co/2026/ai/data)
- 同一调查称 AI 记忆与 agent 编排工具"现有采用与声明兴趣之间存在显著差距"，该品类仍在找定位；相比之下编码 agent 市场更成熟（Claude Code 66%、GitHub Copilot 59%）— [Stack Overflow Survey 2026 AI](https://survey.stackoverflow.co/2026/ai)
- Stack Overflow 2026-04 脉冲调查（约 1,100 人）：68% 偏好可预测的单 agent 而非复杂多 agent 配置 — [Stack Overflow Blog 2026-05-27](https://stackoverflow.blog/2026/05/27/agents-on-a-leash-agentic-ai-remains-mostly-monitored-at-work/)
- 下载量代理指标（二手、口径含 CI/镜像流量）：2026-07 快照 LangChain 约 3.09 亿/30 天、LangGraph 约 6,650 万、CrewAI 约 1,080 万；另一来源给出 LangGraph 3,450 万/月、CrewAI 520 万/月，数字随来源和时间差异大 — [the-agent-report.com 2026-07](https://the-agent-report.com/2026/07/ai-agent-frameworks-comparison-2026-langgraph-crewai-autogen/)；[letsdatascience](https://letsdatascience.com/blog/ai-agent-frameworks-compared)（低可信度）
- 社区观点："模型请求工具→执行→回传→循环"只需约 40 行代码，不需要框架依赖 — [dev.to field guide](https://dev.to/moksh/picking-an-ai-agent-framework-in-2026-a-python-and-typescript-field-guide-20o8)；"LLM frameworks replaced by agent SDKs" 类文章 — [MindStudio](https://www.mindstudio.ai/blog/llm-frameworks-replaced-by-agent-sdks/)（观点类）
- 历史：Hacker News 2024-06 热帖 "Why we no longer use LangChain"（id=40739982）抱怨多层抽象 — [Hacker News](https://news.ycombinator.com/item?id=40739982)（经搜索摘要）；LangChain 与 LangGraph 于 2025-10 达到 1.0 并承诺 2.0 前无破坏性变更（二手）— [futureagi](https://futureagi.com/blog/best-langchain-production-llm-alternatives-2026/)
- 厂商自身的"退守代码层"信号：OpenAI 下线可视化 Agent Builder，推荐迁移到 Agents SDK — [OpenAI Deprecations](https://developers.openai.com/api/docs/deprecations)
- 托管运行时的框架中立化：AgentCore 明确支持 LangChain、Strands、CrewAI 等任意框架 — [AgentCore FAQ](https://aws.amazon.com/bedrock/agentcore/faqs/)；Microsoft Agent Framework 可直接编排 Claude Agent SDK 与 GitHub Copilot SDK — [InfoQ 2026-08-03](https://www.infoq.com/news/2026/08/agent-framework-harness-ga/)
- 博客层面的普遍定位：LangGraph 被视为复杂有状态生产工作流的默认选项，CrewAI 偏快速原型；厂商 SDK 在"已押注单一模型厂商"时最强，代价是锁定 — [requesty.ai](https://www.requesty.ai/blog/best-ai-agent-sdks-compared-2026-langchain-crewai-openai-anthropic-google)；[particula.tech](https://particula.tech/blog/langgraph-vs-crewai-vs-openai-agents-sdk-2026)（二手）

### Inferences
- **份额格局**：厂商 SDK 已成为主流选项之一（OpenAI Agents SDK 与 LangChain 仅差约 6 个百分点，ADK 14% 接近 LangGraph 的 75%），第三方框架中受冲击最明显的是"多 agent 角色扮演"类（CrewAI 5.5%、AutoGen 4.5%）；LangChain/LangGraph 依靠模型中立与生态仍保持领先。
- **驱动因素**：(1) 模型厂商把 harness 能力（compaction、沙箱、computer use、tool search）放进自家 API 与 SDK，第三方框架只能追随；(2) MCP 让工具生态不再是第三方框架的护城河；(3) 开发者偏好单 agent + 轻量编排（68%、Terminal Use 19%），削弱了重框架的必要性。
- **反向力量**：多模型/多云需求、厂商产品退役风险（Agent Builder 一年即下线）、托管服务的合规限制（ZDR、数据驻留），使"模型中立框架 + MCP/A2A"仍有稳固需求。
- **选型速查（基于上文已引用事实归纳）**：

| SDK | 语言 | 首发 / 当前版本（2026-10） | 核心抽象 | 模型无关性 | 最适合场景 |
|---|---|---|---|---|---|
| OpenAI Agents SDK | Python, TS | 2025-03 / Py 0.24.0、TS 0.21.0 | Agent、Handoff、Guardrail、Session、Tracing、Sandbox agent、Realtime | 中（LiteLLM/Any-LLM 适配，新功能偏 OpenAI） | OpenAI 模型的客服/分诊多 agent、语音 agent、沙箱长任务；托管选 Agents API |
| Claude Agent SDK | Python, TS（其他语言走 CLI 子进程） | 2025-09（更名）/ Py 0.2.170、TS 0.3.306 | Claude Code harness：内置工具、权限、hooks、subagents、skills、plugins、sessions、MCP | 低（仅 Claude，多云渠道） | 编码 agent、需要"一台电脑"的长时程自主 agent；托管选 Managed Agents |
| Google ADK | Python, TS, Go, Java, Kotlin | 2025-04 / Py 2.12.0（2.0 GA 2026-05） | Agent、Workflow Runtime 图节点、多 agent 层级、Task API、Eval | 中高（多适配器，Gemini 优化） | Google Cloud 企业多 agent、确定性+LLM 混合工作流、A2A 跨组织协作 |
| AWS Strands | Python, TS | 2025-05 预览、2025-07 1.0 / Py 1.61.1、TS 1.21.0 | 模型驱动 Agent、agents-as-tools、handoff、swarm、graph、Harness | 高（Bedrock/Anthropic/OpenAI/Gemini/Ollama/LiteLLM） | AWS 合规企业 agent、AgentCore 托管长任务、强执行策略场景 |
| MS Agent Framework | .NET, Python | 2025-10 预览、2026-04 1.0 | Agent、Harness、Workflow（sequential/parallel/Magentic） | 中高 | Azure/.NET 企业、多厂商编码 agent 统一治理 |

### Gaps
- 未找到 Gartner、Forrester、IDC 等分析师对 agent 框架市场份额的量化报告。
- Stack Overflow 调查未把 Claude Agent SDK、Microsoft Agent Framework 列为选项，无法与其他框架直接比较。
- 未找到 2026 年 Hacker News/Reddit 上专门讨论"厂商 SDK 取代 LangChain"的高质量帖子链接（只有 2024 年历史热帖与二手博客转述）。
- PyPI/npm 下载量的权威一手统计未在本次调研中获取（如 pepy.tech、npm 官方统计）。
