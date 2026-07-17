---
title: "Instructor Certification — outcome"
date: "2026-03-07"
tags: ["project/experts", "topic/instructor-certification", "outcome"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

# Instructor Certification

**Outcome:** Delivered a complete end-to-end instructor certification system — CQRS domain library with four handlers and three API routes on the backend, plus instructor apply page, admin review queue, profile badge, and email templates on the frontend.

## What shipped
- `CertificationSubmitSchema` (expertiseAreas array, credentials min 20) and `CertificationReviewSchema` (approve/reject/revoke discriminated union)
- Four handlers: `handleCertificationSubmit`, `handleCertificationApprove`, `handleCertificationReject`, `handleCertificationRevoke`
- `getCertificationQueue` query (findMany PENDING with user include, ordered by appliedAt asc)
- API routes: `POST /api/v1/certifications` (submit), `GET /api/v1/certifications` (own status), `GET /api/v1/admin/certifications` (pending queue), `PATCH /api/v1/admin/certifications/:id` (approve/reject/revoke)
- `isCertified: boolean` on UserProfile DTO — derived from relation (status=CERTIFIED, take:1), not a stored column
- Amber BadgeCheck badge on public profile header when `isCertified` is true
- Instructor certification page (`/certifications`) with multi-step form and status display
- Admin certification queue page (`/admin/certifications`) with approve/reject/revoke action modals
- `useCertification` and `useCertificationQueue` SWR hooks
- React Email templates: `certification-approved` and `certification-rejected`; email registry entries added
- i18n strings in en/ar/es for `certifications.page` namespace
- Admin dashboard Quick Actions section with Certifications link card
- 26+ unit tests across schema, handler, query, and mapper files

## Key decisions
- `adminId` (not `reviewedById`) used at the handler boundary for clarity; extracted from `requireAdmin().userId` in routes
- Revoke requires no `rejectionReason` — admin can revoke without explanation; sets REVOKED status (not NOT_APPLIED) to preserve audit trail
- Approve and reject each do a single `findUnique` with user include rather than two separate queries
- `mapIsCertified` extracted as a pure helper in `profile.mapper.ts` to enable independent unit testing
- `session.user.roles.includes('instructor')` pattern used (session type does not expose `isInstructor` directly)
- Email template key pattern: `creators.certifications-approved` (plural `certifications`, singular action suffix)

## Patterns established
- Handlers return `{ error, status }` or `{ certification }` — never throw HTTP concerns
- Admin review handlers: `adminId` is required, fetched from `requireAdmin().userId` in routes
- Locale wrapper: `export default async function {Locale}CertificationsPage() { return <SharedPage /> }`
- Admin auth guard: `requireAdmin()` returns `{ authorized }`; render AccessDenied component if false
- `useCertification` hook wraps `useApiQuery` with stable fetcher via `useCallback`
- Admin action modal pattern: hidden trigger button + Modal.Backdrop open/close (HeroUI v3 compound pattern)

## Key files
- `src/lib/certifications/commands/certification-submit.schema.ts`
- `src/lib/certifications/commands/certification-review.schema.ts`
- `src/lib/certifications/handlers/certification-submit.handler.ts`
- `src/lib/certifications/handlers/certification-approve.handler.ts`
- `src/lib/certifications/handlers/certification-reject.handler.ts`
- `src/lib/certifications/handlers/certification-revoke.handler.ts`
- `src/lib/certifications/queries/certification-queue.query.ts`
- `src/lib/certifications/dto/certification.dto.ts`
- `src/lib/certifications/mappers/certification.mapper.ts`
- `src/lib/user/profile/dto/profile.mapper.ts` (mapIsCertified helper)
- `src/hooks/use-certification.ts`
- `app/api/v1/certifications/route.ts`
- `app/api/v1/admin/certifications/route.ts`
- `app/api/v1/admin/certifications/[certificationId]/route.ts`
- `app/(i18n)/_shared/(user)/certifications/page.tsx`
- `app/(i18n)/_shared/(user)/certifications/_components/certification-application-client.tsx`
- `app/(i18n)/_shared/admin/certifications/page.tsx`
- `app/(i18n)/_shared/admin/certifications/_components/certifications-queue-client.tsx`
- `src/notifications/channels/email/templates/creators/certification-approved.tsx`
- `src/notifications/channels/email/templates/creators/certification-rejected.tsx`
