---
title: "EXP-286 — community posts GET popular/discussed: totalPosts incoherent"
date: "2026-06-02"
updated: "2026-06-02"
tags: ["bug", "community", "api", "pagination", project/experts]
category: "bug"
source: "agent-scan"
source_id: "Raw/bugs/bug-exp-286-community-posts-totalposts-incoherent.md"
status: open
resolution: unknown
---

# EXP-286 — Community posts GET popular/discussed: totalPosts reflects full DB count but only 500 posts navigable

**Linear:** https://linear.app/experts/issue/EXP-286  
**FP:** `07a618296c89`  
**Severity:** Medium  
**Status:** open  
**Filed:** 2026-06-02  
**Routine:** R3

## File / Symbol

`apps/experts-app/app/api/v1/community/posts/route.ts` — `GET` handler (popular/discussed sort paths)

## Root Cause

The EXP-242 fix (PR #768, commit `ba220ef`) correctly caps `totalPages` via `reachableTotal = Math.min(totalPosts, INMEM_SORT_WINDOW)`. However, the `totalPosts` field in the JSON response still returns the raw DB count (`prisma.post.count()`). A community with 10,000 posts returns `totalPosts: 10000` but `totalPages` is capped to `Math.ceil(500 / limit)`. The `currentPage` param can exceed `totalPages`, producing ghost pages.

## Impact

Clients receive `totalPosts` that implies more pages exist than are reachable. Pagination UIs may render phantom page numbers. `currentPage > totalPages` returns an empty last page rather than a 400.

## Fix

Return `totalPosts: reachableTotal` (capped to `INMEM_SORT_WINDOW`) for popular/discussed sorts. Add a guard that resets `currentPage` to `totalPages` when it exceeds the cap.

## Agent Fingerprint

`<!-- agent-fp: 07a618296c89 -->`

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
