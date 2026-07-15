---
title: "EXP-115: ai/embeddings/sync route CRON_SECRET timing-unsafe"
linear_id: "EXP-115"
agent_fp: "c40c7c44a324"
spinoff_of: "EXP-111"
date: "2026-05-25"
severity: "High"
status: "Backlog"
tags: [bug, security, cron, project/experts]
category: "bug"
source: "automation"
---

# EXP-115: ai/embeddings/sync route CRON_SECRET timing-unsafe

**Linear:** EXP-115 | **Fingerprint:** `<!-- agent-fp: c40c7c44a324 -->` | **Spinoff of:** EXP-111

## Summary

The `/api/v1/internal/ai/embeddings/sync` cron route (renamed from `embeddings/sync` in the 2026-05-10 relocation) uses plain `!==` for `CRON_SECRET` comparison. This is a timing side-channel that allows an attacker to enumerate secret characters by measuring response latency.

## Impact

- Timing oracle on the `CRON_SECRET` value — attacker can recover the secret byte-by-byte.
- Once recovered, attacker can trigger arbitrary embedding sync batch runs, potentially overloading the DB or causing quota accounting skew.
- Fail-open if `CRON_SECRET` is absent from environment.

## Root Cause

The route was created before PR #470 introduced the `timingSafeEqual` pattern. The file was relocated (`lib/recommendations/sync/` → `lib/ai/embeddings/`) but the auth check was not upgraded.

## Fix

Apply the same `timingSafeEqual` + fail-closed pattern as PR #470. Extract a shared `verifyCronSecret(req: Request): Response | null` helper that all cron routes call, to prevent future regressions.

## Related

- EXP-111 (parent), EXP-114 (storage-janitor), EXP-116 (admin cron routes), EXP-120 (missing tests)
- Decision-Log: `timingSafeEqual` cron auth invariant (2026-05-25)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
