---
title: "Noon Production Hardening — outcome"
date: "2026-04-03"
tags: ["project/experts", "topic/noon-production-hardening", "outcome"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

# Noon Production Hardening

**Outcome:** Hardened the Noon subscription flow for production with checkout-URL reuse, a reconciliation system (handler, routes, daily cron, audit log), self-service cancel/reconcile routes, resilient 3DS-timeout UX, and a full admin payments operations workspace.

## What shipped
- Checkout reuse: added `checkoutUrl` to `NoonPendingCheckout`; the gateway reuses an unexpired checkout URL for the same user/plan/interval instead of creating duplicate Noon sessions; stale/cancelled checkout rows are discarded and replaced.
- Reconciliation layer: command, Zod schema, and handler using Noon as source of truth; supports `admin`, `batch`, `billing_view`, and `webhook_failure` sources; reconciliation audit rows stored in `billing.webhook_events` with `reconciliation:` eventId prefix and `reconciliation_no_change` / `reconciliation_corrected` results.
- Self-service routes: `/api/v1/commerce/subscriptions/cancel` (cancel-at-period-end) and `/reconcile` (billing-view), both resolving the user's active Noon subscription server-side; failed Noon webhooks trigger best-effort `webhook_failure` reconciliation.
- Admin payments backend: query/route surface for failed webhooks, stuck checkouts, active subscriptions, reconciliation log, single + dual-auth batch reconcile (`requireAdmin` or Bearer `CRON_SECRET`), plus a daily Vercel cron for batch reconcile.
- Admin payments UI: shared `/admin/payments` page with four operational tabs (failed webhooks, stuck checkouts with cleanup action, active subscriptions with per-row Sync Now reconcile, reconciliation log); localized en/ar/es wrappers, noindex metadata, and an admin-dashboard quick-action link.
- User billing UX: silent background reconcile for active paid subscriptions, cancel-at-period-end confirmation modal with refresh, and a dedicated amber 3DS-timeout state (polls 3s × 40) instead of a false cancellation; en/ar/es billing + pricing copy.
- Wave-0 backend tests for cancel, reconcile auditing, and duplicate-checkout reuse.

## Key decisions
- Checkout reuse scoped to matching `userId` + `planId` + `billingInterval` to prevent cross-plan checkout leakage.
- `WebhookEvent` doubles as the reconciliation audit log via an explicit naming contract; failed-webhook views exclude reconciliation rows by eventId and result so audits don't pollute the operations view.
- Cancel/reconcile routes tie to the authenticated user's active subscription rather than trusting a client-provided `subscriptionId`.
- Webhook-failure reconciliation is best-effort and non-blocking, with observability on both triggered and failed attempts.
- Provider typing widened from `"stripe"`-only to `PaymentProvider` across create/renew commands.
- Reconciliation correction limited to fields Noon can authoritatively supply (status and meaningful provider dates).

## Patterns established
- Route-safe Zod schemas for reconciliation commands; reconciliation handlers return structured objects, not HTTP responses.
- Self-service subscription routes: authenticate first, validate lightweight payload, then load the active Noon subscription through a query.
- Admin payment routes delegate to query/handler files (auth → Zod → query/handler), exposing focused JSON envelopes.
- Operational admin tabs share a HeroUI pattern: Card shell, Tabs, Table, EmptyState, action buttons with targeted `mutate` refreshes.
- User-facing Noon flows prefer explicit degraded-state UX over generic failure copy.

## Key files
- Reconciliation: `src/lib/subscriptions/commands/subscription-reconcile.{command,schema}.ts`, `src/lib/subscriptions/handlers/subscription-reconcile.handler.ts`
- Self-service: `app/api/v1/commerce/subscriptions/{cancel,reconcile}/route.ts`, `src/lib/subscriptions/queries/get-active-noon-subscription.query.ts`
- Admin backend: `src/lib/payments/queries/get-{failed-noon-webhooks,stuck-noon-checkouts,admin-noon-subscriptions,noon-reconciliation-log}.query.ts`, `app/api/v1/admin/payments/**`, `vercel.json`
- Admin UI: `app/(i18n)/_shared/admin/payments/**`, locale wrappers under `app/(i18n)/{en,ar,es}/admin/payments/`, `src/lib/metadata/admin-payments-metadata.ts`
- User UX: `app/(i18n)/_shared/payment/status/page.tsx`, `app/(i18n)/_shared/(user)/settings/billing/page.tsx`
- Schema: `src/lib/payments/gateways/noon/noon.gateway.ts`, migration `20260403014646_add_checkout_url_to_noon_pending_checkout`

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
