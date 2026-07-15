---
title: "EXP-196: manageCurriculum button inverted — active courses locked out, archived courses editable"
linear_id: "EXP-196"
agent_fp: "e9bb508fbffa"
date: "2026-05-29"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, courses, ui, project/experts]
category: "bug"
source: "automation"
---

# EXP-196: manageCurriculum ternary inverted

**Linear:** [EXP-196](https://linear.app/experts/issue/EXP-196) | **Fingerprint:** `e9bb508fbffa`

## Summary
`CourseOverviewPage` Quick Actions card introduced in PR #619 (merged 2026-05-29T17:27Z) has an inverted `manageCurriculum` guard: `disabled={!isArchived}` instead of `disabled={isArchived}`. Active (non-archived) courses show the Manage Curriculum button as disabled, completely locking creators out of the curriculum editor. Archived courses incorrectly show the button as enabled.

## Repro
1. Login as instructor. Navigate to an active course → `/creator/courses/<id>`.
2. Quick Actions card → "Manage Curriculum" button is disabled.
3. Navigate to an archived course → button is enabled (wrong).

## Fix needed
In `apps/experts-app/app/(i18n)/_shared/creator/courses/[id]/page.tsx` `CourseOverviewPage` `manageCurriculum` button: change `disabled={!isArchived}` → `disabled={isArchived}`. Introduced by commit `de6c28f30171`.

## Related
PR #619 (introduced regression), EXP-197/198/199 (JWT staleness on same PR's API surface)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
