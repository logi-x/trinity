---
title: "2026-05-22 Experts Agent Digest"
date: "2026-05-22"
tags: [agent, digest, project/experts]
category: "daily"
source: "automation"
source_id: "Raw/sources/2026-05-22-experts-agent-digest.md"
---

# 2026-05-22 Experts Agent Digest

Window: 2026-05-22T00:00:00Z → 2026-05-22T23:59:59Z.

---

## New today

Issues created 2026-05-22 with agent fingerprints (R1/R2 authored):

| ID | FP | Title | Priority | Status |
|---|---|---|---|---|
| EXP-78 | `50a0efcf0017` | [security] JWT role-staleness in event thumbnail upload — revoked admin bypasses host check | Medium | Backlog |
| EXP-76 | `226fb913256a` | [bug] Course progress POST: lesson-to-course ownership check skipped for completed=false — cross-course completion counter inflation | High | Todo |
| EXP-75 | `b9f675e5f4db` | [bug] Certificate POST: caller-supplied courseTitle written to DB — credential title forgery | High | In Progress |

Non-routine issues also created today (no agent-fp; not listed above): EXP-74 ([security] URGENT: Rotate Noon merchant credentials, Urgent, ops-only), EXP-73 ([security] EXP-68 follow-ups: schema constraint + body-parse ordering + modules-route test, High), EXP-72 ([security] Per-user storage quota on /api/v1/internal/upload, Medium, split from EXP-57).

---

## Repeated pattern

