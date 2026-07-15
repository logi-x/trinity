---
title: "EXP-127: Advisory lock hashtext() int32 birthday collision at ~55k users"
linear_id: "EXP-127"
agent_fp: "dc1af44c704a"
date: "2026-05-25"
severity: "Medium"
status: "Backlog"
tags: [bug, storage, advisory-lock, correctness, project/experts]
category: "bug"
source: "automation"
---

# EXP-127: Advisory lock hashtext() int32 birthday collision at ~55k users

**Linear:** EXP-127 | **Fingerprint:** `<!-- agent-fp: dc1af44c704a -->` | **Severity: Medium**

## Summary

The EXP-80 reservation flow uses `pg_advisory_xact_lock(hashtext(userId)::bigint)` to serialize concurrent uploads per user. `hashtext()` in PostgreSQL is a 32-bit hash function — casting it to `bigint` does not expand the range; it merely sign-extends the int32 value. The effective key space is 2³² ≈ 4.3 billion values.

By the birthday paradox, collision probability:
- At 10k users: ~1.2%
- At 55k users: ~31% (one collision expected)
- At 77k users: ~50% probability of at least one collision
- At 100k users: ~69% probability

When two users share a lock key, User A's upload blocks while User B holds the lock — and vice versa. This creates false mutual exclusion between unrelated users.

## Impact

- **Correctness**: Two users with colliding keys are unnecessarily serialized. Upload A must wait for Upload B to complete, even though they are for completely different users.
- **Availability**: At high concurrency, a slow upload from User B blocks all uploads for User A (and potentially chains if more users share the key).
- **Data integrity risk**: In the pathological case, if the reservation check includes the wrong user's usage row due to the serialized transaction, quota could be checked against the wrong account (depends on exact query scoping — needs audit).
- **Scale concern**: The platform is pre-launch; this will become a problem before 100k users.

## Root Cause

```sql
SELECT pg_advisory_xact_lock(hashtext('user-uuid-here')::bigint)
```
`hashtext()` returns `integer` (int32). The `::bigint` cast widens to 64 bits but does not increase entropy — the upper 32 bits are always the sign extension of bit 31, halving the usable range to 2³¹ distinct values.

## Fix

Use a full 64-bit key derivation:

```sql
-- Option A: MD5-based (uniform distribution)
SELECT pg_advisory_xact_lock(
  ('x' || md5('user:' || userId))::bit(64)::bigint
)

-- Option B: Integer surrogate key (if users table has integer PK)
SELECT pg_advisory_xact_lock(user_integer_id)
```

Option A is preferred for UUID user IDs (no schema change required). Option B requires adding an integer surrogate PK to the `users` table.

## Decision-Log

This issue is recorded in Decision-Log (2026-05-25): advisory lock keys must use the full 64-bit range; `hashtext()` is prohibited as a key derivation function.

## Related

- EXP-80 (advisory-lock reservation — where the flaw was introduced)
- EXP-121, EXP-122, EXP-124, EXP-128 (storage ledger correctness cluster)
- Decision-Log: storage reservation pattern (2026-05-25)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
