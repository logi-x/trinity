---
title: "EXP-231: [chore] Decommission the R2 orphan reaper — remove reapR2Orphans + flag + route + schedule"
linear_id: "EXP-231"
agent_fp: "010c9bb2c1f6"
date: "2026-05-31"
severity: "Low"
status: "open"
resolution: "unknown"
tags: [bug, storage, r2, chore, project/experts]
category: "bug"
source: "automation"
---

# EXP-231: Decommission R2 orphan reaper

**Linear:** [EXP-231](https://linear.app/experts/issue/EXP-231) | **Status:** In Progress (blocked)

## Summary
With EXP-229 (env isolation) and EXP-230 (last PUT-first route) both resolved, the R2 orphan reaper (`reapR2Orphans`) no longer has a valid use case. All upload routes now create `File` rows before any R2 PUT. The reaper exists only to clean up a class of orphans that can no longer be created.

However, a one-time historical orphan cleanup run must occur before the reaper is removed, to drain any pre-fix orphans from R2.

## Hard prerequisites before this can be actioned
1. EXP-229 (env isolation) — resolved PR #687 ✓
2. EXP-230 (last PUT-first route) — resolved PR #690 ✓
3. One-time historical R2 orphan cleanup run (manual or cron-triggered)

## Planned removal
- `reapR2Orphans` function from `storage-orphan-reaper.ts`
- `ENABLE_R2_ORPHAN_REAPER` feature flag
- `/api/v1/internal/storage-orphan-reaper` route
- Cron schedule entry in docker-compose

## Related
- EXP-229 (env isolation — prerequisite, resolved)
- EXP-230 (PUT-first conversion — prerequisite, resolved)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
