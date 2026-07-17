---
title: "Experts codebase — Architecture"
date: "2026-03-06"
tags: ["project/experts", "topic/planning", "topic/architecture"]
category: "docs/experts-reference"
repo_root: /Users/ahmedsulaimani/projects/experts/apps/experts-app
monorepo_root: /Users/ahmedsulaimani/projects/experts
updated: "2026-07-15"
---

# Architecture

**Analysis Date:** 2026-03-06

## Pattern Overview

**Overall:** Full-Stack Next.js Monolith with CQRS-Influenced Domain Layer

**Key Characteristics:**

- Single Next.js 16 app hosts both frontend (App Router pages) and backend (API routes under `app/api/`)
- Domain logic is encapsulated in `src/lib/{domain}/` with a CQRS-influenced structure: schemas, commands, handlers, mappers, queries, and DTOs are separated per operation
- Pages are locale-aware: each locale (`en`, `ar`, `es`) has its own routing subtree under `app/(i18n)/{locale}/` that re-exports shared page components from `app/(i18n)/_shared/`
- Client components use SWR via `useApiQuery` hook; server components call `auth()` and Prisma directly

## Layers

**Routing / Page Layer:**

- Purpose: Define URL structure, handle locale, load data for server-rendered pages
- Location: `app/(i18n)/{locale}/` (locale-specific thin wrappers), `app/(i18n)/_shared/` (actual page implementations)
- Contains: `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`
- Depends on: Client components, server-side `auth()`, shared page components
- Used by: Next.js router

**API Route Layer:**

- Purpose: HTTP interface for browser clients and mobile apps
- Location: `app/api/v1/{domain}/route.ts`
- Contains: `GET`/`POST`/`PUT`/`DELETE` handlers; authentication check, input parsing, delegation to handler, mapping to DTO
- Depends on: `src/lib/auth`, domain handlers, mappers, aggregation utilities
- Used by: `useApiQuery`, `useEvents`, mobile clients

**Domain Handler Layer:**

- Purpose: Orchestrate business logic for a specific command/query
- Location: `src/lib/{domain}/handlers/{operation}.handler.ts`
- Contains: Prisma queries, business rules, aggregation calls
- Depends on: Prisma, domain-specific includes, aggregations
- Used by: API routes

**Domain Command/Query Layer:**

- Purpose: Define and validate inputs with Zod schemas
- Location: `src/lib/{domain}/commands/{operation}.schema.ts` and `{operation}.command.ts`
- Contains: Zod schemas, inferred TypeScript types exported as command types
- Used by: API routes (parse input), handlers (consume typed command)

**DTO / Mapper Layer:**

- Purpose: Shape Prisma models into API response shapes
- Location: `src/lib/{domain}/dto/`, `src/lib/{domain}/mappers/`
- Contains: Interface types (DTOs), mapper functions
- Depends on: Prisma result types, aggregation maps
- Used by: API routes after handler returns raw DB results

**Data Access Layer:**

- Purpose: Persistent storage via Prisma ORM
- Location: `src/lib/prisma.ts` (singleton client), `prisma/schema.prisma` (schema)
- Contains: PrismaClient singleton with pg connection pool; auto-shutdown handlers
- Depends on: `DATABASE_URL` env var, `@prisma/adapter-pg`
- Used by: All handlers, server components, server actions

**Component Layer:**

- Purpose: UI building blocks
- Location: `src/components/{domain}/` and `src/components/ui/`
- Contains: React components (Client and Server), organized by domain (`courses/`, `events/`, `creator/`, etc.) and UI primitives (`ui/`)
- Depends on: Custom hooks, HeroUI, shadcn/ui, TailwindCSS
- Used by: Pages, other components

**Hook Layer:**

