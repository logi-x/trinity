---
description: Provide recommendations for a decision
argument-hint: "[decision context]"
allowed-tools: Read, Write, Glob, Bash(mkdir:*), mcp__trinity__*
---

# Recommend

Recommendations for: **$ARGUMENTS**

## Steps

1. Obtain the task ID and clarify options (at least 2) with trade-offs.
2. Ground facts in Sentinel-verified Scout claims + cited Cornelius records.
3. Explicit assumptions, risks, next steps, success metrics.
4. Save a contract-compliant artifact to `/home/developer/shared-out/strategy/recommendations/{task-id}-strategy-r{N}.md`.
5. Notify Steward; hand accepted product/solution directions to Forge when needed.
6. Reply with path + recommended option in 4 bullets.
