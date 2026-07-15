---
title: "EXP-294 — Community comment & post author email exposed to unauthenticated callers (PII)"
date: "2026-06-03"
updated: "2026-06-03"
tags: ["security", "pii", "community", "api", "email", project/experts]
category: "bug"
source: "agent-scan"
source_id: "Raw/bugs/bug-exp-294-community-author-email-pii.md"
status: open
resolution: unknown
---

# EXP-294 — Community comment & post author email exposed to unauthenticated callers (PII)

**Linear:** https://linear.app/experts/issue/EXP-294
**FP:** `62b3ed0583aa`
**Severity:** Medium (PII disclosure)
**Status:** open
**Filed:** 2026-06-03
**Routine:** R3

## File / Symbol

`apps/experts-app/app/api/v1/community/posts/[id]/comments/route.ts` — `GET` handler (comment author include)
`apps/experts-app/app/api/v1/community/posts/[id]/route.ts` — `GET` handler (post author include)
Redis `CommentData` / `PostData` types (also carry `author.email` in cached payloads)

## Repro

1. Any unauthenticated caller sends `GET /api/v1/community/posts/{id}` or `GET /api/v1/community/posts/{id}/comments`.
2. Response includes `author: { email: "user@example.com", ... }`.
3. Email is also written to the Redis comment/post cache, so it persists for the TTL and is served to all callers including anonymous.

## Root Cause

Pre-existing behavior that predates the EXP-291 hardening cluster. The Prisma `include: { user: { select: { ... email ... } } }` (or equivalent) was never scrubbed from the public GET payload. Surfaced during the security-auditor review of PR #794. Multi-site PII contract change — filed separately rather than smuggled into EXP-291.

## Fix

After confirming no frontend consumer reads `author.email` from the community API:
1. Remove `email` from the Prisma `select` on author in both GET handlers.
2. Remove `email` from the `CommentData` and `PostData` Redis type definitions.
3. Flush affected Redis keys or let TTL expire.

## Agent Fingerprint

`<!-- agent-fp: 62b3ed0583aa -->`

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
