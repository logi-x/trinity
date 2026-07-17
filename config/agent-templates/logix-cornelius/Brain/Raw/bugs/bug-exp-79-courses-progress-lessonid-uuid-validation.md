---
title: "EXP-79 — Validate lessonId UUID in POST /courses/[id]/progress before Prisma — malformed input returns 500 instead of 400"
date: "2026-05-22"
status: resolved
resolution: merged PR #396
tags: [bug, input-validation, courses, project/experts]
linear: "https://linear.app/experts/issue/EXP-79/bug-validate-lessonid-uuid-in-post-coursesidprogress-before-prisma"
fingerprint: "a619815990b0"
---

## Summary

`POST /api/v1/courses/[id]/progress` reads `lessonId` from the request body and passes it directly to Prisma without UUID validation. A malformed `lessonId` (non-UUID string) triggers a Prisma validation error that surfaces as an unhandled 500 Internal Server Error instead of a 400 Bad Request.

## Root cause

`apps/experts-app/app/api/v1/courses/[id]/progress/route.ts` — POST handler: no Zod UUID validation on `lessonId` before the Prisma `findUnique` call. Pre-existing across the file; not introduced by PR #392.

## Agent fingerprint

`<!-- agent-fp: a619815990b0 -->`

## Status

`resolved` — merged PR #396 (2026-05-22T19:21Z). UUID validation added for both `lessonId` and `courseId` before Prisma calls.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
