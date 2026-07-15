---
title: "Phases and Tracks"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/roadmap"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# Phases and Tracks

High-level roadmap for Logix Command Center. Implementation checklists and slice specs stay in the **repo** (see [[Projects/Logix/KERNEL/docs/meta/repo-doc-inventory|repo doc inventory]]).

| Phase | Focus | Status |
| ----- | ----- | ------ |
| **1** | Command center core (web, API, domains, portal, vault, finance UI foundation) | Shipped in branch |
| **1.1** | Finance domain redesign (revenue engine, model) | Planned |
| **1.2** | (see repo `docs/plans/phase-1.2.md`) | Planned |
| **2** | CLI, SDK hardening, protocol/MCP surface | Shipped in branch |
| **2.1** | CLI parity over SDK, MCP slice 3, dashboard attention queue, PAT self-service | Active plan track |
| **3** | Agent runtime, runner, approval gates | Planned |
| **4** | External integrations | Planned |
| **5** | Autopilot loops | Planned |

## Phase 2.1 goals (summary)

Close daily-usability gaps without finance (1.1) or autonomous execution (3):

- Thin CLI handlers for remaining `@logix/sdk` domains (clients, projects, invoices, requests, agents, vault, activity, dashboard).
- MCP registry aligned with CLI; tighten Tier A/B exposure.
- Dashboard as a real **attention queue**; PAT management in Settings.
- Fix local DX: API vs web `baseUrl` precedence and port documentation (`3060` web / `3061` API).

**Canonical working plan:** `docs/plans/2026-07-05-command-center-maturity.md` in repo.

## Architecture guardrails (all slices)

- Business logic in `apps/api` services; web uses `@logix/sdk` only (no `@logix/db` in web).
- Permissions via `@logix/permissions`; CLI/MCP never widen PAT scopes.
- Mutations record domain events + audit via `@logix/events`.
- No repo patch/commit/push/deploy from CLI/MCP until Phase 3 runner model.
