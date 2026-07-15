---
title: "EXP-171: Unauthenticated diagnostic endpoint exposes Share table schema and sample record"
linear_id: "EXP-171"
agent_fp: "7f7d070769dd"
date: "2026-05-28"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, api, project/experts]
category: "bug"
source: "automation"
---

# EXP-171: Unauthenticated Share diagnostic endpoint

**Linear:** [EXP-171](https://linear.app/experts/issue/EXP-171) | **Fingerprint:** `7f7d070769dd`

## Summary
`GET /api/v1/content/share/test` is a test/diagnostic endpoint shipped to production with no authentication guard. Handler calls `prisma.share.count()` and `prisma.share.findFirst()`, returning Share table schema and a sample record to any unauthenticated caller.

## Location
`apps/experts-app/app/api/v1/content/share/test/route.ts` (entire file, introduced in commit `842d6baa2d71`)

## Impact
Unauthenticated PII disclosure. Share table record content and schema exposed publicly.

## Fix
Delete the diagnostic route entirely, or gate with `requireAdmin()` + ops secret. Pattern: proxy.ts does not gate `/api/*`; every route must guard itself (Decision-Log 2026-05-13).

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
