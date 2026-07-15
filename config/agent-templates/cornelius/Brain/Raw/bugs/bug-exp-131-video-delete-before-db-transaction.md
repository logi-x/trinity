---
title: "EXP-131: Video DELETE removes R2 object before DB transaction — zombie file records and quota not released on DB failure"
linear_id: "EXP-131"
agent_fp: "106ac9d02e72"
date: "2026-05-26"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, storage, video, r2, toctou, project/experts]
category: "bug"
source: "automation"
---

# EXP-131: Video DELETE removes R2 object before DB transaction — zombie file records and quota not released on DB failure

**Linear:** [EXP-131](https://linear.app/experts/issue/EXP-131/bug-video-delete-removes-r2-object-before-db-transaction-zombie-file) | **Fingerprint:** `<!-- agent-fp: 106ac9d02e72 -->` | **Severity: High**

## Summary

The `DELETE /api/v1/courses/{id}/modules/{mid}/lessons/{lid}/video` handler calls `r2.send(DeleteObjectCommand)` **before** executing `prisma.$transaction([attachment.delete, file.delete])`. If the DB transaction fails (transient connection drop, FK constraint violation, Prisma client timeout), the R2 object is permanently removed while the `Attachment` and `File` DB records remain — producing zombie records that reference a non-existent R2 key, and a permanent quota charge for a file the user can never access or delete again.

## Trigger Scenario

1. Instructor calls `DELETE /api/v1/courses/{id}/modules/{mid}/lessons/{lid}/video`.
2. `r2.send(DeleteObjectCommand)` succeeds — video object permanently deleted from R2.
3. `prisma.$transaction([attachment.delete, file.delete])` fails (transient DB error).
4. **Resulting state:**
   - R2 object: **gone** (unrecoverable).
   - `Attachment` record: still exists, `fileId` points to a now-stale `File` row.
   - `File` record: still exists with `status: ready`, R2 key pointing to nothing.
   - `user_storage_usage.used_bytes`: **not decremented** — `releaseStorageBytes()` (from EXP-121) is called inside the same try/catch; it is `.catch()`-wrapped so it does not fail the handler, but since the DB delete failed, the file's `userId` lookup may also fail or return stale data.
   - User is permanently quota-charged for a file they cannot access or remove.

## Impact

- **Data loss:** video file permanently deleted with no recovery path.
- **Quota leak:** `used_bytes` not decremented; user is permanently over-charged.
- **Zombie records:** `File` and `Attachment` rows become stale, pointing to missing R2 keys.
- **Audit failure:** the orphan reaper (`runOrphanAttachmentSweep`) may eventually discover the stale records, but cannot restore the R2 object.

## Fix Direction

Reverse the operation order:
1. Execute `prisma.$transaction([attachment.delete, file.delete])` first.
2. Only call `r2.send(DeleteObjectCommand)` **after** the DB transaction commits successfully.
3. If the R2 delete subsequently fails, log for manual cleanup — the DB record is already removed, so the R2 object becomes a true orphan that the orphan reaper will sweep in the next cycle.

This is identical to the fix pattern applied in EXP-51 (`runStorageJanitorSweep`, PR #348, 2026-05-21).

## Pattern Note

This is the **second confirmed instance** of R2-before-DB delete ordering in this codebase:
- EXP-51 (2026-05-21): `runStorageJanitorSweep` in the storage-janitor worker — fixed via PR #348.
- EXP-131 (2026-05-26): `DELETE .../video` route handler — unfixed.

A global audit of all `r2.send(DeleteObjectCommand)` callsites is recommended to surface any remaining occurrences before a third instance appears. See Decision-Log (2026-05-26) for the platform invariant.

## Related

- [EXP-51](https://linear.app/experts/issue/EXP-51) — R2-before-DB ordering in storage janitor sweep (same pattern, resolved 2026-05-21)
- [EXP-121](https://linear.app/experts/issue/EXP-121) — EXP-121 fix (PR #493) that operates on the same DELETE handler
- [EXP-130](https://linear.app/experts/issue/EXP-130) — ledger asymmetry in the same video surface
- Decision-Log: R2 object deletion ordering invariant (2026-05-26)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
