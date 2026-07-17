---
title: "2026-06-11 Experts — GSD .planning extraction (issue candidates + done ledger)"
date: "2026-06-11"
tags: [project/experts, gsd, planning, backlog, issues, extraction, certification, admin, analytics]
category: "daily"
source: "session"
source_id: "Raw/sources/2026-06-11-experts-gsd-planning-extraction.md"
---

# Experts — GSD `.planning` Extraction

Operator directive: **extract GSD planned/pending/done work into the brain to be tracked as GH issues later.**
Source of truth: `apps/experts-app/.planning/` (GSD workspace, milestone **v1.1 — Course Trust & Certification Depth**).
Read-only extraction; no repo changes. This note is the **issue-candidate source of truth**; outstanding items are
mirrored as rows in [[Action-Tracker]].

## Outcome (2026-06-11) — verified + filed

After extraction, all 5 candidates were **verified against live code** (4 parallel Explore passes over `apps/experts-app`). This corrected 2 of 5 — proving the "verify before filing" discipline:

| Item | Verified reality | Action |
| ---- | ---------------- | ------ |
| **O1** Recognition Type UI/admin | Backend shipped (Phase 8); UI/badge/cert-column/admin-column genuinely missing | **Filed [#987](https://github.com/logi-x/experts/issues/987)** (`completeness`) |
| **O2** Admin Users UI | **Already fully shipped** in code — only missing a GSD summary doc | **Not filed** |
| **O3** Completion certificates | Model + manual issuance + dashboard exist; missing auto-issuance, public verify, working PDF | **Filed [#988](https://github.com/logi-x/experts/issues/988)** (`completeness`) |
| **O4** Learning Polish | **Already fully shipped** — drag-drop reorder, prerequisites, resume, progress, navigation all present | **Not filed** |
| **O5** Platform Metrics | Phase 14 shipped the analytics tabs/pages; real delta = catalog/community/cohort/MRR-ARR/ZATCA/PostHog/alerting/API | **Filed [#989](https://github.com/logi-x/experts/issues/989)** (`completeness`+`backlog`) |

#987 ⇄ #988 cross-reference each other (shared `CourseCertificate` issuance path). All filed via experts-beacon with `agent-fp` fingerprints; GH dedup scan was clean. **GSD 14-05, and the ex-Phase-2/3 backlog items, can be marked done in `.planning` — the code already satisfies them.**

The per-item blocks below are the original extraction (pre-verification); read them with the corrections in this table.

---

## ⚠️ Read this before filing any issue: the GSD tracking docs are STALE

The roadmap tables and requirement checkboxes do **not** reflect real status. Trust the per-phase
`SUMMARY.md` / `VERIFICATION.md` files, not `ROADMAP.md` or `REQUIREMENTS-v1.1.md`.

Concrete drift found 2026-06-11:

- `ROADMAP.md` says **Phase 8 "Not started, 0/2"** — but Phase 8 has both `08-0{1,2}-SUMMARY.md` and an
  `08-VERIFICATION.md` marked **`status: passed`, 8/8 must-haves** (verified 2026-05-12). Phase 8 is **DONE**.
- `ROADMAP.md` says **Phase 14 "0/5 Planned"** — but `14-01..14-04` each have a `SUMMARY.md`; only **`14-05` is
  plan-only** (no summary). Phase 14 is **4/5 done**, not 0/5.
- `REQUIREMENTS-v1.1.md` traceability shows **CREC-\*** all unchecked and **CSCH-06/09/10** unchecked, yet Phase 7
  SUMMARYs + Phase 8 VERIFICATION prove CSCH-06/09/10 and CREC-01/02/03/04/06/08 shipped. Checkboxes are stale.

**Real completion signal = presence of `NN-SUMMARY.md` per plan + a passing `NN-VERIFICATION.md`.**

Status scan (plans / summaries / verification per phase):

| Phase | plans | summaries | verification | Real status |
| ----- | ----- | --------- | ------------ | ----------- |
| 01 | 2 | 2 | 1 | ✅ done (v1.0) |
| 04 | 3 | 3 | 1 | ✅ done (v1.0) |
| 05 | 3 | 3 | 0 | ✅ done (v1.0, validation-only — known tech debt) |
| 06 | 2 | 2 | 1 | ✅ done |
| 07 | 3 | 3 | 0 | ✅ done |
| 08 | 2 | 2 | 1 | ✅ done (roadmap says "not started" — WRONG) |
| 09 | 0 | 0 | 0 | ❗ **outstanding** — context only |
| 10 | 6 | 6 | 0 | ✅ done |
| 11 | 1 | 1 | 1 | ✅ done |
| 12 | 2 | 2 | 1 | ✅ done |
| 13 | 6 | 6 | 0 | ✅ done |
| 14 | 5 | 4 | 0 | ◐ 4/5 — **14-05 outstanding** |
| 15 | 5 | 5 | 1 | ✅ done |

---

## Outstanding work — issue candidates

Five filable items. Ordered by readiness. Each block is shaped to drop straight into a GH issue.

### O1 — Phase 9: Course Recognition Type — UI & Admin  `[epic; suggest split into 2]`

- **Status:** Context gathered + implementation decisions locked (D-01…D-14), **0 plans written, 0 executed.**
  Phase 8 (the DB/domain dependency) is **done**, so Phase 9 is unblocked for planning + execution.
- **Requirements:** CREC-05, CREC-07, CREC-09, CREC-10.
- **Source:** `.planning/phases/09-course-recognition-type-ui-and-admin/09-CONTEXT.md` (only file).
- **Scope (from locked decisions):**
  - **CREC-05** — Creator course form: gated recognition-type field as **radio cards** (3 cards: General
    Learning / Professional Training / Academic Program). Ineligible cards stay visible but locked with
    "Requires [Verified/Academic] certification" helper + inline "Apply for [level] certification →" link to the
    existing `creator/certifications` flow. Default `GENERAL_LEARNING`; edit preserves current value (API owns
    enforcement). (D-06, D-07, D-08)
  - **CREC-07** — Public course **detail page** badge near "What you get" / certificate section. Only
    PROFESSIONAL_TRAINING and ACADEMIC_PROGRAM render a badge (GENERAL_LEARNING shows nothing). HeroUI **Chip**
    (not Badge — Phase 10 convention), primary tokens. (D-09, D-10, D-11)
  - **CREC-09** — Certificate issuance wired to recognition type × instructor `certificateIssuanceEnabled`:
    - **Schema change** — add `recognitionType` column to **`Certificate`** model + migration, backfill existing
      rows to `GENERAL_LEARNING`. Value is **snapshotted at issuance** (historic certs don't mutate on
      reclassification). This schema work lives in Phase 9, not Phase 8. (D-02, D-05)
    - Issuance gate (D-04): GENERAL_LEARNING → always issue a simple "Completion of [course]" document;
      PROFESSIONAL_TRAINING → training cert iff instructor VERIFIED|ACADEMIC; ACADEMIC_PROGRAM → academic cert iff
      instructor ACADEMIC **and** `certificateIssuanceEnabled = true`.
    - **Scope expansion flag (D-03):** GENERAL_LEARNING completion document is a *new, distinct* template beyond the
      existing training/academic templates — size template work accordingly.
  - **CREC-10** — Admin courses table: read-only "Type" column (same Chip), filter dropdown + sortable. No admin
    override (CREC-F1 stays v2-deferred). (D-12, D-13, D-14)
- **Suggested issue split:**
  - **9a** — Creator gated field (CREC-05) + public badge (CREC-07). Pure UI + i18n (en/ar/es), no schema.
  - **9b** — `Certificate.recognitionType` schema/migration + issuance gate + GENERAL_LEARNING completion-doc
    template (CREC-09) + admin column/filter (CREC-10). Carries the migration + template weight.
- **Cross-link:** CREC-09's GENERAL_LEARNING completion document **overlaps O3** (Course Completion Certificates).
  Decide whether O3 is subsumed by 9b or vice-versa before filing both.
- **Open items left to planner:** exact Chip variants/colors per level, narrow-width radio-card layout, en/ar/es
  copy drafts (user reviews), `Certificate.recognitionType` column naming, completion-doc file paths under
  `src/lib/courses/certificates/`.

### O2 — Phase 14-05: Admin Users UI — verify & fix  `[verify-and-fix; check code first]`

- **Status:** `14-05-PLAN.md` written, **no `14-05-SUMMARY.md`** → not executed per GSD records. It is a
  *verify-and-fix* plan (wave 2, depends on 14-01 which is done), so the underlying users UI may already exist in
  code — **confirm actual code state before filing as net-new work.**
- **Requirements:** ADMIN-USERS-04, ADMIN-USERS-05.
- **Source:** `.planning/phases/14-.../14-05-PLAN.md`.
- **Scope:** verify `useAdminUserDetail` SWR key is `null` when no user selected (no stale fetches); confirm action
  endpoints `PATCH /api/v1/admin/users/{id}/status`, `PATCH .../role`, `POST .../password-reset` + cache mutate +
  toast; confirm all 6 locale wrappers exist (en/ar/es × `/users` and `/users/[userId]`); `selectedUserId` as single
  source of truth for the detail drawer. Acceptance: typecheck + full test suite green.
- **Note:** small, mechanical. Likely a "verify + close" or a tiny fix PR rather than a feature.

### O3 — Course Completion Certificates  `(deferred ex-Phase 2)`

- **Status:** Deferred out of v1.0 before close; re-homed to backlog. **0/2 plans, not started.**
- **Requirements:** COMP-01, COMP-02, COMP-03, COMP-04, COMP-05.
- **Source:** `.planning/ROADMAP.md` → Backlog.
- **Scope:** (1) certificate issuance logic, data model, verification API; (2) PDF generation, dashboard view,
  certificate display page — student auto-receives a downloadable, verifiable PDF on course completion.
- **Cross-link:** **Overlaps O1/CREC-09** (completion document + `Certificate` model + issuance flow). These two
  should be reconciled — likely the same `src/lib/courses/certificates/` domain. Do not file as fully independent.

### O4 — Learning Experience Polish  `(deferred ex-Phase 3)`

- **Status:** Deferred out of v1.0 before close; re-homed to backlog. **0/2 plans, not started.**
- **Requirements:** CURR-01..04, LEARN-01..04.
- **Source:** `.planning/ROADMAP.md` → Backlog.
- **Scope:** (1) curriculum builder drag-and-drop reordering + content feedback; (2) student learning-journey bug
  fixes — resume, persistence, progress bar, navigation.

### O5 — Platform Metrics & Analytics — new phase to plan  `(pending todo)`

- **Status:** Pending GSD todo — needs a `/gsd-plan-phase`. Solution section is TBD.
- **Source:** `.planning/todos/pending/2026-05-04-platform-metrics-analytics-phase.md` (created 2026-05-04).
- **Scope:** consolidated platform-wide metrics/signals/analytics layer across six domains — User Engagement
  (DAU/WAU/MAU; baseline 42 active), Content Performance (49 published courses, per-course enrollment, ratings),
  Subscription Metrics (active subs per plan, free→paid conversion), Financial (MRR/ARR, ZATCA compliance signal),
  Community Engagement (0 published posts = baseline gap), Marketing Effectiveness (campaign perf, acquisition
  attribution, cohort retention). Define metric catalog first; audit DB sources; pick aggregation layer (DB views vs
  service vs Statsig/PostHog); build admin dashboard.
- **Open questions:** unified dashboard vs per-domain views; realtime vs daily-batch; reuse Statsig MCP for product
  analytics or keep separate.
- **Cross-link:** **Overlaps Phase 14 analytics tabs** (D-08/D-09: User Acquisition, Content Performance, Platform
  Engagement, Revenue Analytics on `/admin/views`). Phase 14 shipped the tabbed shell; this todo is the deeper
  instrumentation/metric-catalog layer behind it. Scope to avoid duplicating Phase 14.

---

## Done ledger — shipped (reference / closed-issue history)

Not for filing as open issues. Captured so nothing is lost when `.planning` is archived.

### v1.0 — Instructor Certification  (shipped 2026-03-08, archived 2026-05-12, tag `gsd/v1.0-instructor-certification`)

| Phase | Title | Plans | Requirements | Notes |
| ----- | ----- | ----- | ------------ | ----- |
| 1 | Instructor Certification (e2e) | 2/2 | PHASE1-\* | application → admin queue → approve/reject/revoke → email → profile badge |
| 4 | Enhanced cert form (multi-step + uploads) | 3/3 | PHASE4-\* | AES-256-GCM nationalId, private R2 + 15-min signed URLs, 5-step wizard, localStorage drafts |
| 5 | Gated certification levels | 3/3 | CERT5-\* | VERIFIED→ACADEMIC gating, amber/indigo badges; **no formal VERIFICATION.md** (accepted tech debt) |

### v1.1 — Course Trust & Certification Depth  (in progress; these phases done)

| Phase | Title | Plans | Requirements | Completed |
| ----- | ----- | ----- | ------------ | --------- |
| 6 | Deep Cert Schema — DB Foundation | 2/2 | CSCH-01..05, 07, 08 | 2026-03-10 |
| 7 | Deep Cert Schema — Domain, Migration, UI | 3/3 | CSCH-06, 09, 10 | 2026-05-12 |
| 8 | Course Recognition Type — DB & Domain | 2/2 | CREC-01, 02, 03, 04, 06, 08 | 2026-05-12 (VERIFICATION passed 8/8) |
| 10 | shadcn/ui → HeroUI + primary color tokens | 6/6 | UI-MIG-01..04 | 2026-03-31 |
| 11 | Noon Subscription Webhook Handler | 1/1 | NOON-WEBHOOK-01 | 2026-03-31 |
| 12 | Noon Checkout Metadata Reliability | 2/2 | NOON-META-01..05 | 2026-03-31 |
| 13 | Noon Production Hardening | 6/6 | NOON-HARD-01..09 | 2026-03-31 |
| 14 | Admin Control Plane (users/monetary/analytics/health) | **4/5** | ADMIN-USERS/MON/ANALYTICS/HEALTH-\* | 14-01..04 done; **14-05 → O2** |
| 15 | Embeddings & Recommendations — Foundation | 5/5 | EMBED-01..05 | 2026-04-27 (pgvector embeddings for courses/events/posts) |

### v2-deferred requirements (explicitly out of scope — not issue candidates yet)

- **Recognition type:** CREC-F1 (admin override), CREC-F2 (catalog filter), CREC-F3 (issuer split), CREC-F4 (CPD/CME).
- **Cert schema:** CSCH-F1 (server autosave), CSCH-F2 (reviewer checklist/scores), CSCH-F3 (expiration/renewal),
  CSCH-F4 (3rd-party KYC), CSCH-F5 (reviewer pool), CSCH-F6 (institutional metadata).

---

## When filing GH issues from this note

1. Verify against **live code/main**, not these planning docs (docs are stale — see top warning).
2. Reconcile the **O1 (CREC-09) ↔ O3** completion-certificate overlap and the **O5 ↔ Phase 14 analytics** overlap
   before filing — don't create duplicate/competing issues.
3. O2 is "verify-first" — check the users UI in code before deciding it's open work.
4. Follow the repo issue conventions (experts-beacon: fingerprint, `agent-fp` marker, labels) if filing via routine.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
