---
title: "Experts App"
aliases:
  - experts-app
repo_root: /Users/ahmedsulaimani/projects/experts/apps/experts-app
date: "2026-04-11"
updated: "2026-04-17"
status: "active"
freshness: "volatile"
verified: "2026-06-11"
source_of_truth: "/home/logix/experts"
verify_with:
  - "git log"
  - "GitHub issues and PRs"
  - "Linear"
tags: ["entity", "projects", "project/experts", "project/experts-app", "topic/nextjs", "topic/lms"]
category: "entity/project"
source: "generated"
source_id: "Entities/Projects/Experts App.md"
---
# Experts App (web)

Vault-side mirror of the **Next.js** full-stack LMS (**`apps/experts-app`** in the **experts** monorepo): App Router UI, `/api/v1` route handlers, Prisma + PostgreSQL, NextAuth, i18n, and mirrored **`.cursor/rules`**. Canonical tree: **`Projects/Experts/Experts App/`** (docs **V1–V4**, guides, rules, agent entry files).

## Links

- [[Entities/Organizations/Experts Company Ltd|Experts Company Ltd]]

## Overview

Vault-side mirror of the **Next.js** full-stack LMS (**`apps/experts-app`** in the **experts** monorepo): App Router UI, `/api/v1` route handlers, Prisma + PostgreSQL, NextAuth, i18n, and mirrored **`.cursor/rules`**. Canonical tree: **`Projects/Experts/Experts App/`** (docs **V1–V4**, guides, rules, agent entry files).

<p align="left"><a href="https://experts.com.sa" target="_blank"><img src="https://i.ibb.co/CJGyzJs/logo-full-512.png" width="360" alt="Experts Logo"></a></p>

This package is the **main Experts web application**: Next.js 16 (App Router), **PostgreSQL** + **Prisma 7**, **NextAuth v5**, versioned REST APIs under **`app/api/v1`**, and the full LMS/product UI.

> **Full architecture and onboarding:** see [[Projects/Experts/DEVELOPER_GUIDE|Developer guide]] (vault **source of truth** for monorepo architecture).  
> **Paths, conventions, and reference files:** AGENTS.md.  
> **Extended checklist (SEO, features, migration context):** CLAUDE.md.

---

## Stack

| Layer        | Technology                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------ |
| Framework    | Next.js 16, React 19                                                                       |
| UI           | Tailwind CSS v4, HeroUI v3, shadcn/Radix where needed                                      |
| API          | Route handlers; primary surface `app/api/v1/{domain}/`                                     |
| Domain logic | `src/lib/{domain}/` — Zod schemas, handlers, queries, DTOs, mappers                        |
| Database     | PostgreSQL, Prisma 7 (`@prisma/adapter-pg`)                                                |
| Auth         | NextAuth v5 (`src/lib/auth.ts`)                                                            |
| i18n         | next-intl — **en**, **ar**, **es** — `src/i18n/messages/` (relative to `experts-app` root) |
| Client fetch | `useApiQuery` + SWR — `src/hooks/use-api-query.ts` (relative to `experts-app` root)        |
| Async work   | BullMQ + Redis; PDF / ZATCA workers — `src/workers/` (relative to `experts-app` root)      |
| Tests        | Vitest; Playwright E2E — `tests/e2e/` (relative to `experts-app` root)                     |

The stack is **not** Laravel + MySQL; historical references to a separate `experts-api` image as the primary backend do not describe this package.

---

## Requirements

- **Node** ≥ 22
- **pnpm** 10.x (monorepo root pins `packageManager`)
- **PostgreSQL** (connection string in `.env`)
- **Redis** when running queues, workers, or realtime integration

Copy or create **`.env`**, **`.env.test`**, and **`.env.e2e`** as required by your team. These files are not committed.

---

## Commands (this directory)

```bash
pnpm dev              # http://localhost:3025 — Turbopack
pnpm build && pnpm start
pnpm lint             # ESLint
pnpm typecheck:tsc    # TypeScript --noEmit

pnpm test             # Vitest (loads .env.test)
pnpm test:watch
pnpm test:e2e         # Playwright

pnpm db:migrate       # prisma migrate dev
pnpm db:push          # prisma db push
pnpm db:seed          # seed script
pnpm db:studio        # Prisma Studio
pnpm prisma generate
```

Workers and local “all services” orchestration:

```bash
pnpm worker:pdf
pnpm worker:zatca
pnpm email:dev
pnpm all              # dev + selected workers + email preview (see package.json)
```

From the **repository root**, the same workflows are exposed as `pnpm experts:*` (see root `package.json`).

---

## Project structure (abbreviated)

```
app/
  (i18n)/ # en | ar | es + _shared implementations
  api/
    v1/                   # versioned REST API
    webhooks/             # payment / provider webhooks
  sitemap*.xml/           # SEO sitemaps
  layout.tsx, globals.css, providers.tsx
src/
  lib/{domain}/           # commands, handlers, queries, dto, mappers
  modules/                # cross-domain services (billing, identity, …)
  components/
  hooks/
  i18n/
  notifications/
  queue/
  workers/
  generated/prisma/
prisma/
  schema.prisma
  migrations/
types/                    # global .d.ts
```

