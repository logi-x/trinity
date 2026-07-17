---
title: "Noon Checkout Metadata Reliability — outcome"
date: "2026-03-31"
tags: ["project/experts", "topic/noon-checkout-metadata", "outcome"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

# Noon Checkout Metadata Reliability

**Outcome:** Replaced the broken Noon order deep-search metadata extraction with a DB-backed pending-checkout record, so subscription checkout metadata (plan code, billing interval, user, plan) is reliably persisted at intent creation and read back at verification.

## What shipped
- `NoonPendingCheckout` Prisma model in the billing schema: unique `internalReference` key, UUID primary key, `expiresAt` index (24h TTL), and a nullable `checkoutUrl`.
- Persist-before-redirect: `createNoonSubscriptionIntent` writes the pending-checkout row after Noon API success (avoiding orphan rows on API failure).
- Verify route now reads metadata via `prisma.noonPendingCheckout.findUnique({ where: { internalReference } })` instead of deep-searching the Noon order response.
- Distinct 400 responses for "Checkout session not found" vs "Checkout session expired".
- Post-verification cleanup: `deleteMany` by `internalReference` plus a fire-and-forget purge of expired rows; `getNoonOrderByReference` moved after the DB lookup so missing/expired sessions return 400 without hitting the Noon API.

## Key decisions
- `userId` and `planId` stored as plain strings, not FK relations — the record is a transient checkout session, not a relational entity.
- Expired-session cleanup is fire-and-forget (non-awaited `deleteMany().catch()`) to avoid blocking the response.
- Removed the unused `findEnumValue` deep-search helper; retained Noon-native field helpers (`findSubscriptionIdentifier`, `findNumberValue`, `findStringValue`).

## Patterns established
- DB-backed pending checkout: for gateways without merchant-metadata fields, persist metadata keyed by `internalReference` before redirect, read at verify, delete after use.

## Key files
- `prisma/schema.prisma` and `prisma/migrations/20260331212502_phase_12_noon_pending_checkout/migration.sql`
- `src/lib/payments/gateways/noon/noon.gateway.ts`
- `app/api/v1/commerce/subscriptions/checkout/verify/route.ts`

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
