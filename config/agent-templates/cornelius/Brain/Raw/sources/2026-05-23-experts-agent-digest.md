---
title: "2026-05-23 Experts Agent Digest"
date: "2026-05-23"
tags: [agent, digest, project/experts]
category: "daily"
source: "automation"
source_id: "Raw/sources/2026-05-23-experts-agent-digest.md"
---

# 2026-05-23 Experts Agent Digest

Window: 2026-05-22T00:00:00Z → 2026-05-23T23:59:59Z.

---

## New today

Issues created with agent fingerprints (`<!-- agent-fp:`) in the last 24h:

| ID | FP | Title | Priority | Status |
|---|---|---|---|---|
| EXP-88 | `0253a1037e64` | [security] JWT role-staleness in PUT /api/v1/events/[id] — revoked admin edits any event | Urgent | Todo |
| EXP-89 | `5b2fd78b32ae` | [security] JWT role-staleness in DELETE /api/v1/events/[id] — revoked admin permanently deletes any event | Urgent | Todo |
| EXP-90 | `c53cfd8af8a6` | [security] JWT role-staleness in GET /api/v1/events/[id] — revoked admin reads private meeting credentials | High | Todo |
| EXP-87 | `2d5b36fd7b73` | [security] File.size column is Int32 — overflows at ~2.1GB; migrate to BigInt before any tier exceeds 2GB | High | Backlog |
| EXP-86 | `eda762c80f1e` | [security] Extract enforceStorageQuota guard + apply to all R2-write routes (EXP-72 follow-up) | Medium | Backlog |
| EXP-85 | `f5c264dbf6b4` | [security] JWT role-staleness in event clone — revoked admin bypasses host check (EXP-78 follow-up) | Medium | **Done** |
| EXP-84 | `d72831b12e3e` | [security] JWT role-staleness in event list — revoked admin bypasses host check (EXP-78 follow-up) | Medium | **Done** |
| EXP-83 | `2b75b1305d16` | [bug] VALIDATE course_isfree_price_consistency constraint after prod data sweep (EXP-73 follow-up) | Low | Backlog |
| EXP-82 | `04250008207c` | [bug] Admin storage dashboard + over-quota alerts | Low | Backlog |
| EXP-81 | `834b7e67b87f` | [bug] Stale pending file row cleanup + R2 orphan reaper | Low | Backlog |
| EXP-80 | `c3eb6a48c4db` | [security] Race-safe storage usage ledger (UserStorageUsage + reservation flow) | Medium | Backlog |
| EXP-79 | `a619815990b0` | [bug] Validate lessonId UUID in POST /courses/[id]/progress before Prisma — malformed input returns 500 instead of 400 | Medium | **Done** |

Duplicates filed by concurrent scan (cancelled immediately): EXP-91 (dup of EXP-88), EXP-92 (dup of EXP-89), EXP-93 (dup of EXP-90).

---

## Repeated pattern

**JWT role-staleness — 7× in 3 days (EXP-69, EXP-78, EXP-84, EXP-85, EXP-88, EXP-89, EXP-90):** This is the dominant finding class of the week. The same vulnerability — trusting `session.user.isAdmin` (JWT-derived) instead of a live DB lookup — has been found across 7 route surfaces in 3 consecutive days. Four are resolved. Three remain open in a single file: `app/api/v1/events/[id]/route.ts` (GET, PUT, DELETE). The file appeared 3× in today's findings alone, making it the current highest-concentration privilege logic surface in the codebase.

A Decision-Log row from 2026-05-22 covers mutations. A new row added today extends the invariant to sensitive-data reads (EXP-90 demonstrates a GET leaking Zoom credentials and passwords).

**`app/api/v1/events/[id]/route.ts` — 3× today (EXP-88, EXP-89, EXP-90):** After fixes land, a shared `deriveRolesFromDB` guard at the file boundary (not per-handler) is the recommended structural fix.

---

## Resolved since yesterday

Ten issues transitioned to Done during this window:

| ID | Title | Completed at | PR |
|---|---|---|---|
| EXP-85 | JWT role-staleness in event clone | 2026-05-23T00:46:43Z | #410 |
| EXP-84 | JWT role-staleness in event list (POST /events) | 2026-05-22T22:57:59Z | #406 |
| EXP-79 | Validate lessonId UUID before Prisma | 2026-05-22T19:21:21Z | #396 |
| EXP-78 | JWT role-staleness in event thumbnail upload | 2026-05-22T22:32:52Z | #399 |
| EXP-76 | Course progress POST: lesson-to-course ownership | 2026-05-22T18:23:55Z | #392 |
| EXP-75 | Certificate POST: courseTitle from DB | 2026-05-22T08:11:27Z | #390 |
| EXP-74 | Noon credential rotation + log audit (ops) | 2026-05-23T00:55:30Z | — |
| EXP-73 | EXP-68 follow-ups: schema constraint + body-parse | 2026-05-22T22:32:48Z | #398 |
| EXP-72 | Per-user storage quota preflight gate | 2026-05-22T23:35:22Z | #408 |
| EXP-70 | Host-header injection + forgot-password + /console/health | 2026-05-22T22:57:46Z | #407 |

