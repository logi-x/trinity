---
title: "Memory System"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/memory"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
source_id: "docs/architecture/memory-system.md"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# Memory System

One `Memory` table with a `kind` enum — shared search, links, visibility, and entity associations for decisions, ADRs, incidents, runbooks, client/project notes, agent context, proposal notes, repository notes, loop summaries, episodes, and general notes.

| Field | Role |
| ----- | ---- |
| `title`, `body`, `summary` | Searchable narrative |
| `data` | Kind-specific structure (e.g. ADR status/context/decision/consequences) |
| `clientId`, `projectId`, `agentId`, `repositoryId` | Entity anchors |
| `visibility` | `internal` or client-shared |
| `searchVector` | PostgreSQL FTS (trigger-maintained) |
| `embedding` | pgvector `vector(1536)` for future embedding jobs |

`MemoryLink` connects memories to other memories or arbitrary entity references. Phase 1 includes an embedding stub worker queue but does not call an embedding provider.

See [[Projects/Logix/KERNEL/docs/decisions/ADR 0002 — Single Memory Table|ADR 0002]].
