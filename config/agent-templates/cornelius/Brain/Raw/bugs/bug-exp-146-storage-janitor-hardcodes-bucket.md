---
title: "EXP-146: storage-janitor sweeps hardcode R2_BUCKET_USER_UPLOADS, ignore File.bucket"
linear_id: "EXP-146"
agent_fp: "4f5c6023b95a"
spinoff_of: "EXP-145"
date: "2026-05-27"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, storage, project/experts]
category: "bug"
source: "automation"
---

# EXP-146: storage-janitor sweeps hardcode R2_BUCKET_USER_UPLOADS

**Linear:** [EXP-146](https://linear.app/experts/issue/EXP-146) | **Fingerprint:** `4f5c6023b95a`

## Summary
`storage-janitor.sweeps.ts` lines 108 and 247 call `deletePublicAsset` with hardcoded `R2_BUCKET_USER_UPLOADS` instead of reading `File.bucket`. Objects in other buckets (media, certifications) are silently skipped on sweep.

## Location
`apps/experts-app/src/workers/storage-janitor/storage-janitor.sweeps.ts:108,247`

## Impact
Storage-janitor orphan sweeps silently fail to delete objects in non-user-uploads buckets. Accumulated storage leak.

## Fix
Read `File.bucket` from the DB record and pass it to `deletePublicAsset` at each call site.

## Related
EXP-145 (parent), EXP-147 (deleteFromR2 same class)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
