---
title: "EXP-222: AskAiSessionProvider loadConversation race condition on concurrent navigation"
linear_id: "EXP-222"
agent_fp: "auto"
date: "2026-05-30"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, ai, race-condition, client, project/experts]
category: "bug"
source: "automation"
---

# EXP-222: AskAiSessionProvider loadConversation race

**Linear:** [EXP-222](https://linear.app/experts/issue/EXP-222) | **Status:** Open

## Summary
`AskAiSessionProvider.loadConversation` calls `setConversation(null)` immediately, then starts an async fetch. If the user navigates to a different conversation before the fetch resolves, the stale response can overwrite the newly loaded conversation state, rendering the wrong conversation.

## Repro
1. Open AI conversation A
2. Quickly navigate to conversation B before A finishes loading
3. Conversation A's data renders in the B slot (or vice versa)

## Fix Needed
Add an AbortController to the fetch call and cancel the in-flight request on navigation. Alternatively, add a stale-check guard: compare the requested conversation ID against the current navigation target before calling `setConversation`.

## Related
- EXP-220 — deleted_at migration (underlying data issue)
- EXP-221 — unhandled rejections in AI route handlers

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
