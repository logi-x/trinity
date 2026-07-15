---
title: "EXP-145: 4 routes recorded wrong bucket in File.bucket after EXP-77 origin split"
linear_id: "EXP-145"
agent_fp: "a833e0781ac8"
date: "2026-05-27"
severity: "High"
status: "resolved"
resolution: "merged PR #529"
tags: [bug, storage, project/experts]
category: "bug"
source: "automation"
---

# EXP-145: 4 routes recorded wrong bucket in File.bucket

**Linear:** [EXP-145](https://linear.app/experts/issue/EXP-145) | **Fingerprint:** `a833e0781ac8`

## Summary
4 routes called `prisma.file.create` with `bucket: R2_BUCKET_STATIC` while `uploadPublicAsset()` writes to `R2_BUCKET_USER_UPLOADS`. Storage janitor/sweeps would silently 404 on deletes.

## Affected routes
- `community/posts/[id]/thumbnail`
- `events/[id]/thumbnail`
- `courses/[id]/thumbnail`
- `internal/upload`

## Fix
PR #529 corrected all 4 routes to record `bucket: R2_BUCKET_USER_UPLOADS`.

## Related
EXP-77 (origin split), EXP-146 (janitor still hardcodes bucket), EXP-147 (deleteFromR2 hardcodes wrong bucket)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
