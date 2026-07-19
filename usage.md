Don’t delete the existing `howa` first. Trinity soft-deletes agents and reserves their names, so immediate recreation under `howa` would fail. Use a canary-and-rename swap instead.

### 1. Create the PHP-enabled canary

```bash
/home/logix/.venv/bin/python - <<'PY'
import json
from trinity_cli.client import TrinityClient

client = TrinityClient()

result = client.post("/api/agents", json={
    "name": "howa-php84",
    "template": "github:logi-x/howa",
    "source_branch": "main",
    "source_mode": True,
    "type": "project",
    "base_image": "trinity-agent-base:howa-php84-0.8.2",
    "resources": {
        "cpu": "4",
        "memory": "8g",
    },
})

print(json.dumps(result, indent=2))
PY
```

This raw REST call is necessary because the current MCP and CLI create commands don’t expose `base_image`.

### 2. Verify the canary

```bash
trinity agents get howa-php84

docker inspect agent-howa-php84 \
  --format '{{.Config.Image}} {{.State.Status}}'

docker exec agent-howa-php84 \
  sh -lc 'php --version && composer --version'
```

Install dependencies and run both Laravel suites:

```bash
docker exec -u developer agent-howa-php84 bash -lc '
set -euo pipefail

for app in client admin; do
  cd "/home/developer/apps/$app"
  composer install --no-interaction --prefer-dist
  composer check-platform-reqs
  php artisan test
done
'
```

Only continue if the agent is healthy and the results are acceptable.

### 3. Swap the names

Renaming preserves the old agent as an immediate rollback:

```bash
trinity agents rename howa howa-pre-php84
trinity agents rename howa-php84 howa
trinity agents start howa
```

If the second rename fails, restore immediately:

```bash
trinity agents rename howa-pre-php84 howa
trinity agents start howa
```

### 4. Restore canonical metadata

The old agent’s rename will move Atlas’s permission edge to `howa-pre-php84`, so reset it explicitly:

```bash
/home/logix/.venv/bin/python - <<'PY'
import json
from trinity_cli.client import TrinityClient

client = TrinityClient()

tags = client.put(
    "/api/agents/howa/tags",
    json={"tags": ["howa", "project"]},
)

permissions = client.put(
    "/api/agents/atlas/permissions",
    json={"permitted_agents": ["howa", "experts", "cornelius"]},
)

subscription = client.put(
    "/api/subscriptions/agents/howa"
    "?subscription_name=claude-max-new"
)

print(json.dumps({
    "tags": tags,
    "permissions": permissions,
    "subscription": subscription,
}, indent=2))
PY
```

### 5. Final verification

```bash
trinity agents get howa

docker inspect agent-howa \
  --format 'image={{.Config.Image}} status={{.State.Status}}'

docker exec agent-howa \
  sh -lc 'php --version && composer --version'
```

Then run HoWA’s `/status` and one Atlas → HoWA smoke.

Keep `howa-pre-php84` stopped until the new agent has passed validation. It provides a straightforward rollback without depending on Trinity’s soft-delete recovery.