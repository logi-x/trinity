---
title: "EXP-151: Routines 07/08 grant Bash+WebFetch to autonomous cron agents reading adversary-controlled content"
linear_id: "EXP-151"
agent_fp: "9ad9431817ea"
date: "2026-05-27"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, platform, project/experts]
category: "bug"
source: "automation"
---

# EXP-151: Routines 07/08 Bash+WebFetch grant to autonomous agents

**Linear:** [EXP-151](https://linear.app/experts/issue/EXP-151) | **Fingerprint:** `9ad9431817ea`

## Summary
`.claude/routines/07-codebase-completeness-audit.json` and `08-linear-board-audit.json` grant `Bash` + `WebFetch` to autonomous cron agents that read adversary-controlled content (Linear issue bodies, PR descriptions). Distinct from EXP-143 (different files, WebFetch scope, autonomous execution, `allow_unrestricted_git_push` to brain).

## Location
`.claude/routines/07-codebase-completeness-audit.json` + `08-linear-board-audit.json` / `allowed_tools`

## Impact
Indirect prompt injection path via crafted Linear issue bodies. An attacker who can file Linear issues could exfiltrate CI secrets or invoke destructive commands during an audit run.

## Fix
Remove `Bash` and `WebFetch` from R7/R8 `allowed_tools`, or restrict to an explicit read-only allowlist matching the R9 pattern (Read, Grep, Glob, specific MCP calls only).

## Related
EXP-143 (same class, .claude/agents), EXP-173 (R9 push grant)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
