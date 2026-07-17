---
title: "2026-05-21 Experts Agent Digest"
date: "2026-05-21"
tags: [agent, digest, project/experts]
category: "daily"
source: "automation"
source_id: "Raw/sources/2026-05-21-experts-agent-digest.md"
---

# 2026-05-21 Experts Agent Digest

Window: 2026-05-20T00:00:00Z → 2026-05-21T23:59:59Z.

---

## New today

Issues opened by routines (body contains `<!-- agent-fp:`) in the last 24 h.

### Wave 1 — Bug-finder (EXP-48..53)

| Linear ID | FP | Priority | Status | One-liner |
|---|---|---|---|---|
| [EXP-48](https://linear.app/experts/issue/EXP-48) | `18063f5fd318` | High | **Resolved** | Orphan-sweep `every` filter silently skips files with multiple orphaned attachments — fixed PR #349 |
| [EXP-49](https://linear.app/experts/issue/EXP-49) | `197d47660102` | High | **Resolved** | Unbounded `findMany` in `runStorageJanitorSweep` OOM-crashes Next.js — fixed PR #350 |
| [EXP-50](https://linear.app/experts/issue/EXP-50) | `fc9c31c29e7a` | High | **Resolved** | No ownership check on `attachmentId` allows IDOR cross-course file linkage — fixed PR #347 |
| [EXP-51](https://linear.app/experts/issue/EXP-51) | `9a8cca3642bf` | High | **Resolved** | TOCTOU: R2 deleted before DB guard in pending-file sweep — fixed PR #348 |
| [EXP-52](https://linear.app/experts/issue/EXP-52) | `43a087f194c2` | Critical | **Resolved** | JSON-LD `JSON.stringify` does not escape `</script>`; stored XSS on public course pages — fixed PR #369 |
| [EXP-53](https://linear.app/experts/issue/EXP-53) | `95412bb984d6` | Medium | **Open** | Creator route guard disabled in `proxy.ts`; `/creator/*` accessible to any authenticated user |

### Wave 2 — Incident triage into Linear (EXP-54..71)

All 18 historical security incidents (incident#1..18 in `~/brain-v2/Raw/reviews/`) were triaged into Linear today. Each issue body begins with `<!-- agent-fp: <12-hex> -->`.

| Linear ID | FP | Priority | Status | One-liner |
|---|---|---|---|---|
| [EXP-54](https://linear.app/experts/issue/EXP-54) | `eb17b849c258` | Urgent | Done | /internal/debug/* credential leak + community IDOR + markdown XSS + Tabby fail-open + CRON_SECRET bypass |
| [EXP-55](https://linear.app/experts/issue/EXP-55) | `23e901d2126d` | High | Done | /internal/upload allows text/html, text/javascript under attacker-chosen domain/entityId |
| [EXP-56](https://linear.app/experts/issue/EXP-56) | `31a9d52e12b4` | High | Done | Course/event thumbnail IDOR — Prisma `where:` missing owner |
| [EXP-57](https://linear.app/experts/issue/EXP-57) | `bf13d711cd77` | Medium | In Progress | Per-user storage quota missing; rate-limit shipped PR #310, quota open |
| [EXP-58](https://linear.app/experts/issue/EXP-58) | `32f9c0969d97` | High | Done | Upload transactional integrity: pending→ready + storage-janitor + orphan sweep (PRs #311, #337) |
| [EXP-59](https://linear.app/experts/issue/EXP-59) | `07157ef04386` | Medium | Done | Upload routes re-verify `buffer.byteLength` after `arrayBuffer()` — PR #312 |
| [EXP-60](https://linear.app/experts/issue/EXP-60) | `57b049e61f2c` | Low | Canceled | CDN/Traefik/R2 hardening — infra-side, deferred |
| [EXP-61](https://linear.app/experts/issue/EXP-61) | `c6b67de10a28` | High | Done | Anonymous data exposure on course-detail/presence/viewers — PR #314 |
| [EXP-62](https://linear.app/experts/issue/EXP-62) | `5bff6a2d626a` | Medium | Done | Thumbnail extension derived from validated MIME, not client filename — PR #315 |
| [EXP-63](https://linear.app/experts/issue/EXP-63) | `80198be9cf82` | Medium | In Progress | Drop `raw.githubusercontent.com` from `font-src`; CSP report endpoint shipped (#316); self-hosted fonts open |
| [EXP-64](https://linear.app/experts/issue/EXP-64) | `3570f3824763` | Medium | In Progress | Lesson-resource Content-Disposition + per-domain MIME allowlist + RFC 5987 (steps 1+2 done, step 3 open) |
| [EXP-65](https://linear.app/experts/issue/EXP-65) | `0997a3069ae4` | High | Done | Host-header injection in `getRequestBaseUrl` on `/share/*` — PR #320 |
| [EXP-66](https://linear.app/experts/issue/EXP-66) | `df256311e5f9` | Low | Done | CSP dev-mode `unsafe-eval` isolated + prod-locked regression test — PR #329 |
| [EXP-67](https://linear.app/experts/issue/EXP-67) | `713f7dfac482` | Medium | In Review | Creator curriculum upload UX & auth gaps (dropzones, quiz 403, lesson-resource position) |
| [EXP-68](https://linear.app/experts/issue/EXP-68) | `95b437cb68ba` | Urgent | Todo | Paid-content bypass via progress/quiz + Noon API credentials logged |
| [EXP-69](https://linear.app/experts/issue/EXP-69) | `a0b8f55e493a` | Urgent | Todo | Production/staging secrets committed to git + role revocation does not invalidate JWT |
| [EXP-70](https://linear.app/experts/issue/EXP-70) | `e20b15a445a8` | High | Todo | Password-reset URL poisoning via Host/Origin + forgot-password enumeration + /console/health disclosure |
| [EXP-71](https://linear.app/experts/issue/EXP-71) | `e2e233c4f650` | High | In Review | App takes full CSP ownership with per-request nonce + JsonLd conversions (Phase 4B) |

---

## Repeated pattern

Files / symbols appearing 3+ times in the findings index within the last 30 days.

| File / Symbol | Count | Issues |
|---|---|---|
| `storage-janitor.sweeps.ts` | 3 | EXP-48 (`runOrphanAttachmentSweep`), EXP-49 (`runStorageJanitorSweep`), EXP-51 (`runStorageJanitorSweep`) |

**Signal**: The storage-janitor sweep module produced 3 of the 6 bug-finder findings this window, spanning three distinct defect classes (predicate logic error, missing pagination, race condition). All three are now resolved. Recommend a dedicated integration-test harness against a real Prisma client — not mocks — before the next sweep iteration ships.

---

## Resolved since yesterday

| Linear ID | FP | Title | Resolution |
|---|---|---|---|
| EXP-50 | `fc9c31c29e7a` | IDOR on `attachmentId` in lesson-asset create | Merged PR #347 (`eb9dea35`): ownership guard added |
| EXP-51 | `9a8cca3642bf` | TOCTOU: R2 before DB guard in pending-file sweep | Merged PR #348 (`5877e626`): DB-first ordering |
| EXP-48 | `18063f5fd318` | Orphan-sweep `every` filter guard incorrect | Merged PR #349 (`b8c72fe1`): `some + every OR` predicate with stateful mock — attempt 2 |
| EXP-49 | `197d47660102` | Unbounded `findMany` OOM-crash | Merged PR #350 (`dc51aba2`): `take:/orderBy:` + module-level lock + test-isolation reset — attempt 2 |
| EXP-52 | `43a087f194c2` | Stored XSS via `</script>` in JSON-LD | Merged PR #369 (`309778c4`): `escapeJsonForScript` — unicode-escape `<`, `>`, `&`, U+2028, U+2029 |

---

## In-flight fixes

No open agent PRs at end of window. PRs #349, #350 (EXP-48, EXP-49 attempt 2) and PR #369 (EXP-52) all merged today.

---

## Merged PRs

| PR | Merge SHA | Title | Type |
|---|---|---|---|
| [#338](https://github.com/logi-x/experts/pull/338) | `7710a56c` | feat(course-detail): enhance enrollment handling and API query structure | feature |
| [#347](https://github.com/logi-x/experts/pull/347) | `eb9dea35` | fix(lesson-assets): verify attachment ownership before linking (EXP-50) | security |
| [#348](https://github.com/logi-x/experts/pull/348) | `5877e626` | fix(storage-janitor): DB-first delete to prevent TOCTOU (EXP-51) | correctness |
| [#349](https://github.com/logi-x/experts/pull/349) | `b8c72fe1` | fix(storage-janitor): converge orphan sweep on multi-orphan files (EXP-48) [attempt 2] | correctness |
| [#350](https://github.com/logi-x/experts/pull/350) | `dc51aba2` | fix(storage-janitor): bound pending-file sweep + test-isolation reset (EXP-49) [attempt 2] | correctness |
| [#369](https://github.com/logi-x/experts/pull/369) | `309778c4` | fix(security): unicode-escape JSON-LD payload to prevent script-tag breakout (EXP-52) | security |

**Changelog-worthy**: PR #369 (critical stored XSS — `escapeJsonForScript` helper + test). PR #349 (orphan-sweep predicate with stateful mock). PR #350 (OOM bound + test isolation). PR #347 (IDOR). PR #348 (data-corruption race). PR #338 adds `EnrollmentStatusResponse` type + mutation in `useCourseDetail`.

---

## Migrations / env / infra changes

No Prisma migration files landed in this window.

**Crontab hardening** (commits `221b691b`, `18cb272f`): Prepend `bash` to all cron entries; update `ROUTINE_LOG_DIR` path — low-risk ops, no schema change.

**Routines infrastructure** (commits `1d9b540a`, `b2769092`, `fc1883a5`):
- New automated routine suite: vulnerability scanning (R2), bug detection (R1), bug fixing (R3), docs digest (R4), agent PR gatekeeper.
- Pool dispatcher (`_pool-dispatch.sh`) + worktree setup (`_setup-worktrees.sh`): parallel R3 bug-fixing with slot locking.
- R3 refactor: picks `Needs Rework` issues; tracks attempt count; escalates to `Needs Human` at cap. Gatekeeper validates verdicts by current PR head SHA.

---

## Architectural notes

1. **DB-first ordering for all storage mutations** (EXP-51 / PR #348): DB guard runs before any R2/blob-store call. Applies to all future storage mutation flows. *Decision-Log row present from prior digest pass.*

2. **Pool dispatcher pattern for R3 bug-fixing** (commit `b2769092`): Parallel worktree slots with file-lock-based slot assignment allow concurrent bug fixes without mutual interference. First pool-of-workers pattern in the routines layer. *→ Decision-Log row added.*

3. **Attempt cap + Needs Human escalation** (commit `fc1883a5`): R3 tracks fix attempts per issue; moves issues to `Needs Human` at cap. Prevents infinite retry loops. *→ Decision-Log row added.*

4. **Prisma `every` semantics trap** (EXP-48 root cause / PR #349): `every: {id: X}` over a non-empty relation is vacuously true when other members exist not matching `id = X`. Correct guard: `some: {id: X} + every: {OR: [{id: X}, {allScopesNone}]}`. Fixed in attempt 2 with stateful Prisma mock.

---

## Docs that need updating

| File | Reason |
|---|---|
| `apps/experts-app/proxy.ts` | EXP-53: creator route guard still needs re-enabling |
| `apps/experts-app/src/lib/upload/guards/upload-quota.guard.ts` | EXP-57: per-user storage quota not yet implemented |
| `_routines/README.md` | Document pool dispatcher, worktree setup, attempt tracking, Needs Human escalation |
| `Raw/sources/2026-05-20-experts-orphan-sweep-and-role-gate.md` | R2-first ordering noted there was superseded by EXP-51 fix (PR #348) |

---

## Still open

| Linear ID | Status | Severity | Summary |
|---|---|---|---|
| EXP-53 | open | Medium | Creator route guard disabled in `proxy.ts`; `/creator/*` accessible to any authenticated user |
| EXP-57 | In Progress | Medium | Per-user storage quota missing on upload route |
| EXP-63 | In Progress | Medium | Self-hosted fonts pending; `raw.githubusercontent.com` still in `font-src` |
| EXP-64 | In Progress | Medium | Lesson-resource Content-Disposition step 3 (per-domain MIME allowlist) open |
| EXP-67 | In Review | Medium | Creator curriculum upload UX & auth gaps (PR open, awaiting merge) |
| EXP-68 | Todo | Urgent | Paid-content bypass + Noon credentials logged — 3 open findings |
| EXP-69 | Todo | Urgent | Production/staging secrets in git + JWT role revocation gap |
| EXP-70 | Todo | High | Password-reset poisoning + enumeration + /console/health disclosure |
| EXP-71 | In Review | High | CSP Phase 4B production cutover pending |

---

## Needs human attention

1. **EXP-69 — CRITICAL: committed secrets** (`.env.production`, `.env.staging`, `.env.e2e`, `slack.secret` in git history): Immediate rotation required. Action-Tracker deadline 2026-05-23.

2. **EXP-68 — CRITICAL: Noon API credentials logged + paid-content bypass**: `console.log(makeNoonAuthHeader())` writes merchant credentials to runtime logs. Noon credential rotation + log audit required alongside the business-logic gate fix.

3. **EXP-53 — MEDIUM: creator route guard disabled** (flagged 2026-05-20 and twice in this digest): Any authenticated user can reach `/creator/*`. Needs triage assignment.

4. **EXP-70 — HIGH: password-reset URL poisoning**: Attacker-controlled `Host`/`Origin` poisons the reset link. No PR yet.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
