#!/bin/bash
# 云端会话启动时确保 P2 语料（data/p2/raw/）已就绪。语料被 gitignore，新会话的仓库里没有它，
# 这里按 src/p2-rag/fetch_corpus.py 里固定的上游 commit 重建（约 4 秒）。
set -euo pipefail

# 只在云端会话跑；本机运行一次 fetch_corpus.py，语料就一直在
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}"

# 脚本或本 hook 变了才重建（上游 commit 和选页规则都写在 fetch_corpus.py 里）。
# 哈希文件放在被 gitignore 的 data/p2/raw/ 里：语料没了它也跟着没了，也不会被 git add 带上
hashes=data/p2/raw/.session-start.sha256
if [ ! -f data/p2/raw/_manifest.json ] || ! sha256sum --check --status "$hashes" 2>/dev/null; then
  # 先删旧哈希，重建失败的话下次启动会再试
  rm -f "$hashes"

  # 脚本打印的分组表很长，hook 的 stdout 会进会话上下文，所以丢掉；
  # 失败原因（含 git 的原话）走 stderr，不能吞，set -e 让 hook 报错退出
  GIT_TERMINAL_PROMPT=0 python3 src/p2-rag/fetch_corpus.py > /dev/null

  # 列出本脚本和所有决定语料内容的文件
  sha256sum .claude/hooks/session-start.sh src/p2-rag/fetch_corpus.py > "$hashes" || rm -f "$hashes"
fi

# 每次启动（含 resume / clear / compact）都说一声，stdout 会进会话上下文，让 Claude 知道语料在哪
python3 - <<'PY'
import json

m = json.load(open("data/p2/raw/_manifest.json", encoding="utf-8"))
t = m["totals"]
print(f"P2 语料已就绪：data/p2/raw/（{t['pages']} 页 / {t['words']} 词，上游 commit {m['meta']['commit'][:10]}），逐页来源和官网 URL 见 _manifest.json")
PY
