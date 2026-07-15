---
date: 2026-04-29
source: codex-session
project: Experts
topic: Ask AI global assistant
status: implemented
tags: [project/experts]
---

# Per-role Ask AI assistant

Implemented the V1 role-aware Ask AI model for Experts.

## Done

- Kept one global floating `Ask AI` button behind Statsig gate `ask_ai_global_assistant`.
- Preserved the admin-only V1 visibility rule for testing.
- Added assistant modes:
  - `learner`: published content plus the user's own enrollments, event registrations, bookmarks, recent views, and recommendation profile signal summary.
  - `creator`: creator-owned courses/events plus owned analytics summaries for enrollments, registrations, ratings, and views.
  - `admin`: broad platform/business context, published content, counts, and active subscription/service plans.
- Added server-side mode access rules:
  - all modes require authentication;
  - `admin` requires admin;
  - `creator` requires instructor or admin;
  - non-admin public access remains disabled unless `ASK_AI_PUBLIC_ROLLOUT_ENABLED=true`.
- Added `POST /api/v1/ai/ask` request `mode` and optional `conversationId`.
- API response now includes `{ answer, sources, mode, conversationId }`.
- Added indefinite conversation/message persistence in `ask_ai_conversations` and `ask_ai_messages`.
- Added EN/AR/ES i18n for mode labels, mode-specific empty text, suggestions, disclaimers, and new error states.
- Added focused route tests for auth, mode access, validation, rate limiting, and successful calls.
- Added curated legal/source-code context for legal and policy questions, including refund behavior from public policy plus route/handler implementation facts.
- Standardized public refund copy to seven (7) calendar days across Terms, FAQ, homepage FAQ, and Ask AI context.
- Ask AI legal sources now render as localized "Read more" links to the matching legal page.
- Added separate Ask AI knowledge-base RAG storage for curated documents: `ai_knowledge_documents` and `ai_knowledge_chunks`.
- Added V1 curated source manifest for public legal policies plus allowlisted vault/company notes.
- Added internal KB sync route at `POST /api/v1/internal/ai/knowledge/sync`, authenticated by `CRON_SECRET` or admin fallback.
- Ask AI now retrieves approved KB chunks by embedding the user question, filtering by mode/visibility, and injecting the results before live DB context.
- Added Docker staging cron to sync KB documents hourly at minute 15.

## Still Pending

- Run manual staging QA after applying the new migration.
- Validate Statsig gate targeting in staging/production.
- Decide when to enable learner/creator non-admin testing with `ASK_AI_PUBLIC_ROLLOUT_ENABLED=true`.
- Evaluate answer quality and decide whether to move from compact DB context to full vector/RAG retrieval.
- Apply the KB migration in staging, run the first KB sync, and QA legal/company retrieval with source chips.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
