#!/usr/bin/env python3
"""单题多模型单次评分：读 results/single-*.json 的答复 → 代码判分 + 裁判判分 → 落盘。

用法：
    python3 scripts/score_single.py test-化学09 --tag 化学09 \
        --judge <judge-model> \
        --sources single-化学09-20260803-143123.json,single-化学09-stream-....json
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import sys
import time

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from lib.judge import judge_answer                                  # noqa: E402
from lib.providers import build_provider, load_dotenv_if_present    # noqa: E402
from lib.scoring import E_MAX_DEFAULT, RunResult                    # noqa: E402
from lib.task_loader import discover_tasks                          # noqa: E402


def collect(sources, results_dir):
    """按 sources 顺序读入答复；同一模型出现多次时后者覆盖前者（重试结果优先）。"""
    latest = {}
    for name in sources:
        path = name if os.path.isabs(name) else os.path.join(results_dir, name)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for run in data.get("runs", []):
            if run.get("ok") and run.get("text", "").strip():
                latest[run["model"]] = dict(run, source=os.path.basename(path))
    return latest


def score_one(task, judge_provider, model, run):
    answer = run["text"]
    auto = task.grade_fn([{"role": "assistant", "content": answer}], _ROOT,
                         {"task_id": task.task_id})
    final = float(auto.get("auto_final_answer_score", 0.0))
    jr = judge_answer(judge_provider, reference=task.reference, steps=task.steps,
                      rubric=task.rubric, answer=answer,
                      baseline_steps=task.baseline_steps)
    rr = RunResult(final_answer_score=final, step_score=jr.step_score,
                   logic_score=jr.logic_score, actual_steps=jr.actual_steps)
    e_norm = rr.norm_efficiency(task.baseline_steps, E_MAX_DEFAULT)
    print(f"  ✓ {model}: 最终 {final:.3f} 步骤 {jr.step_score:.3f} "
          f"逻辑 {jr.logic_score:.3f} → S_i={rr.success:.4f} "
          f"(N={jr.actual_steps}, E_norm={e_norm:.4f})", flush=True)
    return {
        "model": model, "source": run.get("source"),
        "elapsed_s": run.get("elapsed_s"), "chars": len(answer),
        "finish_reason": run.get("finish_reason"),
        "answer": answer, "auto_detail": auto,
        "final_answer_score": round(final, 4),
        "step_score": round(jr.step_score, 4),
        "logic_score": round(jr.logic_score, 4),
        "actual_steps": jr.actual_steps,
        "S_i": round(rr.success, 4),
        "E_norm": round(e_norm, 4),
        "S_eff_i": round(rr.efficiency_score(task.baseline_steps, E_MAX_DEFAULT), 4),
        "judge_detail": jr.detail,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("task")
    ap.add_argument("--sources", required=True, help="results/ 下的 single-*.json，逗号分隔")
    ap.add_argument("--tag", default="")
    ap.add_argument("--judge", default="")
    ap.add_argument("--config", default=os.path.join(_ROOT, "config.json"))
    ap.add_argument("--concurrency", type=int, default=3)
    args = ap.parse_args()

    load_dotenv_if_present()
    with open(args.config, encoding="utf-8") as f:
        config = json.load(f)
    jcfg = dict(config["judge"], stream=True, timeout=1200, max_tokens=4096)
    if args.judge:
        jcfg["model"] = args.judge
    judge_provider = build_provider(jcfg)

    task = discover_tasks(os.path.join(_ROOT, "tasks"), task_ids=[args.task])[0]
    results_dir = os.path.join(_ROOT, "results")
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    answers = collect(sources, results_dir)

    print(f"题目 {task.task_id}（N0={task.baseline_steps}）；裁判 {judge_provider.model}；"
          f"待评 {len(answers)} 个模型\n", flush=True)

    items = list(answers.items())
    with cf.ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        scored = list(ex.map(lambda kv: score_one(task, judge_provider, *kv), items))
    scored.sort(key=lambda r: r["S_i"], reverse=True)

    stamp = time.strftime("%Y%m%d-%H%M%S")
    tag = args.tag or task.task_id
    out = os.path.join(results_dir, f"scored-{tag}-{stamp}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"task": task.task_id, "N0": task.baseline_steps,
                   "judge": judge_provider.model, "E_max": E_MAX_DEFAULT,
                   "sources": sources,
                   "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "runs": scored}, f, ensure_ascii=False, indent=2)

    print(f"\n{'模型':<20} {'最终':<7} {'步骤':<7} {'逻辑':<7} {'S_i':<8} {'N':<4} {'S_eff'}")
    for r in scored:
        print(f"{r['model']:<20} {r['final_answer_score']:<7} {r['step_score']:<7} "
              f"{r['logic_score']:<7} {r['S_i']:<8} {r['actual_steps']:<4} {r['S_eff_i']}")
    print(f"\n落盘：{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
