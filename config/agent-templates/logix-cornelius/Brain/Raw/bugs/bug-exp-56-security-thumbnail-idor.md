---
title: "EXP-56 — Course/event thumbnail IDOR — non-owner could overwrite thumbnails"
date: "2026-05-21"
status: resolved
resolution: fixed — PR #309 (commit 2e20df9c)
tags: [bug, security, idor, authorization, thumbnail, project/experts]
linear: "https://linear.app/experts/issue/EXP-56"
fingerprint: "31a9d52e12b4"
---

## Summary

Thumbnail upload/replace routes for courses and events did not include the requesting user in the Prisma `where:` clause, so any authenticated user could overwrite a thumbnail on a resource they did not own.

## Repro

1. Authenticate as user A; note courseId owned by user B
2. POST to `/api/v1/courses/<courseIdB>/thumbnail` with a new image
3. Observe: thumbnail overwritten without ownership check

## Agent fingerprint

`<!-- agent-fp: 31a9d52e12b4 -->`

## Status

`resolved` — PR #309 adds `createdById: session.user.id` to Prisma where clause.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
