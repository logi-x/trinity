---
title: "EXP-258: Community posts GET unbounded search string allows large ILIKE pattern DoS"
date: "2026-06-01"
status: open
resolution: unknown
tags: [bug, security, api, community, dos, project/experts]
linear: "https://linear.app/experts/issue/EXP-258/spinoff-exp-242-community-posts-get-unbounded-search-string-allows"
fingerprint: "43a31eb41924"
---

## Summary

The `search` query parameter in `GET /api/v1/community/posts` is passed directly to two `{contains: search, mode: "insensitive"}` Prisma predicates with no length cap. This translates to two `ILIKE '%<string>%'` clauses. An unauthenticated attacker can submit a large string (e.g. 100 KB) triggering an expensive full-table ILIKE scan, causing DB CPU spikes and query timeouts.

## Location

`apps/experts-app/app/api/v1/community/posts/route.ts:39-43` — `search` param used in two `contains` predicates with no `maxLength` validation.

## Repro Steps

1. `GET /api/v1/community/posts?search=<100KB string>` — no authentication required.
2. DB executes two full-table ILIKE scans; query time spikes proportionally.

## Agent Fingerprint

`43a31eb41924` (R3)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
