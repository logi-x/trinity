---
title: "Experts user-driven recommendations implementation"
date: "2026-04-29"
tags: ["project/experts", "recommendations", "embeddings", "pgvector", "docker-cron"]
category: "session"
source: "codex"
source_id: "2026-04-29-experts-user-driven-recommendations"
---

Implemented a user-driven recommendations pipeline for the Experts dashboard.

Key decisions:

- Keep `content_embeddings` as the content semantic index.
- Add `user_recommendation_profiles` as a cached per-user/per-locale pgvector profile.
- Refresh profiles in batches through the existing Docker cron sidecar instead of refreshing on every user action.
- Use the authenticated dashboard as the V1 personalization surface.
- Keep detail-page "You might also like" as item-to-item related content.

Implementation notes:

- Signals are collected from the last 90 days across course enrollments, event registrations, bookmarks, ratings, likes/reactions, and authenticated views.
- Signal weights: completed course enrollment 8, active/pending enrollment 6, event registration 5, bookmark 4, rating value 1-5, like/reaction 3, authenticated view 1.
- Recency decay applies over the 90-day window with a floor so older signals still contribute weakly.
- Signals without matching `content_embeddings` rows are ignored.
- Personalized API excludes already consumed content: enrolled courses, registered events, bookmarked/liked content, recent views, and the user's own posts.
- New or low-signal users receive fallback recommendations from latest published visible courses, events, and posts.

Touched surfaces:

- `prisma/schema.prisma` and migration `20260429000000_user_recommendation_profiles`.
- `src/lib/recommendations/profiles/user-recommendation-profile.ts`.
- `src/lib/recommendations/queries/get-personalized-recommendations.query.ts`.
- `app/api/v1/recommendations/personalized/route.ts`.
- `app/api/v1/internal/recommendations/profiles/refresh/route.ts`.
- Dashboard row component `src/components/recommendations/PersonalizedRecommendations.tsx`.
- Docker cron sidecar hourly refresh entry.

Verification:

- Focused Vitest suites for profile weighting, personalized query fallback/exclusion, public personalized route, internal refresh route, and existing related recommendations route.
- Touched-file type checks passed.
- Prisma schema validation passed.

Follow-up same day:

- Updated public `/features` page with a dedicated AI-driven platform section.
- Added localized EN/AR/ES copy for shipped AI capabilities:
  - creator content drafts,
  - quiz question generation,
  - semantic discovery,
  - personalized dashboard recommendations,
  - unified related content.
- Added localized EN/AR/ES copy for possible future AI features:
  - translation assistance,
  - event agenda builder,
  - controlled platform content tutor,
  - adaptive learning paths,
  - creator performance insights,
  - content quality review.
- Verified touched feature page and feature locale files with `pnpm typecheck:touched`.

Still pending:

- Deploy migration and cron update to staging.
- Run manual staging QA for profile refresh, dashboard recommendations, fallback behavior, exclusions, and public `/features` copy in EN/AR/ES.
- Decide the next AI roadmap implementation priority.

Ask AI branch follow-up:

- Created branch `codex/ask-ai-global-assistant`.
- Added admin-only Ask AI API route at `POST /api/v1/ai/ask`.
- Added floating Ask AI UI behind Statsig gate `ask_ai_global_assistant`.
- The assistant uses live platform context from published courses, events, community posts, active plans, and business facts.
- Added EN/AR/ES copy under `global.askAi`.
- Added route tests for admin auth, validation, success, and rate limiting.

Ask AI pending:

- Configure the Statsig gate in staging/production.
- Manually test the floating assistant as admin and non-admin.
- Evaluate whether compact DB context is good enough or whether full vector/RAG retrieval is needed.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
