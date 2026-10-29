# 低代码 / 可视化 AI 智能体平台 与 中国智能体框架生态（截至 2026-10-21）

> 研究说明：GitHub 星数、许可证、最新版本、最近提交时间均于 **2026-10-21** 通过 GitHub API（`gh api repos/...`）实时获取，引用对应仓库链接即为数据来源。新闻/媒体类信息标注了发布日期；第三方博客、自媒体可信度较低的信息已明确标注。

**GitHub 快照（2026-10-21 采集）**

| 项目 | 星数 | 许可证（GitHub 识别） | 最新版本（日期） | 最近 push | 状态 |
|---|---|---|---|---|---|
| n8n-io/n8n | 208,190 | NOASSERTION（Sustainable Use License） | n8n@2.44.5（2026-10-21） | 2026-10-21 | 活跃 |
| langgenius/dify | 159,104 | NOASSERTION（改版 Apache 2.0） | 1.17.1（2026-09-10） | 2026-10-21 | 活跃 |
| langflow-ai/langflow | 155,885 | MIT | v1.12.7（2026-10-21） | 2026-10-21 | 活跃 |
| infiniflow/ragflow | 92,581 | Apache-2.0 | v1.0.0-rc2（2026-10-16） | 2026-10-21 | 活跃 |
| bytedance/deer-flow | 84,230 | MIT | v2.1.0（2026-09-24） | 2026-10-21 | 活跃 |
| FlowiseAI/Flowise | 55,512 | NOASSERTION（Apache 2.0 + 企业目录商业许可） | flowise@3.1.4（2026-07-29） | 2026-08-13 | **已归档（archived=true）** |
| agentscope-ai/agentscope | 33,581 | Apache-2.0 | v2.0.10（2026-10-12） | 2026-10-21 | 活跃 |
| labring/FastGPT | 29,889 | NOASSERTION（改版 Apache 2.0） | v4.17.2（2026-10-09） | 2026-10-21 | 活跃 |
| 1Panel-dev/MaxKB | 23,006 | GPL-3.0 | v2.10.7-lts（2026-10-15） | 2026-10-21 | 活跃 |
| coze-dev/coze-studio | 21,738 | Apache-2.0 | v0.5.1（2026-02-05） | 2026-07-29 | 更新明显放缓 |
| QwenLM/Qwen-Agent | 17,200 | Apache-2.0 | GitHub release v0.0.26（2025-05）；PyPI 0.0.34（2026-02-16） | 2026-03-04 | 更新放缓 |
| cloudwego/eino | 13,371 | Apache-2.0 | v0.9.22（2026-10-19） | 2026-10-19 | 活跃 |
| langchain4j/langchain4j | 13,270 | Apache-2.0 | 1.22.0（2026-10-08） | 2026-10-21 | 活跃 |
| jd-opensource/joyagent-jdgenie | 11,931 | Apache-2.0 | v1.0.0（2025-09-18） | 2026-02-12 | 放缓 |
| alibaba/spring-ai-alibaba | 11,044 | Apache-2.0 | v1.1.2.2（2026-03-10）；v2.0.0-M1.1（2026-06-25） | 2026-10-07 | 活跃 |
| spring-projects/spring-ai | 9,558 | Apache-2.0 | 2.0.1（2026-08-21）；2.1.0-M1（2026-09-25） | 2026-10-16 | 活跃 |
| agentscope-ai/agentscope-java | 6,066 | Apache-2.0 | v2.0.4（2026-10-08） | 2026-10-21 | 活跃 |
| coze-dev/coze-loop | 5,782 | Apache-2.0 | v1.5.1（2026-01-20） | 2026-10-21 | 活跃 |

