#!/usr/bin/env bash
set -euo pipefail

# ---- Resolve .env in parent directory ----
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_PATH="${SCRIPT_DIR}/../.env"

# ---- Load .env if exists ----
if [[ -f "$ENV_PATH" ]]; then
  # export only KEY=VALUE pairs, trimming whitespace
  while IFS='=' read -r key value; do
    [[ -z "$key" ]] && continue
    [[ "${key:0:1}" == "#" ]] && continue
    [[ -z "$value" ]] && continue

    key="$(echo "$key" | xargs)"
    value="$(echo "$value" | xargs)"

    export "$key=$value"
  done < "$ENV_PATH"
fi

# ---- Default values ----
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8999}"

# ---- Minimal log ----
echo "[prod.sh] HOST=${HOST} PORT=${PORT}"

# ---- Activate venv ----
if [[ -d "${SCRIPT_DIR}/../.venv" ]]; then
  source "${SCRIPT_DIR}/../.venv/bin/activate"
fi

# ---- Run ----
uvicorn app.main:app \
  --host "${HOST}" \
  --port "${PORT}" \
  --log-level warning \
  --no-access-log
