#!/bin/bash
# Runs on every container start (base-image startup.sh).
# Rebuilds the FAISS/search venv when the agent base image Python changes.
set -euo pipefail
cd /home/developer
if [[ -x resources/local-brain-search/ensure_venv.sh ]]; then
  bash resources/local-brain-search/ensure_venv.sh
fi
