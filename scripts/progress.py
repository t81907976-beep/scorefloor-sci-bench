#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ScoreFloor-Sci-Bench 跑测实时进度面板。

只解析日志 + 读题库，不碰跑测进程，随时开关无副作用。

用法：
    python3 scripts/progress.py                    # 打印一次当前进度
    python3 scripts/progress.py -w                 # 每 15s 自动刷新，跑完自动停
    python3 scripts/progress.py -w -i 5            # 自定义刷新间隔（秒）
    python3 scripts/progress.py --log logs/xx.log  # 指定日志（默认取最新一份）
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import subprocess
import sys
import time
from typing import Dict, List, Optional, Tuple

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SUBJECT_CN = {"chemistry": "化学", "physics": "物理", "math": "数学", "biology": "生物"}

# 心跳行格式与 lib/runner.py 的 print 一一对应
RE_HEADER = re.compile(r"题数:\s*(\d+)；每题\s*(\d+)\s*次")
RE_TASK_START = re.compile(r"▶\s+(\S+?)（(\w+)，N0=(\d+)）")
RE_RUN_DONE = re.compile(
    r"·\s+(\S+)\s+run\s+(\d+)/(\d+)\s+(✓ 出正文|✗ 空答复|♻ 命中缓存)"
)
# 耗时单独取行尾括号：空答复行中间还有「(重抽耗尽)」括号，不能并进上面的正则
RE_DUR = re.compile(r"\((\d+)s\)\s*$")
RE_FINISHED = re.compile(r"全 Bench 总分|完整结果已写入")

C = {
    "reset": "\033[0m", "bold": "\033[1m", "dim": "\033[2m",
    "green": "\033[32m", "yellow": "\033[33m", "red": "\033[31m", "cyan": "\033[36m",
}

# __MORE__


def _c(text: str, *styles: str) -> str:
    if not sys.stdout.isatty():
        return text
    return "".join(C[s] for s in styles) + text + C["reset"]


def _wide_len(text: str) -> int:
    """终端显示宽度：CJK 字符占 2 列。"""
    import unicodedata
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def _pad(text: str, width: int) -> str:
    return text + " " * max(width - _wide_len(text), 0)


def _bar(done: int, total: int, width: int = 30, color: str = "green") -> str:
    total = max(total, 1)
    filled = int(round(width * min(done / total, 1.0)))
    return _c("█" * filled, color) + _c("░" * (width - filled), "dim")


def _fmt_dur(seconds: float) -> str:
    seconds = int(max(seconds, 0))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h} 时 {m} 分"
    if m:
        return f"{m} 分 {s} 秒"
    return f"{s} 秒"


def latest_log(explicit: Optional[str]) -> Optional[str]:
    if explicit:
        return explicit if os.path.exists(explicit) else None
    logs = glob.glob(os.path.join(_ROOT, "logs", "*.log"))
    return max(logs, key=os.path.getmtime) if logs else None


def _birthtime(path: str) -> float:
    """日志创建时间。macOS 有 st_birthtime；Linux 退回 st_mtime 以免把 ctime 当起点。"""
    st = os.stat(path)
    return getattr(st, "st_birthtime", None) or st.st_mtime


def runner_alive() -> Optional[int]:
    """跑测进程还在吗？返回 pid，否则 None。"""
    try:
        out = subprocess.run(["pgrep", "-f", "lib.runner"],
                             capture_output=True, text=True, timeout=5).stdout
    except Exception:
        return None
    for tok in out.split():
        if tok.strip().isdigit():
            return int(tok)
    return None


class TaskProgress:
    def __init__(self, task_id: str, subject: str):
        self.task_id = task_id
        self.subject = subject
        self.done_runs: Dict[int, float] = {}   # run_idx -> 耗时秒（缓存命中记 0）
        self.empty = 0
        self.started = False

    @property
    def done(self) -> int:
        return len(self.done_runs)

    @property
    def avg_seconds(self) -> Optional[float]:
        real = [s for s in self.done_runs.values() if s > 0]
        return sum(real) / len(real) if real else None


