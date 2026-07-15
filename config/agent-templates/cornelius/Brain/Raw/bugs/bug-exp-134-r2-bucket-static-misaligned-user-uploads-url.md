---
title: "EXP-134: R2_BUCKET_STATIC write target misaligned with R2_USER_UPLOADS_PUBLIC_URL after EXP-77 origin split"
linear_id: "EXP-134"
agent_fp: "9b6c4687133d"
date: "2026-05-26"
severity: "High"
status: "in-progress"
resolution: "unknown"
tags: [bug, completeness, storage, r2, origin-split, project/experts]
category: "bug"
source: "automation"
---

# EXP-134: R2_BUCKET_STATIC write target misaligned with R2_USER_UPLOADS_PUBLIC_URL after EXP-77 origin split

**Linear:** [EXP-134](https://linear.app/experts/issue/EXP-134) | **Fingerprint:** `<!-- agent-fp: 9b6c4687133d -->` | **Severity: High**

## Summary

After the EXP-77 origin split (PR #454), `getR2UserUploadsPublicBaseUrl()` returns the `files.experts.com.sa` CDN origin for user upload URLs. However, `upload-public-asset.command.ts` still uses `R2_BUCKET_STATIC` as its bucket argument when uploading public assets. The write target (`R2_BUCKET_STATIC`) and the URL domain (`R2_USER_UPLOADS_PUBLIC_URL` → `files.experts.com.sa`) are misaligned: files are written to the static bucket but URLs point to the files-origin CDN, making uploaded objects unreachable.

## Impact

- **Production invariant failure**: Every user upload via `upload-public-asset.command.ts` is written to the wrong bucket. The CDN URL returned points to a bucket/origin where the object does not reside.
- **Silent failure**: The upload call succeeds (R2 write to static bucket completes); the object is just unreachable at the URL surfaced to the client. Instructors uploading avatars, cover photos, or course thumbnails since EXP-77 merged may have non-functioning image URLs.
- **Detected 2+ days post-merge**: An attempted fix (commit `a56de86`) was reverted (`f46a100`) in the same window, likely due to surfacing EXP-135 simultaneously.

## Root Cause

PR #454 (EXP-77) updated the URL helper (`getR2UserUploadsPublicBaseUrl`) to point at `files.experts.com.sa` but did not update the bucket argument in `upload-public-asset.command.ts`, which remained hardcoded to `R2_BUCKET_STATIC`.

## Fix

Change the bucket argument in `upload-public-asset.command.ts` to use `R2_BUCKET_USER_UPLOADS` (matching the files-origin CDN). This must be done atomically with confirming that `R2_BUCKET_USER_UPLOADS` is documented in `.env.example` (EXP-135 dependency).

Add an integration test asserting that the bucket written to equals the bucket implied by the public URL returned, to prevent future origin-split regressions.

## Related

- EXP-77 (origin split — source of this gap)
- EXP-135 (R2_BUCKET_CERTIFICATIONS missing from .env.example — sibling completeness gap)
- EXP-138 (umbrella tracker for post-EXP-77 follow-ups)
- Decision-Log 2026-05-23: runtime-signed CDN domain policy (explicit per-bucket origins in proxy.ts)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
