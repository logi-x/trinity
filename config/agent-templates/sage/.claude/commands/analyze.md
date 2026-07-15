---
description: Analyze a strategic question or situation
argument-hint: "[question or situation]"
allowed-tools: Read, Write, Glob, Bash, mcp__trinity__*
---

# Analyze

Strategic analysis of: **$ARGUMENTS**

## Steps

1. Frame the problem and decision criteria for Logix.
2. Pull Scout research from `/home/developer/shared-in/logix-scout/research/` (fallback: `shared-in/scout/research/`).
3. Query Cornelius for client/org facts when relevant - do not invent.
4. List implications and open questions.
5. Save to `/home/developer/shared-out/strategy/analyses/{YYYY-MM-DD}-{slug}-analysis.md`.
6. Reply with path + key implications.
