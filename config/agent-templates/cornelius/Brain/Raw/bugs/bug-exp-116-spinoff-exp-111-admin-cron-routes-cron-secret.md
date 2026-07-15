---
title: "EXP-116: admin cron routes CRON_SECRET timing-unsafe"
linear_id: "EXP-116"
agent_fp: "c39011b3339e"
spinoff_of: "EXP-111"
date: "2026-05-25"
severity: "High"
status: "Backlog"
tags: [bug, security, cron, project/experts]
category: "bug"
source: "automation"
---

# EXP-116: admin cron routes CRON_SECRET timing-unsafe

**Linear:** EXP-116 | **Fingerprint:** `<!-- agent-fp: c39011b3339e -->` | **Spinoff of:** EXP-111

## Summary

All admin-namespaced cron routes use plain `!==` for `CRON_SECRET` comparison. This affects multiple routes under `/api/v1/internal/admin/` that are scheduled in the Docker cron sidecar.

## Impact

- Timing oracle across all admin cron routes.
- Admin cron routes perform privileged operations (user management, reporting, data cleanup). Unauthorized invocation could trigger bulk data operations.
- Pattern is now confirmed in at least 4 distinct route groups (EXP-111, EXP-114, EXP-115, EXP-116).

## Root Cause

No shared auth helper for cron route authentication. Each route implements its own check, and the correct pattern (PR #470) was not propagated. This is a structural gap, not a point bug.

## Fix

1. Extract `verifyCronSecret(req: Request): Response | null` into a shared utility (`lib/cron/auth.ts` or similar).
2. Replace all plain `!==` comparisons across the codebase with calls to this helper.
3. Add a lint rule or integration test that detects any new cron route that doesn't call `verifyCronSecret`.

## Related

- EXP-111 (parent), EXP-114 (storage-janitor), EXP-115 (ai/embeddings/sync), EXP-120 (missing tests)
- Decision-Log: `timingSafeEqual` cron auth invariant (2026-05-25)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
