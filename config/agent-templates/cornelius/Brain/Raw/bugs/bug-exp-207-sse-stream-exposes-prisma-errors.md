---
title: "EXP-207: streamAskAiQuestion catch block leaks Prisma error.message to client via SSE stream"
linear_id: "EXP-207"
agent_fp: "auto"
date: "2026-05-30"
severity: "Medium"
status: "resolved"
resolution: "PR #638 — replace error.message with opaque error code; log raw error server-side only"
tags: [bug, ai, error-disclosure, security, project/experts]
category: "bug"
source: "automation"
---

# EXP-207: SSE stream exposes Prisma errors

**Linear:** [EXP-207](https://linear.app/experts/issue/EXP-207) | **Status:** Resolved (PR #638)

## Summary
`streamAskAiQuestion` in `ask-ai-assistant.ts` passed `error.message` directly into the SSE stream on catch. Prisma errors include table names, column names, and constraint identifiers — all of which flowed to the client.

## Fix
PR #638 replaced `error.message` in the SSE catch block with an opaque error code. The raw Prisma error is now logged server-side only, following the `safeErrorJson` pattern from PR #604.

## Related
- EXP-189 — src/lib ESLint error-disclosure rule (resolved PR #636)
- PR #604 — safeErrorJson sweep (100 route files)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
