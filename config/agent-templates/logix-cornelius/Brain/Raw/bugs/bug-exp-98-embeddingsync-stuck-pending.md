---
title: "EXP-98 — failed embed BullMQ job leaves EmbeddingSync stuck in pending with no error recorded"
date: "2026-05-24"
status: open
resolution: unknown
tags: [bug, ai, embeddings, bullmq, data-integrity, project/experts]
linear: "https://linear.app/experts/issue/EXP-98/bug-failed-embed-bullmq-job-leaves-embeddingsync-stuck-in-pending-with"
fingerprint: "9d983ab4e6fb"
---

## Summary

When a BullMQ embed job exhausts all retries and moves to `failed` state, `setupAiResultHandler` never writes an error to the `EmbeddingSync` row. The row remains in `pending` indefinitely. The admin retry flow targets rows with `status = "failed"` only — meaning the stuck row is invisible to the retry UI and will not surface until the next batch reconciliation cron cycle (whose cycle time is undocumented).

Same handler file as EXP-97. Independent root cause but shares the same reliability gap.

## Root cause

`apps/experts-app/src/lib/ai/embeddings/ai-result.handler.ts / setupAiResultHandler` — the handler listens to BullMQ `completed` and `failed` events. On the `failed` event path, the handler does not write to the `EmbeddingSync` error column or transition the row to a terminal `failed` state. The `enqueueEmbedOnPublish` call in `embed.service.ts` sets the initial `pending` status, but no code path ever moves it to `failed` when BullMQ retries are exhausted.

Fix: on the `failed` event, write the BullMQ job error (available in the event payload's `failedReason`) to the `EmbeddingSync` error column and transition the row to `failed` status.

## Agent fingerprint

`<!-- agent-fp: 9d983ab4e6fb -->`

## Status

`open` — Todo (No priority set). EmbeddingSync rows silently stuck in `pending` are invisible to the admin retry flow. Batch reconciliation cron is current mitigation but cycle time is undocumented. Should be batched with EXP-97 fix in `ai-result.handler.ts`.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
