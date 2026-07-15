---
title: "Experts event pricing sync"
date: "2026-04-14"
project: "Experts App"
source: "codex session"
tags: ["project/experts", "creator", "events", "pricing", "affiliate", "coupon"]
---

# Summary

Aligned `/creator/events` pricing conditions with the existing `/creator/courses` behavior.

## Changes made

- Updated `src/lib/events/forms/sections/event-pricing-section.tsx` so event pricing matches course pricing rules.
- Paid event price input now only shows when the event is not free and respects the same published/promotion lock state.
- Affiliate promotion controls now only appear when price is above `MINIMUM_ALLOWED_AFFILIATE_COMMISSION_AMOUNT`.
- Coupon controls now only appear after an affiliate commission cap exists and the event price is above the same threshold.
- When event price drops below the affiliate/coupon threshold, the form clears affiliate and coupon fields to avoid stale hidden state.
- Updated `src/lib/events/forms/event.schema.ts` so paid events require a positive price and free events require zero.
- Updated event create-page upgrade CTA to use `/pricing` to match the course create flow.

## Verification

- `pnpm exec prettier --check` passed for touched files.
- Repo `pnpm typecheck` currently fails because of pre-existing unrelated lint errors elsewhere in the app, including `app/(i18n)/_shared/admin/views/page.tsx`.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
