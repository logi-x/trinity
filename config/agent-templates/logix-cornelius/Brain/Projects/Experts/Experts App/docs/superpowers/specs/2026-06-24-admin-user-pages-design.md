---
title: "2026 06 24 admin user pages design"
date: "2026-06-24"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/specs/2026-06-24-admin-user-pages-design.md"
---
# Verbose Admin User Pages (detail + edit) — Design

**Date:** 2026-06-24
**Status:** Approved (brainstorming)
**Surface:** `apps/experts-app` — admin users

## Problem

The admin user surface uses a **drawer** (`user-detail-drawer.tsx`) for everything. It is cramped
and shows a thin slice of the user (profile + enrollments + invoices + accounts + recent activity).
It also omits subscription/grant info entirely — so after an admin grants a subscription there is no
way to see the user's current plan, grant type, who granted it, or why.

We want dedicated, verbose pages and to remove the drawer:

- `/admin/users/[id]` — a **verbose, tabbed** read view showing _everything available_ about a user.
- `/admin/users/[id]/edit` — edit profile fields + all admin actions in one place.

## Decisions (from brainstorming)

- **Edit scope:** profile fields (fullName, username, bio, phone, location, avatar) **+** all admin
  actions (role / status / verify / grant / password-reset) consolidated. **Email is read-only**
  (auth identity). Needs a new profile-update endpoint.
- **All-info scope:** everything reasonably available from the `User` relation graph.
- **Layout:** sticky identity header + **tabbed** sections.
- **Drawer:** **removed**; row-click / "Open" navigate to `/admin/users/[id]`.

## Slices (one feature, three shippable slices)

### Slice 1 — Data layer: verbose profile DTO + query

Replace the thin `AdminUserDetailDTO` with a sectioned **`AdminUserProfileDTO`** (nested per-tab
sub-DTOs; camelCase; ISO date strings; no Prisma types leaked; no `email` in any nested author DTO).
One `getAdminUserProfile(userId)` built from **parallel reads**: `_count` aggregates for
high-cardinality relations and bounded `take` slices (recent N) for rendered lists.

Sections, grounded in the real `User` relations:

- **Overview** — profile (fullName, username, email, phone, location, bio, avatarUrl,
  defaultAuthProvider, createdAt), headline counts, **current subscription incl. grant**
  (`planCode`/`planName`, `provider`, `status`, period, `grantType` = `manual|paid|free`,
  `grantedBy` {id, fullName}, `grantReason`), address, portfolio presence.
- **Learning** — enrollments (course, status, progress, enrolledAt), certificates
  (`CourseCertificate`), quiz/exam attempt counts, lesson-progress summary.
- **Billing** — subscription **history** (with grant fields), invoices, coupon redemptions,
  refund requests, content-access grants.
- **Community** — posts, comments, likes, ratings, shares (counts + recent), followers/following
  counts, bookmarks/bookmark-folders.
- **Instructor** (conditional: `isInstructor || courseInstructors || eventHosts`) — authored
  courses, hosted events, event-speaker roles, certification profile/applications/certifications,
  portfolio.
- **Security** — auth accounts (provider, providerAccountId, createdAt), auth tokens
  (recent + count), business memberships, storage usage/reservations/alert, incident logs.
- **Activity** — activity log, Ask-AI conversation count, views count.

`grantType` derivation: `provider === "free"` → `free`; `provider === "manual"` → `manual`;
otherwise → `paid`. `grantedBy`/`grantReason` come from the columns added in PR #1167.

Extends the existing `GET /api/v1/admin/users/[userId]` route to return the new DTO (route stays
thin; logic in the query). The list DTO/query are unchanged.

### Slice 2 — Detail page (tabbed) + remove drawer

`/admin/users/[id]` becomes a real page. Client component using `useApiQuery` with the four states
(skeleton-first via `isAwaitingFirstData`, error, empty, data; keep stale on failed refetch).

- **Sticky identity header**: avatar, fullName, @username, email, chips (status, admin, instructor,
  verified, current plan), joined date; action buttons (Edit → edit page, plus the action controls).
- **Tabs** (HeroUI `Tabs`, `dir`-aware): Overview / Learning / Billing / Community / Instructor* /
  Security / Activity — each a stack of admin-kit `SectionCard`s.
- **Remove the drawer**: delete `user-detail-drawer.tsx`; the list page (`page.tsx`) row-click and
  "Open" button `router.push` to `/admin/users/[id]`; drop `initialUserId`/`closeHref` plumbing and
  the `useAdminUserDetail` call from the list. The per-locale `[userId]/page.tsx` re-exports the new
  `_shared` detail page.

### Slice 3 — Edit page + profile-update endpoint + consolidated actions

`/admin/users/[id]/edit`:

- Form editing **profile fields** (fullName, username, bio, phone, location, avatarUrl); **email
  read-only**. Backed by a new **`PATCH /api/v1/admin/users/[userId]/profile`** (new handler +
  Zod schema, `requireAdmin()`, `safeErrorJson`, `auth()` inside the try). Writes to `Profile`
  (fullName/bio/avatarUrl/phone/location per column ownership) and `User.username` if owned there —
  verified against the schema before writing.
- The **action controls** (role / status / verify / grant / password-reset) are extracted from the
  drawer into a reusable `user-actions.tsx` used by both the detail header and the edit page; they
  call the existing endpoints. `grant-subscription-modal.tsx` is reused as-is.
- Save → toast → `router.push` back to the detail page; `mutate()` refreshes.

## Cross-cutting (per experts-constellation)

- RTL-first: `useIsRTL()` `dir` on roots, logical utilities, charts/numbers LTR.
- i18n: every string via `useTranslations`; keys added to **en + ar + es** `admin.json` in the same
  position with real translations.
- Accessibility: tabs labelled, regions named, decorative icons `aria-hidden`, errors `role="alert"`.
- Admin kit + HeroUI v3 compound components + semantic tokens only.
- Every admin route enforces `requireAdmin()` + Zod validation.
- Per-locale route re-exports for `[userId]` and `[userId]/edit` (en/ar/es).

## Testing

- **Pure helpers** (unit): `grantType` derivation + plan/grant formatting, status→badge, the verbose
  mapper sections, profile-form validation.
- **Components** (`renderToStaticMarkup`, node env, HeroUI/next-intl/useIsRTL mocked): the tabbed
  view (renders headers/sections), the edit form (renders fields, email read-only).
- **Handler** (mocked Prisma): profile-update writes the right columns; rejects unknown user (404);
  validates input.

## Out of scope (YAGNI)

Login-as/impersonation, bulk edits, an admin-edit audit log beyond `observe()`, editing email or
OAuth links.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
