---
title: "Experts codebase — Structure"
date: "2026-03-06"
tags: ["project/experts", "topic/planning", "topic/architecture"]
category: "docs/experts-reference"
repo_root: /Users/ahmedsulaimani/projects/experts/apps/experts-app
monorepo_root: /Users/ahmedsulaimani/projects/experts
updated: "2026-07-15"
---

# Codebase Structure

**Analysis Date:** 2026-03-06

## Directory Layout

```
experts-app/                          # App root (cwd for all commands)
├── app/                              # Next.js App Router root
│   ├── (i18n)/                       # i18n route group (hidden from URL)
│   │   ├── _shared/                  # Locale-agnostic page implementations
│   │   │   ├── (auth)/               # Auth route group: login, register, etc.
│   │   │   ├── (console)/            # Internal console/status pages
│   │   │   ├── (content)/            # Shareable content: hashtags, share pages
│   │   │   ├── (home)/               # Marketing/landing pages
│   │   │   ├── (user)/               # User account pages: dashboard, settings
│   │   │   ├── admin/                # Admin dashboard pages
│   │   │   ├── affiliate/            # Affiliate portal pages
│   │   │   ├── community/            # Community post pages
│   │   │   ├── courses/              # Course catalog and detail pages
│   │   │   ├── creator/              # Creator studio pages
│   │   │   └── events/               # Event catalog and detail pages
│   │   ├── ar/                       # Arabic locale wrappers (re-export _shared)
│   │   ├── en/                       # English locale wrappers (re-export _shared)
│   │   └── es/                       # Spanish locale wrappers (re-export _shared)
│   ├── (user)/                       # Non-localized user routes (profile-del)
│   ├── [username]/                   # Public user profile pages
│   ├── api/                          # API routes (backend)
│   │   ├── auth/                     # NextAuth endpoints
│   │   ├── dev/                      # Development-only endpoints
│   │   ├── v1/                       # Versioned API
│   │   │   ├── admin/                # Admin-only endpoints
│   │   │   ├── commerce/             # Affiliates, billing, checkout, invoices, subscriptions
│   │   │   ├── community/            # Posts, comments, stats
│   │   │   ├── console/              # Internal console API
│   │   │   ├── content/              # Categories, hashtags, share
│   │   │   ├── courses/              # Course CRUD + enrollment
│   │   │   ├── creator/              # Creator tools API
│   │   │   ├── events/               # Event CRUD + registration
│   │   │   ├── internal/             # Internal/service endpoints
│   │   │   ├── quizzes/              # Quiz endpoints
│   │   │   ├── user/                 # User profile and settings
│   │   │   └── users/                # User directory
│   │   └── webhooks/                 # Payment provider webhooks
│   ├── invoice/                      # Invoice rendering routes
│   ├── og-live/                      # Open Graph image generation
│   ├── layout.tsx                    # Root layout (locale/theme detection)
│   ├── globals.css                   # Global TailwindCSS styles
│   └── providers.tsx                 # Global React context providers
├── src/                              # Application source (non-routing)
│   ├── components/                   # React UI components
│   │   ├── ui/                       # Primitive UI components (shadcn/ui base)
│   │   ├── courses/                  # Course-specific components
│   │   ├── events/                   # Event-specific components
│   │   ├── creator/                  # Creator-specific components
│   │   ├── community/                # Community/post components
│   │   ├── affiliate/                # Affiliate components
│   │   ├── bookmarks/                # Bookmark components
│   │   ├── charts/                   # Chart/visualization components
│   │   ├── carousel/                 # Carousel components
│   │   ├── icons/                    # Icon components
│   │   ├── likes/                    # Like/reaction components
│   │   ├── lifecycle/                # Lifecycle UI components
│   │   ├── markdown/                 # Markdown editor/renderer
│   │   ├── mentions/                 # @mention components
│   │   ├── notifications/            # Notification components
│   │   ├── payments/                 # Payment UI components
│   │   ├── posts/                    # Post components
│   │   ├── profile/                  # Profile components
│   │   ├── ratings/                  # Rating/review components
│   │   ├── share/                    # Social share components
│   │   ├── shared/                   # Cross-domain shared components
│   │   ├── viewers/                  # View count/viewer components
│   │   ├── views/                    # View tracking components
│   │   ├── og/                       # OG image components
│   │   ├── errors/                   # Error page components
│   │   ├── Navbar.tsx                # Global navigation bar
│   │   ├── GlobalSearch.tsx          # Global search component
│   │   ├── ImageUpload.tsx           # Image upload component
│   │   ├── PresenceProvider.tsx      # Real-time presence context
│   │   ├── SessionProvider.tsx       # NextAuth session wrapper
│   │   ├── LanguageSwitcher.tsx      # Locale switcher
│   │   └── ThemeSwitcher.tsx         # Dark/light mode switcher
│   ├── hooks/                        # Custom React hooks
│   │   ├── use-api-query.ts          # Universal SWR + auth hook
│   │   ├── use-events.ts             # Events data hook
│   │   ├── use-courses.ts            # Courses data hook
│   │   ├── use-affiliate.ts          # Affiliate data hook
│   │   ├── use-notifications.ts      # Notifications hook
│   │   ├── use-realtime.ts           # Real-time connection hook
│   │   ├── use-presence.ts           # User presence hook
│   │   └── use-*.ts                  # Other domain hooks
│   ├── lib/                          # Domain libraries and utilities
│   │   ├── prisma.ts                 # Prisma singleton with pg pool
│   │   ├── auth.ts                   # NextAuth v5 configuration
│   │   ├── auth-context.tsx          # Client-side auth context/hook
│   │   ├── redis.ts                  # Redis client (ioredis)
│   │   ├── r2.ts                     # Cloudflare R2 client
│   │   ├── stripe.ts                 # Stripe SDK instance
│   │   ├── logger.ts                 # Structured logger (debug/info/warn/error)
│   │   ├── utils.ts                  # General utility functions
│   │   ├── permissions.ts            # Server-side permission queries
│   │   ├── money.ts                  # Currency/money formatting
│   │   ├── cached-queries.ts         # 'use cache' server-side queries
│   │   ├── revalidation.ts           # revalidateTag wrappers (server actions)
│   │   ├── validate-uuid.ts          # UUID validation helper
│   │   ├── notification-service.ts   # Notification dispatch
│   │   ├── events/                   # Events domain library
│   │   │   ├── commands/             # Zod schemas + command types
│   │   │   ├── handlers/             # Business logic per operation
│   │   │   ├── queries/              # Query parsers and projections
│   │   │   ├── mappers/              # Prisma → DTO mappers
│   │   │   ├── dto/                  # DTO interface definitions
│   │   │   ├── includes/             # Prisma include objects
│   │   │   ├── lifecycle/            # Event lifecycle logic
│   │   │   └── services/             # Event-level service functions
│   │   ├── courses/                  # Courses domain library (same structure as events)
│   │   │   ├── catalog/
│   │   │   ├── curriculum/
│   │   │   ├── enrollments/
│   │   │   ├── learn/
│   │   │   ├── lifecycle/
│   │   │   ├── queries/
│   │   │   └── utils/
│   │   ├── payments/                 # Payment abstraction layer
│   │   │   ├── gateways/             # Stripe, Noon, Tabby implementations
│   │   │   ├── commands/             # Payment command schemas
│   │   │   ├── utils/
│   │   │   └── payment.service.ts    # Unified payment service
│   │   ├── billing/                  # Subscription/billing domain
│   │   ├── community/                # Community/posts domain
│   │   ├── users/                    # User management domain
│   │   ├── creator/                  # Creator tools domain
│   │   ├── admin/                    # Admin domain
│   │   ├── affiliate/                # Affiliate domain
│   │   ├── orders/                   # Order processing
│   │   ├── subscriptions/            # Subscription helpers
│   │   ├── storage/                  # File storage commands/helpers
│   │   ├── aggregations/             # Cross-cutting data aggregations (ratings, views)
│   │   ├── realtime/                 # WebSocket/SSE real-time layer
│   │   ├── lifecycle/                # Content lifecycle state machine
│   │   ├── observability/            # Observer pattern for DB/Redis/logging
│   │   ├── emails/                   # Email templates and helpers
│   │   ├── notifications/            # Notification service
│   │   ├── share/                    # Social sharing
│   │   ├── bookmarks/                # Bookmark management
│   │   ├── metadata/                 # SEO metadata helpers
│   │   └── sitemap/                  # Sitemap generation
│   ├── modules/                      # Higher-level bounded context services
│   │   ├── billing/                  # business-entity.service.ts, publishing.service.ts
│   │   ├── identity/                 # user.service.ts
│   │   ├── learning/                 # (learning domain services)
│   │   ├── permissions/              # permissions.service.ts
│   │   ├── publishing/               # publishing.service.ts
│   │   ├── revenue/                  # revenue.service.ts
│   │   └── social/                   # (social domain services)
│   ├── i18n/                         # Internationalization
│   │   ├── config.ts                 # Locale config (en, ar, es)
│   │   ├── request.ts                # next-intl request config
│   │   ├── routing.ts                # next-intl routing config
│   │   └── messages/                 # Translation message files
│   │       ├── en/                   # English messages by domain
│   │       ├── ar/                   # Arabic messages by domain
│   │       └── es/                   # Spanish messages by domain
│   ├── generated/                    # Auto-generated (do not edit)
│   │   └── prisma/                   # Prisma Client types and runtime
│   ├── functions/                    # Edge/serverless function utilities
│   │   └── formatter.ts
│   ├── notifications/                # Notification channel implementations
│   │   ├── channels/
│   │   ├── notification.service.ts
│   │   └── types.ts
│   ├── queue/                        # BullMQ queue definitions (currently disabled)
│   ├── workers/                      # Background workers
│   │   ├── pdf/                      # PDF generation worker
│   │   └── zatca/                    # ZATCA compliance worker
│   └── types/                        # TypeScript ambient type declarations
│       ├── content.d.ts
│       └── next-auth.d.ts
├── types/                            # App-level global type declarations
│   ├── content.d.ts
│   └── next-auth.d.ts
├── prisma/                           # Database schema and migrations
│   ├── schema.prisma                 # Prisma schema (source of truth)
│   ├── migrations/                   # Migration SQL files
│   ├── seed.ts                       # Database seeder entry
│   └── seeders/                      # Domain-specific seed files
├── public/                           # Static assets served at root
├── tests/                            # Integration/e2e test files
├── scripts/                          # Utility scripts
├── docs/                             # Developer documentation
├── app/layout.tsx                    # Root layout
├── app/globals.css                   # Global styles
├── next.config.ts                    # Next.js configuration
├── prisma.config.ts                  # Prisma migration config
├── tsconfig.json                     # TypeScript config (@/* alias → src/*)
├── vitest.config.ts                  # Vitest test configuration
├── eslint.config.mjs                 # ESLint configuration
├── package.json                      # Dependencies and scripts
└── Dockerfile                        # Production container image
```

