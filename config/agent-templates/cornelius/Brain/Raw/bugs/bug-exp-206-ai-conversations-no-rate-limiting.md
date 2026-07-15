---
title: "EXP-206: AI conversation list/detail/delete routes missing rate limit"
linear_id: "EXP-206"
agent_fp: "auto"
date: "2026-05-30"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, ai, rate-limit, security, project/experts]
category: "bug"
source: "automation"
---

# EXP-206: AI conversations missing rate limit

**Linear:** [EXP-206](https://linear.app/experts/issue/EXP-206) | **Status:** Open

## Summary
`authorizeAskAiSession` does not call `checkAskAiRateLimit` (or an equivalent sliding-window guard) for the AI conversation list, detail, and delete routes. The rate limit implemented in PR #626 for the AI question stream is absent on these endpoints.

## Impact
Authenticated users can enumerate, read, and delete AI conversations at unbounded request rates. The list endpoint combined with EXP-205's unbounded query (now fixed) was a DoS amplifier.

## Fix Needed
Apply `checkAskAiRateLimit` (or equivalent) in `authorizeAskAiSession` for AI conversation list/detail/delete routes. Reference PR #626 sliding-window implementation.

PR #649 applied a partial fix — verify full per-route enforcement is in place.

## Related
- EXP-205 — unbounded pagination (resolved)
- EXP-221 — AI routes missing try/catch (open)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
