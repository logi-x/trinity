---
title: "Local Development"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/dev"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
source_id: "README.md"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# Local Development

**Prerequisites:** Node.js ≥26, pnpm 11.9.0 (Corepack or `npx pnpm@11.9.0`), Docker Compose, root `.env` from `.env.example`.

## First-time setup

```bash
cp .env.example .env
npx pnpm@11.9.0 dev:infra
npx pnpm@11.9.0 local:setup
npx pnpm@11.9.0 dev
```

Open `http://localhost:3060`. `local:setup` runs install, migrations, seed, and CLI build.

## Day-to-day

| Task | Command |
| ---- | ------- |
| Infra only | `npx pnpm@11.9.0 dev:infra` |
| All dev servers | `npx pnpm@11.9.0 dev` |
| API only | `npx pnpm@11.9.0 api:dev` |
| Web only | `npx pnpm@11.9.0 web:dev` |
| Worker only | `npx pnpm@11.9.0 worker:dev` |
| Apply migrations | `npx pnpm@11.9.0 db:deploy` |
| Dev migrations | `npx pnpm@11.9.0 db:migrate` |
| Reseed | `npx pnpm@11.9.0 db:seed` |
| Pre-push gate | `npx pnpm@11.9.0 verify` |

## Full Docker

Default compose profile is infra only. Apps in containers:

```bash
docker compose --profile full up --build
```

## Seed users (local)

| User | Email | Password | Scope |
| ---- | ----- | -------- | ----- |
| Ahmed Al-Sulaimani | `ahmed@logi-x.org` | `logix-dev-2026` | Internal owner |
| Mansour Al-Fahad | `owner@experts.sa` | `experts-dev-2026` | Experts client portal |

See [[Projects/Logix/KERNEL/docs/guides/cli|CLI]] for `logix` build/link and JSON output conventions.
