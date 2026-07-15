---
title: "EXP-173: R9 routine has allow_unrestricted_git_push on brain without deployed server-side guard"
linear_id: "EXP-173"
agent_fp: "b153a4209619"
date: "2026-05-28"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, security, platform, project/experts]
category: "bug"
source: "automation"
---

# EXP-173: R9 allow_unrestricted_git_push without server-side guard

**Linear:** [EXP-173](https://linear.app/experts/issue/EXP-173) | **Fingerprint:** `b153a4209619`

## Summary
`.claude/routines/09-routines-audit.json` sets `allow_unrestricted_git_push: true` on `logi-x/brain`. The routine's orchestrator has `Bash(git push:*)` in `allowed_tools`. The brain-side enforcement layer (EXP-158) was closed as documentation only; the actual workflow must be operator-deployed. Until deployed, the restricted grant is advisory only.

## Location
`.claude/routines/09-routines-audit.json` — `sources[1].git_repository.allow_unrestricted_git_push`

## Impact
The R9 routine can push to logi-x/brain without any server-side validation. If the routine is compromised via prompt injection, it can overwrite brain vault files.

## Fix
Deploy the brain-side push guard workflow (per `Raw/guides/2026-05-28-brain-agent-push-guard-deploy.md`) before R9 is enabled in production.

## Related
EXP-158 (brain-agent-push-guard), EXP-143 (agent Bash grants), EXP-151 (routines 07/08)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
