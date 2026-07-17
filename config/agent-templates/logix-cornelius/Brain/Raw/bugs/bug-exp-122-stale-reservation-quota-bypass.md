---
title: "EXP-122: Stale reservation opens quota-bypass window between reserve and finalize"
linear_id: "EXP-122"
agent_fp: "8f0122152042"
date: "2026-05-25"
severity: "Medium"
status: "Todo"
tags: [bug, storage, quota, race-condition, project/experts]
category: "bug"
source: "automation"
---

# EXP-122: Stale reservation opens quota-bypass window between reserve and finalize

**Linear:** EXP-122 | **Fingerprint:** `<!-- agent-fp: 8f0122152042 -->` | **Severity: Medium**

## Summary

The storage reservation flow (EXP-80) reserves bytes atomically via `pg_advisory_xact_lock`. However, if a reservation is created but never finalized (e.g., client abandons the upload after receiving the presigned URL), the stale reservation holds against the user's quota indefinitely — until the orphan reaper runs. During this window, the user is effectively blocked from their real available quota.

Conversely, if the reaper runs but does not atomically check the finalization state, it may release reservations that are in active transit (brief window between R2 PUT and finalize call), allowing a second upload that would push the user over quota.

## Impact

- Users can be falsely quota-blocked by stale reservations (degraded experience).
- In the race window between reaper release and upload finalize, quota can be transiently bypassed.
- Affects correctness of quota enforcement for concurrent uploaders.

## Root Cause

Reservations do not have a hard expiry column. The reaper cleans them up on a schedule, but the gap between orphan creation and reaper execution (potentially hours) is the bypass window.

## Fix

1. Add an `expires_at` column to `user_storage_reservations` (default: `NOW() + interval '15 minutes'`).
2. The quota check should count only non-expired reservations.
3. The reaper should only clean up `expires_at < NOW()` reservations — not active ones.
4. The finalize step should verify the reservation is still valid (not expired) before committing.

## Related

- EXP-80 (advisory-lock reservation ledger)
- EXP-121 (used_bytes not decremented on deletion)
- EXP-124 (reservation DELETE lacks ownership check)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
