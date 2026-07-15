---
title: "EXP-125: reapR2Orphans unbounded memory scan — OOM DoS vector"
linear_id: "EXP-125"
agent_fp: "28017fa2ea51"
date: "2026-05-25"
severity: "Medium"
status: "Backlog"
tags: [bug, storage, oom, performance, project/experts]
category: "bug"
source: "automation"
---

# EXP-125: reapR2Orphans unbounded memory scan — OOM DoS vector

**Linear:** EXP-125 | **Fingerprint:** `<!-- agent-fp: 28017fa2ea51 -->` | **Severity: Medium**

## Summary

`reapR2Orphans` lists all R2 objects in the bucket and loads their metadata into memory to compare against DB file records. At production scale (millions of objects), this single-pass unbounded listing will exhaust the process's heap, causing an OOM crash in the storage-orphan-reaper container.

## Impact

- OOM crash in the `storage-orphan-reaper` cron container restarts the container on every run.
- Crash may leave partial deletes (some orphans deleted, some not), producing an inconsistent state.
- The cron sidecar crash affects all cron routes in the same container (single point of failure).
- In a worst case, an attacker who can upload many files and then delete the DB records (or simply by normal platform growth) can trigger a reliable OOM on every reaper run.

## Root Cause

The R2 SDK's `list()` returns paginated results, but `reapR2Orphans` does not use pagination — it collects the full list before processing. The implementation is:

```ts
const objects = await r2.list({ prefix: "uploads/" }); // returns all objects
```

No cursor-based pagination, no batch size limit.

## Fix

Use cursor-based pagination with a configurable batch size:

```ts
let cursor: string | undefined;
do {
  const page = await r2.list({ prefix: "uploads/", cursor, limit: 500 });
  await processOrphanBatch(page.objects);
  cursor = page.truncated ? page.cursor : undefined;
} while (cursor);
```

Process and delete each batch before fetching the next to keep memory usage constant.

## Related

- EXP-81 (orphan reaper implementation)
- EXP-121 (used_bytes decrement — complement to orphan reaper)
- Pattern: same root cause as EXP-94/EXP-95 (BullMQ unbounded queue processing)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
