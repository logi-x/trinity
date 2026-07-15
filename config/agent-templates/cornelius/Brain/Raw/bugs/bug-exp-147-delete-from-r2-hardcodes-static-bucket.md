---
title: "EXP-147: deleteFromR2 hardcodes R2_BUCKET_STATIC — wrong bucket for user-upload cover cleanup"
linear_id: "EXP-147"
agent_fp: "33154b3f570e"
spinoff_of: "EXP-145"
date: "2026-05-27"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, storage, project/experts]
category: "bug"
source: "automation"
---

# EXP-147: deleteFromR2 hardcodes R2_BUCKET_STATIC

**Linear:** [EXP-147](https://linear.app/experts/issue/EXP-147) | **Fingerprint:** `33154b3f570e`

## Summary
`deleteFromR2` in `r2.ts:20` hardcodes `R2_BUCKET_STATIC`. After the EXP-77 origin split, user-upload covers land in `R2_BUCKET_USER_UPLOADS`, so every cover replacement leaks the old R2 object permanently.

## Location
`apps/experts-app/src/lib/r2.ts:20` + `src/lib/user/profile/handlers/cover-upload.handler.ts:62`

## Impact
Permanent storage leak on every cover photo replacement. Storage janitor cannot reclaim these objects either (EXP-146 same class).

## Fix
Pass bucket parameter to `deleteFromR2`; callers supply the correct bucket from `File.bucket`.

## Related
EXP-145 (parent), EXP-146 (janitor same class)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
