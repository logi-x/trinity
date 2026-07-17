---
title: "EXP-133: storage-janitor/orphan-sweep CRON_SECRET timing-unsafe + fail-open"
linear_id: "EXP-133"
agent_fp: "2e044db85786"
date: "2026-05-26"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, cron-auth, storage, project/experts]
category: "bug"
source: "automation"
---

# EXP-133: storage-janitor/orphan-sweep CRON_SECRET timing-unsafe + fail-open

**Linear:** [EXP-133](https://linear.app/experts/issue/EXP-133) | **Fingerprint:** `<!-- agent-fp: 2e044db85786 -->` | **Severity: Medium**

## Summary

The `POST /api/v1/internal/storage-janitor/orphan-sweep` route uses the same timing-unsafe authentication pattern previously fixed in EXP-111 for the reaper routes: plain `!==` comparison for `CRON_SECRET` (not `timingSafeEqual`), and falls through to `requireAdmin` when `CRON_SECRET` is unset. This is the same class as EXP-112 (`storage-janitor/sweep/route.ts`). The issue is amplified post-PR #493 because the orphan-sweep now calls `releaseStorageBytes` — an admin who can trigger the sweep can force premature file deletion and quota decrement outside the 24h grace window.

## Impact

- **Timing oracle**: The plain `!==` comparison leaks secret length via timing side-channel — an attacker can determine CRON_SECRET length by measuring response latency.
- **Fail-open admin escalation**: When `CRON_SECRET` is not set, any authenticated admin can POST to the route and trigger full R2 orphan deletion + storage ledger decrements.
- **Amplified by EXP-121 fix**: Post-PR #493, the orphan-sweep calls `releaseStorageBytes`. An admin abusing this route can decrement `used_bytes` for arbitrary files outside the intended reap schedule, desynchronizing the storage ledger.

## Root Cause

Authentication pattern in `storage-janitor/orphan-sweep/route.ts`:

```typescript
if (!cronSecret || authHeader !== `Bearer ${cronSecret}`) {
  const { authorized, error: authError } = await requireAdmin(request);
  if (!authorized) return NextResponse.json({ error: authError }, { status: 401 });
}
```

This is identical to the pattern fixed in EXP-111 (PR #478) for the reaper routes.

## Fix

Apply the same `timingSafeEqual` pattern used in `reservation-cleanup/route.ts` and `storage-pending-reaper/route.ts` after PR #478: fail-closed (500) when `CRON_SECRET` is unset; use `crypto.timingSafeEqual` for comparison. Remove the `requireAdmin` fallback entirely.

Consider extracting `verifyCronSecret(request)` as a shared helper (tracked as EXP-116) to prevent this class from recurring.

## Related

- EXP-111 (timing-unsafe CRON_SECRET on reaper routes — resolved via PR #478)
- EXP-112 (same class on embedding-janitor sweep — review-blocked)
- EXP-114 (spinoff: storage-janitor sweep route)
- EXP-116 (extract shared verifyCronSecret helper)
- Decision-Log 2026-05-25: timingSafeEqual cron auth invariant

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