## Directory Purposes

**`app/(i18n)/_shared/`:**

- Purpose: Contains the actual page implementations shared across all locales
- Contains: `page.tsx`, `layout.tsx`, sub-components in `_components/`, client shells (e.g., `events-client.tsx`)
- Key files: `app/(i18n)/_shared/events/page.tsx`, `app/(i18n)/_shared/courses/page.tsx`

**`app/(i18n)/{locale}/`:**

- Purpose: Locale-specific routing entry points; thin wrappers only
- Contains: `page.tsx` files that re-export from `_shared/`, `layout.tsx` that provides `NextIntlClientProvider`
- Pattern: `export default async function EnglishEventsPage() { return <SharedEventsPage /> }`

**`app/api/v1/`:**

- Purpose: Versioned REST API for browser and mobile clients
- Contains: `route.ts` files with Next.js route handlers
- Key files: `app/api/v1/events/route.ts`, `app/api/v1/courses/route.ts`, `app/api/v1/commerce/checkout/route.ts`

**`src/lib/{domain}/`:**

- Purpose: Domain business logic, separated into commands, handlers, mappers, DTOs
- Key domains: `events/`, `courses/`, `payments/`, `community/`, `creator/`, `users/`, `affiliate/`

**`src/components/ui/`:**

- Purpose: Base UI primitives (shadcn/ui pattern, styled with TailwindCSS)
- Key files: `src/components/ui/button.tsx`, `src/components/ui/badge.tsx`, `src/components/ui/tabs.tsx`

