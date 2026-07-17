---
title: "EXP-128: user_storage_usage.used_bytes column has no non-negative CHECK constraint"
linear_id: "EXP-128"
agent_fp: "9eb0ef7a1d1c"
date: "2026-05-25"
severity: "Low"
status: "Backlog"
tags: [bug, storage, schema, project/experts]
category: "bug"
source: "automation"
---

# EXP-128: user_storage_usage.used_bytes column has no non-negative CHECK constraint

**Linear:** EXP-128 | **Fingerprint:** `<!-- agent-fp: 9eb0ef7a1d1c -->` | **Severity: Low**

## Summary

The `user_storage_usage.used_bytes` column was created without a `CHECK (used_bytes >= 0)` constraint. Once EXP-121 (deletion decrement) is implemented, a race between a deletion and a decrement could transiently produce a negative `used_bytes` value, which would persist in the DB without any enforcement.

A negative `used_bytes` would allow all quota checks to pass (user appears to have more space than their limit), effectively disabling quota enforcement for the affected user.

## Impact

- Negative `used_bytes` silently disables quota enforcement for the affected user.
- Silent data corruption — no error is raised, the value persists.
- Risk is low until EXP-121 (deletion decrement) lands; after that, the race window opens.

## Root Cause

The `user_storage_usage` table was created as part of EXP-80 without a non-negative CHECK constraint on `used_bytes`. The column is defined as `BigInt` but has no floor value enforcement.

## Fix

Add a migration:
```sql
ALTER TABLE user_storage_usage
  ADD CONSTRAINT used_bytes_non_negative CHECK (used_bytes >= 0);
```

In Prisma schema:
```prisma
model UserStorageUsage {
  used_bytes BigInt @default(0) // add: @@check(fields: [used_bytes], constraint: "used_bytes_non_negative", expr: "used_bytes >= 0")
}
```

Note: Prisma does not natively support CHECK constraints in schema; use a raw migration file.

## Related

- EXP-80 (ledger creation)
- EXP-121 (used_bytes decrement on deletion — introduces the negative-value risk)
- EXP-127 (advisory lock collision — can cause cross-user accounting if lock keys collide)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
