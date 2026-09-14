# AI 智能体研发学习蓝图（6 个月 · Python · 对标大厂 JD）

> 版本 v1.0 · 2026-09-09 · 项目：langGraph-learn
> 适用对象：十年资深研发，理论概念已有基本了解、几乎未写过 LLM 应用代码；每周 8–12 小时；目标是 6 个月后以"AI 智能体研发"身份对标大厂 JD 跳槽/转岗。

---

## 0. 一页纸总览

| 维度 | 设定 |
|---|---|
| 起点 | 理论为主，几乎没写过 LLM 应用代码 |
| 终点 | 能独立设计、实现、评测并交付一个多 Agent 系统；作品集覆盖 JD 表中全部"必备"与"新兴·高频"项，并能对每一项讲出可量化的结果 |
| 周期 | 6 个月 / 26 周，按每周 10 小时计约 260 小时（弹性区间 210–310 小时） |
| 主线框架 | LangGraph（本项目的主线）；RAG 侧配 LlamaIndex；低代码侧以 Dify 做对照 |
| 语言栈 | Python 3.12+，用 uv 管依赖，Docker 跑 Milvus / Elasticsearch |
| 交付物 | 5 个渐进式项目 + 1 个毕业项目（每个都带评测集与 README）、1 套面试题库、3–5 篇技术笔记 |
| 验收方式 | 每月末一次里程碑验收，逐条对照第 6 节的 Definition of Done |

**三条贯穿始终的原则**

1. **项目驱动、评测先行。** 每个项目在写 Agent 之前先写 10 条测试用例。这是 JD 里"评测"一项的入口，也是把"会用"变成"高级"的唯一途径——面试时能不能说出"改了 X 之后指标从 71% 到 84%"，是档位的分水岭。
2. **主线一条，广度靠对照。** LangGraph 深挖到源码级；LangChain / LlamaIndex / Dify / CrewAI / AutoGPT 用"读设计 + 做一次同任务对照实验"的方式覆盖，不平均用力。
3. **用资深研发的肌肉记忆。** 状态机、契约设计、可观测、幂等重试、测试金字塔，这些老本行直接迁移到 Agent 工程上，这是你与应届 AI 方向候选人拉开差距的地方，也是 JD 里"设计并实施复杂的多 Agent 协作方案"真正考察的东西。

---

## 1. 目标定义

### 1.1 终局画像：市场语境下的"AI 智能体专家"

从图中 JD 的措辞看，大厂招的不是"会调 API 的人"，而是能对**非确定性系统做工程化**的人。拆成三层：

- **能设计**：把一个业务问题拆成合适的形态——单 Agent、确定性工作流、还是多 Agent 协作；并且知道什么时候*不该*用 Agent。
- **能交付**：RAG + Tool-Use + Memory + MCP 接入 + 部署 + 可观测，端到端跑在生产环境里。
- **能证明**：有评测集、有指标、有回归，能把"感觉变好了"说成数字。

### 1.2 六个月可验收目标（G1–G7）

| 编号 | 目标 | 验收证据（6 个月末必须拿得出来） |
|---|---|---|
| G1 | 高级 Prompt 工程与结构化输出 | 不依赖框架手写 tool-calling 循环；有 Prompt 版本化与评测记录，能展示迭代前后分数变化 |
| G2 | 生产级 RAG | Milvus 与 Elasticsearch 各跑通一遍；混合检索 + Rerank；Ragas 评测报告，faithfulness ≥ 0.85 |
| G3 | LangGraph 单 Agent → 多 Agent 编排 | 带持久化、Human-in-the-loop、长期记忆的 Agent；Supervisor 编排 ≥ 3 个子 Agent，有并行分支 |
| G4 | MCP / Skills / Connector 生态 | 自建 ≥ 3 个 MCP 服务器打通模拟的 CRM / ERP / OA；写 ≥ 2 个符合 Agent Skills 标准的 Skill |
| G5 | 评测体系 | 统一评测集 ≥ 150 条；LLM-as-Judge 与人工标注一致性 ≥ 0.8；评测跑在 CI 里做回归 |
| G6 | 上下文工程 / Harness 工程 / SDD | 对一个 Agent 做上下文优化并量化 token 下降；用 SDD（spec → plan → tasks）完整交付一个项目 |
| G7 | 求职就绪 | 简历里 6 个项目每个一句带数字的描述；面试题库 8 主题 × 10 题；3 篇公开技术笔记 |

---

