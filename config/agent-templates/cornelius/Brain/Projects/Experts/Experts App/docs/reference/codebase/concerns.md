---
title: "Experts codebase — Concerns"
date: "2026-03-06"
tags: ["project/experts", "topic/planning", "topic/quality"]
category: "docs/experts-reference"
repo_root: /Users/ahmedsulaimani/projects/experts/apps/experts-app
monorepo_root: /Users/ahmedsulaimani/projects/experts
updated: "2026-07-15"
---

# Codebase Concerns

**Analysis Date:** 2026-03-06

---

## Security Considerations

**Unauthenticated Internal Debug Endpoints:**

- Risk: Several `/api/v1/internal/debug/*` endpoints expose system internals with no authentication or admin check
- Files:
  - `app/api/v1/internal/debug/redis/route.ts` — no auth; exposes Redis host URL, tests cache operations, publishes to pub/sub channels
  - `app/api/v1/internal/debug/env/route.ts` — no auth; reveals mail provider host and from-address config
  - `app/api/v1/internal/debug/notifications/route.ts` — no auth; triggers real email/Slack notifications to any target
  - `app/api/v1/internal/debug/accounts/route.ts` — no auth; returns raw user + linked OAuth account records for any user ID
  - `app/api/v1/internal/workers/init/route.ts` — no auth; exposes internal worker health status
  - `app/api/v1/internal/featured-data/route.ts` — no auth; publicly accessible (low risk but still leaks internal structure)
- Current mitigation: None. Only `app/api/v1/internal/debug/mailtrap/route.ts` has a `NODE_ENV === "development"` check (not enforced as a response block — just a flag)
- Recommendations: Add `auth()` + admin role check to all internal/debug endpoints. Consider routing them behind a secret header (`x-internal-secret`) or restricting entirely to `NODE_ENV !== "production"`

**Certificate Issuance Without Server-Side Completion Verification:**

- Risk: `POST /api/v1/user/certificates` creates a certificate for any authenticated user who supplies a `courseId`, without verifying actual course completion or lesson progress
- Files: `app/api/v1/user/certificates/route.ts`
- Impact: Any enrolled user can claim a certificate without completing the course
- Fix approach: Check `enrollment.progress === 100` and `enrollment.completedAt IS NOT NULL` before issuing a certificate; trigger certificate creation server-side from the progress handler, not the client

**Quiz Anti-Cheat System Claimed but Not Implemented:**

- Risk: The UI copy (`src/i18n/messages/en/creator/courses.ts:323`) states "An anti-cheat system is applied to detect abnormal behavior" but no actual server-side enforcement exists (no tab-switch detection, no time anomaly checks, no server-side answer validation)
- Files: `src/i18n/messages/en/creator/courses.ts` (line 323), quiz submission handlers
- Impact: Creates a false expectation of security enforcement; quiz answers are fully controllable from the client
- Fix approach: Either remove the claim from UI copy, or implement basic server-side timing/attempt validation in quiz submission handlers

**Sensitive Data Logged in Production:**

- Risk: `app/api/v1/internal/debug/mailtrap/route.ts` logs API keys, mail from-address, email content, and full HTML body via `console.log` at the function level — not gated by NODE_ENV
- Files: `app/api/v1/internal/debug/mailtrap/route.ts` (multiple `console.log` lines)
- Current mitigation: None; `isDev` is set but not used to suppress logs
- Fix approach: Remove console.log statements; use structured logger with level gating

**173 console.log/warn/error Calls in API Routes:**

- Risk: Raw console logging in 178 API route files means unstructured, potentially PII-containing data can appear in production logs
- Files: Distributed across `app/api/` (173 occurrences)
- Fix approach: Replace with the structured `logger` from `src/lib/logger.ts`; audit for PII before shipping

---

## Tech Debt

**Incorrect Import Path Convention (`@/` instead of `@/`):**

- Issue: 155 occurrences of `from '@/...'` exist throughout the codebase. The correct alias per `tsconfig.json` is `@/*` mapping to `./src/*`, so `@/` double-paths the `src/` directory. This works only by accident
- Files (examples):
  - `src/lib/events/detail/event-detail-page.tsx` (lines 9-12)
  - `src/lib/events/detail/sections/event-detail-sidebar.tsx` (line 24)
  - `app/api/auth/forgot-password/route.ts` (line 6)
  - `app/api/auth/register/route.ts` (line 7)
  - `app/api/v1/admin/zatca/retry/route.ts` (lines 5-6)
  - `app/sitemap-en.xml/route.ts`, `app/sitemap-es.xml/route.ts` (line 1)
