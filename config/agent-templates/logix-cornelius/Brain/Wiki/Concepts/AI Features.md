---
title: "AI Features"
date: "2026-04-16"
tags: ["topic/ai", "project/experts-app", "topic/creator-tools"]
category: "topic"
source: "codex"
source_id: "Wiki/Concepts/AI Features.md"
updated: "2026-07-15"
---

# AI Features — Experts App

## Overview

AI-powered creator tools built on top of OpenAI `gpt-4o-mini` via the `openai` npm package. All AI endpoints live under `app/api/v1/ai/`.

## Architecture

### API endpoint

`POST /api/v1/ai/suggest`

**Auth:** Session required. Role must be `instructor` or `admin`.

**Rate limit:** 20 requests / user / hour. Fixed-window counter in Redis at `ai:suggest:rl:<userId>`. Fails open if Redis is unavailable.

**Request shape:**

```ts
{
  entityType: "course" | "event" | "lesson",
  fieldType: "title" | "description" | "content" | "outcomes" | "requirements" | "tags" | "quiz_questions",
  context: {
    title?: string,       // max 120 chars
    description?: string, // max 220 chars
    category?: string,    // max 80 chars
    level?: string,       // max 40 chars
    eventType?: string,   // max 60 chars
    count?: number,       // used by quiz_questions (1–10, default 5)
  },
  locale: "en" | "ar" | "es"
}
```

**Response shape:**

- Success: `{ suggestion: string }` — single string for text fields; newline-separated items for list fields; **JSON array string** for `quiz_questions`.
- Error: `{ errorCode: string }` with appropriate HTTP status. Codes: `ai_busy`, `ai_unavailable`, `ai_config_error`, `ai_no_context`, `ai_rate_limited`, `ai_unknown`.

**Token budgets:**

| fieldType                     | max_tokens |
| ----------------------------- | ---------- |
| title, description            | 100        |
| outcomes, requirements, tags  | 200        |
| content (course/event/lesson) | 800        |
| quiz_questions                | 1200       |

### Context sanitization

All context strings are: stripped of newlines (prompt injection prevention) and truncated to safe lengths before being embedded in prompts. Prompt instructions are always in English; the `locale` param only controls the response language.

### Client hooks

- `use-ai-suggest.ts` — base hook, stores `errorCode: string | null`.
- `use-ai-suggest-list.ts` — wraps the base hook, splits newline response into `string[]`, strips leading bullet symbols.
- `use-ai-quiz-questions.ts` — calls `fieldType: "quiz_questions"`, parses JSON response (strips markdown fences), returns `GeneratedQuestion[]` with auto-generated IDs. Fails gracefully to `errorCode: "ai_unknown"` on parse failure.

### UI components

- `AiSuggestButton` (`src/components/ui/ai-suggest-button.tsx`) — ghost button triggering a HeroUI Popover with suggestion preview + Use this / Try again / Dismiss actions. Accepts `resolveError(code)` callback for i18n.
- `AiSuggestListButton` (`src/components/ui/ai-suggest-list-button.tsx`) — same pattern but shows a checklist. Items auto-selected on arrival; user can toggle. Add all / Add selected (N) appends to existing list.

## Where AI suggest is wired

| Location                   | Fields                              | Component                                                        |
| -------------------------- | ----------------------------------- | ---------------------------------------------------------------- |
| Course details section     | title, description, content         | `CourseDetailsSection`                                           |
| Course extras section      | outcomes, requirements, tags        | `CourseExtrasSection`                                            |
| Event general section      | title, description, content         | `EventGeneralSection`                                            |
| Event extras section       | outcomes, requirements              | `EventExtrasSection`                                             |
| Lesson dialog (curriculum) | content ("Draft for me")            | `LessonDialog` — `AiSuggestButton` with `entityType="lesson"`    |
| Quiz dialog (curriculum)   | quiz_questions ("Generate with AI") | `QuizDialog` — `useAiQuizQuestions` inline, pending review panel |

## Quiz question generation flow

1. Instructor clicks "Generate with AI" in the quiz dialog header.
2. `useAiQuizQuestions.generate({title, description, count: 5})` fires.
3. API returns JSON array → parsed into `GeneratedQuestion[]` with crypto UUIDs.
4. Questions appear in a review panel below the buttons (question text preview, numbered list).
5. "Add to quiz" merges them into `quizForm.questions`; "Dismiss" discards.
6. Questions go in as `type: "multiple_choice"`, `points: 1`, 4 options each with exactly one `isCorrect: true`.

## i18n

