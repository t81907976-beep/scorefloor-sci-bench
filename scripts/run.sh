#!/usr/bin/env bash
#
# ScoreFloor-Sci-Bench 一键评测入口
#
# 用法：
#   1. 复制配置：cp config.example.json config.json，填入你的 base_url / 模型名
#   2. 导出密钥：在项目根建 .env 写入 MODEL_API_KEY= / JUDGE_API_KEY=，或直接 export
#   3. 预检：    ./scripts/run.sh --check
#      看模型：  ./scripts/run.sh --list-models
#      跑全部：  ./scripts/run.sh
#      跑单学科：./scripts/run.sh --subjects chemistry
#      跑单题：  ./scripts/run.sh --tasks test-化学05 --runs 5
#      多模型横评：./scripts/run.sh --models "model-a,model-b" --subjects chemistry --runs 5
#      自检链路：./scripts/run.sh --dry-run
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

CONFIG="${CONFIG:-config.json}"
if [[ ! -f "$CONFIG" ]]; then
  echo "找不到配置文件 $CONFIG"
  echo "请先: cp config.example.json config.json  并填入 base_url / 模型名 / 密钥环境变量"
  exit 1
fi

PY="${PYTHON:-python3}"
exec "$PY" -m lib.runner --config "$CONFIG" "$@"
