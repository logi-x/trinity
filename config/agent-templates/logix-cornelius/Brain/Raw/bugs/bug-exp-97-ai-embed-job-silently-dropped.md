---
title: "EXP-97 — completed embed job silently dropped when BullMQ removeOnComplete evicts job record before async callback"
date: "2026-05-24"
status: open
resolution: unknown
tags: [bug, ai, embeddings, bullmq, data-loss, project/experts]
linear: "https://linear.app/experts/issue/EXP-97/bug-completed-embed-job-silently-dropped-when-bullmq-removeoncomplete"
fingerprint: "7287d3880d98"
---

## Summary

BullMQ `removeOnComplete: {count: 50}` housekeeping can clean up a completed job's Redis key before the async `QueueEvents` callback fires in `setupAiResultHandler`. When this race is lost, `getJob()` returns `null`; the handler silently exits without writing `content_embeddings`. The publish event that triggered the embed job appears to have succeeded, but the embedding is never persisted.

## Root cause

`apps/experts-app/src/lib/ai/embeddings/ai-result.handler.ts / setupAiResultHandler` — on `completed` event, the handler calls `queue.getJob(jobId)` to retrieve job data. If `removeOnComplete` has already evicted the Redis key (possible under load or if the key count exceeds 50), `getJob()` returns `null`. No null guard or fallback path exists; the embedding write is silently skipped.

Fix: replace `getJob()` with direct use of the `returnvalue` payload available in the `QueueEvents` `completed` event listener arguments, or cache the job data at dispatch time keyed by job ID.

## Agent fingerprint

`<!-- agent-fp: 7287d3880d98 -->`

## Status

`open` — Todo (No priority set). Silent data loss in AI embedding pipeline. Batch reconciliation cron is current mitigation but cycle time is undocumented.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
