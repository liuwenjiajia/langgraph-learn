"""构建 P2 语料：从 langchain-ai/docs 抽出 LangChain / LangGraph 的 Python 文档，写入 data/p2/raw/。

data/p2/raw/ 在 .gitignore 里不入库；换机器或语料丢了，重跑本脚本即可复现（默认固定到 PINNED_COMMIT）。

    uv run src/p2-rag/fetch_corpus.py              # 拉固定 commit，生成语料
    uv run src/p2-rag/fetch_corpus.py --ref main   # 刷新到上游最新（页数、字数会变）
    uv run src/p2-rag/fetch_corpus.py --src DIR    # 用已有的 langchain-ai/docs 检出，不联网

范围（src/oss 下；"哪些页属于 Python 站点"沿用上游的构建规则）：
  收：langchain/、langgraph/、concepts/、integrations/（共享 + Python 专属）、python/migrate、python/releases、reference/、顶层通用页
  不收：deepagents/、openwiki/（别的产品）；javascript/；contributing/（贡献指南）；*/frontend/（React/Vue 等纯前端 JS 页）；
        只出现在 JS 导航里的共享页；frontmatter 带 url 的纯外链页；TEMPLATE.mdx

每页只做两处改动，其余（frontmatter、import、<Tip> 等 MDX 组件、@[...] 链接）原样保留，留给 loader 处理：
  1. 解析 :::python / :::js 围栏，只留 Python 块。共享页里 JS/TS 占比很高，不去掉会污染检索。
  2. 把 `import X from '/snippets/*.mdx'` + `<X />` 内联成片段正文。官网上代码示例就在片段里，
     不内联的话，loader 删掉组件标签后这些示例会无声丢失。

文件路径镜像官网路由：raw/oss/python/langgraph/persistence.mdx ↔ https://docs.langchain.com/oss/python/langgraph/persistence
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_URL = "https://github.com/langchain-ai/docs"
# 固定 commit，页数和字数才可复现；想要最新内容用 --ref main
PINNED_COMMIT = "d948a8ac1016cde08899f706c5552b2babc23202"
SITE = "https://docs.langchain.com"
# 只检出文本：整库约 540MB（全是图片），这四类约 17MB
SPARSE = ["/LICENSE", "/src/docs.json", "/src/oss/**/*.mdx", "/src/snippets/**/*.mdx"]

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "data" / "p2" / "raw"
MANIFEST = "_manifest.json"

EXCLUDE_TOP = {"deepagents", "openwiki", "javascript", "contributing"}
# 任意层级的目录：frontend 是纯前端 JS 页；example_data 是 loader 文档的输入样本，不是页面
EXCLUDE_ANYWHERE = ("frontend", "example_data")
# 清单里的 js_blocks 统计这些语言的代码块，用来标出处理后仍带 JS 内容的页面
JS_LANGS = {"typescript", "ts", "tsx", "javascript", "js", "jsx", "mjs", "vue", "svelte"}

# 与上游 pipeline/preprocessors/markdown_preprocessor.py 的围栏正则一致，渲染结果才和官网 Python 站点相同
FENCE = re.compile(
    r"(?P<indent>[ \t]*)(?<!\\):::(?P<language>\w+)\s*\n"
    r"(?P<content>((?:.*\n)*?))"
    r"(?P=indent)[ \t]*(?<!\\):::"
)
SNIPPET_IMPORT = re.compile(r"^import\s+(\w+)\s+from\s+['\"](/snippets/[^'\"]+\.mdx)['\"];?[ \t]*\n?", re.M)
FRONTMATTER = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*\n", re.S)
CODE_FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})")


def keep_python(md: str) -> str:
    def pick(m: re.Match) -> str:
        lang = m.group("language")
        if lang not in ("python", "js"):
            return m.group(0)  # :::note 之类的提示框不是语言围栏
        return m.group("content") if lang == "python" else ""

    return re.sub(r"\\(:::)", r"\1", FENCE.sub(pick, md))  # \::: 是转义，还原成字面量


def indent_block(text: str, pad: str) -> str:
    return "\n".join(pad + line if line.strip() else line for line in text.split("\n"))


def inline_snippets(md: str, src: Path, warnings: list[str], trail: tuple[str, ...] = ()) -> tuple[str, list[str]]:
    """展开 .mdx 片段，返回 (文本, 内联过的片段路径)。.jsx/.tsx 是组件、没有文本，不动。"""
    names: dict[str, str] = {}

    def take(m: re.Match) -> str:
        path = m.group(2)
        if not (src / path.lstrip("/")).is_file():
            warnings.append(f"片段不存在: {path}")
            return m.group(0)
        names[m.group(1)] = path
        return ""  # import 行摘掉；用到的会内联，没用到的（JS 版本，围栏删掉后没人引用）也不留

    md = SNIPPET_IMPORT.sub(take, md)
    used: list[str] = []
    for name, path in names.items():
        tag = re.compile(rf"^([ \t]*)<{name}[ \t]*/>[ \t]*$", re.M)
        if not tag.search(md):
            continue
        if path in trail:
            warnings.append(f"片段循环引用: {path}")
            continue
        snippet = keep_python((src / path.lstrip("/")).read_text(encoding="utf-8"))
        body, inner = inline_snippets(snippet, src, warnings, trail + (path,))
        body = body.strip("\n")
        md = tag.sub(lambda m: indent_block(body, m.group(1)), md)  # 保留标签所在缩进，列表/Tab 里的代码块才不会错位
        used += [path, *inner]
        if re.search(rf"<{name}\b", md):
            warnings.append(f"片段 {name} 还有没展开的用法（不在行首独占一行）")
    return md, used


def split_frontmatter(text: str) -> tuple[str, str]:
    m = FRONTMATTER.match(text)
    return (m.group(1), text[m.end():]) if m else ("", text)


def frontmatter_value(fm: str, key: str) -> str | None:
    m = re.search(rf"^{key}:[ \t]*(.*)$", fm, re.M)
    return m.group(1).strip().strip("\"'") if m else None


def page_title(fm: str, body: str) -> str | None:
    # 个别页面（如 providers/cala）没有 frontmatter，退而取正文第一行的 # 标题
    if title := frontmatter_value(fm, "title"):
        return title
    m = re.match(r"\s*#[ \t]+(.+)", body)
    return m.group(1).strip() if m else None


def excluded_dir(rel: Path) -> str | None:
    if rel.parts[0] in EXCLUDE_TOP:
        return rel.parts[0]
    return next((f"*/{d}" for d in EXCLUDE_ANYWHERE if d in rel.parts[:-1]), None)


def count_text(text: str) -> tuple[int, int, int, int]:
    """返回 (词数, 字符数, 代码块内词数, 残留 JS/TS 代码块数)。词数 = 空白切分，与 wc -w 同口径。"""
    code_words = js_blocks = 0
    fence = None
    for line in text.split("\n"):
        m = CODE_FENCE.match(line)
        if fence is None:
            if m:
                fence = m.group(1)
                info = line.strip()[len(fence):].strip().split(" ")[0].lower()
                js_blocks += info in JS_LANGS
            continue
        s = line.strip()
        if s and set(s) == {fence[0]} and len(s) >= len(fence):
            fence = None
        else:
            code_words += len(line.split())
    return len(text.split()), len(text), code_words, js_blocks


def nav_routes(docs_json: Path) -> tuple[set[str], set[str]]:
    """Build 菜单下 Python / TypeScript 两个下拉里列出的页面路由。"""

    def walk(node):
        if isinstance(node, str):
            yield node
        elif isinstance(node, list):
            for x in node:
                yield from walk(x)
        elif isinstance(node, dict) and "pages" in node:
            yield from walk(node["pages"])

    found = {}
    for product in json.loads(docs_json.read_text(encoding="utf-8"))["navigation"]["products"]:
        for item in product.get("menu", []):
            if item.get("item") == "Build":
                for dd in item["dropdowns"]:
                    found[dd["dropdown"]] = set(walk(dd["tabs"]))
    if not {"Python", "TypeScript"} <= found.keys():
        sys.exit("docs.json 的导航结构变了：找不到 Build 下的 Python / TypeScript 下拉，需要更新 nav_routes()")
    return found["Python"], found["TypeScript"]


def route_of(rel: Path) -> str:
    """src/oss 下的相对路径 → 官网 Python 站点的路由。共享页在构建时被放进 oss/python/ 下。"""
    r = rel.with_suffix("").as_posix()
    return f"oss/{r}" if rel.parts[0] == "python" else f"oss/python/{r}"


def group_of(route: str) -> str:
    parts = route.split("/")[2:]
    if parts[0] == "integrations":
        return f"integrations/{parts[1]}" if len(parts) > 2 else "integrations/(root)"
    return parts[0] if parts[0] in ("langchain", "langgraph", "concepts", "migrate", "releases") else "other"


def write_pages(repo: Path, tmp_out: Path, commit: str) -> dict:
    src = repo / "src"
    oss = src / "oss"
    py_nav, js_nav = nav_routes(src / "docs.json")

    pages: list[dict] = []
    skipped: dict[str, list[str]] = defaultdict(list)
    excluded_dirs: dict[str, int] = defaultdict(int)

    for p in sorted(oss.rglob("*.mdx")):
        rel = p.relative_to(oss)
        if label := excluded_dir(rel):
            excluded_dirs[label] += 1
            continue

        raw = p.read_bytes()
        text = raw.decode("utf-8").replace("\r\n", "\n")  # 有个页面（langchain/philosophy）是 CRLF，不统一的话 frontmatter 解析不出来
        fm, _ = split_frontmatter(text)
        route = route_of(rel)
        shared = rel.parts[0] != "python"
        if frontmatter_value(fm, "url"):
            skipped["外链页（frontmatter 有 url，无正文）"].append(rel.as_posix())
            continue
        if p.name == "TEMPLATE.mdx":
            skipped["模板占位页"].append(rel.as_posix())
            continue
        if shared and route.replace("oss/python/", "oss/javascript/", 1) in js_nav and route not in py_nav:
            skipped["只在 JS 导航里，不构建 Python 版"].append(rel.as_posix())
            continue

        warnings: list[str] = []
        text = keep_python(text)
        text, snippets = inline_snippets(text, src, warnings)
        body = split_frontmatter(text)[1]
        if not body.strip():
            skipped["保留 Python 块后正文为空"].append(rel.as_posix())
            continue
        if re.search(r"^[ \t]*:::", text, re.M):
            warnings.append("含 ::: 行（上游围栏没配平，官网渲染同样如此；或是 :::note 式提示框）")

        words, chars, code_words, js_blocks = count_text(text)
        dest = tmp_out / f"{route}.mdx"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8", newline="\n")
        pages.append({
            "path": dest.relative_to(tmp_out).as_posix(),
            "source": f"src/oss/{rel.as_posix()}",
            "url": f"{SITE}/{route.removesuffix('/index')}",
            "title": page_title(fm, body),
            "group": group_of(route),
            "words": words,
            "chars": chars,
            "code_words": code_words,
            "js_blocks": js_blocks,
            "inlined_snippets": snippets,
            "warnings": warnings,
            "source_sha256": hashlib.sha256(raw).hexdigest(),
        })

    totals = {k: sum(pg[k] for pg in pages) for k in ("words", "chars", "code_words")}
    totals["pages"] = len(pages)
    by_group: dict[str, dict[str, int]] = defaultdict(lambda: {"pages": 0, "words": 0, "chars": 0})
    for pg in pages:
        for k in ("words", "chars"):
            by_group[pg["group"]][k] += pg[k]
        by_group[pg["group"]]["pages"] += 1

    manifest = {
        "meta": {
            "source_repo": REPO_URL,
            "commit": commit,
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "license": "MIT, 见同目录 LICENSE（Copyright (c) 2025 LangChain）",
            "word_count": "len(text.split())，统计的是落盘文件全文（含 frontmatter、代码块）",
            "transforms": [
                "保留 :::python 围栏内容、删除 :::js 围栏（与上游同一条正则）",
                "内联 /snippets/*.mdx 片段并移除对应 import；.jsx/.tsx 组件不动",
                "CRLF 统一为 LF",
            ],
            "excluded_dirs": dict(excluded_dirs),
        },
        "totals": totals,
        "by_group": dict(sorted(by_group.items())),
        "skipped": dict(skipped),
        "pages": pages,
    }
    (tmp_out / MANIFEST).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    license_file = repo / "LICENSE"
    if license_file.is_file():
        shutil.copy(license_file, tmp_out / "LICENSE")
    return manifest


def build(repo: Path, out: Path, commit: str) -> None:
    # 先写临时目录再替换，中途失败不会把已有语料删掉；临时目录不在 .gitignore 里，所以一定要清掉
    tmp_out = out.with_name(out.name + ".tmp")
    shutil.rmtree(tmp_out, ignore_errors=True)
    try:
        manifest = write_pages(repo, tmp_out, commit)
        if out.exists():
            if any(out.iterdir()) and not (out / MANIFEST).is_file():
                sys.exit(f"{out} 非空且不是本脚本生成的（没有 {MANIFEST}），为免误删，请先手动处理")
            shutil.rmtree(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp_out.rename(out)
    finally:
        shutil.rmtree(tmp_out, ignore_errors=True)  # 成功时已被改名，这里是空操作
    print_report(manifest, out)


def print_report(manifest: dict, out: Path) -> None:
    t, groups = manifest["totals"], manifest["by_group"]
    print(f"\n语料已写入 {out}（commit {manifest['meta']['commit'][:10]}）\n")
    print(f"{'pages':>6s}{'words':>10s}{'chars':>11s}  group")
    core = {"pages": 0, "words": 0, "chars": 0}
    for g, v in groups.items():
        print(f"{v['pages']:6d}{v['words']:10d}{v['chars']:11d}  {g}")
        if not g.startswith("integrations/"):
            for k in core:
                core[k] += v[k]
    print("-" * 40)
    print(f"{core['pages']:6d}{core['words']:10d}{core['chars']:11d}  核心文档（非 integrations）")
    print(f"{t['pages']:6d}{t['words']:10d}{t['chars']:11d}  合计")
    print(f"\n其中代码块内 {t['code_words']} 词（{100 * t['code_words'] / t['words']:.0f}%）")
    for reason, files in manifest["skipped"].items():
        print(f"跳过 {len(files):3d} 页：{reason}")
    for d, n in manifest["meta"]["excluded_dirs"].items():
        print(f"不收 {n:3d} 页：{d}/")
    flagged = [pg for pg in manifest["pages"] if pg["warnings"] or pg["js_blocks"]]
    if flagged:
        print(f"\n需留意的页面 {len(flagged)} 个（详见 {MANIFEST}）：")
        for pg in flagged[:12]:
            print(f"  {pg['path']}  js_blocks={pg['js_blocks']} {'; '.join(pg['warnings'])}")


def fetch(ref: str, dest: Path) -> str:
    env = {**os.environ, "GIT_LFS_SKIP_SMUDGE": "1"}  # 只要文本，LFS 对象也不拉

    def git(*args: str) -> str:
        r = subprocess.run(["git", "-C", str(dest), *args], env=env, capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"git {' '.join(args)} 失败（{r.returncode}）：\n{r.stderr.strip()}")  # 不带 stderr 的话网络/代理问题没法排查
        return r.stdout.strip()

    git("init", "-q")
    git("remote", "add", "origin", REPO_URL)
    git("config", "extensions.partialClone", "origin")  # 配合 --filter=blob:none：先不拉文件内容，检出时只按需拉稀疏范围内的
    git("fetch", "-q", "--depth", "1", "--filter=blob:none", "origin", ref)
    git("sparse-checkout", "set", "--no-cone", *SPARSE)
    git("checkout", "-q", "FETCH_HEAD")
    return git("rev-parse", "HEAD")


def main() -> None:
    ap = argparse.ArgumentParser(description="从 langchain-ai/docs 构建 P2 语料（LangChain / LangGraph 的 Python 文档）")
    ap.add_argument("--ref", default=PINNED_COMMIT, help="要拉取的 commit 或分支（默认固定 commit，保证可复现）")
    ap.add_argument("--src", type=Path, help="已有的 langchain-ai/docs 检出目录；给了就不联网")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"输出目录（默认 {DEFAULT_OUT.relative_to(REPO_ROOT)}）")
    args = ap.parse_args()

    if args.src:
        probe = subprocess.run(["git", "-C", str(args.src), "rev-parse", "HEAD"], capture_output=True, text=True)
        build(args.src, args.out, probe.stdout.strip() or "unknown")
    else:
        with tempfile.TemporaryDirectory(prefix="langchain-docs-") as tmp:
            build(Path(tmp), args.out, fetch(args.ref, Path(tmp)))


if __name__ == "__main__":
    main()