- Impact: Fragile resolution; can silently break on certain tsconfig or bundler changes
- Fix approach: Batch search-replace `from "@/` → `from "@/` across all non-generated files

**Leftover Copy/Duplicate Files:**

- Issue: Two development-time copy files committed to the repository
- Files:
  - `src/lib/courses/detail/course-detail-page copy.tsx` (460 lines, near-duplicate of `course-detail-page.tsx`)
  - `src/components/ui/button copy.tsx`
- Impact: Causes confusion about canonical implementation; linters may or may not pick them up due to the space in the filename
- Fix approach: Delete both files; verify nothing imports them (currently nothing does)

**Denormalized `totalLessons` Counter on Course Model:**

- Issue: `Course.totalLessons` is maintained via increment/decrement in lesson create/delete handlers. Module delete handler has the decrement commented out (`// data: {totalLessons: {decrement: deletedLessons}}`)
- Files:
  - `prisma/schema.prisma` (line 361)
  - `src/lib/courses/curriculum/lessons/handlers/course-lesson-create.handler.ts` (line 65)
  - `src/lib/courses/curriculum/lessons/handlers/course-lesson-delete.handler.ts` (line 42)
  - `src/lib/courses/curriculum/modules/handlers/course-module-delete.handler.ts` (line 42 — commented out)
- Impact: Counter can drift from actual count when modules with lessons are deleted, producing stale UI data. This was identified as a known issue in `to-do.txt`
- Fix approach: Remove `totalLessons` column; compute lesson count via `_count.lessons` in Prisma queries

**Draft/Published Status Inconsistency:**

- Issue: Known drift between `publishingStatus` stored in the DB and what the creator UI displays. Seed data or status transitions may leave courses showing as "draft" in `/creator/courses` but visible in public `/courses`. Noted in `to-do.txt`
- Files: `src/lib/courses/catalog/handlers/course-update.handler.ts`, course list queries
- Impact: Creator dashboard shows "0 active courses" while public page shows the same courses as published
- Fix approach: Audit the `publishingStatus` field across all create/update paths; ensure UI reads the single source of truth

**Placeholder Telephone Number in JSON-LD Structured Data:**

- Issue: `+966-XX-XXX-XXXX` is committed as the contact telephone in the homepage's JSON-LD structured data
- Files: `src/lib/metadata/home-layout-metadata.ts` (line 148)
- Impact: Invalid SEO structured data; search engines may penalize or ignore the schema
- Fix approach: Replace with a real number or remove the `contactPoint` block until a number is available

**`uuid` Dependency Pinned to `latest`:**

- Issue: `"uuid": "latest"` in `package.json` is an unpinned floating version
- Files: `apps/experts-app/package.json`
- Impact: Next install could silently upgrade to a breaking major version
- Fix approach: Pin to a specific version (e.g., `^9.0.0` or `^10.0.0`)

**Beta/Pre-release Dependencies in Production:**

- Issue: Three packages are pinned to beta/alpha versions
  - `@heroui/react`: `3.0.0-beta.8` (primary UI library — entire component system is on a beta build)
  - `@heroui/styles`: `3.0.0-beta.8`
  - `next-auth`: `^5.0.0-beta.30` (authentication — critical path)
  - `@uiw/react-json-view`: `^2.0.0-alpha.40`
- Files: `apps/experts-app/package.json`
- Impact: Breaking changes, undocumented API shifts, and no stability guarantees for the UI library and auth provider
- Fix approach: Monitor release timelines; pin exact beta versions; plan upgrade path to stable when released

**`moment.js` Used Despite `date-fns` Being the Standard:**

- Issue: `moment` is listed as a production dependency (a large, legacy library) and is used in at least one file while `date-fns` is the project-wide standard
- Files: `src/lib/generate-qr-code.tsx` (line 1)
- Impact: Adds ~300KB to the bundle unnecessarily
- Fix approach: Replace the single `moment` usage in `generate-qr-code.tsx` with `date-fns`; remove `moment` from dependencies

