---
title: "EXP-178: Storage orphan-reaper can delete static CDN assets"
linear_id: "EXP-178"
agent_fp: "manual-exp178"
date: "2026-05-28"
severity: "Urgent"
status: "resolved"
resolution: "merged PR #582 — getProtectedBuckets guard + getCertificationsBucket fail-closed"
tags: [bug, storage, project/experts]
category: "bug"
source: "automation"
---

# EXP-178: Storage orphan-reaper can delete static CDN assets

**Linear:** [EXP-178](https://linear.app/experts/issue/EXP-178) | **Fingerprint:** `manual-exp178`

## Summary
The R2 orphan-reaper (`storage-orphan-reaper.ts`) could permanently delete manually-uploaded static assets in the `static` bucket (`cdn.experts.com.sa/assets/*`). These objects have no corresponding `File` DB rows by design and must never be deleted. The reaper would scan the `static` bucket and delete anything not in the DB.

## Fix
PR #582: `getProtectedBuckets()` guard added; orphan-reaper now skips buckets in the protected list. `getCertificationsBucket()` added as a fail-closed helper (no silent fallback to `static`). Operator: restore any deleted `cdn.experts.com.sa/assets/*` objects from backup; remediate `File` rows WHERE `bucket='static'`.

## Related
EXP-134 (upload-public-asset bucket mismatch), EXP-145 (4 routes wrong bucket), EXP-146 (janitor hardcoded bucket)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