## 2. 市场对标：JD 技能表（原文收录）

以下为你提供的 JD 分析表，作为本蓝图的验收基准原样收录。

### 大模型应用栈（真正区分档位的地方）

| 技能 | 频率 | JD 原文级细节 |
|---|---|---|
| **RAG / 向量检索** | 必备 | 几乎全部 JD。配 Milvus / Elasticsearch 等向量数据库。 |
| **Agent 开发与多智能体编排** | 必备 | 字节要求"设计并实施复杂的多 Agent 协作方案"；阿里云要求"多 Agent 编排、Tool-Use、Memory 管理"。 |
| **MCP / Skills / Connector 生态** | 新兴 · 高频 | 腾讯要求通过 MCP 打通客户 CRM / ERP / OA；MiniMax 与中软国际的交付物直接写明"MCP 服务器、子 Agent、Agent Skills"。这是 2026 年 JD 相对 2025 年最明显的新增。 |
| Prompt 工程（高级） | 必备 | 各家都写"高级"而非"会用"。 |
| 上下文工程 / Harness 工程 / SDD | 新兴 · 中频 | 腾讯云服务 JD 的特征词汇，反映 AI Coding 与 Agent Runtime 的最新实践。 |
| 框架 | — | LangChain、LangGraph、LlamaIndex、Dify、AutoGPT、CrewAI。 |
| 评测 | 新兴 · 中频 | LLM-as-Judge、Auto-rater、评测集构建、回归用例移交。 |

### 2.1 JD 技能 → 蓝图覆盖映射

| JD 技能 | 频率 | 主要覆盖阶段 | 目标深度 | 作品集证据 |
|---|---|---|---|---|
| RAG / 向量检索 | 必备 | 第 2 月（第 5 月做评测升级） | 能选型、能调优、能评测；Milvus 与 ES 都上手 | P2 企业知识库问答 + Ragas 报告 |
| Agent 开发与多智能体编排 | 必备 | 第 3–4 月 | LangGraph 源码级理解；Supervisor / 并行 / Handoff 三种模式 | P3 单 Agent、P4 多 Agent 系统 |
| MCP / Skills / Connector 生态 | 新兴 · 高频 | 第 4 月 | 读懂 2026-07-28 规范；能写服务器与客户端；能写 Skill | P4 中的 3 个 MCP 服务器 + 2 个 Skills |
| Prompt 工程（高级） | 必备 | 第 1 月起步，第 5 月评测驱动升级 | 结构化输出、prompt chaining、缓存、版本化、评测驱动迭代 | P1 的 promptfoo 用例与迭代记录 |
| 上下文工程 / Harness 工程 / SDD | 新兴 · 中频 | 第 5 月 | 能做 compaction、子 Agent 隔离、just-in-time 检索；能用 SDD 交付 | P5 的上下文优化报告 + spec 文档 |
| 框架 | — | 第 3 月主线 + 第 6 月对照周 | LangGraph 深、其余能讲清取舍 | 一篇六框架对照笔记 |
| 评测 | 新兴 · 中频 | 第 2 月入门，第 5 月体系化 | LLM-as-Judge 设计与校准、Auto-rater、评测集构建、回归移交 | P5 评测与回归平台 |

---

## 3. 能力模型与资深研发的迁移策略

### 3.1 四层能力模型

| 层 | 内容 | 对应月份 |
|---|---|---|
| L1 模型交互层 | API 与消息格式、结构化输出、Tool-Use 协议、流式、token 与成本、prompt caching | 第 1 月 |
| L2 检索与知识层 | 分块、Embedding 选型、向量库、混合检索、Rerank、RAG 评测、高级 RAG 模式 | 第 2 月 |
| L3 编排与运行时层 | 状态图、持久化 / checkpoint、HITL、Memory、多 Agent 模式、MCP / Skills、Harness | 第 3–4 月 |
| L4 质量与工程层 | 离线 / 在线评测、可观测、上下文工程、SDD、部署、成本与安全 | 第 5–6 月 |

### 3.2 可以直接复用的老本行

| 你已有的能力 | 在 Agent 工程里的对应物 |
|---|---|
| 状态机 / 工作流引擎 | LangGraph 的 State、Node、Edge、Reducer、Checkpointer |
| 微服务契约与接口设计 | 工具 Schema 设计、MCP 服务器的 tools / resources / prompts 设计 |
| 日志、tracing、指标 | LangSmith / OpenTelemetry 对 Agent 的 trace 与成本观测 |
| 测试金字塔 | 评测金字塔：Prompt 单元测试 → 组件评测（检索、单工具）→ 端到端评测 |
| 幂等、重试、超时、熔断 | Agent 可靠性：per-node timeout、错误处理节点、优雅停机、可恢复 checkpoint |
| Code review 与 spec 文化 | SDD：spec → plan → tasks，把需求变成可验证的合约 |