**`example-chart.tsx` — Unused 1,417-Line File:**

- Issue: A large example/prototype chart file exists with no imports from the rest of the codebase. It is referenced in `to-do.txt` as a template to copy from, not as production code
- Files: `src/components/charts/example-chart.tsx`
- Impact: Dead code adds noise, increases type-checking time, and contains two `eslint-disable-next-line` suppressions
- Fix approach: Remove or move to a `docs/` or `scripts/` directory

---

## Known Bugs

**"Start Learning" Button Does Not Navigate:**

- Symptoms: Button refreshes the current page instead of redirecting to the correct learn page
- Files: Course detail page CTA logic (`src/lib/courses/detail/`)
- Trigger: Noted explicitly in `to-do.txt` ("Start Learning button does nothing, it's kind of refreshing current page instead of redirecting to correct page")
- Workaround: None currently

**Event Edit Access Not Bound to Creator:**

- Symptoms: Event edit page does not enforce ownership — it must be manually linked by user ID to test
- Files: Event edit route and handler (`src/lib/events/forms/`)
- Trigger: Any authenticated user could potentially access another user's event edit page
- Workaround: Manual DB linkage required for testing

**User Presence System Unstable:**

- Symptoms: Viewer count disappears after ~60 seconds and does not recover without page refresh; first-visit presence not tracked until focus change
- Files:
  - `src/lib/realtime/polling-transport.ts`
  - `src/hooks/use-presence.ts`
  - `app/api/v1/internal/presence/` (all routes)
- Trigger: Both anonymous and authenticated viewer presence resets; noted in `to-do.txt`
- Workaround: Refresh page

**Linked Account Disconnect on Google OAuth Connect:**

- Symptoms: When an email/password user connects a Google account, the email/password provider shows as "not connected" afterwards — the primary auth method loses its UI indicator
- Files: `src/lib/auth.ts`, `app/api/auth/link-account/`
- Trigger: Navigate to `/settings/security` → connect Google account → return to settings
- Workaround: None

**Quiz Completion Loop:**

- Symptoms: After passing a quiz and pressing "Continue," the user is looped back to "Start Quiz" which immediately shows "You already passed this quiz" with a "Continue" button that loops again
- Files: `src/lib/courses/quizzes/components/quiz-player.tsx`
- Trigger: Quiz at end of module with no next lesson

---

## Performance Bottlenecks

**Polling-Based Real-Time Transport Queries Database on Every Poll:**

- Problem: The realtime sync endpoint (`GET /api/v1/internal/realtime/sync`) queries the PostgreSQL database on every polling request. Debug logging is embedded in the hot path with comments to "remove in production" that have not been removed
- Files:
  - `app/api/v1/internal/realtime/sync/route.ts` (629 lines; 4 debug log points on lines 89, 313, 472, 589)
  - `src/lib/realtime/polling-transport.ts` (debug logging on lines 38, 144, 182)
  - `src/lib/realtime/global-coordinator.ts` (debug logging on lines 38, 57, 90, 127)
- Impact: Every connected client generates a DB query on each poll interval; scales poorly under load
- Improvement path: Replace database polling with Redis Streams or proper SSE (commented Redis code exists in the file as `// import {getRedis}`); remove debug logging immediately

**178 API Route Files with Console Logging in the Hot Path:**

- Problem: `console.log` calls in API route handlers add synchronous I/O and unstructured output on every request
- Files: Distributed across `app/api/` (178 occurrences)

**Large Monolithic Components:**

- Problem: Several components exceed 800 lines and are hard to split, test, or tree-shake
- Files:
  - `src/components/profile/profile-settings.tsx` — 1,627 lines
  - `src/lib/events/forms/sections/event-schedule-section.tsx` — 941 lines
  - `src/lib/events/forms/use-event-form.ts` — 859 lines
  - `src/lib/auth.ts` — 855 lines
  - `src/lib/courses/curriculum/lessons/lesson-types/video/video.player.tsx` — 853 lines
  - `src/components/events/EventCard.tsx` — 816 lines
- Improvement path: Extract sub-components; split hooks into smaller composables

---

## Fragile Areas

