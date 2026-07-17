---
title: "Runner Safety Model"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/runner"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
source_id: "docs/architecture/runner-safety-model.md"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# Runner Safety Model

Phase 1 does **not** execute repository commands, shell commands, deploy hooks, or autonomous agents. It stores metadata for later phases after explicit approval gates exist.

Future runner contract:

1. Command center remains source of truth.
2. Runners authenticate as `agent_service` or a narrower future service role.
3. Actions are records with actor, scope, command metadata, risk, and approval status.
4. High-risk actions require human approval before dispatch.
5. Execution logs stream back as immutable events and run logs.
6. Repository operations use isolated worktrees with explicit project/repository scope.
7. No runner receives broad database credentials or raw session cookies.

Repository command tables in Phase 1 are **metadata only** — planning and documentation, not executable surfaces.
