---
title: "EXP-191: No rate limiting on realtime sync polling endpoint (EXP-174 follow-up)"
linear_id: "EXP-191"
agent_fp: "manual-exp191"
date: "2026-05-29"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, realtime, project/experts]
category: "bug"
source: "automation"
---

# EXP-191: Realtime sync endpoint has no rate limiting

**Linear:** [EXP-191](https://linear.app/experts/issue/EXP-191) | **Fingerprint:** `manual-exp191`

## Summary
The IDOR fix in EXP-174 (PR #612) explicitly deferred rate limiting to avoid throttling normal sync polling. The `GET /api/v1/internal/realtime/sync` endpoint is polled every ~3 seconds by clients with no server-side rate cap. A dedicated caller can drive sustained DB load or enumerate channel data at maximum poll rate.

## Repro
1. Authenticate as any user.
2. Loop: `GET /api/v1/internal/realtime/sync?cursor=0&channels=post:<id>:events` at 3s intervals.
3. No rate limiting response observed.

## Related
EXP-174 (IDOR, parent — resolved PR #612), EXP-194 (Section 3 DoS amplifier), EXP-195 (liker userId exposure)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
