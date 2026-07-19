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

### Slash command (on-demand)

```
/vault-maintenance
/vault-maintenance --commit-brain
/vault-maintenance --full --commit-brain
```

Defined at `.claude/commands/vault-maintenance.md` (declared in `template.yaml` → `commands`).

### Trinity schedule prompt (nightly)

Paste as the Scheduled Task message (or keep the live DB copy in sync):

```
Scheduled nightly vault maintenance (unattended — no approval gates apply; this schedule IS the approval). Scope: Brain/ git sync + Orb-safe pipeline (FAISS → coherence+tensions → Orb export). Do NOT use --full (that wipes tensions).

1. Run `/vault-maintenance --commit-brain` in the FOREGROUND and wait until it finishes before ending your turn. Do not background it; do not end early. It can take ~20–45 minutes; your execution window is 60 minutes.
   Equivalent shell: `./resources/run_vault_maintenance.sh --commit-brain`
2. Do NOT run `/refresh-index`, `bootstrap`, `bootstrap --force`, or invent alternate steps. The command already:
   - If Brain/ is dirty: commits ONLY Brain/ with message `chore(vault): nightly sync <YYYY-MM-DD>` and pushes the current branch (no force, never amend). If clean, skips.
   - Stops if an index rebuild is already running.
   - Rebuilds FAISS, runs `coherence --tensions` (does not wipe tensions), exports Orb `data.json`, appends ONE line to Brain/Log.md (that line is not committed; it rides along in a later sync).
3. Reply with the script's summary block verbatim: `synced` / skipped, `notes_before` / `notes_after`, and any errors.

Weekly or after renames / ghost Orb paths (manual or a separate schedule): `/vault-maintenance --full --commit-brain`.
```


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

# 2) Recreate agent container(s) onto that image
#    (workspace volumes kept — Brain/, venv, .env stay)

# Single agent
docker exec trinity-backend python3 -c "
import asyncio
from services.docker_service import get_agent_container
from services.agent_service.lifecycle import recreate_container_with_updated_config
name = 'logix-system'
c = get_agent_container(name)
assert c, 'agent container not found'
asyncio.run(recreate_container_with_updated_config(name, c, 'system'))
print('recreated', name)
"

# Multiple agents
docker exec trinity-backend python3 -c "
import asyncio
from services.docker_service import get_agent_container
from services.agent_service.lifecycle import recreate_container_with_updated_config
names = [
    'logix-system',
    'cornelius',
    'experts',
    'howa',
    'atlas',
]
async def main():
    for name in names:
        c = get_agent_container(name)
        if not c:
            print('skip (not found):', name)
            continue
        await recreate_container_with_updated_config(name, c, 'system')
        print('recreated', name)
asyncio.run(main())
"
```

UI **Stop → Start is not enough** — Docker keeps the old image ID until the container is recreated. After recreate, `.trinity/setup.sh` rebuilds the FAISS venv if Python changed.

Verify:

```bash
docker inspect agent-logix-cornelius --format '{{.Image}} {{.Config.Image}}'
# Image should be a new digest; Config.Image usually trinity-agent-base:latest
```

