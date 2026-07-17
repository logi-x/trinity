---
title: "2026-05-24 Experts Agent Digest"
date: "2026-05-24"
tags: [agent, digest, project/experts]
category: "daily"
source: "automation"
source_id: "Raw/sources/2026-05-24-experts-agent-digest.md"
---

# 2026-05-24 Experts Agent Digest

Window: 2026-05-23T00:00:00Z → 2026-05-24T23:59:59Z.

---

## New today

Issues created with agent fingerprints (`<!-- agent-fp:`) in the last 24h:

| ID | FP | Title | Priority | Status |
|---|---|---|---|---|
| EXP-97 | `7287d3880d98` | [bug] completed embed job silently dropped when BullMQ removeOnComplete evicts job record before async callback | No priority | Todo |
| EXP-98 | `9d983ab4e6fb` | [bug] failed embed BullMQ job leaves EmbeddingSync stuck in "pending" with no error recorded | No priority | Todo |
| EXP-99 | `984201e58b86` | [bug] subscription checkout route missing Tabby KSA eligibility check — non-SA users get 502 instead of 400 | No priority | Todo |
| EXP-100 | `302812779a63` | [bug] cf-ipcountry header spoof bypasses Tabby KSA restriction when origin is reachable directly | No priority | Todo |
| EXP-101 | `a37207aca1c4` | [security] Production PostgreSQL (5432) and Redis (6379) bound to 0.0.0.0 — database ports publicly reachable, bypassing any OS firewall | High | Backlog |
| EXP-102 | `4e6bbe0deae2` | [security] redis:latest unversioned image tag in production — unpinned image allows silent version drift and supply-chain risk | High | Backlog |

---

## Repeated pattern

**BullMQ embed pipeline — 2× today (EXP-97, EXP-98), same handler file:** Both issues target `ai-result.handler.ts/setupAiResultHandler`. EXP-97 exposes a fragile reliance on `getJob()` after removeOnComplete eviction; EXP-98 exposes missing error column writes on the `failed` path. Not yet at the 3× threshold for a named pattern, but the concentration in a single file is a strong early signal. The Decision-Log note from 2026-05-10 ("batch reconciliation cron is safety net until worker is confirmed stable") remains the current mitigation — but the cron cycle time is unknown.

**Tabby KSA eligibility — 2× open today (EXP-99, EXP-100) + EXP-96 resolved:** PR #439/#440 closed the course/event checkout surface (EXP-96). Today's findings reveal the subscription checkout route (EXP-99) and the upstream eligibility resolver (EXP-100) were not updated. This mirrors the JWT-staleness wave: a surface-level fix did not propagate to sibling routes. A systematic sweep of all Tabby-touching routes is needed.

