# Claude Code 定制效果评测：工具与方法调研

> 调研日期：2026-09-28 ｜ 本机环境：Claude Code 2.1.259（macOS）
> 要回答的问题：在 Claude Code 上叠加 CLAUDE.md、skills、plugins、hooks 等定制后，怎样量化"加之前 vs 加之后"的效果差异？有哪些评测工具可用？
> 可信度标记：🔬 本机实测 ｜ 📄 官方文档 / 论文一手来源 ｜ ⚠️ 推论或未核实

---

## 1. 结论速览

| 要评测的定制 | 首选 | 备选 | 理由 |
|---|---|---|---|
| 一个 plugin（含其 skills / agents / hooks / MCP） | `claude plugin eval` 📄 | skill-creator | 官方内置"无插件基线"对照臂，直接给出 `WITH` / `W/OUT` / `Δ`；需 ≥ v2.1.269，本机 2.1.259 先 `claude update` |
| 单个 skill（效果 + 触发率） | skill-creator 插件 📄 | 包成插件后用 `claude plugin eval` | 在对话内迭代：with/without 基准、两版本盲评、description 触发率优化 |
| 用户级 CLAUDE.md、hooks、整套配置 | 自建 A/B：`claude -p`，基线臂用 `--safe-mode` 🔬 | promptfoo、Harbor（见第 4 节） | 官方 eval 的隔离沙箱**不加载** CLAUDE.md、hooks、个人 skills，目前没有官方一键方案 |
| 真实使用中的成本与使用率 | `/skill-doctor`、`/usage`、`/doctor`、`claude plugin details` 📄 | OpenTelemetry → 观测平台 | 只能观测趋势，不能替代对照实验；用来找"从没用过却常驻上下文"的定制 |

三条核心判断：

1. **成本一定涨，收益不一定。** 你当前的全部定制让每次请求多带约 **10.9k token** 常驻上下文 🔬；ETH 的论文发现上下文文件总体不提升任务成功率，推理成本却 +20% 以上 📄；SkillsBench 中人工精选的 skill 平均 +16.6pp，但并非每个任务都受益 📄。结论：每一项定制都要用数据证明自己。
2. **触发与效果分开测。** 官方文档明确要求分别度量"该触发时是否触发"和"触发后输出是否正确" 📄；Vercel 的评测里 56% 的用例 skill 根本没被调用 📄。
3. **实验设计比选哪个工具更重要。** 同题配对、每臂 ≥ 3 次、固定模型、每次干净环境、看 Δ 和 pass^k 而不是单次结果；小于 3pp 的差异要存疑 📄。

---

## 2. 本机实测：你的定制带来的常驻成本 🔬

### 2.1 各插件的常驻 token（`claude plugin details <name>`）

| 插件 | 组件 | 常驻 token（每次会话都付） |
|---|---|---|
| compound-engineering | 42 skills | ~3,213 |
| claude-obsidian | 19 skills、3 agents、4 hooks | ~2,517 |
| financial-analysis | 20 skills | ~1,282 |
| mattpocock-skills | 25 skills | ~1,117 |
| investment-banking | 16 skills | ~922 |

