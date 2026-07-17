#!/bin/bash
# Usage-based learning management CLI wrapper
#
# Commands:
#   ./run_learning.sh status           # Show learning statistics
#   ./run_learning.sh status --json    # JSON output
#   ./run_learning.sh reset --confirm  # Reset all learned data
#   ./run_learning.sh export           # Export learning data
#   ./run_learning.sh top              # Show top notes by Q-value
#   ./run_learning.sh log read "Note"  # Manually log a read event

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$SCRIPT_DIR/ensure_venv.sh"
cd "$SCRIPT_DIR"
source venv/bin/activate
python learning.py "$@"
