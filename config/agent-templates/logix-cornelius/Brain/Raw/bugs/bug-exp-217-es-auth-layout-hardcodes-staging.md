---
title: "EXP-217: es-auth layout hardcodes staging.experts.com.sa as base URL"
linear_id: "EXP-217"
agent_fp: "auto"
date: "2026-05-30"
severity: "Medium"
status: "resolved"
resolution: "PR #665 — use canonical resolver"
tags: [bug, url, config, i18n, project/experts]
category: "bug"
source: "automation"
---

# EXP-217: es-auth layout staging URL hardcode

**Linear:** [EXP-217](https://linear.app/experts/issue/EXP-217) | **Status:** Resolved (PR #665)

## Summary
The `es-auth` layout component hardcoded `https://staging.experts.com.sa` as the base URL for canonical links and OG metadata. The Spanish-locale auth layout was always pointing at staging in production.

## Fix
PR #665 replaced the hardcoded URL with a call to `getPublicBaseUrl()` from the canonical resolver.

## Related
- EXP-204, EXP-216, EXP-218 — same class

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
