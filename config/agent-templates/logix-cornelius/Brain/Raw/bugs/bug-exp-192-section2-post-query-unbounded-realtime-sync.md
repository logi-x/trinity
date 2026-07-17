---
title: "EXP-192 — [spinoff: EXP-174] Section 2 prisma.post.findMany has no take: bound in realtime sync route"
date: "2026-05-29"
status: resolved
resolution: "take:50 added to Section 2 prisma.post.findMany via PR #613 (EXP-192). Regression test added."
tags: [bug, api, realtime, performance, dos, project/experts]
linear: "https://linear.app/experts/issue/EXP-192/spinoff-exp-174-add-take-bound-to-section-2-post-query-in-realtime"
fingerprint: "3c5002d2354f5487be89ae2023e1872843218d9a"
---

## Summary

`apps/experts-app/app/api/v1/internal/realtime/sync/route.ts:203` — `prisma.post.findMany` in Section 2 ("comments on posts user is following or has commented on") had no `take:` limit. A user who has commented on thousands of posts generates an unbounded post-ID set that flows into downstream queries on every poll tick (~3s).

## Root cause

Section 2 comment-query already had `take: 50`, but the subsequent `prisma.post.findMany` that resolves post IDs from the comment results lacked a matching bound. Filed by R5 (gatekeeper) during EXP-174 PR review.

## Spinoff from

EXP-174 (realtime sync IDOR). R5 gatekeeper noted the missing `take:` during EXP-174 PR review.

## Agent fingerprint

`<!-- agent-fp: 3c5002d2354f5487be89ae2023e1872843218d9a -->`

## Status

`resolved` — `take:50` added in PR #613 (commit 7212c89c). Regression test asserts the bound. CI-green squash, no gatekeeper required (one-line, low-sev).

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
