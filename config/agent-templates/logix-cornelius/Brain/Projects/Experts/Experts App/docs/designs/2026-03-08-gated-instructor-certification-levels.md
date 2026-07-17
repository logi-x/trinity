---
title: "Gated Instructor Certification Levels — outcome"
date: "2026-03-08"
tags: ["project/experts", "topic/gated-certification-levels", "outcome"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

# Gated Instructor Certification Levels

**Outcome:** Delivered a two-tier (VERIFIED / ACADEMIC) instructor certification system with gate enforcement, a 4-step VERIFIED wizard, a 2-step ACADEMIC wizard, dual-level profile badges, and a full admin view including a Certified Instructors tab with revoke action.

## What shipped
- DB migration renaming `PERFORMANCE` enum value to `VERIFIED` in `CertificationType`
- `VerifiedApplicationSchema` and `AcademicApplicationSchema` (type-discriminated Zod schemas)
- `handleVerifiedApplicationSubmit` — instructor gate (`isInstructor` column check, not roles array)
- `handleCertificationSubmit-academic` — VERIFIED CERTIFIED gate (403 `VERIFIED_REQUIRED` if not satisfied)
- `getCertificationQueue` updated to side-load `verifiedCertData` for ACADEMIC queue items in one extra `findMany`
- `POST /api/v1/certifications` dispatches by `body.type` (VERIFIED or ACADEMIC)
- `GET /api/v1/certifications` returns `{ verified: DTO|null, academic: DTO|null }`
- `UserProfile.certificationLevel: "VERIFIED" | "ACADEMIC" | null` (ACADEMIC wins) on public profile API
- `useCertification` hook shape changed from `{ certification }` to `{ verified, academic }`
- `LevelOverview` component — 3-card layout with framer-motion stagger, state-driven CTAs, L3 Academic card grayed/locked when VERIFIED not CERTIFIED
- `CertificationsPageClient` — URL-driven view switching (`?apply=verified` / `?apply=academic`) with client-side route guards (`router.replace(pathname)` when ineligible)
- `VerifiedApplicationClient` — 4-step wizard (BasicInfo, Credentials/Education, WorkExperience, ProofOfExpertise) with work history entries, 6-type proof type Select dropdown, Description helper text, per-step Zod validation, localStorage draft v1
- `AcademicApplicationClient` — 2-step wizard (Credentials & Education + Agreements) with VERIFIED gate error handling
- Profile badge renders amber for VERIFIED CERTIFIED, indigo for ACADEMIC CERTIFIED
- Admin queue Type column with chip colors (amber=Verified, indigo=Academic); combined L2/L3 Application Data modal
- Admin Certified Instructors tab (`?tab=certified`) — `GET /api/v1/admin/certifications/certified`, `getCertifiedInstructors` query, `useCertifiedInstructors` hook, `AdminCertificationsNav` tab component, revoke action
- `getLevelOverviewState` pure helper for testable state derivation
- i18n keys in en/ar/es: `levelOverview.*`, `certifiedInstructors.*`, `errors.verifiedRequired`, `wizard.verifiedTitle/academicTitle`

## Key decisions
- ACADEMIC takes priority over VERIFIED when computing `certificationLevel` (ACADEMIC > VERIFIED)
- `POST /api/v1/certifications` dispatches by `body.type` (not union schema) — clearer per-type error messages
- Gate check uses `prisma.user.findUnique({ select: { isInstructor: true } })` — handlers are auth-agnostic
- URL-driven view switching chosen over local `useState` — enables deep-linking and browser back/forward navigation
- Admin certified instructors implemented as a tab on existing `admin/certifications` page (not a new route) to avoid locale wrapper duplication
- Old `certification-submit.handler.ts` retained through phase 5 for backward compat; cleaned up after wizards verified
- `Prisma.JsonNull` used for nullable JSON `applicationData` field
- Legacy draft key `certifications.application.draft.v2` cleared on verified wizard mount

## Patterns established
- Type-discriminated dispatch: `if (body.type === X)` branch to dedicated handler
- Two-level gate: VERIFIED for any instructor, ACADEMIC requires VERIFIED CERTIFIED
- Queue side-load: collect target userIds from main query, batch-fetch related records, build lookup map
- `getLevelOverviewState` pure function extracting display flags for unit testing
- Per-step validation: only current step schema `.safeParse()` runs before advancing
- `buildVerifiedSubmitPayload` pure helper maps wizard state → API payload shape (each proof discriminant maps correctly)
- Admin view tabs: URL `searchParam` (`tab=certified`) for server-side tab selection, enabling SSR and deep-linking

## Key files
- `prisma/migrations/20260307094558_verified_enum_rename/migration.sql`
- `src/lib/certifications/handlers/certification-submit-verified.handler.ts`
- `src/lib/certifications/handlers/certification-submit-academic.handler.ts`
- `src/lib/certifications/queries/certification-queue.query.ts`
- `src/lib/certifications/queries/certified-instructors.query.ts`
- `src/lib/user/profile/dto/profile.dto.ts` (certificationLevel)
- `src/lib/user/profile/dto/profile.mapper.ts` (mapCertificationLevel)
- `src/hooks/use-certification.ts`
- `app/api/v1/certifications/route.ts`
- `app/api/v1/admin/certifications/certified/route.ts`
- `app/(i18n)/_shared/(user)/certifications/_components/level-overview.tsx`
- `app/(i18n)/_shared/(user)/certifications/_components/certifications-page-client.tsx`
- `app/(i18n)/_shared/(user)/certifications/_components/verified-application-client.tsx`
- `app/(i18n)/_shared/(user)/certifications/_components/academic-application-client.tsx`
- `app/(i18n)/_shared/admin/certifications/_components/certifications-queue-client.tsx`
- `app/(i18n)/_shared/admin/certifications/_components/certified-instructors-client.tsx`
- `app/(i18n)/_shared/admin/certifications/_components/admin-certifications-nav.tsx`
- `src/components/profile/profile-header.tsx`
