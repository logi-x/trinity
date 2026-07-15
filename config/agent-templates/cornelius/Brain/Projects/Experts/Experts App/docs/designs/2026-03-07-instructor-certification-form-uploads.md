---
title: "Instructor Certification Form with File Uploads — outcome"
date: "2026-03-07"
tags: ["project/experts", "topic/instructor-certification-uploads", "outcome"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

# Instructor Certification Form with File Uploads

**Outcome:** Evolved the instructor certification form into a 5-step wizard with AES-256-GCM national ID encryption, private R2 document storage with signed-URL access, and an enhanced admin review queue showing full structured application data.

## What shipped
- `AttachmentMetaSchema` (id, url, filename, documentType enum, size, uploadedAt) and `InstructorApplicationSchema` covering all 5 wizard steps
- `ProofOfExpertiseItemSchema` — discriminated union across 6 types: `published_work`, `portfolio`, `public_speaking`, `online_profile`, `media_mention`, `peer_reference`
- `handleVerifiedApplicationSubmit` / `handleAcademicApplicationSubmit` updated to encrypt `basicInfo.nationalId` via AES-256-GCM before storage; `applicationData` deprecated (set to null)
- 11 new optional columns on `InstructorCertification` model: `fullName`, `nationalIdEncrypted`, `countryOfResidence`, `primaryExpertiseField`, `yearsOfExperience`, `linkedinUrl`, `websiteUrl`, `educationCredentials`, `workExperience`, `proofOfExpertise`, `agreements`
- `src/lib/crypto/field-encryption.ts` — AES-256-GCM encrypt/decrypt keyed from `FIELD_ENCRYPTION_KEY` env var; dev fallback warns and uses deterministic key
- `POST /api/v1/certifications/documents/upload` — auth check, PDF/image ≤10 MB, uploads to `R2_BUCKET_CERTIFICATIONS`, returns `{key, fileName, fileSize, uploadedAt}` (no public URL)
- `GET /api/v1/certifications/documents/signed-url?key=...` — auth + ownership check, returns 15-min pre-signed GetObject URL
- `hasNationalId: boolean` flag in DTO — `nationalIdEncrypted` never exposed in any API response
- Full rewrite of `certification-application-client.tsx` as a 5-step wizard with per-step Zod validation before advancing; Step 5 requires 4 agreement checkboxes
- localStorage draft key `certifications.application.draft.v2`; old v1 key cleared on mount
- `SignedFileLink` component — fetches signed URL on-demand per file click; URL not pre-fetched
- Admin queue enhanced with `ApplicationDataSection` showing all structured data in expandable HeroUI Disclosure; nationaId shown only as "ID on file: Yes/No"
- 2-step intermediate wizard (04-02) shipped first then superseded by the 5-step form (04-03)
- 50 certifications tests passing

## Key decisions
- `attachments` field uses `min(1)/max(5)` without `.default([])` — API enforces at least one attachment; UI prevents submission before upload
- `documentType` enum restricted to `[cv, certificate, portfolio, reference]`
- `db push` used instead of `migrate dev` due to migration history drift in dev DB
- `applicationData` set to null on new submissions — deprecated field cleared to avoid stale data
- Draft persists attachments and `uploadEntityId` (not just step 1 fields) so uploaded files survive navigation
- TagGroup expertise chip input uses `string[]` state (not `useListData`) — simpler and functionally equivalent

## Patterns established
- Discriminated union Zod schema for proof-of-expertise types
- Encrypted PII column (`nationalIdEncrypted`) with boolean `hasNationalId` in DTO — raw encrypted value never in any API response
- Private R2 bucket with signed URL access (15-min expiry)
- Multi-step wizard with per-step Zod validation (validate only current step before advancing)
- localStorage draft key versioning (v2) with v1 migration/cleanup on mount
- Per-file upload flow: validate client-side → POST FormData → accumulate `AttachmentMeta` in state → final submit sends JSON

## Key files
- `src/lib/crypto/field-encryption.ts`
- `src/lib/certifications/commands/certification-submit.schema.ts` (InstructorApplicationSchema, ProofOfExpertiseItemSchema)
- `src/lib/certifications/handlers/certification-submit.handler.ts`
- `src/lib/certifications/dto/certification.dto.ts` (hasNationalId added)
- `app/api/v1/certifications/documents/upload/route.ts`
- `app/api/v1/certifications/documents/signed-url/route.ts`
- `app/(i18n)/_shared/(user)/certifications/_components/certification-application-client.tsx`
- `app/(i18n)/_shared/admin/certifications/_components/certifications-queue-client.tsx`
- `prisma/schema.prisma` (11 new columns on InstructorCertification)

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
