#!/bin/bash
# Trinity Integration Tests
# Requires the full Docker stack to be running (./scripts/deploy/start.sh).
# Excluded from run-smoke.sh (which has a ~30s, no-Docker contract).
#
# Includes:
#   tests/security/      — Redis network isolation + ACL enforcement (#589)
#   tests/integration/   — webhook rate-limit regression (#589) and others

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
source .venv/bin/activate
# Pull TRINITY_TEST_PASSWORD / REDIS_BACKEND_PASSWORD from project .env.
source "$SCRIPT_DIR/setup-env.sh"

echo "========================================="
echo "  TRINITY INTEGRATION TESTS"
echo "  Requires: live Docker stack"
echo "========================================="
echo ""

time python -m pytest -m integration -v --tb=short "$@"
