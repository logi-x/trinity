---
title: "EXP-121: used_bytes never decremented on file deletion — storage ledger silent corruption"
linear_id: "EXP-121"
agent_fp: "f4dd620c958d"
date: "2026-05-25"
severity: "High"
status: "Todo"
tags: [bug, storage, ledger, corruption, project/experts]
category: "bug"
source: "automation"
---

# EXP-121: used_bytes never decremented on file deletion — storage ledger silent corruption

**Linear:** EXP-121 | **Fingerprint:** `<!-- agent-fp: f4dd620c958d -->` | **Severity: High**

## Summary

The `user_storage_usage` ledger's `used_bytes` column is incremented when files are uploaded (via the reserve→finalize pattern in EXP-80), but is **never decremented** when files are deleted. Every file deletion silently under-reports available storage. Over time, `used_bytes` can exceed the user's actual storage consumption by an unbounded amount.

## Impact

- **Quota enforcement is incorrect.** Users can be falsely blocked from uploading when they have deleted files to free up space.
- **Admin storage dashboard (EXP-82) shows inflated usage per user.** Storage metrics cannot be trusted.
- **Silent, compounding.** Every delete operation worsens the discrepancy with no observable error. The corruption is silent and permanent until manually corrected.
- **High severity** — affects every user who deletes files after EXP-80 lands in production.

## Root Cause

The file deletion handler (`DELETE /api/v1/files/:id` or equivalent) removes the R2 object and the DB record, but does not update `user_storage_usage.used_bytes`. The ledger only has an increment path (reserve→finalize); there is no corresponding decrement path for the delete operation.

## Fix

In the file deletion transaction, decrement `used_bytes` by the file's size:

```ts
await db.$transaction([
  db.file.delete({ where: { id: fileId } }),
  db.userStorageUsage.update({
    where: { userId },
    data: { used_bytes: { decrement: file.size } },
  }),
]);
```

Add `CHECK (used_bytes >= 0)` constraint (EXP-128) to prevent negative values if a deletion races ahead of the finalization.

## Prerequisite

EXP-128 (non-negative CHECK constraint) should land before or concurrently with this fix to prevent negative ledger values during any race window.

## Related

- EXP-80 (advisory-lock reservation ledger — increment path)
- EXP-128 (non-negative CHECK on used_bytes)
- EXP-122 (stale reservation quota-bypass)
- Decision-Log: storage dependency chain invariant (2026-05-23)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
