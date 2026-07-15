---
title: "EXP-228: [refactor] Ask AI button visibility: replace hardcoded route deny-list with layout-based allow-list"
linear_id: "EXP-228"
agent_fp: "cab2a2be679d"
date: "2026-05-31"
severity: "Low"
status: "resolved"
resolution: "PR #685 — replaced deny-list in AskAiAssistant with layout opt-in; pages that want the widget include it in their layout"
tags: [bug, ai, refactor, project/experts]
category: "bug"
source: "automation"
---

# EXP-228: Ask AI deny-list replaced with allow-list

**Linear:** [EXP-228](https://linear.app/experts/issue/EXP-228) | **Status:** Resolved (PR #685)

## Summary
`AskAiAssistant` was mounted globally in `providers.tsx` and used a growing hardcoded deny-list of route paths to hide itself on specific pages. Every new page that should not show the AI widget required a manual addition to this list.

## File
`apps/experts-app/src/components/ai/AskAiAssistant.tsx:191-209`

## Fix
PR #685 replaces the deny-list with a layout composition pattern. Pages opt in by including the `AskAiAssistant` in their layout rather than relying on the global mount to conditionally hide.

## Related
- Part of the AI Ask assistant feature suite

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
