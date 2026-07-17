#!/bin/bash
# Vault + Orb maintenance pipeline for Cornelius.
#
# Default (nightly-safe): FAISS index → coherence+tensions → Orb export.
# Does NOT force-bootstrap (that wipes tensions); use --full after renames
# or when the Orb shows ghost/stale paths.
#
# Usage (from agent home /home/developer):
#   ./resources/run_vault_maintenance.sh
#   ./resources/run_vault_maintenance.sh --full
#   ./resources/run_vault_maintenance.sh --skip-index
#   ./resources/run_vault_maintenance.sh --commit-brain
#
# Exit codes: 0 ok, 1 error, 2 skipped (index already running).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DO_INDEX=1
DO_FULL=0
DO_COMMIT=0
DO_COHERENCE=1
DO_EXPORT=1

usage() {
  sed -n '2,16p' "$0" | sed 's/^# \?//'
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --full) DO_FULL=1; shift ;;
    --skip-index) DO_INDEX=0; shift ;;
    --commit-brain) DO_COMMIT=1; shift ;;
    --skip-coherence) DO_COHERENCE=0; shift ;;
    --skip-export) DO_EXPORT=0; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

DATE="$(date -u +%Y-%m-%d)"
NOTES_BEFORE=""
NOTES_AFTER=""
SYNCED="skipped"

log() { printf '[vault-maintenance] %s\n' "$*"; }

count_notes() {
  find Brain -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' '
}

if pgrep -f 'index_brain|run_index\.sh' >/dev/null 2>&1; then
  log "ERROR: an index rebuild is already running — refusing to start"
  exit 2
fi

NOTES_BEFORE="$(count_notes)"
log "notes on disk before: ${NOTES_BEFORE}"

# Rebuild FAISS venv if base-image Python changed (also on container start via .trinity/setup.sh)
bash "$ROOT/resources/local-brain-search/ensure_venv.sh"

# --- optional Brain/ commit (schedule can enable with --commit-brain) ---
if [[ "$DO_COMMIT" -eq 1 ]]; then
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    # Only stage Brain/ paths; never amend, never force-push.
    if git status --porcelain -- Brain/ | grep -q .; then
      git add -- Brain/
      git commit -m "chore(vault): nightly sync ${DATE}"
      BRANCH="$(git rev-parse --abbrev-ref HEAD)"
      git push -u origin "HEAD:refs/heads/${BRANCH}"
      SYNCED="synced"
      log "committed and pushed Brain/ on ${BRANCH}"
    else
      SYNCED="skipped"
      log "Brain/ clean — no commit"
    fi
  else
    log "WARN: not a git checkout — skipping --commit-brain"
  fi
fi

# --- FAISS (must precede tensions / coherence --tensions) ---
if [[ "$DO_INDEX" -eq 1 ]]; then
  log "running FAISS index (foreground)…"
  ./resources/local-brain-search/run_index.sh
  log "FAISS index done"
fi

# --- Brain Dependency Graph ---
if [[ "$DO_FULL" -eq 1 ]]; then
  log "FULL: bootstrap --force (wipes tensions; rebuilds classifications)…"
  ./resources/brain-graph/run_brain_graph.sh bootstrap --force
fi

if [[ "$DO_COHERENCE" -eq 1 ]]; then
  log "coherence --tensions…"
  ./resources/brain-graph/run_brain_graph.sh coherence --tensions
  log "coherence done"
fi

# --- Orb payload ---
if [[ "$DO_EXPORT" -eq 1 ]]; then
  log "exporting Orb data.json…"
  python3 resources/agent-visualization/export_data.py
  log "export done"
fi

NOTES_AFTER="$(count_notes)"
LOG_LINE="[${DATE}] maintenance | nightly index refresh - ${NOTES_AFTER} notes indexed (before=${NOTES_BEFORE}, brain_git=${SYNCED})"
mkdir -p Brain
printf '%s\n' "$LOG_LINE" >> Brain/Log.md
log "$LOG_LINE"

# Machine-readable summary for schedule replies
cat <<EOF
---
synced: ${SYNCED}
notes_before: ${NOTES_BEFORE}
notes_after: ${NOTES_AFTER}
full_bootstrap: ${DO_FULL}
index: ${DO_INDEX}
coherence: ${DO_COHERENCE}
export: ${DO_EXPORT}
EOF
