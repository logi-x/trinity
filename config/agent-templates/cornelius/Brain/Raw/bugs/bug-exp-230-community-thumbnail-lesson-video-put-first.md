---
title: "EXP-230: [bug] community-thumbnail & lesson-video uploads are PUT-first — no-row orphan on DB failure"
linear_id: "EXP-230"
agent_fp: "34d82d6b179c"
date: "2026-05-31"
severity: "Medium"
status: "resolved"
resolution: "PR #690 — converted both routes to pending-first: File row + Attachment created in $transaction before R2 PUT"
tags: [bug, storage, r2, upload, project/experts]
category: "bug"
source: "automation"
---

# EXP-230: Last two PUT-first upload routes converted to pending-first

**Linear:** [EXP-230](https://linear.app/experts/issue/EXP-230) | **Status:** Resolved (PR #690)

## Summary
The community-thumbnail and lesson-video upload routes wrote the R2 object **before** the `File` row. A post-PUT DB failure left an untracked R2 object (no-row orphan) — the only remaining leak not covered by the DB-driven pending reaper.

These two routes were missed by incident #5's pending→ready remediation (commit `ef77e544`, 2026-05-14), which fixed the other three upload routes.

## Files
- `apps/experts-app/app/api/v1/community/posts/[id]/thumbnail/route.ts`
- `apps/experts-app/app/api/v1/courses/[id]/modules/[moduleId]/lessons/[lessonId]/video/route.ts`

## Fix
PR #690 converts both routes to the established pending-first pattern:
1. Create `File` row (`status: "pending"`) + `Attachment` in one `$transaction` BEFORE the PUT.
2. PUT to R2; on failure the pending row remains for the DB-driven pending reaper — never an untracked object.
3. Flip status to `"ready"` after the PUT succeeds.

## Related
- Incident #5 remediation (2026-05-14, commit ef77e544)
- EXP-229 (orphan-reaper env isolation)
- EXP-231 (decommission orphan reaper — now unblocked by this fix)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
