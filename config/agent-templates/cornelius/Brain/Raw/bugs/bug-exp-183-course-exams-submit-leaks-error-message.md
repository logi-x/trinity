---
title: "EXP-183 — [spinoff: EXP-170] course-exams submit route leaks raw error.message in production"
date: "2026-05-29"
status: resolved
resolution: "Migrated to DomainError + safeErrorJson via PR #604 (EXP-170 full sweep). Not-found, already-submitted, and expired exam paths now throw DomainError with safe client messages."
tags: [bug, security, api, error-disclosure, course-exams, project/experts]
linear: "https://linear.app/experts/issue/EXP-183/spinoff-exp-170-course-exams-submit-route-leaks-raw-errormessage-in"
fingerprint: "21719349276427fd8dbf34d026a6dcb0784a3ec8"
---

## Summary

`POST /api/v1/course-exams/attempts/{id}/submit` used `const message = error instanceof Error ? error.message : "Failed to submit exam"; return NextResponse.json({error: message}, {status: 500})` — a two-step capture pattern that forwarded raw Prisma / internal error text to the response body in all environments including production.

## Root cause

`apps/experts-app/app/api/v1/course-exams/attempts/[id]/submit/route.ts:44` — two-step `const message = error.message` pattern inside catch block, forwarded as `{error: message}` in the JSON response. The ESLint sink rule (added by PR #557) only matched the direct one-step form; the two-step form was not caught until EXP-187 fixed the lint selector.

## Spinoff from

EXP-170 (class-level error-disclosure sweep). Filed by R5 (PR gatekeeper) during attempt-2 BLOCK review of PR #599.

## Agent fingerprint

`<!-- agent-fp: 21719349276427fd8dbf34d026a6dcb0784a3ec8 -->`

## Status

`resolved` — Migrated to `safeErrorJson` + `DomainError` in PR #604 (EXP-170 full sweep, attempt 3). Specific not-found / already-submitted / expired conditions now throw `DomainError` with a safe client message.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
