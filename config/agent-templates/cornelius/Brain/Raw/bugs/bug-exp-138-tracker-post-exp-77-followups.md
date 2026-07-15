---
title: "EXP-138: [tracker] Post-EXP-77 follow-ups (origin split aftermath)"
linear_id: "EXP-138"
agent_fp: ""
date: "2026-05-26"
severity: "Medium"
status: "in-progress"
resolution: "unknown"
tags: [bug, completeness, tracker, r2, origin-split, project/experts]
category: "bug"
source: "automation"
---

# EXP-138: [tracker] Post-EXP-77 follow-ups (origin split aftermath)

**Linear:** [EXP-138](https://linear.app/experts/issue/EXP-138) | **Severity: Medium** | **Status: In Progress**

## Summary

Umbrella tracker for completeness gaps discovered after EXP-77 (user-uploads origin split) shipped. EXP-77 itself is Done (DNS + URL helper + CSP widening landed in PR #449 / PR #454). This tracker exists because R7 (codebase-completeness audit) surfaced four post-merge gaps that all stem from the split not being applied atomically across write-path, URL-helper, env-documentation, and seeder references.

## Sub-issues

| # | Title | Status |
|---|-------|--------|
| EXP-134 | R2_BUCKET_STATIC write target misaligned with R2_USER_UPLOADS_PUBLIC_URL | In Progress |
| EXP-135 | R2_BUCKET_CERTIFICATIONS missing from .env.example | In Progress |
| (seeder URLs) | User seeder still references old bucket URLs | tracked under umbrella |
| (avatar/cover deletion) | Avatar and cover photo deletion paths reference wrong bucket after split | tracked under umbrella |

## Related

- EXP-77 (the origin-split PR that shipped the gaps)
- EXP-134, EXP-135 (direct children)
- Decision-Log 2026-05-23: runtime-signed CDN domain policy

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
