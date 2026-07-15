---
title: "2026-05-26 Experts Agent Digest"
date: "2026-05-26"
tags: [agent, digest, project/experts]
category: "daily"
source: "automation"
source_id: "Raw/sources/2026-05-26-experts-agent-digest.md"
---

# 2026-05-26 Experts Agent Digest

Window: 2026-05-25T00:00:00Z → 2026-05-26T23:59:59Z.

---

## New today

Issues created with agent fingerprints (`<!-- agent-fp:`) in the last 24h:

| # | Title | Status | Severity | FP | Created |
|---|-------|--------|----------|----|---------|
| [EXP-130](https://linear.app/experts/issue/EXP-130) | [bug] Video upload+delete cycle depletes `user_storage_usage` — phantom quota on /internal/upload | Backlog | High | `7e218630cc7a` | 2026-05-26 |
| [EXP-131](https://linear.app/experts/issue/EXP-131) | [bug] Video DELETE removes R2 object before DB transaction — zombie file records | Backlog | High | `106ac9d02e72` | 2026-05-26 |
| [EXP-132](https://linear.app/experts/issue/EXP-132) | [security] Stack trace unconditionally exposed in lesson video route 500 responses | Backlog | Medium | `e9da01839dd5` | 2026-05-26 |
| [EXP-133](https://linear.app/experts/issue/EXP-133) | [security] storage-janitor/orphan-sweep CRON_SECRET timing-unsafe + fail-open (same class as EXP-112) | Backlog | Medium | `2e044db85786` | 2026-05-26 |
| [EXP-134](https://linear.app/experts/issue/EXP-134) | [completeness] R2_BUCKET_STATIC write target misaligned with R2_USER_UPLOADS_PUBLIC_URL after EXP-77 | In Progress | High | `9b6c4687133d` | 2026-05-26 |
| [EXP-135](https://linear.app/experts/issue/EXP-135) | [completeness] R2_BUCKET_CERTIFICATIONS consumed in upload route but absent from .env.example | In Progress | High | `8805a6e85dd0` | 2026-05-26 |
| [EXP-136](https://linear.app/experts/issue/EXP-136) | [completeness] ZATCA_SIMULATOR_ENDPOINT consumed in zatca.config.ts but absent from .env.example | **Done** | Low | `201f41ef3af9` | 2026-05-26 |
| [EXP-137](https://linear.app/experts/issue/EXP-137) | [completeness] ZATCA_REPORTING_ENDPOINT legacy fallback consumed but absent from .env.example | **Done** | Low | `f0d7bcec12bd` | 2026-05-26 |
| [EXP-138](https://linear.app/experts/issue/EXP-138) | [tracker] Post-EXP-77 follow-ups (origin split aftermath) — umbrella for 4 completeness gaps | In Progress | Medium | — (routine tracker) | 2026-05-26 |
| [EXP-139](https://linear.app/experts/issue/EXP-139) | [bug] checkZatca health check returns ok when environment-specific ZATCA endpoint is missing | Backlog | High | `60a80638abd7` | 2026-05-26 |
| [EXP-140](https://linear.app/experts/issue/EXP-140) | [security] ZATCA debug event name mismatch exposes gov API responses via global DEBUG flag | Backlog | Medium | `a6d7ead53650` | 2026-05-26 |
| [EXP-141](https://linear.app/experts/issue/EXP-141) | [security] R2 and Redis credentials committed in plaintext to git history | Backlog | **Critical** | `7471e694ff96` | 2026-05-26 |
| [EXP-142](https://linear.app/experts/issue/EXP-142) | [security] ZATCA_FORCE_REPORT_FAIL and ZATCA_FORCE_SIGN_FAIL lack production APP_ENV guard | Backlog | Medium | `88435ae7f1e0` | 2026-05-26 |
| [EXP-143](https://linear.app/experts/issue/EXP-143) | [security] .claude/agents definitions grant unrestricted Bash to agents processing adversary-controlled content | Backlog | Medium | `4ac8e6df6ea6` | 2026-05-26 |

**14 new** agent-fp issues this window. 2 resolved same-day (EXP-136, EXP-137 via PR #503). 3 in progress (EXP-134, EXP-135, EXP-138). 9 remain in Backlog.

---

## Repeated pattern

Findings appearing 3+ times in the last 30 days (from `Raw/agent-state/findings-index.md`):

| Pattern | Count (distinct issues) | Linear IDs | Current state |
|---------|------------------------|------------|---------------|
| CRON_SECRET timing-unsafe / fail-open on cron routes | 7 | EXP-111, EXP-112, EXP-114, EXP-115, EXP-116, EXP-119, EXP-133 | 1 resolved (EXP-111); 1 review-blocked (EXP-112); 5 open |
| Storage quota ledger correctness gaps | 5 | EXP-80, EXP-121, EXP-122, EXP-124, EXP-130 | 2 resolved (EXP-80, EXP-121); 3 open |
| R2 storage-janitor race / atomic guard failures | 4 | EXP-48, EXP-51, EXP-111, EXP-133 | 2 resolved; 2 open |
| Payment eligibility surface gaps (Tabby/CF) | 3 | EXP-100, EXP-123, EXP-129 | 2 resolved; 1 open (EXP-129) |
| JWT role staleness at write/read endpoints | 6 | EXP-69, EXP-78, EXP-84, EXP-85, EXP-89, EXP-90 | All resolved |

---

## Resolved since yesterday

Linear issues flipped to Done in the last 24h:

| # | Title | Merged via | Resolved at |
|---|-------|-----------|-------------|
| EXP-111 | CRON_SECRET timing-unsafe on pending/orphan reaper routes | PR #478 | 2026-05-26T08:33Z |
| EXP-113 | checkAndSendStorageAlerts has no cron trigger — dead code in production | PR #481 | 2026-05-26T08:36Z |
| EXP-121 | used_bytes never decremented on file deletion — permanent quota lockout | PR #493 | 2026-05-26T08:42Z |
| EXP-123 | CF_ORIGIN_SECRET absent on non-production env trusts all cf-ipcountry headers | PR #498 | 2026-05-26T15:20Z |
| EXP-136 | ZATCA_SIMULATOR_ENDPOINT consumed but absent from .env.example | PR #503 | 2026-05-26T20:05Z |
| EXP-137 | ZATCA_REPORTING_ENDPOINT legacy fallback undocumented | PR #503 | 2026-05-26T20:05Z |

6 resolved. EXP-136 and EXP-137 are same-day create-and-resolve. EXP-80 (PR #470, 2026-05-25T01:32Z) and EXP-100 (PR #465, 2026-05-25T00:02Z) resolved in the tail of yesterday's window are counted in the 2026-05-25 digest.

---

## In-flight fixes

Agent-opened issues currently In Progress with active work:

| # | Title | Opened | PR |
|---|-------|--------|----|
| EXP-134 | R2_BUCKET_STATIC write target misaligned with R2_USER_UPLOADS_PUBLIC_URL | 2026-05-26 | — |
| EXP-135 | R2_BUCKET_CERTIFICATIONS missing from .env.example | 2026-05-26 | — |
| EXP-138 | [tracker] Post-EXP-77 follow-ups (umbrella) | 2026-05-26 | — |

EXP-112 (`review-blocked`) remains stuck since 2026-05-25 — PR #482 received a gatekeeper BLOCK on attempt 1 (missing tests for dual-mode routes: approve-pending, refunds/cleanup). No new attempt opened today.

---

## Merged PRs

7 PRs merged in window 2026-05-25T00:00:00Z → 2026-05-26T23:59:59Z:

| PR | Title | Linear | Merged |
|----|-------|--------|--------|
| [#465](https://github.com/logi-x/experts/pull/465) | fix(payments): address CF origin-secret guard review findings [attempt 2] | EXP-100 | 2026-05-25T00:02Z |
| [#470](https://github.com/logi-x/experts/pull/470) | fix(storage): race-safe storage reservation ledger [attempt 5] | EXP-80 | 2026-05-25T01:32Z |
| [#478](https://github.com/logi-x/experts/pull/478) | fix(storage): timing-safe CRON_SECRET auth on pending/orphan reaper routes | EXP-111 | 2026-05-26T08:33Z |
| [#481](https://github.com/logi-x/experts/pull/481) | fix(storage): wire checkAndSendStorageAlerts cron route and docker-compose entry | EXP-113 | 2026-05-26T08:36Z |
| [#493](https://github.com/logi-x/experts/pull/493) | fix(storage): decrement used_bytes on file deletion to prevent permanent quota lockout | EXP-121 | 2026-05-26T08:42Z |
| [#498](https://github.com/logi-x/experts/pull/498) | fix(payments): fail-closed when CF_ORIGIN_SECRET absent on non-production env | EXP-123 | 2026-05-26T15:20Z |
| [#503](https://github.com/logi-x/experts/pull/503) | fix/zatca env vars unification | EXP-136, EXP-137 | 2026-05-26T20:05Z |

**Semver signal: PATCH.** All merges are security hardening, bug fixes, and operational wiring. No new user-facing API surface. No breaking schema changes this window.

---

## Migrations / env / infra changes

- **`.env.example`** — Major R2 bucket naming overhaul across multiple commits: `R2_BUCKET_MEDIA` → `R2_BUCKET_USER_UPLOADS`; new vars `R2_BUCKET_BACKUPS`, `R2_BUCKET_CERTIFICATIONS`, `R2_API_TOKEN`, `R2_BACKUPS_URL`, `R2_INVOICES_FORCE=true`. ZATCA env var naming clarified (commits `2e1bb46`, `a422e0c`, PR #503).
- **`docker/workers/docker-compose.yml` deleted** in PR #503. **⚠️ Critical:** this file contained R2 API token, R2 secret access key, and Redis password committed in plaintext. Deletion from the working tree does NOT purge them from git object store — `git show <parent-sha>` still exposes credentials. See EXP-141.
- **Docker-compose staging/production** — Storage alerts cron sidecar wired at `0 */4 * * *` schedule (PR #481, EXP-113).
- **R2 bucket refactor attempted then reverted** — Commit `a56de86` refactored storage commands to use `R2_BUCKET_USER_UPLOADS`; commit `f46a100` immediately reverted it. The underlying write/URL mismatch survives as EXP-134.
- **New routine definitions** — `.claude/agents/codebase-completeness-auditor.md` and `.claude/agents/linear-board-auditor.md` added (commits `0c0de88`, `243fb72`, `7f6ffd4`). Both grant Bash tool access — EXP-143 flags this as a prompt-injection risk.

---

## Architectural notes

1. **`.claude/agents` Bash tool grant** (EXP-143, commits `0c0de88`/`243fb72`/`7f6ffd4`): `codebase-completeness-auditor` and `linear-board-auditor` both grant unrestricted Bash to agents that read adversary-controlled Linear issue bodies, PR descriptions, and source code comments. This creates an indirect prompt injection path where a crafted issue body could exfiltrate CI secrets or invoke destructive shell commands during an audit run. Recommendation: restrict Bash to read-only commands (`find`, `grep`, `cat`) in both definitions. **Decision-Log row added.**

2. **R2 bucket/URL mismatch post-EXP-77** (EXP-134): After the EXP-77 origin-split (PR #454), `upload-public-asset.command.ts` continues writing to `R2_BUCKET_STATIC` while `getR2UserUploadsPublicBaseUrl()` returns the `files.experts.com.sa` origin URL. Every user upload is silently written to the wrong bucket. The immediately reverted commit `f46a100` confirms an attempted fix was rolled back, likely because it surfaced EXP-135 simultaneously. This is a production-invariant failure: every URL returned for a recent upload points at an object that does not exist on the files-origin CDN.

3. **ZATCA simulator mode refactor** (PR #503, EXP-136/137): `resolveZatcaConfig` now returns `reportingEndpoint: undefined` for the simulator environment; local-only ZATCA clearance validation. `ZATCA_SIMULATOR_ENDPOINT` and the `ZATCA_REPORTING_ENDPOINT` legacy fallback removed from config. EXP-136 and EXP-137 closed same-day.

4. **EXP-138 umbrella tracker** signals that EXP-77 (user-uploads origin split) shipped with 4 post-merge gaps still unresolved 2+ days after merge: EXP-134 (bucket/URL mismatch), EXP-135 (certifications bucket undocumented), seeder URLs pointing at old bucket, and avatar/cover deletion using wrong bucket path. Pattern: origin-split PRs require a post-merge completeness audit to catch mismatch between write path and URL helper.

---

## Docs that need updating

- **ZATCA configuration notes** — `.env.example` now reflects removal of `ZATCA_SIMULATOR_ENDPOINT` and `ZATCA_REPORTING_ENDPOINT` legacy alias. Any brain vault ZATCA setup guide should note that simulator mode uses local validation only (`reportingEndpoint: undefined`); no remote endpoint required.
- **R2 / storage architecture** — `upload-public-asset.command.ts` bucket target is still misaligned (EXP-134); existing storage architecture docs may describe a write path that is incorrect post-EXP-77 split until EXP-134 closes.
- **`.claude/agents` definitions guide** — The new `codebase-completeness-auditor` and `linear-board-auditor` definitions should be documented with explicit security constraints on Bash tool scope (read-only commands only) once EXP-143 is resolved.

---

## Still open

Open agent-filed issues not addressed today:

| # | Title | Severity | Age | Status |
|---|-------|----------|-----|--------|
| EXP-112 | CRON_SECRET timing-unsafe in embedding-janitor sweep route | Medium | 1d | review-blocked (PR #482 gatekeeper BLOCK) |
| EXP-122 | Stale reservation opens quota-bypass window between reserve and finalize | Medium | 1d | open |
| EXP-124 | Storage reservation DELETE lacks user_id ownership check | Medium | 1d | open |
| EXP-125 | reapR2Orphans unbounded R2 listing — OOM DoS in storage-janitor worker | Medium | 1d | open |
| EXP-126 | Admin storage metrics overThreshold query missing LIMIT — unbounded PII export | Medium | 1d | open |
| EXP-127 | hashtext() advisory lock int32 birthday collision at ~55k users | Medium | 1d | open |
| EXP-129 | Tabby verify/webhook paths bypass KSA geo-restriction entirely | High | 1d | open |
| EXP-103 | 5 upload routes still bypass enforceStorageQuota | High | 2d | open |
| EXP-130 | Video upload+delete cycle depletes user_storage_usage (EXP-121 regression) | High | <1d | open (new today) |
| EXP-131 | Video DELETE removes R2 object before DB transaction | High | <1d | open (new today) |
| EXP-132 | Stack trace unconditionally exposed in lesson video 500 responses | Medium | <1d | open (new today) |
| EXP-133 | orphan-sweep CRON_SECRET timing-unsafe + fail-open (same class as EXP-112) | Medium | <1d | open (new today) |
| EXP-139 | checkZatca health check false-ok when env-specific ZATCA endpoint missing | High | <1d | open (new today) |
| EXP-140 | ZATCA debug event exposes gov API responses via DEBUG=true | Medium | <1d | open (new today) |
| EXP-141 | R2 + Redis credentials committed in plaintext to git history | **Critical** | <1d | open (new today) — immediate rotation required |
| EXP-142 | ZATCA_FORCE_REPORT_FAIL/SIGN_FAIL lack APP_ENV!=production guard | Medium | <1d | open (new today) |
| EXP-143 | .claude/agents Bash grant — indirect prompt injection path | Medium | <1d | open (new today) |

---

## Needs human attention

Items appearing in 3+ consecutive digests still open/in-review, plus critical/blocked escalations:

1. **Traefik CSP removal — 7th consecutive digest.** `proxy.ts` is the sole authoritative CSP source since 2026-05-22 (Decision-Log 2026-05-22). Traefik `headers.contentSecurityPolicy` must be removed as the capstone step. No PR open. Due 2026-06-01. Action-Tracker row from 2026-05-22 remains Open.

2. **EXP-141 — CRITICAL: credentials in git history (new today).** `docker/workers/docker-compose.yml` was deleted in PR #503 but the R2 API token, R2 secret access key, and Redis password remain in the git object store at commit `a422e0c`'s parent SHA. Running `git show <parent-sha> -- docker/workers/docker-compose.yml` exposes them to anyone with repo access. All three credentials must be **rotated immediately** regardless of EXP-141 fix status.

3. **EXP-103 — 3rd consecutive digest** (2026-05-24, 2026-05-25, 2026-05-26). 5 upload routes still bypass `enforceStorageQuota`. End-to-end quota enforcement is incomplete until all upload surfaces are gated.

4. **EXP-83 — 4th consecutive digest.** `course_assets` table VALIDATE constraint (NULL `attachment_id` + NULL `url` rows allowed). No PR open. Appeared in 2026-05-23, 2026-05-24, 2026-05-25, 2026-05-26 digests.

5. **EXP-112 — review-blocked (2nd digest).** PR #482 received a gatekeeper BLOCK on attempt 1 for missing tests on dual-mode routes (approve-pending, refunds/cleanup). R3 cannot proceed without a human resolving the test coverage question or providing a targeted override.

6. **EXP-129 — 2nd digest.** Tabby `verify` and `webhook` paths bypass KSA geo-restriction. Forged payment completion events from non-KSA IPs can mutate payment state. No PR open.

7. **EXP-127 — 2nd digest.** `hashtext()` advisory lock birthday collision probability reaches ~1% at ~55k users and ~50% at ~77k users. The EXP-80 reservation ledger is built on a concurrency primitive that degrades silently at production scale.

---

## Subagent outputs

### release-manager

**Semver recommendation: PATCH.** 7 merged PRs — all security hardening, bug fixes, and cron wiring. No new user-facing API surface, no feature flags added, no breaking schema changes. Migration notes: (1) PR #493 (EXP-121) adds `releaseStorageBytes()` call in the DELETE video route and orphan-sweep — no schema change, but operators on stale deploys retain the quota-lockout regression; (2) PR #503 (ZATCA unification) deletes `docker/workers/docker-compose.yml` — any compose override referencing that file will fail at container start. Branch hygiene: R2 refactor commit `a56de86` was landed and immediately reverted (`f46a100`) in the same window; main is clean. Next semver candidates: EXP-103 close (all upload routes quota-gated) → MINOR; EXP-134 close (bucket/URL mismatch resolved) → PATCH; advisory lock hash fix (EXP-127) → PATCH.

### architecture-reviewer

Two items deserve Decision-Log rows this window:

1. **`.claude/agents` Bash access constraint** — Agent definitions in `.claude/agents/` must not grant Bash (or any write/execute tool) to agents whose input corpus includes adversary-controlled content. EXP-143 is the direct signal. Mirrors the 2026-05-13 principle that no component may rely on upstream trust for security-critical actions. **Decision-Log row added.**

2. **Atomic update requirement for origin-split PRs** — EXP-134 demonstrates that an origin-split PR (EXP-77 / PR #454) updated the URL helper but not the upload-command bucket selection, creating a write/read mismatch that survived 2+ days in production. Recommendation: any PR that changes CDN origin for a bucket must update both the write-path bucket selector and the read-path URL builder atomically, and include an integration test asserting the bucket written to equals the bucket implied by the public URL returned.

---

## Statistics

| Metric | Count |
|--------|-------|
| New agent-fp issues | 14 |
| Resolved same-day (new) | 2 (EXP-136, EXP-137) |
| Carry-forward resolved today | 4 (EXP-111, EXP-113, EXP-121, EXP-123) |
| **Total resolved this window** | **6** |
| In-flight (In Progress) | 3 (EXP-134, EXP-135, EXP-138) |
| Review-blocked | 1 (EXP-112) |
| **Merged PRs** | **7** (#465, #470, #478, #481, #493, #498, #503) |
| New Decision-Log rows | 1 |
| **Needs human attention** | **7** (Traefik CSP, EXP-141, EXP-103, EXP-83, EXP-112, EXP-129, EXP-127) |

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