def parse_log(path: str) -> dict:
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()

    runs_per_task, task_total = 5, 0
    tasks: Dict[str, TaskProgress] = {}
    order: List[str] = []
    durations: List[float] = []

    for line in text.splitlines():
        m = RE_HEADER.search(line)
        if m:
            task_total, runs_per_task = int(m.group(1)), int(m.group(2))
            continue
        m = RE_TASK_START.search(line)
        if m:
            tid, subj = m.group(1), m.group(2)
            tp = tasks.setdefault(tid, TaskProgress(tid, subj))
            tp.started = True
            if tid not in order:
                order.append(tid)
            continue
        m = RE_RUN_DONE.search(line)
        if m:
            tid, run_idx, kind = m.group(1), int(m.group(2)), m.group(4)
            d = RE_DUR.search(line)
            secs = float(d.group(1)) if d else 0.0
            tp = tasks.setdefault(tid, TaskProgress(tid, ""))
            if tid not in order:
                order.append(tid)
            if kind.startswith("✗"):
                tp.empty += 1
                # 空答复也真实消耗了挂钟时间，计入总耗时用于 ETA
                if secs > 0:
                    durations.append(secs)
            else:
                tp.done_runs[run_idx] = secs
                if secs > 0:
                    durations.append(secs)

    return {
        "runs_per_task": runs_per_task,
        "task_total": task_total,
        "tasks": tasks,
        "order": order,
        "durations": durations,
        "finished": bool(RE_FINISHED.search(text)),
        "started_at": _birthtime(path),
        "mtime": os.path.getmtime(path),
    }


def known_tasks() -> List[Tuple[str, str]]:
    """从题库读出全部题目 (task_id, subject)，用于展示还没进队列的题。"""
    out = []
    tasks_dir = os.path.join(_ROOT, "tasks")
    for subj in sorted(os.listdir(tasks_dir)):
        d = os.path.join(tasks_dir, subj)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".md") and not fn.upper().startswith("TASK_TEMPLATE"):
                out.append((os.path.splitext(fn)[0], subj))
    return out


