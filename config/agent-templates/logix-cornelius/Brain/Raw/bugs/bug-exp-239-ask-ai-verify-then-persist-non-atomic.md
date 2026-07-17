---
title: "EXP-239: Ask AI verify-then-persist is non-atomic; soft-deleted conversations receive new messages"
linear_id: "EXP-239"
agent_fp: "auto"
date: "2026-05-31"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, ai, project/experts]
category: "bug"
source: "automation"
---

# EXP-239: AI verify-then-persist TOCTOU on soft-deleted conversations

**Linear:** [EXP-239](https://linear.app/experts/issue/EXP-239) | **Status:** Backlog

## Summary
`verifyConversation` and `persistAskAiExchange` are two separate DB round-trips with no enclosing transaction. If a conversation is soft-deleted between the verification check and the persist step (while OpenAI is streaming), `persistAskAiExchange` inserts messages into the logically-deleted conversation. The messages are invisible in the UI but persist in the DB as orphaned rows.

## File
`apps/experts-app/src/lib/ai/ask/ask-ai-assistant.ts` — `prepareAskAiTurn` / `persistAskAiExchange`

## Repro
1. Start a long-streaming AI response (3+ seconds).
2. While the stream is running, delete the conversation from a second session.
3. The soft-delete sets `deleted_at`; the streaming response continues.
4. On stream completion, `persistAskAiExchange` inserts messages under the deleted conversation.

## Fix
Wrap `verifyConversation` + `persistAskAiExchange` in a single `$transaction` that re-checks `deleted_at IS NULL` as part of the persist upsert, preventing writes to soft-deleted conversations.

## Related
- EXP-220 (missing `deleted_at` migration, resolved PR #679)
- EXP-232 (client-supplied history injection)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
