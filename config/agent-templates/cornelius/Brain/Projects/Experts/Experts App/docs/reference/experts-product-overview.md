---
title: "Experts — Product Overview"
date: "2026-04-04"
tags: ["project/experts", "topic/product-overview", "outcome"]
category: "docs/experts-reference"
source: "consolidated from planning PROJECT/REQUIREMENTS/ROADMAP/research (GSD planning, retired)"
updated: "2026-07-15"
---

# Experts — Product Overview

> Consolidated from the retired GSD planning notes (PROJECT, REQUIREMENTS v1.0/v1.1,
> ROADMAP, research summary). This is a **point-in-time snapshot** of intent as of the
> v1.0–v1.1 planning period (Mar–Apr 2026); for current behavior trust the code, not this note.
> stable repo reference in [[Projects/Experts/Experts App/docs/reference/codebase/architecture|reference/codebase]].

## What this is

Experts is an expert-led online learning platform (LMS): instructors create and sell
courses and live events; learners enroll and progress through structured curricula; the
platform facilitates quality through community, certification, and monetization. Built as a
single **Next.js 16** full-stack app with a **CQRS-style domain layer**, **PostgreSQL/Prisma**,
and three locales (**en/ar/es**, RTL-aware).

**Core value:** learners find and complete expert-led courses and events — instructors create
quality content, the platform verifies that quality, and learners trust the result.

## Platform capabilities (validated / existing)

- **Auth** — email/password + OAuth (Google, GitHub, Apple) via NextAuth v5
- **Courses** — catalog browse/search/filter; instructor curriculum builder (modules + lessons)
- **Events** — creator event creation (slots, agendas, registration); discovery + filter
- **Learning** — enrollments, lesson progress tracking
- **Community** — posts, comments, likes, sharing
- **Monetization** — affiliate system (referrals, commissions, payouts); payment gateways
  (Stripe, Noon, Tabby)
- **Platform** — admin panel (analytics, affiliate mgmt); i18n en/ar/es with RTL; SEO
  (metadata, sitemaps, hreflang per locale); Cloudflare R2 media; React Email notifications;
  400+ Vitest tests

## Milestones

- ✅ **v1.0 — Instructor Certification** (shipped 2026-03-08): two-level (VERIFIED / ACADEMIC)
  gated application flow, admin review queue, profile badges, certified-instructors view.
  → outcomes: [[Projects/Experts/Experts App/docs/designs/2026-03-07-instructor-certification|instructor-certification]],
  [[Projects/Experts/Experts App/docs/designs/2026-03-08-gated-instructor-certification-levels|gated levels]]
- 🚧 **v1.1 — Course Trust & Certification Depth**: a full application/evidence/review audit
  trail replacing the flat certification model, plus **course recognition types** (General
  Learning / Professional Training / Academic Program) gated by instructor certification level.
  → outcomes: [[Projects/Experts/Experts App/docs/designs/2026-03-09-cert-schema-db-foundation|cert-schema-db-foundation]],
  [[Projects/Experts/Experts App/docs/designs/2026-03-10-cert-schema-domain-migration-ui|cert-schema-domain-migration-ui]]

### Other consolidated build streams
- **Noon payments** — subscription webhook, checkout-metadata reliability, production hardening
  (see `docs/designs/2026-03-31-noon-*` and `2026-04-03-noon-production-hardening`)
- **Admin control systems** — users / monetary / analytics / performance
  ([[Projects/Experts/Experts App/docs/designs/2026-04-04-admin-control-systems|admin-control-systems]])
- **UI migration** — shadcn → HeroUI + purple/violet → primary-color tokens
  ([[Projects/Experts/Experts App/docs/designs/2026-03-20-shadcn-to-heroui-migration|shadcn-to-heroui-migration]])

## Key architectural decisions (v1.1, from research)

- **`InstructorCertificationProfile` read cache** — one indexed row per instructor answering
  "what is this instructor's current level?" without joining application history on every
  course create/update/publish. The single source of truth for instructor level.
- **Schema-first ordering** — migrate the deep certification schema *before* building the
  recognition-type guard on top of it, to avoid a two-pass refactor.
- **Enforcement completeness** — `canInstructorUseRecognitionType()` is a pure guard called
  from **all three** course handler entry points (create, update, publish), and always
  re-fetches the instructor's level from the DB, never from session data.
- **Migration safety** — additive `ADD COLUMN ... DEFAULT 'GENERAL_LEARNING'` (never null
  against live data); backfill the profile cache for existing certified instructors before
  the old flat table is deprioritized; old table kept read-only.

## Roadmap status (as of snapshot)

In-progress at snapshot time (verify against current code — several have since shipped):
course-completion PDF certificates (COMP-01..05), curriculum-builder UX (CURR-01..04),
student learning-journey reliability (LEARN-01..04), and the v1.1 recognition-type UI.
