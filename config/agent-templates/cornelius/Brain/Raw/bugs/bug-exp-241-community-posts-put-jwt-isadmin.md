---
title: "EXP-241: Community posts PUT uses JWT-derived isAdmin — revoked admin bypasses ownership gate and pin guard"
date: "2026-05-31"
status: open
resolution: unknown
tags: [bug, security, jwt-staleness, community, auth, project/experts]
---

## Summary

The `PUT /api/v1/community/posts/[id]` handler derives `isAdmin` from the JWT payload rather than re-querying the database. A user whose admin role is revoked retains the JWT claim for up to 30 days, allowing them to: (1) edit any post bypassing the ownership check, and (2) pin/unpin any post (a capability normally restricted to admins).

## File

`apps/experts-app/app/api/v1/community/posts/[id]/route.ts` — `PUT` handler

## Repro

1. Grant User A admin role in DB. User A signs in; JWT contains `roles: ["admin"]`.
2. User B creates a community post.
3. Revoke User A's admin role in DB. Do NOT invalidate the JWT.
4. User A sends `PUT /api/v1/community/posts/<B's post id>` with `{ "pinned": true }` — succeeds (should be denied).

## Agent Fingerprint

`f64b4f6e1ec5` (R3)

## Linear

https://linear.app/experts/issue/EXP-241

## Fix

Re-derive actor role from DB in the PUT handler using a `getDbCommunityActor` pattern (analogous to `getDbCourseActor` from PR #684/EXP-212). See Decision-Log 2026-05-31 for the domain-actor pattern decision.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