**`src/hooks/`:**

- Purpose: Client-side data fetching hooks backed by SWR
- Key files: `src/hooks/use-api-query.ts`, `src/hooks/use-events.ts`, `src/hooks/use-courses.ts`

**`src/modules/`:**

- Purpose: Service layer for bounded contexts that span multiple lib domains
- Key files: `src/modules/billing/publishing.service.ts`, `src/modules/identity/user.service.ts`

**`src/generated/prisma/`:**

- Purpose: Auto-generated Prisma Client; never edit directly
- Regenerate with: `pnpm prisma generate`

**`src/i18n/messages/`:**

- Purpose: Translation strings organized by domain and locale
- Structure: `src/i18n/messages/{locale}/{domain}/{page}.ts`

## Key File Locations

**Entry Points:**

- `app/layout.tsx`: Root layout; locale detection, theme, provider setup
- `app/providers.tsx`: All global React context providers
- `app/page.tsx`: Root page (redirect logic)

**Authentication:**

- `src/lib/auth.ts`: NextAuth v5 config (providers, callbacks, JWT)
- `src/lib/auth-context.tsx`: Client-side `AuthProvider` and `useAuth()` hook

**Database:**

- `src/lib/prisma.ts`: Prisma singleton with connection pooling
- `prisma/schema.prisma`: Database schema (source of truth for all models)

