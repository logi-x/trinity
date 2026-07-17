---
title: "Newsletter Plan"
date: "2026-05-07"
tags: [plan, project/experts]
category: "plan"
---

# Newsletter Subscription Branch Plan

## Summary

Create branch `codex/newsletter-subscription` from the current `main` checkout and add a production-ready newsletter capture flow for `apps/experts-app`: public footer form, persisted subscriber records, duplicate-safe resubscribe behavior, and a real unsubscribe page/API.

## Key Changes

- Add Prisma persistence in the `public` schema:
  - `NewsletterSubscription` model with `id`, lowercased unique `email`, `status`, `locale`, `source`, `subscribedAt`, `unsubscribedAt`, request metadata, and timestamps.
  - `NewsletterSubscriptionStatus` enum: `subscribed`, `unsubscribed`.
  - Add a Prisma migration and regenerate the client.
- Add newsletter domain code under `src/lib/newsletter/`:
  - Zod schemas for subscribe/unsubscribe payloads.
  - Handler for subscribe: validate email, normalize lowercase, create or resubscribe existing records, update locale/source/metadata.
  - Handler for unsubscribe: verify signed email token, mark matching subscription as `unsubscribed`, set `unsubscribedAt`.
  - Utility for HMAC-signed unsubscribe links using the app secret, so users cannot unsubscribe arbitrary addresses by guessing URLs.
- Add public API routes:
  - `POST /api/v1/newsletter/subscribe` with `{email, locale?, source?}` returning `{success, status}` where status is `subscribed`, `alreadySubscribed`, or `resubscribed`.
  - `POST /api/v1/newsletter/unsubscribe` with `{email, token}` returning `{success: true}` even when already unsubscribed.
- Add UI:
  - Shared client component `NewsletterSignupForm` using existing Tailwind/HeroUI patterns and localized copy.
  - Wire it into the public/footer variants currently represented by `FooterV2`, `CompanyFooter`, and `CreatorFooter`.
  - Add localized unsubscribe page at `/en/newsletter/unsubscribe`, `/ar/newsletter/unsubscribe`, and `/es/newsletter/unsubscribe` via shared i18n route implementation.
  - Update `EmailFooter` unsubscribe links to point to `/en/newsletter/unsubscribe?email=...&token=...` using the signed token utility.
- Add i18n messages in `en`, `ar`, and `es` for success, duplicate, validation, loading, failure, and unsubscribe states.

## Required Safety Step

Before editing any existing function/class/method, run GitNexus impact analysis for the target symbol, report the blast radius, and stop for user confirmation if risk is HIGH or CRITICAL. Before commit, run GitNexus change detection to confirm only expected newsletter/footer flows changed.

## Test Plan

- Unit tests for newsletter schemas, email normalization, subscribe/resubscribe behavior, and signed unsubscribe token verification.
- Route tests or focused integration tests for:
  - invalid email returns 400,
  - new email subscribes,
  - duplicate subscribed email returns duplicate-safe success,
  - unsubscribed email can resubscribe,
  - invalid unsubscribe token is rejected,
  - valid unsubscribe marks the record unsubscribed.
- Touched-file typecheck with `pnpm typecheck:touched -- <changed files>`.
- Final app checks before commit: `pnpm test` and `pnpm typecheck`.

## Assumptions

- No external email provider sync in this branch.
- No admin subscriber management/export UI in this branch.
- The branch will be created from the current `main` checkout as `codex/newsletter-subscription`.
- Newsletter data belongs in the `public` schema, not `billing` or `seq`.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
