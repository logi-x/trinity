---
title: "Hybrid Ask Ai Rag Plan"
date: "2026-04-29"
tags: [plan, project/experts]
category: "plan"
---

# Hybrid Ask AI RAG Plan

## Summary

Build a separate Ask AI knowledge-base index for curated documents, while keeping live DB context for fresh platform data. V1 indexes legal policies and approved vault/company notes only. Code-derived context stays out of V1, except existing curated hardcoded legal facts can remain until replaced by KB retrieval.

## Key Changes

- Add separate KB storage, not `content_embeddings`:
  - `ai_knowledge_documents`: source type, source key, title, canonical path, locale, visibility, allowed modes, content hash, metadata, timestamps.
  - `ai_knowledge_chunks`: document id, chunk text, chunk index, token estimate, embedding `vector(1536)`, metadata, timestamps.
  - Use raw SQL for pgvector insert/upsert, matching existing embedding patterns.
- Add curated source manifest:
  - Legal sources from public policy content, canonical paths like `/refund-policy`, `/terms`, `/privacy`.
  - Vault sources from explicit allowlist only, starting with Ask AI branding guide and company/profile notes.
  - No broad vault crawling and no source-code scanning in V1.
- Add sync pipeline:
  - `POST /api/v1/internal/ai/knowledge/sync`
  - Auth: `CRON_SECRET` bearer or admin fallback.
  - Reads source manifest, chunks changed documents, embeds with `text-embedding-3-small`, upserts document/chunk rows, marks removed chunks inactive/deleted.
  - Add Docker cron entry, default hourly or daily; legal/vault docs change less often than content.
- Update Ask AI context assembly:
  - Keep current live DB context for courses, events, posts, metrics, creator-owned analytics, and learner signals.
  - Add `retrieveAskAiKnowledge({ mode, question, limit })` that embeds the question and fetches nearest KB chunks filtered by `allowedModes`, visibility, and active status.
  - Inject retrieved KB chunks after mode instructions and before live DB context, with source IDs returned in `sources`.
  - For legal source chips, keep UI mapping to localized “Read more” links using the source document path.
- Replace hardcoded legal context gradually:
  - V1 can keep the curated legal block as fallback.
  - Once KB legal retrieval is verified, remove or reduce hardcoded `LEGAL_CONTEXT` to avoid duplicated policy facts.

## Interfaces

- Ask AI API response remains:
  - `{ answer, sources, mode, conversationId }`
- `sources` may include:
  - `course:<id>`, `event:<id>`, `post:<id>`, `plan:<code>`
  - `kb:<documentId>#<chunkIndex>` or stable aliases like `legal:refund-policy`
- Add admin/internal status query later if needed:
  - pending/synced/failed documents
  - last sync time
  - chunk count by source type

## Test Plan

- Unit tests:
  - legal/vault source manifest parsing
  - chunking is stable and respects max chunk size
  - source hash prevents unnecessary re-embedding
  - retrieval filters by mode and visibility
- Route tests:
  - sync rejects missing/invalid cron secret for non-admin
  - sync upserts changed legal/vault docs
  - sync reports failed sources without aborting the batch
- Ask AI tests:
  - learner retrieves public legal/company chunks only
  - creator retrieves creator-safe policy/company chunks
  - admin retrieves admin-allowed chunks
  - legal questions include a “Read more” source path
  - normal course recommendation questions still rely primarily on live DB/personal context
- Verification:
  - `pnpm typecheck:touched` for Ask AI, KB sync, schema/migration, i18n/UI source rendering.
  - focused Vitest suites for KB sync/retrieval and Ask AI route/context.

## Assumptions

- V1 knowledge sources are legal policies plus approved vault/company notes.
- V1 does not auto-index source code.
- Separate KB tables are preferred over reusing `content_embeddings`.
- Live platform data remains queried directly from DB, not copied into KB docs.
- Question embeddings use `text-embedding-3-small` with 1536 dimensions.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