官方文档：常驻 ≥ 2,000 token 的插件会在 `/plugin` 详情里被高亮提示 📄（[Measure plugin cost and usage](https://code.claude.com/docs/en/plugins/measure)）。上表前两项超过这条线。

### 2.2 全部定制 vs `--safe-mode`

同一提示（"只回复 OK"）、同一模型（haiku）、空目录，各跑一次：

| 指标 | 全部定制 | `--safe-mode` |
|---|---|---|
| 输入侧 token（input + cache 写 + cache 读） | 42,742 | 31,879 |
| 可用 skills | 164 | 19（全部为内置） |
| 可用 subagents | 59 | 5 |
| MCP servers | 11 | 0 |
| 工具数 | 91 | 31 |
| 能否看到用户级 CLAUDE.md | 能（正确引用红线"不捏造事实"） | 不能（回复 `NONE`） |

→ 全部定制 ≈ **每次请求 +10.9k token**。`--safe-mode` 是经过验证的干净基线。

### 2.3 实测中踩到的坑

| 现象 | 影响 | 对策 |
|---|---|---|
| 两次调用成本 $0.086 vs $0.013，差距主要来自第二次命中了第一次写入的缓存前缀 | 直接比美元会高估/低估定制成本 | 比较 token 数，或先预热各臂缓存；成本只看多次运行的均值 |
| `--safe-mode` 下 `init` 事件的 `plugins` 字段仍列出 10 个插件，但它们的 skills / agents 都没加载 | 看 `plugins` 字段会误判基线不干净 | 以 `skills`、`agents`、`mcp_servers` 字段为准 |
| `--safe-mode --plugin-dir <插件>` 叠加后插件**不加载**（mattpocock skills 0 个） | 无法用 safe-mode 拼出"只开某一个插件"的臂 | 单插件消融交给 `claude plugin eval` |
| `--safe-mode --append-system-prompt-file <文件>` 有效（测试规则被遵守） | 可以近似构造"只加 CLAUDE.md"的臂 | 注意位置差异：CLAUDE.md 平时以上下文消息注入，而不是 system prompt ⚠️ |
| `-p --output-format stream-json` 不加 `--verbose` 直接报错 | 脚本跑不起来 | 固定加 `--verbose`；脚本里加 `< /dev/null`，避免等待 stdin 的 3 秒提示 |
| 本机 `claude plugin eval init --bare` 只打印 "plugin eval is currently in early access" | 命令看得到但用不了 | 官方排障：构建早于 GA 版本，`claude update` 后在新会话重试 📄 |
| `claude plugin details tdd-agents@skills-dir` 报找不到 | 只有 `SKILL.md` 的个人 skill 不是插件，官方 eval 无法直接指向它 | 包一层 `.claude-plugin/plugin.json` + `skills/<name>/SKILL.md` 再评测 |

---

## 3. 官方工具

### 3.1 `claude plugin eval` 📄

v2.1.269 发布（2026 年第 37 周，9 月 7–11 日）。来源：[Test plugins with evals](https://code.claude.com/docs/en/plugin-evals)、[Week 37 更新说明](https://code.claude.com/docs/en/whats-new/2026-w37)。

**工作方式**：每个用例在隔离的 `claude -p` 子进程里运行，只加载被测插件；跑完后用 grader 检查最终回复、transcript 或生成的文件。

| 维度 | 说明 |
|---|---|
| 对照 | 默认两臂：带插件（WITH）与不带任何插件（W/OUT），`Δ = WITH − W/OUT`；`--ablation none` 只跑带插件臂，成本减半 |
| 重复 | 每臂默认 3 次（`runs` 1–50）；单次得分 = 通过的 grader 占比（可加权），用例得分 = 各次均值，≥ `--threshold`（默认 1.0）算通过 |
| 防 Δ 虚高 | "skill 是否被调用"（`tool_used: Skill`）这类只可能在带插件臂通过的 grader，默认只作指示、不计分；可用 `arm: both` / `arm: with-only` 调整 |
| 用例格式 | `evals/<case>/prompt.md`（frontmatter：`runs`、`model`、`max_turns` 默认 10、`timeout_seconds` 默认 300、`allowed_tools`、`append_system_prompt`、`env` 仅限 `EVAL_*`、`tags`、`plugins`）+ `graders/*.md`；可选 `case.yaml`（`context.scaffold_script` / `history_file` / `add_dirs`） |
| 生成用例 | `claude plugin eval init` 以访谈方式生成用例和 grader；`init --bare <name>` 生成空模板 |
| 常用参数 | `--runs`、`--model`、`--judge-model`（默认小模型）、`--threshold`、`--max-cost-usd`、`--json`、`--report`、`--mocks`（MCP mock）、`--allow-tools` |
| 成本 | ≈ 用例数 × runs × 2 臂次 agent 运行，外加每个 `llm` / `baseline` grader 每次 3 次评审调用；计入订阅用量或 API 账单 |
| 报告 | 终端汇总表 + `evals/results/<时间戳>/report.html` 与 `aggregate-result.json` |
| 依赖 | Claude Code ≥ 2.1.269；git ≥ 2.31（如装了 git） |

**6 种 grader**（不支持自定义代码 grader）：

| 类型 | 是否花钱 | 通过条件 |
|---|---|---|
| `regex` | 免费 | 正则命中 `last_message` / `trace` / `files` / 指定文件内容；可要求不包含或恰好 N 次 |
| `tool_used` | 免费 | 某工具被调用次数在 `[min, max]` 内，可用 `input_match` 匹配入参 |
| `tool_order` | 免费 | 某工具的首次调用早于另一工具 |
| `file_exists` | 免费 | 运行中**新建**了匹配 glob 的文件 |
| `llm` | 花钱 | 评审模型按 rubric 三票两胜 |
| `baseline` | 花钱 | 评审模型认为本次不差于参考 transcript |

**对你的限制**：

- 隔离沙箱里"个人和项目级配置都不加载"：用户设置、hooks、CLAUDE.md、MCP、其它插件、memory、个人 skills 都不在 📄。所以它能测插件，**不能直接测你的用户级 CLAUDE.md**。
- 只有 `SKILL.md` 的个人 skill 需要先包成插件目录 🔬。
- 评测已安装的第三方插件时，用例从插件安装副本的 eval 目录读取；多数插件没带用例，可以把插件复制到本地目录再加用例 ⚠️。
- 想借它测 CLAUDE.md，有两条未实测的思路 ⚠️：
  - 做两套用例，一套在 `append_system_prompt` 里放入 CLAUDE.md 内容，都用 `--ablation none` 跑，手工比分；
  - 把 CLAUDE.md 包成一个用 SessionStart hook 注入内容的插件，直接得到 Δ。

### 3.2 skill-creator 插件 📄

来源：[Skills 文档](https://code.claude.com/docs/en/skills)、[插件源码](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator)、本机 `SKILL.md`。

- 安装：`/plugin install skill-creator@claude-plugins-official`，然后对 Claude 说 "evaluate my xxx skill with skill-creator"。
- 能力：
  - `evals/evals.json` 存用例；
  - 并行跑 with-skill 与 baseline（新 skill 对比"无 skill"，改进旧 skill 对比旧版快照）；
  - grader / comparator / analyzer 三个子 agent；
  - `aggregate_benchmark` 输出通过率、耗时、token 的 mean ± stddev 与 delta；
  - HTML eval viewer 供人工复核；
  - 两个版本盲评 A/B；
  - description 触发率优化：20 条应触发 / 不应触发的查询，60/40 划分训练 / 测试集，每条跑 3 次，最多迭代 5 轮。
- 与 `claude plugin eval` 的分工：
  - skill-creator 在对话内迭代单个 skill；
  - `claude plugin eval` 是 CLI，适合回归和 CI；
  - 两者用例格式互不通用 📄。
- 注意：它生成的 skill 同样需要评测。SkillsBench 发现模型自己生成的 skill 平均没有收益（v1），部分配置甚至低于无 skill 基线（v4 正文，子代理检索）📄。

### 3.3 自建 A/B 的 CLI 积木

| 实验臂 | 构造方式 | 状态 |
|---|---|---|
| 基线（无任何定制） | `--safe-mode` | 🔬 已验证：CLAUDE.md、个人/插件 skills、agents、MCP 全部不加载 |
| 全量定制 | 不加任何开关 | 🔬 |
| 只加 CLAUDE.md（近似） | `--safe-mode --append-system-prompt-file ~/.claude/CLAUDE.md` | 🔬 机制可用；⚠️ 注入位置与真实 CLAUDE.md 不同 |
| 只加某一个插件 | 用 `claude plugin eval`；`--bare --plugin-dir` 按 help 支持，但 `--bare` 只认 `ANTHROPIC_API_KEY` 或 `--settings` 里的 `apiKeyHelper`（不读订阅登录） | 🔬 `--safe-mode --plugin-dir` 不生效；`--bare` ⚠️ 未实测 |
| 全量去掉 skills | `--disable-slash-commands`（help："Disable all skills"） | ⚠️ 未实测 |

可用的输出数据：

- `--output-format json` 🔬 的字段：`result`、`is_error`、`num_turns`、`duration_ms`、`duration_api_ms`、`total_cost_usd`、`usage`（input / cache 写 / cache 读 / output token）、`modelUsage`、`permission_denials`、`subagent_stats` 等。
- `--output-format stream-json --verbose` 🔬：
  - 首条 `init` 事件列出本次加载的 skills、agents、MCP、tools，可用来确认实验臂配置正确；
  - 之后逐条记录 `tool_use`，其中 `Skill` 调用的 `input.skill` 可以直接算触发率。
- 其它有用开关：
  - `--model` 固定模型；
  - `--max-budget-usd` 单次成本上限；
  - `--no-session-persistence` 不污染会话历史；
  - `-w` 在 worktree 中运行。

附录 A 是一个按上述积木写好、本机跑通的三臂 A/B 脚本。

### 3.4 观测类（看趋势，不做对照）📄

| 工具 | 回答什么问题 | 来源 |
|---|---|---|
| `claude plugin details <name>` | 插件常驻 / 按需加载各花多少 token | [plugins/measure](https://code.claude.com/docs/en/plugins/measure) |
| `/skill-doctor` | 每个 skill 的成本与调用频率，标出"在列表里但从未被调用"的 skill | 同上 |
| `/doctor` | 找出未使用的 skills / MCP / plugins 及其上下文成本、慢 hooks | [commands](https://code.claude.com/docs/en/commands) |
| `/usage`（别名 `/cost`）、`/context`、`/insights` | 用量占比；上下文网格；最近会话的 HTML 分析报告 | 同上 |
| OpenTelemetry | 见下 | [monitoring-usage](https://code.claude.com/docs/en/monitoring-usage) |

OpenTelemetry 的用法：

- 开启：`CLAUDE_CODE_ENABLE_TELEMETRY=1`。
- 指标：`claude_code.cost.usage`、`token.usage`、`session.count`、`lines_of_code.count`、`commit.count`、`pull_request.count`、`active_time.total` 等。
- 事件：`user_prompt`、`tool_result`、`tool_decision`、`api_request` 等。
- 成本和 token 指标带 `skill.name` / `plugin.name` / `agent.name` 属性；第三方插件名默认脱敏，设 `OTEL_LOG_TOOL_DETAILS=1` 才会显示。

观测数据受每天任务组成变化的干扰，只能说明趋势（例如定制前后单会话成本、每活跃小时的提交数），不能据此下因果结论。

---

## 4. 第三方框架

先说结论：第三方工具里，能把 Claude Code（或 Claude Agent SDK）**整体当被测系统、原生跑 baseline vs treatment** 的只有 promptfoo、Harbor、Inspect AI + inspect_swe 三个。Braintrust、LangSmith、Langfuse 这类观测平台对 Claude Code 主要是采集数据；要做 A/B，得自己写 task 函数去调 Agent SDK。

以下版本号取自 GitHub Releases / PyPI / npm（2026-09-28，子代理检索）。

### 4.1 能原生做对照实验的

| 工具 | 被测对象 | 怎么做 A/B | Grader | 重复试验 | 隔离 | 许可 / 状态 |
|---|---|---|---|---|---|---|
| **promptfoo** | Claude Agent SDK（provider `anthropic:claude-agent-sdk`，别名 `anthropic:claude-code`）📄 | 同一批用例配两个带 label 的 provider，结果并排展示 | 规则、JS / Python、`llm-rubric`、`skill-used` / `not-skill-used`、轨迹类（tool-used / tool-sequence 等）、cost、latency | `--repeat N`（调试时加 `--no-cache`） | 工作目录（写文件的任务需每次一次性工作区） | MIT；2026-03-09 宣布加入 OpenAI，声明继续开源 📄；v0.123.1 |
| **Harbor** | 容器里的 Claude Code CLI（内置 `claude-code` agent）📄 | 两套配置分成两个 job 各跑一次（统计按 agent + 模型 + 数据集聚合，同一个 job 里的两套配置会被合并，据源码推断） | 任务自带 `tests/` 写 reward，另有 rewardkit、LLM judge | `-k` 每题重复，自动算 pass@k | Docker 及 Daytona / Modal 等云沙箱 | Apache-2.0；v0.23.0；Terminal-Bench 官方执行框架 |
| **Inspect AI + inspect_swe** | 沙箱里的 Claude Code（`claude_code()` agent，模型调用经代理回到 Inspect，可换任意模型）📄 | 建两个 Task，或用 `--solver` / `-S` 覆盖参数；日志可汇总成 dataframe 对比 | 内置 match / includes / 模型评分，也可写进沙箱跑测试的自定义 scorer | `--epochs N` + reducer（`pass_at_k` 等），带标准误 | Docker / k8s / 云沙箱 | MIT；UK AISI + Meridian Labs；inspect-ai 0.3.271、inspect_swe 0.2.71 |

**promptfoo 要点**（与你学习蓝图 P1 的 promptfoo 路线重合，学一次两处用）：

- **默认不加载任何定制**："By default … does not look for settings files, CLAUDE.md, or slash commands." 📄
  - 要用 `setting_sources: ['project', 'local']` 等方式显式开启；
  - skill 用 `skills: 'all'` 或名单开启；
  - 插件目前只支持 `local` 类型。
- **工具权限**：不设 `working_dir` 时在临时目录运行且没有工具；设了之后默认只有 `Read` / `Grep` / `Glob` / `LS` 只读工具 📄。两个臂的工具权限必须一致，否则比的就不是定制本身。
- **推荐流程**：官方"Test agent skills"指南用两个 provider 分别指向 v1 / v2 两个 fixture 目录比较 skill 版本 📄：
  - 断言分三层：`skill-used`（路由对不对）→ 输出质量 → 成本 / 时延；
  - 用 `--repeat 3` 采样，`--no-cache` 防止回放旧结果。
- **注意**：`setting_sources: ['user']` 会读本机真实的 `~/.claude`，实验不可复现。建议把待测的定制放到项目级目录或包成插件。
- **没有 API key 也能用**：provider 配置里设 `apiKeyRequired: false`，promptfoo 就会跳过 API key 预检，由本机 Claude Code 用订阅登录自行鉴权。这是官方文档"Local Claude Code Session (No API Key)"一节的写法 📄。本机 Max 订阅已跑通，完整步骤见附录 B 🔬。
- 两臂配置：
  - `setting_sources: []` 对比 `[user]` 🔬 已实测（附录 B）；
  - 本地插件臂 `plugins: [{ type: local, path: ./my-plugin }]` ⚠️ 未实测。

**Harbor 要点**：

- 用法示例：`harbor run -t <task> -a claude-code -m anthropic/claude-sonnet-5`。
- 定制注入方式：
  - skills、MCP 可按任务或 agent 注入；
  - 原生 settings 用 `--ak` 传；
  - CLAUDE.md 没有专门参数，要放进任务的 environment 目录 📄。
- `claude-code` agent 在容器里默认以 `bypassPermissions` 运行（子代理读源码）。这依赖容器隔离，不要照搬到本机。
- 自带 Terminal-Bench、SWE-bench 等 85 个基准适配器。想拿公开基准验证定制时，它最省事。

### 4.2 观测 / 实验平台（主要负责采集数据）

| 平台 | 接 Claude Code 会话 | 接 Agent SDK | 实验对比 | 开源 / 自托管 |
|---|---|---|---|---|
| Braintrust | 插件（hooks 转发） | `wrapClaudeAgentSDK` | `Eval()`、baseline 对比、回归标红 | SDK 开源，平台闭源；自托管限 Enterprise |
| LangSmith | 插件（Stop hook） | `configure_claude_agent_sdk` | experiment 对比、pairwise | SDK MIT；自托管为 Enterprise 附加项 |
| Langfuse | 插件（Stop hook 读 transcript） | OpenInference（OTel） | `run_experiment` + 对比视图 | MIT（`ee` 目录除外），可免费自托管；2026-01 被 ClickHouse 收购 |
| Arize Phoenix | coding-harness-tracing 插件 | OpenInference | experiments（支持 repetitions） | ELv2，可自托管 |
| W&B Weave | weave-claude-code 插件（OTel） | `weave.init` 自动 patch | Evaluation + Leaderboard（trials） | SDK Apache-2.0；自托管需 Self-Managed |
| DeepEval | 无原生集成 | 无专门集成 | pytest 式；ArenaGEval 盲测两两比较 | Apache-2.0 |

以上各行由子代理检索，来源见第 9 节。这类平台的价值：

- 给真实会话留痕，事后复盘；
- 提供现成的实验对比 UI。

被测的 task 函数（按配置启动 Agent SDK、隔离工作区）要自己写。现成参考实现是 [langchain-ai/skills-benchmarks](https://github.com/langchain-ai/skills-benchmarks)：

- 在 Docker 里无头跑 Claude Code；
- CONTROL（无 skill）对比 ALL_MAIN_SKILLS；
- `pytest --count` 重复运行，结果写入 LangSmith experiment。

### 4.3 用量 / 成本分析

- **ccusage**（MIT，v20.0.26）：
  - 读取 `~/.claude/projects` 下的会话日志，出日 / 月 / 会话报表；
  - 只能事后统计，要对比 A/B 得让两组跑在不同项目目录。
- **Claude Code 原生 OTel**：
  - `OTEL_METRICS_EXPORTER=prometheus` 可直接暴露给 Prometheus；
  - `OTEL_RESOURCE_ATTRIBUTES` 可以给实验组打标签（子代理检索）；
  - 社区有现成 Grafana 面板（ID 25255）。

### 4.4 专门评测 skill / CLAUDE.md 的社区项目

以下由子代理按 GitHub API 检索，stars 为数量级：

| 项目 | 做什么 | 状态 |
|---|---|---|
| [vercel-labs/agent-eval](https://github.com/vercel-labs/agent-eval) | 对比文档、MCP、模型等配置的实验框架，支持 Claude Code 和 Codex | ~260★，活跃 |
| [NVIDIA/SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator) | ACES 论文实现，有 / 无 skill 配对运行 | ~520★，活跃 |
| [benchflow-ai/skillsbench](https://github.com/benchflow-ai/skillsbench) | SkillsBench 基准本体（基于 Harbor） | ~1.8k★ |
| [npezarro/claude-bakeoff](https://github.com/npezarro/claude-bakeoff) | 两份 CLAUDE.md 做 A/B，用 LLM 评审 | 个人项目 |
| wshobson/agents 中的 PluginEval | 不跑真实 agent 会话，任何非空回复都算"激活" | 不适合测触发率 |
| skill-bench/skill-eval-action | 评测 skill 的 GitHub Action | 3 个月无提交，维护放缓 |

### 4.5 怎么选

| 你的情况 | 选 |
|---|---|
| 测插件或单个 skill | 官方 `claude plugin eval` / skill-creator，不需要第三方 |
| 测 CLAUDE.md 或整套配置，想要现成的用例管理、并排对比 UI | promptfoo（且与学习蓝图 P1 重合） |
| 想要最少依赖、完全掌控 | 附录 A 的脚本 |
| 需要容器隔离、大规模并行或公开基准（Terminal-Bench / SWE-bench） | Harbor |
| 需要严格统计（epochs、标准误）或换非 Anthropic 模型对照 | Inspect AI + inspect_swe |
| 已经在用某个观测平台 | 用它的 experiment 功能 + 自写 task，或只拿来给真实会话留痕 |

---

## 5. 实证：定制到底有没有用

| 研究 | 设计 | 关键结果 | 对你的启示 |
|---|---|---|---|
| Vercel，[AGENTS.md outperforms skills in our agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)（2026-01-27）📄 | Next.js 16 新 API 任务；Build / Lint / Test 判分；模型与试验次数未披露 | 基线 53%；默认 skill 53%（**56% 用例未触发**）；显式指令调 skill 79%；AGENTS.md 内嵌压缩文档索引 100% | 触发是第一道坎，要单独测；被动常驻的精简信息可能比按需 skill 更稳 |
| ETH Zurich 等，[Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988)（v2 2026-06-23）📄 | SWE-bench Lite 等任务集；Claude Code / Codex / Qwen Code；无文件 vs LLM 生成 vs 开发者手写 | 上下文文件"总体不提升成功率"，推理成本 +20% 以上；文件里的指令会被遵守，但仓库概览没帮助 | CLAUDE.md 只写非标准、必须遵守的约束；少写"项目介绍" |
| [SkillsBench](https://arxiv.org/abs/2602.12670)（v4 2026-06-14）📄 | 87 任务 × 8 领域 × 18 个"模型 + harness"组合，有 / 无 skill 配对 | 精选 skill 使通过率 33.9% → 50.5%（+16.6pp），各组合 +4.1 ~ +25.7pp；部分任务变差；自生成 skill 无收益（子代理检索正文） | skill 有真实收益但因任务而异，必须逐个测；不要默认"让 Claude 写的 skill 就有用" |
| OpenAI，[Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills)（2026-01-22，子代理检索） | 方法文，无对照数字 | 每个 skill 10–20 条 prompt（含 `should_trigger` 列和负例），先用 JSONL 事件做确定性检查，再用 rubric 结构化打分 | 与 `claude plugin eval` 的设计思路一致，可直接借鉴用例设计 |
| LangChain，[Evaluating Skills](https://www.langchain.com/blog/evaluating-skills)（2026-03-05，子代理检索） | Docker 干净环境；完成率、触发率、轮数 | Claude Code 有 / 无 skill 完成率 82% / 9%；把 skill 使用指引写进 CLAUDE.md 后触发更稳定；相似 skill 约 20 个时易选错 | skill 越多越容易选错；你当前可用 skill 有 164 个 🔬 |

另有几篇 2026 年论文（arXiv 2601.20404、2607.27250、NVIDIA ACES 2608.20614、2608.14036）结论方向不完全一致，由子代理检索，未逐条复核，只作线索：

- 有研究报告 AGENTS.md 能降低时延和 token；
- 有研究发现上下文文件对正确率无可测影响；
- skill 池从 5 个扩到 100 个时，检索正确率大幅下降。

---

## 6. 方法论与常见坑

| 主题 | 要点 | 来源 |
|---|---|---|
| 非确定性 | 单次运行几乎没有信息量；pass@k 表示 k 次里至少一次成功，pass^k 表示 k 次全部成功，衡量"稳定变好"要看 pass^k | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)（2026-01-09）📄 |
| 起步规模 | 20–50 个取自真实失败的简单任务就是好开端；能力型评测起步通过率低，回归型评测应接近 100% | 同上 📄 |
| 结果 vs 过程 | 按产出评分而不是按路径评分，以免测试过脆；但要读大量 transcript 校验 grader 本身 | 同上 📄 |
| 每用例两类 grader | 一个评结果（最终回复或文件），一个评过程（`tool_used` / `tool_order`），分别回答"对不对"和"是不是定制导致的" | [plugin-evals](https://code.claude.com/docs/en/plugin-evals) 📄 |
| LLM 评审的稳定性 | 要读的文本越长越不稳定：长输出用 `regex`，`llm` 只用于短输出，rubric 写成具体的 PASS / FAIL 条件；Δ 为负时先怀疑评审模型（可换 `--judge-model sonnet`） | 同上 📄 |
| 隔离 | 每次试验从干净环境开始，避免上一轮残留影响下一轮 | Demystifying evals 📄 |
| 噪声底线 | 仅资源配置不同就让 Terminal-Bench 2.0 分数相差 6pp；小于 3pp 的差异在配置未对齐前应存疑 | [Infrastructure noise](https://www.anthropic.com/engineering/infrastructure-noise)（2026-02-05）📄 |
| 统计 | 同题多次采样、做配对差分、报标准误；小样本只能排除大效应 | [A statistical approach to model evals](https://www.anthropic.com/research/statistical-approach-to-model-evals)（2024-11，子代理检索） |
| 模型漂移 | 固定 `--model`，否则会把模型升级误判为定制效果；增强能力型的 skill 可能随模型升级变得多余，模型更新后要重跑 | plugin-evals 📄；[skill-creator 博客](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)（子代理检索） |
| 多模型 | skill 效果依赖底层模型，要在计划使用的 Haiku / Sonnet / Opus 上分别测 | [Skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) 📄 |
| 先评测后写 | 先在无 skill 时跑代表性任务、记下失败，再写最少的指令去修复，并与基线比较 | 同上 📄 |
| 成本口径 | 缓存会让同样的调用成本差数倍；比较 token 或多次均值 | 本机实测 🔬 |

---

## 7. 给你的落地方案

按投入从小到大：

| 步骤 | 做什么 | 工具 | 产出 |
|---|---|---|---|
| 0 | 升级到 ≥ 2.1.269，确认 git ≥ 2.31 | `claude update` | 可以用 `claude plugin eval` |
| 1 | 零成本体检：找出从未触发、常驻成本高的定制，先砍或停用 | `/skill-doctor`、`/doctor`、`claude plugin details` | 定制清单与其常驻成本 |
| 2 | 建任务集：从自己真实会话里挑 20 个任务，分三类——定制应当起作用的、定制不该影响的（回归题）、skill 应触发 / 不应触发的正负例 | 手工整理 | `tasks/*/prompt.md` + fixture |
| 3 | 为每题写 grader：结果 + 过程 + 规则（见下表） | regex / tool_order / 脚本 | `grade.py` 或 `graders/*.md` |
| 4a | 插件、单个 skill：看 Δ 和触发率 | `claude plugin eval`、skill-creator | `report.html` / `benchmark.json` |
| 4b | CLAUDE.md、整套配置：三臂 A/B（base / claudemd / full），每臂 ≥ 3 次，固定模型 | 附录 A 脚本，或 promptfoo | 每臂得分、Δ、pass^k、token |
| 5 | 决策：Δ 不显著但成本上升的定制就精简或删除；保留下来的用例留作回归集，模型升级后重跑 | — | 精简后的配置 + 回归集 |

**把你的 CLAUDE.md 规则翻译成可自动判定的 grader**（示例）：

| CLAUDE.md 规则 | grader |
|---|---|
| 默认用中文回复 | 用英文提问，`regex` 检查最终回复含中文字符 |
| 动手前先读 `ARCHITECTURE.md` | `tool_order`：`Read`（入参匹配 ARCHITECTURE）早于首个 `Edit` / `Write` |
| 用法变动同步 `README.md` | `regex` 检查 README 文件内容包含新配置项 |
| 交付前自己验证 | `tool_used`：`Bash`，入参匹配 `pytest` / `npm test` |
| 设计阶段落 spec | `file_exists`：`docs/specs/*.md` |
| 不捏造事实 | 难以自动判定：`llm` rubric 加人工抽查 |

---

## 8. 未核实 / 待跟进

- `/skill-doctor` 是会话内命令，本次没有实际运行，输出字段以官方文档描述为准。
- 借 `claude plugin eval` 测 CLAUDE.md 的两条思路（`append_system_prompt`、SessionStart hook 插件）未实测。
- `--bare --plugin-dir`、`--disable-slash-commands` 两种实验臂未实测。
- 以下内容由子代理检索、我未逐条复核：
  - 第 5 节标注"子代理检索"的数字；
  - 第 5 节末尾列出的几篇论文。
- 第 4 节的版本号、许可、收购信息、观测平台表格和社区项目表格由子代理检索，均附一手来源。我亲自复核过的只有：
  - promptfoo 的 provider 文档、skills 指南和加入 OpenAI 的公告；
  - Harbor 的预集成 agent 文档；
  - inspect_swe 的 `claude_code()` 文档。
- 以下两点是子代理读源码得出的推断，未实测：
  - Harbor "同一 job 内两套配置会被合并统计"；
  - `claude-code` agent 默认 `bypassPermissions`。
- promptfoo 的本地插件臂（`plugins` 配置）和写文件类任务的一次性工作区方案未实测。无 API key 冒烟、`setting_sources` 两臂 A/B、`skills: all` + `skill-used` 已实测，见附录 B。
- 本机 A/B 实测只有单次、haiku 模型，仅验证链路可用，不代表你的定制在真实任务上的效果。

---

## 9. 来源

官方（Anthropic / Claude Code）：

- Test plugins with evals：https://code.claude.com/docs/en/plugin-evals
- Week 37 更新说明（v2.1.263 → v2.1.269）：https://code.claude.com/docs/en/whats-new/2026-w37
- Skills（评测章节、skill-creator）：https://code.claude.com/docs/en/skills
- Measure plugin cost and usage：https://code.claude.com/docs/en/plugins/measure
- Plugin loading（`@skills-dir` 定义）：https://code.claude.com/docs/en/plugins/loading
- Commands：https://code.claude.com/docs/en/commands
- Monitoring（OpenTelemetry）：https://code.claude.com/docs/en/monitoring-usage
- skill-creator 插件：https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator
- Skill authoring best practices：https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Demystifying evals for AI agents（2026-01-09）：https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Quantifying infrastructure noise in agentic coding evals（2026-02-05）：https://www.anthropic.com/engineering/infrastructure-noise

研究与案例：

- Vercel（2026-01-27）：https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
- Evaluating AGENTS.md（arXiv 2602.11988）：https://arxiv.org/abs/2602.11988
- SkillsBench（arXiv 2602.12670）：https://arxiv.org/abs/2602.12670
- OpenAI eval-skills：https://developers.openai.com/blog/eval-skills
- LangChain Evaluating Skills：https://www.langchain.com/blog/evaluating-skills
- Improving skill-creator（Anthropic 博客）：https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills
- A statistical approach to model evals：https://www.anthropic.com/research/statistical-approach-to-model-evals

第三方框架：

- promptfoo：
  - Claude Agent SDK provider：https://www.promptfoo.dev/docs/providers/claude-agent-sdk/
  - Test agent skills 指南：https://www.promptfoo.dev/docs/guides/test-agent-skills/
  - 加入 OpenAI（2026-03-09）：https://www.promptfoo.dev/blog/promptfoo-joining-openai/
  - Releases：https://github.com/promptfoo/promptfoo/releases
- Harbor：
  - 仓库：https://github.com/harbor-framework/harbor
  - 预集成 agents：https://docs.harborframework.com/core-concepts/agents/pre-integrated-agents
  - Terminal-Bench：https://www.tbench.ai/news
- Inspect AI：https://inspect.aisi.org.uk/ ；inspect_swe `claude_code()`：https://meridianlabs-ai.github.io/inspect_swe/claude_code.html
- 观测平台：
  - Braintrust：https://www.braintrust.dev/docs/integrations/claude-agent-sdk
  - LangSmith：https://docs.langchain.com/langsmith/trace-claude-code
  - Langfuse：https://langfuse.com/integrations/developer-tools/claude-code
  - Langfuse 被 ClickHouse 收购：https://clickhouse.com/blog/clickhouse-acquires-langfuse-open-source-llm-observability
  - Phoenix：https://arize.com/docs/phoenix/integrations/coding-agents/claude-code
  - Weave：https://github.com/wandb/weave-claude-code
  - DeepEval：https://github.com/confident-ai/deepeval
- LangChain skills-benchmarks：https://github.com/langchain-ai/skills-benchmarks
- 用量分析：
  - ccusage：https://github.com/ryoppippi/ccusage
  - Grafana 面板 25255：https://grafana.com/grafana/dashboards/25255-claude-code-metrics-prometheus/

本机实测：Claude Code 2.1.259 的 `--help`、`claude plugin details`、`claude -p` 的 json / stream-json 输出（2026-09-28）。

---

## 附录 A：三臂 A/B 脚本（本机跑通）

用于评测 CLAUDE.md / 整套配置这类官方 eval 覆盖不到的定制。三个臂：`base`（`--safe-mode`）、`claudemd`（safe-mode + 追加 CLAUDE.md）、`full`（全部定制）。

目录约定：

```text
harness/
├── ab.sh               # 跑实验：每个臂 × RUNS 次，每次在全新临时目录里执行
├── trace_metrics.py    # 从 stream-json trace 提取通用指标（工具调用序列、skill 调用、token、成本）
├── summarize.py        # 汇总：每臂得分、Δ（相对 base）、pass^k、token、成本、逐项检查通过数
└── tasks/<task>/
    ├── prompt.md       # 任务原文（不要提你的规则，才能测出规则是否生效）
    ├── fixture/        # 初始工作区
    └── grade.py        # 判分：输出一行 JSON {checks, score, ...}
```

`ab.sh`：

```bash
#!/usr/bin/env bash
# 用法：RUNS=3 MODEL=sonnet ./ab.sh tasks/<task>
# 任务目录：prompt.md（任务）、fixture/（初始工作区）、grade.py（判分，输出一行 JSON）
set -eo pipefail
TASK=$(cd "$1" && pwd); ROOT=$(pwd); RUNS=${RUNS:-3}; MODEL=${MODEL:-sonnet}
for ARM in base claudemd full; do
  case $ARM in
    base)     FLAGS=(--safe-mode) ;;                                                          # 无任何定制
    claudemd) FLAGS=(--safe-mode --append-system-prompt-file "$HOME/.claude/CLAUDE.md") ;;    # 只加 CLAUDE.md（近似）
    full)     FLAGS=() ;;                                                                     # 全部定制
  esac
  for i in $(seq "$RUNS"); do
    WS=$(mktemp -d) && cp -R "$TASK/fixture/." "$WS/"
    OUT="$ROOT/results/$(basename "$TASK")/$ARM-$i" && mkdir -p "$OUT"
    (cd "$WS" && claude -p "$(cat "$TASK/prompt.md")" ${FLAGS[@]+"${FLAGS[@]}"} \
       --model "$MODEL" --permission-mode acceptEdits \
       --output-format stream-json --verbose --no-session-persistence \
       --max-budget-usd 2 < /dev/null > "$OUT/trace.jsonl") || echo "run failed: $ARM-$i" >&2
    python3 "$TASK/grade.py" "$WS" "$OUT/trace.jsonl" > "$OUT/grade.json"
  done
done
python3 "$ROOT/summarize.py" "$ROOT/results/$(basename "$TASK")"
```

说明：

- `${FLAGS[@]+"${FLAGS[@]}"}` 的写法是为了兼容 macOS 自带的 bash 3.2：空数组直接展开会报错。
- `acceptEdits` 只放行文件编辑。任务需要跑命令时，另加 `--allowed-tools "Bash(pytest *)"` 这类精确授权，不建议在本机用 `bypassPermissions`。

`trace_metrics.py`：

```python
"""从 claude -p --output-format stream-json 的 trace 中提取通用指标。"""
import json


def metrics(trace_path):
    m = {"tool_calls": [], "skills": [], "result": None, "cost_usd": None,
         "turns": None, "tokens_in": 0, "tokens_out": 0}
    for line in open(trace_path, encoding="utf-8"):
        if not line.strip():
            continue
        ev = json.loads(line)
        if ev.get("type") == "assistant":
            for c in ev["message"].get("content", []):
                if c.get("type") == "tool_use":
                    m["tool_calls"].append((c["name"], c.get("input", {})))
                    if c["name"] == "Skill":
                        m["skills"].append(c.get("input", {}).get("skill"))
        elif ev.get("type") == "result":
            u = ev.get("usage", {})
            m.update(result=ev.get("result"), cost_usd=ev.get("total_cost_usd"),
                     turns=ev.get("num_turns"),
                     tokens_in=sum(u.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")),
                     tokens_out=u.get("output_tokens") or 0)
    return m
```

`summarize.py`：

```python
"""汇总 results/<task>/<arm>-<i>/grade.json：每个臂的平均分、pass^k、token 与成本。"""
import json, pathlib, statistics, sys
from collections import defaultdict

rows = defaultdict(list)
for g in sorted(pathlib.Path(sys.argv[1]).glob("*/grade.json")):
    rows[g.parent.name.rsplit("-", 1)[0]].append(json.loads(g.read_text()))
base = statistics.mean(r["score"] for r in rows["base"]) if rows.get("base") else None
print(f"{'arm':<10}{'runs':>5}{'score':>8}{'Δ':>8}{'pass^k':>8}{'tok_in':>9}{'cost$':>8}")
for arm, rs in rows.items():
    s = statistics.mean(r["score"] for r in rs)
    delta = f"{s - base:+.2f}" if base is not None else "-"
    passk = all(r["score"] == 1 for r in rs)
    tok = statistics.mean(r["tokens_in"] for r in rs)
    cost = statistics.mean(r["cost_usd"] or 0 for r in rs)
    print(f"{arm:<10}{len(rs):>5}{s:>8.2f}{delta:>8}{str(passk):>8}{tok:>9.0f}{cost:>8.3f}")
    for k in rs[0]["checks"]:
        print(f"  - {k}: {sum(r['checks'][k] for r in rs)}/{len(rs)}")
```

示例任务 `tasks/add-config/`：

- fixture 是一个小项目：`README.md` 里有配置表，`ARCHITECTURE.md` 说明配置集中在 `config.py`，另有 `config.py` 和 `main.py`。
- `prompt.md` 故意用英文、不提任何规则：

  ```text
  Add a new config option LOG_LEVEL (default "info", read from the environment) to this project. Put it in config.py.
  ```

`grade.py`：1 条结果检查 + 3 条 CLAUDE.md 规则检查。

```python
"""add-config 任务判分：1 条结果检查 + 3 条 CLAUDE.md 规则检查。"""
import json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from trace_metrics import metrics

ws, m = pathlib.Path(sys.argv[1]), metrics(sys.argv[2])
calls = m["tool_calls"]
first_edit = next((i for i, (n, _) in enumerate(calls) if n in ("Edit", "Write")), len(calls))
checks = {
    "impl": "LOG_LEVEL" in (ws / "config.py").read_text(),               # 结果：功能实现
    "readme_synced": "LOG_LEVEL" in (ws / "README.md").read_text(),      # 规则：用法变动同步 README
    "arch_read_first": any(n == "Read" and "ARCHITECTURE" in json.dumps(i)  # 规则：动手前先读 ARCHITECTURE.md
                           for n, i in calls[:first_edit]),
    "reply_zh": bool(re.search(r"[一-鿿]", m["result"] or "")),   # 规则：默认中文回复
}
print(json.dumps({"checks": checks, "score": sum(checks.values()) / len(checks),
                  **{k: m[k] for k in ("tokens_in", "tokens_out", "cost_usd", "turns", "skills")}},
                 ensure_ascii=False))
```

**本机跑通结果**（`RUNS=1 MODEL=haiku`，只为验证链路，n=1 不能下结论）🔬：

| 臂 | 得分 | 功能实现 | 同步 README | 先读 ARCHITECTURE | 中文回复 | 输入侧 token |
|---|---|---|---|---|---|---|
| base | 0.25 | ✅ | ❌ | ❌ | ❌ | 130,938 |
| claudemd | 0.25 | ✅ | ❌ | ❌ | ❌ | 133,754 |
| full | 0.50 | ✅ | ❌ | ❌ | ✅ | 180,504 |

从这次运行能看到三点：

1. 链路可用：三个臂配置正确，`init` 事件显示的 skills / agents / MCP 数量符合预期，trace、判分、汇总都正常。
2. "同步 README""先读 ARCHITECTURE" 两条规则，两个带 CLAUDE.md 的臂都没遵守。
3. 追加到 system prompt 的 `claudemd` 臂没用中文回复，真实注入的 `full` 臂用了。这可能是注入位置不同（第 3.3 节的 ⚠️），也可能只是随机性。

要回答"定制是否有用"，至少需要：

- 用你真实常用的模型——你的 `~/.claude/settings.json` 默认模型是 `haiku`；
- `RUNS ≥ 3`；
- 20 个左右的任务。

---

## 附录 B：promptfoo + Claude Code，无 API key 上手（本机跑通）

实测环境（2026-09-28）：

- promptfoo 0.123.1（全局安装）；
- Node v25.2.1；
- `claude auth status` 显示 `"authMethod": "claude.ai"`、`"subscriptionType": "max"`；
- 未设置 `ANTHROPIC_API_KEY`。

### B.1 原理

调用链：`promptfoo` → provider `anthropic:claude-agent-sdk` → Claude Agent SDK → 启动 Claude Code 二进制 → Claude Code 用你的订阅登录鉴权。

promptfoo 默认要求 API key：没有 key、且未设 `apiKeyRequired: false` 时会直接报错 "Anthropic API key is not set"（[provider 源码](https://github.com/promptfoo/promptfoo/blob/main/src/providers/claude-agent-sdk.ts)）。官方文档"Local Claude Code Session (No API Key)"一节给出的做法就是设 `apiKeyRequired: false`，原话是 "the SDK still needs to be able to authenticate on its own"（[文档](https://www.promptfoo.dev/docs/providers/claude-agent-sdk/)）。

### B.2 安装与冒烟测试

1. 确认没有设置 `ANTHROPIC_API_KEY`。官方说明：同时存在订阅登录和 API key 时，Claude Code 会优先使用 key（[Authentication](https://code.claude.com/docs/en/authentication)）。
2. 建评测目录并安装 SDK。provider 从配置文件所在目录（或当前目录）解析 `@anthropic-ai/claude-agent-sdk`，不会使用 promptfoo 自带的那一份，所以要在评测目录里装一份：

   ```bash
   mkdir -p ~/cc-evals && cd ~/cc-evals
   npm init -y
   npm install @anthropic-ai/claude-agent-sdk
   ```

   下载量（0.3.283）：SDK 本体约 5 MB，加上 macOS 原生二进制包 `@anthropic-ai/claude-agent-sdk-darwin-arm64` 约 225 MB。

   本机也可以不重复下载（非官方做法，本次验证用的就是它）：全局 promptfoo 自带 SDK 0.3.263，软链过来即可。promptfoo 升级后，这份 SDK 的版本也会随之变化。

   ```bash
   mkdir -p node_modules/@anthropic-ai
   ln -s /opt/homebrew/lib/node_modules/promptfoo/node_modules/@anthropic-ai/claude-agent-sdk node_modules/@anthropic-ai/claude-agent-sdk
   ```

3. 写 `promptfooconfig.yaml`：

   ```yaml
   description: claude-code-subscription-smoke
   prompts:
     - 'What is 1+1? Answer in one short sentence.'
   providers:
     - id: anthropic:claude-agent-sdk
       config:
         apiKeyRequired: false   # 跳过 API key 预检，由 Claude Code 用订阅登录鉴权
         model: haiku
         max_turns: 1
   tests:
     - assert:
         - type: contains
           value: '2'
   ```

4. 运行并查看：`promptfoo eval --no-cache`，然后 `promptfoo view` 打开网页对比。

实测结果：

- PASS，输出 `1+1 equals 2.`，约 6.8k token；
- 返回的 metadata 含 `skillCalls`、`toolCalls`、`numTurns`、`durationMs`、`modelUsage`、`permissionDenials`，可直接用于断言。

### B.3 A/B：无定制 vs 用户级定制 🔬

`ab.yaml`：

```yaml
description: claude-md-ab
prompts:
  - 'What is 1+1? Answer in one short sentence.'   # 故意用英文提问，测 CLAUDE.md 的"默认中文回复"规则
providers:
  - id: anthropic:claude-agent-sdk
    label: baseline
    config: &base
      apiKeyRequired: false
      model: haiku
      max_turns: 1
      setting_sources: []        # 默认值：不读任何 settings / CLAUDE.md
  - id: anthropic:claude-agent-sdk
    label: user-config
    config:
      <<: *base
      setting_sources: [user]    # 读 ~/.claude/settings.json 与 ~/.claude/CLAUDE.md
tests:
  - description: 默认中文回复
    assert:
      - type: javascript
        value: /[一-鿿]/.test(output)
```

运行命令：`promptfoo eval -c ab.yaml --no-cache --repeat 3`

| 臂 | 中文回复 | 输出 | 单次估算成本 |
|---|---|---|---|
| baseline | 0/3 | `1 + 1 = 2.` ×3 | $0.0138 |
| user-config | 2/3 | `1 + 1 = 2.`、`1 加 1 等于 2。`×2 | $0.0160 |

结论：CLAUDE.md 的规则确实生效，但在 haiku 上不稳定（pass@3 通过，pass^3 未通过）。这正说明必须用 `--repeat` 多次采样。

### B.4 评测 skill 是否被触发 🔬

```yaml
providers:
  - id: anthropic:claude-agent-sdk
    config:
      apiKeyRequired: false
      model: haiku
      max_turns: 3
      setting_sources: [user]
      skills: all                # 允许调用发现到的全部 skill；也可以写名单
tests:
  - assert:
      - type: skill-used         # 另有 not-skill-used，用于测"不该触发"的负例
        value: mattpocock-skills:grilling
```

实测：提示"用 grilling 技能质询我的计划……"，`skillCalls` 记录到 `mattpocock-skills:grilling`，断言通过。

### B.5 写文件、跑命令的任务 ⚠️ 未实测

按官方 [Evaluate coding agents](https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/) 指南的思路：

- `working_dir` 指向任务目录；
- `append_allowed_tools: ['Write', 'Edit', 'Bash']`；
- `permission_mode: acceptEdits`；
- 断言组合 `javascript`（检查文件或测试结果）、`llm-rubric`、`cost`。

会写文件的用例每次都要用一次性工作区；或者 `-j 1` 串行执行，每次运行前重置目录，避免多次运行互相污染。

### B.6 注意事项

| 事项 | 说明 |
|---|---|
| 用量 | promptfoo 显示的 cost 是按 API 价目的估算。订阅下不单独计费，但会消耗订阅用量额度（与 `claude plugin eval` 文档的说法一致）。`apiKeyRequired: false` 时 promptfoo 源码会自动跳过缓存，每次都是真实调用 |
| 合规 | 官方写明 Pro / Max 的用量额度"assume ordinary, individual usage of Claude Code and the Agent SDK"。禁止的是第三方开发者在自己的产品里提供 claude.ai 登录、代用户走订阅凭据，或收集、中转凭据（[Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance)）。个人本机评测属于前者；不要把订阅用于替他人跑评测或对外提供服务 |
| CI / 无浏览器环境 | 用 `claude setup-token` 生成一年期 OAuth token，自己设置为环境变量 `CLAUDE_CODE_OAUTH_TOKEN`（不要提交进仓库）。它只能发模型请求；`--bare` 模式不读这个变量 |
| 可复现 | `setting_sources: [user]` 读的是实时的 `~/.claude`，改了配置结果就会变。做回归时，把被测配置快照到项目级 `.claude/`，再用 `setting_sources: [project]` 配合各自的 `working_dir` |
| 隐私 | 可以设 `PROMPTFOO_DISABLE_TELEMETRY=1` 关闭 promptfoo 遥测 |
