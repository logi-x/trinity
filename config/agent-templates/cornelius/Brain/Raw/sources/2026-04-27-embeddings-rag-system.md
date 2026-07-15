---
title: "2026-04-27"
date: "2026-04-27"
tags: [project/experts]
category: "daily"
source: "daily"
source_id: "Raw/sources/2026-04-27-embeddings-rag-system.md"
---

# 2026-04-27

## Focus

- Plan embeddings/RAG system for Experts platform ("You Might Also Like" recommendations)

## Sessions

<!-- Link to any session files created today, e.g. [[Raw/sources/2026-04-14-experts-event-pricing-sync]] -->

## Tasks

- [ ] Phase 1: Add `EmbeddingSync` Prisma model + migration
- [ ] Phase 1: Build `embedding-sync.service.ts` with OpenAI SDK
- [ ] Phase 1: Wire sync on course/event/post publish hooks
- [ ] Phase 1: Admin debug page for sync status
- [ ] Phase 2: Build 3 query handlers (courses / events / posts)
- [ ] Phase 2: Add `GET /api/v1/recommendations` route
- [ ] Phase 2: Redis cache for embedding vectors (TTL 1h)
- [ ] Phase 3: `<YouMightAlsoLike>` component
- [ ] Phase 3: Add widget to course detail, event detail, community post pages
- [ ] Phase 3: i18n strings en/ar/es
- [ ] Stretch: Learner interest profile + personalized feed ("Recommended for You" dashboard section)

## Notes

- 2026-04-27 implementation update: Phase 15 foundation is implemented in `apps/experts-app` on branch `feature/embeddings-recommendations`.
- Foundation scope completed: pgvector schema/migration, `ContentEmbedding`, `EmbeddingSync`, recommendations sync service/worker/status query, publish-hook queueing, internal sync route, admin embeddings debug page, and Docker cron sidecar scheduling.
- Deployment correction: Experts is deployed on a VPS inside Docker Compose, not Vercel. `apps/experts-app/vercel.json` was removed; scheduled jobs now run from `docker/staging/docker-compose.yml` via an Alpine cron sidecar.
- Required VPS env: `CRON_SECRET` shared by `experts-app` and `cron`; `OPENAI_SECRET` available to `experts-app`.
- Current schedules:
  - every 2 minutes: `POST /api/v1/internal/embeddings/sync`
  - daily at 03:00: `POST /api/v1/admin/payments/reconcile/batch`
- Avoid `instrumentation.ts` `setInterval` for scheduled jobs unless running exactly one app instance; multiple replicas would duplicate job execution.

## Links

---

## Plan — Embeddings/RAG System (pgvector + OpenAI)

> Created: 2026-04-27 | Project: experts-app | Branch: feature/embeddings-recommendations

### Feature Goals

1. **"You Might Also Like"** — surface related courses/events/posts after viewing or enrolling
2. **Smart Search** — semantic search across content (not just keyword)
3. **Personalized Feed** — rank community posts and events by learner interest profile
4. **Cross-entity Recommendations** — e.g. "Event about this course topic" shown on a course page

### Embeddings Strategy

- Model: `text-embedding-3-small` via OpenAI API (generation only — no OpenAI Vector Stores)
- Vectors stored in Postgres via `pgvector` extension — same DB, no extra infra
- Each row stores: entity ID, entity type, locale, embedding vector (1536 dims), synced timestamp
- Similarity search via `<=>` cosine distance operator directly in SQL

### Prisma Schema Addition

```prisma
model EmbeddingSync {
  id         String    @id @default(cuid())
  entityType String    // "course" | "event" | "post"
  entityId   String
  vectorId   String?   // OpenAI vector ID after sync
  status     String    @default("pending") // pending | synced | failed
  syncedAt   DateTime?
  createdAt  DateTime  @default(now())
  updatedAt  DateTime  @updatedAt
  @@unique([entityType, entityId])
}
```

### CQRS Domain Layout

```
src/lib/recommendations/
  queries/
    get-similar-courses.query.ts
    get-similar-events.query.ts
    get-related-posts.query.ts
  handlers/
    get-similar-courses.handler.ts   ← pgvector cosine search
    get-similar-events.handler.ts
    get-related-posts.handler.ts
  dto/
    recommendation.dto.ts
  sync/
    embedding-sync.service.ts        ← calls OpenAI, writes vector to pgvector
    embedding-sync.worker.ts         ← polls EmbeddingSync table (DB queue)
```

### Query Flow

1. `GET /api/v1/recommendations?entityId=&entityType=&limit=5`
2. Fetch seed entity's vector from `ContentEmbedding` table
3. pgvector cosine search: `ORDER BY embedding <=> $seed_vector LIMIT 5`
4. Filter by same locale + published status in same SQL query
5. Hydrate full records from Postgres → return shaped response

### Sync Queue Flow (DB polling)

