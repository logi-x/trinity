---
title: "EXP-205: getAskAiConversationForUser findMany unbounded — no pagination on AI conversation list"
linear_id: "EXP-205"
agent_fp: "auto"
date: "2026-05-30"
severity: "Medium"
status: "resolved"
resolution: "PR #637 — add take:N + orderBy:{createdAt:'desc'} to getAskAiConversationForUser"
tags: [bug, ai, pagination, project/experts]
category: "bug"
source: "automation"
---

# EXP-205: askAiConversation unbounded findMany

**Linear:** [EXP-205](https://linear.app/experts/issue/EXP-205) | **Status:** Resolved (PR #637)

## Summary
`getAskAiConversationForUser` called `prisma.askAiConversation.findMany` without a `take:` bound. A user with many conversations caused an unbounded DB scan on every conversation list load.

## Fix
PR #637 added `take: N` + `orderBy: { createdAt: 'desc' }` and exposed cursor-based pagination on the conversation detail API endpoint.

## Related
- EXP-206 — AI conversation rate limiting (open)
- EXP-220 — deleted_at migration missing (deployment blocker)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
