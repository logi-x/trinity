---
title: "EXP-179: Profile cover photo — no live update, inconsistent buttons, wrong crop"
linear_id: "EXP-179"
agent_fp: "manual-exp179"
date: "2026-05-28"
severity: "Medium"
status: "resolved"
resolution: "merged PR #585"
tags: [bug, profile, ui, project/experts]
category: "bug"
source: "automation"
---

# EXP-179: Profile cover photo UX issues

**Linear:** [EXP-179](https://linear.app/experts/issue/EXP-179) | **Fingerprint:** `manual-exp179`

## Summary
Three UX bugs in `profile-header.tsx`: (1) new cover didn't appear until page refresh — `handleCoverChange` discarded the server-returned URL; (2) inconsistent button hover behaviour dark/light; (3) crop was using incorrect 1500×500 dimensions instead of 4:1 banner.

## Fix
PR #585: `coverOverride` state added for immediate live update; `router.refresh()` called after upload; 4:1 banner enforced; scrim action buttons for consistent hover. Cross-tab freshness preserved via router refresh.

## Related
EXP-180 (default cover 404)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
