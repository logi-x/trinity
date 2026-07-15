---
title: "EXP-210: Course publish route parses request body before auth check"
linear_id: "EXP-210"
agent_fp: "auto"
date: "2026-05-30"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, auth, order-of-operations, project/experts]
category: "bug"
source: "automation"
---

# EXP-210: Publish route body parse before auth

**Linear:** [EXP-210](https://linear.app/experts/issue/EXP-210) | **Status:** Open

## Summary
The course publish route calls `req.json()` (body parse) before performing the authentication check. Unauthenticated callers can consume the request body and trigger any body-parse side effects before being rejected with 401.

## Impact
Waste of server resources; potential for body-parse-level exploits if the JSON parser has edge cases. Mildly increases the attack surface for unauthenticated callers.

## Fix Needed
Move authentication check (session resolution + role derivation) to before the `req.json()` call. Return 401 before consuming the body for unauthenticated requests.

## Related
- EXP-209, EXP-211–213 — JWT staleness spinoffs from same PR #619 batch

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
