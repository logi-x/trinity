---
title: "Prompts"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["inbox", "legacy"]
category: "inbox/legacy"
source: "migrated"
source_id: "Inbox/Legacy Random/prompts.md"
---
There's an issue with exam's form dirty state tracking

Unsaved changes, yet save changes button remains disabled

---

Great, that''s fixed now...

I found another related issue in all dialogs, when I change an input -> becomes dirty correctly -> save changes correctly -> change another input -> dirty state becomes broken, and doesn't detect new changes

---

Let's align exam dialog to quiz dialog and add things like ( exam's own version )

Cooldown (minutes)
No cooldown
Note: Cooldown is optional. Leave it blank to allow immediate retries after each attempt.

the alert

Hidden from learners
Draft quizzes do not appear in the learner curriculum and won't block progress.

and notes at the end

---

Is it worth implementing a url/localStorage state persistence for all dialogs? What are the advantages and disadvantages?

---

I want to extract this section

@experts/apps/experts-app/app/(i18n)/\_shared/creator/courses/[id]/curriculum/sections/quiz-dialog.tsx:742-846

and create an enhanced reusable component that's features rich and uses existing features like:

react-photo-view

filesize

enhanced previews

etc...

so it can be re-used across quizzes/exams/lessons etc...

We might consider using @experts/apps/experts-app/src/components/carousel/gallery.tsx later on in @experts/apps/experts-app/app/(i18n)/\_shared/courses/[id]/learn/page.tsx

---

The data model is the constraint — the quiz/exam question schema only has imageUrl: string | null and fileUrl: string | null. The component should be designed for the general case (multiple of each) and the quiz-dialog simply constrains it to 1 via maxImages/maxFiles. Let me also build one unified dropzone that categorizes drops by MIME type.

So, what are my options to make the uploads more dynamic ?

I found this in the schema

@experts/apps/experts-app/prisma/schema.prisma:456-481

we might create CourseResource and link all course resources to it including lesson video which replaces LessonResource and imageUrl/fileUrl in both CourseExamQuestion and QuizQuestion, so instead of one video per lesson due to videoUrl which results in the same constraint

Is this doable, and is it better to do so ?

---

I want to create assets at the course level, so we can reuse them in quizzes/exams/lessons etc...

following up on this @brain-v2/Wiki/Concepts/Assessments.md:24-25 which was planned here /home/logix/brain-v2/Raw/plans/course-assets-plan.md and a summary of it here /home/logix/brain-v2/Raw/sources/2026-04-17-experts-course-media-platform-session.md

I want to create assets at the course level, so creator can upload all assets needed for the student to review before starting learning or explore while learing

currently, /creator/courses/[id]/curriculum when first loaded, it shows

Lesson workspace
Add learning content to [course_name]

and a box

Choose a chapter and lesson type
The selected content editor will appear here.

There should be an upper level before diving into modules -> lessons/quizzes/exams which has the course level assets, with explanation for it, similar to what we described above, and I should be able to navigate backand forth to/from it

---

I want to create a learner landing page, or enhance existing one, to show the course level assets.

---

I want to create Ask AI global assistant, that can answer questions about a course, events, products, services, etc... as well as learn about the business and the company.

---

The colors feels off somehow, right ?

I think it uses the colors from

- **Brand logo component** lives in `src/components/icons/experts/logos.tsx`: `logo`, `logoSmall`, `logoFull`, `footerFullLogo`, `footerFullLogoV2`. SVG with two linear gradients (leaf: `#B1DF10→#5F8A02`, X: `#2AAECF→#2A5E9B`) plus neutral wordmark path (`#939393`).

What I want to do the inverse, use colors from /home/logix/experts/apps/experts-app/app/globals.css to update the logo's colors, what colors might be used ?

---

I want to create a Gallery, all files uploaded by me "auth user", sorting by file type, size, etc... directory structure, a full storage implementation, and usage tracker, so we can add limits later on for each subscription

---

To understand the structure we're aiming for

We have:

- course-level assets
- per-lesson assets
- single asset resource per lesson-type
- per-quiz/exam assets

I do want stronger control for all of the above, but we''ll come to that later on...

And I want to unify how things gets uploaded

Currently:
Course-level materials, has Add link or URL and Upload buttons, and not the new DND drop zone

the new DND drop zone should be

When the dropzone is shown, selected by default shows DND and
@experts/apps/experts-app/src/components/ui/single-asset-source-input.tsx:71-84
says Paste Url which's when clicked shows the input, and the button changes to upload

Or even better, convert
@experts/apps/experts-app/src/components/ui/single-asset-source-input.tsx:71-84
to tabs Upload "shows DND", Paste URL "shows input"

Also, we might add a new tab shown only for specific cases like audio (record) section

This logic should be applied to all levels

- course-level assets
- per-lesson assets
- single asset resource per lesson-type
- per-quiz/exam assets

for consistency, and much better/cleaner UX

I do want stronger control for all of the above, but we''ll come to that later on...
I do want stronger control for all of the above, but we''ll come to that later on...
I do want stronger control for all of the above, but we''ll come to that later on...
I do want stronger control for all of the above, but we''ll come to that later on...

---

I want to create an announcement banner at the top of the page, that can be used to announce important news, updates, etc...

- the main idea which can be extended later on, is to add something similar to an online store, that says @user just bought [product name], in experts case, it could say @user just enrolled in [course name], or @user just completed [lesson name], or @user just passed [quiz/exam name], etc... and it should be instant, not delayed might use a websocket for that.

Let's make it as a Statsig experiment, that can be used to test the announcement banner, and can be extended later on to add more features like:

- add a link to the announcement banner
- add a button to the announcement banner
- add a image to the announcement banner
- add a video to the announcement banner
- add a audio to the announcement banner
- add a text to the announcement banner
- add a countdown to the announcement banner
- add a notification to the announcement banner
- add a popup to the announcement banner

and acceible only to admins/moderators

---

I think it's a good time to create Ask AI global assistant, that can answer questions about a course, events, products, services, etc... as well as learn about the business and the company.

in a new branch...

we might as well make it as Statsig gated feature, available to admins only

---

What about searching for courses, events, products, services, etc... ? How can we make it more intelligent ?

---

How to do what you suggested earlier?
Longer term, better is a hybrid:

DB context for live content and metrics.
Code-derived context for product rules and operational behavior.
Vault/company docs for branding, business, policies, and playbooks.
Later, index all of that into embeddings/RAG so Ask AI retrieves relevant chunks instead of hardcoding every context builder.

---

GREAT, what about searching for courses, events, products, services, etc... ? How can we make it more intelligent ?
@experts/apps/experts-app/src/components/GlobalSearch.tsx

---

Recommended Phases

Now: Add company profile + brand guidelines as structured context.
Next: Add embeddings/RAG for company docs, courses, events, posts, plans.
Then: Track questions and feedback.
Later: Fine-tune only if the assistant repeatedly fails on tone, format, or classification despite good context.
Important distinction

RAG = teaches it facts dynamically.
Prompt/brand profile = teaches it how to speak.
Feedback data = teaches your system what to improve.
Fine-tuning = changes model behavior, but should come later.

---

let's enhance the Ask AI button and maybe use a shimmer effect from e.g.

```tsx
import { AnimatedShinyText } from "@/components/ui/animated-shiny-text";
import { ShinyButton } from "@/components/ui/shiny-button";
import { Spinner } from "@heroui/react";
import { StarsIcon } from "lucide-react";

<div
  className="group relative mx-auto flex items-center justify-center cursor-pointer"
  onClick={getNewStats}
>
  <ShinyButton className="flex items-center justify-center cursor-pointer">
    {isGenerating ? (
      <div className="flex items-center gap-2">
        <Spinner size="sm" />
        <AnimatedShinyText className="text-sm font-medium">
          Generating...
        </AnimatedShinyText>
      </div>
    ) : (
      <>
        <StarsIcon className="w-3 h-3 " />{" "}
        <AnimatedShinyText className="text-sm font-medium">
          Generate AI Insights
        </AnimatedShinyText>
      </>
    )}
  </ShinyButton>
</div>;
```

Read the prior conversation. The constraint is real and the prior recommendation was to **add a separate worker image class** (`Dockerfile.db-worker` or similar) rather than violate the pure-worker boundary. That recommendation was never implemented — the team chose the cron-sidecar HTTP path instead, which is what's running today. So you're effectively reopening the question with wider scope.

Confirmed the constraint is still in force:

- `package.worker.json` has 9 deps, no `@prisma/client`, no AI SDKs
- `tsup.config.ts` line 21: `// Workers are framework-free: NO Prisma, NO DB client`
- `tsup.config.ts` line 33: `// Workers are pure - no Prisma, no dynamic imports`

This isn't accidental — it's the whole point of that image. Adding `@prisma/client` (with engines) inflates the slim image by ~50MB and pulls in postgres drivers. Adding `openai` + `@google/genai` + `@anthropic-ai/sdk` adds another ~5–10MB. PDF and ZATCA workers don't need any of that.

## The three real options

### A. Pure AI worker — extend the existing image, no DB access

Match the ZATCA contract exactly: app fetches context, packs it into the job payload, worker does pure compute, results return via BullMQ/`QueueEvents` and the app persists.

```
job payload:    { kind: "EMBED", text: "...assembled by app...", entityType, entityId, requestId }
worker action:  openai.embeddings.create(text) → return { vector }
app side:       QueueEvents listener writes to content_embeddings + flips embedding_sync row
```

**Add to `package.worker.json`:** `openai`, eventually `@google/genai`/`@anthropic-ai/sdk`.
**Don't add:** `@prisma/client`.
**Add to `tsup.config.ts` entry array:** `ai/start-ai-worker.ts`.

Costs: refactoring required. Today's `runEmbeddingSyncBatch` does multi-table Prisma joins (`fetchCourseText`, `fetchEventText`, `fetchPostText`) inside the function. To go pure, those fetches move into the enqueueing service in `lib/ai/embeddings/`, and the worker only sees pre-assembled text.

Architecturally this is **strictly better** — proper separation of concerns, mirrors ZATCA, no duplicate DB connection pools in worker containers.

Works well for: **embeddings, RAG retrieval, single-shot model calls, vector indexing of known content**. These are all stateless I/O.

### B. Separate DB-capable worker image — `Dockerfile.worker.db` + `package.worker.db.json`

Two image classes living side-by-side. Pure image stays pure (PDF, ZATCA). New DB image includes `@prisma/client` + AI SDKs for workloads that legitimately need mid-flight DB access.

This is what the prior conversation recommended. Costs: two Dockerfiles, two slim package manifests, two tsup configs (or one with multiple targets), two compose service classes. Roughly doubles infra surface.

Works well for: **agent systems with tools** (the agent loop calls Prisma between model turns), **long-running pipelines that materialize intermediate state**, and as a transitional path for the existing embedding sync code without a refactor.

### C. Hybrid — both A and B as you grow into them

Pure AI worker for stateless work, DB-capable AI worker only when agent tooling forces it.

## My recommendation: start with A, add B only when an agent forces it

The reasoning, concretely:

1. **Most of your roadmap is naturally stateless.** Embeddings, RAG retrieval, recommendation scoring, vector pipelines — all of these are `(input, context) → output` with no need for DB access mid-execution. Pre-fetching context in the app and passing snapshots in job payloads is the correct shape.
2. **You already have a worker image. Re-using it has compounding payoff.** One Dockerfile, one slim manifest, one tsup config, one CI lane.
3. **The ZATCA pattern is proven.** It handles complex multi-step jobs without DB access. The `workers-init.ts` QueueEvents wiring is exactly the result-persistence pattern AI workers need.
4. **Image size matters more for AI workers than PDF/ZATCA.** AI workers will scale wider (queue depth from agent runs, embedding backfills); slim images mean faster cold starts and lower memory on each replica.
5. **You only pay the B tax when you actually need it.** If/when agents-with-tools land and you discover the pre-fetch pattern is impractical for tool loops, you spin up `Dockerfile.worker.db` then. No premature infra.

For the existing embedding sync specifically: **don't migrate it to the worker yet**. Keep `runEmbeddingSyncBatch` as a cron-batch in the app container — it works, it's calibrated, and migrating means refactoring the Prisma joins out. Build the new pure AI worker for _new_ AI work first (real-time embedding-on-publish, RAG indexing pipelines, agent runs that fit the pure model). Migrate the cron-batch later, or never — its 2-minute cadence is fine for backfills.