```
publish course/event/post
    ↓
mutation handler → upsert EmbeddingSync { entityId, status: "pending" }
    ↓
cron job (every 2 min) → batch picks up pending rows (50 at a time)
    ↓
calls OpenAI text-embedding-3-small → writes vector to ContentEmbedding table
    ↓
updates EmbeddingSync { status: "synced", syncedAt }
```

No Redis pub/sub needed. No dependency on experts-realtime.

### Deployment Scheduler

The production deployment uses a Docker cron sidecar, not Vercel Cron.

```yaml
cron:
  image: alpine:3.20
  environment:
    - CRON_SECRET=${CRON_SECRET}
    - APP_BASE_URL=http://experts-app:3025
```

The sidecar writes a root crontab at startup and calls internal API routes over the Compose network:

```sh
*/2 * * * * curl -fsS -X POST -H "Authorization: Bearer $CRON_SECRET" "$APP_BASE_URL/api/v1/internal/embeddings/sync"
0 3 * * * curl -fsS -X POST -H "Authorization: Bearer $CRON_SECRET" -H "Content-Type: application/json" -d '{}' "$APP_BASE_URL/api/v1/admin/payments/reconcile/batch"
```

### UI

- `<YouMightAlsoLike>` — generic component, accepts `entityType` + `entityId`
- Mounted on course detail, event detail, and community post detail pages
- Skeleton loading, graceful empty state (hide widget if no results)
- Query uses `/api/v1/recommendations` and pgvector similarity over `content_embeddings`
- Old `<RelatedPosts>` is now a compatibility wrapper around `<YouMightAlsoLike entityType="post" />`
- Locale-aware: embedding query currently filters on the persisted embedding locale (`ar`)

### Implementation Phases

| Phase                           | Work                                                                               | Est.     |
| ------------------------------- | ---------------------------------------------------------------------------------- | -------- |
| 1 — Foundation                  | Prisma model, sync service, publish hook wiring, admin debug page                  | 1–2 days |
| 2 — Query API                   | 3 handlers, `/api/v1/recommendations` route, Redis cache                           | 1 day    |
| 3 — UI                          | `<YouMightAlsoLike>`, wire into 3 pages, i18n                                      | 1 day    |
| 4 — Personalization _(stretch)_ | Learner interest profile (averaged embeddings), "Recommended for You" on dashboard | TBD      |

### Key Decisions

| Decision                | Choice                                                       | Rationale                                                                                           |
| ----------------------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| Embedding generation    | OpenAI `text-embedding-3-small`                              | Best cost/quality ratio; handles Arabic well                                                        |
| Vector storage + search | pgvector (same Postgres DB)                                  | No extra infra; sub-10ms cosine search at our scale; keeps data in-house                            |
| Sync queue              | `EmbeddingSync` DB table + polling cron                      | Durable, retryable, debuggable; no Redis pub/sub coupling to experts-realtime                       |
| Scheduler               | Docker cron sidecar in Compose                               | VPS deployment does not run Vercel Cron; sidecar keeps schedule with deployment and logs via Docker |
| Re-embed trigger        | Publish only, not every draft save                           | Cost control                                                                                        |
| Multi-locale            | Embed in content's primary locale; filter by locale in query | Avoids cross-language false positives                                                               |
| Cold start fallback     | Show "popular courses" until first sync                      | Avoids empty widget on new content                                                                  |
| Backfill                | Async bulk job via same worker, 50 items/batch               | ~$0.04 one-time for 10K items; respects 1M TPM limit                                                |

### Prisma Schema Additions

```prisma
model ContentEmbedding {
  id         String   @id @default(cuid())
  entityType String   // "course" | "event" | "post"
  entityId   String
  locale     String
  embedding  Unsupported("vector(1536)")
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt
  @@unique([entityType, entityId, locale])
  @@index([entityType])
}

model EmbeddingSync {
  id         String    @id @default(cuid())
  entityType String
  entityId   String
  status     String    @default("pending") // pending | synced | failed
  syncedAt   DateTime?
  error      String?
  createdAt  DateTime  @default(now())
  updatedAt  DateTime  @updatedAt
  @@unique([entityType, entityId])
}
```

### Files to Touch

- `prisma/schema.prisma` — add `ContentEmbedding` + `EmbeddingSync`
- `apps/experts-app/src/lib/recommendations/` — new domain folder (full CQRS layout above)
- `apps/experts-app/app/api/v1/recommendations/route.ts` — new route
- `apps/experts-app/app/api/v1/internal/embedding-sync-worker/route.ts` — cron worker endpoint
- `docker/staging/docker-compose.yml` — Docker cron sidecar for scheduled internal route calls
- Existing course/event/post publish handlers — add `EmbeddingSync` upsert
- `apps/experts-app/src/components/recommendations/YouMightAlsoLike.tsx` — new component
- `apps/experts-app/src/i18n/messages/{en,ar,es}.json` — recommendation i18n keys

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
