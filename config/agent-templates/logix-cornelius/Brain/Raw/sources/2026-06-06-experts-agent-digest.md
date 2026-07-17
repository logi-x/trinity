---
title: "2026-06-06 Experts Agent Digest"
date: "2026-06-06"
tags: [agent, digest, project/experts]
category: "daily"
source: "automation"
source_id: "Raw/sources/2026-06-06-experts-agent-digest.md"
---

# Experts Agent Digest — 06 June 2026

**Window:** 2026-06-05T00:00:00Z → 2026-06-06T23:59:59Z  
**Prior digest:** [[Raw/sources/2026-06-03-experts-agent-digest.md]]

---

## Summary Table

| Metric | Count |
|--------|-------|
| New agent-fp issues (today) | 0 |
| Resolved since yesterday | 33 |
| In-flight fixes (In Review) | 2 (EXP-120, EXP-133 — carried) |
| Merged PRs | 21 |
| Needs human attention | 5 |

---

## New Today

No new issues filed by routines today. The R3 scanner produced zero new findings in this 24h window. This is consistent with the prior session's aggressive backlog sweep (33 issues resolved), which likely reduced scan surface significantly.

---

## Repeated Pattern

From `Raw/agent-state/findings-index.md` — files/symbols appearing 3+ times in last 30 days:

