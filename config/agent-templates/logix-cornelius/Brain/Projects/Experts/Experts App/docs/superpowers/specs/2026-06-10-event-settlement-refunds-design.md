---
title: "2026 06 10 event settlement refunds design"
date: "2026-06-10"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/specs/2026-06-10-event-settlement-refunds-design.md"
---
# Event Settlement & Refunds — Design Spec

**Date:** 2026-06-10 (v4 — E-1 realigned to the legal copy shipped by #973; v3 added the second-panel triage, see `docs/superpowers/reviews/spec-review-v2.md`; first round in `…/spec-review-v1.md`)
**Status:** Approved (operator decisions E-1..E-8 confirmed)
**Issue:** #966
**Parent:** #936 instructor settlement system (Plan A #961, Plan B #962) — this is the named "Events phase" follow-on.
**Related:** #965 (subscription refunds — rides the same polymorphic `RefundRequest` model later). #969/#973: the legal-docs-curator's first run rewrote `legal.refundPolicy.liveEvents` (en/ar/es) to the E-1 rule **ahead of this implementation** (intentional agent test); the published copy now matches E-1 exactly. Residual drift: `ask-ai-assistant.ts` facts still state the old 48h rule — fixed in this phase (§7).

## 1. Problem

Events are excluded from the settlement ledger (spec decision D-9): a paid event registration produces **no** `OrderSettlement` and hosts earn nothing in the ledger. The exclusion exists because there is no event refund flow — an event earning, once created, could never be clawed back, so a refunded ticket would still pay the host.

This phase ships the three pieces **together** (shipping any subset reopens the un-clawback-able money hole):

1. An event refund flow (request → approve → process), full parity with courses, plus a minimal attendee surface (E-8).
2. The `"event"` settlement branch (hosts earn via the existing ledger).
3. Settlement clawback wired into the new refund flow via a shared helper.

## 2. Operator decisions (this spec's equivalents of D-1..D-9)

| #   | Decision                   | Choice                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| --- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| E-1 | Refund eligibility         | **Course-style N-day window from `registeredAt`, capped at event start.** Eligible iff: registration `completed` ∧ paid ∧ within window ∧ event (first occurrence per §2.1) has not started. **History:** v2 briefly switched to a 48h-before-start cutoff to match the then-published legal copy; PR #973 (legal-docs-curator) has since shipped the capped-at-start rule to `legal.refundPolicy.liveEvents` in en/ar/es, so code and published policy now agree on this rule.                                                                                      |
| E-2 | Flow scope                 | **Full parity with courses**: attendee request route, admin approve/reject/process, credit note + ZATCA, settlement **and affiliate-commission** clawback, stale-request cleanup.                                                                                                                                                                                                                                                                                                                                                                                    |
| E-3 | Refund data model          | **Polymorphic widening of `RefundRequest`** (not a sibling table): `sourceType` + nullable source FKs. Chosen explicitly to also carry `"subscription"` later (#965).                                                                                                                                                                                                                                                                                                                                                                                                |
| E-4 | Earning maturation         | **`payableAt` = event end (max non-cancelled occurrence `endsAt`) + the standard holding window.** A matured event earning can never need a refund clawback: the refund window closes at event start, maturation begins after event end + window.                                                                                                                                                                                                                                                                                                                    |
| E-5 | Implementation shape       | **Sibling mirroring + one shared extraction** (Approach A): event handlers mirror course handlers; the settlement-clawback block is extracted into one shared helper both call. No generic refund engine (subscription semantics would warp it; refactor+feature mixing forbidden).                                                                                                                                                                                                                                                                                  |
| E-6 | Re-purchase after refund   | **Blocked.** `event-register.handler` currently only blocks `status === "completed"`; a `refunded` registration would re-register via the `(eventId, userId)` upsert, **recycling the same registration id** — the settlement unique `("event", registrationId)` would treat the second purchase as already-settled (host earns nothing) and `commissionAlreadyAttributed` (matches any status) would block re-attribution. The register handler gains a `refunded` guard with a clear error. Re-purchase support (new-row-per-purchase model) is a named follow-on. |
| E-7 | Re-request after rejection | **Strict course parity: one refund request per registration, ever** (plain `@unique registrationId`, any status blocks a second request). The time-bound-window lockout risk after a hasty rejection is accepted; admins own the consequence.                                                                                                                                                                                                                                                                                                                        |
| E-8 | Attendee surface           | **Minimal attendee UI ships in this phase**: a "Request refund" action + request-status display on the attendee's event registration view, gated by an eligibility pre-check (friendly errors; the real check stays at request/process time). Full states + i18n en/ar/es + tests per experts-constellation. Courses remain API-only (out of scope). The legal copy's "submitted to our support team" paragraph becomes stale once this ships — left to the legal-docs-curator's next run (post-ship).                                                               |

### 2.1 Event timing resolution (no `startsAt`/`endsAt` on `Event`)

`Event` has **no** start/end columns — timing lives entirely in `EventOccurrence` rows. All timing reads in this phase use:

- `eventStart` = **min `startsAt` over non-`cancelled` occurrences**.
- `eventEnd` = **max `endsAt` over non-`cancelled` occurrences**.
- **Zero usable occurrences** (none, or all cancelled):
    - _Refund eligibility:_ there is no scheduled start, so the not-yet-started gate **passes**; the window-from-registration gate alone decides.
    - _Settlement writer:_ **skip recording** with a `settlement.event.no_occurrence` warn observation (no settlement = no maturation-invariant breach). The reconcile sweep picks the registration up once a usable occurrence exists.
- **`payableAt` is a snapshot at settlement time and is immutable.** If occurrences are rescheduled after recording, `payableAt` is not recomputed (mirrors course behavior; a reschedule-to-later event can theoretically mature an earning before the event ends — accepted as a rare, admin-visible edge; payouts remain admin-processed).

## 3. Data model

### 3.1 `RefundRequest` widening (billing schema, live table — additive migration)

```prisma
model RefundRequest {
    id             String             @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
    sourceType     String             @default("course") @map("source_type") @db.VarChar(20) // "course" | "event" (later "subscription")
    enrollmentId   String?            @unique @map("enrollment_id") @db.Uuid    // nullable now
    registrationId String?            @unique @map("registration_id") @db.Uuid  // NEW
    userId         String             @map("user_id") @db.Uuid
    reason         String?
    status         RefundStatus       @default(requested)
    requestedAt    DateTime           @default(now()) @map("requested_at") @db.Timestamptz(6)
    resolvedAt     DateTime?          @map("resolved_at") @db.Timestamptz(6)
    enrollment     CourseEnrollment?  @relation(fields: [enrollmentId], references: [id], onDelete: Cascade)
    registration   EventRegistration? @relation(fields: [registrationId], references: [id], onDelete: Cascade)
    user           User               @relation(fields: [userId], references: [id], onDelete: Cascade)

    @@index([userId])
    @@index([status])
    @@index([sourceType, status])
    @@map("refund_requests")
    @@schema("billing")
}
```

- Nullable `@unique` columns are correct under Postgres (NULLs are distinct): every course row has `registrationId NULL`, every event row has `enrollmentId NULL`, and per-source one-request-ever uniqueness (E-7) holds. The migration includes the explicit `ALTER COLUMN enrollment_id DROP NOT NULL`.
- The cross-schema FK (`billing.refund_requests` → `public.event_registrations`) follows the existing `enrollment_id` → `public.course_enrollments` precedent.
- `EventRegistration` gains the **inverse relation** (`refundRequest RefundRequest?`); `pnpm db:generate` + Prisma validation are explicit steps in the sequence.
- Migration backfills `source_type = 'course'` for all existing rows (the column default makes this implicit; an explicit `UPDATE` documents it).
- **Exactly-one-source is enforced in app code** (every create sets exactly one FK matching `sourceType`); a DB CHECK constraint is drift-invisible to the Prisma gate, so it is not relied upon. Both unique constraints stay real FKs — no orphanable polymorphic ids.
- Existing course queries keep working unchanged: they filter by `enrollmentId`, which is unique and non-null on every course row.

### 3.2 No other schema changes

`OrderSettlement`, `CreatorEarning`, `CreatorPayout` carry events as-is (`sourceType "event"`, `sourceId = EventRegistration.id`, `itemType "event"`, `itemId = eventId`). The payout system needs zero changes. E-6's block keeps `sourceId = registrationId` collision-free (one paid lifecycle per registration row).

## 4. Event refund flow (mirrors courses, file-for-file)

| Course file (template)                                            | Event sibling                                                                                                            |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `course-enrollment-refund-request.handler` (attendee)             | `event-registration-refund-request.handler`                                                                              |
| `…-refund-approve.handler` / `…-refund-reject.handler`            | event siblings                                                                                                           |
| `…-refund-process.handler` (credit note + ZATCA + clawback)       | `event-registration-refund-process.handler`                                                                              |
| `…-refund-cleanup.handler` (stale auto-reject)                    | shared — the existing table-wide cleanup covers both source types with the same staleness window (confirmed intentional) |
| `refund-policy.ts` (`withinRefundWindow`, `MAX_PROGRESS_PERCENT`) | `event-refund-policy.ts` (pure: window-from-registration ∧ not-yet-started gate)                                         |

**Eligibility (E-1):** registration `completed` ∧ `amountPaid > 0` ∧ `withinRefundWindow(registeredAt)` (same window constant as courses) ∧ `requestedAt < eventStart` (occurrence resolution per §2.1).

**Snapshot-at-request rule (EXP-129 house pattern):** the **time gates** (window + start cutoff) are evaluated against `requestedAt`, not the processing moment — a timely request never expires while waiting on an admin (the course handler's process-time `withinRefundWindow(enrolledAt)` re-check would otherwise make the hard event deadline a slow-admin trap). **State gates** (registration still `completed`, paid, not already refunded) are re-checked against current state at process time. Course handlers keep their existing behavior (out of scope).

**Course-only gates that do not translate:** `progress ≤ MAX_PROGRESS_PERCENT` and the certificate check have no event analog and are intentionally absent. The published policy's platform-credit alternative remains **admin discretion in v1** (no wallet exists), documented so the omission is deliberate. The #973 copy already drops attendance-based denial in favor of the hard started-event cutoff, which the code enforces directly.

**Invoice correlation:** `Invoice` persists `(contentType: "event", contentId: eventId)` — **`contentId` is the event id, not the registration id, and `occurrenceId` is not stored on the invoice**. The event handler mirrors the course lookup exactly: `invoice.findFirst({userId, contentType: "event", contentId: eventId}, orderBy: {createdAt: "desc"})`. The latest-invoice heuristic has the same re-purchase ambiguity courses already have — and E-6's block removes the event re-purchase case entirely.

**Terminal status:** processing sets `EventRegistration.status = "refunded"` (the enum value exists; event revenue stats and the spot/capacity `_count` filter (`status: "completed"`) already handle it — a refunded registration automatically frees its seat) — **not** `cancelled`.

**Process transaction** (interactive, mirroring the course handler post-#962): credit note exists/created outside, then ONE `$transaction`: settlement snapshot read → shared settlement clawback (§5) → **affiliate-commission clawback** (§5.1) → registration `completed → refunded` → refund request `processed` → observe with `cancelledEarnings`/`cancelledCommissions`/`platformLossAmount`.

**Notifications:** the course refund flow sends **no** user-facing notifications today (the email/chat registries have zero refund keys; handlers only `observe()`). Parity therefore ships events without notifications — a **deliberate deferral**, named follow-on: refund lifecycle notifications for courses + events together (notify() requires entries in BOTH email and chat registries per house rule).

## 5. Shared settlement clawback (the one extraction)

Extract the #962 clawback block from `course-enrollment-refund-process.handler.ts` into:

```
src/lib/settlement/clawback-settlement.ts
  clawbackSettlementForSource(tx, {sourceType, sourceId, adminUserId, refundRequestId})
    → {cancelledEarnings, platformLossAmount}
```

Behavior (verbatim from the course handler, parameterized by source):

1. Settlement lookup by the `(sourceType, sourceId)` unique; `NO_MATCH_UUID` fallback (flag-off-era sales are safe no-ops).
2. Sum already-`paid` lines → `platformLossAmount` (finance signal; paid earnings are never clawed — Tier-2 policy).
3. Cancel in-flight payouts linked to the to-be-cancelled earnings (status-guarded `pending/processing` cancel, then **unlink only payouts actually cancelled** — the #962 refund-vs-complete race guard), `notes: refund_cancellation:<requestId>`, `processedBy: adminUserId`.
4. Cancel `pending/approved` earnings keyed on the settlement; reverse the settlement (`recorded → reversed`).

The helper lives in `src/lib/settlement/` and imports **no** course/event domain code (dependency direction: domains → settlement lib). The course handler refactors to call this helper — behavior-identical, proven by its existing 12-test suite passing unchanged. The event process handler calls it with `("event", registrationId)`.

### 5.1 Affiliate-commission clawback (event mirror of #916)

Event purchases create affiliate commissions (`event-registration-complete.handler.ts`), so the event process handler must mirror the course handler's in-tx commission clawback: cancel `pending/approved` commissions keyed by `(userId: buyer, itemType: "event", itemId: eventId)`. Paid commissions are not clawed (same policy).

**Hold-window fix:** `calculateHoldUntil` currently holds event commissions only **3 days**, while the E-1 refund window stays open until event start — a commission could mature and pay out while still refundable. Fix in this phase: event commission `holdUntil = max(createdAt + 3d, eventStart)`. Mechanics: `handleAffiliateAttribution`'s input does not carry the event start — thread an optional `eventStartsAt` through `input.source` from the registration-completion context (which already queries the earliest occurrence) with a DB-lookup fallback inside the helper; when no occurrence exists, fall back to the current 3-day hold. **`referral.expiresAt`** (same helper's other call site) keeps its current semantics — it is click-attribution expiry, not refund exposure; unchanged. Courses unchanged.

## 6. Settlement writer — the `"event"` branch

- `SettlementSourceType = "course" | "event" | "subscription"`.
- `resolveEventFacts(registrationId)`: `EventRegistration` (`status === "completed"`, `amountPaid > 0` — same gates as courses) → `Event` + `hosts` (`EventHost.userId/role/revenueShare`) → `resolveContributorShares(hosts, "host")` (`HostRole` primary value is `"host"`, NOT the course `"primary"` — passing the wrong role makes every single-host event fire the fallback warn; the existing resolver + partial-null fallback-to-primary semantics, warn observation included).
- Money math: the existing `priceOrder` with the same default split/gateway constants; instructor-funded affiliate via the existing `commission.findFirst({itemType: "event", itemId: eventId, status notIn cancelled/paid})`.
- **`payableAt` (E-4):** `calculateEventPayableDate(occurrences) = eventEnd (§2.1) + standard holding window` — pure helper beside the course one; the occurrence query must select `endsAt` explicitly (the completion handler's existing occurrence select fetches `startsAt` only). Zero usable occurrences → skip recording (§2.1). Snapshot-immutable per §2.1.
- Inline fault-isolated call in the event registration completion path after the ZATCA enqueue (same try/observe shape as courses/subscriptions); idempotent + P2002-as-success; flag-gated.
- Reconcile sweep gains a third bounded anti-join over `public.event_registrations` (`status='completed' AND amount_paid>0`, `NOT EXISTS` settlement with `source_type='event'`); the single `limit` budget is **split fairly** (⌊limit/3⌋ per source, spillover in order) instead of course-first starvation.
- **Rollout posture:** events ride the existing `SETTLEMENT_LEDGER_ENABLED` flag — no event-specific sub-flag. The prod flag is still **off**; the existing D-8 go-live decision (including the historical-backfill question and the cron-sidecar wiring of the reconcile/mature/stats routes, which is still missing from `docker/production/docker-compose.yml`) now explicitly covers historical completed event registrations too. On dev (flag on) events start settling at deploy, which is desired. The settlement seeder (`prisma/seeders/20-settlements.ts`, merged) gains the event branch so dev data exercises it.

## 7. Surfaces

- **Attendee (E-8):** request-refund route mirroring the course request route (session-only identity, eligibility pre-check for a friendly error, real check at request/process), PLUS the minimal UI: "Request refund" action + status display on the attendee's event registration view, eligibility-aware, full loading/empty/error states, en/ar/es, RTL, tests — per experts-constellation.
- **Admin refund routes:** the existing `/api/v1/admin/refunds/[id]/{approve,reject,process}` routes currently call course handlers directly, and course handlers assume non-null `enrollmentId`. Each route loads the request and **dispatches by `sourceType`** to the course or event handler; course handlers keep their non-null assumption.
- **Admin refunds queue:** the query/DTO move out of `src/lib/courses/enrollments/` into a **neutral billing/refunds module**, with a **discriminated DTO**: shared fields + `sourceType` + nullable course block (`enrollment`/course title/progress) + nullable event block (registration/event title/start). Two traps the move must clear: (a) the current `baseWhere` filters `enrollment.course.publishingStatus = "published"` — a course-shaped relation filter that would silently hide every event row; the widened query applies it to course rows only; (b) the admin triage badge counts ALL `status:"requested"` rows — the list must show event rows or the badge never clears. The table renders a source chip and per-source columns; course rows render exactly as today.
- **AI assistant facts:** `ask-ai-assistant.ts` refund-policy facts still state the superseded 48h rule (#973 missed it) — update the event fact line to the E-1 rule in this phase.
- **Creator/admin payout surfaces:** untouched — event earnings appear automatically (the earnings table already renders `itemType`).
- i18n: en/ar/es for every new string; RTL per house rules.

## 8. Out of scope (named follow-ons)

- **Re-purchase after refund** (E-6) — requires the new-row-per-purchase registration model (drop the `(eventId, userId)` unique); also unblocks re-attribution (`commissionAlreadyAttributed` matches any status today, including `cancelled`).
- **Bulk event-cancellation refunds** ("event cancelled → refund all registrations") — per-registration refunds work today; bulk is an admin convenience layered on the same process handler. Re-evaluation trigger: the first post-launch host cancellation needing attendee refunds.
- **Subscription refunds** — #965 (rides `sourceType: "subscription"` on the widened table).
- **Refund lifecycle notifications** (courses + events together; notify() dual-registry rule).
- **Clawback of already-`paid` earnings/commissions** — platform-loss signal only, same policy as courses/affiliates.
- **Platform-credit refunds** — admin discretion in v1 (§4); no wallet model exists.
- **Credit-note idempotency hardening** — `CreditNote.invoiceId` is not unique and the existence check sits outside the transaction (course parity); a double-process race could duplicate a credit note on courses today too. File as a separate cross-source hardening issue rather than fixing one side here.
- **Legal copy "submitted to support" paragraph refresh** once E-8's self-serve UI ships — legal-docs-curator's next run.

## 9. Testing

- `event-refund-policy.ts` eligibility matrix as pure-function tests (window edges, start-cutoff edges, snapshot-at-request semantics, started event, multi-occurrence + cancelled-occurrence + zero-occurrence resolution).
- Each handler: vitest node-env mocked-prisma suites mirroring the course refund suites (including the interactive-`$transaction` mock shape and the concurrently-completed-payout double-pay guard test).
- `clawback-settlement.ts` tested once directly; the course handler's existing suite passes unchanged post-refactor (the behavior-preservation proof).
- Writer: event-branch tests mirroring the course ones (single host with `"host"` primary role and NO fallback warn, multi-host split, partial-null fallback, P2002, payableAt anchored after event end, zero-occurrence skip).
- E-6 guard: register-after-refund returns the block error; settlement/commission keys never see a recycled registration.
- **Regression:** course and subscription writer suites re-run against the widened `recordOrderSettlement` (not just new event tests); reconcile fairness test (budget split).
- **Concurrency:** double-process guard, payout-complete-vs-refund race (existing pattern), reconcile-vs-refund overlap.
- Migration: DB-free diff + `db:check:drift`; a test asserting existing course refund queries still match (enrollmentId non-null path).

## 10. Sequencing

Single PR (one cycle, same shape as Plan B): schema widening + inverse relation + `db:generate` → policy + writer branch → shared clawback extraction (course refactor) → event refund handlers/routes (incl. E-6 register guard, commission clawback + holdUntil fix) → admin route dispatch + neutral query/DTO move → reconcile + inline wire → surfaces (admin queue + attendee UI + AI-fact line) → seeder event branch → reviewer panel → ship with `Closes #966`. Flag posture per §6 — prod flag remains off; legal copy already matches E-1 via #973.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
