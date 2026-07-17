---
title: "EXP-237: Ask AI accepts client-supplied history verbatim, enabling prompt context injection"
linear_id: "EXP-237"
agent_fp: "auto"
date: "2026-05-31"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, ai, project/experts]
category: "bug"
source: "automation"
---

# EXP-237: AI Ask accepts client-supplied history verbatim

**Linear:** [EXP-237](https://linear.app/experts/issue/EXP-237) | **Status:** Backlog  
**Duplicate class of:** EXP-232 (same root cause; fix together)

## Summary
`buildOpenAiMessages` passes the client-supplied `history` array directly into the OpenAI messages array without substituting DB-stored messages. A user can inject arbitrary `role: "assistant"` turns to manipulate their own AI session context.

## File
`apps/experts-app/src/lib/ai/ask/ask-ai-assistant.ts` — `buildOpenAiMessages`

## Fix
Ignore client-supplied `history` when constructing the OpenAI message array; always load messages from DB when a conversation exists, or use an empty history for new conversations.

## Related
- EXP-232 (same root cause, R3 fingerprint — fix both simultaneously)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
