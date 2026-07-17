---
title: "EXP-301: GET /posts/{id}/comments silently truncates beyond 200"
date: "2026-06-03"
status: open
resolution: unknown
tags: [bug, community, pagination, ux, project/experts]
linear_url: "https://linear.app/experts/issue/EXP-301"
agent_fp: "00ccd3cef33a"
severity: medium
area: api/community
file: "apps/experts-app/app/api/v1/community/posts/[id]/comments/route.ts"
symbol: GET
source: "generated"
source_id: "Raw/bugs/bug-exp-301-comments-get-no-hasmore-signal.md"
---

# EXP-301: GET /posts/{id}/comments — silent truncation, no hasMore signal

**Linear:** https://linear.app/experts/issue/EXP-301  
**FP:** `00ccd3cef33a` (R3)  
**Severity:** Medium  
**Filed:** 2026-06-03

## Summary

PR #794 (EXP-289 fix) added `take: COMMENT_FETCH_CAP` (200) to the comments GET handler, but the response still returns just the array with no `hasMore`, `totalCount`, or `nextCursor` field. A post with >200 comments silently drops oldest comments with no client-observable signal.

## Repro

1. A post has 201+ comments (achievable organically or via EXP-299 rate-limit bypass).
2. `GET /api/v1/community/posts/<UUID>/comments` returns exactly 200 comments.
3. Response body has no `hasMore`, `totalCount`, or pagination cursor.
4. Client cannot know comments were truncated.

## Impact

- Oldest comments become permanently inaccessible to any client
- No UX affordance to load more
- Breaking for communities that grow beyond 200 comments on a post

## Fix

Add `hasMore: comments.length === COMMENT_FETCH_CAP` and `totalCount: await prisma.comment.count({ where: { postId } })` to the response. Long-term: implement cursor-based pagination.

## Related

- EXP-289: Fixed (PR #794) — unbounded GET added take:200 cap
- COMMENT_FETCH_CAP constant: `src/lib/community/constants/comments.ts`

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