### 3.3 需要"换脑子"的三件事

1. **非确定性。** 同一输入不同输出，测试从"断言相等"变成"评分与阈值"。这也是为什么评测必须先行。
2. **上下文是稀缺资源。** 不是把所有东西塞进 Prompt；上下文工程本质上是资源管理——什么时候加载、加载多少、什么时候压缩、什么时候隔离到子 Agent。
3. **让模型做决定 vs. 让代码做决定。** Workflow（代码控制流程）与 Agent（模型控制流程）的取舍是 Anthropic《Building Effective Agents》的核心观点，也是面试系统设计题的常见考点：能用确定性工作流解决的，不要上 Agent。

---

## 4. 六个月路线图

每个月的结构固定为：目标 → 理论输入 → 动手实践 → 里程碑项目 → 验收标准 → JD 对应项。4 周的月份（第 1、2、3、6 月）按约 40–43 小时估算，5 周的月份（第 4、5 月，内容最重）按约 50 小时估算；每月大致为理论 8–14 小时、项目 25–30 小时、评测复盘与写作 4–8 小时，合计与 26 周 × 10 小时的总预算相当。

### 阶段 0：准备周（第 0 周，约 6 小时）

- 环境：Python 3.12、uv、VS Code 或 Cursor、Docker（用来跑 Milvus 与 Elasticsearch）。
- 仓库：建一个 monorepo `langgraph-learn`，每个项目一个子目录（`p1-cli-assistant/`、`p2-rag/` …），根目录放 `docs/`（学习日志）与 `evals/`（评测集）。
- 模型：至少一个国内 API（DeepSeek，或阿里云百炼的通义千问）+ 一个海外 API（Claude 或 OpenAI）。前者便宜、适合大量实验；后者在 MCP、Skills、Tool-Use 的生态配合上最顺。本地 Ollama 可选。预算每月 ¥50–150 足够。
- 账号：LangSmith（免费层）、GitHub、Hugging Face。
- 规范：每周一条学习日志（模板见第 5 节）；每个项目目录必须有 README、`evals/` 和一个可一键运行的入口。

### 第 1 个月：模型交互与高级 Prompt（第 1–4 周）

**目标**：不靠任何框架，把 LLM 应用最底层的四件事跑通——对话与流式、结构化输出、工具调用循环、Prompt 的版本化与评测。

**理论输入（约 12 小时）**
- Anthropic《Building Effective Agents》——先建立"Workflow vs Agent"的判断框架。
- Anthropic / OpenAI 官方 Prompt Engineering 文档：system prompt 设计、few-shot、chain-of-thought、prompt chaining、结构化输出（JSON Schema / Pydantic）、prompt caching。
- 论文 ReAct（Yao et al., 2022）：理解"推理 + 行动"循环的原始形态。
- Anthropic Academy《Building with the Claude API》或 OpenAI 对应的 API 文档，任选一家精读，另一家过一遍差异。

**动手实践（约 25 小时）**
- 用原生 SDK 手写：多轮对话、streaming、Pydantic 结构化输出、tool calling 循环（自己写 while 循环处理 tool_use → tool_result）。
- 用 promptfoo 建立 ≥ 20 条 Prompt 用例，做 3 轮 Prompt 迭代，记录每轮分数。
- 记录每次调用的 token 与费用，做一张成本表。

**里程碑项目 P1：命令行研发助手**
一个 CLI 工具，能读本地代码仓库、执行受限 shell 命令、总结 `git diff` 并生成 commit message。工具调用循环全部手写，工具权限白名单化。

**验收标准**
- 手写 tool-calling 循环通过 10 条以上的多步工具调用用例；结构化输出 100% 通过 schema 校验。
- promptfoo 用例 ≥ 20 条，有迭代前后的分数对比。
- 能清楚解释：temperature / top_p、上下文窗口、token 计费、prompt caching、function calling 的协议细节、流式事件格式。

**JD 对应**：Prompt 工程（高级）、Agent 开发（基础）。

### 第 2 个月：RAG 与向量检索（第 5–8 周）

