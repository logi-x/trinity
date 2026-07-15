---
title: "intro.md"
date: "2026-04-11"
tags: ["project/experts", "topic/-intro"]
category: "projects/experts"
up: "[[Entities/Projects/Experts App]]"
updated: "2026-07-15"
---

↑ [[Entities/Projects/Experts App|Experts App]]


Purpose & context

Ahmed is building **Experts** — a Saudi Arabia–focused LMS / education platform: courses, certifications, affiliates, payments (SAR), and creator tools. End users, instructors, and admins; regional needs include **SAR**, gateways such as **Stripe, Noon, Tabby**, **RTL**, and **Arabic** (plus **en** / **es** in-app via next-intl).

The product is a **single full-stack Next.js app** (`apps/experts-app`) with **PostgreSQL + Prisma** and **NextAuth v5** — not a separate Laravel API. The repo also includes **WebSocket realtime** (`apps/experts-realtime`, Redis pub/sub, default port 3026), optional **Prisma helpers** (`apps/experts-prisma`), and a **thin repo root** with **pnpm** scripts that delegate into `experts-app`. Legacy multi-app (`experts-admin`, `experts-portal`, `experts-auth`) and **`@experts/*` workspace packages** are **gone**; code lives under `app/` and `src/` with `tsconfig` aliases (`@/lib`, `@/components`, etc.).

**Canonical docs for agents:** [`project.md`](project.md) (structure + stack), `CLAUDE.md` (commands, SEO, checklists), `AGENTS.md` (paths, gates, HeroUI index).

Active domains include course discovery, certifications, affiliate analytics, billing/membership, admin, creator flows, auth, and org management — implemented as **API routes** + **CQRS-style** handlers under `src/lib/{domain}/`.

---

Current state

UI work leans on **HeroUI v3** (`@heroui/react`) and **Tailwind CSS v4**; **shadcn/Radix** where HeroUI does not cover a pattern. Client data fetching should use **`useApiQuery`** (SWR + auth), not ad-hoc `useSWR` for app APIs. **Docker** is for staging/canary/production; local app dev is typically **Node on the host** (e.g. `pnpm dev` on port **3025**).

---

On the horizon

Feature work continues in one codebase: shared patterns (hooks, components) under `src/`, versioned APIs under `app/api/v1/`. Testing: **Vitest** (unit/integration), **Playwright** (E2E). Realtime/notifications may use **`experts-realtime`** + app token contract ([realtime-contract.md](./docs/V4/realtime-contract.md)).

---

Key learnings & principles

- **Read before restyling:** Check `app/globals.css`, existing components, and tokens before introducing conflicting Tailwind or one-off CSS.
- **Restore look, keep wins:** Prefer keeping performance/architecture improvements while restoring intended visuals if a change regresses UI.
- **Clean over noisy UI:** Favor clear, functional layouts over heavy decoration (e.g. org/settings-style pages).
- **Prisma / API boundaries:** Validate with **Zod** in domain commands; avoid business logic in thin route files; use handlers + DTO mappers.
- **SWR / `useApiQuery` keys:** Keys must reflect **pagination, filters, and locale** so cache and refetch stay correct.
- **Effects & dependencies:** Unstable objects in dependency arrays and circular effects are the usual cause of infinite loops in list/filter UIs.
- **Docker + Turbopack:** **glibc**-based images for build stages where native tooling matters; Alpine/musl can force slower fallbacks for some toolchains.

---

Approach & patterns

- Ahmed often points at a component or short brief and expects **production-ready** output: TypeScript, a11y, sensible memoization, and polish.
- **Extract subcomponents** (`StatusChip`, `LevelCard`, …) for reuse and clarity.
- **Hooks** for non-trivial logic; API hooks go through **`useApiQuery`** with correct keys and mutations.
- **Filtering:** Client-side for small sets; server-side + **URL state** for large lists and deep links.
- **Project tracking:** May use structured tasks elsewhere; in-repo source of truth is code + `CLAUDE.md` / Experts project rules _(mirrors `.cursor/rules` in the clone)_.

---

Tools & resources

- **App:** Next.js **16**, React **19**, TypeScript, Tailwind **v4**, HeroUI **v3**, Framer Motion / Motion, **next-intl**, **Zod**, SWR via **`useApiQuery`**, Recharts, React Hook Form, **Sonner**, Prisma **7**, NextAuth **v5**, Redis/BullMQ workers.
- **Data:** PostgreSQL; Prisma client in `src/generated/prisma/`.
- **Tests:** Vitest; Playwright for E2E (`pnpm test:e2e` in app).
- **Monorepo:** pnpm, Turbo; primary package **`@logi-x/experts-app`**.

Paths in this file are **repo-relative** (`apps/experts-app/...`). Adjust for your machine (WSL, macOS, etc.).
