---
title: "EXP-259: Community posts GET unknown sort value silently returns undefined-order results"
date: "2026-06-01"
status: open
resolution: unknown
tags: [bug, api, community, validation, project/experts]
linear: "https://linear.app/experts/issue/EXP-259/spinoff-exp-242-community-posts-get-unknown-sort-value-silently"
fingerprint: "9cdb1de81b76"
---

## Summary

`GET /api/v1/community/posts` accepts a `sort` query parameter with no enum validation. The handler processes `"recent"`, `"popular"`, and `"discussed"` explicitly. Any other value falls through to `prisma.post.findMany` with no `orderBy` clause, returning posts in undefined DB order. No error is returned to the client.

## Location

`apps/experts-app/app/api/v1/community/posts/route.ts:23` — `const sort = searchParams.get("sort") || "recent"` with no `z.enum()` or equivalent guard.

## Repro Steps

1. `GET /api/v1/community/posts?sort=arbitrary` — 200 OK response.
2. Results are in undefined order (no `orderBy`); no validation error.

## Agent Fingerprint

`9cdb1de81b76` (R3)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
