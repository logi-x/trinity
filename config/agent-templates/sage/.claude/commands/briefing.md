---
description: Generate an executive briefing from recent research
argument-hint: "[topic]"
allowed-tools: Read, Write, Glob, Bash(mkdir:*), mcp__trinity__*
---

# Briefing

Executive briefing on: **$ARGUMENTS**

## Steps

1. Obtain the task ID and gather latest Sentinel-verified Scout research under `shared-in/logix-scout/research/`.
2. Add Cornelius notes if the topic touches known clients/projects.
3. Keep it short (max ~1 page): situation, so-what, recommended watchouts/actions.
4. Save a contract-compliant artifact to `/home/developer/shared-out/strategy/briefings/{task-id}-strategy-r{N}.md`.
5. Notify Steward and reply with path + headline bullets.
