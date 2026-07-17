---
title: "Access Control"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "topic/access-control", "access-control", "security", "rbac"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Access Control.md"
---

# Access Control — RBAC and Permissions

Authorization model across the Experts platform: route guards, content access, admin controls, and realtime channel authorization.

## Layers

| Layer             | Mechanism                       | Where                                |
| ----------------- | ------------------------------- | ------------------------------------ |
| Session           | `auth()` — NextAuth v5          | All API routes and Server Components |
| Admin guard       | `requireAdmin()`                | Admin-only API routes                |
| Content access    | Enrollment + subscription check | Course/event learn routes            |
| Realtime channels | `sanitizeRealtimeChannels()`    | WebSocket subscriptions              |

## API Route Pattern

Every protected API route follows: **authenticate → guard → handle**. Handlers return structured results — never throw HTTP concerns:

```typescript
// app/api/v1/{domain}/route.ts
const session = await auth();
if (!session)
  return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

// Admin-only
const { authorized, userId, error } = requireAdmin(session);
if (!authorized) return NextResponse.json({ error }, { status: 403 });

// Handler
const result = await someHandler(prisma, userId, input);
if (result.error)
  return NextResponse.json({ error: result.error }, { status: result.status });
return NextResponse.json(result.data);
```

## `requireAdmin()`

Located in `src/lib/auth.ts` (or auth helpers). Returns `{ authorized, userId, error }`. Used for all `/admin/*` API routes and admin pages. Never throws — callers check the return value.

## Content Access Guard — Courses (Known Bug, April 2026)

A live issue was found (2026-04-09): any unauthenticated user could access `/courses/[id]/learn` directly via URL, bypassing the enrollment check. The learn route was missing an enrollment/subscription guard at the page and API level.

**Correct guard pattern for paid content:**

```typescript
// Server Component or API route for /courses/[id]/learn
const session = await auth();
if (!session) redirect("/login");

const enrollment = await prisma.enrollment.findFirst({
  where: { userId: session.user.id, courseId: params.id, status: "active" },
});
if (!enrollment) redirect(`/courses/${params.id}`); // paywall
```

Search results (GlobalSearch) must also filter lesson results for users without active enrollments — returning lessons from paid courses in search is a secondary leak path.

## Modules

Domain-level permissions live under `src/modules/permissions/`. Cross-cutting authorization helpers (e.g. "can this user publish?", "does this user own this course?") should live here rather than inline in handlers.

## Realtime Channel Authorization

WebSocket channel subscriptions are authorized server-side via `sanitizeRealtimeChannels()` in `src/lib/realtime/channel-auth.ts`. Users can only subscribe to channels they are permitted to hear:

- `notifications:user:<userId>` — own notifications only
- `post:<uuid>:events` — public or member-accessible posts
- `presence:user:<userId>` — own presence stream

The same rules are mirrored in `apps/experts-realtime/channel-sanitize.ts`. Max 64 channels per socket.

## Page-Level Access (i18n Routes)

Protected pages live under locale-scoped routes (`app/(i18n)/_shared/`). For gated content, the shared implementation does the session + access check. Locale wrappers are thin re-exports — the guard must be in `_shared/`, not in the locale wrapper.

## Related

- [[Wiki/Concepts/Auth]]
- [[Wiki/Concepts/WebSockets]]
- [[Wiki/Concepts/i18n]]
- [[Projects/Experts/Experts App/docs/reference/realtime-contract]]
