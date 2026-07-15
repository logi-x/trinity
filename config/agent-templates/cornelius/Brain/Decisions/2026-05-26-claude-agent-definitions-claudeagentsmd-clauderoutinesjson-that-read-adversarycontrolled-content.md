---
title: "Claude agent definitions (`.claude/agents/*.md`, `.claude/routines/*.json`) that read adversary-controlled content (Line"
date: "2026-05-26"
decision: "Claude agent definitions (`.claude/agents/*.md`, `.claude/routines/*.json`) that read adversary-controlled content (Linear issue bodies, PR descriptions, external URLs) must not be granted `Bash` or `"
stakeholders: "Logix, Security"
review_by: "2026-08-26"
source: "[[Raw/sources/2026-05-26-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Claude agent definitions (`.claude/agents/*.md`, `.claude/routines/*.json`) that read adversary-controlled content (Linear issue bodies, PR descriptions, external URLs) must not be granted `Bash` or `WebFetch` tools; allowed tools must be restricted to explicit read-only commands (`find`, `grep`, `cat`, `ls`).

**Rationale:** EXP-143/EXP-151. Bash access in an agent that reads Linear issue bodies creates an indirect prompt-injection path: a malicious issue body can instruct the agent to exfiltrate CI secrets via Bash. WebFetch similarly enables SSRF or exfiltration via outbound HTTP.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-26-experts-agent-digest.md]]
