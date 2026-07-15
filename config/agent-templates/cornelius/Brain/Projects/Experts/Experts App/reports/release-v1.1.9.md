---
title: "Experts App v1.1.9 — release notes"
date: "2026-05-08"
updated: "2026-06-01"
tags: ["project/experts", "project/experts-app", "topic/release", "docs/changelog"]
category: "Projects/Experts/Experts App/reports"
source: "generated"
source_id: "Projects/Experts/Experts App/reports/release-v1.1.9.md"
---

# Experts App v1.1.9

**Status:** **Released** — **`v1.1.9-stable`** (**2026-06-01**), per published `CHANGELOG.md` frontmatter. The **1.1.8** changelog slice was **skipped in favour of 1.1.9**.

**Line started:** **2026-05-08** (version bump on `main` after **1.1.8**).

**Git commit range (summary source):** `44eff14287f3406394206e8a0359eec7008b622e` … `45fceafc48bd0df7573f9c4b85627825777aa9d5` (~**409 commits**).

**Channel tags on this line:** `v1.1.9-alpha.1`, `v1.1.9-beta.1` … `v1.1.9-beta.6`, `v1.1.9-rc.4` … `v1.1.9-rc.9`, **`v1.1.9-stable`**.

**Next semver:** new work belongs under **1.2.0 — Unreleased** only after this line is frozen in git + changelog (see `release-changelog.mdc` in repo `.cursor/rules/`).

## Links