---

## In-flight fixes

No open Routine 3 PRs at end of window. EXP-88, EXP-89, EXP-90 are in `Todo` — R3 has not yet picked them up. EXP-87, EXP-86, and EXP-80–83 are in Backlog and will be queued after EXP-88/89/90 are cleared.

---

## Merged PRs

Twenty PRs merged in the last 24 hours (security-heavy sprint).

**Auth hardening — JWT staleness + HTTP boundary**

| PR | Title | Linear |
|---|---|---|
| #410 | fix(events/clone): derive isAdmin from DB — JWT staleness | EXP-85 |
| #406 | fix(events): derive isAdmin from DB on POST /api/v1/events | EXP-84 |
| #399 | fix(events/thumbnail): derive isAdmin from DB | EXP-78 |
| #375 | fix(auth): derive isAdmin from DB in approve+reject routes | EXP-69 |
| #407 | fix(auth): host-header injection + forgot-password silent success + /console/health admin gate [attempt 2] | EXP-70 |
| #370 | fix(auth): restore /creator route guard in proxy.ts | EXP-53 |
| #382 | fix(security): EXP-68 HTTP-boundary hardening — paid-content paywall complete | EXP-68 |

**Input validation + schema**

| PR | Title | Linear |
|---|---|---|
| #398 | fix(security): EXP-73 follow-ups — schema check + body-parse order + modules test | EXP-73 |
| #396 | fix(courses/progress): validate lessonId + courseId UUIDs before Prisma | EXP-79 |
| #392 | fix(courses/progress): enforce lesson-to-course ownership for completed=false [attempt 2] | EXP-76 |
| #390 | fix(certificates): remove courseTitle from POST body — always source from DB | EXP-75 |
| #381 | fix(courses): gate enrollment progress updateMany on status="completed" | EXP-68 |

**CSP**

| PR | Title | Linear |
|---|---|---|
| #409 | Enhance CSP: allow Cloudflare R2 signed video URLs + R2 integration | — |
| #380 | refactor(csp): separate production-only CSP directives | — |
| #379 | feat(csp): add Tabby checkout domains + PostCard priority prop | — |
| #377 | feat(security): add GTM + Google Analytics to CSP | — |
| #374 | fix(csp): self-host fonts, remove raw.githubusercontent.com, add upgrade-insecure-requests/manifest-src/worker-src | EXP-63 |

**Feature + infra**

| PR | Title | Linear |
|---|---|---|
| #408 | fix(upload): per-user storage quota preflight gate | EXP-72 |
| #378 | refactor(event-creation): streamline image handling + enhance event access checks | — |
| #397 | Dev/update deps | — |