**`storage-janitor.sweeps.ts` — 3× in last 30 days (EXP-48, EXP-49, EXP-51):** all three issues resolved today (PRs #348, #349, #350). Pattern is closed; no new storage-janitor findings filed this window.

**JWT role-staleness — emerging pattern (2× in 2 days, not yet 3×):** EXP-69 (approve/reject routes deriving `isAdmin` from JWT rather than DB) was resolved today via PR #375. On the same day, EXP-78 was filed against the event-thumbnail route where PR #378 introduced a new host check using `session.user.isAdmin` (JWT-derived) rather than a DB lookup. Two distinct surfaces in two consecutive days. Not yet at the 3× threshold but a strong signal: any write endpoint gating on an admin or host role via JWT claim carries the same 30-day revocation gap.

---

## Resolved since yesterday

Seven issues transitioned to Done during this window:

| ID | Title | Completed at |
|---|---|---|
| EXP-71 | CSP Phase 4B: app takes full CSP ownership | 2026-05-22T01:00:45Z |
| EXP-69 | Committed secrets + JWT role revocation gap | 2026-05-22T04:15:23Z |
| EXP-68 | Paid-content bypass + Noon credentials logged | 2026-05-22T05:09:55Z |
| EXP-67 | Creator curriculum upload UX & auth gaps | 2026-05-22T01:03:23Z |
| EXP-64 | Content-Disposition + per-domain MIME allowlist + RFC 5987 | 2026-05-22T06:24:32Z |
| EXP-63 | Drop raw.githubusercontent.com from font-src; CSP hardening | 2026-05-22T04:15:21Z |
| EXP-57 | Per-user storage quota (quota half split to EXP-72) | 2026-05-22T01:08:05Z |

---

## In-flight fixes

No open Routine 3 PRs at end of window. EXP-75 (certificate courseTitle forgery) moved to In Progress at 2026-05-22T06:34:38Z — work has started but no PR has been opened yet. EXP-70 (password-reset URL poisoning) also moved to In Progress at 2026-05-22T06:32:20Z with no PR yet.

---

## Merged PRs

Fourteen PRs merged in the last 24 hours:

| PR | Title | Linear | Type |
|---|---|---|---|
| #382 | fix(security): EXP-68 HTTP-boundary hardening — paid-content paywall complete | EXP-68 | security |
| #381 | fix(courses): gate enrollment progress updateMany on status="completed" | EXP-68 | security |
| #380 | refactor(csp): separate production-only CSP directives | — | refactor |
| #379 | feat(csp): add Tabby checkout domains to CSP; enhance PostCard priority prop | — | csp |
| #378 | refactor(event-creation): streamline image handling; enhance event access checks | — | refactor |
| #377 | feat(security): add GTM and Google Analytics to CSP | — | csp |
| #375 | fix(auth): derive isAdmin from DB in approve+reject routes (EXP-69) | EXP-69 | security |
| #374 | fix(csp): self-host fonts, remove raw.githubusercontent.com; add upgrade-insecure-requests (EXP-63) | EXP-63 | security |
| #370 | fix(auth): restore /creator route guard in proxy.ts (EXP-53) | EXP-53 | security |
| #369 | fix(security): unicode-escape JSON-LD payload to prevent script-tag breakout (EXP-52) | EXP-52 | security |
| #350 | fix(storage-janitor): bound pending-file sweep + test-isolation reset (EXP-49) [attempt 2] | EXP-49 | correctness |
| #349 | fix(storage-janitor): converge orphan sweep on multi-orphan files (EXP-48) [attempt 2] | EXP-48 | correctness |
| #348 | fix(storage-janitor): DB-first delete in runStorageJanitorSweep to prevent TOCTOU (EXP-51) | EXP-51 | correctness |
| #347 | fix(lesson-assets): verify attachment ownership before linking (EXP-50) | EXP-50 | security |

---

## Migrations / env / infra changes

**No Prisma migrations landed this window.**

**Env cleanup (committed secrets remediation):**
- `.env.production`, `.env.staging`, `.env.e2e`, `slack.secret` deleted from repo (commit `e8b99b71`)
- `.gitignore` updated to exclude all `*.env*` and `*.secret` patterns (commits `cfaaf095`, `e8b99b71`)
- `.env.example` added with safe placeholder values (commit `528b8543`)
- Routine database connection strings updated (`DATABASE_URL`, `SHADOW_DATABASE_URL`) in bug-fixing routine bootstrap (commit `f9372946`)

**No docker-compose or Dockerfile changes.**

**Routines infrastructure (direct pushes to main):**
- 7 new agent files added: accessibility-auditor, ai-engineer, analytics-architect, architecture-reviewer, code-reviewer, concept-architect, database-engineer (commit `68908dd6`)
- Pool dispatcher (`_pool-dispatch.sh`) + worktree setup (`_setup-worktrees.sh`) landed (commits `7d9b8cf8`, `46c3ccf1`)
- R3 validation step added: must pass `pnpm experts:check` + `pnpm experts:test` before committing (commit `578a02fe`)
- Routine secrets now loaded from `~/.experts-routines.env` (commits `16baafd7`, `46c3ccf1`)
- CI: added `DATABASE_URL` and `ZATCA_SDK_CONFIG_PATH` env vars for unit tests (commit `16baafd7`)

---

## Architectural notes

**JWT role-staleness is a systemic vulnerability class.** EXP-69 (approve/reject routes) was resolved today via PR #375 (derive `isAdmin` from DB). Within the same window, PR #378 introduced a new event-thumbnail host check using `session.user.isAdmin` — immediately filed as EXP-78. The pattern: any write endpoint that gates on an admin or host role via a JWT claim is vulnerable to the same 30-day revocation gap. This warrants a Decision Log entry: "All write endpoints that gate on admin/host role MUST derive that role from the DB at request time, not from the JWT claim."

**CSP layer is now fully owned by the app (proxy.ts).** EXP-63 (fonts self-hosted, `upgrade-insecure-requests`/`manifest-src`/`worker-src` added, PR #374) and EXP-71 (per-request nonce + JSON-LD conversions, PR implicit in Done status) both closed today. The Traefik `headers.contentSecurityPolicy` directive should now be dropped from `traefik/` config per EXP-71 deploy instructions — this is a required manual deployment step.

**Routines architecture fully live for the first time.** This window is the first session with all five routines operating simultaneously: R1 (bug detection), R2 (vulnerability scanning), R3 (bug fixing with pool dispatcher + attempt cap), R4 (docs digest), and Gatekeeper. Seven new specialist agent types are available to R3. The pool dispatcher and worktree setup landing in this window complete the R3 parallelism model.

---

## Docs that need updating

- `apps/experts-app/app/api/v1/events/[id]/thumbnail/route.ts` — PR #378 refactored the host check using JWT-derived `isAdmin`; EXP-78 now requires this to be replaced with a DB-derived auth check before the file is considered correct.
- `_routines/README.md` — pool dispatcher (`_pool-dispatch.sh`), 7 new specialist agent types, verbose mode, secret loading from `~/.experts-routines.env`, and the R3 validation gate (`pnpm experts:check` + `pnpm experts:test`) all landed this window and are not yet documented.
- `traefik/` config — CSP Phase 4B is complete; the Traefik `headers.contentSecurityPolicy` header must be dropped now that `proxy.ts` owns the full CSP. This is a required deployment action per EXP-71 scope.
- `SECURITY.md` — updated security policy landed (commits `b513c826`, `a18c791c`); verify the file reflects current state post-EXP-68/EXP-69 remediation.

---

## Still open

| ID | Status | Severity | Summary |
|---|---|---|---|
| EXP-78 | Backlog | Medium | JWT role-staleness in event thumbnail host check (new today, same class as EXP-69) |
| EXP-76 | Todo | High | Course progress POST: lesson-to-course ownership check missing for completed=false path |
| EXP-75 | In Progress | High | Certificate POST: caller-supplied courseTitle written to DB — credential title forgery |
| EXP-74 | Todo | Urgent | Noon credential rotation + log audit (ops ticket, human required, no agent-fp) |
| EXP-73 | Todo | High | EXP-68 follow-ups: schema constraint + body-parse ordering + modules-route test |
| EXP-72 | Todo | Medium | Per-user storage quota on /api/v1/internal/upload (split from EXP-57) |
| EXP-70 | In Progress | High | Password-reset URL poisoning + account enumeration + /console/health |

---

## Needs human attention

1. **EXP-74 (Urgent) — Noon credential rotation + log audit:** ops-only ticket, explicitly excluded from R3 scope, no agent-fp. Credentials were logged and must be rotated by a human with access to the Noon merchant dashboard. Log audit required to confirm blast radius.
2. **EXP-70 (High) — Password-reset URL poisoning + account enumeration + /console/health:** In Progress as of 2026-05-22T06:32:20Z but no PR opened by end of window. Appears in a second consecutive digest without a fix. Needs a check on whether R3 is blocked or has not yet scheduled a fix attempt.
3. **EXP-69 / EXP-68 — credential rotation still outstanding:** Code fixes are Done (PRs #375, #382) but the ops-side credential rotation for both the committed secrets (EXP-69) and the Noon credentials logged in plaintext (EXP-68) has not been confirmed complete. Both require human action outside the codebase.
4. **Traefik CSP header removal:** EXP-71 is marked Done but the corresponding Traefik config change (dropping `headers.contentSecurityPolicy`) is a deployment-time action that must be performed manually. No PR was filed for this step.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
