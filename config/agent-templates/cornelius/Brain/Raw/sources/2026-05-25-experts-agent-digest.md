---
title: "2026-05-25 Experts Agent Digest"
date: "2026-05-25"
tags: [agent, digest, project/experts]
category: "daily"
source: "automation"
source_id: "Raw/sources/2026-05-25-experts-agent-digest.md"
---

# 2026-05-25 Experts Agent Digest

Window: 2026-05-24T00:00:00Z → 2026-05-25T23:59:59Z.

---

## New today

Issues created with agent fingerprints (`<!-- agent-fp:`) in the last 24h:

| # | Title | Status | Severity | Created |
|---|-------|--------|----------|---------|
| EXP-97 | BullMQ removeOnComplete evicts embedding jobs before results are processed | Resolved | Medium | 2026-05-24 |
| EXP-98 | Failed embed BullMQ jobs leave stale pending EmbeddingSync rows | Resolved | Low | 2026-05-24 |
| EXP-99 | Subscription checkout missing Tabby eligibility pre-check | Resolved | Medium | 2026-05-24 |
| EXP-100 | CF-IPCountry header spoofable by authenticated user → locale bypass | Resolved | Medium | 2026-05-24 |
| EXP-101 | Production PostgreSQL (5432) + Redis (6379) listening on 0.0.0.0 | Resolved | High | 2026-05-24 |
| EXP-102 | redis:latest unversioned image in Docker Compose | Resolved | Low | 2026-05-24 |
| EXP-103 | [spinoff: EXP-80] Migrate 5 remaining upload routes to enforceStorageQuota | Open | High | 2026-05-24 |
| EXP-104 | [spinoff: EXP-77] Delete dead R2 exports (createPresignedGetUrl, getFileStream) | Resolved | Low | 2026-05-24 |
| EXP-105 | [spinoff: EXP-77] Seed legacy CDN migration list from existing R2 keys | Resolved | Low | 2026-05-24 |
| EXP-106 | [spinoff: EXP-82] Wire storage warning/limit notification emails | Resolved | Medium | 2026-05-24 |
| EXP-107 | [spinoff: EXP-100] Route-level CF-IPCountry DB-write skip | Resolved | Low | 2026-05-24 |
| EXP-108 | [spinoff: EXP-100] Subscription locale fallback when CF header absent | Resolved | Low | 2026-05-24 |
| EXP-109 | [spinoff: EXP-80] Schema-qualified Prisma model refs in reservation flow | Resolved | Low | 2026-05-24 |
| EXP-110 | [spinoff: EXP-80] Error handling + structured logging in reservation-cleanup cron | Resolved | Medium | 2026-05-24 |
| EXP-111 | storage-pending-reaper and storage-orphan-reaper CRON_SECRET timing-unsafe | In Review | High | 2026-05-25 |
| EXP-112 | CRON_SECRET timing-unsafe comparison in embedding-sync janitor | In Review | High | 2026-05-25 |
| EXP-113 | checkAndSendStorageAlerts has no cron route — dead unreachable function | In Review | Medium | 2026-05-25 |
| EXP-114 | [spinoff: EXP-111] storage-janitor CRON_SECRET fail-open (plain !== check) | Backlog | High | 2026-05-25 |
| EXP-115 | [spinoff: EXP-111] ai/embeddings/sync route CRON_SECRET timing-unsafe | Backlog | High | 2026-05-25 |
| EXP-116 | [spinoff: EXP-111] admin cron routes CRON_SECRET timing-unsafe | Backlog | High | 2026-05-25 |
| EXP-117 | [spinoff: EXP-113] checkAndSendStorageAlerts hardcodes free-tier quota threshold | Backlog | Low | 2026-05-25 |
| EXP-118 | [spinoff: EXP-113] StorageAlert createMany dedup race condition | Todo | Medium | 2026-05-25 |
| EXP-119 | [spinoff: EXP-113] CRON_SECRET comparison length leak via timing side-channel | Todo | Medium | 2026-05-25 |
| EXP-120 | [spinoff: EXP-112] Missing auth unit tests for cron routes | Todo | Low | 2026-05-25 |
| EXP-121 | used_bytes never decremented on file deletion — storage ledger silent corruption | Todo | High | 2026-05-25 |
| EXP-122 | Stale reservation opens quota-bypass window between reserve and finalize | Todo | Medium | 2026-05-25 |
| EXP-123 | CF_ORIGIN_SECRET absent on non-prod — trusts all cf-ipcountry headers | Todo | Medium | 2026-05-25 |
| EXP-124 | Storage reservation DELETE endpoint lacks user_id ownership check | Backlog | High | 2026-05-25 |
| EXP-125 | reapR2Orphans unbounded memory scan — OOM DoS vector | Backlog | Medium | 2026-05-25 |
| EXP-126 | Admin storage metrics overThreshold query missing LIMIT clause | Backlog | Low | 2026-05-25 |
| EXP-127 | Advisory lock hashtext() int32 birthday collision at ~55k users | Backlog | Medium | 2026-05-25 |
| EXP-128 | user_storage_usage.used_bytes column has no non-negative CHECK constraint | Backlog | Low | 2026-05-25 |
| EXP-129 | Tabby verify/webhook paths bypass KSA geo-restriction entirely | Backlog | High | 2026-05-25 |

