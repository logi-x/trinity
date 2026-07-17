---
title: "Experts — Security Incident #1 Remediation"
date: "2026-05-13"
tags: ["project/experts", "session", "security", "project/experts-app", "auth", "webhooks", "xss", "idor", "privilege-escalation", "tabby"]
category: "session"
source: "session"
source_id: "Raw/sources/2026-05-13-experts-security-incident-1-remediation.md"
---

# Experts — Security Incident #1 Remediation

Date: 2026-05-13
Branch: `fix/security-incidents-20260513` → merged to `main` as `4c2dca6e` via [PR #307](https://github.com/logi-x/experts/pull/307)
Source: `~/brain-v2/Raw/reviews/incident#1/security.md`

## Summary

Remediated 8 validated medium-or-higher findings from the scheduled appsec review. All findings were verified reachable through `apps/experts-app/proxy.ts`, which explicitly passes `/api/*` through without auth — so any unguarded route handler is anonymously callable.

## Fixes Shipped

| Severity | Category                          | Finding                                                                                                                                                   | Resolution                                                                                                                                                   |
| -------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Critical | Data exposure                     | `GET /api/v1/internal/debug/accounts?id=<uuid>` returned `User` + `Account` rows including `passwordHash`, `accessToken`, `refreshToken`.                 | Route deleted.                                                                                                                                               |
| Critical | Authz / IDOR                      | `PUT /api/v1/community/posts/[id]` had no auth/ownership check.                                                                                           | Added `auth()`, strict Zod body schema, owner-or-admin gate, admin-only `isPinned`.                                                                          |
| High     | Multiple (SSRF, secrets, fan-out) | `/api/v1/internal/debug/{redis,notifications,mailtrap,env}` unauth.                                                                                       | All four routes deleted.                                                                                                                                     |
| High     | Stored XSS                        | `MarkdownPreview.tsx` had `skipHtml={false}` with no sanitizer (rehype-sanitize had been uninstalled).                                                    | Reinstalled `rehype-sanitize@6.0.0`, applied strict schema extending `defaultSchema` — blocks `iframe`, `script`, `object`, `embed`, `form`; drops `srcDoc`. |
| Critical | Webhook forgery                   | `TabbyWebhookProvider.verify()` returned silently when `TABBY_WEBHOOK_SECRET` was unset, including in prod.                                               | In `NODE_ENV=production`, throw if secret missing.                                                                                                           |
| High     | Privilege escalation              | NextAuth JWT `update` trigger wrote `token.roles = session.user.roles` — any logged-in user could call `update({user:{roles:["admin"]}})` and gain admin. | Update trigger now re-hydrates roles from DB; never trusts client payload.                                                                                   |
| High     | Data exposure                     | `/api/v1/console/diagnostics/{history,stream}` exposed `systemEvent` rows and SSE stream to anonymous clients.                                            | Both gated behind `requireAdmin()`.                                                                                                                          |
| Medium   | Authn bypass                      | `admin/refunds/cleanup` and `admin/commissions/approve-pending` accepted `Authorization: Bearer undefined` when `CRON_SECRET` env was unset.              | Require non-empty cronSecret before bearer comparison.                                                                                                       |

## Key Design Decisions

### Roles must be DB-derived in the JWT update callback

Original code in `src/lib/auth.ts`:

```ts
if (trigger === "update" && session) {
  // ...
  if (session.user?.roles) {
    token.roles = session.user.roles;
  }
}
```

The `update()` payload is client-controlled. **Any field written to the token from the update payload becomes a privilege oracle.** Rule going forward: in the `jwt` callback, on the `update` trigger, only allow profile/account display fields to flow through. Roles and admin/instructor flags must be re-fetched from the DB:

```ts
const dbUser = await prisma.user.findUnique({
  where: { id: token.userId as string },
  select: { isAdmin: true, isInstructor: true },
});
token.roles = [
  "user",
  ...(dbUser.isInstructor ? ["instructor"] : []),
  ...(dbUser.isAdmin ? ["admin"] : []),
];
```

### Webhooks fail closed in production when the secret is missing

Tabby's verifier was previously fail-open if `webhookSecret` was unset, including in prod. New rule: any payment webhook provider must `throw` in `NODE_ENV=production` when its signing secret is absent, even if the inbound request carries no signature header. Operational invariant: **the absence of a secret is an error, not "verification skipped"**.

### Markdown UGC: sanitizer is a hard requirement

When `@uiw/react-markdown-preview` is rendered with `skipHtml={false}`, raw HTML in the markdown source is passed through `rehype-raw` and rendered. Without `rehype-sanitize`, that is a same-origin script execution vector for any UGC author. The fix re-installs `rehype-sanitize@6.0.0` and applies a schema that explicitly removes `iframe`, `script`, `object`, `embed`, `form` from `defaultSchema.tagNames` and drops `srcDoc` from the universal attribute allowlist.

The `defaultSchema` already forbids event handlers (`on*`) and dangerous URL protocols (`javascript:`, `data:` outside specific media tags). The extension is defense-in-depth on top of that.

### Proxy `/api/*` passes unconditionally — every route must guard itself

`apps/experts-app/proxy.ts` matches `NON_LOCALE_ROUTES` first and returns `NextResponse.next()` for any path under `/api/`. There is **no** middleware-level auth. Every route handler under `apps/experts-app/app/api/**` is anonymously reachable unless it calls `auth()` / `requireAdmin()` / `requireInstructor()` / `resolveAuthenticatedUserId()` itself. Any new internal/debug route must be either deleted before production or gated explicitly.

## Test Fix — `course-workflow.handlers.test.ts`

Phase 8 added recognitionType-vs-cert-level validation to `handleCoursePublish`. The "publishes an approved course with limit check" test broke because the new path calls `prisma.courseInstructor.findFirst` and `getInstructorCertificationLevel`, neither of which were mocked. Aligned the test:

- Added `vi.mock` for `@/lib/certifications/queries/certification-level.query` and `@/lib/ai/embeddings/embed.service`.
- Added `prisma.courseInstructor.findFirst` mock.
- Expanded the `findUnique` resolved value with `totalLessons`, `price`, `publishedAt`, `couponEnabled`, `recognitionType`, `_count`.
- Corrected the recognitionType enum literal from the stale `"GENERAL"` to `"GENERAL_LEARNING"`.

## Files Changed (16, +173 / −728)

Deletes — `apps/experts-app/app/api/v1/internal/debug/{accounts,env,mailtrap,notifications,redis}/route.ts`

Modifies:

- `apps/experts-app/app/api/v1/community/posts/[id]/route.ts`
- `apps/experts-app/app/api/v1/console/diagnostics/{history,stream}/route.ts`
- `apps/experts-app/app/api/v1/admin/refunds/cleanup/route.ts`
- `apps/experts-app/app/api/v1/admin/commissions/approve-pending/route.ts`
- `apps/experts-app/src/components/markdown/MarkdownPreview.tsx`
- `apps/experts-app/src/lib/auth.ts`
- `apps/experts-app/src/notifications/channels/webhook/providers/tabby.provider.ts`
- `apps/experts-app/package.json` + `pnpm-lock.yaml` (rehype-sanitize)
- `apps/experts-app/src/lib/courses/catalog/handlers/__tests__/course-workflow.handlers.test.ts`

## Operational Follow-Ups

- **Before next prod deploy**: confirm `TABBY_WEBHOOK_SECRET` is present in the production env store. The handler now throws if it isn't. Rotate the secret in the Tabby dashboard and env store in lockstep.
- **Client breakage to watch for**: any code calling `session.update({user:{roles:[...]}})` will no longer mutate roles — that pathway silently no-ops. UI relying on it is likely already broken or never worked.
- **Tooling gotcha encountered**: `tsconfig.tsbuildinfo` cached stale `.next/dev/types/...` paths from deleted routes, causing pre-push `TS6053` errors. Resolution: `rm apps/experts-app/tsconfig.tsbuildinfo`. Documented in `Wiki/Concepts/Monorepo.md`.

## Related

- [[Wiki/Concepts/Auth]]
- [[Wiki/Concepts/Access Control]]
- [[Wiki/Concepts/Webhooks]]
- [[Wiki/Concepts/Payments]]
- [[Wiki/Concepts/Monorepo]]
- [[Decision-Log]]
- [[Action-Tracker]]

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