**目标**：搭出一条可评测的生产级 RAG 管线，Milvus 与 Elasticsearch 都上手，并用指标说明每个优化点的收益。

**理论输入（约 12 小时）**
- 分块策略（固定窗口、递归、语义、按文档结构）与它们对召回的影响。
- Embedding 选型：bge-m3、Qwen3-Embedding、text-embedding-3 系列；中文场景的评测口径（C-MTEB）。
- Milvus 架构与索引类型（HNSW、IVF）；Elasticsearch 的 BM25 + kNN 混合检索；RRF 融合；Rerank（bge-reranker-v2-m3）。
- RAG 评测指标：faithfulness、answer relevancy、context precision / recall；Ragas 论文与文档。
- 高级 RAG 概览：query rewriting、HyDE、parent-document retrieval、GraphRAG（只需理解适用场景）。
- LlamaIndex 官方文档的 RAG 部分——它是 RAG 侧最成体系的框架，也是 JD 框架列表的一员。

**动手实践（约 25 小时）**
- Docker 起 Milvus 与 Elasticsearch；同一份语料分别入库，对比纯向量、纯 BM25、混合检索三种召回。
- 加 Rerank 前后对比；调分块大小与 overlap 做消融实验。
- 用 Ragas 建 ≥ 50 条评测集（问题 + 标准答案 + 参考片段），跑出评测报告。

**里程碑项目 P2：企业知识库问答**
选一个有真实体量的文档集（某开源项目的完整文档，或你熟悉行业的公开规范文档），构建入库 → 检索 → 生成 → 引用溯源的完整管线，LlamaIndex 与手写管线各实现一版做对照。

**验收标准**
- Milvus 与 ES 各有一套可运行的配置；混合检索 + Rerank 的 context recall 相对纯向量有可量化提升。
- Ragas 评测集 ≥ 50 条，faithfulness ≥ 0.85，并有一份说明每个优化点收益的报告。
- 能回答面试常见题："为什么召回了却答错""分块怎么定""什么时候该用 GraphRAG"。

**JD 对应**：RAG / 向量检索（必备）、评测（入门）、框架（LlamaIndex）。

### 第 3 个月：LangGraph 与单 Agent 工程化（第 9–12 周）

**目标**：把 LangGraph 学到源码级，做出一个带持久化、人工审批、长期记忆和完整 trace 的生产形态 Agent。

**理论输入（约 12 小时）**
- LangGraph 核心概念：StateGraph、Node、Edge、Reducer、Command、Send、Subgraph；Checkpointer 与 durable execution；`interrupt` 实现 Human-in-the-loop；Store 实现长期记忆；Streaming 模式。
- LangGraph 1.x 的工程特性：per-node 超时与错误处理、优雅停机与可恢复 checkpoint、Delta Channel（长会话消息历史增量存储）、v3 事件流协议。
- LangChain 1.x 的 `create_agent` 与 middleware 机制；Deep Agents（LangChain 的开源 agent harness）。
- 课程：LangChain Academy 的《Introduction to LangGraph》与《Foundation: Introduction to Deep Agents》；《Quickstart: LangSmith Essentials》。
- 读一遍 LangGraph 的 Pregel 执行引擎源码（`langgraph/pregel/`），理解 superstep 与 channel 模型——这是你作为资深研发最能发挥的地方。

**动手实践（约 25 小时）**
- 把 P1 的手写循环改写成 LangGraph 图；对比两种实现的可维护性。
- 接入 PostgreSQL / SQLite Checkpointer，实现会话恢复与时间旅行（回退到某个 checkpoint 重跑）。
- 在写操作前加 `interrupt` 做人工审批；用 Store 做跨会话的用户偏好记忆。
- 全链路接入 LangSmith tracing，观察每个节点的 token 与延迟。

**里程碑项目 P3：研发知识助手（P1 + P2 的 LangGraph 版）**
一个能查知识库（P2）、也能操作代码仓库（P1）的 Agent：持久化会话、写操作需人工确认、记住用户偏好、支持子图复用、全链路可观测。

**验收标准**
- 图结构清晰，有 ≥ 1 个子图、≥ 1 个条件边、≥ 1 个 interrupt。
- 进程重启后会话可恢复；能演示回退到某个 checkpoint 重新执行。
- LangSmith 上有完整 trace；能给出每次对话的平均 token 与 P95 延迟。
- 能讲清 LangGraph 的 superstep / channel 模型，以及它与 LangChain `create_agent` 的关系。

