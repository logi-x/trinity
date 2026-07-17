---
title: "Ai Worker Scaffold Plan"
date: "2026-05-10"
tags: [plan, project/experts]
category: "plan"
---

# AI Worker Scaffold Plan

## Summary

Stand up a dedicated AI worker container in `apps/experts-app` to host upcoming AI capabilities (embeddings, RAG, agent systems, recommendation engines, vector pipelines) and to give WakaTime a clean physical surface for the `experts-ai` billing project. The AI worker follows the existing PDF/ZATCA pattern: pure compute, NO Prisma, NO DB access — job payloads carry context snapshots; the app-side `QueueEvents` listener persists results.

The worker is no longer scaffolding-only. `EMBED` is implemented end-to-end for real-time embeddings, and `GENERATE` now has a pure worker foundation for single-shot model calls. The existing `runEmbeddingSyncBatch` cron-batch (`/api/v1/internal/ai/embeddings/sync`, every 2 min) stays as a safety-net backfill until the worker path is confirmed stable in production.

## Background — Why a separate AI worker, not embedding-in-place

A prior conversation (phase-15, brain note) identified that the existing `Dockerfile.worker` image is intentionally framework-free / no Prisma / no DB client (see `package.worker.json`, `src/workers/tsup.config.ts:19-21,32-34`). PDF and ZATCA were built for that constraint: app fetches data, packs a context snapshot in the job payload, worker does pure compute, app persists results via `setupPdfResultHandler` / `setupZatcaResultHandler` listening to `QueueEvents` (`src/modules/billing/services/workers-init.ts`).

Two options were on the table for AI work:

- **A. Pure AI worker** — match the ZATCA contract. Worker has zero DB access; orchestration lives in the app layer. Slim image preserved; one Dockerfile across all worker types. Requires refactoring AI logic to receive pre-fetched context instead of doing Prisma reads inside the worker.
- **B. Separate DB-capable worker image** (`Dockerfile.worker.db` + `package.worker.db.json`). Two image classes side-by-side. Avoids refactor, doubles infra surface.

**Decision: A.** Most of the AI roadmap is naturally stateless (`(input, context) → output`). The ZATCA pattern is proven for complex multi-step jobs. Slim images matter more for AI workers than for PDF/ZATCA because AI workers will scale wider on queue depth. Option B remains available later if agent-with-tools workloads force mid-flight DB access.

## What's Done

### New files

- `apps/experts-app/src/workers/ai/ai.worker.ts` — pure BullMQ worker on the `ai` queue. Kind-discriminated dispatch; throws on unknown kind. Concurrency + rate limiter env-driven (`AI_WORKER_CONCURRENCY`, `AI_WORKER_LIMITER_MAX`, `AI_WORKER_LIMITER_DURATION_MS`). Observability events: `ai.worker.{ready,active,failed,error}`.
- `apps/experts-app/src/workers/ai/start-ai-worker.ts` — entrypoint mirroring `start-zatca-worker.ts`. Loads dotenv (`.env.local` → `.env` → `.env.test`), validates `DATABASE_URL` + `REDIS_URL`, dynamic-imports the worker module, sets up `SIGTERM`/`SIGINT` graceful close.
- `apps/experts-app/src/workers/ai/.wakatime-project` — contains `experts-ai`. Re-attributes wall-clock time on this directory to the `experts-ai` WakaTime project for separate billing.
- `apps/experts-app/src/lib/ai/queue/ai.contract.ts` — dependency-free shared worker/app contract. Defines `AI_QUEUE_NAME`, `EmbedJob`, `GenerateJob`, and the `AiJob` discriminated union without importing Redis, observability, Prisma, or provider SDKs.
- `apps/experts-app/src/lib/ai/queue/ai.jobs.ts` — app-side Redis queue singleton plus `enqueueEmbedJob()` and `enqueueGenerateJob()`.
- `apps/experts-app/src/lib/ai/handlers/ai-result.handler.ts` — `setupAiResultHandler()` returning a `QueueEvents` instance the caller must hold. Persists `EMBED` results via Prisma and logs `GENERATE` results as ready for async consumers.
- `apps/experts-app/src/lib/ai/embeddings/processors/embed.processor.ts` — pure worker-side OpenAI embeddings processor.
- `apps/experts-app/src/lib/ai/generation/processors/generate.processor.ts` — pure worker-side OpenAI chat-completion processor for single-shot generation jobs.

### Edits

