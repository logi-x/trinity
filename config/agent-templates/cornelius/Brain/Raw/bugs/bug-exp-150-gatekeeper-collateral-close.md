---
title: "EXP-150: Gatekeeper collateral-close allows silent Linear issue closure via PR magic words"
linear_id: "EXP-150"
agent_fp: "c0773ce1e857"
date: "2026-05-27"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, platform, project/experts]
category: "bug"
source: "automation"
---

# EXP-150: Gatekeeper collateral-close via PR magic words

**Linear:** [EXP-150](https://linear.app/experts/issue/EXP-150) | **Fingerprint:** `c0773ce1e857`

## Summary
The gatekeeper routine's `collateral-close-block` logic in `.claude/routines/05-gatekeeper.prompt.md` allows a contributor to silently close any Linear security issue by including `Closes/Fixes/Resolves EXP-XXX` in a PR body, without validating the issue is actually fixed.

## Location
`.claude/routines/05-gatekeeper.prompt.md/collateral-close-block`

## Impact
A contributor can close a security issue without implementing the fix. The gatekeeper would record the closure without verifying the bug is actually addressed.

## Fix
Gatekeeper should verify the issue body mentions it is genuinely resolved (e.g., PR diff addresses the reported location) before accepting collateral-close.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