- [[Entities/Projects/Experts App|Experts App (entity hub)]]
- [Google Docs — V1.1.9](https://docs.google.com/document/d/1oJb9RHMSWVPRfXk0o43Y-YH1Pn46u7SUL0Kw73v0gkU/edit)
- **Canonical technical log:** `apps/experts-app/public/reports/CHANGELOG_RAW.md` (relative to monorepo root)
- **Published changelog:** `apps/experts-app/public/reports/CHANGELOG.md` (relative to monorepo root)

## Release channels

Numbered snapshots per line (**alpha** → **beta** → **RC** → **stable**). Channel tags are readiness checkpoints; **stable** is the production-facing tag for this line. Definitions: **IMPORTANT** block at top of `CHANGELOG.md`.

---

## What to test since last release?

**1.1.9** includes all changes since **1.1.8**. Focus areas for learners, creators, admins, and platform ops (mirrors published changelog).

### Security, CSP, and upload hardening

- Incident remediation **#1–#15:** internal upload lockdown, thumbnail ownership, per-user upload rate limits, pending→ready lifecycle, storage janitor, buffer rechecks, defense-in-depth headers, course detail / presence / viewers exposure fixes, CSP nonce + Report-Only → enforcing CSP (4A/4B), violation reporting, MIME→extension for R2 keys, inline-renderable MIME allowlist, RFC 5987 filenames, cookie-scope regression tests.
- **EXP-68:** paid content paywall; enrolled learners keep access when a course is temporarily unpublished.
- **EXP-170 family:** `safeErrorJson`, `DomainError`, ESLint error-disclosure sink on `src/lib`; no raw `error.message` / stack in API responses.
- **Cron:** timing-safe `CRON_SECRET`, fail-closed when unset.
- **EXP-174:** realtime sync IDOR, channel caps, ReDoS; removed unauthenticated share/test diagnostic endpoint.

### Storage, R2, quotas, and course-scoped uploads

- **`lesson_resources` dropped**; unified **`course_lesson_assets`** / flat **`CourseAsset`** XOR; **`course_*` schema naming**.
- Course-scoped upload tree; pending-first uploads; PUT-first guardrail; R2 orphan reaper decommissioned (**EXP-231**) → janitor sweeps.
- Quota ledger (reservations, `File.size` BigInt, tier-aware alerts, admin storage dashboard, cron alerts).
- Storage janitor crons in staging/production compose (orphan sweep, reservation cleanup, etc.).

### Ask AI and conversations

- **`AskAiConversation.deletedAt`** + in-tx soft-delete re-check (**EXP-239**).
- Stream abort before load (**EXP-222**), 200-message cap (**EXP-205**), rate limits (**EXP-206**), UUID guards on `[id]` (**EXP-221**), sanitized SSE errors (**EXP-207**).
- Ask AI route visibility: explicit allow model (deny-list removed).
- Lazy OpenAI client for build without **`OPENAI_SECRET`** (**EXP-181**).

### Courses, curriculum, recognition

- **Recognition type (Phases 08–09):** `recognitionType`, `recognitionReviewStatus`, eligibility, review scanner, admin UI.
- DB-authoritative roles on course lifecycle routes (**EXP-197/199/212/213**); pending approval on submit (**EXP-214**); archive/delete dialogs.
- Lesson assets CRUD post–resource drop; attachment ownership (**EXP-50**); progress UUID validation (**EXP-79**).

### Payments and Tabby

- Tabby **KSA-only** + checkout UX when ineligible (**EXP-96/99+**); CSP for Tabby domains.
- Noon sanitize tests (**EXP-94**); fail-closed **`CF_ORIGIN_SECRET`** (**EXP-123**); checkout error sanitization (**EXP-201**).

### Realtime and community

- Sync rate limits and bounded queries (**EXP-191–195**); post like channel isolation; shared post Zod schema (**EXP-224/240**).

### Auth, SEO, session

- Auth package under **`src/lib/auth/`** (**EXP-200**); canonical app origin (**EXP-204/216–218**); login remount fix (**EXP-225**); `/creator` guard (**EXP-53**).

### Certifications, certificates, company collateral

- Phase 07 cert schema migration; certificate `courseTitle` from DB (**EXP-75**); company print/watermark/showcase polish.

### Ops, Docker, CI

- Cron sidecar **`APP_BASE_URL`**, hidden **`CRON_SECRET`**, loopback DB/Redis, Node 24-alpine; Prisma migrate secrets (**EXP-190**); migration-drift CI (**EXP-227**); deploy gates + Slack notifications; **`APP_VERSION`** on deploy jobs.

### Agents, routines, tooling

- R7/R8/R9 routines, pool dispatcher, GitNexus skill/index updates.

### UI polish

- Alert-dialog sweep; course archive/delete; course detail enrollment queries; creator event role staleness; admin embeddings under AI.

---

## Stakeholder summary

(Same **1.1.9** line — programme owners, instructors, ops.)

- **Newsletter:** public signup and unsubscribe.
- **Company profile & print:** invoices, letterhead, business cards, watermarks, typography.
- **Courses & curriculum:** creation reliability, module assets, uploads, EN/AR course-building, AI curriculum suggestions.
- **Statsig:** gradual gates (creator onboarding, dashboard beta, Ask AI, features page); dynamic banner/CTA; session-aware behaviour; analytics / session replay where enabled.
- **Platform:** smoother staging/production deploys; realtime and stability housekeeping.

---

## Suggested verification checklist

### Product (stakeholder)

- Newsletter subscribe / unsubscribe.
- Company collateral print (invoice, letterhead, business card); watermark EN/AR; container `.env` sourcing (quoted watermark).
- Course create/edit; module assets; curriculum uploads EN/AR; AI suggest flows.
- Statsig gates and dynamic config (banner, hero CTA, Ask AI visibility).

### Security and access

- Anonymous users cannot read paid course detail content; enrolled users retain access on temporary unpublish.
- Upload routes: ownership, rate limits, pending→ready; CSP reports in staging without breaking core flows.
- Cron routes reject missing/wrong secret; no error stack in API JSON.

### Storage and media

- Lesson/community/video uploads complete and appear in UI; quota dashboard and over-threshold alerts sane on test accounts.
- Janitor cron endpoints succeed in staging (orphan sweep, reservation cleanup) with auth.

### Payments

- Tabby visible only when KSA-eligible; disabled state + billing address hint when not.
- Checkout failure messages generic (no provider payload leak).

### Ask AI

- Conversation load aborts prior stream; soft-deleted conversation cannot accept new messages; rate limits on management APIs.

### Courses and admin

- Recognition type rules on publish; submit sets pending approval; archive/delete dialogs; module lesson/quiz routes respect fresh DB roles.

### Deploy / ops

- `docker compose` migrate job with secrets; **`APP_VERSION`** on deployed image; healthcheck; **`v1.1.9-stable`** (or current tag) pull on target host.
- Migration-drift CI green on release branch.

---

## Historical note

Early brain draft (2026-05-11) described only **8–11 May** and **`v1.1.9-beta.3`**. This file now tracks the **full 1.1.9 line** through **stable** and matches the published changelog synthesis (**2026-05-31** notes block in repo).
