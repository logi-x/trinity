---
title: "EXP-126: Admin storage metrics overThreshold query missing LIMIT clause"
linear_id: "EXP-126"
agent_fp: "3334a6094169"
date: "2026-05-25"
severity: "Low"
status: "Backlog"
tags: [bug, storage, admin, performance, project/experts]
category: "bug"
source: "automation"
---

# EXP-126: Admin storage metrics overThreshold query missing LIMIT clause

**Linear:** EXP-126 | **Fingerprint:** `<!-- agent-fp: 3334a6094169 -->` | **Severity: Low**

## Summary

The admin storage dashboard (EXP-82) has a query that returns all users over their storage threshold. The query uses a raw `WHERE used_bytes > threshold` without a `LIMIT` clause or pagination. On a large user base, this query will return an unbounded result set, potentially timing out or exhausting memory in the API handler.

## Impact

- API response time degrades linearly with the number of over-quota users.
- At scale, the admin dashboard storage metrics page becomes unusable (timeout or OOM).
- Related: EXP-96 (admin user list also unbounded, pending pagination fix).

## Root Cause

The query was written for the initial implementation with a small test dataset. No LIMIT or cursor was added because the result set was always small during development.

## Fix

Add pagination to the `getOverThresholdUsers` query:
```ts
const users = await db.userStorageUsage.findMany({
  where: { used_bytes: { gte: thresholdBytes } },
  orderBy: { used_bytes: "desc" },
  take: pageSize,
  skip: (page - 1) * pageSize,
});
```

Return a paginated response with `total` count and `hasMore` flag.

## Related

- EXP-82 (admin storage dashboard)
- EXP-96 (admin user list pagination — same pattern)
- EXP-80 (user_storage_usage ledger)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
