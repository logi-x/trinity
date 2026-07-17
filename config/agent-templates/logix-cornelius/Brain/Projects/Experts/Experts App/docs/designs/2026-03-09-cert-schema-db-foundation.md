---
title: "Deep Cert Schema DB Foundation — outcome"
date: "2026-03-09"
tags: ["project/experts", "topic/cert-schema-db", "outcome"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

# Deep Cert Schema DB Foundation

**Outcome:** Established a 7-table normalized certification schema alongside the existing `InstructorCertification` model, including 26 canonical `CertificationField` rows and 52 `CertificationBadge` rows seeded via idempotent slug-keyed upserts.

## What shipped
- 4 new enums: `CertificationApplicationStatus`, `CertificationEvidenceType`, `CertificationEvidenceStatus`, `CertificationReviewDecisionAction`
- 7 new Prisma models: `CertificationField`, `CertificationBadge`, `InstructorCertificationProfile`, `CertificationApplication`, `CertificationEvidence`, `CertificationReviewDecision`, `CertificationBadgeAssignment`
- 4 new `User` model relations: `certificationProfile`, `certificationApplications`, `certificationReviewDecisions`, `applicationReviews` (with named disambiguation)
- Migration `20260309145348_phase_6_deep_cert_schema` applied; all 7 tables created with correct FKs, indexes, and unique constraints
- Prisma client regenerated — all new types exported
- `prisma/seeders/18-certification-fields-and-badges.ts` — 26 `CertificationField` + 52 `CertificationBadge` rows via slug-keyed upserts
- Badge slug convention: `verified-{field-slug}` and `academic-{field-slug}` — queryable by pattern from Phase 7 onward
- Seeder wired into `prisma/seed.ts` at step 10.6

## Key decisions
- New models appended after existing `InstructorCertification` block — old model left completely untouched (serves as rollback target)
- `CertificationApplication.currentReviewerId` relation named `"ApplicationCurrentReviewer"` to avoid ambiguity with existing named relations on User
- FK delete behaviors follow existing pattern: Cascade for owner FKs, SetNull for optional reviewer/field FKs, Restrict for badge FKs
- Badge slug convention locked as `verified-{field-slug}` / `academic-{field-slug}` — all 26 slugs are canonical and immutable
- `05-subscriptions.ts` seeder fixed from `plan.create()` → `plan.upsert()` to restore idempotency (was blocking seed from reaching step 10.6)

## Patterns established
- UUID primary keys via `gen_random_uuid()` on all new models
- `@@schema('public')` on all new models and enums — consistent with existing domain
- Slug-keyed upsert for any reference data seeder: always upsert, never create, for idempotency
- `fieldMap` (slug → id) built after field upsert loop to avoid multiple DB lookups in badge loop

## Key files
- `prisma/schema.prisma` (4 enums, 7 models, 4 User relations added)
- `prisma/migrations/20260309145348_phase_6_deep_cert_schema/migration.sql`
- `prisma/seeders/18-certification-fields-and-badges.ts`
- `prisma/seed.ts`
- `prisma/seeders/05-subscriptions.ts` (idempotency fix)
