# AI 智能体开发框架热度与量化采用指标（截至 2026-10-21）

> 数据采集说明（写报告时请保留）：
> - **GitHub Star / Fork / 最近推送**：GitHub REST API `GET /repos/{owner}/{repo}`，抓取时间 **2026-10-21 08:41 UTC**（本会话实测）。
> - **Star 增长**：GitHub 2026-09 新增的官方接口 `GET /repos/{owner}/{repo}/stargazers/history`（API 版本 2026-03-10，按周返回新增 star 数，最新在前）——[GitHub Docs](https://docs.github.com/en/rest/activity/starring?apiVersion=2026-03-10#get-repository-star-history)、[GitHub Changelog 2026-09-04](https://github.blog/changelog/2026-09-04-new-api-endpoint-provides-privacy-safe-star-history-data)。本会话于 2026-10-21 实测。窗口定义（均为完整自然周，周日起）：
>   - **近 4 周** = 2026-09-20 ~ 2026-10-17；**近 13 周** = 2026-07-19 ~ 2026-10-17；**前 13 周** = 2026-04-19 ~ 2026-07-18；**近 52 周** = 2025-10-19 ~ 2026-10-17。
>   - “加速比” = 近 13 周 ÷ 前 13 周（>1 表示在加速）。“YoY%” = 近 52 周新增 ÷（当前总数 − 近 52 周新增）。
>   - 注意：接口未说明每周数字是否扣除了取消 star，按“新增”理解。
> - **PyPI 下载**：pypistats.org API（`/recent` 的 last_month = 近 30 天，**不含镜像**），2026-10-21 抓取。**npm 下载**：api.npmjs.org `point/last-month`（2026-09-19 ~ 2026-10-18）及 `range`（按月汇总）。
> - **背景变化**：GitHub 自 2026 年中起把 stargazer 列表接口限制为仓库管理员/协作者可见，旧的“逐个 stargazer 时间戳”方法（star-history.com 原方法）对第三方仓库失效（本会话实测 REST 返回 401/404，GraphQL 返回空列表）——[star-history.com 博客](https://www.star-history.com/blog/github-stargazer-api-restriction)、[codercops 博客](https://blog.codercops.com/blog/github-removed-public-stargazer-lists-2026)。
> - **OSS Insight 数据不可靠（2026）**：本会话实测其 API 返回的累计 star 与 GitHub 实际值严重不符（如 langchain-ai/deepagents 8,560 vs 实际 30,469；agentscope 16,244 vs 33,581），且 2026-05~08 几乎平线，疑似 GH Archive 数据缺口——[OSS Insight API 示例](https://api.ossinsight.io/v1/repos/langchain-ai/langgraph/stargazers/history?per=month)。**报告中不要引用 OSS Insight 2026 年的数字。**

## Q1：主要智能体框架的 GitHub Star 数与近期 Star 增长

### Takeaway
按累计 Star，“低代码/平台型”项目遥遥领先（n8n 20.8 万、Dify 15.9 万、Langflow 15.6 万），代码优先框架中 LangChain（14.8 万）独一档，其后是 MetaGPT、AutoGen、CrewAI、LlamaIndex、LangGraph、Agno（4.3 万~7.1 万）；但按近 52 周新增 Star，增长最猛的是 DeerFlow（+6.7 万）、n8n（+6.3 万）、Dify（+4.5 万）、LangChain（+3.3 万）、Deep Agents（+2.6 万，+605%）、LangGraph（+2.4 万，+121%）、CrewAI（+2.1 万）、AgentScope（+2.1 万，+157%）；近一个季度绝大多数框架 star 流入在**减速**（加速比中位数约 0.75），仅 Strands、AgentScope、DSPy 及语音智能体框架（LiveKit Agents、Pipecat）在加速。

### Cited Findings

**表 1：代码优先（SDK/库）框架 —— GitHub 数据（2026-10-21 实测）**

| 框架 | 仓库 | Stars | 近4周 | 近13周 | 前13周 | 加速比 | 近52周 | YoY | 最近推送 |
|---|---|---|---|---|---|---|---|---|---|
| LangChain (Py) | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 148,186 | 1,725 | 6,739 | 8,784 | 0.77 | 32,907 | +29% | 2026-10-21 |
| MetaGPT | [FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT) | 70,945 | 535 | 1,831 | 2,579 | 0.71 | 13,119 | +23% | **2026-01-21** |
| AutoGen | [microsoft/autogen](https://github.com/microsoft/autogen) | 61,504 | 518 | 1,985 | 2,966 | 0.67 | 11,695 | +23% | 2026-10-16 |
| CrewAI | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 59,942 | 1,144 | 4,423 | 6,834 | 0.65 | 21,466 | +56% | 2026-10-21 |
| LlamaIndex | [run-llama/llama_index](https://github.com/run-llama/llama_index) | 52,592 | 379 | 1,834 | 2,443 | 0.75 | 8,506 | +19% | 2026-10-21 |
| LangGraph (Py) | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 43,628 | 1,560 | 6,105 | 8,086 | 0.76 | 23,922 | +121% | 2026-10-21 |
| Agno（原 Phidata） | [agno-agi/agno](https://github.com/agno-agi/agno) | 42,850 | 609 | 1,744 | 1,976 | 0.88 | 9,191 | +27% | 2026-10-21 |
| DSPy | [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | 38,712 | 572 | 2,598 | 2,500 | **1.04** | 9,763 | +34% | 2026-10-20 |
| AgentScope（阿里） | [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | 33,581 | 1,526 | 5,609 | 4,140 | **1.35** | 20,523 | +157% | 2026-10-21 |
| Deep Agents（LangChain） | [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) | 30,469 | 857 | 4,119 | 5,434 | 0.76 | 26,145 | **+605%** | 2026-10-21 |
| OpenAI Agents SDK (Py) | [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | 30,192 | 600 | 2,290 | 5,599 | **0.41** | 13,941 | +86% | 2026-10-20 |
| smolagents（HF） | [huggingface/smolagents](https://github.com/huggingface/smolagents) | 29,956 | 536 | 1,629 | 1,825 | 0.89 | 6,905 | +30% | 2026-10-06 |
| Mastra (TS) | [mastra-ai/mastra](https://github.com/mastra-ai/mastra) | 28,972 | 738 | 2,684 | 3,333 | 0.81 | 11,739 | +68% | 2026-10-21 |
| Semantic Kernel | [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel) | 28,681 | 136 | 474 | 716 | 0.66 | 2,682 | +10% | 2026-10-21 |
| Vercel AI SDK | [vercel/ai](https://github.com/vercel/ai) | 27,428 | 578 | 1,904 | 2,168 | 0.88 | 9,223 | +51% | 2026-10-21 |
| Haystack | [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | 26,800 | 263 | 933 | 1,126 | 0.83 | 4,038 | +18% | 2026-10-21 |
| OpenAI Swarm（实验性教学框架） | [openai/swarm](https://github.com/openai/swarm) | 22,065 | 103 | 340 | 563 | 0.60 | 1,893 | +9% | 2026-04-15 |
| Google ADK (Py) | [google/adk-python](https://github.com/google/adk-python) | 21,933 | 367 | 1,369 | 1,665 | 0.82 | 8,435 | +62% | 2026-10-21 |
| Pydantic AI | [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) | 20,764 | 683 | 2,181 | 2,269 | 0.96 | 8,015 | +63% | 2026-10-21 |
| LangChain.js | [langchain-ai/langchainjs](https://github.com/langchain-ai/langchainjs) | 18,285 | 80 | 384 | 535 | 0.72 | 2,503 | +16% | 2026-10-20 |
| CAMEL | [camel-ai/camel](https://github.com/camel-ai/camel) | 17,942 | 210 | 599 | 764 | 0.78 | 3,656 | +26% | 2026-10-19 |
| Qwen-Agent（阿里） | [QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) | 17,200 | 114 | 483 | 854 | 0.57 | 5,507 | +47% | **2026-03-04** |
| Microsoft Agent Framework | [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | 14,244 | 605 | 2,055 | 2,694 | 0.76 | 10,347 | **+266%** | 2026-10-21 |
| Eino（字节 CloudWeGo, Go） | [cloudwego/eino](https://github.com/cloudwego/eino) | 13,371 | 256 | 1,061 | 1,692 | 0.63 | 5,794 | +76% | 2026-10-19 |
| LangChain4j (Java) | [langchain4j/langchain4j](https://github.com/langchain4j/langchain4j) | 13,271 | 156 | 699 | 1,044 | 0.67 | 4,159 | +46% | 2026-10-21 |
| Spring AI Alibaba | [alibaba/spring-ai-alibaba](https://github.com/alibaba/spring-ai-alibaba) | 11,044 | 166 | 752 | 1,123 | 0.67 | 4,730 | +75% | 2026-10-07 |
| VoltAgent (TS) | [VoltAgent/voltagent](https://github.com/VoltAgent/voltagent) | 10,854 | 212 | 817 | 1,868 | 0.44 | 7,339 | +209% | 2026-10-15 |
| Spring AI | [spring-projects/spring-ai](https://github.com/spring-projects/spring-ai) | 9,558 | 111 | 459 | 679 | 0.68 | 2,771 | +41% | 2026-10-16 |
| AWS Strands Agents | [strands-agents/harness-sdk](https://github.com/strands-agents/harness-sdk)（原 sdk-python，已改名） | 8,889 | 1,509 | 2,260 | 993 | **2.28** | 5,180 | +140% | 2026-10-21 |
| Google ADK (Go) | [google/adk-go](https://github.com/google/adk-go) | 8,884 | 107 | 449 | 932 | 0.48 | 8,870 | 新（约 2025-11 公开） | 2026-10-21 |
| Claude Agent SDK (Py) | [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | 8,316 | 179 | 694 | 1,319 | 0.53 | 5,667 | +214% | 2026-10-21 |
| AgentScope Java | [agentscope-ai/agentscope-java](https://github.com/agentscope-ai/agentscope-java) | 6,067 | 335 | 1,512 | 1,927 | 0.78 | 5,964 | 新 | 2026-10-21 |
| AG2（AutoGen 社区分叉） | [ag2ai/ag2](https://github.com/ag2ai/ag2) | 5,008 | 74 | 246 | 383 | 0.64 | 1,398 | +39% | 2026-10-20 |
| OpenAI Agents SDK (JS) | [openai/openai-agents-js](https://github.com/openai/openai-agents-js) | 3,933 | 100 | 524 | 714 | 0.73 | 2,243 | +133% | 2026-10-21 |
| LangGraph.js | [langchain-ai/langgraphjs](https://github.com/langchain-ai/langgraphjs) | 3,370 | 74 | 257 | 332 | 0.77 | 1,213 | +56% | 2026-10-21 |
| Claude Agent SDK (TS) | [anthropics/claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript) | 1,827 | 64 | 192 | 364 | 0.53 | 1,588 | +664% | 2026-10-21 |
| Google ADK (Java) | [google/adk-java](https://github.com/google/adk-java) | 1,754 | 26 | 114 | 182 | 0.63 | 1,028 | +142% | 2026-10-21 |
| Google ADK (JS) | [google/adk-js](https://github.com/google/adk-js) | 1,445 | 36 | 149 | 291 | 0.51 | 1,411 | 新 | 2026-10-20 |
| ModelScope ms-agent | [modelscope/ms-agent](https://github.com/modelscope/ms-agent) | 4,417 | 30 | 93 | 175 | 0.53 | 950 | +27% | 2026-10-19 |

（数据来源：GitHub REST API repos 端点与 stargazers/history 端点，2026-10-21 实测；端点说明见 [GitHub Docs](https://docs.github.com/en/rest/activity/starring?apiVersion=2026-03-10#get-repository-star-history)）

**表 2：低代码/平台型与“智能体应用”类项目（对照组，2026-10-21 实测）**

| 项目 | 仓库 | Stars | Forks | 近13周 | 加速比 | 近52周 | YoY | 备注 |
|---|---|---|---|---|---|---|---|---|
| n8n | [n8n-io/n8n](https://github.com/n8n-io/n8n) | 208,191 | 61,202 | 12,678 | 0.90 | 62,837 | +43% | 工作流自动化+AI 节点 |
| Dify | [langgenius/dify](https://github.com/langgenius/dify) | 159,108 | 25,146 | 10,434 | 0.88 | 44,876 | +39% | LLM 应用/智能体平台 |
| Langflow | [langflow-ai/langflow](https://github.com/langflow-ai/langflow) | 155,884 | 10,239 | 4,471 | 0.81 | 25,320 | +19% | 可视化，基于 LangChain |
| RAGFlow | [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | 92,581 | 11,056 | 7,569 | 1.03 | 27,758 | +43% | RAG+Agent 引擎（中国团队） |
| DeerFlow（字节） | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 84,230 | 11,773 | 7,418 | 0.48 | **67,039** | **+390%** | 深度研究/超级智能体 harness |
| mem0 | [mem0ai/mem0](https://github.com/mem0ai/mem0) | 67,558 | 7,972 | 6,665 | 0.84 | 26,830 | +66% | 智能体记忆层 |
| Flowise | [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise) | 55,512 | 25,071 | 1,161 | 0.40 | 10,670 | +24% | **已归档**（archived=true，最后推送 2026-08-13） |
| Sim | [simstudioai/sim](https://github.com/simstudioai/sim) | 29,857 | 3,858 | 916 | 0.60 | 13,355 | +81% | 可视化智能体工作流 |
| Activepieces | [activepieces/activepieces](https://github.com/activepieces/activepieces) | 25,145 | 4,367 | 1,897 | 1.13 | 6,737 | +37% | 自动化 |
| Letta | [letta-ai/letta](https://github.com/letta-ai/letta) | 25,213 | 2,650 | 1,437 | 0.81 | 6,676 | +36% | 有状态智能体 |
| Coze Studio（字节扣子开源版） | [coze-dev/coze-studio](https://github.com/coze-dev/coze-studio) | 21,738 | 3,130 | 660 | 0.81 | 4,309 | +25% | 最后推送 **2026-07-29** |
| Pipecat | [pipecat-ai/pipecat](https://github.com/pipecat-ai/pipecat) | 16,679 | 2,926 | 3,069 | **1.41** | 8,273 | +98% | 语音智能体 |
| LiveKit Agents | [livekit/agents](https://github.com/livekit/agents) | 14,875 | 3,972 | 3,444 | **2.50** | 7,064 | +90% | 语音/实时智能体 |
| Coze Loop | [coze-dev/coze-loop](https://github.com/coze-dev/coze-loop) | 5,782 | 801 | 187 | 0.76 | 916 | +19% | 智能体评测/观测 |
| AutoGPT | [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) | 187,688 | 45,913 | 3,071 | 0.98 | 12,563 | +7% | 早期“自治智能体”，已转平台 |
| Claude Code（参照） | [anthropics/claude-code](https://github.com/anthropics/claude-code) | 152,714 | 26,669 | 15,074 | 0.64 | 113,918 | +294% | 编码智能体，非框架 |
| OpenAI Codex（参照） | [openai/codex](https://github.com/openai/codex) | 130,249 | 20,525 | 31,326 | **1.33** | 83,457 | +178% | 编码智能体，非框架 |
| browser-use（参照） | [browser-use/browser-use](https://github.com/browser-use/browser-use) | 118,715 | 13,187 | 13,682 | 0.79 | 48,647 | +69% | 浏览器智能体库 |
| Gemini CLI（参照） | [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | 107,480 | 14,752 | 2,595 | 0.45 | 31,562 | +42% | 编码智能体 |
| OpenHands（参照） | [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | 91,441 | 12,135 | 10,569 | 1.05 | 28,458 | +45% | 编码智能体平台 |
| goose（参照） | [aaif-goose/goose](https://github.com/aaif-goose/goose)（原 block/goose，已迁组织） | 55,478 | 6,425 | 4,601 | 0.51 | 35,701 | +181% | 通用智能体 |
| LiteLLM（参照） | [BerriAI/litellm](https://github.com/BerriAI/litellm) | 61,700 | 12,533 | 7,905 | 0.76 | 32,125 | +109% | 模型网关 |

（来源同上：GitHub REST API，2026-10-21 实测）

**历史快照对照（用于确认 15 个月趋势）**
- arXiv 论文《An Empirical Study of Agent Developer Practices in AI Agent Frameworks》表 2（数据截至 **2025-07**）：LangChain 119k、MetaGPT 59.2k、AutoGen 51.4k、LlamaIndex 45.1k、CrewAI 40k、Semantic Kernel 26.6k、LangGraph 20.6k、Swarm 20.6k、CAMEL 14.7k stars。对比 2026-10：LangGraph 20.6k→43.6k（翻倍+），CrewAI 40k→59.9k，AutoGen 51.4k→61.5k，SK 26.6k→28.7k（几乎停滞）——[arXiv 2512.01939](https://arxiv.org/html/2512.01939v1)。注意该论文正文 4.2.3 节与表 2 的 MetaGPT/LangGraph 数字自相矛盾（正文写 MetaGPT 48.7K、LangGraph 9.6K）——同一来源。
- 该论文在 1,575 个使用智能体框架的 GitHub 项目中统计实际依赖：LangChain 105 个、LangGraph 26、AutoGen 22、CrewAI 19、LlamaIndex 12、Swarm 5、BabyAGI 3、CAMEL 3、Semantic Kernel 2、MetaGPT 2；结论是“star 不能可靠预测真实采用”（MetaGPT star 最多但仅 2 个项目使用）——[arXiv 2512.01939](https://arxiv.org/html/2512.01939v1)。

**仓库状态/改名事实（2026-10-21 实测 GitHub API）**
- `strands-agents/sdk-python` 请求被重定向到 `strands-agents/harness-sdk`，描述为“Build an agent harness and control it end-to-end. Open-source SDK for production AI agents in Python & TypeScript”；原 `strands-agents/sdk-typescript` 已 archived（最后推送 2026-06-03）——[GitHub harness-sdk](https://github.com/strands-agents/harness-sdk)、[GitHub sdk-typescript](https://github.com/strands-agents/sdk-typescript)。第三方称改名与 AWS “agent harness”定位有关，未找到 AWS 官方公告——[搜索结果中的二手分析](https://rywalker.com/research/strands-agents)（未核实）。
- `block/goose` 重定向至 `aaif-goose/goose`——[GitHub](https://github.com/aaif-goose/goose)。
- `FlowiseAI/Flowise` archived=true，最后推送 2026-08-13——[GitHub](https://github.com/FlowiseAI/Flowise)。
- `microsoft/TaskWeaver` archived=true（最后推送 2026-03-23）——[GitHub](https://github.com/microsoft/TaskWeaver)。

### Inferences
- **“谁在最上面”取决于口径**：若以 star 论，前四名全是平台/低代码（n8n、Dify、Langflow）加上 LangChain；若只看“写代码用的智能体框架”，LangChain 系（LangChain 14.8 万 + LangGraph 4.4 万 + Deep Agents 3.0 万 + LangChain.js/LangGraph.js 2.2 万 ≈ 24 万）是绝对第一大阵营。
- **2025-10 ~ 2026-10 增量榜（代码优先框架）**：LangChain +3.3 万 > Deep Agents +2.6 万 > LangGraph +2.4 万 > CrewAI +2.1 万 ≈ AgentScope +2.1 万 > OpenAI Agents SDK +1.4 万 > MetaGPT +1.3 万 > Mastra +1.2 万 ≈ AutoGen +1.2 万 > MAF +1.0 万。LangChain 公司一家的三个仓库合计 +8.3 万，说明其“1.0 + Deep Agents”策略在 star 层面非常成功。
- **近一个季度普遍降温**：除 Strands（改名/“harness”重新定位带来的近 4 周 1,509 star 暴涨，占其近 13 周 67%）、AgentScope（2.0 发布后持续加速）、DSPy、语音智能体（LiveKit、Pipecat）外，几乎所有框架的季度 star 流入都低于上一季度；同期编码智能体（Codex 加速 1.33）吸走了大量注意力。
- **大厂官方 SDK 的 star 普遍“偏低”**：Claude Agent SDK（8.3k）、Strands（8.9k）、MAF（14.2k）、Google ADK（21.9k）star 远低于其下载量（见 Q2），说明官方 SDK 更多靠平台捆绑分发而非社区“收藏”。
- **中国社区项目**：DeerFlow（+6.7 万/年）、Dify（+4.5 万）、RAGFlow（+2.8 万）、AgentScope（+2.1 万）是 2025-2026 年中国团队增速最快的智能体相关仓库；MetaGPT（推送停在 2026-01，主页已指向商业产品 atoms.dev）、Qwen-Agent（推送停在 2026-03）、Coze Studio（推送停在 2026-07）呈停滞迹象。

### Gaps
- GitHub star-history 接口每周数字是否为“净增”（扣除取消 star）未在文档中说明。
- 无法独立核实 star 是否存在刷量；Langflow（15.6 万 star）与其包下载量/Docker 拉取量的巨大落差（见 Q2）值得注意，但未找到可靠的刷星调查报道。
- Gitee/GitCode 等国内托管平台的 star 数据未采集（AgentScope 等 Gitee 镜像显示 0 star，不具参考价值——搜索结果所见）。

## Q2：PyPI / npm 月下载量及与 Star 的背离

### Takeaway
下载量与 star 讲的是另一个故事：Python 侧 LangChain（1.70 亿/30天）与 LangGraph（4,477 万）依旧称霸，但**官方 SDK 下载量远超其 star 排名**——AWS Strands（3,711 万）、Claude Agent SDK（2,978 万）、OpenAI Agents SDK（1,245 万）、Google ADK（1,011 万）都远超 CrewAI（244 万）、Agno（178 万）、smolagents（43 万）；TypeScript 侧 Vercel AI SDK（`ai`，1.19 亿/月）一骑绝尘，`@anthropic-ai/claude-agent-sdk`（4,794 万/月）一年内增长约 50 倍，已超过 LangChain.js 全家。MetaGPT（7.1 万 star）月下载仅 3,393 次，是 star/使用背离最极端的例子。

### Cited Findings

**表 3：PyPI 近 30 天下载（pypistats，不含镜像，2026-10-21 抓取）**

| 包 | 近30天 | 近7天 | 对应框架 |
|---|---|---|---|
| [langchain](https://pypistats.org/packages/langchain) | 170,457,766 | 37,281,283 | LangChain |
| [langchain-core](https://pypistats.org/packages/langchain-core) | 144,826,657 | 36,120,156 | LangChain |
| [langgraph](https://pypistats.org/packages/langgraph) | 44,769,952 | 12,518,113 | LangGraph |
| [strands-agents](https://pypistats.org/packages/strands-agents) | 37,112,498 | 8,817,200 | AWS Strands |
| [langchain-openai](https://pypistats.org/packages/langchain-openai) | 36,847,880 | 10,027,892 | LangChain 集成 |
| [claude-agent-sdk](https://pypistats.org/packages/claude-agent-sdk) | 29,777,372 | 7,817,779 | Claude Agent SDK |
| [pydantic-ai-slim](https://pypistats.org/packages/pydantic-ai-slim) | 23,908,854 | 6,868,047 | Pydantic AI（核心包） |
| [openai-agents](https://pypistats.org/packages/openai-agents) | 12,449,784 | 3,271,693 | OpenAI Agents SDK |
| [google-adk](https://pypistats.org/packages/google-adk) | 10,109,331 | 2,316,962 | Google ADK |
| [browser-use](https://pypistats.org/packages/browser-use) | 8,061,974 | 1,515,390 | browser-use |
| [llama-index-core](https://pypistats.org/packages/llama-index-core) | 6,574,473 | 1,488,378 | LlamaIndex |
| [deepagents](https://pypistats.org/packages/deepagents) | 5,660,894 | 1,843,278 | Deep Agents |
| [pydantic-ai](https://pypistats.org/packages/pydantic-ai) | 5,383,780 | 1,530,678 | Pydantic AI（全量包） |
| [dspy](https://pypistats.org/packages/dspy) | 5,312,050 | 1,318,603 | DSPy（另 dspy-ai 436,928） |
| [livekit-agents](https://pypistats.org/packages/livekit-agents) | 3,609,910 | 1,076,285 | LiveKit Agents |
| [llama-index](https://pypistats.org/packages/llama-index) | 2,937,852 | 644,289 | LlamaIndex |
| [crewai](https://pypistats.org/packages/crewai) | 2,442,764 | 668,587 | CrewAI |
| [mem0ai](https://pypistats.org/packages/mem0ai) | 2,020,516 | 608,342 | mem0 |
| [agno](https://pypistats.org/packages/agno) | 1,779,568 | 519,150 | Agno（另 phidata 132,960） |
| [pipecat-ai](https://pypistats.org/packages/pipecat-ai) | 1,043,553 | 330,505 | Pipecat |
| [agent-framework-core](https://pypistats.org/packages/agent-framework-core) | 1,005,851 | 321,132 | Microsoft Agent Framework（另 agent-framework 189,927） |
| [haystack-ai](https://pypistats.org/packages/haystack-ai) | 566,454 | 116,053 | Haystack |
| [smolagents](https://pypistats.org/packages/smolagents) | 425,605 | 112,792 | smolagents |
| [autogen-core](https://pypistats.org/packages/autogen-core) / [autogen-agentchat](https://pypistats.org/packages/autogen-agentchat) | 408,564 / 379,923 | 96,435 / 86,417 | AutoGen 0.4+（另 pyautogen 198,203） |
| [semantic-kernel](https://pypistats.org/packages/semantic-kernel) | 300,767 | 73,141 | Semantic Kernel |
| [agentscope](https://pypistats.org/packages/agentscope) | 196,536 | 44,582 | AgentScope |
| [ag2](https://pypistats.org/packages/ag2) | 164,672 | 41,685 | AG2 |
| [qwen-agent](https://pypistats.org/packages/qwen-agent) | 112,735 | 22,211 | Qwen-Agent |
| [camel-ai](https://pypistats.org/packages/camel-ai) | 42,975 | 11,600 | CAMEL |
| [griptape](https://pypistats.org/packages/griptape) | 43,320 | 10,566 | Griptape |
| [langflow](https://pypistats.org/packages/langflow) | 37,742 | 9,395 | Langflow（主要走 Docker） |
| [letta](https://pypistats.org/packages/letta) | 15,031 | 2,727 | Letta |
| [metagpt](https://pypistats.org/packages/metagpt) | **3,393** | 505 | MetaGPT |
| 参照：[openai](https://pypistats.org/packages/openai) / [anthropic](https://pypistats.org/packages/anthropic) / [litellm](https://pypistats.org/packages/litellm) | 295,856,631 / 150,199,657 / 92,239,101 | — | 模型 SDK/网关 |

**表 4：npm 近一月下载（2026-09-19 ~ 2026-10-18，api.npmjs.org）及一年趋势（2025-10 月 → 2026-09 月，按月汇总）**

| 包 | 近一月 | 2025-10 月 | 2026-09 月 | 倍数 |
|---|---|---|---|---|
| [ai](https://www.npmjs.com/package/ai)（Vercel AI SDK） | 118,618,237 | 17.21M | 106.52M | 6.2× |
| [@ai-sdk/openai](https://www.npmjs.com/package/@ai-sdk/openai) | 60,708,847 | — | — | — |
| [@anthropic-ai/claude-agent-sdk](https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk) | 47,942,851 | 0.96M | 48.50M | **~50×** |
| [@langchain/core](https://www.npmjs.com/package/@langchain/core) | 24,516,502 | 7.98M | 23.21M | 2.9× |
| [@langchain/openai](https://www.npmjs.com/package/@langchain/openai) | 15,808,798 | — | — | — |
| [@langchain/langgraph](https://www.npmjs.com/package/@langchain/langgraph) | 14,810,017 | 2.57M | 14.09M | 5.5× |
| [langchain](https://www.npmjs.com/package/langchain) | 12,279,365 | 5.42M | 12.05M | 2.2× |
| [@openai/agents](https://www.npmjs.com/package/@openai/agents) | 8,391,693 | 0.54M | 7.48M | 13.9× |
| [@mastra/core](https://www.npmjs.com/package/@mastra/core) | 8,027,650 | 0.97M | 7.05M | 7.3× |
| [mastra](https://www.npmjs.com/package/mastra)（CLI） | 3,357,541 | — | — | — |
| [@strands-agents/sdk](https://www.npmjs.com/package/@strands-agents/sdk) | 2,212,702 | ~0 | 2.03M | 2026-07 由 0.20M 跃升至 1.41M |
| [@microsoft/agents-hosting](https://www.npmjs.com/package/@microsoft/agents-hosting) | 1,804,012 | — | — | 注：M365 Agents SDK，非 MAF |
| [deepagents](https://www.npmjs.com/package/deepagents) | 1,438,343 | 0.01M | 1.35M | >100× |
| [@google/adk](https://www.npmjs.com/package/@google/adk) | 1,181,419 | 0.00M | 0.94M | 新 |
| [llamaindex](https://www.npmjs.com/package/llamaindex) | 569,878 | 0.21M | 0.51M | 2.4× |
| [n8n](https://www.npmjs.com/package/n8n) | 467,680 | 0.31M | 0.38M | 平（主要走 Docker） |
| [@llamaindex/workflow](https://www.npmjs.com/package/@llamaindex/workflow) | 433,089 | — | — | — |
| [@voltagent/core](https://www.npmjs.com/package/@voltagent/core) | 148,943 | 0.02M | 0.12M | 6× |
| [flowise](https://www.npmjs.com/package/flowise) | 11,251 | — | — | 已停更 |
| 参照：[@modelcontextprotocol/sdk](https://www.npmjs.com/package/@modelcontextprotocol/sdk) / [@anthropic-ai/sdk](https://www.npmjs.com/package/@anthropic-ai/sdk) / [openai](https://www.npmjs.com/package/openai) | 256.8M / 182.4M / 171.9M | — | — | — |

（数据源：[npm downloads API](https://api.npmjs.org/downloads/point/last-month/ai)，2026-10-21 抓取）

**表 5：PyPI 按自然月下载（pypistats overall，不含镜像；单位百万；2026-05 ~ 2026-09）**

| 包 | 5月 | 6月 | 7月 | 8月 | 9月 |
|---|---|---|---|---|---|
| langchain | 289.65 | 328.34 | 315.78 | 244.57 | 170.34 |
| langgraph | 54.76 | 63.78 | 72.64 | 65.79 | 44.97 |
| strands-agents | 8.67 | 34.39 | 36.27 | 37.41 | 37.17 |
| claude-agent-sdk | 14.23 | 19.92 | 30.17 | 31.62 | 29.86 |
| openai-agents | 32.31 | 31.08 | 35.18 | 35.80 | 12.53 |
| google-adk | 19.73 | 21.35 | 18.82 | 20.35 | 10.25 |
| pydantic-ai-slim | 268.16 | 223.57 | 154.80 | 119.64 | 24.04 |
| llama-index-core | 11.84 | 15.77 | 16.40 | 13.38 | 6.70 |
| crewai | 14.45 | 11.94 | 12.36 | 28.51 | 2.44 |
| dspy | 7.32 | 6.24 | 6.45 | 6.27 | 5.34 |
| deepagents | 4.70 | 5.78 | 6.48 | 5.64 | 5.52 |
| agno | 3.73 | 3.03 | 2.23 | 2.14 | 1.78 |
| agent-framework-core | 1.44 | 1.91 | 2.27 | 2.25 | 0.97 |
| autogen-agentchat | 1.47 | 1.29 | 1.05 | 0.95 | 0.39 |
| semantic-kernel | 2.85 | 2.55 | 2.76 | 2.30 | 0.30 |
| ag2 | 0.72 | 0.61 | 0.50 | 0.33 | 0.18 |
| smolagents | 0.66 | 0.65 | 0.63 | 0.59 | 0.43 |

（来源：[pypistats.org API](https://pypistats.org/api/packages/langgraph/overall?mirrors=false)，2026-10-21 抓取；pypistats 只保留最近 180 天）

**Docker Hub 累计拉取（平台型项目的“下载量”代理，2026-10-21 抓取）**
- [n8nio/n8n](https://hub.docker.com/r/n8nio/n8n) 274,470,029；[langgenius/dify-api](https://hub.docker.com/r/langgenius/dify-api) 25,015,961（dify-web 16,478,342）；[flowiseai/flowise](https://hub.docker.com/r/flowiseai/flowise) 7,118,526（最后更新 2026-07-31）；[langflowai/langflow](https://hub.docker.com/r/langflowai/langflow) 4,332,582；[infiniflow/ragflow](https://hub.docker.com/r/infiniflow/ragflow) 3,923,816。

**第三方对 star/下载背离的分析**
- 一篇第三方分析的标题称“开发者给 Dify 点 star，但实测使用量走 LangGraph——LangGraph 只占 8.5% 的 star，却占所统计 4 个项目 5,090 万月下载的 67.8%”——[Keenable Select](https://select.keenable.ai/r/open-source-ai-agents-usage-github-share/jfXoGkRU0H2l6G2hKZhPGw)（二手，口径未核实）。

### Inferences
- **Python 下载量排名（近 30 天，取各框架主包）**：LangChain ≫ LangGraph > Strands > Claude Agent SDK > Pydantic AI（slim）> OpenAI Agents SDK > Google ADK > LlamaIndex > Deep Agents ≈ DSPy > CrewAI > Agno > MAF > Haystack > smolagents > AutoGen > Semantic Kernel > AgentScope > AG2 > CAMEL > MetaGPT。
- **TypeScript 下载量排名**：Vercel AI SDK ≫ Claude Agent SDK > LangChain.js/LangGraph.js > OpenAI Agents SDK ≈ Mastra > Strands TS > Deep Agents JS > Google ADK JS > LlamaIndex.TS > VoltAgent。npm 数据曲线平滑、一年内几乎所有智能体 SDK 都在数倍增长，是比 PyPI 更可信的趋势信号。
- **Claude Agent SDK 与 Strands 的超高下载量很可能来自“被捆绑/被依赖”**（如 Claude Code 生态工具、CI、AWS 内部工具链/AgentCore 相关模板）而非独立开发者主动选型——证据：其 star 仅 8k 级，且在 SO 2026 调查中 Strands 仅 4.0%、Claude Agent SDK 未出现在选项榜（见 Q3）。此为推断，未找到依赖关系的公开拆解。
- **PyPI 数据在 2026-09 出现剧烈断崖**（semantic-kernel −87%、crewai −91%、pydantic-ai-slim −80%、openai-agents −65%、google-adk −50%、autogen-agentchat −59%，而 claude-agent-sdk、strands、deepagents、agno 基本持平）。降幅不一致，说明是**大规模 CI/自动化安装方的变化或统计口径变化**而非真实开发者流失；报告中引用 PyPI 时应强调“仅作横向量级比较，不宜做月度趋势判断”，月度趋势以 npm 为准。CrewAI 2026-08 的 2,851 万也明显是异常尖峰。
- **平台型项目必须看 Docker 拉取而非包下载**：n8n 的 2.74 亿次 Docker 拉取远超 Dify（约 2,500 万）和 Langflow（433 万），与 star 排名（n8n > Dify > Langflow）方向一致，但 Langflow 的 star/拉取比显著偏高。
- **MetaGPT 是 star 与使用背离的最极端案例**：7.1 万 star vs 月下载 3,393 次（0.05 次/星/月），而 LangGraph 约 1,026 次/星/月。

### Gaps
- 未使用 pepy.tech（需 API Key，且含镜像，数值通常高于 pypistats）；如报告需要 pepy 口径须另行获取。
- Dify、Coze Studio 无 PyPI/npm 包，无可比的“下载量”；Docker Hub 只给累计值，无法算月度。
- 无法拆分下载中“CI/依赖传递”与“开发者直接安装”的比例。
- 2026-09 PyPI 断崖的确切原因未查到公开说明。

## Q3：开发者调查与分析师报告中的框架使用率

### Takeaway
最权威、最新的横向数据来自 **Stack Overflow 2026 开发者调查（2026-10-06 发布，>3 万人）**：在“智能体编排/框架”题（n=4,400）中 LangChain 30.2% 居首，OpenAI Agents SDK 23.8% 第二，LangGraph 18.8%、Llama Stack 17.4%、Google ADK 14.0%、Vercel AI SDK 9.0%、Pydantic AI 8.9%，CrewAI（5.5%）、Semantic Kernel（5.0%）、AutoGen（4.5%）、Strands（4.0%）、Mastra（3.0%）、Dify（2.9%）、Agno（2.4%）均在个位数；自动化类中 Make 38.9%、n8n 32.7%。与 2025 年对比，LangGraph 上升、AutoGen 腰斩（12.0%→4.5%）、CrewAI 下滑（7.5%→5.5%）。

### Cited Findings

**Stack Overflow 2026 开发者调查（结果发布 2026-10-06）**
- 总样本：超过 30,000 人、历时 7 周；使用 AI 编码助手/智能体的受访者中 73% 每日使用；编码智能体使用率 66%、聊天机器人 63%——[Stack Overflow Blog 2026-10-06](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/)。
- **智能体编排/框架（过去一年使用，n=4,400）**：LangChain 30.2%（1,329）、OpenAI Agents SDK 23.8%（1,048）、Terminal Use 18.9%、LangGraph 18.8%（825）、Llama Stack 17.4%、Google ADK 14.0%（617）、Hermes Agent 10.2%、Vercel AI SDK 9.0%、Pydantic AI 8.9%、CrewAI 5.5%、Semantic Kernel 5.0%、AutoGen 4.5%、Strands 4.0%、DSPy 3.6%、Mastra 3.0%、Dify 2.9%、Smolagents 2.6%、Atomic Agents 2.6%、Instructor 2.4%、Agno 2.4%、21st.dev 2.3%、GripTape 2.1%——[SO 2026 AI 数据页](https://survey.stackoverflow.co/2026/ai/data)、[SO 2026 AI 页](https://survey.stackoverflow.co/2026/ai)。
- **智能体自动化/工作流（n=4,173）**：Make 38.9%、n8n 32.7%、Zapier 18.5%、Temporal 6.0%、Prefect 3.0%、Trigger.dev 2.4%、Inngest 2.3%、Gumloop 2.2%、Relay.app 2.2%、DBOS 2.1%、Activepieces 2.0%——[SO 2026 AI 数据页](https://survey.stackoverflow.co/2026/ai/data)。
- **编码智能体（n=12,255，作为参照）**：Claude Code 65.5%、GitHub Copilot 58.7%、OpenAI Codex 29.5%、Cursor 25.5%、Google Antigravity 16.0%、Gemini Code Assist 14.6%——[SO 2026 AI 数据页](https://survey.stackoverflow.co/2026/ai/data)。
- 模型提供方：Anthropic 与 OpenAI 使用水平相近，Google 远居第三（无精确百分比）——[Stack Overflow Blog 2026-10-06](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/)。

**Stack Overflow 2025 开发者调查（2025 年数据，用于对比）**
- 智能体使用频率（n=31,877）：工作中每日用智能体 14.1%、每周 9.0%、每月或更少 7.8%、不用但计划用 17.4%、只用 copilot/补全 13.8%、不打算用 37.9%——[SO 2025 AI](https://survey.stackoverflow.co/2025/ai)。
- 智能体框架/编排（n=3,758）：Ollama 51.1%、LangChain 32.9%、LangGraph 16.2%、Vertex AI 15.1%、Amazon Bedrock Agents 14.5%、OpenRouter 13.4%、LlamaIndex 13.3%、AutoGen 12.0%、Zapier 11.8%、CrewAI 7.5%、Semantic Kernel 6.0%、IBM watsonx.ai 5.7%、Haystack 4.4%、Smolagents 3.7%、Agno 3.4%、phidata 2.1%——[SO 2025 AI](https://survey.stackoverflow.co/2025/ai)。
- 智能体可观测性（n=2,689）：LangSmith 12.5%、Langfuse 8.8%；记忆/数据：Redis 42.9%、GitHub MCP Server 42.8%、mem0 4.0%、Letta 2.5%——[SO 2025 AI](https://survey.stackoverflow.co/2025/ai)。

**LangChain《State of Agent Engineering》**
- 1,340 份回复，调查窗口 2025-11-18 ~ 2025-12-02（页面标注日期 2026-06-12，可能为更新日期）；57.3% 已有智能体在生产（上年 51%），30.4% 在开发并计划上线；万人以上企业 67% 在生产；最大障碍为质量（32%），其次延迟（20%）；89% 有可观测性，62% 有逐步追踪；离线评测 52.4%；超三分之二使用 OpenAI GPT 模型，超四分之三多模型并用。**报告未给出各框架使用占比**；样本中科技行业 63%、百人以下公司 49%，且由厂商发布——[LangChain State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering)。

**学术研究**
- 对 1,575 个项目的实证研究（数据截至 2025-07）：LangChain 依赖项目数 105，LangGraph 26（第二，且 2025 年初后月度使用快速上升），AutoGen 22，CrewAI 19；约 96% 的高 star 项目同时使用两个以上框架；超过 80% 开发者表示难以选出合适框架——[arXiv 2512.01939](https://arxiv.org/html/2512.01939v1)。

### Inferences
- **SO 2025→2026 对比（选项列表有变化，仅作近似）**：LangChain 32.9%→30.2%（基本持平，仍第一）；LangGraph 16.2%→18.8%（上升）；AutoGen 12.0%→4.5%（崩塌，与其进入维护/归档一致）；CrewAI 7.5%→5.5%；Semantic Kernel 6.0%→5.0%；Smolagents 3.7%→2.6%；Agno 3.4%→2.4%。2026 年新进榜且直接冲到高位的是 OpenAI Agents SDK（23.8%）与 Google ADK（14.0%）——大厂官方 SDK 是 2026 年调查口径下最大的新变量。Ollama、LlamaIndex 在 2026 年榜单中未出现，可能是选项调整，不能解读为归零。
- **调查口径的“前五”**（2026）：LangChain、OpenAI Agents SDK、LangGraph、Google ADK、Vercel AI SDK/Pydantic AI；结合下载量，可认为 LangChain/LangGraph 仍是事实标准，OpenAI Agents SDK 是第二极。
- Claude Agent SDK 下载量巨大却未出现在 SO 2026 框架榜，可能因被归入“编码智能体/Claude Code”心智，或调查未列为选项——需在报告中注明这一口径缺口。
- SO 调查样本以欧美开发者为主，Dify（2.9%）、AgentScope、Coze 等中国生态框架被系统性低估。

### Gaps
- **未找到** JetBrains 2025/2026 开发者生态调查中按框架拆分的使用率（搜索仅得到概述，无框架数字）。
- **未找到** Gartner / Forrester / IDC / a16z / Retool 公开的、按开源框架拆分的使用率数据（可能在付费报告中）。
- **未找到** Datadog “State of AI Engineering” 原文；某二手分析提到 Datadog 遥测中框架采用占服务比例约 18%，未能核实——[the-agent-report.com](https://the-agent-report.com/2026/05/state-of-agent-engineering-2026-langchain-datadog/)（未核实）。
- **未找到** 面向中国开发者的、带框架使用率的权威调查（CSDN/InfoQ 中国/机器之心/量子位均未检索到量化榜单）。

## Q4：2025-2026 增长最快 vs 停滞/弃用/合并的框架

### Takeaway
增长最快：LangChain 系的 **Deep Agents**（star +605%，npm 一年 >100 倍）、**LangGraph**（star +121%，npm 5.5 倍）、**Claude Agent SDK**（npm ~50 倍）、**OpenAI Agents SDK**（npm 13.9 倍，SO 2026 第二）、**Mastra**（npm 7.3 倍、获 A 轮）、**Vercel AI SDK**（npm 6.2 倍，月下载破亿）、**Microsoft Agent Framework**（star +266%，2026-04 GA）、**AgentScope**（+157%，唯一加速的主流多智能体框架）以及中国的 **DeerFlow**（+390%）。明确衰退/退场：**AutoGen**（README 声明已归档、不再维护，SO 使用率 12.0%→4.5%）、**Flowise**（2026-07 宣布终止，2026-08 仓库归档）、**Semantic Kernel**（并入 MAF，star 年增仅 10%，PyPI 9 月 −87%）、**MetaGPT**（2026-01 后无推送，下载近乎为零）、**OpenAI Swarm**、**TaskWeaver**（已归档）、**AG2**（PyPI 月下载 2026-05→09 下滑约 75%）。

### Cited Findings
- **AutoGen → Microsoft Agent Framework**：AutoGen README（2026-10-21 读取）写明 “AutoGen is now archived and no longer maintained by Microsoft”，并称 MAF 为 “enterprise‑ready successor to AutoGen”，建议新用户使用 MAF 并按迁移指南迁移（注：GitHub 的 archived 标志当日仍为 false，最后推送 2026-10-16）——[microsoft/autogen README](https://github.com/microsoft/autogen)。
- **MAF 1.0 GA**：2026-04-03 Microsoft Agent Framework .NET 与 Python 同时发布 1.0，API 稳定并承诺长期支持，定位为统一 Semantic Kernel 的企业级基础与 AutoGen 的编排能力；2 月发布 RC——[Microsoft DevBlogs](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)、[Visual Studio Magazine 2026-04-06](https://visualstudiomagazine.com/articles/2026/04/06/microsoft-ships-production-ready-agent-framework-1-0-for-net-and-python.aspx)。二手来源称 AutoGen 于 2025-10 进入维护模式——[agentmarketcap.ai](https://agentmarketcap.ai/blog/2026/04/16/microsoft-agent-framework-1-0-ga-lts-langgraph-crewai-autogen)（二手）。
- MAF 发版节奏极快：python-1.22.0（2026-10-15）、dotnet-1.25.0（2026-10-14）、python-1.21.0（2026-10-08）——[GitHub Releases](https://github.com/microsoft/agent-framework/releases)（2026-10-21 实测）。
- **AG2**：README 称 `pip install ag2` 已不再提供 `autogen` 导入名与经典智能体类，经典 API 移入 “AG2 Classic”——[ag2ai/ag2 README](https://github.com/ag2ai/ag2)。PyPI ag2 月下载 2026-05 0.72M → 2026-09 0.18M——[pypistats](https://pypistats.org/packages/ag2)。
- **Flowise 退场**：被 Workday 收购（2025-08-14 宣布，条款未披露，当时 4.2 万+ star）——[SiliconANGLE 2025-08-15](https://siliconangle.com/2025/08/15/workday-acquires-flowise-boost-ai-powered-workflows/)、[Workday 新闻稿 PDF](https://s21.q4cdn.com/950027458/files/doc_news/Workday-Acquires-Flowise-Bringing-Powerful-AI-Agent-Builder-Capabilities-to-the-Workday-Platform-08-14-2025-2025.pdf)；2026-07-29 宣布停止功能开发、不再接受 PR，2026-08-10 计划转为公开归档，npm 包与 Docker 镜像标记为 deprecated，2026-08-31 核心团队退出 Discord/GitHub；官方给出的理由是开发者越来越依赖 Claude Code、OpenClaw 等编码智能体，僵化的低代码工作流“在复杂度面前很快触顶”——[Flowise Sunset 页面](https://flowiseai.com/sunset)；GitHub 实测 archived=true，最后推送 2026-08-13——[GitHub](https://github.com/FlowiseAI/Flowise)。二手来源称托管版将于 2026-11-30 关停、存在未修补的高危安全公告——（搜索摘要，未核实原文）。
- **Strands 重新定位**：Python 仓库改名为 harness-sdk 并合并 Python/TS（TS 独立仓库 2026-06-03 归档），近 4 周新增 1,509 star（前 13 周仅 993），npm `@strands-agents/sdk` 2026-07 月下载由 0.20M 跃至 1.41M——GitHub API 与 [npm API](https://api.npmjs.org/downloads/range/2025-10-01:2026-09-30/@strands-agents/sdk)（2026-10-21 实测）。
- **LangChain 1.0 / LangGraph 1.0** 于 2025-10 与 B 轮融资同时发布——[Fortune 2025-10-20](https://fortune.com/2025/10/20/exclusive-early-ai-darling-langchain-is-now-a-unicorn-with-a-fresh-125-million-in-funding/)、[SiliconANGLE 2025-10-20](https://siliconangle.com/2025/10/20/ai-agent-tooling-provider-langchain-raises-125m-1-25b-valuation)。
- **AgentScope 2.0**：官方 README 新闻栏显示 2026-05 发布 AgentScope 2.0，6 月陆续加入 Agentic Memory、RAG、Agent Team——（搜索摘要引用其 README，[gittrend 镜像页](https://gittrend.io/repo/agentscope-ai/agentscope)，二手）；GitHub 实测近 13 周 5,609 star，加速比 1.35。
- **增长/衰退的量化证据**：见 Q1 表 1/表 2 的 52 周与加速比列、Q2 表 4 的 npm 倍数列、Q3 的 SO 2025→2026 变化（AutoGen 12.0%→4.5%，LangGraph 16.2%→18.8%）。

### Inferences
- **2025-2026 的结构性变化**：（1）大厂官方 SDK 崛起——OpenAI Agents SDK、Claude Agent SDK、Google ADK、AWS Strands、MAF 在 18 个月内从零做到千万级月下载或调查前五；（2）微软阵营整合（AutoGen + SK → MAF），导致 AutoGen/SK 使用率塌缩、AG2 社区分叉失去动能；（3）“智能体 harness/深度智能体”成为新范式（LangChain Deep Agents、Strands harness、DeerFlow 2.0、Claude Agent SDK），与编码智能体（Claude Code/Codex）同源；（4）低代码出现分化——n8n、Dify 继续增长，Flowise 被收购后关停，其官方理由直接点名编码智能体冲击。
- **“热但在降温”**：CrewAI（star 加速比 0.65，SO 7.5%→5.5%，PyPI 9 月异常下跌）、OpenAI Agents SDK（star 加速比 0.41，但 npm 仍月月新高）——star 降温不等于使用下降，需结合 npm。
- **停滞信号**：MetaGPT（2026-01 起无推送、主页转向 atoms.dev 商业产品）、Qwen-Agent（2026-03 起无推送）、Coze Studio（2026-07 起无推送）、OpenAI Swarm（年增 9%）、Semantic Kernel（年增 10%）、LangChain.js（年增 16%，但 npm 下载仍增长 2.2 倍）。

### Gaps
- Coze Studio 停止推送的原因（是否迁移仓库/转内部开发）未查证。
- MetaGPT 团队是否正式宣布停止维护未查证（仅有推送停滞和主页变化两点证据）。
- Strands “harness” 发布日期（二手称 2026-09-21）未找到 AWS 官方来源。
- OpenAI Swarm README 中“被 Agents SDK 取代”的表述本会话未重新核实（为 2025 年已知信息）。

## Q5：融资、收购与公司背书

### Takeaway
资本层面最强的三家是 **LangChain**（2025-10 B 轮 1.25 亿美元、估值 12.5 亿美元）、**n8n**（2025-10 C 轮 1.8 亿美元、估值 25 亿；2026-05 SAP 战略投资后据报估值 52 亿）和 **Mastra**（2026-04 A 轮 2,200 万美元）；**CrewAI** 自 2024-10 后未见新融资（累计约 1,800 万美元）；**Dify（LangGenius）** 据报 2026-03 完成 3,000 万美元 Pre-A；**Flowise** 被 Workday 收购后于 2026 年关停。其余热门框架多由云/模型大厂直接背书（OpenAI、Anthropic、Google、AWS、Microsoft、阿里、字节）。

### Cited Findings
- **LangChain**：2025-10-20 宣布 1.25 亿美元 B 轮、估值 12.5 亿美元，IVP 领投，Sequoia、Benchmark 跟投，新投资方含 CapitalG、Sapphire、ServiceNow Ventures、Workday Ventures、Cisco、Datadog、Databricks 等；同时发布 LangChain 1.0、LangGraph 1.0、Insights Agent 与无代码 Agent Builder——[Fortune](https://fortune.com/2025/10/20/exclusive-early-ai-darling-langchain-is-now-a-unicorn-with-a-fresh-125-million-in-funding/)、[SiliconANGLE](https://siliconangle.com/2025/10/20/ai-agent-tooling-provider-langchain-raises-125m-1-25b-valuation)。Sacra 称 2025-07 曾有 1 亿美元 B 轮（估值 11 亿），与上述是否为同一轮存在说法冲突——[Sacra](https://sacra.com/research/langchain)。2026 年未检索到新一轮融资。
- **n8n**：2025-10 由 Accel 领投 1.8 亿美元 C 轮、估值 25 亿美元——[Sifted](https://sifted.eu/articles/n8n-hits-2-5bn-valuation)、[Osborne Clarke](https://www.osborneclarke.com/news/osborne-clarke-advises-investors-n8n-gmbhs-unicorn-funding-round-over-usd-180-million)；2026-05 SAP 战略投资，据 Bloomberg 报道估值翻倍至 52 亿美元，并计划把 n8n 嵌入 SAP Joule Studio——[Odaily（援引 Bloomberg）](https://www.odaily.news/en/newsflash/480846)、[Bolsamania 新闻稿](https://www.bolsamania.com/nota-de-prensa_email/mercados/n8n-valuation-doubles-to-52bn-as-sap-makes-strategic-investment-and-plans-to-embed-the-ai-platform-into-joule-studio--22470787.html)。AutomationAtlas 给出的“2025-11 6,000 万美元 C 轮、估值 6 亿”与上述冲突，应视为错误——[AutomationAtlas](https://automationatlas.io/answers/n8n-series-c-valuation-2025/)。
- **Mastra**：2025-10 宣布 1,300 万美元种子轮（YC 领投）；2026-04-09 宣布 2,200 万美元 A 轮（Spark Capital 领投），累计约 3,500 万美元，同时发布 Mastra Studio、Mastra Server、Memory Gateway；客户包括 Brex、Indeed、Marsh McLennan——[Techleap](https://finder.techleap.nl/news/feed/mastra-raises-22m-series-a-to-help-developers-build-ai-agents)（二手聚合；Caplight/PitchBook 累计额略有出入）。
- **CrewAI**：累计约 1,800 万美元（种子轮 boldstart 领投 + A 轮 Insight Partners 领投，2024-10 公布）；2026 年未见新融资；二手报道估计其 2025 年 ARR 约 320 万美元、员工从 29 人增至约 50 人（2026 年中）——[The Bridge Club](https://thebridgeclub.beehiiv.com/p/crewai-secures-18m-for-ai-agents)、[Wikipedia](https://en.wikipedia.org/wiki/CrewAI)、[descubre.vc 2026-09-15](https://www.descubre.vc/noticia/crewai-alcanza-3-2m-en-arr-y-consolida-18m-en-financiamiento-total-2026-09-15)（ARR 为估算，未核实）。
- **Dify / LangGenius**：据报 2026-03 完成 3,000 万美元 Pre-A 轮，HSG 领投，GL Ventures、Alt-Alpha、5Y Capital（五源）、Mizuho Leaguer、NYX Ventures 参投——[yespress](https://yespress.io/products/dify.md)、[ToolJunction](https://www.tooljunction.io/ai-tools/dify-ai/company)（均为二手，ToolJunction 给出的“累计 4,150 万、估值 1.8 亿”可信度低）。2026 年在日本有 KDDI（povo2.0 客服）等案例——[dime.jp](https://dime.jp/company_news/detail/?pr=2663112)。
- **Flowise**：Workday 2025-08-14 收购（条款未披露）——[SiliconANGLE](https://siliconangle.com/2025/08/15/workday-acquires-flowise-boost-ai-powered-workflows/)；2026-07-29 宣布终止——[Flowise Sunset](https://flowiseai.com/sunset)。
- **大厂背书（仓库归属，GitHub 实测）**：OpenAI（openai-agents-python/js）、Anthropic（claude-agent-sdk-python/typescript）、Google（adk-python/go/java/js）、AWS（strands-agents）、Microsoft（agent-framework、semantic-kernel、autogen）、Hugging Face（smolagents）、Pydantic（pydantic-ai）、Vercel（ai）、阿里（agentscope-ai、QwenLM/Qwen-Agent、alibaba/spring-ai-alibaba）、字节（coze-dev、cloudwego/eino、bytedance/deer-flow）、斯坦福（stanfordnlp/dspy）、deepset（haystack）——各仓库链接见 Q1 表 1/表 2。

### Inferences
- 独立框架公司里，LangChain 的资本、调查份额、下载量、star 增量四项全部第一，是 2026 年“最热”框架的最稳妥结论；n8n 则是平台/自动化赛道的绝对龙头（star、Docker 拉取、估值均第一，SO 自动化类 32.7% 仅次于 Make）。
- CrewAI 融资停在 2024 年、调查份额下滑、star 加速比 0.65，处于“声量仍高但动能减弱”阶段；Mastra 则凭 A 轮与 npm 7 倍增长成为 TS 智能体框架的独立新贵（但在 SO 2026 仅 3.0%）。
- 官方 SDK 依靠模型/云平台分发获得下载量，对独立框架公司形成挤压——Flowise 的关停声明与 AutoGen 的退场都是这一趋势的信号。

### Gaps
- Agno、Pydantic（公司）、LlamaIndex、Letta、mem0 等 2025-2026 融资情况本次未检索。
- LangChain 2025 年 7 月/10 月两笔 B 轮是否为同一轮，来源冲突未解决。
- n8n 52 亿美元估值仅见 Bloomberg 转述与新闻稿转载，未获 SAP 官方新闻稿原文。
- Dify Pre-A 融资未找到一手公告（官方博客/工商信息）。
