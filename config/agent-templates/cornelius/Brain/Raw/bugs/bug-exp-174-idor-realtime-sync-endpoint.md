---
title: "EXP-174: IDOR in realtime sync endpoint — arbitrary post activity accessible via user-supplied channels"
linear_id: "EXP-174"
agent_fp: "8ae9786514bf"
date: "2026-05-28"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, api, project/experts]
category: "bug"
source: "automation"
---

# EXP-174: IDOR in realtime sync endpoint

**Linear:** [EXP-174](https://linear.app/experts/issue/EXP-174) | **Fingerprint:** `8ae9786514bf`

## Summary
`GET /api/v1/internal/realtime/sync` accepts a `channels` query parameter containing user-supplied `viewingPostIds`. There is no ownership or access check on the supplied post IDs. Any authenticated user can query activity data for arbitrary posts they do not have access to.

## Location
`apps/experts-app/app/api/v1/internal/realtime/sync/route.ts` — `viewingPostIds` extraction block (~lines 156-170)

## Impact
Authenticated users can leak post activity (view counts, engagement data) for posts they are not permitted to see, including private/unpublished content.

## Fix
Validate that the authenticated user has read access to each supplied `viewingPostId` before returning activity data. Apply ownership check consistent with the content visibility rules.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