**JD 对应**：Agent 开发（Tool-Use、Memory 管理）、框架（LangGraph、LangChain）。

### 第 4 个月：多 Agent 编排 + MCP / Skills 生态（第 13–17 周）

**目标**：做出 JD 原文描述的那种系统——"通过 MCP 打通 CRM / ERP / OA"，并由多 Agent 协作完成跨系统任务。这是 2026 年 JD 相对 2025 年最明显的新增项，也是本蓝图最重的一个月（5 周）。

**理论输入（约 14 小时）**
- 多 Agent 模式：Supervisor、层级式、Swarm / Handoff、用 `Send` 实现的并行 map-reduce；何时不该拆多 Agent（上下文碎片化、成本翻倍）。Anthropic《How we built our multi-agent research system》是最好的案例文章。
- MCP 规范 2026-07-28 版：无状态核心（每个请求自带版本、身份与能力）、多轮往返请求（MRTR，工具可中途向用户要输入）、基于 Header 的路由、可缓存的 list 结果、授权加固（CIMD、RFC 9207）、Tasks 扩展与正式的扩展框架。对比 2025-11 版理解演进方向。
- MCP Python SDK：tools / resources / prompts 三类原语，stdio 与 Streamable HTTP 传输，OAuth 授权。
- Agent Skills 开放标准（agentskills.io，Anthropic 发起并开源）：`SKILL.md` 的 frontmatter（`name`、`description`）、`scripts/` `references/` `assets/` 目录约定、渐进式加载的设计理念。
- 课程：Anthropic Academy《Introduction to Model Context Protocol》《Model Context Protocol: Advanced Topics》《Introduction to agent skills》《Introduction to subagents》。
- A2A（Agent-to-Agent）协议只需概览，能说清它与 MCP 的分工。

**动手实践（约 28 小时）**
- 用 FastAPI + SQLite 各写一个 mock 的 CRM、ERP、OA 服务（客户、报销、日程），每个服务配一个 MCP 服务器（含 tools 与 resources，其中至少一个工具用 MRTR 向用户要缺失参数）。
- 写一个 MCP 客户端接入 LangGraph；同时在 Claude Code 或其他支持 MCP 的客户端里验证互操作。
- 用 LangGraph 实现 Supervisor 编排三个子 Agent，并做一版 Swarm / Handoff 对照。
- 写 2 个 Agent Skills（例如「周报生成」「合同要点提取」），在支持 Skills 的客户端里跑通。

**里程碑项目 P4：企业办公多 Agent 系统**
一个 Supervisor Agent 编排销售查询、报销审批、日程协调三个子 Agent，全部通过自建 MCP 服务器访问模拟的 CRM / ERP / OA；报销审批含人工确认；配套两个可复用的 Skill。

**验收标准**
- ≥ 3 个 MCP 服务器，通过 MCP Inspector 检查；至少一个跨系统任务（如"给上季度前三大客户安排回访并预提差旅报销"）端到端跑通。
- Supervisor 与 Swarm 两种编排对同一任务集的成功率、token、延迟对比表。
- ≥ 2 个符合标准的 Skill，能在两个不同客户端里加载。
- 能就 MCP 无状态化、授权、MRTR 讲出"为什么这样设计"。

**JD 对应**：Agent 开发与多智能体编排（必备）、MCP / Skills / Connector 生态（新兴 · 高频）。

### 第 5 个月：评测体系 + 上下文工程 / Harness 工程 / SDD（第 18–22 周）

**目标**：把前四个项目从"能跑"升级为"可证明"，同时补齐 JD 里两个新兴项。这个月的产出是面试时最能拉开档位的部分。

**理论输入（约 14 小时）**
- 评测金字塔：Prompt 单元测试 → 组件评测（检索质量、单工具正确率）→ 端到端任务评测 → 在线评测与 A/B。
- LLM-as-Judge：rubric 设计、pairwise 对比、位置偏差与冗长偏差的缓解、Judge 与人工标注的一致性校准（论文《Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena》及后续综述）。
- Auto-rater 与评测集构建：从生产 trace 采样、合成数据生成、黄金集的版本管理；"回归用例移交"——把评测集当作测试资产交付给 QA 或下游团队的流程。
- 工具：LangSmith Evaluate、Ragas、DeepEval、promptfoo；各选一个场景用一遍，理解取舍。
- 上下文工程：Anthropic《Effective context engineering for AI agents》；compaction、子 Agent 上下文隔离、just-in-time 检索、记忆文件；Anthropic《Writing effective tools for agents》。
- Harness 工程：OpenAI《Harness Engineering》、Anthropic 关于长时任务 harness 设计的文章；awesome-harness-engineering 总结的十一个设计原语（agent loop、规划与任务拆解、上下文投递与压缩、工具设计、Skills 与 MCP、权限、记忆与状态、任务运行器与编排、验证与 CI、可观测、human-in-the-loop）。
- SDD（Spec-Driven Development）：GitHub Spec Kit 与 Kiro 的 spec → plan → tasks 工作流；用它来驱动 AI Coding，也用它来定义 Agent 的行为合约。