**docker/production/docker-compose.yml — 2× today (EXP-101, EXP-102), both triggered by a single PR merge (#436):** Infrastructure security hotspot. Zero findings → two high-severity findings in a single PR. Database/cache ports defaulting to `0.0.0.0` and unversioned image tags are repeatable mistakes. A new infra hygiene rule in the Decision-Log is warranted.

**JWT role-staleness — pattern closed:** All 7 instances (EXP-69, EXP-78, EXP-84, EXP-85, EXP-88, EXP-89, EXP-90) are now resolved as of today. The pattern that dominated the past week is fully closed.

---

## Resolved since yesterday

Three issues transitioned to Done during this window:

| ID | Title | Completed at | PR |
|---|---|---|---|
| EXP-94 | [bug] Noon Order.name rejects special characters — checkout 403 on titles with brackets/punctuation | 2026-05-24T00:00:18Z | #434 |
| EXP-95 | [bug] Course/event title must start with a letter — block invalid titles at form + API validation | 2026-05-24T00:00:26Z | #435 |
| EXP-96 | [bug] Restrict Tabby checkout to KSA traffic only (human-filed, no agent-fp) | 2026-05-24T04:22:03Z | #439, #440 |

---

## In-flight fixes

No open Routine 3 PRs at end of window. EXP-97 through EXP-100 are in `Todo`. EXP-101 and EXP-102 are in `Backlog`. The new Todo items are expected to be picked up by R3 in the next cycle.

---

## Merged PRs

Six PRs merged today.

**Payment / checkout**

| PR | Title | Linear |
|---|---|---|
| #440 | Show disabled Tabby option with billing address link (EXP-96) | EXP-96 |
| #439 | Restrict Tabby checkout to KSA (EXP-96) | EXP-96 |
| #435 | fix(schemas): require course/event titles start with a letter (EXP-95) [attempt 3] | EXP-95 |
| #434 | fix(payments/noon): add gateway-level wiring tests for sanitizeNoonName (EXP-94) [attempt 3] | EXP-94 |

**CSP**

| PR | Title | Linear |
|---|---|---|
| #437 | feat(csp): add Iconify API CDNs to connect-src and update background image references | — |

**Infrastructure**

| PR | Title | Linear |
|---|---|---|
| #436 | Cleanup/docker remote branch | — |

Note: PR #436 (docker cleanup) introduced EXP-101 and EXP-102 within hours of merging — `ports: 5432:5432` and `ports: 6379:6379` bound to `0.0.0.0`, and `image: redis:latest` unpinned. This is the first instance of a docker-compose cleanup PR immediately generating high-severity security findings.

**Semver signal:** PATCH. Security fixes and hardening. PR #436 is a net-negative until EXP-101 and EXP-102 are resolved.

---

## Migrations / env / infra changes

**No Prisma schema migrations today.**

**Infrastructure (PR #436 — Cleanup/docker remote branch):**
- `docker/production/docker-compose.yml` — added `experts-prd-postgres` with `ports: 5432:5432` (binds to `0.0.0.0:5432`, bypasses UFW/OS firewall via Docker iptables injection) and `experts-prd-redis` with `ports: 6379:6379` (same exposure) and `image: redis:latest` (unpinned). Directly triggered EXP-101 and EXP-102.
- `docker/staging/docker-compose.yml` — same `redis:latest` pattern present (EXP-102 applies to staging as well).
- Fix required: restrict port bindings to `127.0.0.1:PORT:PORT`; pin Redis to a specific versioned image (e.g. `redis:7.2-alpine`).

**CSP (PR #437):** Iconify API CDNs (`api.iconify.design` and related domains) added to CSP `connect-src`. Background image references updated.

**CI (direct commits to main):**
- `621d0bb2` — deploy workflow now posts result to Slack `#experts-deployments`.
- `d31e053a` — Claude/bot-authored PR comments skip CI workflow, preventing infinite feedback loops.
- `69eebe97` — jq syntax fix: parenthesize block concat so `+if/end` parses correctly.

**Routines (direct commits to main):**
- `98dd8a38` — 7 new specialist agent types added to the routines pool: accessibility-auditor, AI-engineer, analytics-architect, architecture-reviewer, code-reviewer, concept-architect, database-engineer.
- `aafeac1d` — "out of scope" follow-ups now filed as Backlog Linear issues instead of footer notes in digest.

---

## Architectural notes

**PR #436 immediately produced 2 high-severity infra security findings:** Infrastructure docker-compose changes merged without a security checklist. Database and cache ports should default to loopback-only (`127.0.0.1:PORT:PORT`). Image tags must always be pinned (e.g. `redis:7.2-alpine`, not `redis:latest`). This warrants a new infra hygiene rule in the Decision-Log: "Any docker-compose port binding that exposes a database or cache service must use `127.0.0.1:PORT:PORT` unless the port is intentionally public. Image tags must be pinned to a specific version."

**Tabby KSA surface expansion not fully closed:** PR #439/#440 (EXP-96) addressed course/event checkout. Subscription checkout (EXP-99) and the eligibility resolver itself (EXP-100) remain open. Pattern mirrors the JWT-staleness wave: a single-surface fix does not propagate to sibling surfaces automatically. A systematic Tabby surface audit is recommended before closing this cluster.

**AI embedding pipeline reliability gap:** EXP-97 and EXP-98 both land in `ai-result.handler.ts`. The handler's fragility stems from two independent design choices: (1) using `getJob()` post-removeOnComplete instead of capturing job data at event time, and (2) no error column write on `failed` event. The batch reconciliation cron is the current safety net (per 2026-05-10 Decision-Log note), but its cycle time is undocumented. Until both EXP-97 and EXP-98 are resolved, silently lost embeddings remain a real failure mode in production.

**7 new specialist agent types added:** Commit `98dd8a38` adds accessibility-auditor, AI-engineer, analytics-architect, architecture-reviewer, code-reviewer, concept-architect, and database-engineer to the routines pool. This significantly expands R3's capability for non-standard bug classes (accessibility, analytics, architecture, database) that the prior pool could not handle.

---

## Docs that need updating

- `docker/production/docker-compose.yml` + `docker/staging/docker-compose.yml` — EXP-101: restrict `ports` bindings to `127.0.0.1:PORT:PORT` for PostgreSQL (5432) and Redis (6379). EXP-102: pin Redis image to a specific version (e.g. `redis:7.2-alpine`).
- `apps/experts-app/src/lib/payments/eligibility/payment-eligibility.ts` — EXP-100: `resolveTabbyEligibility` must validate origin IP (e.g. via a shared secret or Cloudflare IP range check), not only the `CF-IPCountry` header, which can be forged when the origin is reachable directly.
- `apps/experts-app/app/api/v1/commerce/subscriptions/checkout/route.ts` — EXP-99: add Tabby KSA eligibility gate consistent with course/event checkout (EXP-96 pattern).
- `apps/experts-app/src/lib/ai/embeddings/ai-result.handler.ts` — EXP-97: replace `getJob()` call with job-ID cache or use `QueueEvents` listener data directly (job data is available in the event payload). EXP-98: add error column write to `EmbeddingSync` on the `failed` event path.
- `_routines/README.md` — document: 7 new agent types added (`98dd8a38`), "out of scope" Backlog filing convention (`aafeac1d`), CI deploy Slack notification (`621d0bb2`), bot-comment CI guard (`d31e053a`).

---

## Still open

| ID | Status | Severity | Area | Summary |
|---|---|---|---|---|
| EXP-97 | Todo | High | ai/embeddings | BullMQ removeOnComplete eviction drops completed embed job silently |
| EXP-98 | Todo | High | ai/embeddings | Failed embed job leaves EmbeddingSync stuck in "pending" |
| EXP-99 | Todo | High | payments/subscriptions | Subscription checkout missing Tabby KSA eligibility check |
| EXP-100 | Todo | High | payments/eligibility | cf-ipcountry header spoof bypasses Tabby KSA restriction |
| EXP-101 | Backlog | High | docker/platform | Production PostgreSQL (5432) + Redis (6379) bound to 0.0.0.0 |
| EXP-102 | Backlog | High | docker/platform | redis:latest unpinned image tag in production and staging |
| EXP-83 | Backlog | Low | courses/schema | VALIDATE course_isfree_price_consistency after prod data sweep |
| EXP-82 | Backlog | Low | storage | Admin storage dashboard + over-quota alerts |
| EXP-81 | Backlog | Low | storage | Stale pending file cleanup + R2 orphan reaper |
| EXP-80 | Backlog | Medium | storage | Race-safe UserStorageUsage ledger + reservation flow |
| EXP-77 | Backlog | Medium | infra | Split user uploads to files.experts.com.sa (human-only, no agent-fp) |

---

## Needs human attention

1. **EXP-101 (High) — PostgreSQL + Redis ports bound to 0.0.0.0 on production VPS:** Docker's iptables injection bypasses UFW/OS firewall rules. Both `5432` and `6379` are publicly reachable. Requires editing `docker/production/docker-compose.yml` and restarting services. Deadline: immediate. Introduced by PR #436, merged today.

2. **EXP-102 (High) — redis:latest unpinned in production and staging:** `docker-compose pull` on next deploy may silently upgrade to a breaking or compromised Redis version. Requires pinning to `redis:7.2-alpine` (or equivalent stable tag) in both `docker/production/docker-compose.yml` and `docker/staging/docker-compose.yml`. Introduced by PR #436.

3. **Traefik CSP header removal (4th consecutive digest — 2026-05-21, 2026-05-22, 2026-05-23, 2026-05-24):** EXP-71 is Done. The Traefik `headers.contentSecurityPolicy` static directive has NOT been confirmed removed from production. Requires human with VPS access to edit the Traefik config and restart.

4. **EXP-77 — Split user uploads to files.experts.com.sa:** No agent-fp; human-only infrastructure change (DNS + bucket + URL-mapper). Appeared in 2026-05-22 and 2026-05-23 digests. Still unassigned. Needs triage.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
