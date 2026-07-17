#!/bin/bash
# Brain Dependency Graph - CLI Wrapper
#
# Usage:
#   ./run_brain_graph.sh bootstrap [--force]
#   ./run_brain_graph.sh status [--json]
#   ./run_brain_graph.sh inspect "Note Name" [--json]
#   ./run_brain_graph.sh propagate "Note Name" [--magnitude 0.8] [--json]
#   ./run_brain_graph.sh lifecycle [--json]
#   ./run_brain_graph.sh tensions [--similarity 0.75] [--divergence 0.3] [--json]
#   ./run_brain_graph.sh coherence [--days 7] [--tensions] [--json]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LBS_DIR="$SCRIPT_DIR/../local-brain-search"
bash "$LBS_DIR/ensure_venv.sh"
source "$LBS_DIR/venv/bin/activate"
cd "$SCRIPT_DIR"
python cli.py "$@"
