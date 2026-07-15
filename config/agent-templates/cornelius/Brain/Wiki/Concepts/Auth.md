---
title: "Auth"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["topic/auth"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Auth.md"
---

# Auth — Authentication Patterns

Authentication across all Experts platform surfaces: web app, native iOS (Experts OS), and APIs.

## Stack

**NextAuth v5** (`src/lib/auth.ts`) — the single source of truth for sessions in the web app.

| Provider     | Used for                                      |
| ------------ | --------------------------------------------- |
| Credentials  | Email + password login                        |
| Google OAuth | Social login + account linking                |
| GitHub OAuth | Social login + account linking                |
| Apple OAuth  | Social login + account linking (iOS priority) |

## Server vs Client Usage

```typescript
// Server Components and API routes
import { auth } from "@/lib/auth";
const session = await auth();

// Client Components
import { useSession } from "next-auth/react";
// or
import { useAuth } from "@/lib/auth-context";
```

Admin-only routes use `requireAdmin()` — returns `{ authorized, userId, error }`. Never throws HTTP concerns from handlers.

## API Route Pattern

```typescript
// app/api/v1/{domain}/route.ts
const session = await auth();
if (!session)
  return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
```

## Key Decision — Identity vs Authentication Method

**One user, many login methods.** This was a discovered edge case and was explicitly resolved:

A user who registers with email (`sarah@example.com`) and later connects Google (`sarah@gmail.com`) must end up with **both methods connected** — not Google replacing email.

### Wrong model (original bug)

```
User registers with email provider
→ connects Google OAuth
→ Google becomes "Default", email is gone
→ User is now locked out if they disconnect Google
```

### Correct model

```
User {
  id
  email  // canonical / notification email
}

AuthIdentity {
  id
  userId
  provider       // email | google | apple | github
  providerUserId
  providerEmail
  isPrimary      // optional — user-controlled
}
```

### Rules that flow from this

1. **Linking ≠ Switching.** "Connect Google" adds a login method, it does not replace the existing one.
2. **Never auto-disconnect.** A credential is only removed when the user explicitly clicks Disconnect AND another method exists.
3. **Email addresses are attributes, not identity.** `account_email` ≠ `provider_email`. Do not auto-sync or replace.
4. **Primary method is user-controlled, explicit, and reversible.** Never set it as a side effect of linking.

## Experts OS (Native)

Experts OS uses its own session stores but hits the same HTTP auth endpoints (`/api/v1/auth/*`). Session tokens are stored natively (Keychain). See vault: [[Projects/Experts/Experts OS/docs/reference/Networking and API — Experts OS]].

## Auth Pages

Located at `app/(i18n)/{locale}/(auth)/` — login, register, forgot-password, reset-password, verify-email. These are locale-scoped (translated).

## Security Invariants

- **Roles must be DB-derived in the JWT callback.** The `update` trigger in `src/lib/auth.ts` must never write `token.roles = session.user.roles` — `session.update()` is client-controlled and any logged-in user could promote themselves to admin. On every update trigger, re-hydrate `isAdmin`/`isInstructor` from the database. Confirmed via 2026-05-13 security incident (see [[Raw/sources/2026-05-13-experts-security-incident-1-remediation]]).
- **`/api/*` is not proxy-gated.** `apps/experts-app/proxy.ts` passes all `/api/*` requests through without auth checks. Every API route handler must call `auth()` / `requireAdmin()` / `requireInstructor()` / `resolveAuthenticatedUserId()` for itself. Debug/utility routes under `app/api/**` must be deleted before merge or gated with `requireAdmin()` plus an ops secret.
- **Cron bearer auth must short-circuit on empty secret.** Routes that accept `Authorization: Bearer ${CRON_SECRET}` (e.g. `admin/refunds/cleanup`, `admin/commissions/approve-pending`) must check `cronSecret && cronSecret.length > 0` before comparing — otherwise a missing env var matches `Bearer undefined` and bypasses admin auth.

## Related

- [[Wiki/Concepts/Access Control]]
- [[Projects/Experts/Experts App/docs/reference/auth]]
