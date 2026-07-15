---
title: Experts — Security Incident Sweep #2–#11 (13–15 May 2026)
date: 2026-05-15
tags: [security, session, project/experts-app, incident, csp, uploads, realtime, project/experts]
related:
  - "[[Raw/reviews/incident#2/security-13052026]]"
  - "[[Raw/reviews/incident#3/security-13052026]]"
  - "[[Raw/reviews/incident#4/security-13052026]]"
  - "[[Raw/reviews/incident#5/security-13052026]]"
  - "[[Raw/reviews/incident#6/security-13052026]]"
  - "[[Raw/reviews/incident#7/security-13052026]]"
  - "[[Raw/reviews/incident#9/security-14052026]]"
  - "[[Raw/reviews/incident#10/security-14052026]]"
  - "[[Raw/reviews/incident#11/security-14052026]]"
  - "[[Projects/Experts/Experts App/docs/reference/cdn-hardening]]"
---

# Experts Security Incident Sweep — 13 to 15 May 2026

Three-day rolling security workflow run via the standard incident orchestration playbook (investigate → triage → plan → implement → review → fix → validate → commit/push, with main session gating commit/push behind explicit phrases).

## Shipped to main / PR open

| PR   | Incident | Title                                                                              | Status            |
| ---- | -------- | ---------------------------------------------------------------------------------- | ----------------- |
| #308 | #2       | security: authorization on `/api/v1/internal/upload` (per-domain ownership + MIME) | Merged 2026-05-13 |
| #309 | #3       | security: thumbnail route IDOR — object-level authorization                        | Merged 2026-05-13 |
| #310 | #4       | security: atomic Lua sliding-window rate limit on uploads (30/5m + 200/24h)        | Merged 2026-05-13 |
| #311 | #5       | security: pending→ready upload flow + storage janitor (R2 orphan cleanup)          | Merged 2026-05-13 |
| #312 | #6       | security: recheck materialized buffer size against MAX_FILE_SIZE                   | Merged 2026-05-14 |
| #313 | #7       | security: defense-in-depth response headers + WS lifecycle fix                     | Open 2026-05-15   |

## Filed in vault, not yet implemented

| Incident | Class                                                                                                     | Severity                 | Notes                                                                           |
| -------- | --------------------------------------------------------------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------- |
| #8       | scheduled application-security review (3 findings: course detail leak, presence lookup, viewer snapshots) | Mixed (1 High, 2 Medium) | Pre-existing in vault, investigation phase begins 2026-05-15                    |
| #9       | thumbnail extension MIME/filename mismatch                                                                | Medium                   | Two-route surgical fix; mirrors `internal/upload` `MIME_TO_EXT` pattern         |
| #10      | CSP `script-src 'unsafe-inline'` removal                                                                  | Medium                   | Phased migration: depends on #11A landing first; nonce-based middleware         |
| #11      | CSP hardening bundle (5 sub-items)                                                                        | Low-Medium               | Reporting endpoint, font self-host, origin audit, HSTS/Permissions-Policy, etc. |

## Durable policies established this session

These now live in main-session memory (`/home/logix/.claude/projects/-home-logix-experts/memory/`):

1. **Commit flow:** always run `pnpm experts:check` before any commit or push; if FORMAT/LINT/TYPECHECK fails, run `pnpm experts:check:fix` then re-check. Note: the script's "TYPECHECK" lane is misnamed — it runs `eslint .`, not `tsc`. Real `tsc --noEmit` only runs at push time via the husky pre-push hook (and via `pnpm typecheck:tsc` explicitly).
2. **Security-incident commit policy:** in security remediation workflows, no agent commits autonomously. Main session waits for explicit "commit now" / "push now" phrases. Sub-agents must be briefed defensively against self-committing.
3. **`frontend-developer` agent self-commits:** observed pattern across incidents #3 and #4. After every spawn, run `git log --oneline -3` + `git status -sb` to detect rogue commits; never silently amend — surface to user.

## Architectural patterns landed this session

(See linked incident files for full rationale.)

1. **Pending→ready upload state machine** (`File.status` enum) — atomic DB write before R2 PUT, status flip on success, BullMQ janitor sweep for orphans. Schema in `prisma/schema.prisma`, janitor in `src/workers/storage-janitor/`. Used by all three upload routes.
2. **Atomic compare-and-delete in janitor** — `deleteMany({where: {id, status: "pending"}})` is the race-safe pattern for the TOCTOU between janitor and route status flip. Returning `count: 0` means the route won the race; observe `storage-janitor.sweep.skip-raced` and continue.
3. **BullMQ v5 idempotent recurring jobs** — `queue.upsertJobScheduler(schedulerId, {every: ms}, jobShape)`. Replaces the older `queue.add(name, data, {repeat, jobId})` form which is NOT idempotent across worker restarts.
4. **Atomic Lua sliding-window rate limiting** — Redis sorted set + Lua EVAL for the 30/5m + 200/24h budget on `/api/v1/internal/upload`. NaN-safe env parsing (`Number.parseInt(env, 10) || default`). Fail-open on Redis errors so a Redis outage doesn't lock all uploads. Generic error message so the response doesn't leak which limit triggered.
5. **Defense-in-depth response headers at app layer + edge** — production CSP ships from Traefik `secure-headers@file`; `next.config.ts` now also ships `nosniff` + `Referrer-Policy` + `X-Frame-Options` as fallback. Cloudflare Transform Rule sets `nosniff` on `cdn.experts.com.sa/*` independently.
6. **WS connect deduplication** — `connectInFlight: Promise<void> | null` in `WebSocketTransport`. Single token-fetch + socket-open at a time. `kickConnect` and `reconnectAfterIdle` short-circuit when in flight or socket is `CONNECTING`. `GlobalRealtimeCoordinator` debounces leader kicks at 150ms.

## Things this session deliberately did NOT do

- Add a CSP in `next.config.ts`. Production already has one from Traefik; second-shipping risks confusion about authority and isn't a surgical security fix. Migration tracked as incident #10.
- Ship the `style-src 'unsafe-inline'` removal. Tracked as a follow-up after #10 succeeds.
- Touch the Statsig multi-CDN `connect-src` origins (`featureassets.org`, `assetsconfigcdn.org`, `prodregistryv2.org`, `beyondwickedmapping.org`). Confirmed legitimate; documented in the CDN hardening runbook.
- Bundle the thumbnail-extension fix into incident #6's PR. Surgical-scope discipline; filed as #9.

## What to do next on the security track

1. Investigate incident #8 (course detail leak + presence + viewer snapshots) — multi-finding incident, three routes.
2. Land incident #9 (thumbnail extension MIME→ext) — small surgical fix; mirrors `internal/upload` pattern.
3. Wait for #313 review before starting #10/#11 — those depend on the production CSP being the documented baseline.

## External references

- CDN hardening runbook: `~/brain/Projects/Experts/Experts App/docs/security/cdn-hardening.md`
- Action tracker (live): `~/brain/Action-Tracker.md`
- Memory (main session): `~/.claude/projects/-home-logix-experts/memory/`

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