来源：[dify](https://github.com/langgenius/dify)、[n8n](https://github.com/n8n-io/n8n)、[langflow](https://github.com/langflow-ai/langflow)、[ragflow](https://github.com/infiniflow/ragflow)、[deer-flow](https://github.com/bytedance/deer-flow)、[Flowise](https://github.com/FlowiseAI/Flowise)、[agentscope](https://github.com/agentscope-ai/agentscope)、[FastGPT](https://github.com/labring/FastGPT)、[MaxKB](https://github.com/1Panel-dev/MaxKB)、[coze-studio](https://github.com/coze-dev/coze-studio)、[Qwen-Agent](https://github.com/QwenLM/Qwen-Agent)、[qwen-agent PyPI](https://pypi.org/project/qwen-agent/)、[eino](https://github.com/cloudwego/eino)、[langchain4j](https://github.com/langchain4j/langchain4j)、[joyagent-jdgenie](https://github.com/jd-opensource/joyagent-jdgenie)、[spring-ai-alibaba](https://github.com/alibaba/spring-ai-alibaba)、[spring-ai](https://github.com/spring-projects/spring-ai)、[agentscope-java](https://github.com/agentscope-ai/agentscope-java)、[coze-loop](https://github.com/coze-dev/coze-loop)（均为 2026-10-21 GitHub API 数据）

---

## Q1. Dify：定位、增长、1.x 功能、许可证、企业采用与最佳场景

### Takeaway
Dify（LangGenius, Inc.）是全球星数第二的可视化 LLM 应用 / Agentic Workflow 平台（159k 星），1.x 系列从 2025-02 的插件体系一路演进到 2026 年的知识流水线、事件触发、人机协同（HITL）、多人协作以及 **沙箱型 Dify Agent + Skills**；其许可证是"带限制的改版 Apache 2.0"（禁止未授权多租户运营、不得去除前端 LOGO），对 SaaS 化二次分发不友好但对企业内部自用友好。最佳场景是"企业内部私有化部署的 RAG 知识助手 + 可视化业务工作流 + 面向业务人员的 AI 应用工厂"。

### Cited Findings
**基本信息 / 增长**
- 仓库创建于 2023-04-12；截至 2026-10-21 星数 159,104、fork 25,146；最新版本 1.17.1（2026-09-10）。仓库自我描述："Build Agentic workflows, RAG pipelines… Deploy on cloud, VPC, or self-hosted" — [GitHub langgenius/dify](https://github.com/langgenius/dify)
- 2026-03-10 Dify 宣布完成 3,000 万美元 Series Pre-A，由 HSG（原文写作 HSG）领投，GL Ventures、Alt-Alpha Capital、5Y Capital（五源，老股东）、Mizuho Leaguer Investment、NYX Ventures 跟投 — [Dify 官方博客](https://dify.ai/blog/dify-raises-30m-tomorrow-s-organizations-will-be-built-by-people-and-agents)；[IT Brief](https://itbrief.co.uk/story/dify-raises-usd-30m-to-scale-open-source-ai-workflows)
- 官方披露（2026-03）：GitHub 第 51 名最多星开源项目；安装于 "more than 1.4 million machines"；覆盖 "over 175 countries and regions"；"Over 2,000 teams" 和 "280 enterprises"（原文措辞，未说明是否均为付费客户）；愿景 "Many People. Many Agents. One Simple Way to Work."；资金投向：生产级 Agent/Workflow、企业基础能力（性能、合规、权限、审计）、降低非开发者门槛、开源生态 — [Dify 官方博客](https://dify.ai/blog/dify-raises-30m-tomorrow-s-organizations-will-be-built-by-people-and-agents)
- 第三方估值数据：Caplight 列出估值约 1.8 亿美元（未经公司确认）— [Caplight](https://www.caplight.com/company/langgenius-co)；Dealroom 记录 2024-08 一轮 280 万美元融资、投资方含阿里云 — [Dealroom](https://dealroom.co/companies/langgenius/)

**1.x 关键版本演进（均来自 GitHub release notes）**
- **1.0.0（2025-02-28）**：推出插件系统（`.difypkg`），把模型、工具从核心解耦为插件；Workflow 新增 Agent 节点，Agent 策略可由插件定义（不再局限于内置 CoT 等）；新增 Extension 插件（处理外部 Webhook）；上线 Dify Marketplace — [Dify v1.0.0](https://github.com/langgenius/dify/releases/tag/1.0.0)
- **1.6.0（2025-07-10）**：内置双向 MCP 支持（作为 MCP 客户端调用工具、把工作流发布为 MCP Server）— [Dify v1.6.0](https://github.com/langgenius/dify/releases/tag/1.6.0)
- **1.7.0（2025-07-23）** 工具 OAuth & 插件自动升级；**1.8.0（2025-08-27）** 异步工作流、多模型管理 — [Dify releases](https://github.com/langgenius/dify/releases)
- **1.9.0（2025-09-22）**：**Knowledge Pipeline**（可视化节点式文档摄取编排，多数据源插件：本地文件/在线文档/云盘/爬虫，模板与 Pipeline DSL 导入导出，新增 Q&A 分块处理器）+ **基于队列的图执行引擎**；官方点名的 RAG 痛点："restricted integration of data sources / missing critical elements such as tables and images / suboptimal chunking results" — [Dify v1.9.0](https://github.com/langgenius/dify/releases/tag/1.9.0)
- **1.10.0（2025-11-13）**：事件驱动工作流 / Trigger（定时、SaaS 事件如 Slack/GitHub/Linear、Webhook），仅 Workflow 支持 — [Dify v1.10.0](https://github.com/langgenius/dify/releases/tag/1.10.0)
- **1.11.0（2025-12-11）** 多模态知识库；**1.12.0（2026-02-03）** Summary Index — [Dify releases](https://github.com/langgenius/dify/releases)
- **1.13.0（2026-02-11）**：Human Input 节点（HITL：暂停-审阅-编辑-按"批准/拒绝/升级"按钮路由，可通过 Webapp 或 Email 下发）；执行引擎重构为 Celery worker + Redis Pub/Sub，大规模部署需新增 `workflow_based_app_execution` 队列 — [Dify v1.13.0](https://github.com/langgenius/dify/releases/tag/1.13.0)
- **1.14.0（2026-04-29）**：多人实时协同编辑工作流（自托管默认关闭）、HITL Service API — [Dify v1.14.0](https://github.com/langgenius/dify/releases/tag/1.14.0)
- **1.15.0（2026-06-25）**：`difyctl` 命令行客户端（让"personal agents, scripts, and CI pipelines can invoke Dify workflows"）、工作流中展示 CoT 思考面板、长耗时模型轮询 — [Dify v1.15.0](https://github.com/langgenius/dify/releases/tag/1.15.0)
- **1.16.0（2026-07-17）**：**Dify Agent（Beta）**——运行在 Linux 沙箱中的 shell 型 Agent，支持上传 Skills/文件、对话式构建 Agent、可嵌入 Workflow 节点；官方警告"only to trusted, non-malicious users"；MCP 升级到 2025-06-18 协议 — [Dify v1.16.0](https://github.com/langgenius/dify/releases/tag/1.16.0)
- **1.17.0（2026-08-25）**：E2B 云沙箱后端、Home Snapshot、工作区级 Skill 管理（draft→publish→version）、上下文感知历史压缩、可复用 LLM 环境变量、HITL 支持在循环/迭代内、厂商中立统一 Tracing（Phoenix/LangSmith 适配器）、Azure Key Vault / KMS、TiDB 混合检索 — [Dify v1.17.0](https://github.com/langgenius/dify/releases/tag/1.17.0)

**许可证**
- Dify 采用 "a modified version of the Apache License 2.0"：(a) 未经书面授权不得用 Dify 源码运营多租户环境（一个 workspace = 一个租户）；(b) 使用前端（`web/` 目录或 web 镜像）时不得移除/修改 LOGO 和版权信息；贡献者须同意生产方可调整协议、贡献代码可用于商业云服务；另声明"交互设计受外观专利保护" — [Dify LICENSE](https://github.com/langgenius/dify/blob/main/LICENSE)

**企业采用**
- Dify 企业版页面点名客户：Maersk、Yum!、Thermo Fisher、Mizuho、Lilly、Panasonic、ANKER、Novartis、Kakaku.com、Glencore、NTT East、Ricoh、Volvo、ETS、Lion 等，日本企业居多；**页面未列出中国大陆企业**。数据：Maersk 每个 AI 应用构建 2 周（自研需 4 个月）、CX-Assist 主要咨询处理时间缩短 90%+；Kakaku.com 工作流搭建从 1 个月降至 1 天；Lion FY2025 培训 100 名业务用户构建 Agent。企业版提供 SAML/OIDC SSO、细粒度 RBAC、SCIM、防篡改审计日志、PII 脱敏、BYOK、多租户隔离、Helm/Terraform、完全离线部署 — [Dify 企业版（中文）](https://dify.ai/zh/enterprise)
- 国内私有化落地案例：搜索到的多为服务商/营销性质文章，数字无法核实（例如某 Dify 合作伙伴称"147 家国内中大型企业中 83% 的项目 6 个月内被迫重构"，来源不明且带推销意图）— [CSDN（JOTO 撰文，可信度低）](https://adg.csdn.net/6a50912310ee7a33f28c0a08.html)

### Inferences
- **优势**：① 功能最全的"一站式"开源 LLM 应用平台（RAG + Workflow/Chatflow + Agent + 插件市场 + MCP 双向 + 可观测）；② 私有化部署成熟（Docker Compose / Helm / 离线），适合数据不出域的国内企业；③ 社区与生态规模最大（星数、插件市场），中文资料丰富；④ 2026 年快速吸收"沙箱 Agent + Skills + HITL + CLI"新范式，降低被 coding agent 替代的风险。
- **重点解决的问题场景**：企业知识库问答/客服 Copilot（借 Knowledge Pipeline 解决分块、表格图片丢失问题）；文档审核、发票稽核等需要固定流程 + 人工审批的业务流（HITL）；事件驱动的自动化（Trigger）；让业务人员在 IT 治理下自助构建 AI 应用（企业版 RBAC/审计）；作为"AI 中台/后端即服务"被其他系统通过 API/MCP/CLI 调用。
- **弱点/风险**：许可证限制多租户 SaaS 与去 LOGO，ISV 若要做多租户产品需买商业授权；1.13 起执行架构更复杂（Celery 队列、独立 Redis），大规模自托管运维成本上升；版本迭代快、升级需迁移（1.0 插件迁移、1.13 新队列）；Dify Agent 沙箱仍是 Beta，官方明确仅对可信用户开放。

### Gaps
- 未找到可核实的中国大陆知名企业 Dify 落地案例（官方页面未列中国大陆客户）；国内具体客户名称需向官方或权威媒体核实。
- 1.4.0/1.5.0 的核心特性未逐一核对；Dify 云版（SaaS）用户规模未披露。
- 估值仅有第三方追踪数据（约 1.8 亿美元），无公司确认。

---

## Q2. Coze Studio / Coze Loop / 扣子：开源时间、许可证、功能、与商业版关系、Eino 底座、最佳场景

### Takeaway
字节跳动于 2025 年 7 月底把扣子开发平台核心引擎（Coze Studio）和提示词/评测/观测平台（Coze Loop，源自"扣子罗盘 Coze Compass"）以 **Apache 2.0** 开源，后端 Go（基于 CloudWeGo/Eino），开源首周末即获约 9K 星。但到 2026 年，**Coze Studio 开源版更新明显放缓**（最后一个 release v0.5.1 为 2026-02-05，最近 commit 为 2026-07-29），而商业版扣子在 2026 年连续升级到 2.0（1 月，Agent Skills / Agent Plan / Agent Office / 扣子编程）和 3.0（6 月，多人多 Agent 协作、行业技能包、一键接入 Claude Code/Codex CLI/OpenClaw）。Coze Loop 开源版仍在活跃。

### Cited Findings
- 开源时间与协议：BytePlus 官方博客（2025-07-29）宣布开源 Coze Studio 与 Coze Loop，Apache 2.0，"permits commercial use without additional terms and includes clear patent licensing"；Studio 源于扣子开发平台、核心引擎"fully open"；Loop 源于企业级平台 Coze Compass — [BytePlus Blog](https://www.byteplus.com/blog/coze-open-sources-ai-agent-tools)
- 日期口径差异：国内报道称"7月26日"扣子宣布开源两款核心产品（零代码开发平台 Coze Studio、调试工具扣子罗盘 Coze Loop）— [CSDN 转载报道](https://adg.csdn.net/696f39c2437a6b403369b532.html)；官方 BytePlus 英文博客日期为 7-29 — [BytePlus Blog](https://www.byteplus.com/blog/coze-open-sources-ai-agent-tools)。（GitHub 仓库创建时间为 2025-06-24/26，首个 v0.2.1 release 为 2025-07-31 — [coze-studio releases](https://github.com/coze-dev/coze-studio/releases)）
- 热度：开源后 48 小时/一个周末约 9K 星（媒体报道）— [量子位](https://www.qbitai.com/2025/07/314155.html)；[GitCode/CSDN](https://gitcode.csdn.net/6aa0df821a35784c84209090.html)
- Coze Studio 功能（README）：模型服务管理（OpenAI、火山引擎等）、构建/发布 Agent、构建 App、可视化工作流、资源（插件/知识库/数据库/Prompt）、OpenAPI + Chat SDK；后端 Golang、前端 React + TypeScript、微服务 + DDD；最低 2 核 4GB；"derived from the 'Coze Development Platform' which has served tens of thousands of enterprises and millions of developers"；部分功能（如音色定制）仅商业版提供；官方警告公网部署存在注册、代码节点 Python 执行、SSRF、水平越权等风险 — [coze-studio README](https://github.com/coze-dev/coze-studio)
- 部署依赖较多中间件（Elasticsearch、etcd、MinIO、MySQL、RocketMQ、Redis 等），首次部署耗时较长（教程类文章）— [头条教程](https://www.toutiao.com/zixun/7536016890431522851)
- Eino 底座：coze-studio `backend/go.mod` 直接依赖 `github.com/cloudwego/eino v0.4.8` 及 eino-ext 的 ark、claude、deepseek、gemini、ollama、openai 等模型/embedding 组件 — [coze-studio go.mod](https://github.com/coze-dev/coze-studio/blob/main/backend/go.mod)
- 活跃度：coze-studio 最近 5 次提交为 2026-03-25 至 2026-07-29 的修复类提交（OAuth 防钓鱼、嵌套子工作流中断恢复等）；release 停在 v0.5.1（2026-02-05）— [coze-studio commits](https://github.com/coze-dev/coze-studio/commits/main)
- Coze Loop：面向开发者的 Agent 全生命周期平台——Prompt 开发（Playground 对比调试、版本管理）、评测（评测集/评估器/实验，按准确性、简洁性、合规性等多维评分）、可观测（SDK trace 上报、全链路记录），支持 OpenAI、火山方舟等模型；最新 v1.5.1（2026-01-20），2026-10-20 仍有评测/trace 相关提交 — [coze-loop](https://github.com/coze-dev/coze-loop)
- 扣子 2.0（2026-01-19）：品牌升级，集成 Agent Skills（技能商店，行业经验/SOP 打包为可复用模块）、Agent Plan（设定目标后长期拆解执行并主动汇报）、Agent Office（Word/PPT/Excel）、扣子编程（原开发平台升级为面向 Vibe Coding 的云端开发平台）— [IT之家](https://www.ithome.com/0/914/507.htm)；[科技日报](https://www.stdaily.com/web/gdxw/2026-01/19/content_463739.html)；[AIBase](https://www.aibase.com/zh/news/24737)
- 扣子 3.0（2026-06-03 报道）：多人多 Agent 协作、金融/自媒体/医疗/法律/科研等行业技能包、一键加载与多端同步、可一键接入 Claude Code、Codex CLI、OpenClaw 等 — [财联社](https://www.cls.cn/detail/2389018)
- 选型文章观点：无技术团队或需对接字节生态 → Coze 上手最快；但 SaaS 版"数据在字节云"，存在"依赖厂商 · 数据出域"风险 — [掘金（2026-06-11）](https://juejin.cn/post/7649984137365962761)

### Inferences
- **优势**：① 开源版 Apache 2.0 是主流可视化 Agent 平台中许可最宽松的之一（对比 Dify/FastGPT 的多租户限制、n8n 的 fair-code），可做二次开发和商业化；② 继承字节商业平台的产品设计（Agent + Workflow + 插件 + 知识库 + 数据库 + 记忆），对国内用户心智熟悉；③ Go 微服务 + DDD，适合 Go 技术栈团队深度定制；④ Coze Loop 补齐 Prompt 管理/评测/观测（LLMOps）环节，可单独与其他框架搭配使用。
- **重点解决的问题场景**：非技术/轻技术团队快速搭建对话式 Agent 和 Bot（商业版扣子，发布到抖音/飞书/微信等字节及国内渠道）；需要私有化、可商用二开的"类扣子"内部 Agent 平台（Coze Studio）；Agent 上线后的 Prompt 迭代、评测与线上观测（Coze Loop）。
- **弱点**：开源版与商业版存在功能差（音色定制等仅商业版）；开源 Studio 2026 年更新近乎停滞，跟不上商业版 2.0/3.0 的 Skills/Plan/Coding 能力，长期维护存疑；自托管中间件栈重；公网部署安全风险需自行加固。
- 字节的"开源"策略似乎呈现分层：平台（Studio）开源后维护投入下降，而框架层（Eino、DeerFlow）和 LLMOps 层（Loop）保持活跃——这一判断基于提交记录推断，未见官方表态。

### Gaps
- 扣子商业平台 2026 年的开发者数、Agent 数、企业客户数未找到官方数字（仅有开源 README 中"数万企业、数百万开发者"的定性表述）。
- 一篇 2026-07 的盘点类文章（搜索摘要）称"公有云智能体市场前三为火山引擎扣子、百度智能云千帆、腾讯云 ADP"，原文与数据来源（赛迪/IDC）未能逐字核实，不宜作为事实引用。
- 未找到字节官方关于 Coze Studio 开源版后续路线图或维护状态的声明。

---

## Q3. n8n：如何成为主流 AI Agent 工具、融资估值、fair-code 许可、AI Agent 节点、最佳场景

### Takeaway
n8n 原本是 2019 年创立的柏林工作流自动化工具，凭借"可视化画布 + 代码节点 + 大量集成"的底座叠加 LangChain 风格的 AI Agent/工具/记忆/向量库节点，成为 2025-2026 年 GitHub 星数最高的 AI 自动化平台（208k 星）。2025-10 获 1.8 亿美元 C 轮（Accel 领投，估值 25 亿美元），2026-05 SAP 战略投资使估值翻倍至 52 亿美元并将 n8n 嵌入 SAP Joule Studio。许可证为 Sustainable Use License（fair-code，非 OSI 开源）。最佳场景是"把 AI 嵌入跨 SaaS 系统的业务自动化流程"。

### Cited Findings
- 仓库创建于 2019-06-22；星数 208,190、fork 61,202；最新 n8n@2.44.5（2026-10-21）— [GitHub n8n-io/n8n](https://github.com/n8n-io/n8n)
- README 定位："The Platform for AI Agents and Workflow Automation"；"Combine a visual canvas with custom code… connect to 1500+ integrations"；可构建多步 Agent、模型无锁定（OpenAI/Anthropic/Google/开源模型）、人工审批与可观测、JS/Python/npm 代码、RBAC 与审计、9,000+ 工作流模板 — [n8n README](https://github.com/n8n-io/n8n)
- AI 能力文档：Agent、工具、记忆为构建块；一个工作流可组合多个模型；"一键"连接 MCP registry server；有专门章节解释 n8n 如何实现 LangChain 概念；支持向量数据库与 Evaluations — [n8n Advanced AI 文档](https://docs.n8n.io/advanced-ai/)
- n8n 2.0.0 于 2025-12-08 发布，以安全加固为主：默认禁用 ExecuteCommand 与 LocalFileTrigger 节点、OAuth 回调强制鉴权、默认限制文件访问目录、移除 `--tunnel` 等 — [n8n 2.0.0 release](https://github.com/n8n-io/n8n/releases/tag/n8n@2.0.0)
- C 轮（2025-10-09）：1.8 亿美元、估值 25 亿美元，Accel 领投，Meritech、Redpoint、Evantic、Visionaries Club、NVentures（英伟达）、T.Capital 参与，Felicis、Sequoia、Highland Europe、HV Capital 跟投；总融资约 2.4 亿美元 — [Crowdfund Insider](https://www.crowdfundinsider.com/2025/10/254411-berlin-automation-ai-startup-n8n-secures-180m-in-series-c-funding/)；据 Sifted，本轮经历 VC 竞价，Insight Partners 曾出价略低于 30 亿美元，签 term sheet 时（2025-08）收入据报超过 4,000 万美元（公司未确认）— [Sifted](https://sifted.eu/articles/n8n-hits-2-5bn-valuation)
- SAP 战略投资（2026-05-12）：估值 52 亿美元（较不到一年前的 25 亿翻倍），双方签署多年协议将 n8n 嵌入 SAP Joule Studio；n8n 自称拥有 1,400+ 企业客户、170 万月活开发者、1,000+ 集成；SAP 投资金额未披露 — [Bloomberg](https://www.bloomberg.com/news/articles/2026-05-12/sap-invests-in-ai-automation-startup-n8n-at-5-2-billion-value)；[Tech.eu](https://tech.eu/2026/05/12/n8n-s-valuation-doubles-to-5-2bn-following-sap-strategic-investment/)；[n8n 新闻稿（PR Newswire 转载）](https://www.bolsamania.com/nota-de-prensa_amp/mercados/n8n-valuation-doubles-to-52bn-as-sap-makes-strategic-investment-and-plans-to-embed-the-ai-platform-into-joule-studio--22470787.html)
- 第三方数据冲突：Automation Atlas 称 C 轮为 6,000 万美元/约 6 亿估值，与主流报道不符，应视为错误 — [Automation Atlas](https://automationatlas.io/answers/n8n-series-c-valuation-2025/)
- 许可证：主体为 Sustainable Use License v1.0——"You may use or modify the software only for your own internal business purposes or for non-commercial or personal use"，分发只能免费且非商业；文件名/目录含 `.ee` 的代码需 n8n Enterprise License；非 master 分支内容不授权 — [n8n LICENSE.md](https://github.com/n8n-io/n8n/blob/master/LICENSE.md)

### Inferences
- **成为 AI Agent 工具的路径**：n8n 不是"为 LLM 而生"的平台，而是把 Agent 当作自动化流程中的一种节点；其护城河是 1000+（官方另称 1500+）集成和 9000+ 模板——Agent 需要"手脚"（调用 CRM、邮件、表格、IM、数据库），n8n 天然提供；SAP 嵌入 Joule Studio 进一步把它推向企业 ERP 场景。
- **优势**：集成广度最大；可视化 + 代码混合（JS/Python 节点）兼顾运营与工程师；自托管简单；Trigger/定时/Webhook/队列模式成熟；社区模板多。
- **重点解决的问题场景**：跨系统业务自动化中加入 AI 判断（邮件分类与回复、线索打分与 CRM 写入、工单分派、报表生成、内容分发）；运营/增长团队的"AI 自动化"；把 MCP 工具与内部 API 编排成 Agent 可调用的工作流。
- **弱点**：fair-code 许可禁止把 n8n 当作商业服务对外提供（不能做"n8n 托管 SaaS"），企业功能（`.ee`）需付费；RAG/知识库能力较 Dify/RAGFlow/FastGPT 浅，偏"连接器"而非"知识引擎"；中文生态与国内 SaaS（企业微信、钉钉、飞书）集成弱于国内平台（推断，未找到量化数据）；2.0 默认禁用命令执行等节点说明其自托管曾存在较大安全面。

### Gaps
- n8n AI Agent 节点首次推出时间、AI 相关工作流占比等官方数据未在本次检索中找到。
- 中国用户规模/国内企业采用 n8n 的数据未找到。

---

## Q4. Langflow 与 Flowise：所有权与现状核实

### Takeaway
**Langflow** 归属 IBM：IBM 于 2025-02-25 宣布收购 DataStax（Langflow 的所有者），2025-05-28 完成交割；Langflow 仍以 MIT 许可在 `langflow-ai` 组织下高频发版（2026-10-21 发布 v1.12.7，155.9k 星）。**Flowise** 于 2025-08-14 被 Workday 收购，但**团队已于 2026-07-29 宣布停止运营（code freeze），2026-08-13 仓库归档，2026-08-31 EOL**，官方给出的原因是"coding agent 兴起，僵硬的低代码工作流很快触及复杂度上限"。

### Cited Findings
**Langflow**
- IBM 2025-02-25 宣布收购 DataStax，称 DataStax 是 AstraDB、DataStax Enterprise "along with Langflow" 的创造者，并承诺继续支持 Apache Cassandra、Langflow、Apache Pulsar、OpenSearch 社区 — [IBM Newsroom](https://newsroom.ibm.com/2025-02-25-ibm-to-acquire-datastax,-deepening-watsonx-capabilities-and-addressing-generative-ai-data-needs-for-the-enterprise)
- 交割：2025-05-28 正式完成 — [DBTA](https://www.dbta.com/Editorial/News-Flashes/IBM-Officially-Closes-Acquisition-of-DataStax-169711.aspx)；IBM 社区 2025-10 帖子称 2025-11-01 起 DataStax 产品销售转到 IBM 合同体系，Langflow 等将成为 IBM Elite Support 产品（属商务过渡，非法律交割日）— [IBM Community](https://community.ibm.com/community/user/blogs/datastax-pm-team-datastax-pm-team/2025/10/02/ibm-datastax)
- eWeek 报道 IBM 计划将 Langflow 集成进 watsonx.ai — [eWeek](https://www.eweek.com/fr/news/ibm-acquires-datastax/)
- 现状：MIT 许可（LICENSE 版权 "Copyright (c) 2024 Langflow"）；1.x 小版本节奏：1.3.0（2025-03-31）→1.7.0（2025-12-18）→v1.8.0（2026-03-05）→v1.12.0（2026-09-01），最新 v1.12.7（2026-10-21）；功能：可视化构建、组件可用 Python 改源码、交互式 Playground、多 Agent 编排、部署为 API 或导出 JSON、**每个 flow 可部署为 MCP Server**、LangSmith/LangFuse 可观测、Langflow Desktop（Windows/macOS）；正式发布包默认关闭自动登录 — [GitHub langflow-ai/langflow](https://github.com/langflow-ai/langflow)
- 安全事件：CVE-2025-3248（CVSS 9.8），`/api/v1/validate/code` 未鉴权代码执行，1.3.0 修复，2025-05 被 CISA 列入已知被利用漏洞（KEV）目录 — [Help Net Security](https://www.helpnetsecurity.com/2025/05/06/langflow-cve-2025-3248-exploited/)；[The Hacker News](https://thehackernews.com/2025/05/critical-langflow-flaw-added-to-cisa.html)

**Flowise**
- Workday 2025-08-14 宣布收购 Flowise（低代码 AI Agent 构建平台，金额未披露），意在增强其 HR/财务客户的 Agent 构建能力 — [Workday Newsroom](https://newsroom.workday.com/2025-08-14-Workday-Acquires-Flowise,-Bringing-Powerful-AI-Agent-Builder-Capabilities-to-the-Workday-Platform)；[Constellation Research](https://www.constellationr.com/insights/news/workday-acquires-flowise-speed-building-ai-agents-automated-workflows)
- "The Future of Flowise"（联合创始人 HenryHengZJ，2026-08-13 发帖）：原文称 "developers are increasingly relying on new coding agents to handle complex tasks. The typical rigid workflow low-code approach quickly hits the limit when it comes to complexity"，因此"wind down our operations for Flowise"；时间线：**2026-07-29 宣布并冻结代码**（不再接受 PR）→ **2026-08-13 仓库公开归档**（npm 包与 Docker 镜像标记 deprecated）→ **2026-08-31 EOL**（核心团队退出 Discord/GitHub）；鼓励社区 fork，Apache 2.0 代码保留 — [GitHub Discussion #6727](https://github.com/FlowiseAI/Flowise/discussions/6727)
- GitHub API 显示 Flowise `archived: true`，最后版本 flowise@3.1.4（2026-07-29），55,512 星 — [GitHub FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise)
- 许可：Apache 2.0，但 `packages/server/src/enterprise` 目录及带版权声明文件（如 IdentityManager.ts）为商业许可 — [Flowise LICENSE.md](https://github.com/FlowiseAI/Flowise/blob/main/LICENSE.md)

### Inferences
- **Langflow 优势**：MIT 许可最宽松；Python 原生，组件可直接改代码，是"低代码 ↔ 代码"之间最平滑的过渡；flow 即 MCP Server 便于被 Claude/Cursor 等 MCP 客户端调用；有 IBM 背书（watsonx 集成、企业支持）。**场景**：Python 团队的 RAG/Agent 原型快速验证与 API 化、给 coding agent / MCP 客户端提供可视化编排的工具、IBM 生态企业。**弱点**：历史上出现严重未鉴权 RCE 并被在野利用，自托管必须注意鉴权与版本；国内社区热度明显低于 Dify/Coze/FastGPT（推断，见 Q7）。
- **Flowise**：已不是可选的新项目——新选型应排除，存量用户需迁移或依赖社区 fork。其停运声明是"纯低代码工作流平台在 coding agent 时代受冲击"的一手证据，对本报告"低代码 vs 代码"一节价值很高。
- 被收购后停运的现象说明：被大厂收购的低代码平台往往转为母公司内部能力（Workday 内部是否继续使用 Flowise 技术未知），开源社区版的长期维护不可依赖。

### Gaps
- Workday 是否在其产品内继续使用/演进 Flowise 技术、是否有官方社区 fork 接手，未查到。
- Langflow 在 IBM 内的商业化形态（watsonx Orchestrate/ watsonx.ai 内具体产品名）未逐一核实。

---

## Q5. FastGPT、RAGFlow（及 MaxKB）：国内流行的知识库 / RAG 为核心的 Agent 平台

### Takeaway
三者都是"知识库优先"的国产开源平台：**RAGFlow**（英飞流 InfiniFlow，Apache 2.0，92.6k 星）以"深度文档理解"解决复杂 PDF/表格/扫描件的解析质量问题，2026 年推出 Agentic Retrieval 与 Knowledge Compilation，正处于 1.0 RC；**FastGPT**（环界云/Sealos，改版 Apache 2.0，29.9k 星）是轻量的知识库问答 + 可视化工作流平台，迭代极快；**MaxKB**（飞致云 1Panel 团队，GPL-3.0，23k 星）主打企业级智能客服/知识库，开箱即用。三者共同点是适合"文档问答类"场景，与 Dify 相比更聚焦、更轻（RAGFlow 除外，其文档解析栈较重）。

### Cited Findings
**RAGFlow**
- 定位："a leading open-source Retrieval-Augmented Generation (RAG) engine that fuses cutting-edge RAG with Agent capabilities to create a superior context layer for LLMs"；Apache-2.0；仓库创建 2023-12-12，92,581 星 — [GitHub infiniflow/ragflow](https://github.com/infiniflow/ragflow)
- 关键特性（README）："Quality in, quality out"——基于深度文档理解从复杂格式非结构化数据中抽取知识；模板化、可解释的分块；**Knowledge Compilation**（2026-08-19 引入，在文档/数据集层面生成 Wiki、图谱、树、PageIndex、思维导图、时间线和 Skills）；**Agentic Retrieval**（多步检索、问题拆解、证据校验，Low/Medium/High/Ultra 思考模式，2026-08-19 引入）；可视化分块允许人工干预、可追溯引用；支持 Word/PPT/Excel/TXT/图片/PDF/扫描件/结构化数据/网页；多路召回 + 融合重排；2026-07 增加 BigQuery 数据源增量同步，2026-09 增加 sitemap 网站摄取 — [RAGFlow README](https://github.com/infiniflow/ragflow)
- 版本：v0.24.0（2026-02-10）→ v0.25.0（2026-04-21）→ v0.26.0（2026-06-11）→ v0.27.0（2026-08-19）→ v1.0.0-rc1（2026-09-29）→ **v1.0.0-rc2（2026-10-16）**：Chat 引入 Agentic 模式取代四档思考级别、Team/Me 共享、12 个内置解析器与 Pipeline 解析器统一、支持 MinerU 4、新增 arm64 镜像 — [RAGFlow v1.0.0-rc2](https://github.com/infiniflow/ragflow/releases/tag/v1.0.0-rc2)；[RAGFlow releases](https://github.com/infiniflow/ragflow/releases)

**FastGPT**
- 定位（中文 README）："FastGPT 是一个 AI Agent 构建平台，提供开箱即用的数据处理、模型调用等能力，同时可以通过 Flow 可视化进行工作流编排"；提供云服务（fastgpt.io）、社区自托管（Docker / Sealos 一键部署）、商业版 — [GitHub labring/FastGPT](https://github.com/labring/FastGPT)
- 核心功能（README 勾选项）：Agent Skill 编排、对话工作流/插件工作流（含基础 RPA 节点）、用户交互、**双向 MCP**；知识库单点搜索测试、对话引用反馈可修改删除、完整调用链路日志、应用评测；多库复用混用、chunk 修改删除、手动/直接分段/QA 拆分导入、TXT/MD/HTML/PDF/Docx/PPTX/CSV/XLSX、URL 读取、**混合检索 & 重排**、API 知识库；免登录分享、iframe 嵌入、对话记录标注 — [FastGPT README](https://github.com/labring/FastGPT)
- 迭代：v4.16.0（2026-08-16）、v4.17.0（2026-09-11）、v4.17.2（2026-10-09），同时维护 4.14/4.15 补丁线 — [FastGPT releases](https://github.com/labring/FastGPT/releases)
- 许可：Apache 2.0 + 附加条件——未经书面授权不得运营"与 FastGPT 类似的多租户 SaaS 服务"；不得移除/修改控制台 LOGO 与版权；"交互设计受外观专利保护"；© 2023 Sealos — [FastGPT LICENSE](https://github.com/labring/FastGPT/blob/main/LICENSE)

**MaxKB**
- "MaxKB = Max Knowledge Brain"，开源企业级智能体平台：RAG Pipeline（上传/爬取文档、自动分段向量化）、Agentic Workflow（工作流引擎 + 函数库 + MCP 工具调用）、零代码嵌入第三方业务系统、模型无关（DeepSeek/Llama/Qwen 等私有模型及 OpenAI/Claude/Gemini/MiniMax 等）、多模态；Docker 一行启动，并为中国用户提供离线安装文档；**GPL-3.0** — [GitHub 1Panel-dev/MaxKB](https://github.com/1Panel-dev/MaxKB)

**社区评价（可信度中等，个人/社区横评）**
- 横评观点：RAGFlow 处理复杂文档强，但若只有几百份规整文档则"杀鸡用牛刀"；FastGPT 比 Dify 更轻量、专注知识库但功能丰富度不及 Dify；MaxKB 协议为 GPL v3 需留意 — [CSDN 横评：Dify、RAGFlow、MaxKB、FastGPT](https://aicoding.csdn.net/6a5ddffb662f9a54cb9136cb.html)（经搜索摘要获取，未逐页核实）
- 一个电商客服（5,000 份 FAQ 文档）事故复盘：自动分块切断 Q&A 对 + embedding 对中文弱，导致召回 28%；修正后召回升至 82%、准确率 35%→78%、转人工 65%→22% — [掘金（2026-06-11）](https://juejin.cn/post/7649984137365962761)（个人文章，作者自述案例，未经第三方核实）
- Jimmy Song 对比（2025-08）：RAGFlow "deep document understanding RAG engine"、可追溯可解释检索，偏引擎/后端；FastGPT 适合企业知识库助手，许可限制 SaaS，商业可持续性依赖 LabRing — [Jimmy Song 博客](https://jimmysong.io/blog/open-source-ai-agent-workflow-comparison/)（注：发布于 2025-08，部分为历史信息）

### Inferences
- **RAGFlow 优势/场景**：复杂版式文档（扫描件、合同、财报、表格密集的 PDF、PPT）的高质量解析与可追溯引用，是"检索质量是瓶颈"场景的首选；适合法律、金融、制造技术文档、科研资料库；1.0 后定位从"RAG 引擎"扩展为"LLM 上下文层"（Knowledge Compilation 产出 Skills、Agentic Retrieval），可作为其他 Agent 框架/平台的检索后端。弱点：部署与资源开销较大（文档解析模型），工作流/业务编排能力弱于 Dify。
- **FastGPT 优势/场景**：轻量、上手快、中文社区活跃，适合中小企业/部门级知识库问答、客服机器人、iframe 嵌入官网；Sealos 一键部署降低运维门槛。弱点：多租户 SaaS 限制（与 Dify 类似）；功能广度、插件生态不及 Dify。
- **MaxKB 优势/场景**：开箱即用、离线安装友好，契合国内政企内网"智能客服 + 知识库"场景；弱点：GPL-3.0 copyleft——若修改后分发需开源，ISV 集成需评估。
- 总体：国内"知识库问答"是企业 AI 落地的第一大场景，这解释了为何国内出现 FastGPT、MaxKB、RAGFlow、QAnything 等一批 RAG 优先平台，而海外同类更多被通用平台（Dify/Langflow）或云厂商托管服务覆盖（推断）。

### Gaps
- 三者的国内企业客户名单与量化采用数据未找到权威来源。
- RAGFlow 1.0 GA 日期尚未确定（截至 2026-10-21 仍为 rc2）。
- FastGPT 4.16/4.17 具体新增功能未逐一核对 release notes。

---

## Q6. 代码优先的中国框架：Qwen-Agent、Spring AI Alibaba（及 Spring AI）、Eino 及其他

### Takeaway
中国代码框架生态呈"按语言/生态分工"格局：**Python** 侧有 Qwen-Agent（通义千问官方，Qwen Chat 后端，但 2026 年起更新放缓）与 AgentScope（阿里，33.6k 星，另有研究员覆盖）；**Java** 侧有 Spring 官方 Spring AI（2.0 于 2026-06-12 GA，基线 Spring Boot 4）与其上层的 Spring AI Alibaba（Graph + Agent Framework + Admin 可视化平台，绑定阿里云百炼/DashScope、Nacos）；**Go** 侧有字节 CloudWeGo 的 Eino（ADK、DeepAgent、图编排，扣子底座，高频发版）。此外字节 DeerFlow（84k 星，长程 SuperAgent harness）是 2025-2026 年国内最热的 Agent 应用级项目之一。

### Cited Findings
**Qwen-Agent**
- "a framework for developing LLM applications based on the instruction following, tool usage, planning, and memory capabilities of Qwen"；附带 Browser Assistant、Code Interpreter、Custom Assistant 示例；"Now Qwen-Agent plays as the backend of Qwen Chat"；仓库描述：基于 Qwen>=3.0，支持 Function Calling、MCP、Code Interpreter、RAG、Chrome 扩展；Apache-2.0，17.2k 星 — [GitHub QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent)
- 新闻：2026-02-16 Qwen3.5 Agent Demo；2026-01-27 开源 Agent 评测基准 DeepPlanning 并上线文档；2025-09 Qwen3-VL 工具调用；2025-07 Qwen3-Coder 工具调用、原生 API 工具调用（如 vLLM 内置解析）；2025-05 MCP Cookbooks；README 提示其 Python 执行器"not sandboxed… not for production use"（针对 Qwen2.5-Math 示例）— [Qwen-Agent README](https://github.com/QwenLM/Qwen-Agent)
- 版本仍为 0.0.x：PyPI 最新 0.0.34（2026-02-16），仓库最近 push 2026-03-04 — [PyPI qwen-agent](https://pypi.org/project/qwen-agent/)；[GitHub](https://github.com/QwenLM/Qwen-Agent)

**Spring AI（Spring 官方）**
- Spring AI 2.0.0 GA（2026-06-12）：基线 Spring Boot 4.0/4.1 + Spring Framework 7.0、Jackson 3、JSpecify 空安全；工具调用循环移入 Advisor 链（`ToolCallingAdvisor` 自动注册），`ToolSearchToolCallingAdvisor` 渐进暴露工具（支持数百个工具），`StructuredOutputValidationAdvisor` 结构化输出校验重试；MCP Java SDK 2.0.0（符合 2025-11-25 规范），`@McpTool/@McpResource/@McpPrompt` 注解并入核心，默认 Streamable HTTP；社区项目 `spring-ai-agent-utils`（Agent Skills、文件/shell/网页抓取/任务/自动记忆）与 `spring-ai-session`（事件溯源会话记忆、上下文压缩）；`ChatClient` 为主 API — [Spring 官方博客](https://spring.io/blog/2026/06/12/spring-ai-2-0-0-GA-available-now/)
- 1.x → 2.0 是有意义的升级而非替换补丁（模块改名、类迁移、Advisor 变化）— [Visual Studio Magazine](https://visualstudiomagazine.com/articles/2026/06/29/spring-ai-2-0-goes-ga-giving-java-developers-a-more-mature-ai-app-stack.aspx)
- 后续：2.0.1（2026-08-21）、2.1.0-M1（2026-09-25）— [spring-ai releases](https://github.com/spring-projects/spring-ai/releases)

**Spring AI Alibaba（SAA）**
- "Agentic AI Framework for Java Developers"；"A production-ready framework for building Agentic, Workflow, and Multi-agent applications"；三层：**SAA Admin**（一站式可视化 Agent 平台：可视化开发、可观测、评测、MCP 管理，"integrates with open-source low-code platforms like Dify, enabling rapid migration from DSL to Spring AI Alibaba project"）、**Agent Framework**（内置 Context Engineering 与 HITL；`SequentialAgent/ParallelAgent/RoutingAgent/LoopAgent`）、**Graph**（底层运行时：持久化、编排、流式、条件路由、嵌套图、并行，导出 PlantUML/Mermaid）；支持 A2A（结合 Nacos 分布式 Agent 协作）、多模态、语音 Agent、DashScope/OpenAI 等模型与 MCP；JDK 17+；示例默认使用阿里云百炼 API Key — [GitHub alibaba/spring-ai-alibaba](https://github.com/alibaba/spring-ai-alibaba)
- 版本：v1.0.0.2（2025-05-29）、v1.1.0.0（2025-12-30）、v1.1.2.0（2026-02-02）、v1.1.2.2（2026-03-10）、**v2.0.0-M1.1（2026-06-25，对齐 Spring AI 2.0）**；11k 星 — [SAA releases](https://github.com/alibaba/spring-ai-alibaba/releases)
- 社区对比观点：SAA 以 Graph（工作流编排）为核心，AgentScope 以 Agentic（模型自主决策）为核心；阿里方面口径为 AgentScope-Java 适合以 Agent 为核心的应用、SAA 适合基于 Workflow 的应用，SAA 生态将在底层支持 AgentScope — [CSDN 文章](https://gitcode.csdn.net/6a290ce8662f9a54cb7c2ca8.html)（经搜索摘要获取，未逐页核实）
- Java 侧另一主流选择 LangChain4j：1.22.0（2026-10-08），13.3k 星 — [GitHub langchain4j](https://github.com/langchain4j/langchain4j)；AgentScope-Java v2.0.4（2026-10-08），6k 星，"Build distributed, production-grade, long-running agents" — [GitHub agentscope-java](https://github.com/agentscope-ai/agentscope-java)

**Eino（字节 CloudWeGo，Go）**
- "an LLM application development framework in Golang. It draws from LangChain, Google ADK, and other open-source frameworks, and is designed to follow Golang conventions"；提供 Components（ChatModel、Tool、Retriever、ChatTemplate 等，eino-ext 有 OpenAI、Ollama 等实现）、**ADK**（工具调用、多 Agent 协同、上下文管理、中断/恢复支持 HITL、开箱即用 Agent 模式）、Composition（组件编排为图/工作流，可作为工具暴露给 Agent）、**DeepAgent**（拆解任务、委派子 Agent、跟踪进度，可配 shell/Python/网页搜索）— [GitHub cloudwego/eino](https://github.com/cloudwego/eino)
- 仓库创建 2024-12-04；v0.8.0（2026-03-09）→ v0.9.22（2026-10-19），13.4k 星，Apache-2.0；仍为 0.x — [eino releases](https://github.com/cloudwego/eino/releases)
- 扣子开源版后端直接依赖 Eino — [coze-studio go.mod](https://github.com/coze-dev/coze-studio/blob/main/backend/go.mod)

**其他在国内社区热门的项目（简述）**
- **DeerFlow（字节，MIT）**：84,230 星，v2.1.0（2026-09-24），"An open-source long-horizon SuperAgent harness that researches, codes, and creates… sandboxes, memories, tools, skill, subagents and message gateway… tasks that could take minutes to hours" — [GitHub bytedance/deer-flow](https://github.com/bytedance/deer-flow)
- **AgentScope（阿里，Apache-2.0）**：33.6k 星，v2.0.10（2026-10-12），已迁至 `agentscope-ai` 组织（另有研究员详细覆盖）— [GitHub agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope)
- **UI-TARS-desktop（字节，Apache-2.0）**：39.4k 星，"The Open-Source Multimodal AI Agent Stack" — [GitHub](https://github.com/bytedance/UI-TARS-desktop)
- **JoyAgent-JDGenie（京东，Apache-2.0）**："开源的端到端产品级通用智能体"，11.9k 星，v1.0.0（2025-09-18），最近 push 2026-02 — [GitHub](https://github.com/jd-opensource/joyagent-jdgenie)；**OxyGent（京东）**：多 Agent 框架，论文被 ACL 2026 收录，2.1k 星 — [GitHub](https://github.com/jd-opensource/OxyGent)
- **MetaGPT（FoundationAgents）**：70.9k 星但最后 release 为 v0.8.1（2024-04），属于历史热门 — [GitHub](https://github.com/FoundationAgents/MetaGPT)
- **LangBot（Apache-2.0）**：面向 IM 的生产级机器人平台，对接企业微信、公众号、飞书、钉钉、QQ 等，并可集成 Dify、n8n、Langflow、Coze 等作为后端，v4.11.1（2026-10-20）— [GitHub langbot-app/LangBot](https://github.com/langbot-app/LangBot)
- 全球个人 Agent 浪潮（非中国项目，作背景）：OpenClaw 392.7k 星（创建于 2025-11-24，MIT）、NousResearch Hermes Agent 255.7k 星 — [GitHub openclaw](https://github.com/openclaw/openclaw)；[GitHub hermes-agent](https://github.com/NousResearch/hermes-agent)；扣子 3.0 宣称可一键接入 OpenClaw — [财联社](https://www.cls.cn/detail/2389018)

### Inferences
- **Qwen-Agent**：优势是与 Qwen 模型（函数调用模板、推理内容字段、Qwen3-Coder/VL 工具调用）深度对齐、官方背书（Qwen Chat 后端）；**场景**是基于 Qwen 开源模型私有化部署、需要充分发挥 Qwen 原生工具调用/代码解释器能力的 Python 团队。弱点：仍为 0.0.x、2026-03 后几乎无更新、代码执行器非沙箱，不宜作为通用生产框架；阿里在 Python 通用 Agent 框架上的重心似乎转向 AgentScope（推断）。
- **Spring AI / SAA**：解决的核心问题是"国内大量 Java/Spring 存量后端团队无需切换到 Python 即可构建 Agent"，可在同一事务、鉴权、监控体系内与业务系统集成；Spring AI 提供标准抽象层（类比 JDBC），SAA 在其上补齐多 Agent 编排、Graph 持久化、可视化 Admin、Nacos A2A、百炼/DashScope 集成，以及"Dify DSL → Java 工程"的迁移路径——这是国内"低代码验证、代码化落地"路径的直接产品化。弱点：SAA 与阿里云生态耦合较深；2.0 线仍为里程碑版（M1.1）；Spring AI 2.0 升级有破坏性变更。
- **Eino**：解决 Go 技术栈（字节系、云原生/微服务团队）缺少一流 LLM 框架的问题，强类型、并发与部署友好，图编排 + ADK + DeepAgent 覆盖从工作流到自主 Agent；经过扣子等字节内部产品锤炼（以 Coze Studio 依赖为证）。弱点：仍为 0.x，API 演进快；Go 生态的模型/工具组件丰富度不及 Python。
- **DeerFlow** 代表的"长程 SuperAgent harness（沙箱 + 技能 + 子 Agent）"已成为 2026 年国内最受关注的 Agent 形态之一，与 Dify 1.16 的 Dify Agent、扣子 2.0/3.0 的 Agent Plan/Skills 方向一致。

### Gaps
- Eino、SAA 在字节/阿里内部或外部企业的具体落地案例与规模，未找到可引用的官方数据。
- Qwen-Agent 是否已被官方降级维护或由其他项目（如 Qwen Code）取代，无官方说明。
- Spring AI Alibaba 2.0 GA 时间未确定。

---

## Q7. 中国开发者社区如何看"最热"框架/平台，与全球趋势有何不同

### Takeaway
国内社区（掘金、CSDN、知乎类选型文）的讨论高度集中在 **Dify / Coze（扣子）/ FastGPT / MaxKB / RAGFlow** 这组"可私有化的可视化平台 + 知识库"上，以及按语言分的代码框架（Java 看 Spring AI / SAA，Go 看 Eino，Python 看 AgentScope / LangGraph）；全球讨论则更偏向 n8n（自动化）、Langflow 以及 LangGraph/OpenAI/Google ADK 等代码框架，并在 2026 年明显转向 coding agent 与个人 Agent（OpenClaw、Hermes Agent）。差异的根源在于：国内重视私有化/数据不出域、国产模型适配、中文文档、国内 IM/办公生态接入，以及大厂（字节、阿里、京东）开源驱动。需要注意：可找到的国内一手社区数据多为个人博客，缺乏权威统计。

### Cited Findings
- 国内选型文常见决策树：文档复杂、表格多→RAGFlow；多步工作流/工具调用→Dify；知识库问答快速迭代→FastGPT 或 MaxKB；无技术团队或在字节生态→Coze；数据必须私有化→Dify 或 FastGPT（需计入服务器与运维成本）— [CSDN 横评](https://aicoding.csdn.net/6a5ddffb662f9a54cb9136cb.html)；[Dify 论坛对比帖](https://forum.dify.ai/t/dify-coze-n8n-fastgpt-ragflow/528)（经搜索摘要获取，未逐页核实）
- Java 开发者视角：低代码（Dify）被视为"最快的 AI 验证路径"，约两周出原型；Coze SaaS 数据"在字节云"，存在"依赖厂商 · 数据出域"风险 — [掘金（2026-06-11）](https://juejin.cn/post/7649984137365962761)
- Jimmy Song（国内知名云原生博主）指出 Coze、Dify、FastGPT 都以微信群作为社区渠道，FastGPT "active in China"；关键决策因素是"architecture fit, extensibility cost, deployment constraints, and license risk"，而非星数 — [Jimmy Song 博客（2025-08）](https://jimmysong.io/blog/open-source-ai-agent-workflow-comparison/)
- 星数 ≠ 使用量：有第三方分析称 Dify 星数高，但按月下载量衡量，LangGraph 以 8.5% 的星数占比占据 5,090 万月下载中的 67.8% — [Keenable 分析](https://select.keenable.ai/r/open-source-ai-agents-usage-github-share/jfXoGkRU0H2l6G2hKZhPGw)（第三方，方法论未核实；Dify 主要以 Docker 镜像分发，与 PyPI 下载不可直接比较）
- 国内 IM 生态接入需求催生 LangBot 等项目，其把 Dify、n8n、Langflow、Coze 作为后端接入企业微信、公众号、飞书、钉钉、QQ — [GitHub LangBot](https://github.com/langbot-app/LangBot)
- 全球侧信号：Flowise 团队以"coding agents"兴起为由停运 — [Flowise Discussion #6727](https://github.com/FlowiseAI/Flowise/discussions/6727)；n8n 获 SAP 战略投资、嵌入 Joule Studio — [Tech.eu](https://tech.eu/2026/05/12/n8n-s-valuation-doubles-to-5-2bn-following-sap-strategic-investment/)；个人 Agent 项目 OpenClaw 星数达 392.7k — [GitHub openclaw](https://github.com/openclaw/openclaw)
- 国内平台同步转向 Skills/长程 Agent：扣子 2.0 Agent Skills/Agent Plan（2026-01）— [IT之家](https://www.ithome.com/0/914/507.htm)；扣子 3.0 接入 Claude Code/Codex CLI/OpenClaw（2026-06）— [财联社](https://www.cls.cn/detail/2389018)；Dify 1.16 Dify Agent + Skills（2026-07）— [Dify v1.16.0](https://github.com/langgenius/dify/releases/tag/1.16.0)；FastGPT "Agent Skill 编排" — [FastGPT README](https://github.com/labring/FastGPT)；RAGFlow Knowledge Compilation 生成 Skills — [RAGFlow README](https://github.com/infiniflow/ragflow)

### Inferences
- **国内"最热"排序（综合 GitHub 星数与社区讨论频率，属定性判断）**：平台层 Dify ≫ Coze/扣子（商业版用户心智最强、开源版热度在衰减）> RAGFlow > FastGPT ≈ MaxKB；代码层按语言分：Python（AgentScope、LangGraph、Qwen-Agent）、Java（Spring AI / SAA / LangChain4j / AgentScope-Java）、Go（Eino）；应用级 Agent：DeerFlow。
- **与全球差异**：① 国内 n8n 讨论度相对低（集成生态以海外 SaaS 为主，国内 SaaS 连接器少）；② Langflow/Flowise 在国内存在感弱；③ 国内特别多"知识库优先"平台（FastGPT/MaxKB/RAGFlow/QAnything），反映企业知识问答是国内第一落地场景；④ Java、Go 框架在国内地位突出，因为国内企业后端以 Java/Go 为主，海外则以 Python/TypeScript 为主；⑤ 大厂开源（字节：Coze/Eino/DeerFlow/UI-TARS；阿里：SAA/AgentScope/Qwen-Agent；京东：JoyAgent/OxyGent）是国内生态的主要供给方。
- **共同趋势**：2026 年全球与国内平台都在从"固定 DAG 工作流"向"沙箱 + Skills + 长程自主 Agent + HITL"演进，低代码平台纷纷内置 Agent 运行时以对冲 coding agent 冲击。

### Gaps
- 未找到知乎、InfoQ 中文、机器之心关于"2026 年国内最热 Agent 框架"的权威调查或量化榜单；《中国开源年度报告》中 Agent 项目的具体排名未检索到。
- 国内企业级智能体市场份额数据（赛迪、IDC 等）仅见于二手转引，未能核实原始报告。

---

## Q8. 何时选低代码平台，何时选代码优先框架

### Takeaway
低代码平台（Dify/Coze/FastGPT/n8n/Langflow）适合"流程可枚举、需要业务人员参与、追求交付速度、以知识库问答/标准化自动化为主"的场景；代码框架（LangGraph、Spring AI/SAA、Eino、AgentScope、Qwen-Agent）适合"Agent 是核心业务链路、需要与业务系统同事务/同鉴权集成、高并发、深度定制 Agent 循环、需代码级审计与测试"的场景。2026 年的新变量是：coding agent 让写代码的成本骤降，纯低代码工作流平台（如 Flowise）因复杂度天花板被淘汰，而存活的平台都在内置沙箱 Agent、CLI/API/MCP 出口，变成"可被代码和 Agent 调用的后端"。常见的务实路径是"低代码验证 → 核心链路代码化 → 平台保留给运营自助"。

### Cited Findings
- 转向代码框架的信号（Java 开发者视角）：AI 功能成为核心链路且 QPS > 1000；需与业务系统在同一事务、数据库或鉴权范围内集成；要求代码级安全审计；需要深度定制（自定义 Agent loop、Advisor 链）。推荐路径：先在 Dify 验证，再把核心路径逐步迁移到 Spring AI 等代码框架，Dify 保留给运营自助；Dify 二开应避免改内核，通过 API/插件松耦合 — [掘金（2026-06-11）](https://juejin.cn/post/7649984137365962761)
- 低代码适用：PoC、内部工具、FAQ/知识库、预算有限或无 AI 经验的团队；Dify 定制深度"受限于平台能力"，性能调优"有限（通过参数配置）" — [掘金（2026-06-11）](https://juejin.cn/post/7649984137365962761)
- 选型维度应是架构匹配、扩展成本、部署约束、许可证风险；关键任务系统应选有持续支持保障的平台；LangGraph 等代码框架给"想要最大控制力的开发者" — [Jimmy Song 博客](https://jimmysong.io/blog/open-source-ai-agent-workflow-comparison/)
- 低代码天花板的一手证据：Flowise 团队称 "The typical rigid workflow low-code approach quickly hits the limit when it comes to complexity"，并因此停止运营 — [Flowise Discussion #6727](https://github.com/FlowiseAI/Flowise/discussions/6727)
- 平台向代码/Agent 开放出口：Dify 1.15 的 difyctl 让个人 Agent、脚本、CI 调用 Dify 工作流 — [Dify v1.15.0](https://github.com/langgenius/dify/releases/tag/1.15.0)；Langflow 每个 flow 可部署为 API/MCP Server、可导出 JSON — [Langflow README](https://github.com/langflow-ai/langflow)；n8n 支持 JS/Python/npm 代码节点 — [n8n README](https://github.com/n8n-io/n8n)
- 代码框架向可视化靠拢：SAA Admin 支持可视化开发并可把 Dify DSL 迁移为 Spring AI Alibaba 工程、或无代码部署 Agent / 导出独立 Java 项目 — [SAA README](https://github.com/alibaba/spring-ai-alibaba)
- 许可证是低代码平台选型的硬约束：Dify、FastGPT 禁止未授权多租户 SaaS 且不可去 LOGO — [Dify LICENSE](https://github.com/langgenius/dify/blob/main/LICENSE)、[FastGPT LICENSE](https://github.com/labring/FastGPT/blob/main/LICENSE)；n8n 仅限内部业务/非商业使用 — [n8n LICENSE.md](https://github.com/n8n-io/n8n/blob/master/LICENSE.md)；MaxKB 为 GPL-3.0 — [MaxKB](https://github.com/1Panel-dev/MaxKB)；Coze Studio/Loop、RAGFlow 为 Apache-2.0，Langflow 为 MIT — 见各仓库
- 自托管安全面：Langflow CVE-2025-3248 未鉴权 RCE 被在野利用 — [Help Net Security](https://www.helpnetsecurity.com/2025/05/06/langflow-cve-2025-3248-exploited/)；Coze Studio 官方提示公网部署 SSRF/代码节点/越权风险 — [coze-studio README](https://github.com/coze-dev/coze-studio)；n8n 2.0 默认禁用 ExecuteCommand 等高危节点 — [n8n 2.0.0](https://github.com/n8n-io/n8n/releases/tag/n8n@2.0.0)

### Inferences
**对比框架（供报告撰写者直接使用）**

| 维度 | 低代码/可视化平台 | 代码优先框架 |
|---|---|---|
| 交付速度 | 分钟~天级出原型 | 天~周级 |
| 参与者 | 产品、运营、业务专家可直接配置 | 以工程师为主 |
| 定制上限 | 受平台节点/插件能力限制 | 任意控制 Agent 循环、状态、记忆、重试 |
| 工程化 | 版本/测试/CI 依赖平台（DSL 导出、平台内评测） | Git、单测、CI/CD、代码审计天然支持 |
| 系统集成 | 通过 HTTP/插件/MCP 松耦合 | 可与业务同进程、同事务、同鉴权 |
| 性能与扩展 | 参数级调优，大规模需按平台架构扩容 | 可按业务定制并发、缓存、降级 |
| 许可风险 | Dify/FastGPT 多租户限制、n8n fair-code、MaxKB GPL | 多为 Apache-2.0/MIT |
| 运维 | 平台自带中间件栈（Dify/Coze 较重） | 自行搭建，但可复用现有基础设施 |

- **选低代码**：知识库问答/客服、内部效率工具、流程可枚举且需要人工审批的业务流、跨 SaaS 自动化（n8n）、需要业务人员持续迭代 Prompt 与流程、团队缺少 AI 工程能力、需要快速 PoC 验证价值。
- **选代码框架**：Agent 是产品核心或高并发主链路；需要复杂状态机、长程自主执行、多 Agent 协作、精细的失败恢复；与 Java/Go 存量系统深度集成（选 Spring AI/SAA 或 Eino）；需代码级审计、测试与合规；要做多租户 SaaS 产品而低代码平台许可不允许。
- **混合模式（国内最常见的务实路径）**：Dify/FastGPT 承担知识库与运营自助，代码框架承担核心链路，二者通过 API/MCP 互调；或用 RAGFlow 作为统一检索层，被平台和代码框架共同调用；SAA 的 Dify DSL 迁移能力为"平台 → 代码"提供了现成通道。
- **2026 年新判断**：coding agent 降低了代码优先的门槛，"不会写代码所以用低代码"的理由在减弱；低代码平台的持续价值转向治理（RBAC、审计、HITL）、非开发者参与和运营可视化。纯"拖拽 DAG"且无差异化的平台面临 Flowise 式出局风险。

### Gaps
- 未找到对"低代码平台 vs 代码框架"在生产环境的权威量化对比（性能、TCO、故障率）；掘金文章中的 TCO 数字作者自述为示意性质，不可作为事实引用。
- 国内企业从 Dify 等平台迁移到代码框架的真实案例与比例缺乏可靠来源。