**动手实践（约 26 小时）**
- 为 P2 / P3 / P4 建统一评测集（合计 ≥ 150 条），混合规则评分与 LLM-as-Judge。
- 对 30 条样本做人工标注，计算 Judge 一致性并迭代 rubric 直到 ≥ 0.8。
- 把评测接入 GitHub Actions，每次 PR 自动跑回归并输出对比。
- 对 P4 做一次上下文工程优化（压缩历史、子 Agent 隔离、按需加载工具描述），量化 token 下降与成功率变化。
- 用 SDD 方式（先写 spec，再 plan，再 tasks）完成 P5 本身。

**里程碑项目 P5：Agent 评测与回归平台**
一个统一的评测集管理、Judge 评分、CI 回归与报告生成工具，覆盖前三个项目；附带一份"回归用例移交文档"，模拟交付给 QA 团队。

**验收标准**
- 评测集 ≥ 150 条，Judge 与人工一致性 ≥ 0.8，CI 每次 PR 自动跑。
- 上下文优化报告：token 下降 ≥ 30% 且成功率不降。
- P5 的 spec / plan / tasks 三份文档齐全，代码与 spec 一致。
- 能回答："你的 Judge 怎么校准""评测集怎么防止过拟合""上下文压缩会丢什么"。

**JD 对应**：评测（新兴 · 中频）、上下文工程 / Harness 工程 / SDD（新兴 · 中频）、Prompt 工程（高级——评测驱动的迭代）。

### 第 6 个月：毕业项目、框架对照与求职（第 23–26 周）

**目标**：把所有能力收束成一个可展示的端到端系统，补齐框架广度，完成求职材料。

**理论输入（约 8 小时）**
- 部署与运维：LangSmith Deployment 或自建 FastAPI + 队列；成本上限、速率限制、降级策略。
- 安全：prompt injection、工具权限最小化、敏感数据脱敏；OWASP LLM Top 10。
- 框架对照周：Dify、CrewAI、AutoGPT 各做一个同任务实验（建议复用 P4 的一个子任务），写一篇六框架取舍笔记——JD 列的每个框架都要能说出适用场景与局限。

**动手实践（约 30 小时）**

**毕业项目 P6：垂直场景的端到端 Agent 平台**
选一个与目标公司业务相近的场景（例如面向研发团队的"需求分析 + 代码审查 + 知识问答"平台，或客服 / 运营场景），综合 RAG、多 Agent、MCP、评测与部署；交付完整 README、架构图、评测报告、成本报告、部署说明。

**求职材料**
- 简历：6 个项目每个一句 STAR 式带数字的描述（模板见第 7 节）。
- 面试题库：8 个主题（Prompt、RAG、LangGraph、多 Agent、MCP / Skills、评测、上下文工程、系统设计）× 10 题，每题写下自己的回答要点。
- 系统设计演练：至少两道，如"设计一个电商客服多 Agent 系统""设计一个企业内部 MCP 网关"。
- 3 篇公开技术笔记（知乎 / 掘金 / 公众号 / 博客均可），建议主题：LangGraph 执行模型解析、MCP 2026 规范的无状态化解读、LLM-as-Judge 校准实践。

**验收标准**
- P6 可一键部署，有评测报告与成本报告。
- 六框架对照笔记完成。
- 简历、题库、3 篇笔记齐全；完成至少 2 次模拟面试（可以由我扮演面试官）。

**JD 对应**：全部七项的综合验收。

---

## 5. 每周节奏模板（8–12 小时）

| 时段 | 时长 | 内容 |
|---|---|---|
| 输入 | 2–3 小时 | 文档 / 课程 / 论文，**带着当周项目的具体问题读**，不做无目标的通读 |
| 动手 | 5–7 小时 | 项目代码，拆成两次 2.5–3.5 小时的深度时段，效果远好于每天 1 小时 |
| 评测与复盘 | 1 小时 | 跑评测、看 trace、更新学习日志 |
| 输出 | 0.5–1 小时 | 每周一条学习笔记；每月一篇长文或一次项目 README 完善 |

