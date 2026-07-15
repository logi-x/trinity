---
title: "Experts App — Claude project context"
date: "2026-04-11"
tags: ["project/experts", "topic/-project"]
category: "projects/experts"
up: "[[Entities/Projects/Experts App]]"
updated: "2026-07-15"
---

# Experts App — Claude project context

↑ [[Entities/Projects/Experts App|Experts App]]

**Keep in sync with:** `CLAUDE.md` (canonical detail: commands, SEO, checklists, references).  
**Agent conventions:** `AGENTS.md`.  
**Working style / product context:** [`intro.md`](intro.md).

---

## Repository layout (`experts/`)

**pnpm** (Node ≥ 22), **app-first**: primary work in `apps/experts-app`; repo root holds delegation scripts in `package.json`.

```txt
experts/
├── apps/
│   ├── experts-app/       # Primary: Next.js 16 full-stack (this app)
│   ├── experts-realtime/  # WebSocket + Redis pub/sub — default port 3026
│   └── experts-prisma/    # Prisma tooling / migrate helpers
├── docker/                # Staging / canary / production only (not local dev)
├── .github/workflows/
└── package.json           # e.g. pnpm experts:dev → apps/experts-app
```

Mobile clients, if any, live outside this repo; API contracts target this app’s routes.

---

## Tech stack (experts-app)

| Layer        | Stack                                                                                    |
| ------------ | ---------------------------------------------------------------------------------------- |
| Framework    | Next.js 16 (App Router, API routes, Turbopack in dev)                                    |
| UI           | React 19, Tailwind CSS v4, HeroUI v3 (`@heroui/react`) primary, shadcn/Radix fallback    |
| Data         | PostgreSQL, Prisma 7 (`@prisma/adapter-pg`), generated client in `src/generated/prisma/` |
| Auth         | NextAuth v5 (`src/lib/auth.ts`) — credentials + OAuth (e.g. Google, GitHub, Apple)       |
| i18n         | next-intl — locales `en`, `ar`, `es`; messages under `src/i18n/messages/`                |
| Client fetch | SWR via **`useApiQuery`** (`src/hooks/use-api-query.ts`); prefer over raw `useSWR`       |
| Validation   | Zod at API boundary (`src/lib/{domain}/commands/*.schema.ts`)                            |
| Async jobs   | Redis + BullMQ; workers under `src/workers/`                                             |
| Tests        | Vitest; E2E with Playwright (`test:e2e` scripts)                                         |
| Email        | React Email templates under `src/notifications/channels/email/templates/`                |

**Architecture:** CQRS-style domain folders under `src/lib/{domain}/` (commands, handlers, queries, dto, mappers). API routes under `app/api/v1/{domain}/` delegate to handlers and return camelCase DTOs.

---

## App directory map (paths from `apps/experts-app/`)

- **`app/`** — App Router pages and route handlers; **`app/(i18n)/`** locale trees + **`_shared/`** implementations.
- **`app/api/v1/`** — Versioned REST API; **`app/api/webhooks/`** — payment webhooks.
- **`src/lib/`** — Domains, `auth.ts`, `prisma.ts`, integrations (Stripe, R2, Redis, …).
- **`src/modules/`** — Cross-cutting services (billing, identity, learning, …).
- **`src/components/`**, **`src/hooks/`**, **`src/i18n/`**, **`src/notifications/`**, **`src/queue/`**, **`src/workers/`**.
- **`prisma/`** — `schema.prisma`, migrations.
- **`types/`** — Global `.d.ts` types.

**Import aliases:** Defined in `tsconfig.json`. Prefer **`@/lib/...`**, **`@/components/...`**, **`@/hooks/...`**, etc. The catch-all `@/*` maps to the **app root** (`./*`), not only `src/` — see `tsconfig.json` for explicit `@/lib/*`, `@/types/*`, etc.

---

## Realtime (`experts-realtime`)

Separate Node service: WebSocket endpoint, Redis pub/sub, JWT from the app (`POST /api/v1/internal/realtime/token`). Local default **3026**. Contract: [realtime-contract.md](./docs/V4/realtime-contract.md). Root script: `pnpm experts:realtime:dev`.

---

## Commands (quick reference)

From repo root: `pnpm experts:app:dev`, `pnpm experts:server:dev`, `pnpm experts:realtime:dev`, `pnpm build`, `pnpm test`, `pnpm typecheck`.

From `apps/experts-app`: `pnpm dev` (3025), `pnpm db:migrate`, `pnpm db:seed`, `pnpm test`, `pnpm test:e2e`. Full list: **`CLAUDE.md`**.

---

## Code quality norms

- **Tailwind v4 only** for styling (no inline styles / CSS modules for product UI).
- **camelCase** for APIs and TypeScript (see naming-conventions (Experts)).
- **`auth()`** / **`requireAdmin()`** patterns for server routes; **`validateUUID`** for id params where used.
- **Toasts:** `sonner`; server actions / mutations often return `{ serverError }` for UI.

---

## Migration context (historical)

Laravel API and multi-app frontend were retired: **single Next.js app**, **PostgreSQL + Prisma**, **`@/*`-style imports** inside the app (no `@experts/*` workspace packages). Docker is for deployment environments, not required for local app dev.

---

## Working surfaces (vault hubs)

- [[Experts Dashboard|⚠ Experts Dashboard]] — cross-folder triage: overdue actions, open high/critical bugs, decisions due for review + all `#experts` notes.

Live indexes over the vault's `Raw/` ingest zone — surfaced, not moved (the routine fleet
hardcodes these paths):

- [[Projects/Experts/Experts App/Bugs & Ops|Bugs & Ops]] — bug tracker (`Raw/bugs/`) + agent/fleet state.
- [[Projects/Experts/Experts App/Plans & Sessions|Plans & Sessions]] — implementation plans (`Raw/plans/`) + session/research sources (`Raw/sources/`).
- [[Projects/Experts/Experts App/docs|docs]] — curated reference / designs / guides.
- [[Projects/Experts/Experts App/Experts App Map.canvas|Experts App Map]] — visual map: entry → hubs → architecture → domains.

## Further reading

- **`CLAUDE.md`** — SEO workflow, feature checklists, deployment, `.planning/codebase/*`, Cursor rules.
- **`AGENTS.md`** — Ralph/agent paths, quality gates, HeroUI doc index.