def render(log_path: str, state: dict, pid: Optional[int]) -> str:
    runs_per_task = state["runs_per_task"]
    tasks: Dict[str, TaskProgress] = state["tasks"]
    all_tasks = known_tasks()
    task_total = state["task_total"] or len(all_tasks)
    run_total = task_total * runs_per_task
    run_done = sum(t.done for t in tasks.values())
    empty_total = sum(t.empty for t in tasks.values())

    lines: List[str] = []
    if state["finished"]:
        status = _c("● 已完成", "green", "bold")
    elif pid:
        status = _c(f"● 运行中 pid {pid}", "green")
    else:
        status = _c("● 进程已退出（未见完成标记，可能中断）", "red")
    lines.append(f"{_c('ScoreFloor-Sci-Bench 跑测进度', 'bold')}   {status}")
    lines.append(_c(f"日志 {os.path.relpath(log_path, _ROOT)}", "dim"))
    lines.append("")

    pct = run_done / max(run_total, 1) * 100
    lines.append(f"  {_pad('总进度', 10)}{_bar(run_done, run_total, 34)}"
                 f"  {_c(f'{pct:5.1f}%', 'bold')}  {run_done}/{run_total} run")

    elapsed = (state["mtime"] if state["finished"] else time.time()) - state["started_at"]
    durs = state["durations"]
    tail = f"  已用 {_fmt_dur(elapsed)}"
    if run_done and not state["finished"]:
        # ETA 用实测挂钟节奏（elapsed/run_done），已含判分与并发的真实影响；
        # 心跳里的 (Ns) 只是答题耗时，直接拿它推算会偏长。
        eta = (run_total - run_done) * elapsed / run_done
        tail += f"   剩余 约 {_fmt_dur(eta)}"
    if durs:
        tail += f"   答题均值 {sum(durs) / len(durs):.0f}s"
        tail += f"   挂钟 {elapsed / max(run_done, 1):.0f}s/run"
    empty_txt = _c(f"空答复 {empty_total}", "yellow" if empty_total else "dim")
    lines.append(f"  {tail}   {empty_txt}")
    lines.append("")

    # 按学科分组
    by_subject: Dict[str, List[str]] = {}
    for tid, subj in all_tasks:
        by_subject.setdefault(subj, []).append(tid)

    queued = set(state["order"])
    not_queued = 0
    for subj, tids in by_subject.items():
        shown = [t for t in tids if t in queued]
        not_queued += len(tids) - len(shown)
        if not shown:
            continue
        s_done = sum(tasks[t].done for t in shown if t in tasks)
        s_total = len(tids) * runs_per_task
        cn = SUBJECT_CN.get(subj, subj)
        lines.append(f"  {_pad(cn, 10)}{_bar(s_done, s_total, 24, 'cyan')}  {s_done}/{s_total}")
        for tid in shown:
            tp = tasks[tid]
            if tp.done >= runs_per_task:
                mark, color = "✔", "green"
            elif tp.done or tp.started:
                mark, color = "▶", "yellow"
            else:
                mark, color = "·", "dim"
            avg = tp.avg_seconds
            note = f"均 {avg:.0f}s" if avg else "排队中"
            extra = _c(f"  空{tp.empty}", "yellow") if tp.empty else ""
            lines.append(f"    {_c(mark, color)} {_pad(tid, 16)}"
                         f"{_bar(tp.done, runs_per_task, 14, color if color != 'dim' else 'dim')}"
                         f"  {tp.done}/{runs_per_task}  {_c(note, 'dim')}{extra}")
        lines.append("")

    if not_queued:
        lines.append(_c(f"  另有 {not_queued} 道题还未进入队列", "dim"))

    tail = summary_tail(log_path)
    if tail:
        lines.append("")
        lines.append(_c("  ── 评测汇总 ──", "bold"))
        lines.extend("  " + ln for ln in tail.splitlines())
    return "\n".join(lines)


def summary_tail(path: str, limit: int = 40) -> str:
    """跑完后把日志尾部的「评测汇总」块原样带出来。

    价值在于不必再 `tail -f` 一次日志：进度面板本身就是收尾时看总分的地方。
    截到 limit 行，避免汇总很长时把上面的进度条挤出屏幕。
    """
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            txt = f.read()
    except OSError:
        return ""
    idx = txt.find("评测汇总")
    if idx < 0:
        return ""
    block = txt[max(0, idx - 25):].strip().splitlines()
    return "\n".join(block[:limit])


def main() -> int:
    ap = argparse.ArgumentParser(description="ScoreFloor-Sci-Bench 跑测实时进度面板")
    ap.add_argument("--log", default="", help="日志路径（默认取 logs/ 下最新一份）")
    ap.add_argument("-w", "--watch", action="store_true", help="持续刷新，跑完自动停")
    ap.add_argument("-i", "--interval", type=float, default=15.0, help="刷新间隔秒（默认 15）")
    args = ap.parse_args()

    path = latest_log(args.log)
    if not path:
        print("找不到日志。先跑测生成 logs/*.log，或用 --log 指定路径。")
        return 1

    while True:
        state = parse_log(path)
        pid = runner_alive()
        out = render(path, state, pid)
        if args.watch:
            sys.stdout.write("\033[H\033[J" if sys.stdout.isatty() else "\n")
        print(out, flush=True)
        if not args.watch:
            return 0
        if state["finished"] or not pid:
            print(_c("\n跑测已结束，停止刷新。", "bold"))
            return 0
        try:
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print()
            return 0


if __name__ == "__main__":
    raise SystemExit(main())