**Configuration:**

- `next.config.ts`: Next.js config (intl plugin, image domains, turbopack)
- `tsconfig.json`: TypeScript config; `@/*` maps to `./src/*`
- `src/i18n/config.ts`: Locale definitions and defaults

**Core Utilities:**

- `src/lib/logger.ts`: Structured logger
- `src/lib/utils.ts`: General utilities (date formatting, class merging, etc.)
- `src/lib/money.ts`: Currency formatting
- `src/lib/validate-uuid.ts`: UUID validation for path parameters
- `src/lib/permissions.ts`: Server-side role/permission queries
- `src/lib/cached-queries.ts`: Next.js `'use cache'` data queries
- `src/lib/revalidation.ts`: `revalidateTag()` helpers (server actions)

**Payments:**

- `src/lib/payments/payment.service.ts`: Unified payment service
- `src/lib/payments/gateways/stripe/`, `noon/`, `tabby/`: Gateway implementations

**Storage:**

- `src/lib/r2.ts`: Cloudflare R2 SDK instance
- `src/lib/storage/r2.client.ts`: R2 client wrapper
- `src/lib/storage/commands/`: Upload command handlers

**Testing:**

- `src/__tests__/`: Unit and integration tests (root test dir referenced by vitest)
- `tests/`: Additional integration tests
- `vitest.config.ts`: Test configuration

## Naming Conventions

**Files:**

- Page files: `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx` (Next.js conventions)
- Client components: `{domain}-client.tsx` (e.g., `events-client.tsx`, `courses-client.tsx`)
- Hooks: `use-{domain}.ts` (kebab-case with `use-` prefix)
- Handlers: `{entity}-{operation}.handler.ts` (e.g., `event-list.handler.ts`)
- Schemas: `{entity}-{operation}.schema.ts`
- Commands: `{entity}-{operation}.command.ts`
- DTOs: `{entity}.dto.ts`
- Mappers: `{entity}.mapper.ts`
- Services: `{domain}.service.ts`

