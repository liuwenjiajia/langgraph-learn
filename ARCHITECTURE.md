# 架构

本仓库是"AI 智能体研发"学习项目，路线见 [学习蓝图](docs/AI智能体研发学习蓝图-6个月.md)。本文只写骨架：模块划分、职责边界、依赖方向、关键取舍。实现细节看代码。

## 模块划分

| 目录 | 职责 | 技术栈 |
|---|---|---|
| `src/` | 按学习阶段组织的代码，如 `src/day0-init/`（OpenAI / Anthropic SDK 调用示例） | Python 3.13，uv 管依赖（`pyproject.toml`） |
| `docker/` | 本地检索后端：Milvus Standalone + Elasticsearch，仅限本地开发 | Docker Compose |
| `evals/` | 评测套件，每个被测对象一个子目录，各自管理依赖 | 视被测对象而定 |
| `evals/claude-code/` | Claude Code 定制效果 A/B 评测：同一批用例，对比"无定制"与"加载 `~/.claude` 用户级定制" | promptfoo + Claude Agent SDK（Node） |
| `docs/` | 学习蓝图；`docs/research/` 调研笔记；`docs/specs/` 每次改动的实现方案记录 | Markdown |
| `journal/` | 每日学习日志 | Markdown |

## 依赖方向

- `src/` 通过网络端口使用 `docker/` 提供的服务，反之不成立。
- `evals/` 只调用被测对象，不被 `src/` 依赖；各评测套件互不共享依赖。

## 核心数据流：Claude Code 定制评测

```text
promptfoo（全局安装）
  → provider anthropic:claude-agent-sdk（两个实验臂，只差 setting_sources）
  → Claude Agent SDK → Claude Code 二进制 → 本机 Claude 订阅登录鉴权
  → 回复 + 工具调用 / skill 调用记录
  → promptfoo 断言判分，两臂并排对比
```

## 关键取舍

- **鉴权走 Claude 订阅，不用 API key**：provider 设 `apiKeyRequired: false`，由 Claude Code 自己鉴权。代价是每次都是真实调用（promptfoo 此时不缓存），会消耗订阅额度。
- **两臂只差 `setting_sources`**：`[]` 为无定制基线，`[user]` 加载 `~/.claude`。模型、工具、工作目录全部相同，差异才能归因到定制本身。
- **首版只用只读任务**：写文件的任务需要每次运行一个一次性工作区，promptfoo 内置 provider 做不到，留作后续。
- **skill 触发率单独成套、只跑有定制的臂**："skill 是否被调用"只可能在有定制时成立。放进 A/B 会拉低基线、虚增差值。
