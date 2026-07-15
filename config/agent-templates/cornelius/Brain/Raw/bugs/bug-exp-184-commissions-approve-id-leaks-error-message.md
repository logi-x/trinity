---
title: "EXP-184 — [spinoff: EXP-170] admin/commissions/[id]/approve route leaks raw error.message"
date: "2026-05-29"
status: resolved
resolution: "Migrated to safeErrorJson via PR #604 (EXP-170 full sweep)."
tags: [bug, security, api, error-disclosure, commissions, admin, project/experts]
linear: "https://linear.app/experts/issue/EXP-184/spinoff-exp-170-admincommissionsidapprove-route-leaks-raw"
fingerprint: "2d9086d77592ceb9bc7d966785da67dae80eb791"
---

## Summary

The individual `POST /api/v1/admin/commissions/{id}/approve` route returned `error instanceof Error ? error.message : "Failed to approve commission"` directly in the 500 response body. The batch `approve-pending` endpoint was already fixed by EXP-116 (PR #565), but the individual approval endpoint was not swept.

## Root cause

`apps/experts-app/app/api/v1/admin/commissions/[id]/approve/route.ts:100` — catch block returns raw `error.message` in `{error: message}` JSON body with no APP_ENV guard.

## Spinoff from

EXP-170 (class-level sweep). Filed by R5 (gatekeeper) during attempt-2 review of PR #599.

## Agent fingerprint

`<!-- agent-fp: 2d9086d77592ceb9bc7d966785da67dae80eb791 -->`

## Status

`resolved` — Fixed in PR #604 (EXP-170 full sweep).

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
