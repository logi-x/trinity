---
title: "EXP-240: PUT /community/posts/[id] postUpdateBodySchema unguarded — bypasses EXP-224 POST constraints via edit-after-create"
date: "2026-05-31"
status: resolved
resolution: "merged via PR #706"
tags: [bug, community, validation, zod, project/experts]
---

## Summary

`postUpdateBodySchema` in `app/api/v1/community/posts/[id]/route.ts` (lines 215-227) applied none of the security constraints introduced by EXP-224 on the POST schema: no line-break check on `title`, no enum on `category`, no tag count or content limits, no `http(s)://` validation on `thumbnailUrl` or gallery items. An attacker who creates a post through the guarded POST path can bypass all EXP-224 constraints by editing the post via PUT immediately after creation.

## File

`apps/experts-app/app/api/v1/community/posts/[id]/route.ts` — `PUT` handler, `postUpdateBodySchema`

## Repro

1. Create a community post via POST (passes EXP-224 guards).
2. PUT `/api/v1/community/posts/<id>` with `{ "title": "normal\ninjected line" }` — no line-break rejection.
3. The same title would be rejected by POST schema.

## Agent Fingerprint

`e89728f8ca7ddc067f5fbbe8404bfa2dbf83efe7` (R5)

## Linear

https://linear.app/experts/issue/EXP-240

## Resolution

PR #706 introduced a shared Zod schema (`postBodySchema`) for both POST and PUT handlers. EXP-240 opened and closed same day (2026-05-31T11:13Z → Done 2026-05-31T19:52Z).

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
