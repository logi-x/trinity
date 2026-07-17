---
title: "`DomainError` (`@/lib/errors/api-error`) is the canonical mechanism for surfacing an intentional client-facing message +"
date: "2026-05-29"
decision: "`DomainError` (`@/lib/errors/api-error`) is the canonical mechanism for surfacing an intentional client-facing message + status from a route handler; a raw caught error's `.message` must never reach a"
stakeholders: "Logix, Security"
review_by: "2026-06-12"
source: "[[Raw/sources/2026-05-28-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `DomainError` (`@/lib/errors/api-error`) is the canonical mechanism for surfacing an intentional client-facing message + status from a route handler; a raw caught error's `.message` must never reach a `NextResponse.json` body. Enforced by ESLint sink + two-step `no-restricted-syntax` selectors scoped to `app/api//route.{ts,tsx}`.\*\*

**Rationale:** EXP-170-family extension of the 2026-05-28 `safeErrorJson` decision. PR #604 swept 100 route files / 134 sites off the `error instanceof Error ? error.message : "…"` response anti-pattern onto `safeErrorJson`. Intentional messages (quiz/exam submit not-found/already-submitted/expired, profile/avatar/cover validation, event-register "Event mismatch", `PaidCourseEnrollmentError`) now throw `DomainError`, which `safeErrorJson` forwards verbatim (status + message, no details/stack) while collapsing every other error to a generic message. Two lint selectors close recurrence: `error.message` directly inside `NextResponse.json(...)`, and capture into a `message`/`errorMessage`/`msg`/`errMsg` local. KNOWN GAP (EXP-189): `src/lib/**` is globally ESLint-ignored so the rule can't fire there — no current leak, but `prisma-error.handler.ts` P2002 column-name disclosure lives in that tree. Took 3 gatekeeper attempts (#594→#599→#604).

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-28-experts-agent-digest.md]]
