---
title: "EXP-86 — Extract enforceStorageQuota guard + apply to all R2-write routes (EXP-72 follow-up)"
date: "2026-05-23"
status: open
resolution: unknown
tags: [bug, security, storage, quota, project/experts]
linear: "https://linear.app/experts/issue/EXP-86/security-extract-enforcestoragequota-guard-apply-to-all-r2-write"
fingerprint: "eda762c80f1e"
---

## Summary

PR #408 (EXP-72) added a quota preflight gate inline in the `/api/v1/internal/upload` route handler. The guard is not yet a first-class middleware or utility — it is retrofitted in one route. Any other R2-write route added by a developer unaware of the quota system will silently bypass the gate. The guard must be extracted into a reusable `enforceStorageQuota` utility and applied to every R2-write route.

## Root cause

Quota logic lives only in `app/api/v1/internal/upload/route.ts`. No shared guard or lint enforcement.

## Agent fingerprint

`<!-- agent-fp: eda762c80f1e -->`

## Status

`open` — Backlog. Depends only on EXP-72 (merged PR #408). Ready to flip to Todo immediately.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
