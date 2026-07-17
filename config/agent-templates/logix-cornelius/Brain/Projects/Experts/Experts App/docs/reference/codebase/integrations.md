---
title: "Experts codebase — Integrations"
date: "2026-03-06"
tags: ["project/experts", "topic/planning", "topic/integrations"]
category: "docs/experts-reference"
repo_root: /Users/ahmedsulaimani/projects/experts/apps/experts-app
monorepo_root: /Users/ahmedsulaimani/projects/experts
updated: "2026-07-15"
---

# External Integrations

**Analysis Date:** 2026-03-06

## APIs & External Services

**Payment Gateways:**

- Stripe - Subscriptions and international card payments
  - SDK/Client: `stripe` ^20.4.0; client at `src/lib/stripe.ts`
  - Gateway implementation: `src/lib/payments/gateways/stripe/`
  - Auth env vars: `STRIPE_SECRET_KEY`
  - Subscription price IDs configured directly in `src/lib/stripe.ts` (Pro plan monthly/yearly)
  - Webhook endpoint: `app/api/webhooks/` (Stripe events)

- Noon Payments - MENA region hosted checkout
  - Client: `src/lib/payments/gateways/noon/noon.client.ts`
  - Gateway implementation: `src/lib/payments/gateways/noon/noon.gateway.ts`
  - Auth env vars: `NOON_*` (channel, category, API key)
  - Webhook endpoint: `app/api/webhooks/noon/`

- Tabby - Buy-now-pay-later (BNPL) for MENA
  - Client: `src/lib/payments/gateways/tabby/tabby.client.ts`
  - Gateway implementation: `src/lib/payments/gateways/tabby/tabby.gateway.ts`
  - Auth env vars: `TABBY_PUBLIC_KEY`, `TABBY_MERCHANT_CODE`, `TABBY_COUNTRY` (default `SA`)
  - Public vars exposed via `next.config.ts`: `NEXT_PUBLIC_TABBY_*`
  - Webhook endpoint: `app/api/webhooks/tabby/`

**Payment Orchestration:**

- All gateways unified under `src/lib/payments/payment.service.ts`
- Commerce API routes: `app/api/v1/commerce/` (billing, checkout, invoices, subscriptions, payouts, affiliates)

**Cloudflare:**

- Turnstile (CAPTCHA) - Bot protection on forms
  - Verification: `src/lib/turnstile.ts` calls `https://challenges.cloudflare.com/turnstile/v0/siteverify`
  - Client widget: `@marsidev/react-turnstile` ^1.4.2
  - Auth env vars: `TURNSTILE_SECRET_KEY`, `NEXT_PUBLIC_TURNSTILE_SITE_KEY`

**Mapping:**

- Google Maps - Location features
  - SDK: `@googlemaps/js-api-loader` ^2.0.2
  - Auth env vars: `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`

**AI / LLM (dev/optional):**

- OpenAI - `openai` ^6.25.0 (dev dependency); env var `OPENAI_SECRET`
- Google AI - `@google/genai` ^1.43.0 (dev dependency)
- ChromaDB - `chromadb` ^3.3.1 (dev dependency, vector database)

## Data Storage

**Databases:**

- PostgreSQL (primary) - All application data
  - Schemas: `public`, `billing`, `seq` (custom sequence functions)
  - Connection env var: `DATABASE_URL`
  - Client: Prisma 7.x with `@prisma/adapter-pg` and `pg` connection pool (max 10 connections)
  - Pool config: `idleTimeoutMillis: 30000`, `connectionTimeoutMillis: 5000`
  - Prisma client singleton at `src/lib/prisma.ts`
  - Test database: separate `DATABASE_URL` in `.env.test`

**File Storage:**

- Cloudflare R2 (primary object storage) - Images, videos, documents
  - SDK: `@aws-sdk/client-s3` ^3.1002.0 (S3-compatible API)
  - Client at `src/lib/r2.ts`; extended at `src/lib/storage/r2.client.ts`
  - Auth env vars: `R2_ENDPOINT`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_STATIC`, `R2_PUBLIC_URL`
  - Presigned URL support via `@aws-sdk/s3-request-presigner` ^3.1002.0

**Caching / Queue Broker:**

- Redis - Job queue broker (BullMQ) and caching
  - Client: `ioredis` ^5.10.0; singleton at `src/lib/redis.ts`
  - Connection env var: `REDIS_URL` (default `redis://localhost:6379`)
  - Graceful degradation when Redis unavailable
  - BullMQ queues defined in `src/queue/queues.ts` (currently commented out, workers run directly)

## Authentication & Identity

**Auth Provider:**

- NextAuth v5 (beta.30) - Custom multi-provider auth
  - Config: `src/lib/auth.ts`
  - Session strategy: JWT (30-day max age)
  - Session cookies: `authjs.session-token` / `__Secure-authjs.session-token`

**OAuth Providers:**

- Google OAuth2 - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
- GitHub OAuth - `GITHUB_ID`, `GITHUB_SECRET`
- Apple Sign In - `APPLE_ID`, `APPLE_SECRET`
- Credentials (email/password) - Argon2 password hashing via `argon2` ^0.44.0