- `apps/experts-app/src/workers/tsup.config.ts` — added `ai/start-ai-worker.ts` to `entry`. `openai` added to `external` list (linter pre-emptively added it during the edit session).
- `apps/experts-app/package.worker.json` — `openai@^6.37.0` added to `dependencies` (linter pre-emptively added it). Prisma is still excluded — slim image rule preserved.
- `apps/experts-app/package.json` — added `worker:ai` and `worker:ai:test` scripts mirroring `worker:zatca`. Updated the `all` concurrently lane to include `AI` (color `#a78bfa`).
- `apps/experts-app/src/modules/billing/services/workers-init.ts` — wired `setupAiResultHandler()` into `initializeQueueCompletionHandlers()` with the same singleton-guard + observability pattern as PDF/ZATCA. Added `ai` to the `areWorkersInitialized()` return shape. Holds `aiQueueEvents` reference to prevent GC.
- `docker/staging/docker-compose.yml` — added `experts-stg-ai-worker` service. Uses the same shared `loogix/core:experts-stg-worker` image (built from `Dockerfile.worker`) with `command: ["node", "dist/ai/start-ai-worker.mjs"]`. Env: `APP_ENV`, `NODE_ENV`, `REDIS_*`, `DATABASE_URL`, `AI_WORKER_CONCURRENCY` (default 2), `AI_WORKER_LIMITER_MAX` (default 50), `AI_WORKER_LIMITER_DURATION_MS` (default 1000), `OPENAI_SECRET` (required, no default — fails compose-up if missing). Volumes: only `etc/.bash`, `localtime`, `timezone` — no FATOORA/SDK_CONFIG/JAVA_HOME mounts.
- `docker/staging/docker-compose.production.yml` — added `experts-stg-ai-worker` service in `cb1abe26` so the deployed staging compose variant matches the source staging compose.
- `docker/production/docker-compose.yml` and `docker/production/docker-compose.production.yml` — added `experts-prd-ai-worker` service in `2a2ff605` so production has source and deployed compose coverage.

### Verification

- `pnpm typecheck:touched -- src/workers/ai/ai.worker.ts src/workers/ai/start-ai-worker.ts src/lib/ai/queue/ai.jobs.ts src/lib/ai/handlers/ai-result.handler.ts src/modules/billing/services/workers-init.ts` — passed.
- Boundary preserved: worker has zero `@/lib/prisma` or `@prisma/client` imports; all DB access lives in `lib/ai/handlers/`.

## What's Pending

### Operational / infra

- **Staging `.env` additions** — done 2026-05-10. `OPENAI_SECRET` is present; `AI_WORKER_CONCURRENCY`, `AI_WORKER_LIMITER_MAX`, and `AI_WORKER_LIMITER_DURATION_MS` have compose defaults.
- **Production compose** — done 2026-05-10 in `2a2ff605`; `experts-prd-ai-worker` now exists in `docker/production/docker-compose.yml` and `docker/production/docker-compose.production.yml`.
- **Staging deployed compose** — done 2026-05-10 in `cb1abe26`; `experts-stg-ai-worker` now exists in `docker/staging/docker-compose.production.yml`.
- **`pnpm install`** — checked 2026-05-10; `apps/experts-app/pnpm-lock.yaml` already contains `openai@6.37.0`.
- **Worker image rebuild** — verified 2026-05-10 with `APP_VERSION=1.1.9 docker compose -f docker/staging/docker-compose.yml build experts-stg-ai-worker`; AI bundle built without Prisma resolution errors.
- **GitHub worker release flow** — implemented 2026-05-10. Added `.github/ci/docker-worker-release.sh`, `force_build_worker`, worker change detection, worker image build/push, and deploy-side restart for the shared PDF/ZATCA/AI worker services. Compose worker services now accept `EXPERTS_WORKER_IMAGE` with the existing image tags as defaults.
- **GitNexus change detection** — done for the production compose commit; `npx gitnexus detect-changes --scope staged --repo experts` reported no indexed symbol changes.
- **Single-replica caution** — if any AI capability is added that operates on a shared DB-backed queue (like the existing `embedding_sync` table), enforce one replica per worker class OR add row claiming (`FOR UPDATE SKIP LOCKED` / `processing` status). BullMQ-native queues are safe at any concurrency — they only become unsafe if jobs share a DB-side claim.

### Capability work (future, per AI feature)

When the first AI capability ships, the change is local to four files:

1. Add a kind to `AiJob` discriminated union in `src/lib/ai/queue/ai.jobs.ts` with required context fields.
2. Add an enqueue helper next to the kind (mirror `enqueueZatcaJob` shape — set `jobId`, `attempts`, exponential `backoff`).
3. Add a `case` to the worker switch in `src/workers/ai/ai.worker.ts` calling a pure processor in `src/lib/ai/<capability>/processors/`.
4. Add a result branch in `src/lib/ai/handlers/ai-result.handler.ts` that persists via Prisma.

Roadmap items that fit this shape:

