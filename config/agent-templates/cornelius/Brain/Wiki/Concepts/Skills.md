---
title: "Skills"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "topic/skills"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Skills.md"
---

# Skills

In this vault, skills usually means reusable instruction bundles such as `SKILL.md` workflows for agents. In product conversations, it can also mean learner or portfolio skill data, so the term is context-sensitive.

## Vault meaning

The strongest recurring use here is agent workflow packaging: small, reusable instruction sets that teach an assistant how to perform a specialized task consistently.

The canonical filesystem source for reusable LLM skills is `/home/logix/.agents/skills`. Individual clients such as Codex should consume those skills through symlinks into their expected skill directories, while the vault records the registry, routing guidance, and durable decisions in [[Agents/LLM Skills Registry]].

## Why it matters

- Helps standardize recurring workflows across Codex, Claude, and Cursor usage
- Keeps prompts shorter by moving long operational instructions into reusable bundles
- Supports domain-specific execution such as planning, documentation, or design review

## Product-side overlap

Some conversations also use "skills" in the end-user sense: capabilities shown on profiles, portfolios, or filters. When the note refers to platform features rather than agent workflows, check the surrounding project context.

## Related

- [[Entities/Agents]]
- [[Agents/LLM Skills Registry]]
- [[Agents/How To Use Agents]]
- [[Agents/Prompt Template]]
- [[Wiki/Concepts/ui-ux-pro-max]]
