---
title: "EXP-103 — [spinoff: EXP-80] Migrate 5 remaining upload routes to enforceStorageQuota"
date: "2026-05-24"
status: open
resolution: unknown
tags: [bug, storage, quota, upload, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-103"
fingerprint: "agent-fp:R5-exp80-quota-routes-001"
---

## Summary

EXP-72 merged the `enforceStorageQuota` middleware guard, but 5 upload routes were not updated to use it. Users on these routes can upload files without any quota enforcement, silently bypassing the storage limit system.

Affected routes (identified by R5 from EXP-72/EXP-80 merge diff):
1. `POST /api/v1/courses/[id]/assets/upload`
2. `POST /api/v1/courses/[id]/modules/[moduleId]/upload`
3. `POST /api/v1/courses/[id]/lessons/[lessonId]/assets/upload`
4. `POST /api/v1/events/[id]/assets/upload`
5. `POST /api/v1/community/posts/[id]/media/upload`

## Root cause

The `enforceStorageQuota` guard was introduced in EXP-72 and applied to the primary upload route only. R5 identified 5 additional upload paths during EXP-80 merge review that were not patched in the original PR.

## Agent fingerprint

`<!-- agent-fp:R5-exp80-quota-routes-001 -->`

## Status

Open — depends on EXP-80 (race-safe ledger) completing before quota enforcement is meaningful on all routes.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
