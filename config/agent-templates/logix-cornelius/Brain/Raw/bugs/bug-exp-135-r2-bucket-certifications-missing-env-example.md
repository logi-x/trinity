---
title: "EXP-135: R2_BUCKET_CERTIFICATIONS consumed in upload route but absent from .env.example"
linear_id: "EXP-135"
agent_fp: "8805a6e85dd0"
date: "2026-05-26"
severity: "High"
status: "in-progress"
resolution: "unknown"
tags: [bug, completeness, storage, r2, certifications, project/experts]
category: "bug"
source: "automation"
---

# EXP-135: R2_BUCKET_CERTIFICATIONS consumed in upload route but absent from .env.example

**Linear:** [EXP-135](https://linear.app/experts/issue/EXP-135) | **Fingerprint:** `<!-- agent-fp: 8805a6e85dd0 -->` | **Severity: High**

## Summary

The certifications document upload route reads `process.env.R2_BUCKET_CERTIFICATIONS ?? process.env.R2_BUCKET_STATIC ?? "static"` to determine the target R2 bucket. `R2_BUCKET_CERTIFICATIONS` is absent from `.env.example`, meaning any new deployment that follows `.env.example` as an onboarding guide will silently fall back to `R2_BUCKET_STATIC` for certification document uploads — a storage-isolation failure.

## Impact

- **Storage isolation failure**: Instructor certification documents (legal documents) uploaded to production may land in the general-purpose static bucket instead of the dedicated certifications bucket, depending on whether `R2_BUCKET_CERTIFICATIONS` was set out-of-band.
- **Onboarding gap**: A developer setting up a new environment from `.env.example` will not know to set `R2_BUCKET_CERTIFICATIONS`. The silent fallback makes this invisible until a certification upload is audited.
- **High severity**: Bucket-class env variable — silent fallback to wrong bucket is a storage-isolation failure for legal documents.

## Root Cause

`R2_BUCKET_CERTIFICATIONS` was introduced when the certifications upload route was written but was not added to `.env.example`. It is not documented anywhere in the tracked env file.

## Fix

Add `R2_BUCKET_CERTIFICATIONS=<certifications-bucket-name>` to `.env.example` with a descriptive comment. Confirm the bucket is created and the env var is set in both production and staging deployment configs.

## Related

- EXP-134 (R2_BUCKET_STATIC write target misaligned — sibling completeness gap)
- EXP-138 (umbrella tracker for post-EXP-77 follow-ups)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
