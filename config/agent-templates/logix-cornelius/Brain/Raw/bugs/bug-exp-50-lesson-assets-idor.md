---
title: "EXP-50 — No ownership check on attachmentId allows IDOR cross-course file linkage"
date: "2026-05-20"
status: resolved
resolution: "Merged PR #347 (commit eb9dea35): prisma.attachment.findFirst({id, userId}) guard added; returns 404 if attachment does not belong to requesting user."
tags: [bug, security, idor, lesson-assets, high, project/experts]
linear: "https://linear.app/experts/issue/EXP-50"
fingerprint: "fc9c31c29e7a"
---

## Summary

`handleCourseLessonAssetCreate` in `course-lesson-asset-create.handler.ts` accepted any caller-supplied `attachmentId` without verifying it belonged to the requesting user. A malicious authenticated user could link files from any other course or user by supplying a foreign attachment UUID — classic Insecure Direct Object Reference (IDOR).

## Repro

1. Obtain the UUID of an `Attachment` belonging to another user/course.
2. POST to the lesson-asset-create endpoint with that foreign `attachmentId`.
3. Observe: attachment linked to your lesson without authorization error (expected: 404).

## Agent fingerprint

`<!-- agent-fp: fc9c31c29e7a -->`

## Resolution

Merged PR #347 (`fix/lesson-assets-ownership`, commit `eb9dea35`): added `prisma.attachment.findFirst({ where: { id: attachmentId, userId } })` guard before linking; returns 404 if the attachment does not belong to the requesting user. New unit test covers the rejection path.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
