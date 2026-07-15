---
title: "EXP-182: ~30 routes return {error: error.message} as public error field"
linear_id: "EXP-182"
agent_fp: "manual-exp182"
date: "2026-05-29"
severity: "Medium"
status: "resolved"
resolution: "absorbed into PR #604 full sweep (100 files / 134 sites)"
tags: [bug, security, api, project/experts]
category: "bug"
source: "automation"
---

# EXP-182: Error message disclosure — 30+ routes

**Linear:** [EXP-182](https://linear.app/experts/issue/EXP-182) | **Fingerprint:** `manual-exp182`

## Summary
Approximately 30+ routes returned `{error: error.message}` directly in JSON responses with no environment guard, leaking raw Prisma errors, internal stack details, and server paths to clients in production.

## Fix
Absorbed into PR #604 full error-disclosure sweep: 100 route files / 134 call sites migrated to `DomainError` + `safeErrorJson`. `DomainError` carries a client-safe message; `safeErrorJson` forwards `DomainError` verbatim and collapses all other errors to a generic message. Two ESLint `no-restricted-syntax` selectors enforce recurrence prevention in `app/api/**/route.{ts,tsx}`.

## Related
EXP-170 (quiz submit, parent), EXP-183-187 (spinoffs), EXP-189 (src/lib ESLint gap, still open)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
