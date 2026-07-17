---
title: "AGENTS.md"
date: "2026-04-10"
updated: "2026-05-24"
tags: ["entity", "topic", "topic/agents-md"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/AGENTS.md"
---

# AGENTS.md

`AGENTS.md` is the repo-local operating manual for coding agents. In this vault, linked conversations usually mean "the file that teaches Codex or similar tools how to work safely in a specific repository."

## What it is used for

- repo-specific workflow rules
- path and tool conventions
- project structure summaries
- expectations for edits, testing, and documentation
- high-signal context that should persist across sessions

## Why it matters in this vault

Many imported conversations start with or reference `AGENTS.md` instructions. That makes the file more than documentation; it is part of the execution environment for agent-assisted work.

## Good AGENTS.md traits

- points to real commands and real paths
- captures project-specific constraints, not generic advice
- stays aligned with current repo structure
- helps both humans and agents avoid repeated setup mistakes

## Typical maintenance work

- flattening outdated wrapper commands
- correcting tool paths after repo reorganizations
- moving durable instructions out of chat history into canonical docs
- keeping agent behavior aligned with project reality

## Notes

- 2026-05-24: In `/home/logix/experts`, Claude subagents from `.claude/agents/*.md` were migrated to Codex custom agents under `.codex/agents/*.toml`. Codex custom agents require `name`, `description`, and `developer_instructions`; this repo normalized Claude `sonnet` agents to `gpt-5.4` with `model_reasoning_effort = "medium"`, and the Claude `haiku` frontend agent to `gpt-5.4-mini` with medium effort.

## Related

- [[CLAUDE.md]]
- [[Wiki/Concepts/Documentation]]
- [[Agents/How To Use Agents]]
- [[Agents/Prompt Template]]
