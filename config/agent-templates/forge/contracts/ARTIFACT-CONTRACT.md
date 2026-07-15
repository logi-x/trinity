# Logix Artifact Contract

Every artifact passed between agents must use this contract. An artifact without the required metadata is a draft and must not be treated as approved input.

## Required frontmatter

```yaml
---
artifact_id: "<task-id>-<stage>-r1"
task_id: "<stable task or engagement id>"
engagement: "<client or internal initiative>"
producer: "<deployed agent name>"
stage: "research|verification|strategy|concept|deliverable|operations"
status: "draft|verified|rejected|approved|superseded"
created_at: "<ISO-8601 timestamp with timezone>"
supersedes: null
verification: null
inputs:
  - "<artifact id or Cornelius record id>"
handoff_to:
  - "<deployed agent name>"
---
```

Revisions increment `rN`, keep the same `task_id`, and set `supersedes` to the prior `artifact_id`. Never overwrite an existing revision.

## Required body sections

1. `## Summary`
2. `## Claims ledger`
3. `## Assumptions`
4. `## Open questions`
5. `## Actions and handoff`

The claims ledger uses:

| ID | Claim | Kind | Evidence | As-of date | Confidence | Verification |
|---|---|---|---|---|---|---|
| C-001 | Exact, atomic claim | fact / inference / recommendation / internal | URL, artifact ID, or Cornelius record | YYYY-MM-DD | high / medium / low | unverified / verified / disputed |

Rules:

- One independently checkable assertion per claim row.
- Facts require evidence and an as-of date. A bibliography alone is insufficient.
- Inferences and recommendations must cite the fact claim IDs they depend on.
- Internal facts must identify the Cornelius record or be marked `unverified`.
- Negative or exclusivity claims such as “no competitor,” “only provider,” or “mandatory” require direct evidence; otherwise rewrite them as a bounded observation.
- A downstream agent may reformat verified facts but may not silently upgrade an inference or assumption into a fact.
- Sentinel never edits the producer's artifact. It creates a separate `verification` artifact naming the exact `artifact_id` and revision reviewed. Downstream agents may treat the input as verified only when that report has verdict `pass` and no blocking findings.
- Set `verification` to the Sentinel verification artifact ID in a later revision or approval record. Human approval is still required for `approved`.
- Only approved facts, decisions, and final artifacts should be promoted into Cornelius.

## Handoff states

```text
draft -> verified -> approved
  |         |
  +-> rejected
  +-> superseded
```

- `draft`: producer considers the artifact complete enough for review.
- `verified`: a Sentinel verification artifact found adequate support and no blocking contradictions.
- `rejected`: blocking evidence or integrity problems remain.
- `approved`: a human or explicitly authorized owner accepted it.
- `superseded`: a later revision replaces it.

## File naming

Use `{task-id}-{stage}-r{N}.md`. Dates belong in metadata, not identity. Store artifacts under the agent's documented `shared-out` stage directory.