**Import aliases:** `@/lib/*`, `@/components/*`, `@/hooks/*`, etc. map under `src/`; `@/*` resolves to the app package root — prefer specific prefixes (see `tsconfig.json`).

---

## Conventions (short)

- **APIs and JSON:** camelCase (see `` `.cursor/rules/naming-conventions.mdc` `` at monorepo root, relative to repo checkout).
- **Boundaries:** Zod validation in `commands/*.schema.ts`; handlers return structured results; routes map to HTTP.
- **Client data:** use `useApiQuery` for authenticated GETs, not raw `useSWR` by default.
- **Currency in UI:** SAR (Saudi Riyal), not USD.
- **Likes/reactions:** aggregate in list/detail payloads; avoid N+1 API calls (see `` `.cursor/rules/likes-performance-anti-patterns.mdc` `` at monorepo root).
- **Users on content:** load via relations, not denormalized author columns (see `` `.cursor/rules/no-denormalized-user-fields.mdc` `` at monorepo root).

---

## Quality gates

Before opening a PR for substantive changes:

```bash
pnpm typecheck:tsc
pnpm test
pnpm build # optional but recommended; CI builds production
```

---

## Deployed environments (typical)

| Environment | App URL                             |
| ----------- | ----------------------------------- |
| Production  | `https://app.experts.com.sa`        |
| Staging     | `https://app.stg.experts.com.sa`    |
| Canary      | `https://app.canary.experts.com.sa` |
| Local       | `http://localhost:3025`             |

Docker under `` `docker/` `` (relative to **monorepo** root) targets deployment parity, not the default local dev loop.

---

## Related packages

Paths relative to **monorepo root**:

- `` `apps/experts-realtime/` `` — WebSocket gateway (optional).
- `` `apps/experts-prisma/` `` — container-oriented migrate/deploy helpers.
- `` `apps/experts-os/` `` — native iOS app.

---

## Contributing

Follow [[Projects/Experts/CONTRIBUTING|CONTRIBUTING.md]] (monorepo root; vault mirror). For command and style expectations, see AGENTS.md (this app).

**Native client:** API consumer docs and product context live under Experts OS.

---

## Course exams vs module quizzes (status)

Product intent: exams differ from quizzes mainly by **placement** (course-level vs inside modules), **stakes**, **policy** (retries / resets), **UX** (serious framing, countdown, results, certificate linkage), and **reporting** (milestone vs list item). Two engineering options are on the table: extend the **existing quiz model** with something like `practice | graded | final_exam`, or keep a **separate exam entity** only when advanced exam-only features justify it.

**Shipped in repo (April 2026):** separate **`CourseExam`** model plus creator CRUD, catalog `exams[]`, and curriculum **inline** exam editor (alongside module / lesson / quiz). **Not shipped:** learner exam flow, attempt policy, certificate/completion wiring, milestone reporting, or unified `assessmentKind` on quizzes.

Session note with full criteria table and gaps: [[Raw/sources/2026-04-17-experts-exams-vs-quizzes-curriculum]].

---

## Contents (start here)

**This page is the single entry point for Experts App.** From here:

- **Overview** — [[Projects/Experts/Experts App/project|project]] · [[Projects/Experts/Experts App/intro|intro]] · [[Projects/Experts/Experts App/STRUCTURE|STRUCTURE]]
- **Docs index** — [[Projects/Experts/Experts App/docs|docs]] (reference / designs / guides, live) · [[Projects/Experts/Experts App/docs/reference/experts-product-overview|product overview]]
- **Working surfaces** — [[Projects/Experts/Experts App/Bugs & Ops|Bugs & Ops]] · [[Projects/Experts/Experts App/Plans & Sessions|Plans & Sessions]] · [[Projects/Experts/Experts Dashboard|⚠ Dashboard]]
- **Maps** — [[Projects/Experts/Experts App/Experts App Map.canvas|Experts App Map]] · [[Projects/Experts/Experts App/Payments Flow.canvas|Payments Flow]]
- **To-do** — [[Projects/Experts/to-do|active to-do]]

## Project docs

- [[Projects/Experts/DEVELOPER_GUIDE|Developer guide]]
## LLM Entry Points

- Status: Web app project hub.
- Start here: this entity hub, then the project-local docs below.
- [[Projects/Experts/Experts App/project]]
- [[Projects/Experts/DEVELOPER_GUIDE]]
- [[Projects/Experts/Experts App/docs]]
- [[Projects/Experts/Experts App/Bugs & Ops]]
- [[Projects/Experts/Experts App/Plans & Sessions]]
- Actions: [[Actions/Action-Tracker]]
- Decisions: [[Decisions/Decision-Log]]

## Update Rules

- Keep this hub concise and durable.
- Put detailed working context under `Projects/`.
- Put reusable ideas under [[Concepts]].
- Put source-derived summaries under [[Summaries]].
