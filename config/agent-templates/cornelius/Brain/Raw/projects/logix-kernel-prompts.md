You are on the right track, but the “off” feeling is real: the repos are currently split by chronology, not by ownership.
Recommended Ownership
/home/logix/logix-kernel: make this the canonical control plane. It should own auth, users, clients, projects, repositories, memory records, workflows, runner/job records, artifacts, audit/events, and dashboard.
/home/logix/logix-intelligence: keep this as Lucy’s reasoning/runtime engine only: routing, specialists, planner, providers, loop execution. It should stop owning its own canonical projects/memory/actions over time.
/home/logix/mcp-core: currently a Lucy MCP bridge. Either fold it into logix-kernel/apps/mcp as lucy_* tools, or keep it as a thin adapter with no domain logic.
/home/logix/loopkit: keep separate as reusable agent harness/skills library. Do not let it become app state.
/home/logix/n8n-core: treat as workflow prototype/integration runtime. Migrate durable workflows into Kernel, or let Kernel trigger n8n as an external adapter.
/home/logix/logix: looks like public website/UI/marketing. Keep it out of the internal OS architecture.
Main Duplications
Memory exists in both Kernel and Lucy, but with different schemas. Kernel has Memory, links, visibility, FTS/vector fields; Lucy has memories, trust/quarantine, revocation, retrieval, hygiene, and promotion.
Agents/runs/workflows overlap with Lucy loops/actions. Kernel has Agent, AgentRun, Workflow, RunnerJob; Lucy has loop_runs, tool_calls, actions, findings, loop scoring.
MCP is duplicated: Kernel has apps/mcp wrapping the logix CLI; mcp-core wraps Lucy’s API.
Projects/repositories are duplicated: Lucy has its own project registry and repo paths; Kernel already has richer Project/Repository models.
What’s Missing
A single source of truth for project/repo/memory IDs.
A unified approval model. Lucy has good gated action logic; Kernel has the right place to persist/audit it.
A trust/quarantine model in Kernel memory. Lucy’s pending_review, origin_run_id, revoke/promote flow is valuable and should be moved or mirrored into Kernel.
A clear integration contract: Lucy should call Kernel APIs/SDK, not maintain parallel durable state.
Secrets hygiene: I saw live-looking tokens in .mcp.json; move those to env/local ignored config and rotate them.
Best Consolidation Path
Write one ADR: “Kernel is system of record; Lucy is reasoning/runtime.”
Add Kernel models/API for Finding, MemoryTrustState, originRunId, revokedAt, and action approvals.
Change Lucy to read/write projects, memory, findings, and approvals through Kernel SDK/API.
Merge MCP surfaces or namespace them clearly: logix_* for business/control-plane, lucy_* for reasoning.
Keep n8n and loopkit as adapters/libraries, not competing platforms.
The architecture should become: Kernel holds the business OS; Lucy thinks and proposes/executes gated work; MCP/CLI/n8n/loopkit are interfaces around that core.

Pending / not wired yet:

┌─────┬─────────────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬───────────────┐
│  #  │           Gap           │                                                                                           State                                                                                           │     Size      │
├─────┼─────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────┤
│ 1   │ Items → Invoice         │ CampaignItem line items + dual-currency pricing exist on the backend, but nothing converts them to an Invoice — no button, no endpoint wiring. Meant to mirror the proposal→invoice path. │ Small–medium  │
├─────┼─────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────┤
│ 2   │ Plan 2 — channel engine │ Entirely unbuilt. No Channel/MetricSnapshot tables, no BrandKit XOR, no economics read model. Net-new domain→api→sdk→web.                                                                 │ Large         │
├─────┼─────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────┤
│ 3   │ Matrix counts campaigns │ Campaign.producerDepartmentId exists in schema but the matrix view is projects-only, and no departments are seeded.                                                                       │ Small         │
├─────┼─────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────┤
│ 4   │ Portal exposure         │ Client portal surfaces nothing for campaign files/expenses.                                                                                                                               │ Medium        │
├─────┼─────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────┤
│ 5   │ Bug: createProject 500  │ Unguarded findUnique when clientId omitted. Pre-existing, separate from campaigns.                                                                                                        │ Tiny (3-line) │
└─────┴─────────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴───────────────┘