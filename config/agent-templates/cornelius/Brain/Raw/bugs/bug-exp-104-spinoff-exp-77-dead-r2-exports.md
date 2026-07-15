---
title: "EXP-104 — [spinoff: EXP-77] Delete dead R2 exports (createPresignedGetUrl, getFileStream)"
date: "2026-05-24"
status: resolved
resolution: "PR #459: removed createPresignedGetUrl and getFileStream from r2.service.ts. Neither function had any callers after the EXP-77 CDN migration."
tags: [bug, storage, r2, dead-code, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-104"
fingerprint: "agent-fp:R5-exp77-dead-r2-exports-001"
---

## Summary

Two R2 service exports — `createPresignedGetUrl` and `getFileStream` — were dead code with no callers after the EXP-77 legacy CDN migration. Dead exports mislead future developers into thinking these patterns are available and in use.

## Root cause

EXP-77 migrated file delivery to signed CDN URLs. The presigned-get and stream helpers were not removed during that PR.

## Agent fingerprint

`<!-- agent-fp:R5-exp77-dead-r2-exports-001 -->`

## Status

Resolved — PR #459 merged 2026-05-24.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