**Authorization:**

- Role-based via user flags: `isAdmin`, `isInstructor` on `User` model
- Session checks in every protected API route via `auth()` from `src/lib/auth.ts`

## Monitoring & Observability

**Custom Observability:**

- Internal observer pattern at `src/lib/observability/`
- Observers: `LoggerObserver`, `DatabaseObserver`, `RedisObserver`
- `observe()` function used throughout business logic for structured event tracking
- Registered via Next.js instrumentation hook (`instrumentation.ts`)

**Error Tracking:**

- No third-party error tracking service detected (Sentry, Datadog, etc. not found)

**Logs:**

- Custom structured logger at `src/lib/logger.ts`
- Supports JSON format (`LOG_FORMAT=json`) for production log ingestion
- Browser/Node.js compatible (isomorphic)

## Notifications

**Email:**

- Mailtrap - Transactional email delivery
  - Provider: `src/notifications/channels/email/providers/mailtrap.provider.ts`
  - Templates: React Email components at `src/notifications/channels/email/templates/`
  - Auth env vars: `MAILTRAP_HOST`, `MAILTRAP_API_KEY`, `MAIL_FROM`, `MAIL_FROM_NAME`
  - Dev mode uses sandbox endpoint (`/api/send/3391112`)

**Chat / Internal Alerts:**

- Slack - Internal operational notifications
  - Provider: `src/notifications/channels/chat/` (Slack webhook)
  - Auth env var: `SLACK_WEBHOOK_URL`

**Push Notifications:**

- Push provider: `src/notifications/channels/push/providers/push.provider.ts`
- Implementation details not exposed (file empty / interface only at time of analysis)

**SMS:**

- SMS provider: `src/notifications/channels/sms/providers/sms.provider.ts`
- Implementation details not exposed (interface only at time of analysis)

**Notification Service:**

- Unified dispatch via `src/lib/notification-service.ts`
- Channel registry at `src/notifications/`

## CI/CD & Deployment

**Hosting:**

- Docker containers on self-hosted infrastructure
- Traefik reverse proxy for subdomain routing
- Multi-stage Dockerfiles: `Dockerfile` (app), `Dockerfile.worker` (workers), `Dockerfile.prsma` (Prisma migrations)

**CI Pipeline:**

- GitHub Actions with self-hosted runners
- Workflows in `.github/workflows/`
- Docker builds with Buildx

**Deployment Targets:**

| Environment | Subdomain                   |
| ----------- | --------------------------- |
| Production  | `experts.com.sa`            |
| Staging     | `app.stg.experts.com.sa`    |
| Canary      | `app.canary.experts.com.sa` |
| Development | `localhost:3025`            |

## Background Workers

**PDF Worker:**

- `src/workers/pdf/` - PDF invoice/certificate generation using `@react-pdf/renderer`
- Started via `pnpm worker:pdf`; bundled separately with tsup

**ZATCA Worker:**

- `src/workers/zatca/` - Saudi Arabia e-invoicing compliance (ZATCA/Fatoorah)
- Started via `pnpm worker:zatca`; bundled separately with tsup

**Queue Initialization:**

- BullMQ queue completion handlers initialized in `instrumentation.ts` on server start
- Workers connect independently to Redis and PostgreSQL

## Webhooks & Callbacks

**Incoming Webhooks:**

- `app/api/webhooks/` - Stripe, Noon, Tabby payment callbacks

**Realtime Sync:**

- Custom SSE / polling transport at `src/lib/realtime/`
- `RealtimeTransport` interface supports SSE, WebSockets, or polling backends
- Coordinator pattern: `src/lib/realtime/coordinator.ts`, `global-coordinator.ts`, `presence-coordinator.ts`
- No third-party realtime service (Pusher package present in devDependencies but not wired up)

## Environment Configuration

**Required env vars (all environments):**

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `AUTH_SECRET` / `NEXTAUTH_SECRET` - JWT signing secret
- `AUTH_URL` - App base URL
- `STRIPE_SECRET_KEY` - Stripe secret key
- `R2_ENDPOINT`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_PUBLIC_URL` - Cloudflare R2
- `MAILTRAP_HOST`, `MAILTRAP_API_KEY`, `MAIL_FROM`, `MAIL_FROM_NAME` - Email
- `SLACK_WEBHOOK_URL` - Slack notifications
- `TURNSTILE_SECRET_KEY` - Cloudflare Turnstile
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` - Google OAuth
- `GITHUB_ID`, `GITHUB_SECRET` - GitHub OAuth
- `APPLE_ID`, `APPLE_SECRET` - Apple Sign In
- `NOON_*` - Noon payment gateway credentials
- `TABBY_PUBLIC_KEY`, `TABBY_MERCHANT_CODE`, `TABBY_COUNTRY` - Tabby BNPL

**Secrets location:**

- `.env` / `.env.local` for local development (gitignored)
- Environment-specific: `.env.staging`, `.env.canary` (gitignored)
- Test: `.env.test` loaded via `dotenv-cli` in test scripts

---

_Integration audit: 2026-03-06_

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
