# Logix Cornelius Usage

## Rebuild the dependency graph

```bash
# 1) Rebuild the dependency graph (drops/repairs renamed paths)
./resources/brain-graph/run_brain_graph.sh bootstrap --force

# 2) Re-export the Orb payload
python3 resources/agent-visualization/export_data.py

# 3) Optional: FAISS for search (not required for Orb pixels)
./resources/local-brain-search/run_index.sh
```

Expected. `bootstrap --force` **rebuilds the graph from scratch** and resets enrichments to:

```python
"tensions": []
```

Tensions are **not** part of classify/bootstrap. They’re a separate pass (`detect_tensions`) that writes into that list afterward. Your export then correctly showed **0** tensions.

### Restore them

```bash
# Detect tensions again (needs FAISS/embeddings from local-brain-search)
./resources/brain-graph/run_brain_graph.sh tensions

# or full sweep including tensions:
./resources/brain-graph/run_brain_graph.sh coherence --tensions

# then refresh the Orb payload
python3 resources/agent-visualization/export_data.py
```

Hard-refresh the Orb after that.

### Pipeline (for next time)

| Step | What it does to tensions |
|------|---------------------------|
| `bootstrap [--force]` | **Wipes** them |
| `tensions` / `coherence --tensions` | **Repopulates** them |
| `export_data.py` | Copies whatever is in enrichments into the Orb |
| `run_index.sh` | Search only — unrelated |

So: force-bootstrap fixed the renamed meeting paths; you still need a tensions (or coherence) run before the Orb will show contradiction edges again.

---

## Pipeline (for next time)

```bash
./resources/brain-graph/run_brain_graph.sh bootstrap --force
./resources/brain-graph/run_brain_graph.sh tensions
./resources/brain-graph/run_brain_graph.sh coherence --tensions
python3 resources/agent-visualization/export_data.py
./resources/local-brain-search/run_index.sh
```

---

For a normal restart:

```sh
docker restart agent-logix-cornelius
```

But that will **not** load the Pull-button fix; an existing container keeps its old image.

To activate the change, wait until Cornelius is idle, then rebuild and recreate it:

```sh
cd /home/logix/trinity
./scripts/deploy/build-base-image.sh
```

Then recreate the agent container through Trinity’s lifecycle code:

```sh
docker exec trinity-backend sh -lc '
cd /app
PYTHONPATH=/app/src/backend python3 - <<'"'"'PY'"'"'
import asyncio
from services.docker_service import get_agent_container
from services.agent_service.lifecycle import recreate_container_with_updated_config

name = "logix-cornelius"
container = get_agent_container(name)
if not container:
    raise SystemExit(f"Container for {name} was not found")

asyncio.run(recreate_container_with_updated_config(name, container, "system"))
PY
'
```

This interrupts active work but preserves `/home/developer` and its workspace volume.