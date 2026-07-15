---
title: "EXP-180: Profile default cover 404s from files.experts.com.sa"
linear_id: "EXP-180"
agent_fp: "manual-exp180"
date: "2026-05-28"
severity: "High"
status: "resolved"
resolution: "merged PR #587 — resolveStoredCoverPhoto() path-based URL filtering"
tags: [bug, profile, storage, project/experts]
category: "bug"
source: "automation"
---

# EXP-180: Profile default cover 404

**Linear:** [EXP-180](https://linear.app/experts/issue/EXP-180) | **Fingerprint:** `manual-exp180`

## Summary
Profiles with a legacy/default `coverPhoto` value pointing at the user-uploads origin (`files.experts.com.sa/images/og_cover.png`) rendered a broken image (404). The value was stale data from before the EXP-77 origin split; the key doesn't exist on the uploads origin.

## Fix
PR #587: new `resolveStoredCoverPhoto()` helper in `cover-photo.util.ts` — returns `coverPhoto` only when its URL path is under `/uploads/` (a genuine upload), otherwise `null`, allowing the `brand("cover.png")` static CDN fallback to take effect. Applied in both profile DTO queries and `user-metadata.ts`. Operator (optional): null stale `Profile.coverPhoto NOT LIKE '%/uploads/%'`.

## Related
EXP-179 (cover photo UX), EXP-77 (origin split)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
