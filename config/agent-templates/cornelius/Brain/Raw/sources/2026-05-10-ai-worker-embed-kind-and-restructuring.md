---
title: "Ai Worker Embed Kind And Restructuring"
date: "2026-05-10"
tags: [session-log, project/experts]
category: "session-log"
---

# AI Worker — EMBED Kind Implementation + Codebase Restructuring

Date: 2026-05-10
Branch: `feat/add-ai-worker`

## Summary

Implemented the first real AI worker job kind (EMBED) end-to-end, wired re-embedding on both publish and content updates, added observability across all AI surfaces, and restructured the AI/embedding codebase to remove misplaced files.

---

## What Was Built

### EmbedJob — real-time embedding via AI worker

- `src/lib/ai/queue/ai.jobs.ts` — `EmbedJob` type added to `AiJob` union; `enqueueEmbedJob()` with deduped jobId `embed:entityType:entityId`, 3 attempts, exponential backoff (2 s base)
- `src/lib/ai/embeddings/embed.service.ts` — app-side text fetchers for course/event/post + fire-and-forget `enqueueEmbedOnPublish()`
- `src/lib/ai/embeddings/processors/embed.processor.ts` — pure worker-side processor, zero Prisma, calls OpenAI `text-embedding-3-small`, returns `EmbedResult`
- `src/workers/ai/ai.worker.ts` — extended with `switch (kind)` → `case "EMBED"` dispatching to the processor
- `src/lib/ai/handlers/ai-result.handler.ts` — result handler added `handleEmbedResult()`: upserts via `$executeRaw ::vector`, marks `EmbeddingSync` row synced (catches if no row exists)

### Re-embed on publish and update

Six trigger points added:

| Handler                     | Trigger                                                                     |
| --------------------------- | --------------------------------------------------------------------------- |
| `course-publish.handler.ts` | Course publish                                                              |
| `course-update.handler.ts`  | Published course update touching title/description/tags/categoryId          |
| `event-create.handler.ts`   | Event create with published status                                          |
| `events/[id]/route.ts` PUT  | Published event update touching title/description/tags/eventType/categoryId |
| `posts/route.ts` POST       | Post create (always published)                                              |
| `posts/[id]/route.ts` PUT   | Published post update touching title/content/description/category/tags      |

### Observability

Added `observe()` calls to:

- `embed.processor.ts` — `ai.embed.started` / `ai.embed.completed`
- `embed.service.ts` — `ai.embed.enqueued` / `ai.embed.enqueue.skip` / `ai.embed.enqueue.error`
- `ai-result.handler.ts` — `ai.embed.persisted` / `ai.no_handler`
- `ask-ai-assistant.ts` — `ai.ask.question` / `ai.ask.answered` / `ai.ask.openai_error` / `ai.ask.config_error`
- `ai/suggest/route.ts` — `ai.suggest.request` / `ai.suggest.completed` / `ai.suggest.error`

### AI codebase restructuring

| Before                                                   | After                                             |
| -------------------------------------------------------- | ------------------------------------------------- |
| `src/lib/recommendations/sync/embedding-sync.service.ts` | `src/lib/ai/embeddings/embedding-sync.service.ts` |
| `src/lib/recommendations/sync/embedding-sync.worker.ts`  | `src/lib/ai/embeddings/embedding-sync.batch.ts`   |
| `app/api/v1/internal/embeddings/sync/route.ts`           | `app/api/v1/internal/ai/embeddings/sync/route.ts` |
| `src/queue/queues.ts`                                    | Deleted (100% commented-out dead code)            |

All 5 compose cron URLs updated: `/api/v1/internal/embeddings/sync` → `/api/v1/internal/ai/embeddings/sync`.

---

## Key Architectural Constraints

- `$executeRaw ::vector` is required for all embedding column writes. Prisma types `vector(1536)` as `never`.
- Worker imports must use `@/lib/observability/worker-observe` (no DatabaseObserver). App-side uses `@/lib/observability`.
- Deduped jobId means rapid edits collapse; the last enqueue wins. No separate debounce needed.

---

## Pending Ops

1. Add `OPENAI_SECRET` to staging `.env` — done 2026-05-10; staging env already contains the required key.
2. E2E validation on staging: publish course → verify `content_embeddings` row + `EmbeddingSync` marked synced
3. Decommission cron batch after worker is confirmed stable in production
4. Move admin embeddings UI under `admin/ai/embeddings/` — done 2026-05-10 in `69d40633`.

---

## 2026-05-10 Follow-up — GENERATE Kind Foundation

Added the pure AI worker foundation for single-shot generation jobs:

- `src/lib/ai/queue/ai.contract.ts` — added `GenerateJob`, `GeneratePurpose`, and extended `AiJob = EmbedJob | GenerateJob`.
- `src/lib/ai/queue/ai.jobs.ts` — added `enqueueGenerateJob()` with deduped `generate:{purpose}:{requestId}` job IDs, 3 attempts, exponential backoff, and `ai.generate.enqueued` observability.
- `src/lib/ai/generation/processors/generate.processor.ts` — pure worker-side OpenAI chat completion processor, zero Prisma/DB imports, supports text or JSON output.
- `src/workers/ai/ai.worker.ts` — added `case "GENERATE"` dispatch.
- `src/lib/ai/handlers/ai-result.handler.ts` — added `ai.generate.result_ready` result branch. No DB persistence yet; product-specific integrations can consume BullMQ return values or add a persistence target when needed.

Validation:

- `pnpm typecheck:touched -- src/lib/ai/queue/ai.contract.ts src/lib/ai/queue/ai.jobs.ts src/lib/ai/generation/processors/generate.processor.ts src/workers/ai/ai.worker.ts src/lib/ai/handlers/ai-result.handler.ts` — passed.
- `APP_VERSION=1.1.9 docker compose -f docker/staging/docker-compose.yml build experts-stg-ai-worker` — passed. Worker bundle stayed pure; no Prisma resolution errors.

New pending product action:

1. Wire translation assist and event agenda builder flows to `enqueueGenerateJob()` once their UX/API contracts are selected.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