**学习日志模板（每周一条，放在 `docs/journal/`）**

```
## Week N（日期）
- 本周做了什么（3 行以内）
- 一个数字：本周项目里能量化的一个结果
- 一个坑：踩了什么、怎么解决
- 一个问题：还没想明白的事（下周输入阶段优先解决）
- 面试视角：如果面试官问这周的东西，我会怎么讲
```

---

## 6. 里程碑验收清单（Definition of Done）

| 月末 | 项目 | 必须满足 |
|---|---|---|
| M1 | P1 命令行研发助手 | 手写 tool loop 通过 10+ 多步用例；promptfoo ≥ 20 条并有迭代对比；成本表 |
| M2 | P2 企业知识库问答 | Milvus 与 ES 双实现；混合检索 + Rerank 有量化收益；Ragas ≥ 50 条，faithfulness ≥ 0.85 |
| M3 | P3 研发知识助手 | 子图 + 条件边 + interrupt；重启可恢复与时间旅行；LangSmith 全链路 trace 与 P95 延迟 |
| M4 | P4 企业办公多 Agent 系统 | ≥ 3 个 MCP 服务器；跨系统任务端到端；Supervisor vs Swarm 对比表；≥ 2 个 Skill 跨客户端可用 |
| M5 | P5 评测与回归平台 | 评测集 ≥ 150 条；Judge 一致性 ≥ 0.8；CI 回归；上下文优化 token 降 ≥ 30%；spec / plan / tasks 齐全 |
| M6 | P6 毕业项目 + 求职材料 | 一键部署；评测与成本报告；六框架笔记；简历 + 题库 + 3 篇笔记；2 次模拟面试 |

每次验收后在本文件末尾的"进度追踪"里打勾，并把项目 README 与评测报告存进 langGraph-learn 项目。

---

## 7. 作品集 → JD 技能 → 简历映射

| 项目 | 覆盖 JD 技能 | 简历一句话（示例，数字用你的真实结果替换） |
|---|---|---|
| P1 命令行研发助手 | Prompt 工程（高级）、Agent 基础 | 不依赖框架实现工具调用循环与权限白名单；通过 promptfoo 20+ 用例驱动 3 轮 Prompt 迭代，任务通过率由 X% 提升至 Y% |
| P2 企业知识库问答 | RAG / 向量检索、评测 | 基于 Milvus / Elasticsearch 构建混合检索 + Rerank 管线，Ragas 评测 50+ 条，context recall 提升 X%，faithfulness 达 0.8X |
| P3 研发知识助手 | Agent 开发、Memory 管理、框架 | 用 LangGraph 实现带持久化、人工审批与长期记忆的 Agent，支持会话恢复与 checkpoint 回溯，全链路 LangSmith 可观测 |
| P4 企业办公多 Agent 系统 | 多智能体编排、MCP / Skills / Connector | 自建 3 个 MCP 服务器打通 CRM / ERP / OA，Supervisor 编排 3 个子 Agent 完成跨系统任务，成功率 X%；产出 2 个可复用 Agent Skills |
| P5 评测与回归平台 | 评测、上下文工程 / Harness / SDD、Prompt 工程 | 建立 150+ 条评测集与 LLM-as-Judge（人工一致性 0.8X），接入 CI 回归；上下文工程优化使 token 下降 X% 且成功率不降；以 SDD 方式交付 |
| P6 毕业项目 | 全部 | 端到端交付垂直场景 Agent 平台，含部署、评测与成本报告 |

---

## 8. 资源清单（免费优先）

**官方文档与课程**
- LangChain / LangGraph 官方文档与 changelog（docs.langchain.com），LangGraph 目前为 1.2.x（2026-05），LangChain 1.3.x。
- LangChain Academy（academy.langchain.com）：Introduction to LangGraph、Foundation: Introduction to Deep Agents、Quickstart: LangSmith Essentials、Foundation: Introduction to LangSmith Deployment。
- Anthropic Academy（anthropic.skilljar.com）：Building with the Claude API、Introduction to Model Context Protocol、MCP: Advanced Topics、Introduction to agent skills、Introduction to subagents、Claude Code in Action。
- MCP 官方规范与博客（modelcontextprotocol.io / blog.modelcontextprotocol.io），重点读 2026-07-28 版发布说明与 2026 路线图。
- Agent Skills 标准（agentskills.io，GitHub agentskills/agentskills）。
- Hugging Face Agents Course（免费，偏框架无关的基础）；DeepLearning.AI 的 Agent / RAG / 评测系列短课（每门 1–2 小时，用来快速补某个点）。
- Milvus 官方文档与 Zilliz 的 RAG 教程；Elasticsearch 向量检索与混合检索文档；Ragas、DeepEval、promptfoo、LangSmith 文档。

