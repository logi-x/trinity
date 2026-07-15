---
title: "EXP-287 — GET /community/posts/[id]: auth() outside try block"
date: "2026-06-02"
updated: "2026-06-02"
tags: ["bug", "community", "api", "error-handling", project/experts]
category: "bug"
source: "agent-scan"
source_id: "Raw/bugs/bug-exp-287-community-post-auth-outside-try.md"
status: open
resolution: unknown
---

# EXP-287 — GET /community/posts/[id]: auth() moved outside try block, unhandled exception bypasses safeErrorJson

**Linear:** https://linear.app/experts/issue/EXP-287  
**FP:** `2f672f5b4d96`  
**Severity:** Medium  
**Status:** open  
**Filed:** 2026-06-02  
**Routine:** R3

## File / Symbol

`apps/experts-app/app/api/v1/community/posts/[id]/route.ts` — `GET` handler

## Root Cause

The EXP-254 fix (commit `3b55692`) moved `auth()` and `getUserPermissions()` calls to before the outer `try` block to enable the `isPublished` filter logic. If `auth()` throws (e.g. JWT malformed, session provider failure, network error on SSO), the exception propagates unhandled — bypassing the `catch(safeErrorJson)` wrapper — and leaks internal error details or crashes the route with a 500 that shows a raw Next.js error page.

## Impact

Session provider errors on a public-facing endpoint leak internal error information. Severity is bounded by the auth provider's error message content.

## Fix

Wrap `auth()` + `getUserPermissions()` in a `try/catch` or move them back inside the main `try` block. The `isPublished` filter logic can be derived from the optionally-null session result.

## Agent Fingerprint

`<!-- agent-fp: 2f672f5b4d96 -->`

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
