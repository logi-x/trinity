---
description: Generate an executive briefing from recent research
argument-hint: "[topic]"
allowed-tools: Read, Write, Glob, Bash, mcp__trinity__*
---

# Briefing

Executive briefing on: **$ARGUMENTS**

## Steps

1. Gather latest Scout research under `shared-in/logix-scout/research/`.
2. Add Cornelius notes if the topic touches known clients/projects.
3. Keep it short (max ~1 page): situation, so-what, recommended watchouts/actions.
4. Save to `/home/developer/shared-out/strategy/briefings/{YYYY-MM-DD}-{slug}-briefing.md`.
5. Reply with path + headline bullets.
