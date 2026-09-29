# Claude Code 定制 A/B 评测（promptfoo + Max 订阅）

> 日期：2026-09-28
> 背景调研：[Claude Code 定制效果评测工具调研](../research/2026-09-28-Claude-Code定制效果评测工具调研.md)

## 目标

在仓库里搭一个能直接运行的评测起点，回答"我加的定制（CLAUDE.md、skills、plugins）有没有让 Claude Code 变好"。鉴权走 Claude Max 订阅，不需要 API key。

## 范围

| 做 | 不做（后续） |
|---|---|
| CLAUDE.md 规则遵守的 A/B：中文回复、先读 ARCHITECTURE.md、改用法时同步 README | 写文件 / 跑命令的任务：需要一次性工作区 |
| skill 触发率：显式点名、自然表述两类正例，加一个近似负例 | 插件级评测：交给 `claude plugin eval`，它自带无插件基线 |

## 方案

### 目录

```text
evals/claude-code/
├── package.json            # 锁定 @anthropic-ai/claude-agent-sdk，npm scripts
├── promptfooconfig.yaml    # A/B：baseline vs user-config
├── skill-trigger.yaml      # skill 触发率：只跑 user-config
├── fixtures/demo-project/  # 被测任务用的小项目（README、ARCHITECTURE、config.py、main.py）
└── .gitignore              # node_modules/、results/
```

### 实验臂

| 臂 | `setting_sources` | 含义 |
|---|---|---|
| baseline | `[]` | 不加载任何 settings、CLAUDE.md、个人 skill、插件 |
| user-config | `[user]` | 加载 `~/.claude` 下的 settings.json、CLAUDE.md、skills、插件 |

两臂共同配置：

- `apiKeyRequired: false`
- `model: haiku`：与 `~/.claude/settings.json` 的默认模型一致
- `skills: all`
- `working_dir: fixtures/demo-project`：默认只开放只读工具
- MCP 不加载：provider 默认的 strict MCP 配置

### 用例与判分

| 用例 | 断言（`metric` 名） |
|---|---|
| 英文问"1+1 等于几" | 回复含中文（`rule-zh-reply`） |
| 英文问"加 LOG_LEVEL 配置要改哪些文件，先别改" | 提到 `config.py`（`outcome-config-py`）；读过 `ARCHITECTURE.md`（`rule-read-architecture`，查 `metadata.toolCalls`）；提到 README（`rule-sync-readme`）；回复含中文（`rule-zh-reply`） |
| skill：显式点名 grilling | `skill-used: mattpocock-skills:grilling` |
| skill：自然表述"拷问我的计划" | `skill-used`，pattern `mattpocock-skills:grill*` |
| skill：近似负例"帮我排学习时间表" | `not-skill-used`，pattern `mattpocock-skills:grill*` |

运行时默认 `--repeat 3 --no-cache`。

## 关键取舍

- **SDK 锁定 0.3.263**：与全局 promptfoo 0.123.1 的依赖版本一致；本机 npm 缓存已有，安装不需要重新下载。
- **只读任务**：promptfoo 内置 provider 的 `working_dir` 是整个 provider 共用的，多次运行、两臂并发写同一目录会互相污染。只读任务可以安全并发。
- **skill 触发单独成套**：参考 `claude plugin eval` 对 with-only grader 的处理，避免虚增 A/B 差值。
- **promptfoo 用全局安装**：本机已有 0.123.1，不在评测目录重复安装。

## 验证

用本机 Max 订阅跑通两套配置，各 `--repeat 3`，结果与用例预期一致或可解释。

## 差异说明（交付时补）

实现与上文方案的出入：

- `package.json` 除 SDK 外，还锁定了它的三个 peer 依赖（`@anthropic-ai/sdk` 0.124.0、`@modelcontextprotocol/sdk` 1.30.0、`zod` 4.6.5）。版本与 promptfoo 0.123.1 自带的一致，这样可以完全从 npm 缓存离线安装。
- `.gitignore` 只忽略 `node_modules/`。结果存在 promptfoo 本地库里，用 `npm run view` 查看，仓库内不落结果文件。
- fixture 的 `ARCHITECTURE.md` 刻意不写"同步 README"。这样"提到 README"只能来自 CLAUDE.md 规则，不会因为读了架构文档而顺带满足。

交付验证结果（haiku，每项 3 次）：

- A/B：
  - 读 ARCHITECTURE.md：baseline 1/3，user-config 3/3；
  - 中文回复：baseline 0/6，user-config 6/6；
  - `config.py`、README 两项两臂都是 3/3，区分不出差异。
- skill 触发：
  - 显式点名 3/3；
  - 自然表述 2/3；
  - 近似负例 3/3（均未误触发）。
