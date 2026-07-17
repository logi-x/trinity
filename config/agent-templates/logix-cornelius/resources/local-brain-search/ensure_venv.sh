#!/bin/bash
# Recreate the local-brain-search venv when missing, broken, or built for a
# different Python (typical after Trinity base-image rebuilds).
#
# Safe to call often: no-op when venv python matches system + faiss imports.
# Usage:
#   ./ensure_venv.sh
#   source ./ensure_venv.sh && activate   # optional: leave VENV_DIR set

set -euo pipefail

LBS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${LBS_DIR}/venv"
REQ="${LBS_DIR}/requirements.txt"
MARKER="${VENV_DIR}/.trinity-python-version"
HOST_PY="$(python3 -c 'import sys; print("%d.%d.%d" % sys.version_info[:3])')"

venv_ok() {
  [[ -x "${VENV_DIR}/bin/python" ]] || return 1
  [[ -f "$MARKER" ]] || return 1
  [[ "$(cat "$MARKER")" == "$HOST_PY" ]] || return 1
  "${VENV_DIR}/bin/python" -c "import faiss" >/dev/null 2>&1
}

if venv_ok; then
  exit 0
fi

echo "[ensure_venv] recreating local-brain-search venv for Python ${HOST_PY}…" >&2
rm -rf "$VENV_DIR"
python3 -m venv "$VENV_DIR"
"${VENV_DIR}/bin/pip" install -U pip wheel
"${VENV_DIR}/bin/pip" install -r "$REQ"
"${VENV_DIR}/bin/python" -c "import faiss"
echo "$HOST_PY" > "$MARKER"
echo "[ensure_venv] ready (${HOST_PY})" >&2