| Pattern | Occurrences (30d) | State Today |
|---------|-------------------|-------------|
| `storage-reservation.ts` | **3 issues** (EXP-122, EXP-124, EXP-127) | **All resolved today** via PR #857. Race-to-negative, double-release, IDOR — full class closed. |
| `.github/workflows/experts-app.yml` (injection class) | **4 issues** (EXP-261✓, EXP-279✓, EXP-176✓, EXP-304✓) | **All resolved** today (EXP-304, EXP-176 via PR #866). CI injection class fully closed. |
| `ask-ai-assistant.ts` | **4 issues** (EXP-223 open, EXP-232 open, EXP-239✓, EXP-252✓) | EXP-252 resolved today (PR #858 FOR UPDATE). EXP-223 prompt-injection + EXP-232 AskAiDomainError still open. |
| **Community API domain (total)** | **20+ issues** (EXP-242–304 range) | EXP-295 (DELETE lock) + EXP-296 (PUT TOCTOU) remain open. EXP-297/298/299/300/301 resolved today. EXP-293 auth-before-try (37-handler class) still In Progress. |
| **Tabby payment paths** | **5 issues** (EXP-129✓, EXP-307✓, EXP-308✓, EXP-309✓, EXP-305 open) | All geo/auth/currency fixes resolved. EXP-305 (paid-but-not-enrolled remediation) still awaiting owner decision. |

---

## Resolved Since Yesterday

Issues whose Linear status flipped to Done on 2026-06-05 (33 total):

### Agent-pipeline governance (PR #871)

| Issue | Title | Closed By |
|-------|-------|-----------|
| [EXP-42](https://linear.app/experts/issue/EXP-42) | Define agent finding intake contract | PR #871 |
| [EXP-43](https://linear.app/experts/issue/EXP-43) | Define vulnerability finding template | PR #871 |
| [EXP-44](https://linear.app/experts/issue/EXP-44) | Define bug finding template | PR #871 |
| [EXP-45](https://linear.app/experts/issue/EXP-45) | Define implementation handoff contract | PR #871 |
| [EXP-46](https://linear.app/experts/issue/EXP-46) | Define validation evidence checklist | PR #871 |
| [EXP-47](https://linear.app/experts/issue/EXP-47) | Define agent/subagent runbooks | PR #871 |

### Storage (PRs #857–#863)

| Issue | Title | Closed By |
|-------|-------|-----------|
| [EXP-103](https://linear.app/experts/issue/EXP-103) | Migrate 5 upload routes to atomic reserveStorageBytes | PR #859 |
| [EXP-106](https://linear.app/experts/issue/EXP-106) | Wire storage quota-warning notifications | PR #861 |
| [EXP-109](https://linear.app/experts/issue/EXP-109) | Schema-qualify backfill-user-storage-usage refs | PR #862 |
| [EXP-122](https://linear.app/experts/issue/EXP-122) | Reservation ledger race-to-negative | PR #857 |
| [EXP-124](https://linear.app/experts/issue/EXP-124) | Reservation double-release ledger negative | PR #857 |
| [EXP-127](https://linear.app/experts/issue/EXP-127) | Advisory lock int32 birthday collision at ~55k users | PR #857 |
| [EXP-128](https://linear.app/experts/issue/EXP-128) | user_storage_usage.used_bytes no non-negative CHECK | PR #857 |
| [EXP-149](https://linear.app/experts/issue/EXP-149) | checkAndSendStorageAlerts HAVING guard dropped | PR #860 |
| [EXP-202](https://linear.app/experts/issue/EXP-202) | resolveStorageTier test coverage | PR #863 |
| [EXP-321](https://linear.app/experts/issue/EXP-321) | R2_BUCKET_BACKUPS env declared but unread | PR #864 |

### Payments / i18n

| Issue | Title | Closed By |
|-------|-------|-----------|
| [EXP-107](https://linear.app/experts/issue/EXP-107) | cf-ipcountry header DB-skip on spoofed origin | PR #868 (spinoff, already-fixed) |
| [EXP-108](https://linear.app/experts/issue/EXP-108) | Subscription checkout locale collapses Spanish → English | PR #869 |
| [EXP-308](https://linear.app/experts/issue/EXP-308) | Tabby verify currency ternary always coerces to SAR | PR #868 |
| [EXP-309](https://linear.app/experts/issue/EXP-309) | Tabby verify: no auth() check — unauthenticated enrollment completion | PR #868 |
| [EXP-307](https://linear.app/experts/issue/EXP-307) | Tabby geo-guard stub already present on subscription verify | PR #868 (spinoff, already-fixed) |

### Community moderation (PRs #851, #852)

| Issue | Title | Closed By |
|-------|-------|-----------|
| [EXP-297](https://linear.app/experts/issue/EXP-297) | TOCTOU in thumbnail upload bypasses moderation lock | PR #851 |
| [EXP-298](https://linear.app/experts/issue/EXP-298) | GET /comments has no post visibility check | PR #852 |
| [EXP-299](https://linear.app/experts/issue/EXP-299) | POST /comments no rate limit | PR #852 |
| [EXP-300](https://linear.app/experts/issue/EXP-300) | Internal upload community case ignores adminLockedAt | PR #851 |
| [EXP-301](https://linear.app/experts/issue/EXP-301) | GET /comments silent truncation — no hasMore signal | PR #852 |

### Courses / AI

| Issue | Title | Closed By |
|-------|-------|-----------|
| [EXP-252](https://linear.app/experts/issue/EXP-252) | persistAskAiExchange TOCTOU — FOR UPDATE missing | PR #858 |
| [EXP-285](https://linear.app/experts/issue/EXP-285) | Course submit non-atomic | PR #856 |
| [EXP-302](https://linear.app/experts/issue/EXP-302) | Exam reset POST non-atomic | PR #856 |

### Admin / UI / Docs

| Issue | Title | Closed By |
|-------|-------|-----------|
| [EXP-306](https://linear.app/experts/issue/EXP-306) | Dead sonner.tsx Toaster wrapper | PR #870 |
| [EXP-313](https://linear.app/experts/issue/EXP-313) | mapEventToListItemDTO emits host email on public GET (spinoff, already-fixed) | PR #868 context |
| [EXP-314](https://linear.app/experts/issue/EXP-314) | Course instructor email in public hashtag/detail (spinoff, already-fixed) | PR #868 context |
| [EXP-322](https://linear.app/experts/issue/EXP-322) | Admin events moderation console | PRs #853, #855, #867 |
| [EXP-323](https://linear.app/experts/issue/EXP-323) | course-edit.guard.ts skips adminLockedAt (spinoff, already-fixed) | verified on main |

### Infra / CI

| Issue | Title | Closed By |
|-------|-------|-----------|
| [EXP-176](https://linear.app/experts/issue/EXP-176) | CI bake-env exports all credentials via set -a | PR #866 |
| [EXP-274](https://linear.app/experts/issue/EXP-274) | No container memory limits — OOM hazard | PR #865 |
| [EXP-275](https://linear.app/experts/issue/EXP-275) | R2 no automated backup — deletion unrecoverable | PR #864 |
| [EXP-304](https://linear.app/experts/issue/EXP-304) | git fetch missing -- separator in CI | PR #866 |

---

## In-Flight Fixes

| Issue | Title | Status | Since |
|-------|-------|--------|-------|
| [EXP-120](https://linear.app/experts/issue/EXP-120) | CRON_SECRET timing-safe compare fail-open on undefined | In Review (per index) | carried |
| [EXP-133](https://linear.app/experts/issue/EXP-133) | CRON_AUTH_TOKEN timing-safe compare fail-open on undefined | In Review (per index) | carried |

> Note: Linear `In Review` query returned empty; EXP-120/EXP-133 status is as of last findings-index update (2026-06-06T00:00Z). Verify live state before acting.

---

## Merged PRs

| PR | Title | Domain | Issues Closed |
|----|-------|--------|---------------|
| [#871](https://github.com/logi-x/experts/pull/871) | docs(agent-pipeline): intake/triage/handoff/validation/runbooks | Docs | EXP-42–47 |
| [#870](https://github.com/logi-x/experts/pull/870) | chore(ui): remove unused sonner.tsx Toaster | UI | EXP-306 |
| [#869](https://github.com/logi-x/experts/pull/869) | fix(payments): Spanish reachable on Tabby checkout | Payments/i18n | EXP-108 |
| [#868](https://github.com/logi-x/experts/pull/868) | fix(payments): auth+ownership on Tabby verify; currency mismatch | Payments/Security | EXP-308, EXP-309 |
| [#867](https://github.com/logi-x/experts/pull/867) | feat(admin): Orbit Foundation 1a — single nav source of truth | Admin | EXP-322 (slice) |
| [#866](https://github.com/logi-x/experts/pull/866) | fix(ci): git arg-injection + bake-env credential leak | CI/Security | EXP-304, EXP-176 |
| [#865](https://github.com/logi-x/experts/pull/865) | fix(infra): container memory limits + Postgres tuning | Infra | EXP-274 |
| [#864](https://github.com/logi-x/experts/pull/864) | feat(infra): R2 point-in-time backup/restore + opt-in cron | Infra | EXP-275, EXP-321 |
| [#863](https://github.com/logi-x/experts/pull/863) | test(storage): async resolveStorageTier edge cases | Storage | EXP-202 |
| [#862](https://github.com/logi-x/experts/pull/862) | fix(storage): schema-qualify backfill-user-storage-usage | Storage | EXP-109 |
| [#861](https://github.com/logi-x/experts/pull/861) | feat(storage): quota-warning email at 90% | Storage | EXP-106 |
| [#860](https://github.com/logi-x/experts/pull/860) | perf(storage): restore HAVING pre-filter + subscriptions index | Storage/Perf | EXP-149 |
| [#859](https://github.com/logi-x/experts/pull/859) | fix(storage): migrate 5 upload routes to atomic reserveStorageBytes | Storage/Security | EXP-103 |
| [#858](https://github.com/logi-x/experts/pull/858) | fix(ai): lock Ask-AI persist re-check with FOR UPDATE | AI/Security | EXP-252 |
| [#857](https://github.com/logi-x/experts/pull/857) | fix(storage): harden reservation ledger — IDOR, lock DoS, quota-bypass | Storage/Security | EXP-122, EXP-124, EXP-127, EXP-128 |
| [#856](https://github.com/logi-x/experts/pull/856) | fix(courses): atomic course-submit + exam-reset | Courses | EXP-302, EXP-285 |
| [#855](https://github.com/logi-x/experts/pull/855) | fix(admin): events console render crash + nav + deep-link | Admin | EXP-322 (follow-up) |
| [#854](https://github.com/logi-x/experts/pull/854) | chore(agent): equip frontend-developer with HeroUI v3 MCP | Platform/Agents | — |
| [#853](https://github.com/logi-x/experts/pull/853) | feat(admin): events moderation console — list + takedown/restore | Admin | EXP-322 |
| [#852](https://github.com/logi-x/experts/pull/852) | fix(community): comments hardening — visibility, rate limit, pagination | Community | EXP-298, EXP-299, EXP-301 |
| [#851](https://github.com/logi-x/experts/pull/851) | fix(community): moderation-lock TOCTOU — thumbnail + internal upload | Community | EXP-297, EXP-300 |

**Semver classification: MINOR** — two new user-facing features (storage quota-warning email, R2 backup), one significant admin UI overhaul (Orbit Foundation 1a). All backwards-compatible; 21 PRs, no breaking API changes.

---

## Migrations / Env / Infra Changes

**Schema changes (PR #857, EXP-122/127/128):**
- `user_storage_reservations`: added nullable `file_id` column + index — reservation hold now extends to pending-file lifetime, closes quota-bypass window.
- `user_storage_usage.used_bytes`: added non-negative `CHECK (used_bytes >= 0)` constraint.
- Advisory lock keyspace: switched from `hashtext()` int32 to `hashtextextended(namespaced_key, 0)` int64 — closes birthday collision at ~55k users.

**Infra changes (PRs #864, #865):**
- `docker/{production,staging,data}/docker-compose.yml`: all containers now have `mem_limit`/`memswap_limit`/`shm_size` ceilings; Postgres tuning via `command:` GUC flags (production 4 GB, staging 2 GB, dev 1 GB).
- New opt-in `experts-prd-r2-backup` cron service under `backup` compose profile — `rclone copy` (add/update, never delete propagation) into `backups/YYYY-MM-DD/<bucket>/` dated prefixes. Enable with `--profile backup`.

**CI changes (PR #866):**
- `.github/workflows/experts-app.yml`: `git fetch ... "$GH_BASE_REF"` now uses `--` separator; bake-env credential export removed (`set -a` pattern replaced with subshell sourcing).

**Storage alert index (PR #860):**
- `CREATE INDEX IF NOT EXISTS subscriptions_user_status_started_idx ON billing.subscriptions (user_id, status, started_at DESC)` — serves LATERAL lookup in `checkAndSendStorageAlerts`.

---

## Architectural Notes

### 1. Admin nav: Orbit Foundation 1a ships single-source-of-truth (PR #867)

`admin-nav.ts` is now the sole nav config — ADMIN_NAV typed `AdminNavItem[]` with i18n keys, programmatic grouping, and optional active-match predicates. Breadcrumb, sidebar, and grouped nav all derive from it. Prior fragmented pattern (navItems in ADMIN_SHELL + hardcoded sidebar + AdminNavbar subcomponents) is removed. This is load-bearing for slices 1b (kit reuse), 1c (⌘K command registry), 1d (dashboard) — all consume the same contract.

### 2. Agent pipeline governance contracts complete (PR #871)

`docs/agent-pipeline/` now contains typed finding contracts, routing rules, and per-stage runbooks grounded in the real R1–R9 routines. Load-bearing conventions codified: fingerprint dedup inline, symmetric-sibling fix batching, TOCTOU snapshot-at-initiation, R3 auto-fix gating (bug+Todo only). Expect reduced R3 → human clarification friction.

### 3. Storage reservation class fully resolved — pattern locked in

EXP-122/124/127/128 all closed today (PR #857). The reservation ledger pattern is now:
- `FOR UPDATE SKIP LOCKED` on reservation select (prevents lock DoS)
- Owner check inside the same locked read (prevents IDOR)
- `file_id` link from reservation → pending file (closes quota-bypass on finalize failure)
- Non-negative DB constraint as last-resort invariant guard
- 64-bit `hashtextextended` advisory lock keyspace (prevents birthday collision)

This pattern should be referenced for any future two-phase write (reserve → finalize → reap).

### 4. R2 backup architecture: copy-not-sync, dated prefixes, compose-profile opt-in

`rclone copy` semantics (add/update only, deletes never propagate) + `backups/YYYY-MM-DD/` isolation means a misconfig/delete on one day cannot erase prior backups. Opt-in `--profile backup` prevents accidental activation. Off-provider/retention is operator-gated. Same opt-in profile pattern should apply to: DR ops, bulk-mutation jobs, and any secret-consuming service.

### 5. CI injection class fully closed

EXP-261 → EXP-279 → EXP-176 → EXP-304 all resolved. The class (untrusted GitHub context values + credential exports) is closed. Established patterns: `env:` block for all `${{ github.* }}` context values; subshell sourcing for secrets; `--` separator before user-controlled refspecs in git calls.

---

## Docs That Need Updating

| File | Required Update |
|------|----------------|
| `apps/experts-app/app/api/v1/community/posts/[id]/route.ts` | **EXP-295 (High, OVERDUE)**: add `adminLockedAt` guard in DELETE; **EXP-296**: atomic PUT lock |
| `apps/experts-app/src/lib/ai/ask/ask-ai-assistant.ts` | EXP-223: sanitize post context before embedding — XML-tag separation |
| 37 route handlers (`graphify-out/safeErrorJson-audit.md`) | EXP-293: move `auth()`/`getUserPermissions()` inside `try`; add `no-auth-before-try` ESLint rule |
| `apps/experts-app/app/api/v1/community/posts/[id]/comments/route.ts` | EXP-294: strip `author.email` from GET payloads and Redis CommentData type |
| `apps/experts-realtime/src/server.ts` | EXP-262: per-user WebSocket connection cap (impl ready, needs cap-value decision) |

---

## Still Open

| Issue | Title | Severity | Since | Notes |
|-------|-------|----------|-------|-------|
| [EXP-295](https://linear.app/experts/issue/EXP-295) | Owner can DELETE admin-locked post | **High** | 2026-06-03 | IMMEDIATE due 2026-06-04 — 2 days overdue |
| [EXP-296](https://linear.app/experts/issue/EXP-296) | TOCTOU in PUT bypasses moderation lock | Medium | 2026-06-03 | Fix together with EXP-295 atomically |
| [EXP-293](https://linear.app/experts/issue/EXP-293) | auth()-before-try class — 37 handlers + lint rule | Medium | 2026-06-03 | In Progress; PR for lint rule + handlers pending |
| [EXP-294](https://linear.app/experts/issue/EXP-294) | Community author email PII in GET payloads | Medium | 2026-06-03 | Frontend dependency check needed |
| [EXP-223](https://linear.app/experts/issue/EXP-223) | AI prompt injection via community post context | Medium | 2026-05-28 | Due 2026-06-06 per Action-Tracker — DUE TODAY |
| [EXP-262](https://linear.app/experts/issue/EXP-262) | No per-user WebSocket connection cap | Medium | 2026-06-01 | Impl ready; blocked on cap-value decision |
| [EXP-305](https://linear.app/experts/issue/EXP-305) | Tabby paid-but-not-enrolled remediation | Medium | 2026-06-06 | Blocked on refund/void/support-queue decision |
| [EXP-120](https://linear.app/experts/issue/EXP-120) | CRON_SECRET timing-safe fail-open | High | carried | In Review (per index) |
| [EXP-133](https://linear.app/experts/issue/EXP-133) | CRON_AUTH_TOKEN timing-safe fail-open | High | carried | In Review (per index) |
| [EXP-140](https://linear.app/experts/issue/EXP-140) | ZATCA invoice no retry on transient errors | High | 2026-05-22 | |
| [EXP-142](https://linear.app/experts/issue/EXP-142) | ZATCA invoice XML injection (unescaped chars) | High | 2026-05-22 | |
| [EXP-278](https://linear.app/experts/issue/EXP-278) | handleCourseSubmit missing pending guard | High | 2026-06-02 | Re-scoped to cert lane (EXP-292 decision) |

---

## Needs Human Attention

Items appearing in 3+ consecutive digests still open:

| Item | In Digest Since | Priority | Action Required |
|------|----------------|----------|-----------------|
| Traefik `headers.contentSecurityPolicy` removal | 2026-05-22 (**16 consecutive digests**) | Medium | **Critically overdue** since 2026-06-01. `curl -sI https://app.experts.com.sa/en \| grep -i content-security` to verify and then remove the Traefik directive. |
| [EXP-141](https://linear.app/experts/issue/EXP-141) R2 API token + Redis password in git history | 2026-05-26 (11 digests) | **Critical** | BFG/filter-repo history rewrite + token rotation still outstanding. |
| [EXP-295](https://linear.app/experts/issue/EXP-295) Owner can DELETE admin-locked post | 2026-06-03 (**IMMEDIATE, due 2026-06-04**) | **High** | One-line guard: `where: { id, adminLockedAt: null }` in DELETE handler or explicit 403 on `adminLockedAt !== null && !isAdmin`. Moderation fully defeated without it. |
| [EXP-223](https://linear.app/experts/issue/EXP-223) AI prompt injection via community post context | 2026-05-28 (8 digests) | Medium | **Due today** per Action-Tracker (2026-06-06). XML-tag separation on post title/description before embedding in AI learner context. |
| [EXP-262](https://linear.app/experts/issue/EXP-262) WebSocket connection cap — decision blocked | 2026-06-01 (6 digests) | Medium | Impl ready in realtime `server.ts`. Needs owner to decide: cap value (e.g. 10/user) + behavior on hit (reject or queue). Then agent ships in one session. |

---

## Source References

- Commits on `logi-x/experts main` today: 27 (PRs #851–#871 range + 5 direct commits)
- Linear issues resolved today: 33 (EXP-42–47, EXP-103, EXP-106–109, EXP-122, EXP-124, EXP-127–128, EXP-149, EXP-176, EXP-202, EXP-252, EXP-274–275, EXP-285, EXP-297–302, EXP-304, EXP-306–309, EXP-313–314, EXP-321–323)
- Linear issues filed today: 0
- Prior digest: [[Raw/sources/2026-06-03-experts-agent-digest.md]]
- Findings index: [[Raw/agent-state/findings-index.md]] (read-only)

---

_Generated by automated digest routine. Exceptional resolution volume: 33 issues closed, 21 PRs merged in 24h — largest single-day close-out since the initial audit sweep (2026-05-20). Storage reservation class fully resolved (EXP-122/124/127/128). CI injection class fully closed (EXP-261/279/176/304). Orbit Foundation admin redesign (1a) shipped. Agent-pipeline governance docs complete. Two items remain critically overdue: EXP-295 (admin-locked DELETE, 2 days past IMMEDIATE deadline) and Traefik CSP removal (16 consecutive digests, 5+ days past due)._

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
