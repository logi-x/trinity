---
title: "EXP-229: [bug] Storage orphan-reaper has no environment isolation — shared R2 buckets cause cross-env file deletion"
linear_id: "EXP-229"
agent_fp: "b5515fe4d993"
date: "2026-05-31"
severity: "Urgent"
status: "resolved"
resolution: "PR #687 — added APP_ENV isolation gate; reaper refuses to run unless runtime env matches target env"
tags: [bug, security, storage, r2, infra, project/experts]
category: "bug"
source: "automation"
---

# EXP-229: R2 orphan reaper cross-environment data loss

**Linear:** [EXP-229](https://linear.app/experts/issue/EXP-229) | **Status:** Resolved (PR #687)

## Summary
`reapR2Orphans` scans R2 buckets and deletes objects with no corresponding `File` row in **this** environment's DB. If local/staging/production share any R2 bucket (same `R2_BUCKET_USER_UPLOADS` or `R2_BUCKET_MEDIA`), the reaper running in staging would delete production objects, and vice versa.

**Severity depends on bucket sharing:** if buckets are shared across environments, this is actively destroying data every 6h. If every env has its own bucket, this is latent.

## Repro
1. Configure local and staging to share the same `R2_BUCKET_USER_UPLOADS` value.
2. Trigger the orphan-reaper cron in local (no local `File` rows for staging-uploaded objects).
3. Staging R2 objects are deleted; staging `File` rows become orphaned.

## Fix
PR #687 adds an `APP_ENV` environment isolation check — the reaper reads `APP_ENV` at runtime and refuses to scan if it does not match the intended target environment.

## Related
- EXP-230 (community-thumbnail/lesson-video PUT-first, prerequisite for EXP-231)
- EXP-231 (decommission orphan reaper — now unblocked)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
