---
title: "Experts App v1.1.7 — release candidate"
date: "2026-05-04"
updated: "2026-05-04"
tags: ["project/experts", "project/experts-app", "topic/release", "docs/changelog"]
category: "Projects/Experts/Experts App/reports"
source: "generated"
source_id: "Projects/Experts/Experts App/reports/release-v1.1.7.md"
---

# Experts App v1.1.7 (release candidate)

**Status:** Release candidate (as of **2026-05-04**).  
**Window (changelog):** **18 April 2026** → **4 May 2026**.

## Links

- [[Entities/Projects/Experts App|Experts App (entity hub)]]
- [Google Docs — V1.1.7 tab](https://docs.google.com/document/d/1oJb9RHMSWVPRfXk0o43Y-YH1Pn46u7SUL0Kw73v0gkU/edit?tab=t.nb3j8xqi8mgh)
- **Canonical technical log:** `` `apps/experts-app/public/reports/CHANGELOG_RAW.md` `` (**monorepo root**)
- **Published / client-readable changelog:** `` `apps/experts-app/public/reports/CHANGELOG.md` `` (**monorepo root**)

## Summary (stakeholder-facing)

- **AI — embeddings & recommendations (Phase 15):** New **`ContentEmbedding`** and **`EmbeddingSync`** Prisma models on **pgvector** (vector(1536), unique on `entityType + entityId + locale`); Postgres images swapped to **`pgvector/pgvector:pg16`** in data and staging Docker. Sync pipeline (**`embedding-sync.service`** + **`embedding-sync.worker`**) with OpenAI rate-limit aware batching; internal **`/cron`** route (cron-secret auth) on a **Vercel cron every two minutes**; failed rows kept for admin retry. **Publish hooks** enqueue embeddings for courses, events, and community posts. New **admin debug page** exposes pending / synced / failed counts and the latest 20 sync rows. Unified **related content cards** across course / event surfaces with a graceful **fallback**, plus user-driven **dashboard recommendations**.
- **AI — Ask AI assistant:** Admin / creator / learner **modes** with role-aware responses, **conversation IDs**, mode-specific **rate limiting**, **typing indicator**, **copy message** and **clear conversation** controls; new **`AskAiConversation` / Message** models persist history.
- **AI — knowledge sync:** New sync route ingests **curated AI knowledge documents**, chunks + embeds them, and wires curated **legal / refund / policy** context into Ask AI for higher-accuracy answers; tests cover the sync route and retrieval. **`OPENAI_API_KEY` → `OPENAI_SECRET`** rename across services, samples, and docs.
- **Curriculum & lesson player:** New **`useVideoLessonCompletionGate`** hook gates "mark complete" until the required video portion is watched; lesson player now renders **text, PDF, audio, presentation, and video** types consistently. **`CourseAssetsPanel`** supports asset uploads with clearer error handling; **`CourseAssetsTab`** added inside **`ModuleOverview`**. Video watch progress API improved for more reliable engagement tracking. New **attachment content API** returns **signed URLs** with **role + course-status access checks**, content-disposition helper, and unauthorized-access tests.
- **Learn workspace:** Top nav with **dashboard / courses / events** links, **mobile responsive** via **`useIsMobile`**, persistent **sidebar state**, and improved loading indicators on **`LearnerWorkspaceLayout`** and the lesson player. New **lesson type components** for text and video with EN / AR / ES labels.
- **Creator, company & settings:** Full migration **`CreatorLayoutV2` → `CreatorLayout`**; new **`CreatorFooter`**; hardcoded violet/purple replaced with **primary color tokens**. New **Creator Studio Section** on the HomePage (staged behind a comment toggle); **Saudi Riyal** icon used for revenue. Settings pages (**profile**, **privacy**, **billing**, **portfolio**) rebuilt on a shared **Settings UI**; **`ProfileSettings` → `PortfolioSettings`** with experience entries and **social-link normalization / validation**. **Multilingual company profile page** (EN / AR / ES) with shared **`CompanyProfilePage`** and a print-ready PDF design; new **Company workspace**, **business card** generator with multiple designs and print, **letterhead** component, and a dedicated **company collateral** page; auth checks added on company-only surfaces.
- **Marketing & features page:** Expanded discovery with new **`semantic`** filter, refreshed section IDs for accessibility, modernized button styles and **`rounded-3xl`** card borders, new **search** with EN / AR / ES placeholders / results, improved AI features layout. Marketing surface highlights AI platform features.
- **Course detail polish:** **framer-motion** transitions between tabs, **`aria-label`** attributes, and a more responsive tab layout.
- **Analytics, ops & tooling:** **Statsig** integration (**`@statsig/js-client`**, singleton **`StatsigClient`**, **`MyStatsig`** wrapper, server context API, **session replay**, creator **onboarding page**, global promo banner; **`NEXT_PUBLIC_STATSIG_CLIENT_KEY`** in staging). Scheduled jobs moved off Vercel cron onto a **Docker sidecar**. Staging backup rolled to **`staging_data_backup_28-04-2026.sql`**; **Redis password** sourced from env; AWS SDK and assorted dependencies bumped (incl. **`3.1038.0`** / **`3.974.6`** lines). New **GitNexus** Claude skills (**`gitnexus-cli`**, **`gitnexus-debugging`**, **`gitnexus-exploring`**, **`gitnexus-impact-analysis`**, **`gitnexus-refactoring`**, **`gitnexus-guide`**) plus AGENTS.md / CLAUDE.md guidance and MCP server settings (GitNexus + CodeGraph enabled). Comprehensive **architecture document** for the Experts App; **`graph.json` / `graph.html` / `GRAPH_REPORT.md`** under `graphify-out/` with a **`graphify.py`** automation script. **`mobile-tokens.md`** documents SwiftUI design tokens to keep web and native (`apps/experts-os`) aligned.

## Institutional memory

Decisions and deep dives for this work should also appear on the relevant **Wiki/Concepts/** pages (e.g. [[Wiki/Concepts/AI Features|AI]], [[Wiki/Concepts/Recommendations]], [[Wiki/Concepts/Embeddings]], [[Wiki/Concepts/Access Control]], settings, company profile, [[Wiki/Concepts/Analytics]], tooling) when they change long-lived behaviour — not only in this release note.