- Purpose: Client-side data fetching and state encapsulation
- Location: `src/hooks/`
- Contains: SWR-backed hooks per domain (`use-events.ts`, `use-courses.ts`, etc.), shared `use-api-query.ts`
- Depends on: SWR, `useAuth` from `src/lib/auth-context.tsx`
- Used by: Client components

**Domain Library Layer (`src/lib/`):**

- Purpose: Shared utilities, domain services, and cross-cutting concerns
- Location: `src/lib/`
- Contains: Auth (`auth.ts`, `auth-context.tsx`), storage (`r2.ts`, `storage/`), payments (`payments/`), lifecycle, notifications, observability, caching, etc.
- Depends on: Prisma, external SDKs
- Used by: API routes, server components, handlers

**Module Layer (`src/modules/`):**

- Purpose: Higher-level service abstractions per bounded context
- Location: `src/modules/{context}/`
- Contexts: `billing`, `identity`, `learning`, `permissions`, `publishing`, `revenue`, `social`
- Contains: Service classes/functions (e.g., `publishing.service.ts`, `user.service.ts`)
- Depends on: `src/lib/` utilities, Prisma
- Used by: API routes and handlers requiring cross-domain coordination

## Data Flow

**Authenticated API Request (e.g., GET /api/v1/events):**

1. Browser calls `useApiQuery('/api/v1/events', fetcher)` in a Client Component
2. SWR issues HTTP GET to Next.js API route at `app/api/v1/events/route.ts`
3. Route handler calls `auth()` to get session, extracts `userId`
4. `parseEventListSearchParams()` parses and validates URL query params into a typed `EventListCommand`
5. `handleEventList(command)` executes Prisma queries against PostgreSQL
6. Route calls `getRatings()` and `getViews()` for aggregation data (Redis-backed)
7. `mapEventToListItemDTO()` shapes results into API response shape
8. `NextResponse.json()` returns JSON to browser

**Server-Rendered Page:**

1. Next.js renders locale-specific wrapper (e.g., `app/(i18n)/en/events/page.tsx`)
2. Wrapper re-exports shared implementation from `app/(i18n)/_shared/events/page.tsx`
3. Shared page wraps `EventsClient` in `<Suspense>`
4. `EventsClient` (Client Component) initializes, SWR hooks fire on mount
5. Data loads client-side via the API layer

**Locale Routing:**

1. Request arrives; proxy sets `x-locale` header
2. Root layout (`app/layout.tsx`) reads header or cookie to determine locale
3. Next.js routes to `app/(i18n)/{locale}/` subtree
4. Locale layout wraps children with `NextIntlClientProvider` and locale messages
5. Locale-specific page re-exports shared `_shared/` page component

**State Management:**

- Server state: SWR caches API responses; Next.js `'use cache'` directive and `revalidateTag()` for server-side caching
- Client state: React `useState`/`useReducer` within Client Components
- Auth state: `AuthContext` wraps NextAuth session; available via `useAuth()` hook
- Global UI state: Context providers in `app/providers.tsx` (Theme, Share, Bookmark, Presence, AuthPrompt)

## Key Abstractions

**`useApiQuery` Hook:**

- Purpose: Universal SWR wrapper with auth-awareness; delays fetch until auth is ready for `requireAuth: true` queries
- Location: `src/hooks/use-api-query.ts`
- Pattern: Accepts `key`, `fetcher`, `swrConfig`, and `options`; returns SWR response plus `tokenReady` and `isAuthLoading`

**Domain Handler:**

- Purpose: Encapsulates all DB access and business rules for one operation
- Examples: `src/lib/events/handlers/event-list.handler.ts`, `src/lib/courses/handlers/`
- Pattern: Pure async function accepting a typed command, returning a result object; no HTTP concerns

**Zod Schema + Command Type:**

- Purpose: Validate and type-check inputs at API boundary
- Examples: `src/lib/events/commands/event-list.schema.ts`
- Pattern: `z.object(...)` exported as schema; `z.infer<typeof Schema>` exported as command type

