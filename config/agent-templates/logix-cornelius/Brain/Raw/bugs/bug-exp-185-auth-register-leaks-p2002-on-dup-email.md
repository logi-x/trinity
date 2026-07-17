---
title: "EXP-185 — [spinoff: EXP-170] auth/native/register leaks DB constraint details on duplicate email in production"
date: "2026-05-29"
status: resolved
resolution: "Migrated to safeErrorJson via PR #604. Explicit 409 DomainError branch added for P2002 unique-constraint violations so the intended 'email already registered' message is preserved."
tags: [bug, security, api, error-disclosure, auth, project/experts]
linear: "https://linear.app/experts/issue/EXP-185/spinoff-exp-170-authnativeregister-leaks-db-constraint"
fingerprint: "471dcdaf05d1d36a08637b30441254456197c81d"
---

## Summary

`POST /api/v1/auth/native/register` catch block returned `error instanceof Error ? error.message : "Registration failed"` with no environment guard. On duplicate email, Prisma's `P2002` unique-constraint violation message (which includes the constraint name and table) was forwarded verbatim to the caller in production.

## Root cause

`apps/experts-app/app/api/v1/auth/native/register/route.ts:104` — raw `error.message` forwarded via `{error: message}` in the 500 response body.

## Spinoff from

EXP-170 (class-level sweep). Filed by R5 (gatekeeper) during attempt-2 review.

## Agent fingerprint

`<!-- agent-fp: 471dcdaf05d1d36a08637b30441254456197c81d -->`

## Status

`resolved` — Fixed in PR #604. Explicit 409 `DomainError` branch added for P2002; generic catch collapses to `safeErrorJson` fallback.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
