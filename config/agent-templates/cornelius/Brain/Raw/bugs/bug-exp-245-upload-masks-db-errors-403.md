---
title: "EXP-245: Upload route masks DB connection errors as 403 Forbidden"
date: "2026-06-01"
status: resolved
resolution: "merged PR #712"
tags: [bug, upload, api, error-handling, project/experts]
linear: "https://linear.app/experts/issue/EXP-245/bug-upload-route-masks-db-connection-errors-as-403-forbidden"
fingerprint: "4a1c9e7d2b8f"
---

## Summary

`authorizeDomainAccess` in `apps/experts-app/app/api/v1/internal/upload/route.ts` wrapped its Prisma lookup in a `try/catch` that returned `{ok: false}` on any thrown error. The POST handler mapped `{ok: false}` to **403 Forbidden**. DB connection timeouts, pool exhaustion, and unreachable DB all appeared to clients as permission-denied errors rather than retriable service failures.

## Location

`apps/experts-app/app/api/v1/internal/upload/route.ts` — `authorizeDomainAccess` catch block

## Repro Steps

1. Take the database offline or exhaust the connection pool.
2. Send a valid authenticated upload request.
3. Observe 403 Forbidden instead of 503 Service Unavailable.

## Agent Fingerprint

`4a1c9e7d2b8f` (R3)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
