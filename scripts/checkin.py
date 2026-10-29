"""打卡进度：显示今日任务、累计进度和欠账日。

    python3 scripts/checkin.py                 # 今天
    python3 scripts/checkin.py --date 2026-11-02
    python3 scripts/checkin.py --dir docs/plan # 计划目录（默认 docs/plan）

只读 docs/plan/20*.md，不改任何文件；仅用标准库。
"""
import argparse
import datetime as dt
import re
from pathlib import Path

DAY = re.compile(r"^- \[([ x])\] \*\*(\d{4}-\d{2}-\d{2}) 周(.) · D(\d+)/(\d+) · (M\d)｜(.*?)\*\*")
TASK = re.compile(r"^  - \[([ x])\] (★|☆) (\d+)′ (.*)$")
DONE = re.compile(r"^  - 🎯 \*\*完成标准\*\*：(.*)$")


def load(plan_dir):
    days = []
    for f in sorted(Path(plan_dir).glob("20*.md")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if m := DAY.match(line):
                days.append(dict(
                    date=dt.date.fromisoformat(m[2]), wd=m[3], n=int(m[4]), total=int(m[5]),
                    mod=m[6], title=m[7], ticked=m[1] == "x", tasks=[], done="",
                ))
            elif days and (m := TASK.match(line)):
                days[-1]["tasks"].append((m[1] == "x", m[2], int(m[3]), m[4]))
            elif days and (m := DONE.match(line)):
                days[-1]["done"] = m[1]
    return days


def owed(day):
    """当天还没做完的 ★ 分钟数。"""
    return sum(m for ok, mk, m, _ in day["tasks"] if mk == "★" and not ok)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", type=dt.date.fromisoformat, default=dt.date.today())
    ap.add_argument("--dir", default="docs/plan")
    a = ap.parse_args()

    days = load(a.dir)
    if not days:
        raise SystemExit(f"{a.dir} 下没有找到打卡文件")
    today = a.date
    total = days[0]["total"]
    cur = next((d for d in days if d["date"] == today), None)

    print(f"📅 {today} 周{'一二三四五六日'[today.weekday()]}")
    if cur:
        left = sum(1 for ok, mk, *_ in cur["tasks"] if mk == "★" and not ok)
        print(f"D{cur['n']}/{total} · {cur['mod']}｜{cur['title']}  {'✅ 已打卡' if cur['ticked'] else f'（还剩 {left} 项 ★）'}")
        for ok, mk, m, t in cur["tasks"]:
            print(f"  [{'x' if ok else ' '}] {mk} {m}′ {t}")
        print(f"  🎯 {cur['done']}")
    elif today < days[0]["date"]:
        print(f"计划从 {days[0]['date']} 开始。")
    elif today > days[-1]["date"]:
        print("计划已结束，去蓝图末尾的「进度追踪」打勾。")
    else:
        print("今天不在计划日历内（周末 / 假期）：补课日，先清欠账，再做拓展思考。")

    past = [d for d in days if d["date"] < today]
    debt = [d for d in past if not d["ticked"]]
    ticked = sum(d["ticked"] for d in days)
    print(f"\n累计：已打卡 {ticked}/{total} 天；今天之前应完成 {len(past)} 天，欠账日 {len(debt)} 天，"
          f"欠 ★ 共 {sum(owed(d) for d in debt) / 60:.1f}h")

    wk = today.isocalendar()[:2]
    week = [d for d in days if d["date"].isocalendar()[:2] == wk]
    if week:
        all_m = sum(m for d in week for _, mk, m, _ in d["tasks"] if mk == "★")
        done_m = sum(m for d in week for ok, mk, m, _ in d["tasks"] if mk == "★" and ok)
        print(f"本周：★ 完成 {done_m}/{all_m} 分钟（{done_m * 100 // max(all_m, 1)}%）")

    for d in debt[-10:]:
        print(f"  欠账 {d['date']} D{d['n']} {d['title']}：★ 未完成 {owed(d)}′")
    if len(debt) > 10:
        print(f"  …… 另有 {len(debt) - 10} 个更早的欠账日")
    if sum(owed(d) for d in debt) >= 360:
        print("\n⚠️ 欠账 ≥ 6h：按 docs/plan/README.md 的「削减阶梯」处理。")


if __name__ == "__main__":
    main()