- **Real-time embedding-on-publish** — implemented 2026-05-10. Migration of `runEmbeddingSyncBatch` to a kind-discriminated job remains optional and can wait until the cron-batch becomes a bottleneck.
- **RAG indexing pipelines** — chunking + embedding for the `ai_knowledge_documents` / `ai_knowledge_chunks` tables (per `hybrid-ask-ai-rag-plan.md`).
- **Single-shot model calls** — `GENERATE` kind foundation implemented 2026-05-10. Product integrations such as translation assist and event agenda builder still need API/UX wiring.
- **Agent steps** — single-turn agent loops where the app orchestrates multi-step state (mid-flight DB reads still happen in the app layer between turns). If agent-with-tools workloads need mid-flight DB access at agent runtime, escalate to Option B (DB-capable worker image) — see Background.

### Cleanup / follow-ups

- **AI consolidation refactor** — completed 2026-05-10: embedding sync code moved under `lib/ai/embeddings/`, internal route moved under `/api/v1/internal/ai/embeddings/sync`, dead `src/queue/queues.ts` deleted, and admin embeddings UI moved under `/admin/ai/embeddings`.
- **CI worker release script and workflow trigger** — implemented 2026-05-10. Remaining operational validation: run the GitHub workflow manually with `force_build_worker=true` on staging and confirm Docker Hub push plus server restart of `experts-stg-pdf-worker`, `experts-stg-zatca-worker`, and `experts-stg-ai-worker`.

## Required Safety Step

Per `apps/experts-app/CLAUDE.md`: before editing any existing function/class/method, run GitNexus impact analysis (`gitnexus_impact`) for the target symbol and report the blast radius. Before commit, run `gitnexus_detect_changes()` to confirm only expected files changed. The scaffold itself is mostly new files, but `tsup.config.ts`, `package.json`, `package.worker.json`, `workers-init.ts`, and `docker/staging/docker-compose.yml` were modified — verify these are the only existing-file edits.

## Test Plan

Scaffold-only — no behavior to test yet beyond compile + plumbing.

- `pnpm typecheck:touched -- <new + modified files>` — must pass. ✅ Done.
- `TMPDIR=/tmp pnpm worker:ai` locally — passed 2026-05-10; booted, connected, listened idle, and shut down gracefully on timeout SIGTERM. Plain `pnpm worker:ai` failed in this WSL/Codex session before app code ran because `tsx` attempted to create an IPC socket under `/mnt/c/.../Temp`.
- `docker compose -f docker/staging/docker-compose.yml up experts-stg-ai-worker` — should pass env-required checks (or fail loudly on missing `OPENAI_SECRET`).
- `docker compose -f docker/staging/docker-compose.production.yml config --quiet` — passed 2026-05-10 after `cb1abe26`.
- `docker compose -f docker/production/docker-compose.yml config --quiet` and `docker compose -f docker/production/docker-compose.production.yml config --quiet` — passed 2026-05-10 after `2a2ff605`.
- `.github/ci/docker-worker-release.sh` shell syntax — passed `bash -n` 2026-05-10.
- `.github/workflows/experts-app.yml` formatting — passed `pnpm exec prettier --check` 2026-05-10.
- `EXPERTS_WORKER_IMAGE` compose override — verified 2026-05-10 against staging and production deployed compose variants.
- When the first capability lands, full route-test + processor-test coverage per the established ZATCA pattern.

## Assumptions

- AI workloads will be stateless enough that Option A (pure worker) holds for embeddings, RAG, single-shot generation, and agent-step jobs. Mid-flight DB access during agent loops is handled at the app layer between turns.
- A single `ai` queue with kind-discriminated jobs is sufficient for now; per-capability queues can be split later if noisy-neighbour effects appear (e.g. RAG indexing crowding out agent latency).
- `openai` SDK is the primary provider. Anthropic / Google GenAI SDKs can be added to `package.worker.json` and `tsup.config.ts` `external` list when needed without rearchitecting.
- WakaTime `.wakatime-project` markers are gitignored locally; each developer manages their own. Markers placed at:
  - `apps/experts-app/src/lib/ai/`
  - `apps/experts-app/src/components/ai/`
  - `apps/experts-app/app/api/v1/ai/`
  - `apps/experts-app/app/api/v1/internal/ai/`
  - `apps/experts-app/src/lib/recommendations/`
  - `apps/experts-app/src/workers/ai/` (new)
  - `apps/experts-app/prisma/migrations/20260429120000_add_ask_ai_conversations/`
  - `apps/experts-app/prisma/migrations/20260429130000_add_ai_knowledge_base/`
- The existing cron-driven embedding pipeline stays as-is. Migration to the new worker is opt-in per capability, not a forced cutover.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
