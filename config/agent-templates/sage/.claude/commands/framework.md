---
description: Apply a strategic framework (SWOT, Porter's, etc.)
argument-hint: "[framework-name] [subject]"
allowed-tools: Read, Write, Glob, Bash, mcp__trinity__*
---

# Framework

Apply framework to subject: **$ARGUMENTS**

Parse as `{framework-name}` + `{subject}`. Common: SWOT, Porter's Five Forces, Value Chain, BCG, Ansoff.

## Steps

1. Apply only if it clarifies the decision (skip ceremony).
2. Use Scout / Cornelius inputs when available.
3. Save to `/home/developer/shared-out/strategy/frameworks/{YYYY-MM-DD}-{slug}-{framework}.md`.
4. Reply with path + 3 takeaways for Logix.