**Directories:**

- Route groups: `(group-name)` — Next.js convention, excluded from URL
- Shared locale pages: `_shared/` — underscore prefix indicates shared/internal
- Component subdirectories: domain name in plural (`courses/`, `events/`, `creator/`)
- Test directories: `__tests__/` — Jest/Vitest convention

**Exports:**

- Page components: `export default function XxxPage()`
- Client components: Named exports (`export function EventsClient()`)
- Hooks: Named exports (`export function useApiQuery()`)
- Utilities: Named exports

## Where to Add New Code

**New Page (localized):**

1. Create implementation in `app/(i18n)/_shared/{feature}/page.tsx`
2. Create thin locale wrappers in each locale: `app/(i18n)/en/{feature}/page.tsx`, `app/(i18n)/ar/{feature}/page.tsx`, `app/(i18n)/es/{feature}/page.tsx`
3. Each locale wrapper imports and re-exports the shared page

**New API Endpoint:**

- Primary code: `app/api/v1/{domain}/route.ts` (or `app/api/v1/{domain}/[id]/route.ts` for resource routes)
- Command schema: `src/lib/{domain}/commands/{entity}-{operation}.schema.ts`
- Handler: `src/lib/{domain}/handlers/{entity}-{operation}.handler.ts`
- DTO (if needed): `src/lib/{domain}/dto/{entity}.dto.ts`
- Mapper (if needed): `src/lib/{domain}/mappers/{entity}.mapper.ts`

**New Client Component:**

- Domain component: `src/components/{domain}/{ComponentName}.tsx`
- UI primitive: `src/components/ui/{component-name}.tsx`

**New Data Hook:**

- Implementation: `src/hooks/use-{domain}.ts`
- Use `useApiQuery` as the base; wrap with domain-specific logic

**New Domain Library:**

1. Create directory: `src/lib/{domain}/`
2. Add `commands/`, `handlers/`, `dto/`, `mappers/` as needed
3. Follow the events domain as the reference: `src/lib/events/`

**New Database Model:**

1. Add model to `prisma/schema.prisma`
2. Run `pnpm prisma migrate dev --name {description}`
3. Run `pnpm prisma generate` to update client types
4. Create seeder if needed in `prisma/seeders/{nn}-{domain}.ts`
5. Register seeder in `prisma/seeders/config.ts`

**New Translation Key:**

- Add to all three locale files: `src/i18n/messages/en/{domain}/{page}.ts`, `ar/...`, `es/...`

**Utilities:**

- Shared helpers with no domain: `src/lib/utils.ts`
- Domain-specific utilities: `src/lib/{domain}/utils/` or `src/lib/{domain}/helpers/`

## Special Directories

**`src/generated/prisma/`:**

- Purpose: Prisma Client generated code (types, runtime, query engine)
- Generated: Yes — by `pnpm prisma generate`
- Committed: Yes (for type stability in CI)

**`app/(i18n)/_shared/`:**

- Purpose: Actual page content implementations; locale wrappers simply re-export these
- Generated: No
- Committed: Yes

**Planning / codebase maps:**

- **Vault:** [[Projects/Experts/Experts App/docs/reference/experts-product-overview|Experts App planning]] → `planning/codebase/` notes (this mirror)
- **Repo:** `` `apps/experts-app/.planning/codebase/` `` (monorepo root) — GSD codebase analysis consumed by planning agents; generated (e.g. map-codebase), committed

**`.next/`:**

- Purpose: Next.js build output and cache
- Generated: Yes
- Committed: No

**`src/workers/`:**

- Purpose: Standalone background worker scripts for PDF generation and ZATCA compliance; run as separate Node.js processes, not as part of Next.js
- Generated: No
- Committed: Yes

---

_Structure analysis: 2026-03-06_
