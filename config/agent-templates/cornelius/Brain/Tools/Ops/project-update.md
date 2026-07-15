---
title: "Operation - project update"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["ops", "project"]
category: "tools/ops"
source: "generated"
source_id: "Tools/Ops/project-update.md"
---

# Operation - project update

Use when a task changes project knowledge, project status, architecture, operations, or roadmap.

## Steps

1. Open the project hub in `Entities/Projects/`.
2. Follow its `LLM Entry Points` section to the project-local page under `Projects/`.
3. If updating current status, first follow [[Tools/Ops/verify-current]] and record the new `verified` date on the project hub.
4. Update the narrowest durable page that owns the fact.
5. If the change is a decision, update [[Decisions/Decision-Log]] and add or update a decision note.
6. If the change creates work, update [[Actions/Action-Tracker]] and add or update an action note.
7. If the update came from a source/session, create or update a summary in [[Summaries]].
8. Append to [[Log]] when the update is durable and material.
9. Run `python3 Tools/Scripts/vault_lint.py`.

## Placement Rule

- Entity hub: what the project is, status, owners, and entry points.
- Project-local note: detailed documentation, architecture, working context.
- Concept page: reusable idea not owned by one project.
- Raw: immutable source.
- Summary: processed evidence from one source.