**Semver signal:** PATCH. All changes are security fixes and hardening; one guard feature (#408). No breaking API changes.

---

## Migrations / env / infra changes

**Prisma migration landed (PR #398 — EXP-73):**
- `20260523000000_course_isfree_price_consistency` — adds DB-level `CHECK` constraint on `courses` table enforcing `isFree`/`price` consistency. Non-destructive for clean data; requires a production data sweep before `VALIDATE CONSTRAINT` can run (EXP-83 tracks this follow-up).

**No other schema migrations in this window.**

**CSP — Cloudflare R2 signed video URLs (PR #409):** New external CDN origin added to CSP `media-src`/`connect-src` via `proxy.ts`. Architecture note: runtime-signed CDN domains must use explicit per-bucket origins, not wildcards (new Decision-Log row).

**Routines infrastructure (direct commits to main):**
- R3 priority-sorted queue + early claim collapses 5-minute race window (2026-05-22T23:58)
- R1+R2: agent-fp marker embedded as inline code to survive Linear UPDATE (2026-05-22T18:48)
- R3: attempt-cap loop closed; escalated issues excluded; REST API used for label add (2026-05-22T18:38)
- R5 gatekeeper: hardcoded Todo + label transitions for BLOCK path (2026-05-22T18:34)
- Pool dispatch: preflight checks for clean git slots; argument parsing + index refresh (2026-05-22T18:02, T16:04)
- Worktree creation updated to detached mode (2026-05-22T15:39)
- `.env.example` added; DB connection strings updated for routines (2026-05-22T02:46, T02:37)

Note: 11 direct commits to `main` in this window, all automation/infra. Branch protection should require PR reviews for non-automation commits.

---

## Architectural notes

**JWT invariant broadened to sensitive-data reads (new Decision-Log row):** EXP-90 demonstrates a gap in the 2026-05-22 mutation-scoped invariant. A revoked admin can GET a private event's Zoom link and password via a stale JWT. The sensitivity of the data, not the HTTP verb, now governs whether role must be re-derived from DB.

**EXP-90 risk note:** Reading a Zoom password is an immediate, irreversible confidentiality breach. EXP-88/89 (writes) are reversible in a way that EXP-90 is not. Should be treated with at least equal urgency to the Urgent-ranked write issues.

**`app/api/v1/events/[id]/route.ts` concentration:** Three open vulnerabilities share one file (GET/PUT/DELETE). After EXP-88/89/90 are resolved, a shared `deriveRolesFromDB` guard at the file boundary is recommended.

**Storage dependency chain codified (new Decision-Log row):** EXP-72 merging today produced 5 dependent issues. Chain: EXP-72 → EXP-80 → EXP-81 → EXP-86 → EXP-82. Must be respected — no item may merge before its predecessor is production-stable.

**Int32 overflow deadline (new Decision-Log row):** `File.size` overflow at ~2.1GB is a hard prerequisite of the quota tier roadmap, not a follow-up item.

**CSP signed CDN domains (new Decision-Log row):** Runtime-signed R2 URLs require explicit per-bucket origins to prevent broad CSP bypass.

---

## Docs that need updating

- `apps/experts-app/app/api/v1/events/[id]/route.ts` — All three handlers (GET/PUT/DELETE) still use JWT-derived `isAdmin`. Require DB-derived lookup per architectural invariant.
- `_routines/README.md` — Priority-sorted queue, early claim, R3 attempt-cap fix, R1+R2 inline-code FP marker, R5 gatekeeper BLOCK path improvements all landed this window. Not yet documented.
- `traefik/` config — EXP-71 is Done; the Traefik `headers.contentSecurityPolicy` static header must be dropped. Required manual deployment action not yet confirmed completed.
- `prisma/schema.prisma` — EXP-83 follow-up: `VALIDATE CONSTRAINT course_isfree_price_consistency` requires a production data sweep first. Migration `20260523000000_...` was created NOT VALID.

---

## Still open

| ID | Status | Severity | Summary |
|---|---|---|---|
| EXP-90 | Todo | High | JWT staleness GET /events/[id] — revoked admin reads private meeting credentials (Zoom link + password) |
| EXP-89 | Todo | Urgent | JWT staleness DELETE /events/[id] — revoked admin permanently deletes any event |
| EXP-88 | Todo | Urgent | JWT staleness PUT /events/[id] — revoked admin edits any non-archived event |
| EXP-87 | Backlog | High | File.size Int32 overflow at ~2.1GB — time bomb before quota tiers exceed 2GB |
| EXP-86 | Backlog | Medium | Extract enforceStorageQuota guard + apply to all R2-write routes |
| EXP-83 | Backlog | Low | VALIDATE course_isfree_price_consistency after prod data sweep |
| EXP-82 | Backlog | Low | Admin storage dashboard + over-quota alerts |
| EXP-81 | Backlog | Low | Stale pending file cleanup + R2 orphan reaper |
| EXP-80 | Backlog | Medium | Race-safe storage usage ledger |
| EXP-77 | Backlog | Medium | Split user uploads to files.experts.com.sa (infra, human-only, no agent-fp) |

---

## Needs human attention

1. **EXP-90 (High) — JWT staleness on GET /events/[id]:** Revoked admin can read private meeting credentials (Zoom URL + password). Immediate, irreversible confidentiality breach. R3 will pick up as Todo but should be batched with EXP-88/89 in a single PR for `app/api/v1/events/[id]/route.ts`.

2. **EXP-88 + EXP-89 (Urgent) — JWT staleness on PUT/DELETE /events/[id]:** Both in Todo. All three EXP-88/89/90 should be batched in one PR to close the remaining surface in a single file.

3. **Traefik CSP header removal (3rd consecutive digest):** EXP-71 is Done but the Traefik `headers.contentSecurityPolicy` static header has not been confirmed removed. Has appeared in the 2026-05-21, 2026-05-22, and 2026-05-23 digests. Requires human with VPS access.

4. **EXP-77 — Split user uploads to files.experts.com.sa (EXP-64 Step 4):** Requires DNS + bucket + URL-mapper change. No agent-fp; human-only. Appeared in 2026-05-22 digest and again today. Needs triage assignment.

5. **EXP-87 (High) — File.size Int32 overflow:** Not urgent today (quota is 1GB uniform) but is a hard prerequisite of the quota tier roadmap. Must be scoped before any tier exceeds 2GB.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
