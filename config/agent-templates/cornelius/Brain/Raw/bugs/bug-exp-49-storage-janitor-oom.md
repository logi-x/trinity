---
title: "EXP-49 — Unbounded findMany in runStorageJanitorSweep OOM-crashes Next.js process"
date: "2026-05-20"
status: in-review
resolution: unknown
tags: [bug, storage-janitor, oom, performance, high, project/experts]
linear: "https://linear.app/experts/issue/EXP-49"
fingerprint: "197d47660102"
---

## Summary

`runStorageJanitorSweep` in `storage-janitor.sweeps.ts` calls `prisma.file.findMany` with no `take:` limit. Under a large pending-file backlog (100K+ rows), Prisma buffers all rows into a JS array, causing an ~80–160 MB heap spike in the Next.js app process. On a 1 GB VPS with ~300–400 MB baseline usage this OOM-kills the process and drops all in-flight requests. The cron fires again in 5 minutes with the backlog intact, creating a crash loop.

Secondary: no in-process concurrency guard prevents a second cron tick from starting its own full `findMany` while the first sweep is still running, doubling heap consumption.

The sibling `runOrphanAttachmentSweep` correctly uses `take: ORPHAN_SWEEP_BATCH_SIZE`; the pending sweep was not updated when migrated from an isolated BullMQ worker into the app process.

## Repro

1. Accumulate 100K+ `pending` `File` rows.
2. Trigger `POST /api/v1/internal/storage-janitor/sweep`.
3. Observe: Next.js process OOM-killed; server logs show process restart.

## Agent fingerprint

`<!-- agent-fp: 197d47660102 -->`

## In-flight fix

PR #346 (`fix/agent/EXP-49-pending-sweep-batch-limit`) — gatekeeper PASS. Adds `take: PENDING_SWEEP_BATCH_SIZE` (env-configurable, default 200), `orderBy: {createdAt: "asc"}`, and a module-level `pendingSweepRunning` boolean lock (try/finally).

## Status

`in-review` — PR #346 open, awaiting merge.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
