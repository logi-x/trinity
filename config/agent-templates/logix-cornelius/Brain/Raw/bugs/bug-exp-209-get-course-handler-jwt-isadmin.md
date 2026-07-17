---
title: "EXP-209: GET course handler trusts JWT isAdmin without DB re-derivation"
linear_id: "EXP-209"
agent_fp: "auto"
date: "2026-05-30"
severity: "High"
status: "resolved"
resolution: "PR #654 — re-derive admin role from DB before returning draft course data"
tags: [bug, auth, jwt-staleness, security, project/experts]
category: "bug"
source: "automation"
---

# EXP-209: GET course handler JWT isAdmin staleness

**Linear:** [EXP-209](https://linear.app/experts/issue/EXP-209) | **Status:** Resolved (PR #654)

## Summary
The GET course handler returned draft/unpublished course data to callers whose JWT carried `isAdmin: true`, without re-deriving the role from the database. A revoked admin whose JWT had not yet expired retained read access to all unpublished course content.

## Impact
Revoked admin can read any unpublished course draft via the GET course endpoint until their JWT expires (up to 30 days).

## Fix
PR #654 added a DB role re-derivation step before authorizing the draft course data return.

## Related
- EXP-211, EXP-212, EXP-213 — same JWT staleness class on other course routes (open)
- PR #658 — getDbCourseActor shared helper (canonical pattern)
- 2026-05-29 Decision Log: JWT role-staleness deferred at infrastructure level

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
