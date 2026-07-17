---
title: "EXP-83 — VALIDATE course_isfree_price_consistency constraint after prod data sweep (EXP-73 follow-up)"
date: "2026-05-22"
status: open
resolution: unknown
tags: [bug, data-integrity, courses, prisma, project/experts]
linear: "https://linear.app/experts/issue/EXP-83/bug-validate-course-isfree-price-consistency-constraint-after-prod"
fingerprint: "2b75b1305d16"
---

## Summary

PR #398 (EXP-73) added a DB `CHECK` constraint `course_isfree_price_consistency` to enforce that `isFree = true` courses have `price = 0`/`NULL` and `isFree = false` courses have a positive price. The migration was created `NOT VALID` — the constraint exists but is not enforced on existing rows. Running `VALIDATE CONSTRAINT` will fail if any existing rows violate the invariant. A production data sweep is required first.

## Repro steps

1. Run `SELECT id, "isFree", price FROM courses WHERE ("isFree" = true AND price > 0) OR ("isFree" = false AND (price IS NULL OR price = 0))` on production.
2. If any rows returned: fix the data.
3. Then run `ALTER TABLE courses VALIDATE CONSTRAINT course_isfree_price_consistency`.

## Agent fingerprint

`<!-- agent-fp: 2b75b1305d16 -->`

## Status

`open` — Backlog. Do NOT run `VALIDATE CONSTRAINT` until the production data sweep confirms no violating rows.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
