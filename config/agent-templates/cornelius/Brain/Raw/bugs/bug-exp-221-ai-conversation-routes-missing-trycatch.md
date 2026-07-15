---
title: "EXP-221: AI conversation route handlers missing try/catch — unhandled rejections crash route worker"
linear_id: "EXP-221"
agent_fp: "auto"
date: "2026-05-30"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, ai, error-handling, project/experts]
category: "bug"
source: "automation"
---

# EXP-221: AI conversation routes missing try/catch

**Linear:** [EXP-221](https://linear.app/experts/issue/EXP-221) | **Status:** Open

## Summary
AI conversation route handlers (list, detail, delete) do not wrap their async logic in try/catch. Unhandled promise rejections from Prisma or OpenAI calls crash the route worker process rather than returning a structured error response to the client.

## Impact
- Any DB error (e.g., EXP-220 `deleted_at` column missing) causes an unhandled rejection
- Client receives a connection-level error rather than a 500 JSON response
- Route worker may need to be restarted

## Fix Needed
Wrap all async route handler bodies in try/catch. Return `safeErrorJson` on catch (per the 2026-05-23 decision: `safeErrorJson` is the sole permitted error serializer).

## Related
- EXP-220 — deleted_at migration missing (triggers unhandled rejections)
- EXP-206 — rate limiting missing on AI routes
- PR #604 — safeErrorJson pattern reference

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
