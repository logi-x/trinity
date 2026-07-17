# Logix Cornelius Usage

## Vault / Orb maintenance (preferred)

One command covers the correct nightly pipeline (FAISS → coherence+tensions → Orb export):

```bash
# Nightly (safe — does not wipe tensions)
./resources/run_vault_maintenance.sh --commit-brain

# After renames / ghost paths in the Orb
./resources/run_vault_maintenance.sh --full --commit-brain
```

| Flag | Meaning |
|------|---------|
| `--commit-brain` | If `Brain/` is dirty: commit only those paths and push (no amend / no force) |
| `--full` | Also run `bootstrap --force` before coherence (wipes then re-detects tensions) |
| `--skip-index` / `--skip-coherence` / `--skip-export` | Omit a stage |

### Trinity schedule prompt (short)

```
Run ./resources/run_vault_maintenance.sh --commit-brain in the foreground and wait until it finishes (up to ~60 minutes). Do not background it. Reply with the script's summary block (synced, notes_before/after) and any errors verbatim. This schedule is the approval gate — no extra confirmation.
```

Weekly (or when the Orb shows stale/renamed paths), use `--full` instead.

### Pipeline reference

| Step | Role |
|------|------|
| `run_index.sh` | FAISS search index (must run before tensions) |
| `bootstrap --force` | Full graph rebuild; **wipes tensions** — not for every night |
| `coherence --tensions` | Lifecycle + tension refresh |
| `export_data.py` | Writes `data.json` the Brain Orb loads |

---

## After base-image rebuilds (FAISS venv)

The search venv under `resources/local-brain-search/venv` is **inside the workspace volume**, so a new `trinity-agent-base` Python leaves a broken venv (e.g. `No module named 'faiss'`).

Self-heal is wired in three places — no manual recreate needed:

| Hook | When |
|------|------|
| `.trinity/setup.sh` | Every container start (base-image `startup.sh`) |
| `resources/local-brain-search/ensure_venv.sh` | Called by index/search/daemon/maintenance wrappers |
| Python version marker | Rebuilds when host Python ≠ `venv/.trinity-python-version` |

### Rebuild agent base image + pick it up

Do this when you changed `docker/base-image/` (Python, Claude Code, startup.sh, etc.).

```bash
cd /home/logix/trinity

# 1) Build trinity-agent-base:latest  (takes several minutes)
./scripts/deploy/build-base-image.sh

# 2) Recreate the agent container onto that image
#    (workspace volume kept — Brain/, venv, .env stay)
docker exec trinity-backend python3 -c "
import asyncio
from services.docker_service import get_agent_container
from services.agent_service.lifecycle import recreate_container_with_updated_config
name = 'logix-cornelius'
c = get_agent_container(name)
assert c, 'agent container not found'
asyncio.run(recreate_container_with_updated_config(name, c, 'system'))
print('recreated', name)
"
```

UI **Stop → Start is not enough** — Docker keeps the old image ID until the container is recreated. After recreate, `.trinity/setup.sh` rebuilds the FAISS venv if Python changed.

Verify:

```bash
docker inspect agent-logix-cornelius --format '{{.Image}} {{.Config.Image}}'
# Image should be a new digest; Config.Image usually trinity-agent-base:latest
```

