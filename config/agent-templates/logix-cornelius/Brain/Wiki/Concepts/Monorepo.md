---
title: "Monorepo"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "topic/monorepo"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Monorepo.md"
---

# Monorepo — Experts Turborepo Structure

The Experts platform lives in a single `logi-x/experts` monorepo managed with **pnpm workspaces** and **Turborepo**.

## Package Map

| Package                  | Role                                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------------ |
| `apps/experts-app/`      | **Main app** — Next.js 16, Prisma, REST API, UI, BullMQ workers, Vitest, Playwright              |
| `apps/experts-realtime/` | **Optional** — standalone WebSocket gateway (ws + ioredis + jose)                                |
| `apps/experts-prisma/`   | **Optional** — slim Prisma-only image for `migrate deploy` in Docker/CI                          |
| `apps/experts-os/`       | **Native** — SwiftUI Experts OS (Xcode; separate toolchain from Node)                            |
| `docker/`                | Staging/production compose configs — not used for local web dev                                  |
| `.github/workflows/`     | CI pipelines (install, lint, test, build for experts-app)                                        |

## Runtime Requirements

- **Node.js** `>= 22`
- **pnpm** `10.x` (set in root `packageManager`)
- **PostgreSQL** — Prisma; URL in `apps/experts-app/.env`
- **Redis** — BullMQ workers + experts-realtime (required when running workers or realtime)

## Root Convenience Scripts

All `pnpm experts:*` scripts at the monorepo root delegate into `apps/experts-app`:

```bash
pnpm experts:dev              # Next.js dev — port 3025
pnpm experts:build            # Production build
pnpm experts:start            # Production start
pnpm experts:lint             # ESLint
pnpm experts:format           # Prettier check
pnpm experts:test             # Vitest (needs apps/experts-app/.env.test)
pnpm experts:typecheck:tsc    # tsc --noEmit
pnpm experts:realtime:dev     # WebSocket realtime — port 3026
pnpm clean:node_modules       # Remove all node_modules
```

## Day-to-Day from `apps/experts-app/`

```bash
pnpm dev                      # Port 3025, Turbopack
pnpm build && pnpm start
pnpm test / test:watch / test:coverage
pnpm db:migrate               # Prisma migrate dev
pnpm db:push                  # Prisma push (schema sync without migration)
pnpm db:seed                  # Seed database
pnpm db:studio                # Prisma Studio
pnpm prisma generate          # Regenerate Prisma client
```

## Workers (inside experts-app)

Workers are **not** a separate package. They run as Node processes started from `apps/experts-app`, using BullMQ + Redis:

```bash
pnpm worker:pdf               # PDF generation worker
pnpm worker:zatca             # ZATCA e-invoicing worker
pnpm queue:clear              # Clear queues (requires REDIS_URL)
```

See [[Wiki/Concepts/ZATCA]] for ZATCA worker architecture.

## `apps/experts-prisma` — When to Use

Use only for **deploy pipelines** or **Docker-style resets**. For day-to-day development always use `apps/experts-app` migrate/push/seed commands. Both packages share the same Prisma schema — keep them in sync when making schema changes.

```bash
pnpm experts:prisma:deploy    # prisma migrate deploy (CI/Docker)
pnpm experts:prisma:fresh     # migrate reset + seed
```

## End-to-End Data Flow

```
Browser / Experts OS
  └─ HTTP → apps/experts-app (port 3025) — Next.js + API routes
                └─ PostgreSQL (Prisma)
                └─ Redis (BullMQ jobs + pub/sub events)
                     └─ apps/experts-realtime (port 3026) — WebSocket fan-out
                     └─ BullMQ workers (PDF, ZATCA) — inside experts-app process
```

## Quality Gate (before any commit)

```bash
pnpm typecheck && pnpm test && pnpm build 2>&1 | tail -20
```

## Tooling gotchas

- `apps/experts-app/tsconfig.json` includes `.next/dev/types/**/*.ts`. The husky pre-push
  hook (`pnpm experts:typecheck:tsc`) fails with `TS6053: File '.next/dev/types/...' not found`
  when `tsconfig.tsbuildinfo` references stale paths (e.g. after deleting route files) but
  the corresponding `.next/dev/types` entries no longer exist. Fix: delete
  `apps/experts-app/tsconfig.tsbuildinfo` and rerun the typecheck. The next dev/build run
  regenerates the dev types. Confirmed 2026-05-13 during the security incident cleanup.

## Related

- [[Wiki/Concepts/WebSockets]]
- [[Wiki/Concepts/ZATCA]]
- [[Projects/Experts/DEVELOPER_GUIDE]]
- [[Projects/Experts/Experts App/STRUCTURE]]
