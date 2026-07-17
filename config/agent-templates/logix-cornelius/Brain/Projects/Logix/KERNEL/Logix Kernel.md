---
title: "Logix Kernel"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/command-center"]
category: "projects/logix"
up: "[[Entities/Projects/Logix Kernel]]"
repo_root: "/home/logix/logix-kernel"
---

# Logix Kernel

↑ [[Entities/Projects/Logix Kernel|Logix Kernel]]

Monorepo for **Logix Command Center** (pnpm workspace: `apps/`, `packages/`, Docker infra for Postgres/Redis/MinIO). Local UI defaults to `http://localhost:3060` after `dev:infra` + `local:setup` + `dev`.

## Curated docs

**[[Projects/Logix/KERNEL/docs|Docs index]]** — architecture, ADRs, local dev, CLI entry, roadmap summary. Implementation plans and superpowers specs stay in the repo ([[Projects/Logix/KERNEL/docs/meta/repo-doc-inventory|inventory]]).

## Links

- [[Entities/Projects/Logix]]
- [[Entities/Projects/Logix Kernel]]
- [[Projects/Logix/KERNEL/docs|Docs index]]

## Quickstart (repo root)

Paths below are **relative to `repo_root`** (`/home/logix/logix-kernel`).

```bash
cp .env.example .env
npx pnpm@11.9.0 dev:infra
npx pnpm@11.9.0 local:setup
npx pnpm@11.9.0 dev
```

Prerequisites: Node.js ≥26, pnpm 11.9.0, Docker Compose. See [[Projects/Logix/KERNEL/docs/guides/local-development|Local development]] and `README.md` in the repo for Docker, CLI, and workspace layout.
