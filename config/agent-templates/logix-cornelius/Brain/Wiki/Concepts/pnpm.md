---
title: "pnpm"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "tech/pnpm"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/pnpm.md"
---

# pnpm

pnpm is the package manager backbone of the Experts monorepo. It matters here because install behavior, workspace boundaries, script conventions, and CI reproducibility all depend on it.

## What usually comes up

- workspace script dispatch
- lockfile consistency
- dependency resolution surprises
- CI/local mismatches
- package-manager version drift across machines

## Experts context

When a conversation mentions pnpm, it usually affects the whole monorepo rather than one component. Small package-manager decisions can become build, test, or onboarding problems quickly.

## Related

- [[Wiki/Concepts/Monorepo]]
- [[Wiki/Concepts/Node.js]]
- [[Projects/Experts/DEVELOPER_GUIDE]]
