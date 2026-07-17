---
title: "EXP-143: .claude/agents definitions grant unrestricted Bash to agents processing adversary-controlled content"
linear_id: "EXP-143"
agent_fp: "4ac8e6df6ea6"
date: "2026-05-26"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, agents, prompt-injection, platform, project/experts]
category: "bug"
source: "automation"
---

# EXP-143: .claude/agents definitions grant unrestricted Bash to agents processing adversary-controlled content

**Linear:** [EXP-143](https://linear.app/experts/issue/EXP-143) | **Fingerprint:** `<!-- agent-fp: 4ac8e6df6ea6 -->` | **Severity: Medium**

## Summary

Two new Claude Code agent definitions were introduced in commits `0c0de88` and `243fb72` (2026-05-26): `.claude/agents/codebase-completeness-auditor.md` and `.claude/agents/linear-board-auditor.md`. Both grant the `Bash` tool to agents that read and process adversary-controlled content — specifically Linear issue bodies, PR descriptions, and source code comments. This creates an indirect prompt injection path: a malicious Linear issue body could contain instructions that cause the agent to execute arbitrary shell commands via Bash during an audit run.

## Impact

- **Indirect prompt injection**: An attacker who can create or edit a Linear issue (any team member with Linear access, or anyone who can file an issue via the API) can craft a body containing prompt injection instructions. When the `linear-board-auditor` reads and processes this issue, it could be instructed to exfiltrate environment variables, read secret files, or execute destructive commands.
- **CI runner scope**: If these agents run in CI (GitHub Actions), the Bash tool would have access to CI secrets (`GITHUB_TOKEN`, `CRON_SECRET`, R2 credentials, etc.).
- **Medium severity** because it requires Linear access to inject, but the blast radius (arbitrary shell execution in CI context) is high.

## Root Cause

The agent definitions include `tools: ["Bash", "Read", "WebFetch", ...]` without restricting Bash to read-only commands. The content processed by these agents (Linear issue bodies, PR descriptions, source code) is written by humans who may have adversarial intent.

## Fix

1. Remove `Bash` from both agent definitions, or
2. Restrict Bash to an explicit read-only allowlist: `find`, `grep`, `cat`, `ls`, `wc` — no write, execute, network, or destructive commands.
3. Add a system prompt instruction explicitly prohibiting the agent from executing shell commands based on content read from Linear or GitHub.
4. Consider sandboxing agent runs to a read-only workspace.

## Related

- Commits `0c0de88`, `243fb72`, `7f6ffd4` (agent definition additions and enhancements)
- Decision-Log 2026-05-26: Claude Code agent Bash access constraint (added by this digest)
- Decision-Log 2026-05-13: proxy.ts must not rely on upstream trust for auth (analogous principle)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
