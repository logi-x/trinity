---
title: "EXP-263: Community posts GET totalPages uncapped for in-memory sorts — clients receive unreachable page numbers"
date: "2026-06-01"
status: open
resolution: unknown
tags: [bug, api, community, pagination, project/experts]
linear: "https://linear.app/experts/issue/EXP-263/spinoff-exp-242-totalpages-uncapped-for-in-memory-sorts-clients"
fingerprint: "5aba1482"
---

## Summary

Spinoff of EXP-242 identified by R5 scanner. Same root cause as EXP-257 (R3 scanner): `totalPages` in `GET /api/v1/community/posts` for `popular`/`discussed` sorts is computed from the full DB count via `prisma.post.count()` while actual data is capped at 500 posts in memory. Advertised `totalPages` is higher than reachable pages. Fix EXP-257 and EXP-263 together.

## Location

`apps/experts-app/app/api/v1/community/posts/route.ts:92` — `totalPages: Math.ceil(totalPosts / limit)` uses full DB count

## Repro Steps

Same as EXP-257.

## Agent Fingerprint

`5aba1482` (R5)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
