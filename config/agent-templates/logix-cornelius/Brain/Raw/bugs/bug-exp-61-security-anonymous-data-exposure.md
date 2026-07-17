---
title: "EXP-61 — Anonymous data exposure on course detail, presence, and viewers routes"
date: "2026-05-21"
status: resolved
resolution: fixed — PR #314
tags: [bug, security, authorization, data-exposure, anonymous-access, project/experts]
linear: "https://linear.app/experts/issue/EXP-61"
fingerprint: "c6b67de10a28"
---

## Summary

Three routes lacked authentication: (1) course-detail viewer-access gate allowed anonymous users to read draft/unpublished courses; (2) presence routes had no `auth()` call; (3) viewers route lacked auth and leaked PII (user IDs, display names) to anonymous callers.

## Repro

1. Call `/api/v1/courses/<draftCourseId>` without session cookie — observe draft course data returned
2. Call `/api/v1/courses/<id>/presence` without session — observe presence data
3. Call `/api/v1/courses/<id>/viewers` without session — observe user PII

## Agent fingerprint

`<!-- agent-fp: c6b67de10a28 -->`

## Status

`resolved` — PR #314 adds `auth()` guard and viewer-access gate.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
