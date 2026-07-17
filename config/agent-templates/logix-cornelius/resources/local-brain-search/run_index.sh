#!/bin/bash
# Wrapper script for re-indexing the Brain
# Usage: ./run_index.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$SCRIPT_DIR/ensure_venv.sh"
"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/index_brain.py" "$@"