**DTO Interfaces:**

- Purpose: Decouple Prisma model shapes from API contracts
- Examples: `src/lib/events/dto/event.dto.ts`
- Pattern: Plain TypeScript interfaces; mapper functions transform Prisma results to DTO

**`_shared/` Page Components:**

- Purpose: Locale-agnostic implementation of a page; imported by each locale's thin wrapper
- Examples: `app/(i18n)/_shared/events/page.tsx`, `app/(i18n)/_shared/courses/page.tsx`
- Pattern: Server Component exporting `default` function; wraps Client components in `<Suspense>`

**Providers Composition:**

- Purpose: Compose all global client-side context providers in one place
- Location: `app/providers.tsx`
- Pattern: Nested provider tree; SessionProvider > ThemeProvider > I18nProvider > domain providers

## Entry Points

**Root Layout:**

- Location: `app/layout.tsx`
- Triggers: Every request
- Responsibilities: Detect locale and theme from cookies/headers, apply fonts, render `<Providers>`

**Locale Layout:**

- Location: `app/(i18n)/{locale}/layout.tsx`
- Triggers: Requests to locale-prefixed routes
- Responsibilities: Set request locale, load translation messages, provide `NextIntlClientProvider`

**API Routes:**

- Location: `app/api/v1/{domain}/route.ts`
- Triggers: HTTP requests from browser (SWR) or mobile clients
- Responsibilities: Auth check, input parsing, handler delegation, DTO mapping, JSON response

**Root Page (Landing):**

- Location: `app/page.tsx` (redirects) and `app/(i18n)/_shared/(home)/page.tsx`
- Triggers: Visit to `/` or `/{locale}`

**Webhook Handlers:**

- Location: `app/api/webhooks/`
- Triggers: Payment provider callbacks (Stripe, Noon, Tabby)
- Responsibilities: Verify webhook, update order/registration status

## Error Handling

**Strategy:** Try-catch at API route boundary; return structured JSON error with appropriate HTTP status

**Patterns:**

- API routes wrap entire handler in `try { ... } catch (error) { return NextResponse.json({ error: message }, { status: 500 }) }`
- Auth errors return `401` or `403` before handler is invoked
- `validateUUID` utility (`src/lib/validate-uuid.ts`) returns `400` for malformed IDs
- Client hooks surface errors via SWR `error` property; components render error states
- Custom logger (`src/lib/logger.ts`) with levels debug/info/success/warn/error; JSON mode via `LOG_FORMAT=json`

## Cross-Cutting Concerns

**Logging:** Custom `logger` module at `src/lib/logger.ts`; structured output with service/context tags; JSON-only mode for production

**Validation:** Zod schemas in `src/lib/{domain}/commands/*.schema.ts` for API inputs; `validateUUID` for UUID path params

**Authentication:** NextAuth v5 (`src/lib/auth.ts`); server calls use `auth()`, client components use `useSession()` or `useAuth()` context; supports Credentials, Google, GitHub, Apple OAuth providers

**Caching:** Next.js `'use cache'` directive with `revalidateTag()` (`src/lib/cached-queries.ts`, `src/lib/revalidation.ts`); Redis for aggregation data (`src/lib/redis.ts`)

**Internationalization:** `next-intl` with locale routing; messages in `src/i18n/messages/{locale}/`; three locales: `en`, `ar`, `es`; RTL detection via `react-aria-components`

**Observability:** Observer pattern at `src/lib/observability/`; database, redis, and logger observers; diagnostics tooling

**Storage:** Cloudflare R2 via `src/lib/r2.ts` and `src/lib/storage/`; file upload commands in `src/lib/storage/commands/`

**Payments:** Gateway abstraction at `src/lib/payments/`; gateways for Stripe, Noon, and Tabby; unified `PaymentService` (`src/lib/payments/payment.service.ts`)

---

_Architecture analysis: 2026-03-06_
