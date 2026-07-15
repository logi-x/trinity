---
title: "EXP-281 — Community post creation POST has no rate limit — authenticated DoS and spam vector"
date: "2026-06-02"
status: open
resolution: unknown
tags: [bug, security, community, rate-limiting, dos, project/experts]
linear: "https://linear.app/experts/issue/EXP-281/security-community-post-creation-post-has-no-rate-limit-authenticated"
fingerprint: "25ef3eed3a78"
---

## Summary

`app/api/v1/community/posts/route.ts` POST handler has no rate limit. Any authenticated user can issue unlimited POST requests with a minimum-valid body, creating thousands of community posts per second, exhausting DB connection pool capacity, and spamming other users' feeds. The AI RAG system (`getPublishedContentContext`) would also index the spam, degrading AI response quality.

## Root cause

`apps/experts-app/app/api/v1/community/posts/route.ts/POST` — no sliding-window or token-bucket rate limiter applied before or after `auth()`. Compare with `ask-ai` routes which use `checkAskAiRateLimit`. A per-user rate limiter (e.g. Redis sliding window at 5 posts/minute) should be added.

## Agent fingerprint

`<!-- agent-fp: 25ef3eed3a78 -->`

## Status

`open` — Backlog (Medium). Authenticated DoS + spam vector. No rate limit on any community write path.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
