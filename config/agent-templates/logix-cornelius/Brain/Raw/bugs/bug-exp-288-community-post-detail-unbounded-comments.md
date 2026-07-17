---
title: "EXP-288 — Community post detail GET: unbounded comment fetch OOM DoS"
date: "2026-06-02"
updated: "2026-06-02"
tags: ["security", "community", "api", "dos", "unbounded-query", project/experts]
category: "bug"
source: "agent-scan"
source_id: "Raw/bugs/bug-exp-288-community-post-detail-unbounded-comments.md"
status: open
resolution: unknown
---

# EXP-288 — Community post detail GET: unbounded comment fetch OOM DoS

**Linear:** https://linear.app/experts/issue/EXP-288  
**FP:** `47a8e3572d1a`  
**Severity:** Medium  
**Status:** open  
**Filed:** 2026-06-02  
**Routine:** R3

## File / Symbol

`apps/experts-app/app/api/v1/community/posts/[id]/route.ts` — `GET` handler (lines ~59–67)

## Repro

1. Authenticated attacker populates a post with many comments via `POST /api/v1/community/posts/{id}/comments`
2. Unauthenticated caller sends `GET /api/v1/community/posts/{post_uuid}` (public endpoint)
3. Handler fetches all comments via unbounded `include: { comments: true }` (no `take:` limit)
4. DB loads entire comment tree into memory; response size grows linearly with comment count

## Root Cause

`GET /api/v1/community/posts/{id}` is fully public — no authentication required. The inline comment fetch inside the `findFirst`/`findUnique` has no `take:` bound, no pagination, and no `Cache-Control` header to reduce repeated cold hits.

## Relationship to EXP-289 and EXP-290

EXP-290 (no content length cap on POST /comments) amplifies this attack surface: a attacker can store large comment blobs that inflate each GET response further.

## Fix

Add `take: N` (e.g. 50) to the comments include, return cursor-based pagination, add `Cache-Control: public, max-age=30, stale-while-revalidate=60`.

## Agent Fingerprint

`<!-- agent-fp: 47a8e3572d1a -->`

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
