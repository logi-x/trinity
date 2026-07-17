---
title: "EXP-194 — [bug] Section 3 unbounded userPosts/userComments in realtime sync polling — hot-path DoS amplifier"
date: "2026-05-29"
status: open
resolution: unknown
tags: [bug, security, api, realtime, dos, performance, project/experts]
linear: "https://linear.app/experts/issue/EXP-194/bug-section-3-unbounded-userpostsusercomments-in-realtime"
fingerprint: "7e6cad1a8d0d"
---

## Summary

An authenticated user with 1 000+ posts and 5 000+ comments opens the community feed. The browser polls `GET /api/v1/internal/realtime/sync` every ~3 seconds. On every poll tick the handler executes two unbounded `prisma.findMany` calls in Section 3 ("Like activities"):

1. `SELECT id FROM "Post" WHERE authorId = <userId>` — no `take:` — returns all posts the user has ever authored.
2. `SELECT id FROM "Comment" WHERE authorId = <userId>` — no `take:` — returns all comments ever posted.

The resulting ID sets flow into downstream `IN (...)` queries. For a high-volume user this generates massive DB load at 3-second intervals, amplifying load proportional to post/comment count with no cap.

## Root cause

`apps/experts-app/app/api/v1/internal/realtime/sync/route.ts:~281,288` — `prisma.post.findMany({ where: { authorId: userId } })` and `prisma.comment.findMany({ where: { authorId: userId } })` lack `take:` bounds. Noted by R5 gatekeeper during EXP-174 review as a follow-up beyond the IDOR scope.

## Repro

1. Seed user with 1 000+ posts and 5 000+ comments.
2. Open the community feed — polling starts automatically.
3. Profile DB: Section 3 `userPosts` and `userComments` queries both return the full set on every tick.

## Agent fingerprint

`<!-- agent-fp: 7e6cad1a8d0d -->`

## Status

`open` — Backlog (High priority). Fix pattern is established: add `take:` bounds matching Section 2 approach (EXP-192, PR #613). Rate limiting (EXP-191) would provide complementary protection.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
