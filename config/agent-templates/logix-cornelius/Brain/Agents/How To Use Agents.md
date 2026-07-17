---
title: "How To Use Agents"
date: "2026-04-10"
tags: ["agents", "guide"]
category: "guide"
source: "generated"
source_id: "Agents/How To Use Agents.md"
updated: "2026-07-15"
---

## Links

- [[Agents/Agents]]
- [[Entities/Agents]]

## Purpose

Use this note as the default guide for working with Codex, Claude, and Cursor against this vault.

## Standard Context Pack

Every agent prompt should include these parts:

1. Goal
2. Repo or working area
3. Current state
4. Constraints
5. Relevant vault notes
6. Expected output

## Minimum Inputs

For project work, always include:

- The project entity note
- The project rules index
- One canonical project README or guide

For example:

- Experts: [[Entities/Projects/Experts]], Experts rules, [[Projects/Experts/Experts App/README|Experts monorepo README]]
- HoWA: [[Entities/Projects/HoWA]], HoWA rules, [[Projects/HoWA/README|HoWA README]]
- Logix: [[Entities/Projects/Logix]], Logix rules, [[Projects/Logix/README|Logix README]]

## Extra Inputs

Add these only when needed:

- Topic notes from `Wiki/Concepts/*`
- Project-specific docs under `Projects/<Project>/docs/*`

## Workflow

1. Start from [[Agents/Agents]]
2. Open the relevant context pack
3. Copy the prompt template from [[Agents/Prompt Template]]
4. Fill only the fields relevant to the current task
5. Give the agent the smallest useful context set

## Rules

- Use project rules for implementation constraints
- Use entity notes for ownership and graph structure
- Use project docs for detailed reference
