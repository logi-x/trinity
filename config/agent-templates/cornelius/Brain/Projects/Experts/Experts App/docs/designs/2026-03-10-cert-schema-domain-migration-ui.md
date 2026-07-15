---
title: "Cert Schema Domain Migration and UI — outcome"
date: "2026-03-10"
tags: ["project/experts", "topic/cert-schema-migration", "outcome"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

# Cert Schema Domain Migration and UI

**Outcome:** Added the `RESUBMITTED` status to the certification lifecycle, created a backfill seeder migrating legacy certified/pending rows to the new deep schema models, established the `getInstructorCertificationLevel()` abstraction, and delivered checkpoint tests for the NEEDS_INFO flow.

## What shipped
- `RESUBMITTED` added to `CertificationApplicationStatus` enum via migration (`ALTER TYPE ADD VALUE 'RESUBMITTED'`) — placed after `NEEDS_INFO` in logical status flow: SUBMITTED → NEEDS_INFO → RESUBMITTED → APPROVED/REJECTED
- Migration `20260310064259_phase_7_add_resubmitted_status` applied; Prisma client regenerated
- `prisma/seeders/19-cert-profile-backfill.ts` — backfill seeder: legacy CERTIFIED rows → `InstructorCertificationProfile`, legacy PENDING rows → `CertificationApplication`; wired into `prisma/seed.ts` after seeder 18
- Backfill never downgrades: ACADEMIC wins over VERIFIED on conflict (highest tier preserved)
- String fields truncated to DB column limits in backfill (countryCode: 10, claimedFieldName: 255, linkedinUrl/websiteUrl: 500)
- `src/lib/certifications/queries/certification-level.query.ts` — `getInstructorCertificationLevel(userId)` reads from `InstructorCertificationProfile.currentLevel`, returns `CertificationType | null` (null = uncertified under new schema)
- Wave 0 test stubs (`it.todo`) for `certification-request-info.handler` and `certification-resubmit.handler`
- `phase7-needs-info-checkpoint.test.ts` — checkpoint tests for NEEDS_INFO lifecycle verifying: detection and update CTA routing, application history reason semantics, resubmitted timeline date, admin request-info eligibility, review history mapping, Arabic i18n keys
- Exported pure helpers used by checkpoint tests: `getNeedsInfoApplication`, `getNeedsInfoUpdateView`, `getApplicationHistoryReason`, `getResubmittedTimelineDate`, `canRequestMoreInfo`, `toReviewActionTranslationKey`

## Key decisions
- `getInstructorCertificationLevel()` returns `null` when no profile exists — callers treat null as uncertified; all domain handlers/queries should call this rather than querying `InstructorCertification` directly
- RESUBMITTED placed after NEEDS_INFO in the enum (not at the end) to reflect logical flow
- Backfill truncates legacy string fields to new schema column limits rather than failing on constraint error
- Wave 0 stubs created at plan start as Nyquist targets so Plan 02's TDD has concrete test targets to turn GREEN

## Patterns established
- Certification abstraction: all future handlers/queries call `getInstructorCertificationLevel()` rather than querying the old `InstructorCertification` table directly
- Enum-only migration: `ALTER TYPE ADD VALUE` — additive, no data migration needed
- Backfill seeder pattern: query old table, upsert new model, never downgrade tier
- Wave 0 stubs: create `it.todo()` test files at plan start for next plan's TDD targets

## Key files
- `prisma/migrations/20260310064259_phase_7_add_resubmitted_status/migration.sql`
- `prisma/schema.prisma` (RESUBMITTED added to enum)
- `prisma/seeders/19-cert-profile-backfill.ts`
- `prisma/seeders/__tests__/cert-profile-backfill.test.ts`
- `prisma/seed.ts`
- `src/lib/certifications/queries/certification-level.query.ts`
- `src/lib/certifications/queries/__tests__/certification-level.query.test.ts`
- `src/lib/certifications/handlers/__tests__/certification-request-info.handler.test.ts`
- `src/lib/certifications/handlers/__tests__/certification-resubmit.handler.test.ts`
- `app/(i18n)/_shared/(user)/certifications/_components/__tests__/phase7-needs-info-checkpoint.test.ts`
