---
title: "Experts company profile web page"
date: "2026-05-01"
source: "codex-session"
tags: ["project/experts", "company-profile", "i18n", "marketing-site"]
---

## Summary

Implemented a localized `/company-profile` marketing/company profile page in `apps/experts-app`.

## Decisions

- Build the company profile as a real Next.js page, not only as static slide/PDF guidance.
- Keep public copy investor/partner-facing and avoid implementation-stack details.
- Emphasize platform value, learner/expert audiences, commerce/payment readiness, RTL/LTR support, and Saudi/Gulf regional readiness.
- Support Arabic, English, and Spanish because the app message loader expects complete locale coverage.

## Implementation Notes

- Shared implementation: `apps/experts-app/app/(i18n)/_shared/company-profile/page.tsx`.
- Locale wrappers:
  - `apps/experts-app/app/(i18n)/ar/company-profile/page.tsx`
  - `apps/experts-app/app/(i18n)/en/company-profile/page.tsx`
  - `apps/experts-app/app/(i18n)/es/company-profile/page.tsx`
- Translation namespace: `companyProfile`.
- Added `companyProfile` to `src/i18n/request.ts`.

## Verification

- Focused ESLint passed.
- `pnpm typecheck:touched` passed for touched TypeScript files.
- Local Next dev requests returned HTTP 200 for:
  - `/en/company-profile`
  - `/ar/company-profile`
  - `/es/company-profile`

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
