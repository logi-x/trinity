---
title: "Ask Ai Per Role Plan"
date: "2026-04-29"
tags: [plan, project/experts]
category: "plan"
---

# Per-Role Ask AI Assistant

## Summary

Build one global **Ask AI** button with role-aware assistant modes. V1 is visible only to admins for testing through Statsig, but the product model supports learner, creator, and admin modes. Admins can switch between all modes; future non-admin rollout will expose only modes their account is allowed to use.

## Key Changes

- Replace the current admin-only assistant with a mode-aware assistant:
  - `learner`: for content discovery, next-step recommendations, course/event questions, and personalized guidance.
  - `creator`: for creator-owned courses/events, content improvement, and creator analytics summaries.
  - `admin`: for platform operations, business context, promotion, services, metrics, and all-content visibility.
- UI behavior:
  - Single floating `Ask AI` button.
  - Clicking opens chat in the default mode, with an in-chat mode switcher.
  - Default mode priority: admin users default to `admin`; creators default to `creator`; regular users default to `learner`.
  - During V1 rollout, Statsig gate `ask_ai_global_assistant` remains targeted to admins only.
- Server-side access rules:
  - All requests require authentication.
  - `admin` mode requires admin role.
  - `creator` mode requires instructor or admin role.
  - `learner` mode is safe for any authenticated user, but V1 can keep non-admin mode access disabled with an app config default until public rollout.
- API contract:
  - `POST /api/v1/ai/ask`
  - Request adds `mode: "learner" | "creator" | "admin"`.
  - Response returns `{ answer, sources, mode, conversationId }`.
- Context behavior:
  - Learner mode uses published content plus the user’s enrollments, event registrations, bookmarks, recent views, and recommendation/profile signals.
  - Creator mode uses only the creator’s own courses/events plus analytics summaries: enrollments, registrations, ratings, views, and revenue/engagement summaries where available.
  - Admin mode uses all existing platform/business context and can include platform-wide counts, plans, published content, promotion candidates, and operational notes.
- Chat persistence:
  - Store full Ask AI conversations indefinitely.
  - Users can access their own conversations.
  - Admins can audit all conversations.
  - Persist mode, userId, messages, sources, timestamps, and model metadata.
- Keep source boundaries strict:
  - Learner mode must never include admin metrics, creator-private analytics, draft content, payouts, or internal operations.
  - Creator mode must never include other creators’ private analytics or draft content.
  - Admin mode can access broader platform context.

## Test Plan

- API route tests:
  - rejects unauthenticated requests;
  - rejects `admin` mode for non-admins;
  - rejects `creator` mode for non-creators;
  - allows admins to use all modes;
  - validates `mode`, `message`, `history`, and `conversationId`;
  - stores conversation/messages after successful responses.
- Context tests:
  - learner context includes public content and that user’s personal signals only;
  - creator context includes owned content and owned analytics only;
  - admin context includes platform-wide context.
- UI tests or focused component checks:
  - admin sees mode switcher with learner/creator/admin;
  - creator sees learner/creator when public rollout is enabled;
  - learner sees learner only when public rollout is enabled;
  - hidden for non-targeted users during admin-only Statsig rollout.
- Regression checks:
  - existing Ask AI route tests still pass;
  - `pnpm typecheck:touched` for Ask AI API, assistant context, UI, schema/migration, and i18n files.

## Assumptions

- V1 rollout remains **admins only** through Statsig for testing.
- Creator mode is included in this implementation, using own content plus analytics.
- Full chat history is persisted indefinitely.
- Public non-admin rollout is a later switch/config change, not a separate rewrite.
- The current floating chat UI improvements should be preserved; only the mode/access/context model changes.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
