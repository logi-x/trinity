---
title: "2026-05-21 — Triage of incident#1..18 into Linear (EXP-54..71)"
date: "2026-05-21"
tags: [security, incident, linear, triage, project/experts]
category: session
source: session
source_id: Raw/sources/2026-05-21-experts-incident-triage-to-linear.md
---

# Triage of 18 security-incident files into Linear

Filed every `~/brain-v2/Raw/reviews/incident#N/security-*.md` (N=1..18) as its own
Linear issue in team **Experts** (`c8da9c4c-75c0-4402-9283-9eabf2f8388e`).
R3-pickup contract honored: every body begins with `<!-- agent-fp: <12-hex> -->`.

## State mapping (as applied)

| Source frontmatter status            | Linear state |
| ------------------------------------ | ------------ |
| closed                               | Done         |
| in-review / phase-4b-staging-verified| In Review    |
| partial / step-3-implemented         | In Progress  |
| deferred-infra                       | Canceled     |
| open                                 | Todo         |

All issues labeled `bug,security`.

## Ledger

| Incident | Linear | State       | Priority | One-liner |
|----------|--------|-------------|----------|-----------|
| #1       | EXP-54 | Done        | Urgent   | /internal/debug/* credential leak + community-post IDOR + markdown XSS + Tabby fail-open + CRON_SECRET bypass |
| #2       | EXP-55 | Done        | High     | /internal/upload allows text/html, text/javascript under attacker-chosen domain/entityId |
| #3       | EXP-56 | Done        | High     | Course/event thumbnail IDOR (Prisma `where:` missing owner) — PR #309 |
| #4       | EXP-57 | In Progress | Medium   | Per-user storage quota still missing (rate-limit shipped #310) |
| #5       | EXP-58 | Done        | High     | Pending→ready File status + storage-janitor + orphan sweep (PR #311, #337) |
| #6       | EXP-59 | Done        | Medium   | buffer.byteLength re-check after arrayBuffer() (PR #312) |
| #7       | EXP-60 | Canceled    | Low      | CDN/Traefik/R2 hardening — infra-side, out-of-repo |
| #8       | EXP-61 | Done        | High     | Anonymous data exposure on course-detail / presence / viewers (PR #314) |
| #9       | EXP-62 | Done        | Medium   | Thumbnail extension derived from validated MIME, not client filename (PR #315) |
| #10      | EXP-71 | In Review   | High     | App takes full CSP ownership + nonce + JsonLd conversions Phase 4B (PR #324) |
| #11      | EXP-63 | In Progress | Medium   | Drop raw.githubusercontent.com from font-src; CSP report endpoint shipped (#316) |
| #12      | EXP-64 | In Progress | Medium   | Lesson-resource Content-Disposition + per-domain MIME allowlist + RFC 5987 |
| #13      | EXP-65 | Done        | High     | Host-header injection in getRequestBaseUrl on /share/* (PR #320) |
| #14      | EXP-66 | Done        | Low     | CSP dev-mode 'unsafe-eval' isolated + prod-locked regression test (PR #329) |
| #15      | EXP-67 | In Review   | Medium   | Creator curriculum upload UX & auth gaps (dropzones, quiz 403, lesson-resource position) |
| #16      | EXP-68 | Todo        | Urgent   | Paid-content bypass via progress/quiz + **Noon API credentials logged** |
| #17      | EXP-69 | Todo        | Urgent   | **Committed prod/staging secrets** + role revocation does not invalidate JWT |
| #18      | EXP-70 | Todo        | High     | Password-reset URL poisoning + forgot-password enumeration + /console/health disclosure |

## Cross-linking

- **EXP-58** (incident#5) → relatedTo `EXP-48`, `EXP-49`, `EXP-51` — three storage-janitor bugs introduced by the work shipped in #5.
- **EXP-71** (incident#10) → relatedTo `EXP-52` — JsonLd escape bug in the very component this CSP migration introduced.

## Skip detection vs prior EXP-48..53

None of incident#1..18 fingerprint-matched EXP-48..53. Those six are bug-finder-derived findings of issues introduced *by* the incident work (sweeps from #5; JsonLd component from #10; creator route guard regression). All linked rather than duplicated.

## Internal duplicates

None. CSP-themed incidents (#7, #10, #11, #14) all address distinct sub-scopes
(CDN/Traefik infra · nonce migration · report endpoint + font-src · dev-mode eval).
Linked in body text rather than `duplicateOf`.

## Operational follow-ups surfaced

- **Rotate Noon merchant credentials immediately** (EXP-68 finding 3). Logs may
  contain them; audit retained log/observability storage.
- **Rotate every secret in `apps/experts-app/.env.production`, `.env.staging`,
  `.env.e2e`, `apps/experts-app/slack.secret`** and remove from git history
  (EXP-69). Enforce secret scanning + pre-commit blocking.
- Deploy storage-janitor cron entries to staging (EXP-58 pending op task).

## Links

- [[Action-Tracker]]
- [[Decision-Log]]
- [[Wiki/Concepts/CSP|CSP]] — durable lessons captured in EXP-71 body match the topic note

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
