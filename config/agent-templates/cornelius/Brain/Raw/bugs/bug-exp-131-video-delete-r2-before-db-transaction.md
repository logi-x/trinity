---
title: "EXP-131: Video DELETE removes R2 object before DB transaction — zombie file records"
linear_id: "EXP-131"
agent_fp: "106ac9d02e72"
date: "2026-05-26"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, storage, video, r2, transaction, project/experts]
category: "bug"
source: "automation"
---

# EXP-131: Video DELETE removes R2 object before DB transaction — zombie file records

**Linear:** [EXP-131](https://linear.app/experts/issue/EXP-131) | **Fingerprint:** `<!-- agent-fp: 106ac9d02e72 -->` | **Severity: High**

## Summary

The `DELETE /api/v1/courses/[id]/modules/[moduleId]/lessons/[lessonId]/video` handler calls `r2.send(DeleteObjectCommand)` before the Prisma transaction that deletes the `Attachment` and `File` rows. If the DB transaction fails after the R2 delete succeeds, the video is permanently gone from R2 but the database retains a dangling `File` + `Attachment` record. This leaves a zombie file record that cannot be replayed and quota that is never released.

## Impact

- **Data loss**: The R2 video object is permanently deleted even when the DB cleanup fails.
- **Quota corruption**: If `releaseStorageBytes` is not called (DB failure path), the storage ledger is not decremented and the user's quota remains occupied by a file that no longer exists.
- **Zombie records**: `File` and `Attachment` rows persist indefinitely, pointing to a non-existent R2 key. The orphan reaper may attempt to delete the already-gone R2 object, logging spurious errors.

## Root Cause

The handler performs R2 deletion optimistically before the database transaction:

```
r2.send(DeleteObjectCommand)  // R2 delete — irreversible
prisma.$transaction([attachment.delete, file.delete])  // may throw
```

If the Prisma transaction throws (transient DB connection drop, FK constraint violation, client timeout), the video is gone from R2 but the DB records remain.

## Repro Steps

1. Mock or cause a DB transaction failure in `prisma.$transaction` inside the DELETE handler (e.g., inject a transient connection error or introduce a FK violation).
2. Call `DELETE /api/v1/courses/{id}/modules/{mid}/lessons/{lid}/video` for a valid lesson with an attached video.
3. Observe: R2 `DeleteObjectCommand` succeeds; DB transaction fails; the `File` and `Attachment` rows remain; the R2 object is gone.
4. The lesson video is permanently lost with no recovery path.

## Fix

Reorder the operation: complete the Prisma transaction (delete DB records) **before** issuing the R2 `DeleteObjectCommand`. If the DB transaction fails, the R2 object is untouched and the operation can be retried. If the R2 delete fails after a successful DB transaction, the orphan reaper will eventually clean up the R2 object. This matches the standard "DB first, then storage" delete ordering.

Additionally, ensure `releaseStorageBytes` is only called after both the DB transaction and R2 delete succeed, to avoid quota desync on partial failures.

## Related

- EXP-130 (video upload+delete quota asymmetry — related video route issue)
- EXP-121 (storage ledger decrement fix — releaseStorageBytes was added to this handler)
- EXP-48 (orphan sweep fix — similar "R2 before DB" ordering mistake)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
