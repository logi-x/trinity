---
title: "EXP-252: persistAskAiExchange soft-delete re-check has no FOR UPDATE lock — TOCTOU race"
linear_id: "EXP-252"
agent_fp: "5f9fdc5505e8"
date: "2026-06-01"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, concurrency, ask-ai, project/experts]
category: "bug"
source: "automation"
---

# EXP-252: persistAskAiExchange TOCTOU race on soft-deleted conversation

**Linear:** [EXP-252](https://linear.app/experts/issue/EXP-252/bug-persistaskaiexchange-soft-delete-re-check-has-no-for-update-lock) | **Status:** Backlog

## Summary

PR #705 (EXP-239) wrapped `verifyConversation` + `persistAskAiExchange` in a `$transaction` with a `deleted_at IS NULL` re-check to prevent writes to soft-deleted conversations. However, the re-check uses a plain `SELECT` (Prisma `findFirst`) without a `SELECT … FOR UPDATE` row lock. Two concurrent requests to the same conversation can both pass the re-check simultaneously, then both proceed to insert messages into a conversation that was concurrently soft-deleted by a third request.

## File

`apps/experts-app/src/lib/ask-ai/ask-ai-exchange.service.ts` — `persistAskAiExchange`

## Race

```
Request A: BEGIN; SELECT * FROM ask_ai_conversations WHERE id=X AND deleted_at IS NULL → found
Request B: BEGIN; SELECT * FROM ask_ai_conversations WHERE id=X AND deleted_at IS NULL → found
Request C:                UPDATE ask_ai_conversations SET deleted_at=NOW() WHERE id=X
Request A:               INSERT INTO ask_ai_messages ... COMMIT  ← writes to deleted conversation
Request B:               INSERT INTO ask_ai_messages ... COMMIT  ← writes to deleted conversation
```

## Fix

Replace the Prisma `findFirst` re-check with a raw `SELECT … FOR UPDATE` query inside the `$transaction`, or use Prisma's interactive transactions to lock the row before checking `deleted_at`.

## Related

- EXP-239 — original verify-then-persist non-atomic (resolved PR #705)
- EXP-220 — `deleted_at` migration (resolved PR #679)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
