---
title: "Experts AI Tools Session"
date: "2026-04-16"
tags: ["project/experts", "project/experts-app", "topic/ai", "topic/creator-tools", "topic/courses", "topic/events"]
category: "session-log"
source: "codex"
source_id: "Raw/sources/2026-04-16-experts-ai-tools-session.md"
---

# Experts AI Tools Session — 2026-04-16

- Scope: AI-powered creator tools for `apps/experts-app` (course + event forms).
- Branch: `codex/learner-layout-lms-bridge`
- Focus: AI auto-completion and list suggestion for course/event title, description, content, learning outcomes, requirements, and tags.

## What was built

### Core infrastructure

- [x] `POST /api/v1/ai/suggest` — auth-gated (instructor/admin), Zod-validated, Redis rate-limited (20 req/user/hour), context-sanitized, OpenAI `gpt-4o-mini` backend.
- [x] `src/hooks/use-ai-suggest.ts` — client hook, stores `errorCode` (not raw message).
- [x] `src/hooks/use-ai-suggest-list.ts` — wraps `use-ai-suggest`, splits newline response into `string[]`, strips bullet symbols.
- [x] `src/components/ui/ai-suggest-button.tsx` — popover with suggestion preview, Use this / Try again / Dismiss.
- [x] `src/components/ui/ai-suggest-list-button.tsx` — checklist popover, auto-selects all items, user can toggle individually before adding.

### Supported field types (API `fieldType` enum)

| fieldType      | Returns                                | Used on                         |
| -------------- | -------------------------------------- | ------------------------------- |
| `title`        | Single string (50–120 chars)           | Course + Event general sections |
| `description`  | Single string (110–220 chars)          | Course + Event general sections |
| `content`      | Markdown string (200–600 words)        | Course + Event general sections |
| `outcomes`     | Newline-separated list (4–6 items)     | Course extras + Event extras    |
| `requirements` | Newline-separated list (3–5 items)     | Course extras + Event extras    |
| `tags`         | Newline-separated list (6–10 keywords) | Course extras only              |

### Security & reliability

- Rate limit: 20 req/user/hour via Redis fixed-window (`ai:suggest:rl:<userId>`). Fails open if Redis is down.
- Context sanitization: all user-supplied context strings stripped of newlines and truncated before embedding in prompts.
- Error codes returned (never raw OpenAI messages): `ai_busy`, `ai_unavailable`, `ai_config_error`, `ai_no_context`, `ai_rate_limited`, `ai_unknown`.
- Client translates error codes via `t("aiErrors.<code>")` — all 6 locale files updated (en/ar/es × courses/events).

### Course form changes

- `CourseFormSchema` extended with `learningOutcomes: string[]`, `requirements: string[]`, `tags: string[]`.
- `course.mapper.ts`: `mapCourseToFormValues` reads these from DB; `buildCourseUpdatePayload` sends them on save.
- New `CourseExtrasSection` component — outcomes + requirements + tags, each with manual add and AI suggest list button.
- `CourseForm` renders `CourseExtrasSection` between Settings and Pricing.

### Event form changes

- `EventExtrasSection` receives optional `aiContext` prop (title, category, eventType).
- AI suggest list buttons added next to "Add" for both outcomes and requirements.
- `event-form.tsx` passes `aiContext` when rendering the extras section.

### i18n

- All 6 locale files (en/ar/es × courses/events) updated with:
  - `aiSuggest`, `aiAccept`, `aiRetry`, `aiDismiss`, `aiGenerating`
  - `aiSuggestList`, `aiAddAll`, `aiAddSelected`
  - `aiErrors.*` (6 error codes each)
  - Course extras section strings (en/ar/es): extrasTitle, extrasDescription, whatWillTheyLearn, outcomesHelper, requirementsLabel, requirementsHelper, tagsLabel, tagsHelper, addOutcome, addRequirement, addTag, previewForLearners

## AI feature roadmap agreed (future tiers)

### Subscription gating (planned next)

- Restrict AI tools to paid subscriptions with the `"AI content generation"` plan entitlement (Expert or Institution).
- Add a shared `planHasFeature` evaluator and expose `plan.features.aiTools` in `ActivePlanDTO` for preemptive client-side disable.
- Return `ai_plan_required` from AI APIs and localize it across creator courses/events in en/ar/es.

### Tier 2 (next)

- **Quiz question generator** — given lesson content, generate N MCQ questions pre-filling the quiz form. Highest raw instructor impact.
- **Lesson content outline** — "Draft for me" button in the curriculum lesson editor using existing MarkdownEditor + onChange pattern.

### Tier 3

- **Translation assist** — translate any text field to Arabic/Spanish. Removes biggest barrier to multi-language publishing.
- **Event agenda builder** — suggest time-boxed agenda items from event title + type + duration.

## Key decisions made this session

- Use OpenAI SDK (`openai` moved from devDependencies → dependencies); `OPENAI_SECRET` env var already set.
- API returns stable `errorCode` strings, never raw OpenAI messages. Client translates via i18n.
- List suggestions use newline-separated plain text (not JSON) — simpler, robust to model variation.
- Prompt instructions stay in English regardless of locale; `locale` parameter only controls response language.
- Rate limit fails open (allows request) when Redis is unavailable to avoid blocking users during outages.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
