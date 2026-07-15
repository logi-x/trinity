---
title: "EXP-98 — Failed embed BullMQ jobs leave stale pending EmbeddingSync rows"
date: "2026-05-24"
status: resolved
resolution: "PR #454: on BullMQ job 'failed' event, update EmbeddingSync row to status=failed and clear pending flag so the cron batch reconciler can retry."
tags: [bug, ai, embeddings, bullmq, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-98"
fingerprint: "agent-fp:R5-exp80-bullmq-failed-001"
---

## Summary

When a BullMQ embedding job failed, the corresponding `EmbeddingSync` row remained in `pending` status indefinitely. The cron batch reconciler skips `pending` rows, so failed embeddings were never retried.

## Root cause

The `failed` event handler for `EmbedJob` was not implemented. Only `completed` and `error` (global) handlers existed. BullMQ's per-job `failed` event is distinct from the global error handler and was silently dropped.

## Agent fingerprint

`<!-- agent-fp:R5-exp80-bullmq-failed-001 -->`

## Status

Resolved — PR #454 merged 2026-05-24.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