**33 new** agent-fp issues this window (17 first wave + 16 second wave). 13 resolved same-day. 3 in review (EXP-111 PR #478, EXP-112 PR #482, EXP-113 PR #481). 17 open in backlog/todo (EXP-103, EXP-114–EXP-129).

---

## Merged PRs (logi-x/experts)

16 PRs merged in window 2026-05-24T00:00:00Z → 2026-05-25T23:59:59Z:

| PR | Title | Merged |
|----|-------|--------|
| #453 | feat: ai embeddings BullMQ worker — removeOnComplete/removeOnFail TTLs (EXP-97) | 2026-05-24 |
| #454 | fix: clear stale EmbeddingSync rows on BullMQ job failure (EXP-98) | 2026-05-24 |
| #455 | feat: Tabby eligibility pre-check before subscription checkout (EXP-99) | 2026-05-24 |
| #456 | fix: treat CF-IPCountry as display-only hint; never write to DB from header (EXP-100) | 2026-05-24 |
| #457 | fix: bind PostgreSQL and Redis to 127.0.0.1 loopback only (EXP-101) | 2026-05-24 |
| #458 | fix: pin redis image to redis:7.2-alpine in all Compose files (EXP-102) | 2026-05-24 |
| #459 | fix: remove dead R2 presign/stream exports from r2.service.ts (EXP-104) | 2026-05-24 |
| #460 | chore: seed legacy-cdn migration list from existing R2 key scan (EXP-105) | 2026-05-24 |
| #461 | feat: wire StorageWarning + StorageLimit notification emails (EXP-106) | 2026-05-24 |
| #462 | fix: skip CF-IPCountry DB write at route boundary; pass resolved locale downstream (EXP-107) | 2026-05-24 |
| #463 | fix: subscription locale fallback when CF-IPCountry header absent (EXP-108) | 2026-05-24 |
| #464 | fix: schema-qualify Prisma model refs in storage reservation flow (EXP-109) | 2026-05-24 |
| #465 | fix: add error handling + structured logging to reservation-cleanup cron (EXP-110) | 2026-05-24 |
| #466 | feat: Tabby checkout eligibility pre-check — locale detection hardening | 2026-05-24 |
| #467 | chore: Docker Compose network hardening — loopback bind + image pinning | 2026-05-24 |
| #470 | feat: storage reservation cleanup cron sidecar (EXP-80 Phase 3) | 2026-05-25 |

3 PRs opened (in review) at end of window: #478 (EXP-111), #482 (EXP-112), #481 (EXP-113).

---

## Resolved in window

20 Linear issues closed in this window:

**New issues resolved same-day (13):** EXP-97, EXP-98, EXP-99, EXP-100, EXP-101, EXP-102, EXP-104, EXP-105, EXP-106, EXP-107, EXP-108, EXP-109, EXP-110.

**Carry-forward closed this window (7):** EXP-77, EXP-80, EXP-81, EXP-82, EXP-94, EXP-95, EXP-96 — resolved from prior waves during this 24h window.

---

## In-flight (open agent issues)

| # | Title | Opened | PR | Age |
|---|-------|--------|----|-----|
| EXP-111 | CRON_SECRET timing-unsafe — reaper routes | 2026-05-25 | #478 | 0d |
| EXP-112 | CRON_SECRET timing-unsafe — embedding janitor | 2026-05-25 | #482 | 0d |
| EXP-113 | checkAndSendStorageAlerts dead/unwired | 2026-05-25 | #481 | 0d |
| EXP-103 | Upload routes quota gap (5 routes) | 2026-05-24 | — | 1d |

4 issues in active review/work. 16 additional issues in backlog/todo (EXP-114–EXP-129).

---

## Needs human attention

1. **Traefik CSP removal** — **6th consecutive digest** flagging this. `proxy.ts` is sole CSP authority since 2026-05-22; Traefik `headers.contentSecurityPolicy` removal is the capstone step. No PR merged yet. Due 2026-06-01.
2. **EXP-121** (High) — `used_bytes` is **never decremented** when a file is deleted. Every deletion silently under-reports available storage. Quota enforcement is meaningless until this is fixed; silent corruption compounds with every delete operation in production.
3. **EXP-129** (High) — `verify` and `webhook` Tabby routes bypass KSA geo-restriction entirely. Tabby is a KSA-only payment provider; forged completion events from non-KSA origins can mutate payment state without eligibility validation.
4. **EXP-127** — Advisory lock implementation (`pg_advisory_xact_lock`) uses `hashtext()` to map user IDs to int32 lock keys. Birthday collision probability reaches ~1% at ~55k users; at 100k users two users regularly share a lock, creating false mutual exclusion. Design flaw in the just-landed EXP-80 system.
5. **EXP-111** (High) — `storage-pending-reaper` and `storage-orphan-reaper` use plain `!==` for `CRON_SECRET`. Fail-open: anyone who can reach the internal cron route can trigger reaper execution. PR #478 in review.
6. **EXP-103** — 5 upload routes still bypass `enforceStorageQuota`. EXP-72 (quota gate) merged; EXP-80 (ledger) in-flight. All 5 routes must be patched before any storage quota can be enforced end-to-end.
7. **EXP-113** — `checkAndSendStorageAlerts` function implemented but no cron route exists to call it. PR #481 in review; wire into Docker cron sidecar or delete dead code.
8. **EXP-83** — VALIDATE constraint on `course_assets` (3rd digest). No PR open.

---

## Trend analysis

### JWT staleness wave — CLOSED

The JWT role staleness wave (EXP-69, EXP-78, EXP-88, EXP-89, EXP-90, EXP-91, EXP-93 — 7 issues) is fully resolved as of 2026-05-23. No new JWT staleness issues this window. Pattern recorded in Decision-Log 2026-05-22/23.

### CRON_SECRET timing-unsafe — WAVE-WIDE (7+ routes, pattern not contained)

First wave: EXP-111 (reaper routes), EXP-112 (embedding janitor) — both now in review (#478, #482). Second wave adds EXP-114 (storage-janitor), EXP-115 (ai/embeddings/sync), EXP-116 (admin cron routes), EXP-119 (length-leak variant). Pattern spans **4+ distinct route groups**. Point fixes are insufficient; a shared `verifyCronSecret(req)` helper with `timingSafeEqual` + fail-closed on missing secret should be extracted and enforced platform-wide. Architecture-reviewer has recorded the invariant in Decision-Log.

### Storage ledger correctness — DEEP (5 issues, dominant concern)

EXP-80 (advisory-lock reservation) landed with PR #470, but the second wave reveals the ledger is shallower than needed:
- **EXP-121** (High): deletion never decrements `used_bytes` — silent corruption on every file delete
- **EXP-122** (Medium): stale reservation creates a quota-bypass window between reserve and finalize
- **EXP-124** (High): reservation DELETE endpoint lacks `user_id` ownership check — IDOR vulnerability
- **EXP-127** (Medium): `hashtext()` advisory lock birthday collision at ~55k users — design flaw
- **EXP-128** (Low): no non-negative CHECK on `used_bytes` — allows negative values to persist

This cluster is now the dominant correctness concern for the sprint. All 5 issues affect quota enforcement integrity.

### Storage dependency chain — chain integrity at risk

Chain: quota gate (EXP-72) ✓ → race-safe ledger (EXP-80) 🔄 (EXP-121 critical gap) → orphan reaper (EXP-81) ✓ → quota guard on all routes (EXP-103) ⚠️ → admin dashboard (EXP-82) ✓.

EXP-121 means the ledger's `used_bytes` is not a reliable source of truth until deletions are wired. EXP-80 cannot be considered fully resolved until EXP-121 is closed.

### OOM pattern — re-emerging

EXP-125 (`reapR2Orphans` unbounded memory scan) echoes BullMQ concurrency concerns from two weeks ago. Without pagination, the reaper loads all R2 object metadata into memory at once. At production scale this is an OOM DoS vector for the background job. Pattern: unbounded iterator/scan in async job — same root cause as EXP-94/EXP-95.

### Tabby KSA geo-restriction gap — payment path

EXP-129: the `verify` and `webhook` Tabby paths skip the geo-restriction check enforced at checkout. KSA restriction is applied at eligibility but not at fulfillment, meaning a forged webhook POST from outside KSA can complete a payment flow. Architecturally equivalent to the EXP-100 CF-IPCountry bypass fixed this window, but in the payment path — higher severity.

### R5 spinoff depth — 3 levels

Second-wave spinoffs (EXP-114–EXP-119) are level-3 descendants: EXP-80 → EXP-111/112/113 → EXP-114–EXP-119. Each resolved issue surfaces subtler sub-issues in the same domain. The CRON_SECRET and storage-ledger clusters have both reached 3-level depth, indicating the underlying abstraction (ad-hoc auth helpers, manual ledger updates) needs to be systematized rather than patched issue-by-issue.

### BullMQ embedding queue hardening — RESOLVED

EXP-97 (removeOnComplete TTL), EXP-98 (stale sync rows on failure), EXP-94 (concurrency cap), EXP-95 (retry exhaustion) all closed. Embedding worker operational hygiene wave complete.

### Infrastructure security — RESOLVED

EXP-101 (0.0.0.0 bind → loopback), EXP-102 (redis:latest → pinned). Both resolved same-day. Architecture-reviewer recorded loopback binding as a new invariant.

---

## Semver signal

**PATCH** — all activity this window is security hardening, bug fixes, and operational tooling. No new public API surface, no breaking changes, no feature flags added.

Next semver bump candidates:
- When EXP-103 closes (quota enforced on all upload routes) → MINOR (storage quota fully enforced end-to-end)
- When EXP-111/EXP-112/EXP-114–EXP-116 close (cron auth hardened across all routes) → PATCH
- When EXP-121 closes (storage ledger deletion decrement) → PATCH (correctness fix, prerequisite of accurate quota enforcement)
- When EXP-127 is addressed (advisory lock hash collision) → PATCH (reliability at scale)

---

## Subagent outputs

### release-manager

Semver recommendation: **PATCH**. All 16 merged PRs are bug fixes, security hardening, or operational tooling. Second wave produces no merges (16 new Backlog/Todo issues, 3 in-review PRs). No new user-facing features, no API version bumps. Deploy note: `prisma migrate deploy` must precede `reservation-cleanup` container start (creates `user_storage_reservations` and `user_storage_usage` tables). Second-wave EXP-121/EXP-124/EXP-128 will require additional migrations when resolved — `used_bytes` decrement trigger or handler, ownership column index on reservations, and a CHECK constraint respectively.

### architecture-reviewer

Three new Decision-Log entries recorded from first wave. Fourth entry warranted from second wave (EXP-127):

1. **Advisory-lock reservation pattern** — `pg_advisory_xact_lock` per-user as sole concurrency primitive for storage reservations. Two-phase reserve→finalize/release ledger.
2. **timingSafeEqual cron auth invariant** — `CRON_SECRET` comparison must use `timingSafeEqual` on all cron routes; fail-closed on missing secret.
3. **PG/Redis loopback binding invariant** — 5432 and 6379 bound exclusively to `127.0.0.1`; no app-layer credential check substitutes for network boundary.
4. **hashtext() advisory lock birthday collision** (new, EXP-127) — `pg_advisory_xact_lock(hashtext(userId)::bigint)` produces int32-range keys; collision probability hits ~1% at ~55k distinct users. Fix: derive lock keys via `('x'||md5(userId))::bit(64)::bigint` for full 64-bit distribution, or use an integer surrogate key column on `users`.

Open design questions: EXP-121 — should deletion decrement `used_bytes` synchronously in the delete handler or via a DB trigger? Recommend synchronous decrement in the handler to keep the ledger consistent without an async gap. EXP-122 — reservation TTL should be enforced at the DB level (expiry column + scheduled cleanup) rather than relying solely on the cron reaper.

---

## Statistics

| Metric | Count |
|--------|-------|
| New agent-fp issues | 33 (17 first wave + 16 second wave) |
| Resolved same-day (new issues) | 13 |
| Carry-forward resolved this window | 7 (EXP-77, EXP-80, EXP-81, EXP-82, EXP-94, EXP-95, EXP-96) |
| In review at end of window | 3 (EXP-111 PR #478, EXP-112 PR #482, EXP-113 PR #481) |
| Backlog/Todo at end of window | 17 (EXP-103, EXP-114–EXP-129) |
| Merged PRs | 16 |
| In-flight PRs | 3 (#478, #481, #482) |
| New Decision-Log rows | 4 |
| Needs human attention | 8 |

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
