---
title: "Experts — Developer guide (monorepo)"
date: "2026-04-11"
tags: ["project/experts", "topic/developer-guide"]
category: "projects/experts"
type: "index"
repo_root: /Users/ahmedsulaimani/projects/experts/apps/experts-app
monorepo_root: /Users/ahmedsulaimani/projects/experts
updated: "2026-07-15"
---

# Experts — Developer guide (monorepo)

This note is the **vault entry point** for **full-stack architecture** across the Experts monorepo: **web app** (`apps/experts-app`), **in-app workers and queues**, **realtime gateway**, **Prisma deploy package**, and **native Experts OS**. Day-to-day commands and file-level conventions: AGENTS.md. Product depth, SEO, and checklists: CLAUDE.md.

On disk, authoritative code lives in [`logi-x/experts`](https://github.com/logi-x/experts). Paths like `` `apps/experts-app/...` `` are relative to the **monorepo root** unless labeled **experts-app root** (the `apps/experts-app` package directory).

---

## Table of contents

1. [What this platform is](#1-what-this-platform-is)
2. [Monorepo map — all packages](#2-monorepo-map--all-packages)
3. [`apps/experts-app` — web LMS](#3-appsexperts-app--web-lms)
4. [Experts workers and queues (inside `experts-app`)](#4-experts-workers-and-queues-inside-experts-app)
5. [`apps/experts-realtime`](#5-appsexperts-realtime)
6. [`apps/experts-prisma`](#6-appsexperts-prisma)
7. [`apps/experts-os` — native client](#7-appsexperts-os--native-client)
8. [Runtime requirements](#8-runtime-requirements)
9. [Quick start](#9-quick-start)
10. [APIs and domain layer](#10-apis-and-domain-layer)
11. [Data, auth, and integrations](#11-data-auth-and-integrations)
12. [Internationalization and product conventions](#12-internationalization-and-product-conventions)
13. [Testing and quality gates](#13-testing-and-quality-gates)
14. [Deployment and Docker](#14-deployment-and-docker)
15. [Documentation map](#15-documentation-map)

---

## 1. What this platform is

**Experts** is an online learning platform (LMS): courses, enrollments, events, community, billing, admin and creator tooling, certificates, and more.

**Surfaces today:**

| Surface              | Package                                                                                      | Role                                                                 |
| -------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Web**              | [`apps/experts-app`](https://github.com/logi-x/experts/tree/main/apps/experts-app)           | Next.js UI, `app/api/v1` REST, Prisma, NextAuth, BullMQ workers      |
| **Realtime**         | [`apps/experts-realtime`](https://github.com/logi-x/experts/tree/main/apps/experts-realtime) | Optional WebSocket server (Redis pub/sub, presence)                  |
| **Native**           | [`apps/experts-os`](https://github.com/logi-x/experts/tree/main/apps/experts-os)             | SwiftUI **Experts OS** (iOS / Apple platforms) against the same APIs |
| **Migrations (ops)** | [`apps/experts-prisma`](https://github.com/logi-x/experts/tree/main/apps/experts-prisma)     | Prisma **migrate deploy** / **db:fresh** in CI/Docker-style flows    |

**Historical note:** the platform **migrated away from a separate Laravel API and MySQL** to full-stack Next.js + PostgreSQL. Docs that still describe Laravel as the primary API are obsolete unless you are touching legacy migration artifacts.

---

## 2. Monorepo map — all packages

| Path                                                                                                                     | Role                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| [`apps/experts-app/`](https://github.com/logi-x/experts/tree/main/apps/experts-app)                                      | **Main application** — Next.js 16, Prisma, APIs, UI, **workers** (see §4), Vitest, Playwright                           |
| [`apps/experts-realtime/`](https://github.com/logi-x/experts/tree/main/apps/experts-realtime)                            | **Optional** WebSocket gateway (Redis pub/sub); separate dev script from root                                           |
| [`apps/experts-prisma/`](https://github.com/logi-x/experts/tree/main/apps/experts-prisma)                                | **Optional** Prisma CLI + schema/migrations mirror for **containerized migrate** (see §6)                               |
| [`apps/experts-os/`](https://github.com/logi-x/experts/tree/main/apps/experts-os)                                        | **Native** Experts OS (Swift / Xcode); not part of the Node web toolchain                                               |
| [`docker/`](https://github.com/logi-x/experts/tree/main/docker)                                                          | Compose and deployment-oriented configs (staging / workers / parity — **not** the default local web loop)               |
| [`.github/workflows/`](https://github.com/logi-x/experts/tree/main/.github/workflows)                                    | CI (install, lint, test, build for `experts-app`, etc.)                                                                 |
| [`STRUCTURE.md`](https://github.com/logi-x/experts/blob/main/STRUCTURE.md) · [[Projects/Experts/Experts App/STRUCTURE    | vault mirror]]                                                                                                          | **Course-domain** notes (not a full repo tree) |

**End-to-end data flow (simplified):** browsers and **Experts OS** call **`experts-app`** HTTP APIs; optional **WebSocket** clients connect to **`experts-realtime`**, which bridges **Redis** channels the app publishes to; **workers** inside **`experts-app`** consume **BullMQ** jobs backed by the same **Redis**; both app and workers use **PostgreSQL** via Prisma.

---

## 3. `apps/experts-app` — web LMS

Paths below are relative to **`apps/experts-app/`** (experts-app root).

### 3.1 High-level layout

| Area                       | Location                          | Notes                                                          |
| -------------------------- | --------------------------------- | -------------------------------------------------------------- |
| App Router & layouts       | `app/`                            | Pages, layouts, route handlers — **not** under `src/`          |
| Locale routing             | `app/(i18n)/`                     | Locales `en`, `ar`, `es`; shared implementations in `_shared/` |
| Versioned HTTP API         | `app/api/v1/`                     | Primary REST surface for web and native clients                |
| Auth & misc API            | `app/api/`                        | NextAuth, webhooks, non-v1 routes as needed                    |
| Domain logic               | `src/lib/{domain}/`               | Commands, handlers, queries, DTOs, mappers (CQRS-style)        |
| Cross-cutting modules      | `src/modules/`                    | Billing, identity, learning, permissions, etc.                 |
| UI                         | `src/components/`                 | Domain folders + `ui/` (shadcn-style primitives)               |
| Hooks                      | `src/hooks/`                      | Includes `use-api-query` and feature hooks                     |
| i18n                       | `src/i18n/`                       | Messages, `request.ts`, next-intl wiring                       |
| Prisma schema & migrations | `prisma/`                         | **Source of truth** for schema evolution during normal dev     |
| Generated Prisma client    | `src/generated/prisma/`           | Output of `prisma generate`                                    |
| Global types               | `types/`                          | Ambient `.d.ts` where used                                     |
| Notifications & email      | `src/notifications/`              | Templates, registry, notification service                      |
| Queues & workers           | `src/queue/`, `src/workers/`      | BullMQ, PDF/ZATCA workers (§4)                                 |
| Tests                      | `src/**/__tests__/`, `tests/e2e/` | Vitest; Playwright for E2E                                     |

### 3.2 Locale pattern (i18n)

- **User-facing routes** live under `app/(i18n)/{locale}/...` as thin wrappers.
- **Implementations** live under `app/(i18n)/_shared/...` and are re-exported per locale.
- Strings live in **`src/i18n/messages/{locale}/`** (often split by domain).

### 3.3 Import aliases

[`apps/experts-app/tsconfig.json`](https://github.com/logi-x/experts/blob/main/apps/experts-app/tsconfig.json) maps `@/*` to the app package root, with narrower aliases (`@/lib/*` → `src/lib/*`, etc.). Prefer explicit prefixes so paths resolve predictably.

---

## 4. Experts workers and queues (inside `experts-app`)

There is **no** separate `apps/experts-workers` package. **Workers** are the **Node processes** started from **`apps/experts-app`**, using **BullMQ** and **Redis**, with code under:

- `` `src/workers/` `` — e.g. PDF and ZATCA entrypoints
- `` `src/queue/` `` — queue definitions and maintenance scripts

[`apps/experts-app/package.json`](https://github.com/logi-x/experts/blob/main/apps/experts-app/package.json) exposes scripts such as:

| Script                                    | Purpose                                                                                              |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `pnpm worker:pdf` / `worker:pdf:test`     | PDF generation worker                                                                                |
| `pnpm worker:zatca` / `worker:zatca:test` | ZATCA-related worker                                                                                 |
| `pnpm queue:clear` (+ `:test`)            | Clear queues (expects `REDIS_URL`)                                                                   |
| `pnpm all`                                | Dev server plus selected workers and email preview (see `concurrently` definition in `package.json`) |

Run only what you need; workers require **Redis** and correct **`.env`** / **`.env.test`**.

---

## 5. `apps/experts-realtime`

Standalone **WebSocket** service: **ws** + **ioredis**, **jose** for connection verification, Redis pub/sub for channel fan-out and presence-style helpers.

| Concern          | Detail                                                                                                      |
| ---------------- | ----------------------------------------------------------------------------------------------------------- |
| **Default port** | `3026` — from `PORT` or `REALTIME_PORT` (see `src/server.ts`)                                               |
| **Redis**        | `REDIS_URL` (defaults to `redis://127.0.0.1:6379`)                                                          |
| **Repo**         | [`apps/experts-realtime`](https://github.com/logi-x/experts/tree/main/apps/experts-realtime)                |
| **Root scripts** | `pnpm experts:realtime:dev` · `experts:realtime:build` · `experts:realtime:start` · `experts:realtime:test` |

Clients subscribe to Redis-backed channels; message shapes are JSON with a `type` field (see server comments in-repo). Coordinate with web app feature flags and env for **which** host the browser uses in each environment.

---

## 6. `apps/experts-prisma`

A **small Prisma-only package** used to run **`prisma migrate deploy`** and **`migrate reset` / db:fresh** in **Docker** and **root** shortcuts, without pulling the full Next.js app into the image.

| Concern          | Detail                                                                                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Schema**       | Own `prisma/schema.prisma` and `prisma/migrations/` — kept in sync with **`experts-app`** (same database model; coordinate schema changes across both trees) |
| **Env**          | `DATABASE_URL`, optional `SHADOW_DATABASE_URL` (`prisma.config.ts`)                                                                                          |
| **Root scripts** | `pnpm experts:prisma:deploy` · `pnpm experts:prisma:fresh`                                                                                                   |
| **Image**        | [`Dockerfile`](https://github.com/logi-x/experts/blob/main/apps/experts-prisma/Dockerfile) — slim Node image, `pnpm` install, `ENTRYPOINT ["pnpm"]`          |

**Day-to-day development:** prefer **`apps/experts-app`** `pnpm db:migrate` / `db:push` / `db:seed` as documented in AGENTS. Use **`experts-prisma`** when you are working on **deploy pipelines** or **resetting** via the dedicated package.

---

## 7. `apps/experts-os` — native client

**Experts OS** is the **SwiftUI** application (Xcode project under `apps/experts-os`). It consumes the **same versioned HTTP APIs** as the web app (e.g. `app/api/v1/...` on your configured base URL), with native navigation, session, and design-system parity goals documented in the vault.

| Resource             | Link                                                                             |
| -------------------- | -------------------------------------------------------------------------------- | ------------------------------------- |
| **Entity hub**       | [[Entities/Projects/Experts OS                                                   | Experts OS]]                          |
| **Vault docs**       | [[Projects/Experts/Experts OS/docs/reference/Glossary — Experts OS| Experts OS docs (start at glossary)]] |
| **Architecture**     | [[Projects/Experts/Experts OS/docs/reference/Architecture — Experts OS| Architecture — Experts OS]]           |
| **Networking / API** | [[Projects/Experts/Experts OS/docs/reference/Networking and API — Experts OS| Networking and API — Experts OS]]     |
| **Monorepo tree**    | [`apps/experts-os`](https://github.com/logi-x/experts/tree/main/apps/experts-os) |

Native work is **out of scope** for most web-only tasks; treat **Experts OS** as a **separate Xcode toolchain** (Swift, XCTest) that **shares contracts** with the Next.js API.

---

## 8. Runtime requirements

- **Node.js** `>= 22` — root [`package.json` engines](https://github.com/logi-x/experts/blob/main/package.json)
- **pnpm** `10.x` — root `packageManager`
- **PostgreSQL** — Prisma; URL in **`apps/experts-app/.env`**
- **Redis** — BullMQ workers, **experts-realtime**, and some product features when enabled

Secrets live under **`apps/experts-app/`** (`.env`, `.env.test`, `.env.e2e`); they are not committed. **experts-realtime** and **experts-prisma** use their own env as documented in each package.

---

## 9. Quick start

### Web app (from monorepo root)

```bash
pnpm install
cd apps/experts-app
cp .env.example .env   # then adjust for your machine
pnpm db:migrate        # or db:push — follow team practice
pnpm db:seed           # optional
pnpm dev               # http://localhost:3025
```

### Convenience scripts (monorepo root)

```bash
pnpm experts:dev
pnpm experts:build
pnpm experts:start
pnpm experts:lint
pnpm experts:test
pnpm experts:typecheck:tsc
```

### Optional realtime

```bash
pnpm experts:realtime:dev
```

---

## 10. APIs and domain layer

### 10.1 Request flow (`app/api/v1/...`)

1. **Authenticate** — `auth()` (and role helpers where applicable).
2. **Validate** — Zod in `src/lib/{domain}/commands/*.schema.ts`.
3. **Execute** — handlers in `src/lib/{domain}/handlers/*.handler.ts`.
4. **Respond** — DTOs/mappers; **camelCase** JSON.

### 10.2 Client data fetching

Use **`useApiQuery`** ([`src/hooks/use-api-query.ts`](https://github.com/logi-x/experts/blob/main/apps/experts-app/src/hooks/use-api-query.ts)) in Client Components — SWR + auth readiness. Avoid raw `useSWR` for authenticated app APIs unless justified.

### 10.3 Reference implementations

See the **Canonical Reference Files** table in AGENTS.md (paths relative to **experts-app** root).

---

## 11. Data, auth, and integrations

### 11.1 Database

- **ORM:** Prisma 7 + `@prisma/adapter-pg`
- **Migrations:** primary workflow under **`apps/experts-app`**; deploy via CI or **`experts-prisma`** (§6)

### 11.2 Authentication

- **NextAuth v5** — [`src/lib/auth.ts`](https://github.com/logi-x/experts/blob/main/apps/experts-app/src/lib/auth.ts)
- **Server:** `auth()` in routes and RSCs; **Client:** session hooks as used in codebase
- **Native:** Experts OS uses its own session stores against the same HTTP auth endpoints — see vault **Authentication and session** doc

### 11.3 Payments and billing

Stripe and regional providers (e.g. Noon, Tabby) under `src/lib/payments`, `src/modules/billing`, and related routes. Env keys and webhooks are sensitive.

### 11.4 Storage and media

S3-compatible clients, presigning, and media libraries as used in domain code — follow existing upload and URL patterns.

---

## 12. Internationalization and product conventions

- **Locales:** `en`, `ar`, `es` — RTL for Arabic

### SEO

Metadata under `` `src/lib/metadata/` `` (experts-app root); sitemaps / `robots` as App Router routes. Workflow: CLAUDE.md and SEO-guide (monorepo: `` `.cursor/rules/SEO-guide.mdc` ``).

---

## 13. Testing and quality gates

| Layer              | Tool       | Typical command (from `apps/experts-app`)            |
| ------------------ | ---------- | ---------------------------------------------------- |
| Unit / integration | Vitest     | `pnpm test`, `pnpm test:watch`, `pnpm test:coverage` |
| E2E                | Playwright | `pnpm test:e2e`                                      |
| Lint               | ESLint     | `pnpm lint` or `pnpm experts:lint` from root         |
| Typecheck          | TypeScript | `pnpm typecheck:tsc`                                 |

Use **`NODE_ENV=test`** and **`.env.test`** where applicable (see AGENTS). **experts-realtime** has its own **Vitest** scripts via root `pnpm experts:realtime:test`.

---

## 14. Deployment and Docker

- **Local web** default: **Node + PostgreSQL** (+ **Redis** when using workers or realtime). **Docker is not required** for the inner loop.
- **`docker/`** targets **staging / canary / production** parity, workers, and data services.
- **Typical URLs:** production `app.experts.com.sa`, staging `app.stg.experts.com.sa`, canary `app.canary.experts.com.sa`.

CI builds **`apps/experts-app`** (see `.github/workflows/`).

---

## 15. Documentation map

| Document                                                | Purpose                                                                                   |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **This note**                                           | Monorepo architecture — **start here** (vault: `Projects/Experts/DEVELOPER_GUIDE.md`)     |
| [[Projects/Experts/Experts App/docs/guides/guides-index      | Guides index]]                                                                            | Topic guides (payments, shared forms, etc.)                                                                    |
| [[Projects/Experts/Experts App/project                 | project.md]]                                                                             | Compact directory map and stack                                                                                |
| [[Projects/Experts/CONTRIBUTING                         | CONTRIBUTING.md]] · [GitHub](https://github.com/logi-x/experts/blob/main/CONTRIBUTING.md) | Branching and PR expectations                                                                                  |
| [[Projects/Experts/Experts App/STRUCTURE                | STRUCTURE.md]]                                                                            | Course-domain structure (not full repo tree)                                                                   |

## Links

- [[Entities/Projects/Experts]]
- [[Entities/Projects/Experts App|Experts App]]
- [[Entities/Projects/Experts OS|Experts OS]]

When rules disagree with code, **trust the code** and update docs or rules in the same change.

---

_Last aligned with monorepo layout and root `package.json` scripts as of April 2026. If you add a new app under `apps/` or change API versioning, update this guide in the same PR._
