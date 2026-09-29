# langgraph-learn

智能体学习项目，路线见 [学习蓝图](docs/AI智能体研发学习蓝图-6个月.md)；模块划分见 [ARCHITECTURE.md](ARCHITECTURE.md)。

## 评测

### Claude Code 定制 A/B 评测（`evals/claude-code/`）

同一批用例跑两个实验臂，比较你的 Claude Code 定制有没有带来改善：

- **baseline**：不加载任何定制；
- **user-config**：加载 `~/.claude` 下的 CLAUDE.md、settings、skills、插件。

鉴权走本机 Claude 订阅登录（Pro / Max），**不需要 API key**。

**前提**

- Node ≥ 20；
- 全局安装 promptfoo：`npm install -g promptfoo`，已验证版本 0.123.1；
- Claude Code 已用订阅登录：`claude auth status` 显示 `"authMethod": "claude.ai"`；
- 环境里**不要**设置 `ANTHROPIC_API_KEY`，否则 Claude Code 会优先用 key。

**安装**（首次）：

```bash
cd evals/claude-code
npm install
```

`package.json` 锁定了 Claude Agent SDK 0.3.263 及其 peer 依赖，版本与 promptfoo 0.123.1 自带的一致。

**运行**

| 命令 | 作用 |
|---|---|
| `npm run eval` | CLAUDE.md 规则 A/B（`promptfooconfig.yaml`），每个用例每臂跑 3 次 |
| `npm run eval:skills` | skill 触发率（`skill-trigger.yaml`），只跑 user-config 臂 |
| `npm run view` | 打开网页并排查看结果；按 metric 看各条规则的通过率 |

**说明**

- 每次都是真实调用，会消耗订阅额度。promptfoo 显示的 cost 是按 API 价格的估算，不会另外计费。
- 换模型：改 `promptfooconfig.yaml` 里 `model: haiku` 那一处。两臂共用同一个锚点，改一处即可。
- 加用例：在 `tests` 里追加。英文提问、不提规则，才能测出规则是否来自你的 CLAUDE.md。
- 首版只含只读任务；写文件的任务需要一次性工作区，尚未支持。
- 设计与取舍见 [spec](docs/specs/2026-09-28-claude-code定制AB评测.md)；工具选型见 [调研笔记](docs/research/2026-09-28-Claude-Code定制效果评测工具调研.md)。
