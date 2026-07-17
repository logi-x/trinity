---
title: "2026 06 23 admin manual subscription grant design"
date: "2026-06-23"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/specs/2026-06-23-admin-manual-subscription-grant-design.md"
---
# Admin Manual Subscription Grant ("bypass") — Design

**Date:** 2026-06-23
**Status:** Approved (brainstorming)
**Surface:** `apps/experts-app`

## Problem

Admins need to assign a user to a subscription plan **directly, without payment**. Running such
grants through the normal paid checkout path (`subscription-checkout-complete.handler.ts`) is wrong:
it emits an invoice, a ZATCA e-invoice, a settlement-ledger entry, and (potentially) affiliate
attribution. For a comp / staff / partnership grant there was no money movement, so those artifacts
are **misleading financial records**.

We want a clean, auditable path that creates only the access-granting `Subscription` row.

## Why a manual grant is sufficient

Plan entitlements are resolved from the user's **active** `Subscription → Plan` relation
(provider-agnostic — see `subscriptions/queries/get-active-subscription.ts`). Creating an `active`
subscription row with `provider: "manual"` immediately confers the plan's entitlements without
touching any billing artifact. The `PaymentProvider` enum already has a `manual` value, so **no enum
migration** is required.

## Decisions (from brainstorming)

- **Duration:** admin chooses an end date, or "no expiry" (`endsAt = null` = perpetual until revoked).
- **Surface:** admin user-detail page action + a new admin API route.
- **Audit:** persist `grantedBy` (admin userId) + free-text `reason`.
- **Isolation:** implemented in a dedicated git worktree.

## Schema (additive migration)

Add to `model Subscription` (`prisma/schema.prisma`, `billing` schema):

```prisma
grantedById String? @map("granted_by_id") @db.Uuid
grantReason String? @map("grant_reason")
grantedBy   User?   @relation("SubscriptionGrantedBy", fields: [grantedById], references: [id], onDelete: SetNull)
```

Back-relation on `model User`:

```prisma
grantedSubscriptions Subscription[] @relation("SubscriptionGrantedBy")
```

Both new columns are nullable → additive, low-risk migration via `pnpm db:migrate`. Hand-edit the
model block (never `prisma format`); re-check schema indentation after `db:generate`.

## Domain (`src/lib/subscriptions/`)

- `commands/subscription-grant.schema.ts` — Zod: `{ planId: uuid, endsAt: ISO datetime | null, reason: string (min 3) }`.
- `commands/subscription-grant.command.ts` — command type: `{ requestId, userId, grantedById, planId, endsAt, reason }`.
- `handlers/subscription-grant.handler.ts`, in one `prisma.$transaction`:
    1. Verify plan exists and `isActive`; verify target user exists. (Structured `{ error, status }` on failure.)
    2. Cancel the user's other `active` subscriptions (reuse the upgrade-cleanup shape:
       `status: "canceled"`, `endsAt: now`, `cancelAtPeriodEnd: false`).
    3. Create the manual row: `provider: "manual"`, unique `providerRef` (`manual:{userId}:{Date.now()}`),
       `status: "active"`, `startedAt`/`currentPeriodStart` = now, `currentPeriodEnd`/`endsAt` = chosen
       (nullable), `grantedById`, `grantReason`. **No** affiliate, invoice, ZATCA, or settlement calls.
    4. `observe("subscription.manual.granted", …)`.
- `mappers/` → `AdminGrantedSubscriptionDTO` (camelCase).

## API

`POST app/api/v1/admin/users/[userId]/subscription/route.ts`:
`requireAdmin()`, `assertUUID(userId)`, parse + Zod-validate body, take `grantedById` from the
session, call the handler, map `{ error, status }` → HTTP, `safeErrorJson` in catch. Follows the
established admin-route conventions (mirrors `admin/users/[userId]/role/route.ts`).

## Frontend

On the admin user-detail surface: a **"Grant subscription"** action opening a HeroUI v3 dialog —
plan select (from `list-plans`), end-date picker with a "no expiry" toggle, reason textarea. POSTs,
then `mutate()`s the relevant keys. RTL-first, `en`/`ar`/`es` strings, loading/empty/error/success
states per the experts-constellation playbook.

## Tests

Handler unit test (vitest **node** env, mocked Prisma):

- creates a `manual`, `active` row with `grantedById` + `grantReason`;
- cancels prior `active` subscriptions for the user;
- does **not** invoke invoice / ZATCA / settlement / affiliate helpers;
- rejects unknown / inactive plan and unknown user with the right status.

## Out of scope (YAGNI)

- Revocation UI (existing `subscription-cancel-active` handler already cancels).
- Recurring auto-renewal of comps.
- Bulk grants.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
