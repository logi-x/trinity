---
title: "LLM Skills Registry"
date: "2026-05-03"
updated: "2026-05-03"
tags: ["agents", "skills", "codex", "claude", "cursor"]
category: "agents"
source: "generated"
source_id: "Agents/LLM Skills Registry.md"
---

# LLM Skills Registry

This note records the source-of-truth pattern for reusable LLM skills across Codex, Claude, Cursor, and other agent clients.

## Recommendation

Keep reusable skills in one canonical filesystem location:

```bash
/home/logix/.agents/skills
```

Then expose individual skills to each LLM client by symlink, for example:

```bash
ln -sf /home/logix/.agents/skills/brain-daily /home/logix/.codex/skills/brain-daily
```

The vault should know about the skills, but it should not become the executable source of truth for every skill body.

## Why

- One canonical directory avoids skill drift between Codex, Claude, Cursor, and future clients.
- Symlinks let each tool keep its expected local layout without copying files.
- The Obsidian vault is better as durable memory: what skills exist, what they are for, when to use them, and how they relate to projects.
- Skill implementations can evolve as operational tooling, while the vault keeps stable human-readable context.

## Vault Role

Use the brain vault for:

- a registry of available skills and their intent
- links between skills, projects, topics, and context packs
- design decisions about agent workflows
- session close notes when a skill changes because of a real project pattern
- higher-level synthesis such as "when should agents use brain-daily vs brain-query?"

Avoid using the vault as:

- a second copy of every `SKILL.md`
- a client-specific install directory
- a place for generated symlink state
- a dumping ground for every low-level skill implementation detail

## Suggested Structure

Keep this note as the human-readable registry. Add child notes only when a skill needs durable explanation beyond its `SKILL.md`.

Possible children:

- `Agents/Skills/brain-daily.md`
- `Agents/Skills/brain-query.md`
- `Agents/Skills/brain-ingest.md`
- `Agents/Skills/frontend-design.md`
- `Agents/Skills/github.md`

Each child note should summarize:

- canonical skill path
- target clients
- when to use it
- related vault pages
- project-specific caveats
- last meaningful update

## Update Policy

When a skill changes:

1. Edit the canonical skill under `/home/logix/.agents/skills`.
2. Let client symlinks point to that canonical copy.
3. Update this registry or the relevant child note only if the change affects durable usage, routing, or project memory.
4. Link project-specific behavior from the project note or context pack, not from every client install path.

## Related

- [[Wiki/Concepts/Skills]]
- [[Wiki/Concepts/AGENTS.md]]
- [[Entities/Agents]]
- [[Agents/How To Use Agents]]
- [[Agents/Prompt Template]]
- Codex
