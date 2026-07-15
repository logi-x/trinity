---
title: "EXP-289 — Community comments GET: unbounded findMany unauthenticated OOM DoS"
date: "2026-06-02"
updated: "2026-06-02"
tags: ["security", "community", "api", "dos", "unbounded-query", project/experts]
category: "bug"
source: "agent-scan"
source_id: "Raw/bugs/bug-exp-289-community-comments-get-unbounded.md"
status: open
resolution: unknown
---

# EXP-289 — Community comments GET: unbounded findMany, no cache — unauthenticated OOM DoS

**Linear:** https://linear.app/experts/issue/EXP-289  
**FP:** `d1b9205afee9`  
**Severity:** Medium  
**Status:** open  
**Filed:** 2026-06-02  
**Routine:** R3

## File / Symbol

`apps/experts-app/app/api/v1/community/posts/[id]/comments/route.ts` — `GET` handler

## Repro

1. Authenticated attacker populates a post with many comments (amplified by EXP-290 — no content length cap)
2. Unauthenticated caller repeatedly sends `GET /api/v1/community/posts/{id}/comments`
3. `prisma.comment.findMany({ where: { postId } })` has no `take:` bound — fetches all comments
4. No `Cache-Control` header → every request hits the DB cold

## Root Cause

Fully public endpoint. `prisma.comment.findMany` has no pagination or `take:` bound. No response caching reduces DB round-trips under load.

## Fix

Add `take: 50`, `cursor`-based pagination, `Cache-Control: public, max-age=30, stale-while-revalidate=60`. Return `nextCursor` in response for client pagination.

## Agent Fingerprint

`<!-- agent-fp: d1b9205afee9 -->`

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
