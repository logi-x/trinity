---
title: "EXP-293 — auth()/getUserPermissions() before try bypasses safeErrorJson — 37-handler class"
date: "2026-06-03"
updated: "2026-06-03"
tags: ["security", "api", "error-handling", "safeErrorJson", "auth", project/experts]
category: "bug"
source: "agent-scan"
source_id: "Raw/bugs/bug-exp-293-auth-before-try-bypasses-safeerrorjson.md"
status: open
resolution: unknown
---

# EXP-293 — auth()/getUserPermissions() before try bypasses safeErrorJson — 37-handler class

**Linear:** https://linear.app/experts/issue/EXP-293
**FP:** `a5301e354c25`
**Severity:** Medium
**Status:** open
**Filed:** 2026-06-03
**Routine:** R3

## File / Symbol

`apps/experts-app/app/api/v1/**/route.ts` — any handler where `auth()` or `getUserPermissions()` is called before the first `try` block. Full list in `graphify-out/safeErrorJson-audit.md`. Seed: `posts/[id]/route.ts` (EXP-287, fixed PR #792).

## Repro

1. On any of the 37 affected handlers, trigger a degraded-NextAuth state (e.g., DB connection drop during auth session lookup).
2. `auth()` throws before the `try` block is entered.
3. The thrown error bypasses `safeErrorJson` entirely and propagates as an unhandled rejection → raw 500 response with potential framework internals.

## Root Cause

`safeErrorJson()` is the platform's error-sanitization choke point (269 graph edges, betweenness 0.237). For it to protect a handler, all throwable code must be **inside** the handler's `try` block. The EXP-287 fix (PR #792) moved `auth()` inside try for `posts/[id]/route.ts`; safeErrorJson god-node audit then found 37 additional handlers with the same pattern.

## Fix

For each affected handler: move `auth()` and `getUserPermissions()` calls to the first line inside the outermost `try` block. Then add ESLint `no-auth-before-try` rule scoped to `app/api/**/route.ts` to prevent regression. Class fix, not 37 individual issues.

## Agent Fingerprint

`<!-- agent-fp: a5301e354c25 -->`

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
