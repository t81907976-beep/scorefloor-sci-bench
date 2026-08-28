#!/usr/bin/env python3
"""
ScoreFloor-Sci-Bench — 一键评测编排 (Runner)

全自动链路（用户视角）：
    配好 config.json（被测模型 + 裁判模型） → 一条命令 → 拿到评分。

对每道题：
    1. 用被测模型对题面跑 N 次（默认 5）得到 N 条答复
    2. 对每条答复：
       - Automated Checks 的 grade() → 最终答复分（代码侧硬证据）
       - 裁判模型按 Rubric → 逻辑分 / 步骤分 / 有效步骤数 N_i
       - 组装成 lib.scoring.RunResult
    3. N 条 RunResult → lib.scoring.TaskResult → S_success / S_eff / S_consistency / S_task
最后 lib.scoring.summarize() 汇总出 bench_total 与各学科分，落盘到 results/。

用法：
    python -m lib.runner --config config.json
    python -m lib.runner --config config.json --subjects chemistry --runs 5
    python -m lib.runner --config config.json --tasks test-化学05
    python -m lib.runner --config config.json --dry-run       # 不调 API，用占位答复自检链路
    python -m lib.runner --config config.json --check         # 只预检端点/Token/模型名
    python -m lib.runner --config config.json --list-models   # 拉取端点可用模型清单
    python -m lib.runner --config config.json --models "model-a,model-b"  # 多模型横评
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import sys
import time
from typing import List, Optional

# 允许 `python lib/runner.py` 与 `python -m lib.runner` 两种方式
_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_THIS)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from lib.judge import JudgeResult, judge_answer          # noqa: E402
from lib.providers import (                                # noqa: E402
    KNOWN_MODELS,
    BaseProvider,
    ChatResult,
    build_provider,
    has_model_allowlist,
    list_models,
    load_dotenv_if_present,
)
from lib.scoring import RunResult, TaskResult, summarize  # noqa: E402
from lib.task_loader import Task, discover_tasks          # noqa: E402


# --------------------------------------------------------------------------
# dry-run 用的假 provider：不联网，回吐固定占位答复，用于自检整条链路
# --------------------------------------------------------------------------
class MockProvider(BaseProvider):
    name = "mock"

    def chat(self, prompt: str, system: Optional[str] = None) -> ChatResult:
        if system and "评审" in system:
            # 冒充裁判：回一段合法 JSON
            return ChatResult(text=json.dumps({
                "logic_score": 0.8, "step_score": 0.8, "actual_steps": 5,
                "criteria": [], "comment": "dry-run 占位裁判结果",
            }))
        return ChatResult(text="dry-run 占位答复：(5R,6S)-顺-5,6-二甲基环己-1,3-二烯，meso，热对旋主导。")


def _make_provider(cfg: dict, dry_run: bool) -> BaseProvider:
    if dry_run:
        return MockProvider(model=cfg.get("model", "mock"))
    return build_provider(cfg)


# --------------------------------------------------------------------------
# 逐 run 缓存：让中途停掉/换题后能续跑，不浪费已跑完的 run
#
# 缓存键 = 被测模型 + task_id + run 序号 + (题面/参考答案/rubric/裁判) 指纹。
# 题面或裁判一变，指纹就变、旧缓存自动失效，不会串味。
# 只缓存「出了正文」的 run：空答复/重抽耗尽不落缓存，续跑时自然重试。
# --------------------------------------------------------------------------
CACHE_DIR = os.path.join(_ROOT, ".bench-cache")


def _cache_fingerprint(task: Task, judge_model: Optional[str]) -> str:
    h = hashlib.sha256()
    h.update((task.query or "").encode("utf-8"))
    h.update((task.reference or "").encode("utf-8"))
    rubric = task.rubric
    h.update(json.dumps(rubric, ensure_ascii=False, sort_keys=True).encode("utf-8")
             if rubric else b"")
    h.update(str(task.baseline_steps).encode("utf-8"))
    h.update((judge_model or "").encode("utf-8"))
    return h.hexdigest()[:12]


def _cache_path(cache_dir: str, model_name: str, task: Task,
                run_idx: int, fp: str) -> str:
    safe_model = model_name.replace("/", "_")
    return os.path.join(cache_dir, f"{safe_model}__{task.task_id}__run{run_idx}__{fp}.json")


def _load_cached_run(cache_dir: str, model_name: str, task: Task,
                     run_idx: int, judge_model: Optional[str]) -> Optional[dict]:
    fp = _cache_fingerprint(task, judge_model)
    path = _cache_path(cache_dir, model_name, task, run_idx, fp)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _save_cached_run(cache_dir: str, model_name: str, task: Task,
                     run_idx: int, judge_model: Optional[str], run_dict: dict) -> None:
    fp = _cache_fingerprint(task, judge_model)
    os.makedirs(cache_dir, exist_ok=True)
    path = _cache_path(cache_dir, model_name, task, run_idx, fp)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(run_dict, f, ensure_ascii=False, indent=2)
    except Exception:
        pass  # 缓存写失败不影响主链路


# --------------------------------------------------------------------------
# 单次运行：被测模型答一次 → grade → judge → RunResult
# --------------------------------------------------------------------------
def run_once(task: Task, model: BaseProvider, judge: Optional[BaseProvider],
             run_idx: int, workspace: str, runs_total: int = 0) -> dict:
    t0 = time.time()
    res = model.chat(task.query)
    answer = res.text
    # 逐调用实时心跳：出正文/空答复一目了然，避免长任务中途静默。
    # 思考型模型经重抽仍空时 raw 会带 resample_exhausted，这里一并提示。
    raw = res.raw if isinstance(res.raw, dict) else {}
    dt = time.time() - t0
    # 诊断字段：finish_reason（撞 max_tokens 被截断）+ 输出 token 数 + 耗时。
    # 排查「某题让某模型耗时飙升」时，看是超长思考(截断/大输出 token)
    # 还是网关拥塞(正常停止但耗时长)一目了然。
    # raw 形态随链路不同（OpenAI/Anthropic × 流式/非流式）字段位置各异，逐一兜底：
    #   finish_reason: 顶层(两种 SSE 累积器) → choices[0](OpenAI 非流式) → stop_reason(Anthropic 非流式)
    #   输出 token   : completion_tokens(OpenAI) → output_tokens(Anthropic)
    choice0 = (raw.get("choices") or [{}])[0]
    finish_reason = (raw.get("finish_reason")
                     or choice0.get("finish_reason")
                     or raw.get("stop_reason"))
    usage = raw.get("usage") or {}
    completion_tokens = usage.get("completion_tokens")
    if completion_tokens is None:
        completion_tokens = usage.get("output_tokens")
    # OpenAI 截断=finish_reason "length"；Anthropic 截断=stop_reason "max_tokens"
    is_truncated = finish_reason in ("length", "max_tokens")
    if answer.strip():
        trunc = "⚠截断" if is_truncated else ""
        tok = f",{completion_tokens}tok" if completion_tokens is not None else ""
        flag = f"✓ 出正文 {len(answer)}字{tok} [{finish_reason}]{trunc}"
    elif raw.get("resample_exhausted"):
        flag = "✗ 空答复(重抽耗尽)"
    else:
        flag = f"✗ 空答复 [{finish_reason}]"
    print(f"    · {task.task_id} run {run_idx}/{runs_total or '?'}  {flag}  ({dt:.0f}s)",
          flush=True)

    # 代码侧：最终答复分
    final_score = 0.0
    auto_detail: dict = {}
    if task.grade_fn is not None:
        transcript = [{"role": "assistant", "content": answer}]
        try:
            auto_detail = task.grade_fn(transcript, workspace, {"task_id": task.task_id})
            final_score = float(auto_detail.get("auto_final_answer_score", 0.0))
        except Exception as exc:  # 题目自带 grade 出错不应中断整轮
            auto_detail = {"grade_error": str(exc)}
            final_score = 0.0
            # 静默记 0 会让「grade 崩了」和「模型真答错」长得一样，必须喊出来。
            print(f"      ⚠ {task.task_id} grade() 异常，final 分记 0：{exc}", flush=True)

    # 裁判侧：逻辑分 / 步骤分 / 有效步骤数
    if judge is not None:
        jr = judge_answer(
            judge, reference=task.reference, steps=task.steps,
            rubric=task.rubric, answer=answer, baseline_steps=task.baseline_steps,
        )
    else:
        jr = JudgeResult(0.0, 0.0, task.baseline_steps, {"judge": "disabled"})

    return {
        "run_idx": run_idx,
        "answer": answer,
        "final_answer_score": round(final_score, 4),
        "step_score": round(jr.step_score, 4),
        "logic_score": round(jr.logic_score, 4),
        "actual_steps": jr.actual_steps,
        "auto_detail": auto_detail,
        "judge_detail": jr.detail,
        # 诊断：定位「某题拖慢某模型」是截断/超长思考还是网关拥塞
        "gen_seconds": round(dt, 1),
        "finish_reason": finish_reason,
        "completion_tokens": completion_tokens,
        "answer_chars": len(answer),
    }


# --------------------------------------------------------------------------
# 单题：跑 N 次 → 聚合成 TaskResult
# --------------------------------------------------------------------------
def run_task(task: Task, model: BaseProvider, judge: Optional[BaseProvider],
             runs: int, workspace: str, concurrency: int = 1,
             use_cache: bool = False, cache_dir: str = CACHE_DIR,
             model_name: Optional[str] = None) -> tuple:
    print(f"  ▶ {task.task_id}（{task.subject}，N0={task.baseline_steps}）跑 {runs} 次…", flush=True)

    judge_model = judge.model if judge else None
    cache_model = model_name or model.model

    def _one(i: int) -> dict:
        run_idx = i + 1
        if use_cache:
            cached = _load_cached_run(cache_dir, cache_model, task, run_idx, judge_model)
            if cached is not None:
                ans_len = len((cached.get("answer") or ""))
                print(f"    · {task.task_id} run {run_idx}/{runs}  ♻ 命中缓存 {ans_len}字",
                      flush=True)
                return cached
        d = run_once(task, model, judge, run_idx, workspace, runs_total=runs)
        # 只缓存出了正文的 run；空答复/重抽耗尽不落盘，续跑时重试
        if use_cache and (d.get("answer") or "").strip():
            _save_cached_run(cache_dir, cache_model, task, run_idx, judge_model, d)
        return d

    if concurrency > 1:
        with cf.ThreadPoolExecutor(max_workers=concurrency) as ex:
            run_dicts = list(ex.map(_one, range(runs)))
    else:
        run_dicts = [_one(i) for i in range(runs)]

    run_results = [
        RunResult(
            final_answer_score=d["final_answer_score"],
            step_score=d["step_score"],
            logic_score=d["logic_score"],
            actual_steps=d["actual_steps"],
        )
        for d in run_dicts
    ]
    task_result = TaskResult(
        task_id=task.task_id,
        baseline_steps=task.baseline_steps,
        runs=run_results,
        subject=task.subject,
    )
    return task_result, run_dicts


# --------------------------------------------------------------------------
# 全 Bench 编排
# --------------------------------------------------------------------------
def run_bench(config: dict, args) -> dict:
    tasks_dir = config.get("tasks_dir") or os.path.join(_ROOT, "tasks")
    tasks = discover_tasks(
        tasks_dir,
        subjects=args.subjects.split(",") if args.subjects else None,
        task_ids=args.tasks.split(",") if args.tasks else None,
    )
    if not tasks:
        raise SystemExit(f"未找到题目（tasks_dir={tasks_dir}，subjects={args.subjects}，tasks={args.tasks}）")

    model = _make_provider(config["model_under_test"], args.dry_run)
    judge_cfg = config.get("judge")
    judge = _make_provider(judge_cfg, args.dry_run) if judge_cfg else None
    if judge is None:
        print("  ⚠ 未配置 judge，逻辑分/步骤分记 0，仅算最终答复分与一致性。")

    print(f"被测模型: {model.model}（{model.name} 接口）；裁判: "
          f"{judge.model if judge else '无'}"
          f"{f'（{judge.name} 接口）' if judge else ''}；题数: {len(tasks)}；每题 {args.runs} 次")

    task_results = []
    detailed = []
    use_cache = getattr(args, "resume", False)
    cache_dir = getattr(args, "cache_dir", None) or CACHE_DIR
    model_name = config["model_under_test"].get("model")
    task_concurrency = max(1, getattr(args, "task_concurrency", 1) or 1)

    def _one_task(task: Task) -> tuple:
        return run_task(task, model, judge, args.runs, _ROOT, args.concurrency,
                        use_cache=use_cache, cache_dir=cache_dir,
                        model_name=model_name)

    # provider 实例初始化后只读（每次 chat 自建连接），可跨线程共享。
    if task_concurrency > 1:
        print(f"  ⚡ 题目级并发 {task_concurrency}，单题内并发 {args.concurrency}"
              f"（峰值并发请求 ≈ {task_concurrency * max(1, args.concurrency)}）")
        with cf.ThreadPoolExecutor(max_workers=task_concurrency) as ex:
            paired = list(ex.map(_one_task, tasks))
    else:
        paired = [_one_task(t) for t in tasks]

    for task, (tr, run_dicts) in zip(tasks, paired):
        task_results.append(tr)
        detailed.append({"task": task.task_id, "subject": task.subject, "runs": run_dicts,
                         "breakdown": tr.breakdown()})

    report = summarize(task_results)
    report["meta"] = {
        "model_under_test": model.model,
        "model_interface": model.name,
        "judge": judge.model if judge else None,
        "judge_interface": judge.name if judge else None,
        "runs_per_task": args.runs,
        "dry_run": args.dry_run,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    report["detailed"] = detailed
    return report


# --------------------------------------------------------------------------
# 配置预检 / 模型清单：不跑题，只确认端点 + Token + 模型名可用
# --------------------------------------------------------------------------
def do_list_models(config: dict) -> int:
    """GET /models 拉取端点实际可用的模型 id。"""
    load_dotenv_if_present()
    cfg = config["model_under_test"]
    base_url = cfg.get("base_url") or ""
    api_key = cfg.get("api_key") or os.environ.get(cfg.get("api_key_env", ""), "")
    if not api_key:
        print(f"✗ 缺少 Token：环境变量 {cfg.get('api_key_env')} 未设置（可写入项目根的 .env）")
        return 1

    models = list_models(base_url, api_key)
    print(f"{base_url} 可用模型（{len(models)} 个）：")
    for m in models:
        print(f"  · {m}")

    stale = set(models) ^ set(KNOWN_MODELS)
    if has_model_allowlist(base_url) and stale:
        print("\n  ⚠ 与 lib/providers.py 的 KNOWN_MODELS 白名单有差异"
              "（仅影响预检提示，不影响调用）：")
        for m in sorted(set(models) - set(KNOWN_MODELS)):
            print(f"    + 端点新增: {m}")
        for m in sorted(set(KNOWN_MODELS) - set(models)):
            print(f"    - 端点已下线: {m}")
    return 0


def do_check(config: dict, models: Optional[List[str]] = None) -> int:
    """对被测模型和裁判模型各发一次最小请求，确认链路可用。

    传了 models 时逐个预检这些被测模型，适合多模型对比前一次性确认 Token 权限。
    """
    ok = True
    targets = [("被测模型", dict(config["model_under_test"], model=m)) for m in (models or [])]
    if not targets:
        targets = [("被测模型", config["model_under_test"])]
    if config.get("judge"):
        targets.append(("裁判模型", config["judge"]))

    for label, cfg in targets:
        try:
            provider = build_provider(cfg)
            reply = provider.chat("回复两个字：就绪").text.strip()
            print(f"  ✓ {label} {provider.model}（{provider.name} 接口）可用，返回：{reply[:40]}")
        except Exception as exc:
            ok = False
            print(f"  ✗ {label} {cfg.get('model')} 不可用：\n    {exc}")

    print("\n预检通过，可以直接 ./scripts/run.sh 跑测。" if ok else "\n预检未通过，请按上面提示修正 config.json / .env。")
    return 0 if ok else 1


def _save(report: dict, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    model = report["meta"]["model_under_test"].replace("/", "_")
    path = os.path.join(out_dir, f"bench-{model}-{stamp}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return path


def _print_summary(report: dict) -> None:
    print("\n==================== 评测汇总 ====================")
    print(f"全 Bench 总分 S_total = {report['bench_total']}")
    for subj, score in report.get("by_subject", {}).items():
        print(f"  · {subj}: {score}")
    print("  单题：")
    for t in report["tasks"]:
        print(f"    - {t['task_id']}: S_task={t['S_task']} "
              f"(成功{t['S_success']}/效率{t['S_eff']}/一致{t['S_consistency']})")
    print("=================================================")


def _print_leaderboard(rows: List[dict]) -> None:
    """多模型横向对比表，按 S_total 降序。裁判与题目集相同，分数才可比。"""
    print("\n==================== 多模型对比 ====================")
    ok = [r for r in rows if r.get("bench_total") is not None]
    failed = [r for r in rows if r.get("bench_total") is None]
    ok.sort(key=lambda r: r["bench_total"], reverse=True)

    print(f"{'排名':<4} {'模型':<22} {'总分':<8} {'成功率':<8} {'效率':<8} {'一致性':<8}")
    for i, r in enumerate(ok, 1):
        print(f"{i:<5} {r['model']:<22} {r['bench_total']:<8} "
              f"{r['S_success']:<8} {r['S_eff']:<8} {r['S_consistency']:<8}")
    for r in failed:
        # 错误原文可能多行（含网关响应体），表格里只取第一行，完整内容在 compare-*.json
        brief = (r["error"].splitlines() or [""])[0][:60]
        print(f"{'-':<5} {r['model']:<22} 失败: {brief}")
    print("===================================================")


def _mean(xs: List[float]) -> float:
    return round(sum(xs) / len(xs), 4) if xs else 0.0


def _save_comparison(rows: List[dict], meta: dict, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    path = os.path.join(out_dir, f"compare-{stamp}.json")
    payload = {"meta": meta, "leaderboard": sorted(
        [r for r in rows if r.get("bench_total") is not None],
        key=lambda r: r["bench_total"], reverse=True,
    ), "failed": [r for r in rows if r.get("bench_total") is None]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


def run_multi_models(config: dict, args, models: List[str]) -> int:
    """
    依次用多个被测模型跑同一套题（裁判固定不变），各自落盘，最后出横向对比表。
    单个模型失败（Token 无权限、模型下线等）不中断整批。
    """
    out_dir = args.out or os.path.join(_ROOT, "results")
    rows: List[dict] = []
    paths: List[str] = []

    for idx, model_name in enumerate(models, 1):
        print(f"\n########## [{idx}/{len(models)}] 被测模型: {model_name} ##########")
        cfg = json.loads(json.dumps(config))       # 深拷贝，避免污染后续轮次
        cfg["model_under_test"]["model"] = model_name
        try:
            report = run_bench(cfg, args)
        except Exception as exc:
            print(f"  ✗ {model_name} 评测失败：{exc}")
            rows.append({"model": model_name, "bench_total": None, "error": str(exc)[:300]})
            continue

        path = _save(report, out_dir)
        paths.append(path)
        _print_summary(report)
        print(f"结果已写入: {path}")

        tasks = report["tasks"]
        rows.append({
            "model": model_name,
            "bench_total": report["bench_total"],
            "S_success": _mean([t["S_success"] for t in tasks]),
            "S_eff": _mean([t["S_eff"] for t in tasks]),
            "S_consistency": _mean([t["S_consistency"] for t in tasks]),
            "by_subject": report.get("by_subject", {}),
            "result_file": os.path.basename(path),
        })

    _print_leaderboard(rows)
    meta = {
        "judge": (config.get("judge") or {}).get("model"),
        "runs_per_task": args.runs,
        "subjects": args.subjects or "all",
        "tasks": args.tasks or "all",
        "dry_run": args.dry_run,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    cmp_path = _save_comparison(rows, meta, out_dir)
    print(f"\n对比汇总已写入: {cmp_path}")
    return 0 if any(r.get("bench_total") is not None for r in rows) else 1


def _cmd_author(argv: List[str]) -> int:
    """`author` 子命令：补全半成品题目的后三段并自检写回。

    出题模型走 config 的 model_under_test（同评测链路的 build_provider 构造，
    因此思考型出题模型也能配 max_resamples 走截断重抽）。
    """
    from lib.authoring import author_task  # 延迟导入，避免影响主链路

    ap = argparse.ArgumentParser(
        prog="lib.runner author", description="出题补全：填好前三段 → 自动补全后三段 + 双向自检")
    ap.add_argument("--config", required=True, help="配置文件路径（用 model_under_test 作为出题模型）")
    ap.add_argument("--task", required=True,
                    help="半成品题文件路径，或 test-物理06 这样的 task_id（在 tasks_dir 下查找）")
    ap.add_argument("--n-ce", type=int, default=2, help="自检用的反例份数（默认 2）")
    ap.add_argument("--max-attempts", type=int, default=3, help="自检不过时最多重写次数（默认 3）")
    ap.add_argument("--dry-run", action="store_true", help="用占位模型自检链路，不调 API")
    ap.add_argument("--no-write", action="store_true", help="只跑不写回文件（预览）")
    args = ap.parse_args(argv)

    with open(args.config, encoding="utf-8") as f:
        config = json.load(f)

    # 解析 task 路径：既接受文件路径，也接受 task_id
    path = args.task
    if not os.path.isfile(path):
        tasks_dir = config.get("tasks_dir") or os.path.join(_ROOT, "tasks")
        if not os.path.isabs(tasks_dir):
            tasks_dir = os.path.join(_ROOT, tasks_dir)
        hit = None
        for root, _d, files in os.walk(tasks_dir):
            for fn in files:
                if fn.endswith(".md") and os.path.splitext(fn)[0] == args.task:
                    hit = os.path.join(root, fn)
                    break
        if not hit:
            raise SystemExit(f"未找到题文件：{args.task}（既非路径，也未在 {tasks_dir} 下匹配到）")
        path = hit

    model = _make_provider(config["model_under_test"], args.dry_run)
    print(f"出题模型: {model.model}（{model.name}）；目标文件: {path}")

    res = author_task(path, model, n_ce=args.n_ce, max_attempts=args.max_attempts,
                      write=not args.no_write)

    print("\n==================== 补全结果 ====================")
    if res.ok:
        ce_str = ", ".join(f"{c:.3f}" for c in res.ce_scores)
        print(f"✅ {res.task_id} 通过自检（第 {res.attempts} 次）")
        print(f"   标准答案得分={res.ref_score:.3f}  反例得分=[{ce_str}]")
        print(f"   {'已写回 '+path if res.written else '未写回（--no-write）'}")
    else:
        print(f"❌ {res.task_id} 未完成：{res.reason}")
    print("=================================================")
    return 0 if res.ok else 1


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    # 子命令分发：`author` 走出题补全，其余走评测/预检
    if argv and argv[0] == "author":
        return _cmd_author(argv[1:])

    ap = argparse.ArgumentParser(description="ScoreFloor-Sci-Bench 一键评测")
    ap.add_argument("--config", required=True, help="配置文件路径（见 config.example.json）")
    ap.add_argument("--subjects", default="", help="只测这些学科，逗号分隔，如 chemistry,math")
    ap.add_argument("--tasks", default="", help="只测这些题，逗号分隔，如 test-化学05")
    ap.add_argument("--runs", type=int, default=5, help="每题重复运行次数（默认 5）")
    ap.add_argument("--concurrency", type=int, default=1, help="单题内并发跑几次（默认 1）")
    ap.add_argument("--task-concurrency", type=int, default=1, dest="task_concurrency",
                    help="同时并行跑几道题（默认 1=串行）。峰值并发请求 ≈ "
                         "task-concurrency × concurrency，别把网关打爆")
    ap.add_argument("--models", default="",
                    help="被测模型列表，逗号分隔；给多个则依次跑同一套题并出横向对比表，"
                         "覆盖 config.json 的 model_under_test.model")
    ap.add_argument("--out", default="", help="结果输出目录（默认 results/）")
    ap.add_argument("--resume", action="store_true",
                    help="逐 run 缓存续跑：复用之前跑完（出正文）的 run，只补没跑到/空答复的。"
                         "题面或裁判一变缓存自动失效")
    ap.add_argument("--cache-dir", default="", dest="cache_dir",
                    help="缓存目录（默认 .bench-cache/）")
    ap.add_argument("--dry-run", action="store_true", help="不调 API，用占位答复自检链路")
    ap.add_argument("--check", action="store_true",
                    help="只做配置预检：各发一次最小请求，确认端点/Token/模型名可用")
    ap.add_argument("--list-models", action="store_true", dest="list_models",
                    help="拉取端点实际可用的模型清单（GET /models）后退出")
    args = ap.parse_args(argv)

    with open(args.config, encoding="utf-8") as f:
        config = json.load(f)

    models = [m.strip() for m in args.models.split(",") if m.strip()]

    if args.list_models:
        return do_list_models(config)
    if args.check:
        return do_check(config, models)

    if len(models) > 1:
        return run_multi_models(config, args, models)
    if models:
        config["model_under_test"]["model"] = models[0]

    report = run_bench(config, args)
    out_dir = args.out or os.path.join(_ROOT, "results")
    path = _save(report, out_dir)
    _print_summary(report)
    print(f"\n完整结果已写入: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
