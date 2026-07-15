---
description: Analyze a strategic question or situation
argument-hint: "[question or situation]"
allowed-tools: Read, Write, Glob, Bash(mkdir:*), mcp__trinity__*
---

# Analyze

Strategic analysis of: **$ARGUMENTS**

## Steps

1. Obtain the task ID and frame the problem and decision criteria for Logix.
2. Pull Sentinel-verified Scout research from `/home/developer/shared-in/logix-scout/research/` (fallback: `shared-in/scout/research/`).
3. Query Cornelius for client/org facts when relevant - do not invent.
4. Cite verified claim IDs for facts; label all new inferences and assumptions.
5. Save a contract-compliant artifact to `/home/developer/shared-out/strategy/analyses/{task-id}-strategy-r{N}.md`.
6. Notify Steward and reply with path + key implications.