## Concrete contract for the pure AI worker

```ts
// Job kinds (one queue, ZATCA-style discriminator)
type AiJob =
  | { kind: "EMBED"; text: string; entityType; entityId; requestId }
  | { kind: "GENERATE"; prompt: string; model; params; requestId }
  | { kind: "RAG_QUERY"; query: string; ctx: ChunkSnapshot[]; requestId }
  | { kind: "AGENT_STEP"; conversation: Snapshot; requestId }; // single turn only
```

**Worker rule:** zero Prisma imports, zero `@/lib/prisma` references, zero outbound HTTP except to AI providers. If a job needs DB data, the enqueueing service in `lib/ai/...` fetches and packs it.

**App rule:** `QueueEvents` listener (mirror `workers-init.ts`) catches `completed` events, writes results via Prisma, marks tracking rows.

**Rate limiting:** put it on the BullMQ Worker constructor — `limiter: { max: 50, duration: 1000 }` tuned to your OpenAI tier's TPM. Critical; without it the queue will eat 429s.

## Concrete next steps if you go with A

1. Decide: one `ai` queue (kind-discriminated, ZATCA-style) or per-capability queues. **Recommendation: one queue.**
2. Add to `package.worker.json`: `"openai": "^6.37.0"` (you already have it elsewhere).
3. Add to `tsup.config.ts` `entry` array: `resolve(__dirname, "ai/start-ai-worker.ts")`.
4. Add to `tsup.config.ts` `external` array: `"openai"` (and any other provider SDKs).
5. Scaffold `src/workers/ai/{ai.worker.ts, start-ai-worker.ts}` mirroring `zatca/`.
6. Add `worker:ai` and `worker:ai:test` to `package.json` scripts; add to the `all` concurrently lane.
7. Add `ai-worker` service to `docker/staging/docker-compose.yml` mirroring `zatca-worker`, with CMD override `["node", "dist/ai/start-ai-worker.mjs"]`.
8. Wire `QueueEvents` in `workers-init.ts` for the new `ai` queue, mapping completion → DB persistence.
9. Drop a `.wakatime-project` file in `src/workers/ai/`.

This keeps **one** worker image, **one** Dockerfile, **one** slim manifest — and gives you a real AI worker container that scales independently and bills cleanly to `experts-ai`.

Want me to scaffold the empty templates (`ai.worker.ts` skeleton, `start-ai-worker.ts` skeleton, tsup + package.worker.json + docker-compose updates) without any AI logic yet — just the structural plumbing — so you can add capabilities incrementally?

Ok, let's apply new proposed structure in a new branch

boundary calls you should make:

1. yes, recommendations is fundamentally AI-driven
2. use option (a) and follow the convention

---

Let me map what's actually there before I propose anything.

Yes — there's already one AI worker hiding in plain sight: `src/lib/recommendations/sync/embedding-sync.worker.ts` (with its `embedding-sync.service.ts` partner). It doesn't follow the `src/workers/{pdf,zatca}/` co-located pattern the rest of the app uses, and it's filed under `recommendations` rather than `ai` — which is exactly the scattering you want to fix.

## What's actually scattered today

AI-domain code spread across three roots:

| Root                               | What's there                                                                                                                                                                                              |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `src/lib/ai/`                      | `knowledge/` (RAG: chunking, retrieval, sources), `ask/` (assistant)                                                                                                                                      |
| `src/lib/recommendations/`         | `sync/embedding-sync.{worker,service}.ts`, `dto/embedding-sync.dto.ts`, `queries/embedding-sync-status.query.ts`, `commands/embedding-sync-enqueue.command.ts`, `profiles/user-recommendation-profile.ts` |
| `src/components/ai/`               | `AskAiAssistant.tsx`                                                                                                                                                                                      |
| `app/api/v1/ai/`                   | `suggest/`, `ask/`                                                                                                                                                                                        |
| `app/api/v1/internal/ai/`          | `knowledge/sync/`                                                                                                                                                                                         |
| `app/api/v1/internal/embeddings/`  | `sync/` ← AI but not under `ai/`                                                                                                                                                                          |
| `app/api/v1/admin/embeddings/`     | `stats/`, `retry-failed/` ← AI but not under `ai/`                                                                                                                                                        |
| `app/(i18n)/.../admin/embeddings/` | admin UI ← AI but not under `ai/`                                                                                                                                                                         |

The recurring pattern: **anything embedding-related is filed by _consumer_ (recommendations, admin) instead of by _AI capability_**. That's the bug.

## Proposed structure

```
apps/experts-app/src/lib/ai/
├── ask/                    # existing — assistant conversations
├── knowledge/              # existing — RAG: chunking, retrieval, sources
├── embeddings/             # NEW — vector pipeline (move from recommendations/sync)
│   ├── embedding-sync.service.ts
│   ├── embedding-sync.worker.ts
│   ├── embedding-sync.dto.ts          (← from recommendations/dto)
│   ├── embedding-sync.queries.ts      (← from recommendations/queries)
│   ├── embedding-sync.commands.ts     (← from recommendations/commands)
│   └── content-embedding.repo.ts      (consolidate ContentEmbedding access)
├── recommendations/        # NEW — AI-ranking layer (move from lib/recommendations)
│   ├── personalized.query.ts
│   ├── content.query.ts
│   ├── candidates.ts
│   └── user-profile.ts
├── agents/                 # NEW — future agent/tool-use systems
├── providers/              # NEW — openai/gemini/anthropic client wrappers + model registry
└── suggest/                # extract from /api/v1/ai/suggest if logic grows beyond a route handler

apps/experts-app/src/workers/ai/                 # NEW — match pdf/zatca pattern
├── embedding-sync.worker.ts                     # re-export wrapper around lib/ai/embeddings
└── start-embedding-sync-worker.ts               # entrypoint, matches start-pdf-worker.ts

apps/experts-app/src/components/ai/              # already exists, fine where it is

apps/experts-app/app/api/v1/ai/                  # public AI endpoints (existing)
apps/experts-app/app/api/v1/internal/ai/         # internal: move embeddings/sync here
│   ├── knowledge/sync/                          # existing
│   └── embeddings/sync/                         # ← from /internal/embeddings/sync
apps/experts-app/app/api/v1/admin/ai/embeddings/ # ← from /admin/embeddings (or keep admin flat, your call)
apps/experts-app/app/(i18n)/_shared/admin/ai/embeddings/  # likewise
```

## Two boundary calls you should make

1. **Does all of `lib/recommendations` move?** If recommendations is fundamentally AI-driven (embedding similarity, vector search, learned profiles) → yes, move the whole thing under `lib/ai/recommendations`. If parts are deterministic ranking/filtering with no model in the loop → keep those out and only move the AI-touching files. Skim `get-personalized-recommendations.query.ts` and decide based on whether it's calling the embedding service or just SQL ranking.

2. **Worker entrypoint pattern.** Your `pdf` and `zatca` workers split into `{name}.worker.ts` + `start-{name}-worker.ts` under `src/workers/`. The embedding worker doesn't have a `start-*` file. When you move it, either (a) follow the convention — keep the logic in `lib/ai/embeddings/` and put the runner under `src/workers/ai/start-embedding-sync-worker.ts`, or (b) break the convention and adopt a new pattern of self-contained AI workers under `lib/ai/embeddings/`. **Recommend (a)** — consistency with existing workers wins.

## Scope guardrails