All AI copy lives in `creator.courses.form` under these keys:
`aiSuggest`, `aiAccept`, `aiRetry`, `aiDismiss`, `aiGenerating`, `aiSuggestList`, `aiAddAll`, `aiAddSelected`,
`aiDraftLesson`, `aiGenerateQuestions`, `aiAddQuestion`, `aiQuestionsReady`, `aiAddToQuiz`, `aiErrors.*`

All 3 locale files updated for courses (en/ar/es). Events locales carry the shared keys from Tier 1.

## Environment variables

- `OPENAI_SECRET` — OpenAI API key. Required for AI features; endpoint returns `ai_config_error` if missing.
- `REDIS_URL` — used for rate limiting. Features work without it (fails open).

## Embedding pipeline — AI worker (real-time) + cron batch (fallback)

Two paths write to the same `content_embeddings` table; both are active simultaneously.

### Real-time path (AI worker queue)

Triggered on publish and on content updates that touch embedding-relevant fields.

| File                                                  | Role                                                                                  |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `src/lib/ai/queue/ai.jobs.ts`                         | `EmbedJob` type + `enqueueEmbedJob()` with deduped jobId                              |
| `src/lib/ai/embeddings/embed.service.ts`              | App-side: text fetchers + fire-and-forget `enqueueEmbedOnPublish()`                   |
| `src/lib/ai/embeddings/processors/embed.processor.ts` | Worker-side: pure, zero Prisma, calls OpenAI `text-embedding-3-small`                 |
| `src/lib/ai/handlers/ai-result.handler.ts`            | App-side result handler: `$executeRaw ::vector` upsert + marks `EmbeddingSync` synced |

**Deduped jobId:** `embed:entityType:entityId` — rapid edits to the same entity collapse to a single queue entry. 3 attempts, exponential backoff (2 s base).

**Text fetched app-side** before enqueuing. Worker receives plain text string in the job payload — no DB access in the worker.

**`$executeRaw ::vector` is required** for all embedding column writes. Prisma types `vector(1536)` as `never` in the generated client, so `prisma.contentEmbedding.create()` cannot be used.

### Cron/batch path (fallback reconciliation)

| File                                              | Role                                                                          |
| ------------------------------------------------- | ----------------------------------------------------------------------------- |
| `src/lib/ai/embeddings/embedding-sync.service.ts` | Row processor: fetches text, calls OpenAI, upserts via `$executeRaw ::vector` |
| `src/lib/ai/embeddings/embedding-sync.batch.ts`   | Drains pending `EmbeddingSync` rows sequentially (max 50/run)                 |
| `app/api/v1/internal/ai/embeddings/sync/route.ts` | HTTP endpoint called by Docker cron sidecar every 2 min                       |

Cron skips rows already marked `synced` by the result handler, so worker-processed entities are never double-embedded. Cron batch exists as a safety net for missed real-time events and initial backfills.

### Re-embed triggers

| Handler                     | Trigger                      | Fields that trigger re-embed                              |
| --------------------------- | ---------------------------- | --------------------------------------------------------- |
| `course-publish.handler.ts` | Course publish               | — (always on first publish)                               |
| `course-update.handler.ts`  | Course update (if published) | `title`, `description`, `tags`, `categoryId`              |
| `event-create.handler.ts`   | Event create (if published)  | — (always on first publish)                               |
| `events/[id]/route.ts` PUT  | Event update (if published)  | `title`, `description`, `tags`, `eventType`, `categoryId` |
| `posts/route.ts` POST       | Post create                  | — (posts always published on create)                      |
| `posts/[id]/route.ts` PUT   | Post update (if published)   | `title`, `content`, `description`, `category`, `tags`     |

### Observability events

| Event                    | Level | Where                                 |
| ------------------------ | ----- | ------------------------------------- |
| `ai.embed.enqueued`      | info  | `embed.service.ts`                    |
| `ai.embed.enqueue.skip`  | warn  | `embed.service.ts` (entity not found) |
| `ai.embed.enqueue.error` | error | `embed.service.ts` (catch-all)        |
| `ai.embed.started`       | debug | `embed.processor.ts`                  |
| `ai.embed.completed`     | info  | `embed.processor.ts`                  |
| `ai.embed.persisted`     | info  | `ai-result.handler.ts`                |
| `ai.suggest.request`     | info  | `ai/suggest/route.ts`                 |
| `ai.suggest.completed`   | info  | `ai/suggest/route.ts`                 |
| `ai.suggest.error`       | error | `ai/suggest/route.ts`                 |
| `ai.ask.question`        | info  | `ask-ai-assistant.ts`                 |
| `ai.ask.answered`        | info  | `ask-ai-assistant.ts`                 |
| `ai.ask.openai_error`    | error | `ask-ai-assistant.ts`                 |
| `ai.ask.config_error`    | error | `ask-ai-assistant.ts`                 |

