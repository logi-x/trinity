---
title: "EXP-220: DEPLOYMENT BLOCKER — ask_ai_conversations.deleted_at column missing migration"
linear_id: "EXP-220"
agent_fp: "auto"
date: "2026-05-30"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, migration, ai, blocker, project/experts]
category: "bug"
source: "automation"
---

# EXP-220: DEPLOYMENT BLOCKER — deleted_at migration missing

**Linear:** [EXP-220](https://linear.app/experts/issue/EXP-220) | **Status:** Open — **DEPLOYMENT BLOCKER**

## Summary
The `deleted_at` column on `ask_ai_conversations` is referenced in query code but was never added via a Prisma migration. AI conversation continuation and history retrieval are broken. Any deployment that applies pending migrations will succeed at the migration step but fail at runtime when the column is queried.

## Impact
- AI conversation continuation: broken (queries `deleted_at` in WHERE clause)
- AI conversation history: broken (soft-delete filter uses `deleted_at`)
- Next deploy: will not break at migrate step, but all affected endpoints will 500 at first query

## Fix Needed
Add a new (forward-only) migration:
```sql
-- Migration: add_ask_ai_conversations_deleted_at
ALTER TABLE ask_ai_conversations ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP(3);
```

**Do NOT modify any already-applied migration** — doing so causes P3005/P3006 checksum drift (see 2026-05-28 decision log entry on migration invariants).

## Repro
1. Run any endpoint that queries `ask_ai_conversations` with a `deleted_at` filter
2. Observe Prisma error: column `ask_ai_conversations.deleted_at` does not exist

## Related
- EXP-221 — AI routes missing try/catch (open)
- EXP-222 — loadConversation race (open)
- 2026-05-28 decision log: applied migrations must never be modified

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
