---
title: "Experts codebase — Stack"
date: "2026-03-06"
tags: ["project/experts", "topic/planning", "tech/stack"]
category: "docs/experts-reference"
repo_root: /Users/ahmedsulaimani/projects/experts/apps/experts-app
monorepo_root: /Users/ahmedsulaimani/projects/experts
updated: "2026-07-15"
---

# Technology Stack

**Analysis Date:** 2026-03-06

## Languages

**Primary:**

- TypeScript 5.9.x - All application code (strict mode enabled)

**Secondary:**

- SQL - Prisma migrations in `prisma/migrations/`

## Runtime

**Environment:**

- Node.js (LTS) - Server-side Next.js, workers, queue processors

**Package Manager:**

- pnpm 10.30.3
- Lockfile: present (`pnpm-lock.yaml`)

## Frameworks

**Core:**

- Next.js ^16.1.6 - Full-stack framework (App Router, API Routes, Server Components)
- React ^19.2.4 - UI rendering

**Internationalization:**

- next-intl ^4.8.3 - i18n with locale routing; config at `src/i18n/request.ts`; messages at `src/i18n/messages/`; wraps Next.js config via `createNextIntlPlugin`

**Authentication:**

- next-auth ^5.0.0-beta.30 - OAuth2 + Credentials; JWT session strategy; config at `src/lib/auth.ts`

**Database ORM:**

- Prisma ^7.4.2 - Schema at `prisma/schema.prisma`; generated client at `src/generated/prisma/`
- @prisma/adapter-pg ^7.4.2 - PostgreSQL adapter with connection pooling via `pg`

**Testing:**

- Vitest ^4.0.18 - Unit and integration tests; config at `vitest.config.ts`

**Build/Dev:**

- Turbopack - Dev server bundler (`next dev --turbopack`); also used for production build (`next build --turbopack`)
- tsup ^8.5.1 - Worker bundling; config at `src/workers/tsup.config.ts`
- Repo root uses **pnpm delegation scripts** into `apps/experts-app` (no Turborepo at root)

## Key Dependencies

**Critical:**

- `swr` ^2.4.1 - Client-side data fetching with caching; wrapped by `src/hooks/use-api-query.ts`
- `bullmq` ^5.70.1 - Job queue for background workers (PDF generation, ZATCA compliance); uses Redis as broker
- `ioredis` ^5.10.0 - Redis client for BullMQ queues and caching; config at `src/lib/redis.ts`
- `argon2` ^0.44.0 - Password hashing for credentials auth
- `zod` ^4.3.6 - Request validation in API routes
- `stripe` ^20.4.0 - Payment processing SDK; client at `src/lib/stripe.ts`
- `@aws-sdk/client-s3` ^3.1002.0 - S3-compatible storage (Cloudflare R2); client at `src/lib/r2.ts`

**UI:**

- `@heroui/react` 3.0.0-beta.8 - Primary UI component library
- `@radix-ui/*` - Headless UI primitives (accordion, dialog, dropdown, select, etc.)
- TailwindCSS ^4.2.1 - Styling; PostCSS config at `postcss.config.mjs`
- `framer-motion` ^12.35.0 / `motion` ^12.35.0 - Animations
- `lucide-react` ^0.577.0 - Icon library
- `sonner` ^2.0.7 - Toast notifications
- `recharts` ^3.7.0 - Data visualization/charts
- `react-hook-form` ^7.71.2 - Form management
- `@hookform/resolvers` ^5.2.2 - Zod integration for react-hook-form

**Infrastructure:**

- `pg` ^8.19.0 - PostgreSQL client (used by Prisma adapter)
- `react-email` ^1.0.8 + `@react-email/render` ^2.0.4 - Transactional email templates
- `@react-pdf/renderer` ^4.3.2 - PDF generation for invoices/certificates
- `react-intl` (via next-intl) - Localization

**Dev Tools:**

- `@faker-js/faker` ^10.3.0 - Test data generation
- `@tanstack/react-table` ^8.21.3 - Data tables (dev dependency; used in UI)
- `playwright` ^1.58.2 - E2E testing (installed, not actively configured)
- `openai` ^6.25.0 - AI integration (dev dependency)
- `@google/genai` ^1.43.0 - Google AI integration (dev dependency)

## Configuration

**Environment:**

- `.env` / `.env.local` / `.env.staging` / `.env.canary` / `.env.test` - Per-environment config
- `.env.example` - Template listing required variables
- Required: `DATABASE_URL`, `REDIS_URL`, `AUTH_SECRET` / `NEXTAUTH_SECRET`, `STRIPE_SECRET_KEY`, `R2_ENDPOINT`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_PUBLIC_URL`, `MAILTRAP_API_KEY`, `SLACK_WEBHOOK_URL`, `TURNSTILE_SECRET_KEY`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GITHUB_ID`, `GITHUB_SECRET`, `APPLE_ID`, `APPLE_SECRET`, `OPENAI_SECRET`
- Payment-specific: `NOON_*`, `TABBY_PUBLIC_KEY`, `TABBY_MERCHANT_CODE`, `TABBY_COUNTRY`
- Test env loaded via `dotenv -e .env.test` in test scripts

**Build:**

- `next.config.ts` - Next.js config; standalone output mode; Turbopack root config; image patterns wildcard
- `tsconfig.json` - TypeScript strict mode; `ES2017` target; `bundler` module resolution; path aliases for `@/*`, `@/lib/*`, `@/components/*`, `@/hooks/*`, `@/queue/*`, `@/workers/*`, `@/notifications/*`, `@/generated/*`, etc.
- `postcss.config.mjs` - PostCSS with TailwindCSS v4 plugin
- `components.json` - shadcn/ui configuration

**TypeScript Path Aliases:**

```typescript
"@/*"             → "./*"                     // root of experts-app
"@/components/*"  → "./src/components/*"
"@/hooks/*"       → "./src/hooks/*"
"@/lib/*"         → "./src/lib/*"
"@/i18n/*"        → "./src/i18n/*"
"@/queue/*"       → "./src/queue/*"
"@/workers/*"     → "./src/workers/*"
"@/notifications/*" → "./src/notifications/*"
"@/generated/*"   → "./src/generated/*"
"@/test/*"        → "./src/test/*"
"@/types/*"       → "./types/*"
```

## Platform Requirements

**Development:**

- Node.js (LTS)
- pnpm 10.30.3
- PostgreSQL (local instance)
- Redis (local instance, default `redis://localhost:6379`)
- Port 3025 (Next.js app), Port 3030 (experts-server utility app)

**Production:**

- Docker (standalone Next.js output); base image `loogix/experts-base:production`
- Managed PostgreSQL
- Redis
- Traefik for subdomain routing
- Subdomains: `app.experts.com.sa` (prod), `app.stg.experts.com.sa` (staging), `app.canary.experts.com.sa` (canary)

---

_Stack analysis: 2026-03-06_

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