## Recommendations

- Content embeddings remain the semantic index in `content_embeddings`.
- Dashboard personalization uses cached user interest vectors in `user_recommendation_profiles`.
- Profile refresh is batched by Docker cron through `POST /api/v1/internal/recommendations/profiles/refresh`, authenticated with `CRON_SECRET`.
- Profile signals use the last 90 days of completed/active enrollments, event registrations, bookmarks, ratings, likes/reactions, and authenticated views. Signals without matching content embeddings are ignored.
- `GET /api/v1/recommendations/personalized` returns personalized course/event/post cards for authenticated dashboard users and falls back to latest published visible content for missing, stale, or low-signal profiles.
- Detail-page "You might also like" stays item-to-item based on source content embeddings, not browsing history.

## Public feature page positioning

`/features` now presents AI in two groups:

- **Available now:** creator content drafts, quiz question generation, semantic discovery, personalized dashboard recommendations, and unified related content across courses/events/posts.
- **Possible future AI capabilities:** translation assistance, event agenda builder, controlled platform content tutor, adaptive learning paths, creator performance insights, and content quality review.

Important copy distinction: available features are written as shipped platform capabilities; future items are intentionally framed as "possible future" or "planned next" so the marketing page does not over-promise.

## Ask AI global assistant

First implementation branch: `codex/ask-ai-global-assistant`.

- UI surface: floating global "Ask AI" button rendered from app providers.
- Rollout gate: client-side Statsig gate `ask_ai_global_assistant`.
- Access control: only authenticated admins see the UI; API route also requires admin permissions server-side.
- API route: `POST /api/v1/ai/ask`.
- Context source: compact live DB context assembled from published courses, events, community posts, active subscription plans, and business/platform facts.
- Intended use: answer admin questions about courses, events, products/services, platform content, and business/company context.
- Current limitation: not yet full RAG over all content embeddings; useful first slice for admin workflow validation.

## Planned future work (remaining)

### Subscription gating

- Enforce AI access only for paid plans that include the `"AI content generation"` entitlement (Expert and Institution).
- Keep `features.aiTools` exposed in `ActivePlanDTO` so creator UIs can disable AI actions before API calls.

### Tier 3

- **Translation assist** — translate title/description fields to Arabic/Spanish.
- **Event agenda builder** — suggest time-boxed agenda items from event metadata.

### Embedding pipeline — pending ops

- Add `OPENAI_SECRET` to staging `.env` (required for AI worker embedding path).
- Validate AI worker embedding end-to-end on staging: publish a course → check `content_embeddings` row via DB.
- Decommission `runEmbeddingSyncBatch` cron call once the worker path is confirmed stable in production.
- Move admin embeddings UI under `admin/ai/embeddings/` (currently under `admin/recommendations/`).

### Recommendations and AI roadmap

- Run staging QA for dashboard recommendations after migration and cron deploy.
- Monitor whether `user_recommendation_profiles` refresh volume stays cheap enough on VPS cron; move to a real queue if refresh cost grows.
- Decide which public feature-page AI roadmap item should become the next implementation slice.
- Consider a controlled content tutor only over approved platform content, not an unrestricted AI tutor, to reduce cheating/accreditation risk.
- Configure Statsig gate `ask_ai_global_assistant` and validate the admin-only assistant in staging.
- Add vector/RAG retrieval to Ask AI if compact DB context is too shallow for course/event/detail questions.

## Gotchas

- `openai` was in `devDependencies` — moved to `dependencies` as part of this implementation.
- The course edit form schema (`CourseFormSchema`) did not previously include `learningOutcomes`, `requirements`, `tags` — these were only in the create schema. Added in this session; the update handler already supported all three fields.
- List suggestions use newline-separated plain text, not JSON. The hook splits on `\n` and strips bullet symbols. This is more robust than JSON parsing against model variation.
- `prisma.contentEmbedding.create()` cannot be used for the `embedding` column — Prisma types `vector(1536)` as `never`. Always use `prisma.$executeRaw` with `::vector` cast for any embedding column write.
- Worker files must import from `@/lib/observability/worker-observe` (no DatabaseObserver). App-side files (handlers, services) use `@/lib/observability` (full observer stack). Mixing these causes runtime errors.
- `embedding-sync.service.ts` and `embedding-sync.batch.ts` live under `src/lib/ai/embeddings/` (not `src/lib/recommendations/sync/`). The old `recommendations/sync/` location was deleted in the 2026-05-10 restructuring session.
- The internal cron route is now at `/api/v1/internal/ai/embeddings/sync`. The old `/api/v1/internal/embeddings/sync` is gone. All 5 compose files were updated.
