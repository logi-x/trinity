# Sequential Agent Loops

Run the same task against one agent repeatedly, in order, with a bounded run count — for example "process the next backlog item" × 20. Start a loop once, get back a `loop_id`, and disconnect: the loop runs server-side, dispatching each iteration through the standard execution pipeline.

Loops are the sequential counterpart to [Fan-Out](fan-out.md) (parallel batch) and a single chat turn (one-shot).

## Concepts

- **Loop** — A server-managed sequence of up to `max_runs` task executions against one agent. Iterations run strictly one at a time, in order.
- **Message Template** — The task message, re-rendered each iteration. Supports two placeholders:
  - `{{run}}` — the 1-indexed run number
  - `{{previous_response}}` — the trailing 2,000 characters of the previous iteration's response (empty on run 1)
- **Fixed mode** — No stop signal set: the loop runs exactly `max_runs` iterations.
- **Until mode** — A `stop_signal` is set: after each iteration, Trinity checks whether the agent's response contains the stop signal as a plain substring. On match, the loop ends early with reason `stop signal matched`. A recommended sentinel is `[[DONE]]` — tell the agent to emit it when the work is finished.
- **Cooperative stop** — Stopping a loop never kills the in-flight iteration. The current run finishes, then the loop exits with reason `stopped by user`.

## How It Works

1. Open an agent's detail page and select the **Loops** tab.
2. Click **Run Loop** (the agent must be running — the button is disabled otherwise).
3. Fill in the form:
   - **Message template** (required) — e.g. `Process item {{run}}. Previous result: {{previous_response}}`
   - **Max runs** (required, 1–100)
   - **Stop signal** (optional) — substring that ends the loop early
   - **Delay between runs (seconds)** (0–3600)
   - **Timeout per run (seconds)** (10–7200; defaults to the agent's execution timeout)
   - **Model** — per-loop model override (defaults to the agent default)
   - **Allowed tools** — restrict the agent's tools for every iteration, or leave **All Tools (Unrestricted)**
4. Click **Start Loop**. The loop appears in the list below with a live status badge and a **Run N / M** progress counter.
5. Click a loop row to expand it: a per-run table shows each iteration's status, cost, duration, and a response preview, and the **Last response** is rendered as markdown below the table.
6. Click **Stop** on an active loop to request a graceful stop. The badge shows the current iteration finishing, then the loop ends with reason `stopped by user`.

The panel updates in real time via WebSocket events as each run completes, with a periodic backstop refresh while a loop is active.

### Loop Lifecycle

| Status | Meaning |
|--------|---------|
| `queued` / `running` | Loop active; iterations dispatching |
| `completed` | Reached max runs, or the stop signal matched |
| `stopped` | Stopped by a user; the in-flight iteration finished first |
| `failed` | An iteration failed (task error or exception) — the loop aborts at that iteration |
| `interrupted` | The backend restarted mid-loop; loops do **not** auto-resume |

### Observability

Every iteration is a normal execution: it creates its own row with `triggered_by: "loop"` and the parent `loop_id`, visible on the Executions page and per-execution detail view. In analytics timeline views (the agent's Overview tab and execution charts), loop executions appear as their own **Loops** category with a distinct color — they are not folded into Scheduled.

## For Agents

Agents (and scripts) start loops via MCP tools or REST. The permission model matches `chat_with_agent`: owner, admin, or shared access on the target agent; agent-scoped MCP keys need an explicit permission grant.

### MCP Tools

| Tool | Description |
|------|-------------|
| `run_agent_loop` | Start a loop; returns `loop_id` immediately. `agent_name` is required for user-scoped keys; agent-scoped keys default to the bound agent |
| `get_loop_status` | Loop status plus per-run summaries (run number, execution id, status, response preview, cost, duration) and the last full response |
| `stop_loop` | Graceful stop; returns `stopping` (runner signaled) or `already_done` (loop already terminal) |

```typescript
mcp__trinity__run_agent_loop({
  agent_name: "my-agent",
  message: "Process the next backlog item ({{run}} of 20). Reply [[DONE]] if the backlog is empty.",
  max_runs: 20,
  stop_signal: "[[DONE]]",
  delay_seconds: 30
})
// → { success: true, loop_id: "loop_...", status: "queued", ... }
```

### REST API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/agents/{name}/loops` | POST | Start a loop; returns 202 with `{loop_id, status, agent_name, max_runs}` |
| `/api/agents/{name}/loops` | GET | List the agent's loops, most recent first (`?status=`, `?limit=` 1–200, default 50) |
| `/api/loops/{loop_id}` | GET | Status, per-run summaries, last full response (404 unknown; 403 if the caller is neither the initiator nor has agent access) |
| `/api/loops/{loop_id}/stop` | POST | Graceful stop → `{status: "stopping" \| "already_done"}` |

**API Endpoints**: See [Backend API Docs](http://localhost:8000/docs) for full schemas.

```bash
curl -X POST http://localhost:8000/api/agents/my-agent/loops \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Process item {{run}}. Previous result: {{previous_response}}",
    "max_runs": 10,
    "stop_signal": "[[DONE]]",
    "delay_seconds": 5
  }'
```

### Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `message` | — (required) | 1–100,000 chars | Template; supports `{{run}}` and `{{previous_response}}` |
| `max_runs` | — (required) | 1–100 | Hard ceiling on iterations |
| `stop_signal` | none (fixed mode) | ≤200 chars | Substring that ends the loop early; whitespace-stripped, blank = fixed mode |
| `delay_seconds` | 0 | 0–3600 | Pause between iterations |
| `timeout_per_run` | agent's execution timeout | 10–7200 | Per-iteration timeout in seconds |
| `model` | agent default | — | Model override applied to every iteration |
| `allowed_tools` | unrestricted | — | Tool restrictions applied to every iteration |

## Limitations

- **One agent, sequential** — A loop targets a single agent and never runs iterations in parallel. For parallel batches, use [Fan-Out](fan-out.md).
- **Shared capacity** — Each iteration goes through the agent's normal capacity admission and counts against its `max_parallel_tasks` budget alongside chat, schedules, and other traffic.
- **Fail-fast** — Any failed iteration ends the loop with status `failed`; remaining runs are skipped.
- **No resume after restart** — A backend restart marks in-flight loops `interrupted`. They do not auto-resume; start a new loop.
- **Stop is not instant** — The in-flight iteration always finishes; only subsequent iterations are skipped.
- **Bounded inputs** — `max_runs` is capped at 100, delay at 1 hour, and per-run timeout at 2 hours.

## See Also

- [Fan-Out](fan-out.md) — Parallel batch counterpart
- [Scheduling](scheduling.md) — Cron-based recurring tasks
- [Executions](../operations/executions.md) — Where each loop iteration appears
- [Agent Configuration](../agents/agent-configuration.md) — Execution timeout and parallel task limits
