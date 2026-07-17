---
title: "EXP-290 — Community comments POST: no input validation"
date: "2026-06-02"
updated: "2026-06-02"
tags: ["security", "community", "api", "input-validation", "dos", project/experts]
category: "bug"
source: "agent-scan"
source_id: "Raw/bugs/bug-exp-290-community-comments-post-no-validation.md"
status: open
resolution: unknown
---

# EXP-290 — Community comments POST: no input validation allows unbounded content blobs and amplifies DoS chain

**Linear:** https://linear.app/experts/issue/EXP-290  
**FP:** `f0979bbccfad`  
**Severity:** Medium  
**Status:** open  
**Filed:** 2026-06-02  
**Routine:** R3

## File / Symbol

`apps/experts-app/app/api/v1/community/posts/[id]/comments/route.ts` — `POST` handler

## Repro

1. Authenticated user sends `POST /api/v1/community/posts/{id}/comments` with:
   - `body.content`: multi-megabyte string (Postgres `TEXT NOT NULL` — unlimited)
   - `body.parentId`: non-UUID value (e.g. `"'; DROP TABLE comments;--"`)
2. `content` is stored without length cap; large blobs amplify EXP-288/289 DoS surface
3. Malformed `parentId` passed to Prisma returns P2023, leaking ORM internals

## Root Cause

No Zod/schema validation on POST body. `content` has no `maxLength` cap. `parentId` is not validated as a UUID before being passed to `prisma.comment.create`.

## Chain with EXP-288 / EXP-289

Storing large comment blobs via EXP-290 directly amplifies the OOM DoS in EXP-288 (post detail inline comment fetch) and EXP-289 (comments GET unbounded findMany). All three should be fixed together.

## Fix

Add Zod schema: `z.object({ content: z.string().min(1).max(10000), parentId: z.string().uuid().optional() })`. Return 400 on validation failure.

## Agent Fingerprint

`<!-- agent-fp: f0979bbccfad -->`

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