- **Don't move migrations.** `prisma/migrations/*ai*` and `*ask_ai*` are append-only history. Leave them; the `.wakatime-project` markers I gave you already cover them.
- **Don't break import paths in one giant PR.** Two-pass: (1) move `embeddings` + recommendations split, fix imports, ship. (2) Add `agents/` + `providers/` scaffolding when you actually start building those — empty directories are noise.
- **Update `.wakatime-project` markers as you move.** Specifically: drop one in `src/workers/ai/`, drop one in any newly-AI-attributed admin route folder, and remove the broad `src/lib/recommendations/.wakatime-project` if you only move _some_ of recommendations (otherwise you'll bill non-AI ranking work as AI).

## My recommendation

Do this refactor — but as **one focused PR scoped to embeddings consolidation only**:

1. Move `lib/recommendations/sync/embedding-sync.*` → `lib/ai/embeddings/`
2. Add `src/workers/ai/start-embedding-sync-worker.ts`
3. Move `app/api/v1/internal/embeddings/sync/` → `app/api/v1/internal/ai/embeddings/sync/`
4. Move `app/api/v1/admin/embeddings/` → `app/api/v1/admin/ai/embeddings/` (and i18n admin pages too)
5. Update WakaTime markers
6. Run `gitnexus_impact` on the moved symbols beforehand (per CLAUDE.md), and `gitnexus_detect_changes` before committing

Defer `agents/` and `providers/` until you actually need them — empty folders rot and `lib/ai/providers/` only earns its keep when you have ≥2 model providers to abstract.

Want me to run the impact analysis on `embedding-sync.service` and `embedding-sync.worker` to size the blast radius before you commit to this?

---

I just noticed inconsistency in

/home/logix/experts/apps/experts-app/app/api/v1/events/[id]/route.ts
and
/home/logix/experts/apps/experts-app/app/api/v1/community/posts/[id]/route.ts

why don't we extract handlers similar to

/home/logix/experts/apps/experts-app/src/lib/courses/catalog/handlers/course-update.handler.ts

Also, the naming convention is different in /home/logix/experts/apps/experts-app/src/lib/courses and /home/logix/experts/apps/experts-app/src/lib/events

we're using details and catalog, we should stick with one and apply for all

---

I just noticed inconsistencies in uploading assets.

We need to unify the UX and the logic for uploading assets. Also, database schema naming convention is inconsistent.

- course_exam_question_assets
- lesson_assets
- quiz_question_assets
- course_exam_question_assets

we should stick with one and apply for all

---

I just noticed inconsistencies in uploading assets.

We need to unify the UX and the logic for uploading assets. Also, database schema naming convention is inconsistent.

I just noticed inconsistencies in database schema naming convention, e.g.

- course_exam_question_assets
- lesson_assets

should I prefix with courses\_ or without for all ?

all:

course_modules
course_lessons
course_assets
course_module_assets
course_exams
course_exam_questions
course_exam_options
course_exam_attempts
course_exam_answers
course_exam_question_assets
course_enrollments
course_lesson_progress
lesson_video_watch_states
course_certificates
course_instructors
course_price_versions
lesson_assets
lesson_resources -> just realized as a duplicate of above
lesson_prerequisites -> never used
lesson_video_watch_states

---

The three new incidents — triage

# 16 — Business-logic / authorization (paid-content bypass)

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬──────────┬─────────────────────────────────────────────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────┐
│                                                     Finding                                                      │ Severity │                                          Reachability                                           │                            Dedup                            │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ A. Paid-course completion + certificate forgeable without payment (watch-progress / progress / certificate path) │ HIGH     │ Real — enrollment.status not checked on progress mutations; certificate only checks completedAt │ New, not covered by prior incidents                         │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ B. Quiz content + attempts reachable without enrollment (/quizzes/[id]/start)                                    │ HIGH     │ Real — isPublished is the only gate; quiz IDs leak via course/module DTOs                       │ New                                                         │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ C. Noon API credentials logged via console.log(makeNoonAuthHeader())                                             │ HIGH     │ Real — fires on every Noon checkout intent                                                      │ New — secrets-leakage, rotate Noon creds before fixing code │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────┴─────────────────────────────────────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────┘

Recommended order: C first (5-min fix + rotation), then B (centralize assertCourseAccess), then A (gate progress on enrollment.status === "active"|"completed", server-derive completion before issuing certs). A and B both want the same course-access guard, so plan them together.

# 17 — Secrets leakage + auth lifecycle

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┬──────────┬───────────────────────────────────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────────────────┐
│                                               Finding                                               │ Severity │                                     Reachability                                      │                                  Dedup                                  │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ A. .env.production, .env.staging, .env.e2e, slack.secret tracked in git → forge JWT with admin role │ CRITICAL │ Real — anyone with repo/artifact access can read; auth secret enables session forgery │ New, but related to prior secrets-hygiene work                          │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ B. Role revocation doesn't invalidate live JWT (up to 30 days)                                      │ MEDIUM   │ Real — token.roles only refreshes on sign-in/update                                   │ New — needs token-version or DB-fresh role check on sensitive mutations │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────┴───────────────────────────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────────────────┘

Recommended order: A is a true incident, not a code fix. Sequence is: rotate every secret in those files (DB, Redis, Slack, OAuth, webhooks, NEXTAUTH/AUTH_SECRET) → purge from git history (BFG/git filter-repo) → move to secret manager → add gitleaks pre-commit. Code edits come last. B rolls into the same PR set
as #16-A: derive role from DB (requireAdmin) for mutation routes.

# 18 — Auth / data exposure on public endpoints

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬──────────┬──────────────────────────────────────────────────────────────────────┬───────┐
│                                                    Finding                                                     │ Severity │                             Reachability                             │ Dedup │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼──────────────────────────────────────────────────────────────────────┼───────┤
│ A. Password-reset URL host-header poisoning (getBaseUrl(request) trusts Origin/Host/Referer/x-forwarded-proto) │ HIGH     │ Real — unauth; token captured at attacker domain → password takeover │ New   │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼──────────────────────────────────────────────────────────────────────┼───────┤
│ B. Account enumeration on /api/auth/forgot-password (distinct 404/409/429/200)                                 │ MEDIUM   │ Real — native sibling route already does it right; copy the pattern  │ New   │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼──────────────────────────────────────────────────────────────────────┼───────┤
│ C. Unauth /api/v1/console/health leaks env, version, SHA, integrations, dep errors                             │ MEDIUM   │ Real — GET returns full fingerprint without requireAdmin()           │ New   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────┴──────────────────────────────────────────────────────────────────────┴───────┘

A is the highest-leverage fix here: replace getBaseUrl(request) with a CANONICAL_APP_URL env constant for all secret-bearing emails (reset, verify, checkout callback, enrollment callback) — single chokepoint. B is a 10-line response-shape change. C is a one-liner (requireAdmin() + minimal liveness fallback).

│ slack.secret tracked in git → forge JWT with    │ CRITICAL │ can read; auth secret enables session     │ secrets-hygiene work                 │
│ admin role                                      │          │ forgery                                   │                                      │
├─────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────┼──────────────────────────────────────┤
│ B. Role revocation doesn't invalidate live JWT  │          │ Real — token.roles only refreshes on      │ New — needs token-version or         │
│ (up to 30 days)                                 │ MEDIUM   │ sign-in/update                            │ DB-fresh role check on sensitive     │
│                                                 │          │                                           │ mutations                            │
└─────────────────────────────────────────────────┴──────────┴───────────────────────────────────────────┴──────────────────────────────────────┘

Recommended order: A is a true incident, not a code fix. Sequence is: rotate every secret in those files (DB, Redis, Slack, OAuth, webhooks,
NEXTAUTH/AUTH_SECRET) → purge from git history (BFG/git filter-repo) → move to secret manager → add gitleaks pre-commit. Code edits come last. B
rolls into the same PR set as #16-A: derive role from DB (requireAdmin) for mutation routes.

# 18 — Auth / data exposure on public endpoints

┌──────────────────────────────────────────────────────────────────────────────┬──────────┬─────────────────────────────────────────────┬───────┐
│                                   Finding                                    │ Severity │                Reachability                 │ Dedup │
├──────────────────────────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────┼───────┤
│ A. Password-reset URL host-header poisoning (getBaseUrl(request) trusts      │ HIGH     │ Real — unauth; token captured at attacker   │ New   │
│ Origin/Host/Referer/x-forwarded-proto)                                       │          │ domain → password takeover                  │       │
├──────────────────────────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────┼───────┤
│ B. Account enumeration on /api/auth/forgot-password (distinct                │ MEDIUM   │ Real — native sibling route already does it │ New   │
│ 404/409/429/200)                                                             │          │  right; copy the pattern                    │       │
├──────────────────────────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────┼───────┤
│ C. Unauth /api/v1/console/health leaks env, version, SHA, integrations, dep  │ MEDIUM   │ Real — GET returns full fingerprint without │ New   │
│ errors                                                                       │          │  requireAdmin()                             │       │
└──────────────────────────────────────────────────────────────────────────────┴──────────┴─────────────────────────────────────────────┴───────┘

A is the highest-leverage fix here: replace getBaseUrl(request) with a CANONICAL_APP_URL env constant for all secret-bearing emails (reset, verify
---

The three new incidents — triage

# 16 — Business-logic / authorization (paid-content bypass)

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬──────────┬─────────────────────────────────────────────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────┐
│                                                     Finding                                                      │ Severity │                                          Reachability                                           │                            Dedup                            │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ A. Paid-course completion + certificate forgeable without payment (watch-progress / progress / certificate path) │ HIGH     │ Real — enrollment.status not checked on progress mutations; certificate only checks completedAt │ New, not covered by prior incidents                         │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ B. Quiz content + attempts reachable without enrollment (/quizzes/[id]/start)                                    │ HIGH     │ Real — isPublished is the only gate; quiz IDs leak via course/module DTOs                       │ New                                                         │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ C. Noon API credentials logged via console.log(makeNoonAuthHeader())                                             │ HIGH     │ Real — fires on every Noon checkout intent                                                      │ New — secrets-leakage, rotate Noon creds before fixing code │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────┴─────────────────────────────────────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────┘

Recommended order: C first (5-min fix + rotation), then B (centralize assertCourseAccess), then A (gate progress on enrollment.status === "active"|"completed", server-derive completion before issuing certs). A and B both want the same course-access guard, so plan them together.

# 17 — Secrets leakage + auth lifecycle

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┬──────────┬───────────────────────────────────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────────────────┐
│                                               Finding                                               │ Severity │                                     Reachability                                      │                                  Dedup                                  │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ A. .env.production, .env.staging, .env.e2e, slack.secret tracked in git → forge JWT with admin role │ CRITICAL │ Real — anyone with repo/artifact access can read; auth secret enables session forgery │ New, but related to prior secrets-hygiene work                          │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ B. Role revocation doesn't invalidate live JWT (up to 30 days)                                      │ MEDIUM   │ Real — token.roles only refreshes on sign-in/update                                   │ New — needs token-version or DB-fresh role check on sensitive mutations │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────┴───────────────────────────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────────────────┘

Recommended order: A is a true incident, not a code fix. Sequence is: rotate every secret in those files (DB, Redis, Slack, OAuth, webhooks, NEXTAUTH/AUTH_SECRET) → purge from git history (BFG/git filter-repo) → move to secret manager → add gitleaks pre-commit. Code edits come last. B rolls into the same PR set
as #16-A: derive role from DB (requireAdmin) for mutation routes.

# 18 — Auth / data exposure on public endpoints

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬──────────┬──────────────────────────────────────────────────────────────────────┬───────┐
│                                                    Finding                                                     │ Severity │                             Reachability                             │ Dedup │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼──────────────────────────────────────────────────────────────────────┼───────┤
│ A. Password-reset URL host-header poisoning (getBaseUrl(request) trusts Origin/Host/Referer/x-forwarded-proto) │ HIGH     │ Real — unauth; token captured at attacker domain → password takeover │ New   │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼──────────────────────────────────────────────────────────────────────┼───────┤
│ B. Account enumeration on /api/auth/forgot-password (distinct 404/409/429/200)                                 │ MEDIUM   │ Real — native sibling route already does it right; copy the pattern  │ New   │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┼──────────────────────────────────────────────────────────────────────┼───────┤
│ C. Unauth /api/v1/console/health leaks env, version, SHA, integrations, dep errors                             │ MEDIUM   │ Real — GET returns full fingerprint without requireAdmin()           │ New   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────┴──────────────────────────────────────────────────────────────────────┴───────┘

A is the highest-leverage fix here: replace getBaseUrl(request) with a CANONICAL_APP_URL env constant for all secret-bearing emails (reset, verify, checkout callback, enrollment callback) — single chokepoint. B is a 10-line response-shape change. C is a one-liner (requireAdmin() + minimal liveness fallback).

---
Cross-cutting patterns

1. Single course-access guard is missing. #16-A and #16-B both want the same primitive (assertCourseAccess({ courseId, userId })). Build it once, use it on progress / watch / quiz-start / quiz-submit / certificate routes.
2. session.user.roles is over-trusted. #17-A and #17-B both stem from JWT-embedded roles. Mutation routes should re-derive from DB. Pairs with the assertCourseWriteAccess pattern already shipped in PR #337 (your #6 cleanup).
3. Request-derived URLs are a recurring footgun. #18-A on reset URLs is the same class as forwarded-host issues flagged but not promoted in #18's "other reviewed areas." Centralize on CANONICAL_APP_URL.
4. Secrets posture is incoherent. Tracked env files (#17-A) + active log-leak (#16-C). Both demand rotation, not just code edits.

---
Recommended sequencing if you start today

1. #17-A rotation track (ops, can run in parallel) — rotate AUTH_SECRET, DB, Redis, Slack, OAuth, webhooks; purge tracked env files from history; gitleaks pre-commit. Code PR is small; operational work is large.
2. #16-C hotfix (single-line removal of console.log + Noon credential rotation) — smallest blast radius, highest leakage rate.
3. #18-A + #18-C combined PR (canonical-URL helper + admin gate on health). Cheap and unrelated to the course-access work.
4. #16-A + #16-B + #17-B combined PR — introduce assertCourseAccess + DB-fresh role check, retrofit progress / watch / quiz / certificate routes.
5. #18-B as follow-up to #4 (forgot-password uniform response)

---

● Cluster scan of 32 open Backlog issues. Top 3 candidates by "shared fix shape × close-rate per PR × priority":

Recommended clusters

┌──────┬─────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬─────┬───────────┐
│ Rank │                         Cluster                         │                                   Issues                                   │                                                          Fix shape                                                           │ PRs │   ~Time   │
├──────┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼─────┼───────────┤
│ 🥇   │ C — Stack-trace exposure (spinoffs of EXP-132)          │ EXP-153, 154, 155                                                          │ Wrap stack/details with APP_ENV !== "production" guard. Identical to parent's fix. 3 different routes                        │ 1   │ ~30 min   │
├──────┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼─────┼───────────┤
│ 🥈   │ B — CRON_SECRET timing-safe sweep (spinoffs of EXP-111) │ EXP-114, 115, 116 (+ optionally EXP-152)                                   │ Extract requireCronSecret() helper using timingSafeEqual; apply to 6 cron routes. Identical to parent's recently-shipped fix │ 1   │ ~45 min   │
├──────┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼─────┼───────────┤
│ 🥉   │ A — Storage / R2 subsystem sweep                        │ EXP-148, 149, 147, 146, 103, 128, 124, 127, 122, 110, 109, 106 (12 issues) │ Heterogeneous — bucket-name fixes, DB constraint, ownership checks, query rewrite, reservation reap, notifications wire-up   │ 3–4 │ multi-day │
└──────┴─────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴─────┴───────────┘

---

 let's start working on EXP-291

```
EXP-291  [cluster] Community posts & comments API hardening   (Backlog, no bug label → R3 won't grab the epic)
├─ PR1  posts/route.ts
│   ├─ EXP-281  POST no rate limit
│   └─ EXP-286  GET pagination metadata (totalPosts vs navigable)
├─ PR2  posts/[id]/route.ts
│   ├─ EXP-277  DELETE no admin bypass
│   ├─ EXP-280  PUT reverses admin unpublish (needs Post.adminLockedAt)
│   ├─ EXP-287  GET auth() outside try
│   └─ EXP-288  GET unbounded comment.findMany (OOM)
└─ PR3  posts/[id]/comments/route.ts
  ├─ EXP-289  GET unbounded findMany + write-only cache (OOM)
  └─ EXP-290  POST no validation (amplifies 288/289)

```

make sure to follow Rule#4 from `/home/logix/experts/.claude/routines/_dedup-protocol.md`

---

The freshly-generated work falls into three coherent nests:

┌──────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│           Cluster            │                                                                     Issues                                                                      │                                                               Notes                                                               │
├──────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Community moderation-lock    │ EXP-295 (High, delete admin-locked post), 296/297 (TOCTOU bypass moderation lock), 298 (comments no visibility check), 299 (High, no rate       │ 7 issues, three High, all in the community posts/comments/upload routes — the adminLockedAt moderation gate isn't enforced        │
│ enforcement                  │ limit), 300 (High, internal-upload ignores adminLockedAt), 301 (silent truncate)                                                                │ consistently across paths. Tight, co-located, bundles into ~2 PRs by file.                                                        │
├──────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Community author-email PII   │ EXP-294 (needs-rework) + 310 + 311 + 312                                                                                                        │ Same domain, same files as above — all leak author email. Natural to fold into the moderation cluster's PRs since they touch the  │
│                              │                                                                                                                                                 │ same route handlers.                                                                                                              │
├──────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Tabby geo                    │ EXP-305 (paid-but-not-enrolled, no refund), 307/308/309 (geo-guard stub, currency ternary, missing auth())                                      │ Payments spinoffs from EXP-129. Self-contained, but lower priority and only 305 is meaningful-severity.                           │
└──────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

● Nest wired — all 10 now sit under EXP-295 as the anchor. Zero new issues created.

EXP-295 nest — Community moderation-lock & author-email PII (round 2)

EXP-295 ▸ owner can delete admin-locked post  [High · anchor]
├─ PR A · posts/[id]/route.ts (moderation-lock)
│   ├─ EXP-295  DELETE doesn't check adminLockedAt   [High]
│   └─ EXP-296  PUT TOCTOU bypass                      [Med]
├─ PR B · upload paths (moderation-lock)
│   ├─ EXP-297  thumbnail-upload TOCTOU, orphans R2    [Med]
│   └─ EXP-300  /internal/upload ignores adminLockedAt [High]
├─ PR C · posts/[id]/comments/route.ts
│   ├─ EXP-298  GET no post-visibility check           [Med]
│   ├─ EXP-299  POST no rate limit                     [High]
│   └─ EXP-301  GET truncates >200, no hasMore         [Med]
└─ PR D · author-email PII (shared userBasicInclude/mapUserToDTO leak)
    ├─ EXP-294  detail (comments + post)   ⚠️ needs-rework, PR #820 open
    ├─ EXP-310  embeds endpoint                          [—]
    ├─ EXP-311  post-list endpoint                       [—]
    └─ EXP-312  hashtag/search endpoint                  [—]

Two things the child bodies surfaced that sharpen the plan:

1. EXP-294 already has a stranded PR (#820) in needs-rework. PR D isn't greenfield — its first attempt bounced. The four PII issues all funnel through one root cause: userBasicInclude / mapUserToDTO copy email into every public author DTO. So PR D's real fix is narrowing that shared projection once, then the four
endpoints fall out — which also explains why the single-endpoint #820 attempt was insufficient (it left 310/311/312 leaking the same field).
2. PR A + PR B share the exact adminLockedAt guard shape (the select: {adminLockedAt: true} + 403, or updateMany WHERE-predicate for the TOCTOU variants). EXP-280/PR #792 established the pattern; this nest just propagates it to the four paths #792 missed.

Suggested work order: PR B (two High, simplest guard-propagation) → PR D (closes the PII class + clears the needs-rework loose end via the shared projection fix) → PR C → PR A.

for each issue:

- briefly, explain what's is it about first, and how are you going to fix it. make sure to not introduce new issues while fixing them.
- make sure to follow Rule#4 from `/home/logix/experts/.claude/routines/_dedup-protocol.md`
- read how does the gatekeeper operate first in `/home/logix/experts/.claude/routines/05-gatekeeper.prompt.md`
- you can also read `/home/logix/experts/.claude/routines/03-fix-bugs.prompt.md` and fan out defined sub-agents to help you along the way!
- don't forget to the brain `/home/logix/brain-v2/Raw/agent-state/findings-index.md` after each iteration of attempted fix.

---

In effort to fix linear issues generated by bug/security scanners, some functional behaviors of the app got broken.

Correct way of investigating the issues is to:

- find the related fix done on linear, and any related PRs
- explain why that fix caused the functional behavior to break, as mostly it was working before the fix.
- explain the root cause of the issue
- explain the fix
- explain the test cases that were used to verify the fix
- apply the fix, and make sure to not introduce new issues while applying the fix.

Here are the list of issues:

1. clicking on "Create & Build Curriculum" button on `/creator/courses/create` page fails with "Failed to create course. Please try again." error

```
{
    "error": "Course is already approved"
}

 POST /api/v1/courses/92877f2c-3775-469a-bab2-af7d4ab3e1fd/submit 409 in 99ms (next.js: 81ms, proxy.ts: 3ms, application-code: 14ms)
{"name":"embeddings.sync.batch.empty","level":"info","context":{},"timestamp":"2026-06-04T01:22:00.350Z"}
 POST /api/v1/internal/ai/embeddings/sync 200 in 9ms (next.js: 1543µs, proxy.ts: 2ms, application-code: 5ms)
[browser] Error: Failed to submit course
    at handleCreate (app/(i18n)/_shared/creator/courses/create/page.tsx:102:17)
    at async (src/lib/courses/catalog/forms/use-course-form.ts:61:7)
  100 |         const submitRes = await fetch(`/api/v1/courses/${course.id}/submit`, {method: "PO...
  101 |         if (!submitRes.ok) {
> 102 |           throw new Error("Failed to submit course");
      |                 ^
  103 |         }
  104 |       }
  105 | (https://us-assets.i.posthog.com/static/posthog-recorder.js?v=1.379.2:1:91319)

```

While "Save draft" button works

1. who and what invokes AI API calls, and why?

```
{
  "name": "ai.result.job_failed",
  "level": "error",
  "context": {
    "jobId": "embed:post:73bc0a59-e3fa-4171-a168-151101bb3e5e",
    "failedReason": "429 You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: <https://platform.openai.com/docs/guides/error-codes/api-errors."
  },
  "dedupeKey": "ai.result.job_failed:embed:post:73bc0a59-e3fa-4171-a168-151101bb3e5e",
  "timestamp": "2026-06-04T01:25:09.976Z"
}

```

Also, there're some gray-areas where I can't fully tell if the fix applied will effect existing functionality, or introduce new issues.

For example: working on Tabby geo related issues, it touches a sensitive business logic.

Others I didn't identify yet. How can we make sure to not introduce new issues while applying the fix?

We need to make sure this never happens again, we could introduce something like, "will fixing this issue introduce new issues, or regress existing ones, or affect existing functionality?"

 let's file these as issues in Linear.

Let's fix them and make sure to not introduce new issues while applying the fix.

---

Pagination in `/creator/courses` doesn't work as expected.

---

🥇 Recommendation: Course/exam atomicity — EXP-278 + EXP-302

The natural next step after the EXP-292 course state-machine (merged #844) you just shipped.

- EXP-278 (High) — handleCourseSubmit missing a "pending" guard → double-submit while under review corrupts approval state
- EXP-302 (High) — exam-reset POST non-atomic → a concurrent student submission in the gap window silently corrupts in-flight exam data

Why now: same domain (courses/exams), identical fix shape (prisma.$transaction + enum-state guards), you have fresh EXP-292 context, unblocked + R3-shippable, ~1–2h, low blast radius (2 handlers). Ships as 1–2 bundled PRs. Note the scanner-fix happy-path (feedback_scanner_fix_happy_path_regression.md) rule applies — pair each new guard with a happy-path test.

🥈 Highest coherence (but design-gated): Storage ledger — EXP-122 + EXP-124 + EXP-127

All three in one file (src/lib/storage/reservation.ts), one root cause → the textbook "pick one, work the nest," one PR closes all three.

- EXP-122 reserve race past quota · EXP-124 double-release → negative ledger · EXP-127 confirm IDOR (no ownership check)

Catch: the auditor flags it as blocked on a locking-strategy decision (optimistic vs. pessimistic vs. atomic counter) tied to the EXP-80 ledger intent. It's the cleanest bundle on the board if you're willing to make that call first — I can scope the decision in ~15 min and then it's a clean single-PR sweep.

🥉 AI subsystem — EXP-252 (+ EXP-319 tail)

- EXP-252 (High) — persistAskAiExchange TOCTOU: soft-deleted conversations still receive messages mid-stream → orphan rows. ~15-min FOR UPDATE fix, independent, security-relevant.
- EXP-319 is partially done (the EMBEDDINGS_ENABLED kill-switch already shipped #838/#839); the remaining cost-control work is bigger and multi-system.

---

⛔ Remaining 5 — each needs a one-line decision from you

1. EXP-305 (Medium, payments) — Tabby geo-block leaves buyers paid-but-not-enrolled. Decide: refund vs void vs support-queue (and: move the webhook geo-check before captureTabbyPayment?). → then I implement.
2. EXP-262 (security) — per-user WebSocket connection cap. Implementation is ready (~15-line INCR→check→rollback in realtime/src/server.ts); just set the cap (max concurrent WS per user, e.g. 10) + behavior on hit (reject newest). → then I ship it.
3. EXP-83 (Low) — VALIDATE the course is_free/price constraint. Blocked until a prod data sweep confirms no {is_free=true, price>0} rows. → operator runs the sweep, then I flip + validate.
4. EXP-283 (Low, devops) — Dependabot digest automation. Decide: update cadence + grouping. → then I wire .github/dependabot.yml.
5. EXP-203 (Low) — narrow the EXP-189 no-restricted-syntax suppressions in 2 embedding services. A design call on the eslint pattern; low value — happy to do it or leave it.

---

commit/push + open the PR, watch for CI, then merge and do post-merge clean-up routine, then next... loop

pre-merge checklist, from the root of the repo, run:

- [ ] all test must pass by running `pnpm experts:test`
- [ ] must run `pnpm experts:check` and `pnpm experts:check:fix` if needed, and verify the fixes are applied correctly.

post-merge checklist, from the root of the repo, after switching back to `main` branch run:

- [ ] `pnpm gitnexus:analyze`
- [ ] `./g --clean` -> this will delete all merged local/remote branches.

etc
---

What's left is the rest of the original "full redesign" you picked (shell + every page) — i.e. applying the kit to the 11 section pages, which still have
their pre-redesign content. From the original decomposition, that's waves 2–4:

Wave 2 — Operations

- Users — DataTable + FilterBar + DetailDrawer, StatusBadge for roles/status
- Certifications — review queue table + approve/reject detail drawer
- Storage — usage table + over-quota states

Wave 3 — Finance

- Payments, Revenue, Refunds, Payouts, Affiliates — each on DataTable/StatCard/SectionCard, with per-section ⌘K domain actions registered into the
palette registry (e.g. "Approve refund…", "Process payout…")

Wave 4 — Insights & Platform

- Analytics/Views, Health, and the Tools pages (Embeddings, processing-fee calculator, noon-webhook test) — page headers + kit treatment

Plus two non-page items:

- Manual in-app verification of what's merged — the one thing I couldn't do headlessly: /admin dashboard + kit-preview + ⌘K in light/dark and ar RTL.
- Optional shell cleanup — your foundation kept the legacy admin-navbar.tsx rendered in admin-shell.tsx alongside the new sidebar+breadcrumb; if you want
the original "single nav" end-state, that navbar could be removed. I left it because you deliberately kept it.

Each section page is small now that the kit + patterns exist (mostly "wire this section's data into DataTable + register its ⌘K actions"), so they go
fast — one PR per section or per wave.

Want me to start Wave 2 (Operations), do a specific section first, or pause here so you can verify the merged foundation in-app?

---

could you spawn

- workflow-orchestrator
- concept-architect
- code-reviewer
- architecture-reviewer
- product-manager
- general purpose explorer

to review this superpowers spec & plan

/home/logix/experts/docs/superpowers/specs/2026-06-10-buyer-price-breakdown-design.md
/home/logix/experts/docs/superpowers/plans/2026-06-10-buyer-price-breakdown.md

and

/home/logix/experts/docs/superpowers/specs/2026-06-10-event-settlement-refunds-design.md
/home/logix/experts/docs/superpowers/reviews/spec-review-v2.md
/home/logix/experts/docs/superpowers/plans/2026-06-10-event-settlement-refunds.md

for these issue #975 and #966

against the codebase, and assess if anything is missing, or if an enhancement can be applied before we proceed with plan execution. I want to make sure it's a solid one-shot production ready implementation plan, and no foot-gun surprises later on.

The execution plan plan will be buyer-price-breakdown -> merge -> event-settlement-refunds, so we need to make sure there are no conflicts/collisions between the two plans.

---

could you spawn

- workflow-orchestrator
- concept-architect
- code-reviewer
- architecture-reviewer
- product-manager
- general purpose explorer

to review this superpowers spec & plan

/home/logix/experts/docs/superpowers/plans/2026-06-10-event-settlement-refunds.md
/home/logix/experts/docs/superpowers/reviews/spec-review-v2.md
/home/logix/experts/docs/superpowers/plans/2026-06-10-event-settlement-refunds.md

for this issue #issue_number

against the codebase, and assess if anything is missing, or if an enhancement can be applied before we proceed with plan execution. I want to make sure it's a solid one-shot production ready implementation plan, and no foot-gun surprises later on.

---

what about webhooks, I feel it will be very usful, the way you mentioned earlier...

---

general-purpose agents must always use sonnet model, not opus model.

---

Let's add a

```
import {Tooltip} from "@heroui/react";
import {InfoIcon} from "lucide-react";
...
  <Tooltip delay={0}>
    <Button variant="secondary"><InfoIcon /></Button>
    <Tooltip.Content>
      <p>briefly explain the mechanism of the MULTI_CURRENCY system, and SAR as the main processing currency</p>
    </Tooltip.Content>
  </Tooltip>

```

where needed.

---

  Your question: rich standalone coupon system vs. the current inline model

  Short answer: they're not really competitors — the rich system is the better long-term model, but the current inline model just solved the hard part (the money), and you should keep that part. Let me break it down.

  Important connection first: the "previous rich system" you describe almost certainly maps to the orphaned Coupon table that's still sitting in your billing schema (prisma/schema.prisma, with redeemedCount etc.). #935 flagged it as a legacy table that was "never re-wired" during the migration — zero write paths
  today. So this isn't "build new vs keep old"; it's "you have both, one is wired and dumb, one is rich and dead."

  Current inline model (couponEnabled/couponCode/couponType/couponValue on Course/Event)

- ✅ One coupon per item, instructor-funded, snapshotted at checkout → redemption + settlement + ZATCA invoice are all correct now (this is the genuinely hard, money-correctness work, and it's done).
- ❌ One code per course/event; can't reuse a coupon across many items; no usage caps, no expiry, no redemption analytics, no shareable link / QR, no campaign concept.

  Rich standalone Coupon model (your previous system)

- ✅ One coupon → many courses/events (campaigns), usage limits + expiry, redemption tracking/analytics, shareable links + QR (a real marketing instrument), can model platform-funded or instructor-funded.
- ❌ Much more surface: checkout must validate a code against a table + scope, redemption-limit concurrency (atomic counter / CAS to stop over-redemption races), funding-source bookkeeping in settlement, stacking/abuse controls, admin governance UI. And it still needs the per-order snapshot for ZATCA — a coupon
  row alone isn't enough.

  Which is "better" depends on what a coupon is for you

- If it's "a creator sets a discount on their one course" → inline is sufficient and simpler.
- If it's "marketing campaigns: shareable codes, time-boxed, multi-course bundles, tracked" → the rich model wins decisively, and the inline model will hit walls almost immediately. The QR/shareable + multi-item features you mention are exactly the things inline can't grow into cleanly.

  My recommendation: a hybrid, not a rewrite

  Don't throw away the wired plumbing. The order-level snapshot (couponCode/listPrice/discountAmount on the enrollment/registration, read by settlement) is the right settlement contract — keep it as-is. Then resurrect the orphaned Coupon table as the authoring/management/distribution layer on top:

- Coupon (rich: scope, limits, expiry, funding source, QR/share token) → at checkout it resolves down to the same inline snapshot fields the settlement engine already consumes.
- A Coupon ↔ content join gives you multi-item reuse.
- This also closes #935's last open item ("delete or repurpose the orphaned table") — you repurpose it.

  That gets you the rich features and keeps ZATCA/settlement correctness, with the money path unchanged.

  The main risks to design for up front: redemption-limit concurrency (you already have CAS/atomic patterns in the settlement code), funding ambiguity (platform vs instructor — decide per coupon), and abuse/stacking (one coupon per order, scope checks).

  ---
  Two things from you:

  1. Role of coupons — creator-level discounts, or platform marketing campaigns? That's the deciding factor for how far to take the rich model.
  2. This small PR — ship the payout-comparison row now (it's useful regardless of which coupon direction you pick), or hold it?

  I can also pull Lucy's record of why the rich system was dropped during the migration before we commit to resurrecting it — want me to?

---

  Sequencing (each its own PR, after #1085)

  1. Unify course → event model: rewrite course-pricing-section.tsx to consume formData/updateField, drop <Controller>/register. Behavior-preserving refactor; verify with existing tests + gate.
  2. Extract the shared CreatorPricingFields (value/onChange + labels bundle + optional maxAttendees slot); both sections become ~30-line wrappers.

  So: Event section wins as the convergence target.

  How do you want to proceed — (a) land #1085 first (comparison columns + shared messages, already green), then do step 1 as a fresh PR; or (b) roll step 1 into this branch now? I still recommend (a) — keep the feature and the refactor in separate, verifiable diffs.

---

found an issue, the cap logic we implemented for coupons applies correctly, but as soon as promotion (affiliate) is enabled, the cap logic is not applied correctly, and instructor might go negative, we need to fix this. tested on `/admin/pricing-calculator`

---

Let's work on the weakest spot in the codebase structurally, the hardest part (at least to me), the curriculum system. It needs so much work, and I'm not sure where to start.
The hardest because we need to synchronize the curriculum content creation with the curriculum content consumption, and we need to make sure the content is created in the correct order, and the correct order is determined by the position of the content in the curriculum. As well as it's the core of the whole platform, and must be done in a way that is scalable and maintainable. That being said, we need to break down the problem into smaller parts, and work on them one by one.

- Identify the gaps in the curriculum system, and fix them.
-

---

 please spawn legal-docs-curator so it checks against most recent 10 PRs against codebase (legal-related) if any changes occurred

---

similar to what we did in `/creator/courses/[id]/coupons` and `/creator/events/[id]/coupons`, we need to add `/creator/courses/[id]/enrollments` and `/creator/events/[id]/registrations` pages so instructors can list registered/enrolled users per course/event, and let's use the same UI/UX pattern as we did for coupons.

let's add a new `/creator/courses/[id]/statistics` and `/creator/events/[id]/statistics` pages so instructors can see the statistics of the course/event, and let's use the same UI/UX pattern as we did for coupons.

the statistics should include:

- total number of registered/enrolled users
- total number of unique users
- total number of unique users who have completed the course/event
- total number of unique users who have not completed the course/event

---


---

let's add a new page to the platform, `/admin/marketing-campaigns`, so admins can create, edit, and manage marketing campaigns, and let's use the same UI/UX pattern as we did for coupons.

---

A user can’t select event spot for multi days events
In other words, instructor can’t track capacity for registered users in multi date events

Also, there might be some cases where the same event spans in two days with different prices, or to state it clearly, a user can attend one day of the event not both.

We will move max attendees below “Schedule Type” section, and we might need to add max spots per added date so the sum matches max attendees input

---

Since we're at it, how can we attach the invoice in the email sent ? and are we actually sending an email to the buyer upon successful purchase ?

---

I need to find every piece of dead code, duplicate logic, unused components, or unnecessary complexity that was added to the project.

---

I want to create a new sub-agent that its sole purpose and responsibility is to find every piece of:

- Stale - dead code
- duplicate logic
- unused components
- unnecessary complexity that was added to the project
- unused packages/dependencies
- safely remove deprecated code

and clean it up, store it here `/home/logix/experts/.claude/agents` and `/home/logix/experts/.codex/agents`

---

Now I have 100 PRs (back to #984). I'll expand the curated legal-material list with the new themes that surfaced — refund flows (#1003), tax/VAT exemption (#1041, #1044), the full multi-currency/FX pricing-disclosure stack, and more private-content/PDPL work — and dispatch legal-docs-curator.

● legal-docs-curator(Legal docs drift audit vs 100 PRs)
Done (40 tool uses · 139.0k tokens · 8m 56s)


The legal-docs-curator completed the drift audit. It grounded all 50 candidate PRs against live code and the (legal) route group (en/ar/es). Here's the bottom line.

Verdict: 6 drift items, 3 needing counsel — most PRs already in-sync

🔴 Priority 1 — Private-content / PDPL gap (counsel needed)

The whole private-content epic (#1055, #1063, #1067, #1071, #1076–1080, #1082) shipped a ContentAccessGrant table that stores userId/createdById as PDPL-covered personal data, with a retention reaper (90d revoked / 30d expired). There's an internal docs/compliance/content-access-grant-retention.md but nothing in the public privacy policy discloses the collection, purpose, or retention window. Proposed: add disclosure to legal.privacy → collect + security in all three locales.

🟠 Priority 2 — Multi-currency refund basis (counsel needed before flag-on)

The FX stack (#1027, #1029, #1013, #1025) charges and refunds non-SAR purchases in SAR at the locked rate, but legal.refundPolicy → processingMethod never says so. Currently inert (NEXT_PUBLIC_MULTI_CURRENCY_ENABLED off) — but must be fixed before that flag flips on.

🟠 Priority 3 — Coupon cap not disclosed

#1089/#1090 added a server-enforced cap (422) preventing instructor coupon discounts from exceeding their revenue split. Instructors get blocked with no policy explaining why. Add to promotionsCouponPolicy → instructorIssued + instructorRevenuePolicy → discounts.

🟡 Priority 4–6 — Yellow

- #1123 invoice-PDF email — covered by broad privacy language, optional sentence in privacy → use.
- #1143 quizzes — clarify they fall under structuralIntegrity post-publication rules.
- #1041 ZATCA "out-of-scope" posture — the PR body's own open counsel flag is still unresolved.

✅ Verified in-sync / not material

- #1044 (VAT-exempt revenue split) — confirmed landed correctly in all three locales, consistent with #1041.
- #1003 event refunds (7-day-from-registration window) — docs accurate, no stale "48-hour" copy anywhere.
- Affiliate (#1141/#1144/#1142/#1114), auth (#1104/#1107/#1108/#1117), PII-logging (#1135/#1138/#1126), most coupon/ZATCA-format PRs — code matches policy or is internal-only.

Locale parity

Structurally parallel across en/ar/es. One pre-existing bug: ar/legal.json privacy changes.title = "8. Changes to This Policy" (untranslated English heading).

---
Nothing was written or committed — this was audit-only. Want me to:
1. Have the curator apply the doc edits for the 3 non-counsel-blocked items (coupon cap, quiz clarification, invoice-email sentence + fix the Arabic heading), or
2. File GitHub issues (via experts-beacon) for the 3 counsel-gated items so they're tracked, or
3. Both?

---

I want to add a bypass logic for the subscription system so that admins can bypass the subscription system and create a subscription for a user directly.
As well as a bypass logic for the subscription system so admins can be assigned to a plan without payment, as payment will create a misleading subscription record.

---

Where materialized views would win — but with caveats
- Only the genuinely expensive + only-needs-daily-freshness metrics: cohort retention (cohorts × activity across many periods), long-range DAU/MAU, and day-by-day MRR/ARR time-series.

---

I want to create a new chart components system, for example, a price must always show as <SaudiRiyal /> 12,012.00
currently it might show 12012.12345555555 no symbol not formatted, same for numbers/percentages must be formatted correctly, as well as hover card styles.

we might take it from `/creator/dashboard` and/or `/creator/analytics` and globalize them then re-use them in admin charts, so we have a consistent style and one source-of-truth.

---

I want to clean up the skills system, it's a mess, and we need to make it more robust and scalable, and easier to maintain. And rid of unused ones.

---

In experts, we have two separate systems that named the same (certifications) which's confusing in development and for the end-user

can you suggest a way to fix that

I’d split the concepts by ownership:

**Recommended Vocabulary**
- Platform-granted status: **Instructor Verification**
  Current code: `src/lib/certifications`, `InstructorCertificationProfile`, `CertificationApplication`, `/certifications`
- User-entered external proof: **Credentials**
  Current code: `Portfolio.certifications`
- Learner/course completion documents: **Certificates**
  Already mostly named that way in dashboard/creator copy.

That gives users a clearer mental model: “Credentials” are what an instructor submits; “Instructor Verification” is what Experts grants; “Certificates” are documents issued to learners.

**Best Fix Path**
1. Rename product copy first:
   - `/certifications` page title: “Instructor Verification”
   - admin queue: “Verification Queue”
   - profile/portfolio section: “Credentials”
   - keep “Certificates” only for learner-issued course certificates.

2. Rename routes with redirects:
   - New: `/instructor-verification`
   - New: `/admin/instructor-verification`
   - Keep `/certifications` and `/admin/certifications` as redirects for existing links.
   - Keep `/api/v1/certifications` initially, but introduce `/api/v1/instructor-verification` as the preferred API path.

3. Rename portfolio data surface:
   - `Portfolio.certifications Json?` should become `credentials` in Prisma/client DTOs, ideally with `@map("certifications")` first to avoid a risky DB migration.
   - Existing external API responses can temporarily include both:
     - `credentials`
     - deprecated `certifications`

4. Rename platform domain more carefully:
   - `src/lib/certifications` → `src/lib/instructor-verification`
   - `CertificationApplication` → `InstructorVerificationApplication`
   - `CertificationProfileDTO` → `InstructorVerificationProfileDTO`
   - `CertificationType` → maybe `VerificationLevel` with values `VERIFIED`, `ACADEMIC`.

I would not rename the database tables immediately. The platform certification system touches Prisma models, admin queues, public profile badges, course publishing gates, and notifications, so the blast radius is high. Safer approach: rename UI/routes/DTOs first, preserve DB `@@map(...)`, then do table-level migration later only if it still matters.

The key files showing the split are:
- Platform verification domain: [/home/logix/.codex/worktrees/b280/experts/apps/experts-app/src/lib/certifications](/home/logix/.codex/worktrees/b280/experts/apps/experts-app/src/lib/certifications)
- Portfolio field: [/home/logix/.codex/worktrees/b280/experts/apps/experts-app/prisma/schema.prisma:216](/home/logix/.codex/worktrees/b280/experts/apps/experts-app/prisma/schema.prisma:216)
- Instructor certification models: [/home/logix/.codex/worktrees/b280/experts/apps/experts-app/prisma/schema.prisma:2312](/home/logix/.codex/worktrees/b280/experts/apps/experts-app/prisma/schema.prisma:2312)

---

A course/event you recently created in Experts got rejected by the system and flagged as "spam", for the following reasons:

REASON_1
REASON_2
REASON_3

Please work on fixing it, and submit a new review request.

Best Regards,
Experts Moderators Team

---

Issue started here:

A user can’t select event spot for multi days events
In other words, instructor can’t track capacity for registered users in multi date events

Also, there might be some cases where the same event spans in two days with different prices, or to state it clearly, a user can attend one day of the event not both.

Then we moved to consumer logic:

We were working on the consumer logic, now let's move to the creator and fix some wrong/missing implementations:
- I want to add a title/note for specific day of multi-day event, e.g., "Lecture Only" - data/time - lower price - spots, "Lecture + Workshop" - data/time - higher price - spots.
- for above, we might also need a conditional "Full event pass", not sure how we might do that, for example, the event might be individual dates only, or as current full pass + per day.
- isDirty isn't enforced/checked for when new fields (per day price, per day spots) change, we need to fix that.

Creator multi-day tickets
Per-day label

New optional event_occurrences.title (migration 20260626120000_event_occurrence_title).
Each multi-day row has a Day label field (e.g. “Lecture only”, “Lecture + workshop”).
Consumer ticket picker shows the label as the headline and the date/time underneath when a label is set.
Full event pass

Toggle moved to the Schedule section (multi-day only): off = day tickets only; on = full pass (price still in Pricing).
Schedule save now sends fullEventPassEnabled and maxAttendees with the rest of the schedule payload.
Dirty state & schedule save

isScheduleDirty now compares title, day price, day cap, max attendees, and full event pass, not just dates/times.
buildScheduleUpdatePayload was missing per-day price/cap/title and VAT conversion; it now uses the same mapping as the main save (taxExempt from the edit page).
Files to know
Form/UI: event-schedule-section.tsx, use-event-form.ts, event.mapper.ts
API/DB: schedule.ts, create/update handlers, event.dto.ts, Prisma schema + migration
Buyer UI: event-ticket-picker.tsx
i18n: en / ar / es creator.json
Run the migration in your environment:

cd apps/experts-app && pnpm prisma migrate deploy
Note: Saving schedule still replaces occurrences server-side (existing behavior), so occurrence IDs can change until we add stable IDs on partial save; labels/prices/caps will persist correctly after save.

---

Back to events in creator

You did a great job with recent implementation. However, it still doesn't solve my issue.
We might want to make as flexible as possible, maybe nested clusters will do.

The issue we have now is sort of conditional:

Cluster 1:
Lecture + Workshop two days 28-29 Aug, 2026 with 1449SAR as listed price

While Cluster 2:
Lecture Only: first day only 28 Aug, 2026 with 750SAR as listed price

It's not possible to that now.

How can we solve this without complicating thing any further ?


---

The gap isn’t the schedule UI — it’s the ticket model. Right now buyers only get two shapes:

What you want	What exists today
“Lecture + Workshop” — 28–29 Aug, 1449 SAR
Full event pass — event.price, generic label, always all days
“Lecture Only” — 28 Aug only, 750 SAR
One option per occurrence — occurrence.title + occurrence.price
Day 2 not sold alone, but in the bundle
Not supported — every occurrence is its own radio
Bundle label + price independent of “full pass”
Full pass title is fixed copy; price is only event.price
So your example is not achievable cleanly with full pass + per-day rows alone.

Minimal fix that actually fits: ticket offers (your “clusters”)
Keep schedule = calendar (when). Add ticket offers = what you sell (title, price, which days).

Schedule (unchanged)
  • Aug 28 — Lecture block (time)
  • Aug 29 — Workshop block (time)
Ticket offers (new)
  Cluster A: "Lecture + Workshop" | 1449 SAR | includes [Aug 28, Aug 29]
  Cluster B: "Lecture Only"       |  750 SAR | includes [Aug 28]
Buyer UI: one radio per offer, not per occurrence (unless you auto-generate offers from days).

Registration: extend scope beyond full / occurrenceId:

ticketScopeKey = offer id (already varchar, fits)
ticketType = e.g. ticket_offer (or reuse full_event / single_occurrence only where 1:1)
Price from offer.price, not event.price / sum of days
Capacity: per offer and/or per occurrence (bundle sold out when any included day is full — same idea as today’s full pass).

Creator UI: nested under multi-day schedule — “Ticket options” with title, price (VAT-inclusive authoring like today), multi-select of schedule days, optional cap. Drop or hide full event pass when at least one offer exists (offers replace pass + per-day radios).

This is one concept (“sellable products”), not nested schedule + pricing + full pass + per-day price all fighting each other.

Smaller MVP (only if bundle = every scheduled day)
If you will never sell a subset bundle (always all days) and only need to hide day 2 alone:

event.price = 1449, optional fullPassTitle = “Lecture + Workshop”
Day 1: title “Lecture Only”, day price 750
sellSeparately: false on day 2 → hidden from picker, still in full pass
That’s a small schema + picker filter. It does not generalize to 3 days with a 2-day bundle, different bundles, or workshop-only later.

Recommendation
For “Lecture + Workshop” vs “Lecture Only” (and similar), implement ticket offers and treat full pass + per-day price as legacy or auto-migrated defaults. Phase 1: offers only on scheduleType === multiple, no arbitrary nesting — flat list of offers, each links to one or more occurrences.

If you want to proceed in the repo, a sensible slice is:

Prisma EventTicketOffer + EventTicketOfferOccurrence (or occurrenceIds array)
Creator form cluster UI + save on event update
DTO + ticket picker driven by offers
Register/checkout/capacity keyed by ticketScopeKey = offer id
Say if you want that MVP in code next, or only the sellSeparately + fullPassTitle stopgap for the two-day case.

went with MVP, now here we are...

It left some sort of a mess, and glitchy behavior, we need to fix it and make it more robust and scalable, and easier to maintain. As well as rid of unused code and components. Along with enhancing the UI/UX. The agent I was working with did a poor job maintaining a clean codebase, and frontend styling consistency, which made things harder to maintain and understand.

---

I want to create a replica of the front-end event preview section in creator create/edit event page, so a creator can review what the user will see when they enroll in the event. With live changes, and blurred for content (inputs/buttons/etc.) that's not related.

---

How can we enhance "Time Slots" section inputs, as I feel it's messy.

---

I think we need to apply the same changes made for multi-date event to recurring event, right ?

---

We might want to set a very clear isDirty boundry between
main Save Changes and scoped ones, because sometimes when
changes made in schedule section it triggeres both save
changes, but main save changes doesn't actually save
changes. Also, we have placement issue, when adding multi
dates, it becomes hard to see the inputs to save those
changes, we might want to add light auto-save after
sometime and a clear indicator that shows there're unsaved
changes even when buttons are invisible

---

I don't like the Quick Actions section in creator events/courses view pages, it's not useful and it's not clear what it does.


---

let's add a cool down period for publish/unpublish course/event. As I don't like how a creator can publish/unpublish course/event anytime, that might lead to abuse by some creators.

---

Price                         750.00
Coupon “G10”        (10% off) -75.00
Total                         675.00

VAT included                   88.04

Price excl. VAT               652.17
Coupon excl. VAT              -65.21
Taxable amount after discount 586.96
VAT 15%                        88.04
Total incl. VAT               675.00

---

Given creators currently can't unpublish at all, what should the cooldown govern?

  1. Enable unpublish, cooldown-gated
     Let creators unpublish (published→draft) and republish, but lock any further publish-state change for the cooldown window. Replaces today's hard 403 — adds a genuinely useful capability (pull down to fix) while preventing yo-yo abuse. Admins bypass.
  2. Keep unpublish blocked; gate publish
     Leave the 403 on creator unpublish as-is. Add a cooldown only on the publish/archive transitions a creator can make. Narrow effect today (no creator loop exists), but a forward guard.
  3. Cooldown both + allow republish from archive
     Same as the first option, plus let creators republish an archived item (currently irreversible), all under one publish-state cooldown. Largest behavior change.
  4. Type something.

  ←  ☐ Model  ☐ Duration  ✔ Submit  →

How long should the publish-state cooldown be?

❯ 1. 7 days
     Mirrors the existing published-price cooldown (PRICE_CHANGE_COOLDOWN_DAYS = 7) for consistency.
  2. 14 days
     Two weeks — a stronger throttle on publish-state churn.
  3. 30 days
     One month — strongest; treats publish-state as a high-commitment action.
  4. Type something.

---

Plan written. Two things I want explicit on approval, since they bend your literal asks slightly:

1. "One cooldown" → one framework, three per-lever timers (not a single shared column) — so a price tweak doesn't freeze a typo fix and the recently-shipped per-field event price locks aren't regressed. The duration/policy/UX/error vocabulary are unified.
2. Admin normalization is full for structural edits, but publish-state stays admin-exempt — because an admin's publish/unpublish is a moderation takedown (stamps adminLockedAt) and shouldn't be rate-limited. That's the "admins control it elsewhere" you wanted.
3. Two PRs (publish-state + admin-normalization + docs first; structural-edit cooldown second) to isolate the higher-risk curriculum surface — landing one coherent model.

If any of those three should flip, tell me and I'll adjust the plan. Otherwise:

● User approved Claude's plan
Plan saved to: ~/.claude/plans/zippy-moseying-ritchie.md · /plan to edit
Unified significant-change cooldown (courses + events)

Context

The client is unhappy with how rigid the platform is after a creator publishes. Two
restrictions are the pain points (the exact copy they flagged):
- Course post-publish structural lock — once published, modules/lessons/quiz rules are
permanently locked (canEditStructure = draft-only), surfaced in the publish dialog
locked0..8 (creator.json) and legal §3 Structural Integrity (legal.json).
- Publish-state rigidity — creators cannot unpublish at all (hard 403 on
published→draft for courses; events caught by the edit-lock), and archive is irreversible.

The goal is to loosen these into a single, consistent 7-day cooldown model — creators
get flexibility, integrity is preserved via rate-limiting (not permanent locks). The proven
template is the existing price cooldown (pricingLockedUntil + PRICE_CHANGE_COOLDOWN_DAYS=7).

Owner decisions (this session):
1. Unify all major changes under one cooldown concept (publish-state + structural + price).
2. Admins treated as normal creators for these lifecycle gates — remove the isAdmin
bypass from publish/unpublish/archive/structural permission checks. Admins keep control
elsewhere (moderation takedown adminLockedAt, approval workflow, admin console).
3. Unpublish always allowed — no paid-enrollment/registration block; it only hides the item
from new buyers, existing learners/ticket-holders keep access. Cooldown alone throttles
yo-yo abuse. Duration = 7 days (one constant, aligned with price).

Recommended approach

One cooldown FRAMEWORK, per-lever lock fields (not a single shared column). One duration,
one policy module, one error/i18n family, one UX pattern — three levers, one mental model.

▎ Deviation note: a literal single shared column was rejected because it (a) would regress the
▎ intricate per-field event price locks (each EventOccurrence/EventTicketOffer has its
▎ own pricingLockedUntil), and (b) would cross-block unrelated levers (a price tweak freezing
▎ a typo fix) — the opposite of "loosen." The existing price cooldown stays exactly as
▎ shipped, only re-branded into the same vocabulary.

Admin interaction (the one place the 3 decisions meet):
- Structural cooldown applies to admins too (replaces their removed bypass).
- Publish-state cooldown is non-admin only — an admin's publish/unpublish is a
moderation takedown/lift (stamps/clears adminLockedAt) and must never be throttled. This is
exactly the "admins control it elsewhere" the owner asked for.

Schema (Prisma drift-guard discipline: hand-edit model block, never prisma format)

- Course (~`prisma/schema.prisma:394): lastStructureChangeAt, structureLockedUntil, lastPublishStateChangeAt, publishStateLockedUntil— allDateTime? @db.Timestamptz(6)`.
- Event (~`:954): lastPublishStateChangeAt, publishStateLockedUntil`.
- No new indexes (PK lookups). Migration: migrate diff --from-migrations … --to-schema … --script
→ hand-write ADD COLUMN IF NOT EXISTS → pnpm db:generate → pnpm db:check:drift (gate).
- No backfill — existing published items get NULL locks → immediately editable on deploy.
That is the intended loosening (matches how the price columns shipped).

New shared policy module

src/lib/lifecycle/significant-change-policy.ts — exports:
SIGNIFICANT_CHANGE_COOLDOWN_DAYS = PRICE_CHANGE_COOLDOWN_DAYS (imported so they can't drift),
isSignificantChangeLocked(lockedUntil, now), armSignificantChangeLock(now),
getPublishStateCooldownError/getStructureCooldownError (mirror getPricingCooldownError,
reuse addDays/formatPricingLockDate from published-price-policy.ts).

Remove isAdmin (lifecycle gates only — KEEP moderation/approval)

REMOVE: lifecycle.policy.ts isAdmin branches in canPublish/canArchive/canEditStructure/
canEditContent; course-edit.guard.ts isAdmin bypass in assertCourseStructureEditable
(L64-66) + assertCourseContentEditable (L93-95); the three non-admin unpublish 403s
(course-update.handler.ts:108-110, course-publish.handler.ts:112-114,
event-update.handler.ts:125-127).
KEEP (do not touch): everything adminLockedAt/isCourseAdminLocked/isEventAdminLocked +
resolveAdminLockMutation; restricted-status !isAdmin (submitted/approved/rejected); approval
bypass / canHostPublishContent; the admin archive-lift OR-clauses; assertCourseLimit (tier
limit, flagged as out-of-scope).

Handler edits

- course-update.handler.ts / course-publish.handler.ts / course-archive.handler.ts /
event-update.handler.ts: drop the unpublish 403s + {isAdmin} args; add a non-admin
publish-state cooldown gate beside the existing price gate; arm
publishStateLockedUntil/lastPublishStateChangeAt on a publish-state transition. Price
blocks untouched.
- course-edit.guard.ts: structural gate returns 409 getStructureCooldownError when
structureLockedUntil is in the future, else allow (draft OR published-unlocked). Add
armStructureLockIfPublished(courseId, tx?) called by the ~16 curriculum handlers
(modules/lessons/quizzes/exams/assets) on success — only arms when published; drafts edit free.

Structural-edit integrity (loosen, but don't break mid-cohort)

- Broad structural edits become cooldown-gated (once / 7 days) instead of permanently locked.
- Hard-guard the dangerous subset independent of the cooldown: in course-quiz-update/
course-exam-update handlers, when published AND attempts exist, reject edits to
scoring-affecting fields (passingScore, maxAttempts, question set, per-question points)
with a dedicated 409 QUIZ_SCORING_LOCKED.
- lastStructureChangeAt seeds a future learner "content updated" signal (surfacing deferred).

UI (reuse the price-lock UX)

ldown framing ("major changes follow
a 7-day cooldown; one at a time"); keep the quiz-scoring-with-attempts case as the one truly
blocked edit. One-line note added to event-publish-dialog-body.tsx.

i18n + legal (en / ar / es parity)

- New creator.json keys: structureCooldownNotice, publishStateCooldownNotice,
unpublishCooldownTooltip, quizScoringLocked; reword unpublishTooltip; rewrite
publishDialog.locked*/summary.
- Rewrite legal.json coursePublishingPolicy §3 structuralIntegrity (permanent → 7-day
cooldown + scoring protection), §4 pricing (price as one lever of the unified model),
§5 updatesVersioning (unpublish-always-allowed + learners-keep-access). Page component
(PUBLISHING_SECTION_KEYS) needs no change — it's data-driven.
mallest blast radius; leaves the
per-field price system and the 16 curriculum handlers untouched.
- PR 2 — structural-edit cooldown: course-edit.guard.ts gate + armStructureLockIfPublished
wired into the ~16 handlers + quiz/exam scoring guard + curriculum-page note + i18n + tests.
Highest-risk surface (learner integrity, 16 enforcement points) isolated after PR 1 bakes.
- Deferred (flagged, not dropped): learner "content updated" signal; i18n-izing the
hardcoded price/cooldown error strings; a publish-state/structure version-audit table (columns
seed it now); re-verify the event ticket-holder access path doesn't gate on
publishingStatus==="published" (courses confirmed safe via paid-course-enrollment.guard.ts).

Verification

s; course-update /
course-publish / course-archive / event-update handler tests (drop unpublish-blocked
asserts; add publish-state cooldown: non-admin armed→409, admin exempt, clears after 7d);
published-price-policy.test.ts (price regression); quiz/exam scoring-guard + cooldown-notice
component tests (node-env renderToStaticMarkup + string asserts); en/ar/es i18n parity.
- Late repo-wide gate: pnpm experts:check.

Critical files

- apps/experts-app/prisma/schema.prisma (Course ~394, Event ~954)
- apps/experts-app/src/lib/lifecycle/significant-change-policy.ts (new)
- apps/experts-app/src/lib/lifecycle/lifecycle.policy.ts
- apps/experts-app/src/lib/courses/catalog/guards/course-edit.guard.ts
- apps/experts-app/src/lib/courses/catalog/handlers/course-update.handler.ts (+ course-publish/course-archive)
- apps/experts-app/src/lib/events/handlers/event-update.handler.ts
- apps/experts-app/src/components/creator/course-publish-dialog-body.tsx + new cooldown-notice.tsx
- apps/experts-app/src/i18n/messages/{en,ar,es}/creator.json + legal.json

---


Option A — Wrap it up now (my recommendation). We're at "happy" for the system. I'd:
1. Reflect the final palette into DESIGN.md + PRODUCT.md (their colors: values are now stale), and
2. Checkpoint-commit the whole pass on this isolated branch (running pnpm experts:check first).

That closes the loop exactly as you planned and banks the work safely.

Option B — Extend to the components first, then wrap. The one thing still fighting the clean system is the hardcoded hero (purple/amber per slide) and the amber/green difficulty badges — the token redesign is invisible where those bypass it. Conforming them to the single blue is the highest-visible-impact enhancement left. It's more surface area and it's exactly where we diverged last time, so I'd show each change. Then do the DESIGN.md/PRODUCT.md reflection + commit.

Either way I'd lock the token work with a commit — the only question is whether we conform the hero/badges before or after. Given you asked about moving on, I lean A now, B as a separate follow-up whenever you want the page to fully match the system. Which way do you want to go?

---

Yeah, fair. The universe idea is interesting, but it can easily drift into “cool background” instead of a hero that clearly sells **Experts**.

Here are stronger alternative directions we could try.

## 1. The “Living Learning Map”

Instead of space, make the hero an interactive **map of a learner’s growth journey**.

Visual idea: a beautiful 3D/topographic map where courses, coaching, events, community, and certificates are destinations. The user scrolls through a journey: Discover → Learn → Connect → Grow → Become an Expert.

Interaction:

* Mouse movement tilts the map.
* Scroll moves along the learning path.
* Hovering a destination expands a liquid-glass card.
* Learner particles travel along routes.
* The CTA feels like “start your journey.”

Why it might work: it is still cinematic, but more directly tied to education and progress than space.

Risk: could look like a travel app unless executed carefully.

---

## 2. The “Knowledge City”

Experts becomes a premium digital city of learning.

Visual idea: a futuristic city/isometric campus. Each district represents a platform area:

* Courses district
* Coaching tower
* Events arena
* Community plaza
* Expert studios
* Certificates vault

Interaction:

* Scroll zooms through the city.
* Mouse movement creates depth/parallax.
* Buildings light up as stages activate.
* Cards appear as glass panels above districts.

Why it might work: it gives Experts a strong “platform ecosystem” identity. It feels bigger than an LMS.

Risk: can become too illustrative or game-like if overdone.

---

## 3. The “Liquid Knowledge Lens”

This is more abstract and premium.

Visual idea: a huge liquid-glass lens/orb in the center-right. Inside it, the platform world refracts: courses, experts, sessions, community threads, progress. The lens bends light, reacts to mouse movement, and reveals different parts of the ecosystem as the user scrolls.

Interaction:

* Cursor moves the refraction/highlight.
* Scroll rotates the lens through Discover → Connect → Grow.
* Cards appear inside/behind the lens.
* Dragging the lens slightly changes what is revealed.

Why it might work: it gives us the “liquid glass” identity without relying on dashboards or space.

Risk: harder to implement convincingly. Bad execution may look like a blob.

---

## 4. The “Expert Signal”

Experts as a network broadcasting knowledge.

Visual idea: a central “signal core” sends elegant waves outward. Courses, experts, coaching, community, and events receive/respond to the signal. It feels like a premium command system, but not a dashboard.

Interaction:

* Mouse creates ripple waves.
* Scroll expands the signal radius.
* Cards appear where signals intersect.
* Community/activity pulses respond like live network traffic.

Why it might work: modern, clean, interactive, and strongly connected to “Experts spreading knowledge.”

Risk: may become too abstract unless product cards are well integrated.

---

## 5. The “Infinite Course Canvas”

Think Figma/Miro-style, but premium and educational.

Visual idea: the hero shows a large zoomable canvas of learning objects: course modules, expert profiles, live sessions, discussions, certificates, events. The user is looking at a living knowledge workspace.

Interaction:

* Mouse/drag pans the canvas slightly.
* Scroll zooms deeper into the canvas.
* Cards connect and rearrange.
* Hovering shows liquid-glass previews.

Why it might work: very product-relevant. It feels like users are already inside Experts.

Risk: could look like a productivity tool rather than a learning platform.

---

## 6. The “Digital Majlis of Experts”

Not literal traditional imagery, but inspired by the concept of gathering around knowledge.

Visual idea: a premium circular gathering space with expert nodes around a center. Courses, live coaching, discussions, and events appear as knowledge objects shared between people.

Interaction:

* Scroll brings more participants/nodes into the circle.
* Mouse movement creates depth.
* Hovering experts reveals their sessions/courses.
* Community threads appear as floating conversation cards.

Why it might work: culturally relevant without obvious clichés. It communicates learning as social, human, and expert-led.

Risk: needs tasteful execution. Too literal could feel cheesy.

---

## 7. The “Growth Engine”

Experts as a machine/system that turns knowledge into outcomes.

Visual idea: a beautiful futuristic engine made of glass rings, progress arcs, learning modules, expert nodes, and certification outputs. The platform feels powerful and systematic.

Interaction:

* Scroll activates the engine.
* Rings rotate slowly.
* Knowledge streams move through modules.
* Progress/certificates appear at the end.
* Mouse changes lighting and depth.

Why it might work: strong visual metaphor for transformation and ROI.

Risk: could feel too mechanical, less human/social.

---

## 8. The “Editorial Magazine Hero”

Less animated, more luxurious.

Visual idea: a bold, high-end editorial layout with huge typography, layered glass cards, expert portraits/avatars, event snippets, and course previews. More like Apple/Stripe quality than particle effects.

Interaction:

* Scroll reveals sections in elegant layers.
* Cards slide with depth.
* Mouse creates subtle spotlight and glass reflections.
* Content feels premium and readable.

Why it might work: safest path to a polished premium result. Stronger for business credibility.

Risk: less “fun” than the interactive universe/canvas ideas.

---

## My top 3 for Experts

I’d test these three:

### 1. **Living Learning Map**

Best balance between educational meaning, interactivity, and visual uniqueness.

### 2. **Liquid Knowledge Lens**

Best for creating a signature “wow” visual with liquid glass.

### 3. **Knowledge City**

Best for showing Experts as a full ecosystem, not just courses.

Personally, I’d move away from pure space. The space concept is cool, but it can feel detached from the product. A **Living Learning Map** or **Liquid Knowledge Lens** would probably feel more ownable to Experts.

A strong new direction prompt could be:

```md
Stop pursuing the space/universe version for now.

Explore 3 alternative hero concepts for Experts:

1. Living Learning Map
2. Liquid Knowledge Lens
3. Knowledge City

Each concept must include:
- Visual metaphor
- How it represents courses, coaching, events, community, experts, and progress
- Mouse interaction
- Scroll interaction
- Mobile behavior
- Risks
- Why it is better than the current cosmic hero

Do not implement yet.

Produce concept descriptions first, then recommend the strongest one for implementation.
```

My vote: **Living Learning Map**. It can be cinematic, interactive, and directly meaningful: Experts is the place where a learner’s journey becomes visible.

---

Now I can describe the problem precisely. You're right, and the root cause is one mega-section: the "Schedule" accordion item is a 1,587-line component that actually contains five different concerns, in this order:

1. Schedule type (single / multiple / recurring)
2. Max Attendees — capacity, sitting before any dates
3. Dates & times — interleaved with pricing mode, full-event pass, per-day price/seats cards, and ticket options
4. Timezone — separated from the date/time inputs by the entire tickets block
5. Location — type, meeting URL, address + Google Maps autocomplete, buried at the very bottom

Meanwhile a separate "Pricing" accordion holds free/paid + base price + affiliate. So three concerns are split across distant places: pricing (base price in Pricing; day prices, ticket options, full pass in Schedule), capacity (Max Attendees at the top; per-day Seats and offer Seats far below), and location (no home of its own at all). A creator setting up an in-person event scrolls through the whole ticketing apparatus to find the address field.

How I'd enhance it, in three independent steps ordered by value-per-risk:

1. Give Location its own accordion section (cheap, biggest win). Extract the location type / meeting URL / address+maps block into EventLocationSection as a sibling accordion item ("Location" with a map-pin icon, matching the existing section pattern). This also pulls ~400 lines of Maps plumbing out of the schedule component — a pure structural move with near-zero behavior risk. Section order becomes: General → Schedule → Location → Pricing → Hosts → Agenda → Extras.

2. Regroup inside Schedule so it reads top-to-bottom as one story: schedule type → dates/times → timezone immediately after the time inputs (it modifies them, it shouldn't live 400 lines away) → then a clearly-labeled "Tickets & capacity" block containing Max Attendees, the pricing-mode toggle, day cards, and ticket options. Max Attendees moving down next to the other capacity fields ends the capacity split — the three-layer capacity model we just built (#1272) finally sits in one visual group with its tooltips.

3. (Optional, later) Rename and re-anchor the pricing split rather than fight it. Day prices and offer prices genuinely belong next to the days they price — moving them into the Pricing accordion would trade one scattering for another. Instead: rename the section trigger to "Schedule & tickets", and add a one-line cross-link in the Pricing section for multi-day events ("Per-day and ticket-option prices are set in Schedule & tickets ↓") so a creator hunting for prices in Pricing gets routed instead of lost. Half of this note already exists (multiDayBasePriceNote); it just doesn't navigate.

A step further, if you want a real redesign: keep the accordion for editing, but make creation a stepper (General → Schedule → Location → Tickets → Review) reusing these same section components. That's a bigger lift and I'd only do it after 1–2 prove out.

Want me to file this as an issue (with the phased breakdown), or go ahead and implement step 1 — or 1+2 — as the next slice? I'd also happily run the ui-designer agent over the form first if you want a fuller design pass beyond the structural fix.

---


┌─────┬──────────────────────────────────────────────────┬─────────┬────────┬───────────────────────────────────────────────────────────────────────────┐
│  #  │                      Issue                       │   Sev   │ Effort │                                    Why                                    │
├─────┼──────────────────────────────────────────────────┼─────────┼────────┼───────────────────────────────────────────────────────────────────────────┤
│ 1   │ #1285 oversellable seats                         │ 🔴 Crit │ M      │ Revenue integrity; events momentum; atomic-tx fix                         │
├─────┼──────────────────────────────────────────────────┼─────────┼────────┼───────────────────────────────────────────────────────────────────────────┤
│ 2   │ #1284 OTP: no rate-limit + ownership gate        │ 🟠 High │ S/M    │ Brute-force 6-digit OTP; reuses getClientIp/enforceSlidingWindowRateLimit │
├─────┼──────────────────────────────────────────────────┼─────────┼────────┼───────────────────────────────────────────────────────────────────────────┤
│ 3   │ #1283 Stored XSS in course resource URLs         │ 🟠 High │ S/M    │ javascript:/data: URIs; mirror existing videoUrl ^https?:// guard         │
├─────┼──────────────────────────────────────────────────┼─────────┼────────┼───────────────────────────────────────────────────────────────────────────┤
│ 4   │ #1298 Credit-note sequence desync breaks refunds │ 🟠 High │ M      │ Port invoice self-heal (GREATEST/MAX + P2002 retry) to credit path        │
├─────┼──────────────────────────────────────────────────┼─────────┼────────┼───────────────────────────────────────────────────────────────────────────┤
│ 5   │ #1303 N+1 on course/event-detail hot paths       │ 🟡 Med  │ M      │ Batch per-instructor/per-occurrence queries                               │
└─────┴──────────────────────────────────────────────────┴─────────┴────────┴───────────────────────────────────────────────────────────────────────────┘

---

All six are real and well-scoped. Here's my read of the board and a clear recommendation.

Recommendation: #1282 + #1283 — the z.url() stored-XSS cluster

These are the best next issue because they're High severity, high-confidence-real, cleanly bounded, and a natural 2-for-1 sweep — and I already have the exact remediation playbook in memory (z.url() validates structure, not scheme, so javascript:/data: pass → XSS; restrict ^https?:// at the schema and at render).

- #1282 — applicant plants javascript: in a certification URL → fires in the admin review queue's authenticated session. Admin-session takeover is the scariest reach on the board.
- #1283 — instructor plants it in a lesson/quiz/exam resource URL → fires for every enrolled student.
- Same root cause, same fix (a shared safe-URL schema + defensive render guard), likely other bare z.url() sites to sweep in the same diff. One PR closes two Highs.

The rest, ranked

┌─────────────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────┐
│                              Issue                              │                                           Why it's strong                                           │                                        Why not #1                                        │
├─────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│ #1298 credit-note seq desync (High, money)                      │ I have the handleInvoiceCreate self-heal pattern to mirror (project_invoice_number_sequence_desync) │ Single issue; needs the reconcile+P2002-retry ported carefully                           │
├─────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│ #1297 webhook Number(amount ?? 0) zeroes earnings (High, money) │ Real financial-integrity hole, no alarm                                                             │ Fix is partly policy (fail-loud vs reconcile) — worth a design call                      │
├─────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│ #1281 Tabby body/HMAC decoupling (High, security)               │ Genuine signature-bypass; ties to my recent #1296 webhook work                                      │ Noon protocol needs the Bearer substitution — fix must be provider-scoped, more delicate │
├─────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│ #1300 unescaped Prisma.raw IN()                                 │ Defense-in-depth                                                                                    │ Author flags it Medium / not exploitable today                                           │
└─────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────┘

There's also a tight multi-day event-ticketing bug cluster (#1286–#1293) in an area I know well (#1202/#1311) if you'd prefer a themed sweep over security.

Want me to take #1282 + #1283 end-to-end (worktree → shared safe-URL schema + render guard → sweep other bare z.url() → gate → PR), same autonomous flow as the last two? Or point me at a different one.

---

Shipped. 🎉

PR #1317 — multi-day event-ticketing hardening

- Committed 3c3ae7274 (lint-staged pre-commit passed), pushed fix/multiday-event-ticketing-hardening (pre-push experts:check green), PR opened against main with all 7 Closes keywords in the body (auto-close on merge).
- CI: Migration Drift ✅, Migration Immutability ✅, Detect Changes ✅, guard ✅ — only Verify still running (the format/lint/typecheck/test job; it'll match the local green run).

What landed (7 issues, one cohesive PR)

- #1287 High — day-removal 409 (was raw FK-500), race-safe inside the tx under the advisory lock
- #1290 High — refund eligibility scoped to purchased days; request & process handlers now provably agree
- #1289 Med — free→paid 0-price guard decoupled from the schedule branch (API bypass closed)
- #1291 Med — clone copies fullEventPassEnabled + offers + day links
- #1292 Med — private-event guard honors mid-checkout pending (course parity)
- #1286 High — slot delete prunes offer day membership (no silent drop)
- #1288 Med — reachable "clear ticket options" escape hatch (en/ar/es)

#1293 was left out (course-curriculum, not event-ticketing) — say the word and I'll take it next.

Verification: 390 events tests pass + new event-refund-scope suite and regression cases; three review agents (security clean, code-reviewer/qa-tester's one MEDIUM TOCTOU finding fixed in-PR). Memory recorded (project_1317_multiday_ticketing_hardening).

Per our flow I've left the merge to you. Want me to watch Verify to completion and report, or is that all for now?

---

There are still issues in two places I can spot, pricing tab where're we now, and insights Booked by day section

  due to the complex nature of per-day, per-ticket (specially for multi-day), there are many scenarios we need to take into consedration, e.g. an event might sell two days, but bookings are counted for both not separetly. Another example:
  multi-day event 16-12-2026 and 17-12-2026

  We'll get back to this later, in the mean time, we need to fix seeds as it's misleading now and wrong, because it never accounts for the new system for events, we need to make real and accurate, e.g.
  we can simplify it by creating an event with subscriptions for each scenrio under one specific user, and remove the rest junk, or leave 06-events.ts as-is and we comment it out so it doesn't seed, and create a new one.
  example scenario:
  multi date event
  ticket option enabled with two tickets, ticket 1 for day 1, and 2 for day 2

  the important thing is subscriptions for each option so we can see the stats, and which seat get occupied, this will come in handy later on

  ---

The 100% score should represent the overall health of the shape of all inputs for an event rather than just the current

Summary 100%
Title, Category, Type, Schedule

checks.

---

The 5 slices

┌──────────────────────────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬────────────────────────────────────┬──────────────────┐
│            Slice             │                                                                                                            What                                                                                                            │              Backend?              │      Weight      │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────┼──────────────────┤
│ 1. Render existing data      │ Reshape page IA → performance strip, financial waterfall, full pricing table, dates breakdown, registrations summary. All from data the DTO already returns. Extract inline blocks into sections/* (kills the              │ None                               │ Medium           │
│                              │ god-component).                                                                                                                                                                                                            │                                    │ (frontend)       │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────┼──────────────────┤
│ 2. Booked slots              │ Add getCapacitySnapshot enrichment to creator route → per-slot booked/left bars.                                                                                                                                           │ Tiny (1 call, mirrors public       │ Small            │
│                              │                                                                                                                                                                                                                            │ route)                             │                  │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────┼──────────────────┤
│ 3. Coupons + host            │ Two new aggregations on /statistics: coupon usage/discounts, and money-waterfall + per-host revenue split.                                                                                                                 │ New aggregations                   │ Medium           │
│ allocations                  │                                                                                                                                                                                                                            │                                    │                  │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────┼──────────────────┤
│ 4. Registration specs        │ Enrich CreatorEventRegistrationDTO with ticket/slot label, currency, coupon.                                                                                                                                               │ DTO + mapper                       │ Medium           │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────┼──────────────────┤
│ 5. Per-registration invoices │ New creator-scoped invoice-join endpoint.                                                                                                                                                                                  │ New endpoint                       │ Heaviest         │
└──────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────────────────────────────────┴──────────────────┘

Two things the plan flags that need your call

---

Add to calendar button