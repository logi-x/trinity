---
title: "EXP-186 — [spinoff: EXP-170] console/health route leaks raw DB and Redis connection strings in admin responses"
date: "2026-05-29"
status: resolved
resolution: "health route refactored: down() helper now logs error server-side and returns a static 'unreachable' message; connection strings no longer exposed via PR #604."
tags: [bug, security, api, error-disclosure, health, admin, project/experts]
linear: "https://linear.app/experts/issue/EXP-186/spinoff-exp-170-consolehealth-route-leaks-raw-db-and-redis"
fingerprint: "7270e1172f0d"
---

## Summary

`GET /api/v1/console/health` `checkDatabase()` and `checkCache()` catch blocks forwarded `error.message` into `down(message)`, which was serialised directly into the JSON response. DB connection strings like `"connect ECONNREFUSED <ip>:<port>"` and Redis URLs were exposed to any admin-authenticated caller.

## Root cause

`apps/experts-app/app/api/v1/console/health/route.ts:66-67,79-80` — `const message = error instanceof Error ? error.message : "…"` then `down(message)` serialised into `NextResponse.json(response)`.

## Spinoff from

EXP-170 (class-level sweep, gatekeeper attempt-2 BLOCK review).

## Agent fingerprint

`<!-- agent-fp: 7270e1172f0d -->`

## Status

`resolved` — Fixed in PR #604. `down()` now accepts a static string; actual error logged server-side only.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
