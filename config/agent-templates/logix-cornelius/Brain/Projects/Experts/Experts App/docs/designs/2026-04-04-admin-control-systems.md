---
title: "Admin Control Systems: Users, Monetary, Analytics & Health — outcome"
date: "2026-04-04"
tags: ["project/experts", "topic/admin-control-systems", "outcome"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

# Admin Control Systems: Users, Monetary, Analytics & Health

**Outcome:** Filled the missing admin control plane with four subsystems — user management, monetary (revenue + refunds), expanded analytics, and an operational health/incident system — each with backend queries/routes, localized UI, and navigation wiring.

## What shipped
- Users management: paginated/searchable/status-filtered users list query and a deep user-detail audit query (profile, enrollments, invoices, connected accounts, activity); handlers for status change, role change, and admin-triggered password reset; `/api/v1/admin/users` list plus detail/status/role/password-reset endpoints. UI: `/admin/users` with in-place detail drawer and action buttons, plus a direct-entry `/admin/users/[userId]` route reusing the shared page.
- Monetary: extended `/api/v1/admin/revenue` endpoint (returns new admin metrics while preserving the dashboard's `daily`/`bySource` fields) with a revenue dashboard (summary cards, gateway tabs, time-series chart, top-content table); `/admin/refunds` page over the existing refunds API with status filtering and approve/reject/process actions.
- Analytics: four new endpoints (acquisition, content performance, engagement, revenue-per-content) with shared date-range parsing; SWR hooks with longer dedupe intervals; `/admin/views` expanded from two to six tabs over shared date filters.
- Health & incidents: `IncidentLog` model with `IncidentStatus`/`IncidentSeverity` enums; admin incident list/create/update routes and a public incidents endpoint; `/admin/health` with 30s service-status polling, incident log panel, and create/edit modal; public incident history wired into `/console/status`.
- Prisma hot-path indexes for `User.createdAt`, `Enrollment.enrolledAt`, `Invoice.paidAt`.
- Admin shell gained Users, Revenue, Refunds, and Health nav entries; localized copy (en/ar/es) across all new surfaces.

## Key decisions
- User account history represented via connected auth providers + recent activity, not IP/device history (not in schema).
- Admin password reset reuses the existing `auth.password-reset` notification channel, not a separate admin mailer.
- Operational incident state lives in the public schema and is reused by both admin and public status surfaces.
- Extended revenue API stays backward-compatible with the existing dashboard revenue widget.
- Failed-webhook retry shown as a disabled placeholder (backend retry out of scope).

## Patterns established
- Admin routes follow `requireAdmin` + Zod validation + structured JSON, delegating to query/handler files (consistent with payments/refunds admin APIs).
- Admin list pages use `useApiQuery`-backed hooks with compound HeroUI Table/Drawer primitives; locale wrappers are thin re-exports of the shared page.
- The views page remains the analytics hub, layering tabs rather than branching into separate pages.
- Repo HeroUI v3 constraints honored: `Button.isPending` (not `isLoading`), semantic-only Chip variants, `Select.Value` placeholder limits.

## Key files
- Backend: `src/lib/admin/dto/admin-{users,revenue-extended,analytics,incidents}.dto.ts`, `src/lib/admin/queries/admin-{users,revenue-extended,analytics-*,incidents}.query.ts`, `src/lib/admin/handlers/admin-{user-action,incident}.handler.ts`
- Routes: `app/api/v1/admin/{users,revenue,analytics,incidents}/**`, `app/api/v1/public/status/incidents/route.ts`
- UI: `app/(i18n)/_shared/admin/{users,revenue,refunds,views,health}/**`, locale wrappers under `app/(i18n)/{en,ar,es}/admin/**`
- Hooks: `src/hooks/use-admin-{users,revenue,analytics,incidents}.ts`
- Schema/migrations: `prisma/schema.prisma`, `20260404183028_add_admin_indexes`, `20260404184158_add_incident_log`
- Shell: `src/components/admin/AdminShell.tsx`