**`polling-transport.ts` — Debug Logging Marked for Removal But Still Present:**

- Files: `src/lib/realtime/polling-transport.ts` (lines 38, 144, 182)
- Why fragile: Four `// ✅ DEBUG: ... (remove in production)` comments indicate unfinished cleanup; the logging fires on every poll cycle
- Safe modification: Remove the logger calls on those lines and the surrounding `// ✅ DEBUG` comments without touching transport logic

**`course-detail-page copy.tsx` — Imported Nowhere but Contains Real Code:**

- Files: `src/lib/courses/detail/course-detail-page copy.tsx`
- Why fragile: Space in filename makes it invisible to some glob patterns; contains `eslint-disable-next-line react-hooks/exhaustive-deps` suggesting it diverged from the canonical file mid-development
- Safe modification: Delete; verify `src/lib/courses/detail/course-detail-page.tsx` is the canonical version

**`app/api/v1/courses/[id]/progress/route.ts` — No Auth Check:**

- Files: `app/api/v1/courses/[id]/progress/route.ts`
- Why fragile: Identified by grep as lacking `auth()` or session check; if this route modifies enrollment progress it could be exploited
- Safe modification: Add `auth()` check and verify the session user owns the enrollment before updating

**Real-Time Coordinator Exposed to Window in Non-Production:**

- Files: `src/lib/realtime/global-coordinator.ts` (line 297)
- Why fragile: `window.__realtimeCoordinator` is assigned when `NEXT_PUBLIC_DEBUG === "true"` regardless of other flags; if the env var is accidentally set in staging/canary, internal state is browsable via DevTools
- Safe modification: Confirm `NEXT_PUBLIC_DEBUG` is never set in staging/canary/production environments; add a check for explicit `NODE_ENV === "development"` as a second guard

---

## Test Coverage Gaps

**Zero Tests for All React Components:**

- What's not tested: No component tests exist in `src/components/` (0 test files)
- Files: All of `src/components/` — 60+ components including `Navbar.tsx`, `GlobalSearch.tsx`, `ImageUpload.tsx`, payment flows, rating UI
- Risk: UI regressions, prop interface changes, and conditional rendering logic can break silently
- Priority: High

**Zero Tests for All Custom Hooks:**

- What's not tested: No test files exist in `src/hooks/` — 20+ hooks including `use-events.ts`, `use-bookmarks.ts`, `use-realtime.ts`, `use-api-query.ts`
- Files: All of `src/hooks/`
- Risk: Hook logic changes (especially `use-realtime` and `use-events`) can break data flows without detection
- Priority: High

**No Integration Tests for Payment Webhooks:**

- What's not tested: Tabby and Noon webhook handlers have no test coverage
- Files:
  - `app/api/webhooks/tabby/route.ts`
  - `app/api/webhooks/noon/route.ts`
- Risk: Payment confirmation failures are invisible until a real user reports a missing enrollment
- Priority: Critical

**No Coverage Threshold Enforced:**

- What's not tested: `vitest.config.ts` has no `coverage.thresholds` configured; any coverage level passes CI
- Files: `apps/experts-app/vitest.config.ts`
- Risk: Coverage can drop to 0% without a build failure
- Priority: Medium

---

## Missing Critical Features (Tracked in to-do.txt)

**OAuth Token Refresh Not Implemented:**

- Problem: NextAuth v5 session tokens are not refreshed; long-lived sessions can expire mid-use
- Files: `src/lib/auth.ts`
- Impact: Users silently lose authenticated state

**Rate Limiting on Auth Endpoints:**

- Problem: No rate limiting on `/api/auth/register`, `/api/auth/forgot-password`, `/api/auth/verify-email`, or OAuth endpoints
- Files: `app/api/auth/` (all routes)
- Impact: Brute-force and enumeration attacks on authentication endpoints are unrestricted

**Course Completion Certificate Reliability:**

- Problem: Certificate issuance is triggered from the client only (noted in `to-do.txt`): "Completion + Certificate is only triggered client‑side, so it's unreliable (missed if user closes the page)"
- Files: `app/api/v1/user/certificates/route.ts`, learn page client components
- Impact: Completed courses may not generate certificates if the page is closed before the POST fires

---

_Concerns audit: 2026-03-06_

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