**必读文章**
- Anthropic：《Building Effective Agents》《How we built our multi-agent research system》《Effective context engineering for AI agents》《Writing effective tools for agents》。
- OpenAI：《A practical guide to building agents》《Harness Engineering》。
- HumanLayer《12-Factor Agents》；awesome-harness-engineering（GitHub ai-boost）。
- GitHub Spec Kit 与 Kiro 的 SDD 文档。

**论文（按月份对应）**
- M1：ReAct（Yao et al., 2022）。
- M2：RAGAS（Es et al., 2023）；Lost in the Middle（Liu et al., 2023）；Self-RAG。
- M3–M4：Generative Agents（Park et al., 2023）；MCP 与 A2A 规范本身当论文读。
- M5：Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena（Zheng et al., 2023）；一篇 2025–2026 年的 LLM-as-Judge 综述。

**模型与基础组件（中文场景）**
- 模型 API：DeepSeek、阿里云百炼（通义千问）、火山方舟（豆包）、Kimi；海外 Claude / OpenAI / Gemini。
- Embedding / Rerank：bge-m3、Qwen3-Embedding、bge-reranker-v2-m3。
- 向量库：Milvus（含 Milvus Lite 本地版）、Elasticsearch；对照可看 pgvector、Qdrant。

---

## 9. 风险与反模式（资深研发容易踩的坑）

- **课程囤积症。** 只看不做。规则：任何课程时间不得超过当周项目时间的三分之一，看到能动手的点就停下来做。
- **框架跳跃。** 同时学五个框架，每个都停在 quickstart。规则：LangGraph 是唯一主线，其余只做对照实验。
- **没有评测的 Demo。** 面试时说不出任何数字，"感觉效果不错"是最弱的回答。规则：先写用例再写 Agent。
- **过早追新、死记 API。** MCP 规范每半年一变，LangGraph 每季度有新特性。学"为什么这样设计"（无状态化解决什么问题、checkpoint 为什么要可回溯），API 细节现查。
- **把 Agent 当银弹。** 确定性工作流能解决的不要上 Agent，多 Agent 会带来上下文碎片化和成本翻倍——这也是面试系统设计题的常见陷阱。
- **忽视成本与安全。** 从 P1 起就记成本，从 P3 起就做工具权限最小化和 prompt injection 防护；大厂 JD 不写但面试必问。
- **用老经验硬套。** 状态机思维是优势，但"断言相等"式的测试思维要换成"评分与阈值"；不要试图把非确定性"修掉"。

---

## 10. 在 langGraph-learn 项目中的推进方式

本文件是项目总纲。建议的协作节奏：

- **第 0 周**：由我生成环境搭建清单与 monorepo 骨架，以及 P1 的 spec 文档（顺便从第一天就用 SDD 的方式工作）。
- **每周**：你把学习日志贴进项目，我根据日志里的"一个问题"给下周的输入清单，并对代码做 review。
- **每月末**：你把项目 README 与评测报告存进项目，我按第 6 节逐条验收，然后更新下方的进度追踪。
- **第 6 月**：我扮演面试官做模拟面试，并帮你打磨简历上的项目描述。

时间安排上有两个可调项：若某月进度落后，优先压缩该月的理论输入而不是项目；若整体提前，把多出来的时间投入第 5 月（评测与上下文工程），这是投入产出比最高的部分。

---

## 进度追踪

- [ ] 第 0 周：环境、仓库、模型 API、账号就绪
- [ ] M1 · P1 命令行研发助手（验收日期：____）
- [ ] M2 · P2 企业知识库问答（验收日期：____）
- [ ] M3 · P3 研发知识助手（验收日期：____）
- [ ] M4 · P4 企业办公多 Agent 系统（验收日期：____）
- [ ] M5 · P5 评测与回归平台（验收日期：____）
- [ ] M6 · P6 毕业项目 + 求职材料（验收日期：____）
- [ ] 六框架对照笔记
- [ ] 3 篇公开技术笔记
- [ ] 2 次模拟面试
