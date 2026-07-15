---
title: "Operation - verify current"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["ops", "freshness", "verification"]
category: "tools/ops"
source: "generated"
source_id: "Tools/Ops/verify-current.md"
---

# Operation - verify current

Use when the user asks for current state, latest status, open issues, deployment health, PR state, live roadmap, or anything likely to change.

## Steps

1. Read the relevant vault page.
2. Check its freshness metadata:
   - `freshness`
   - `verified`
   - `source_of_truth`
   - `verify_with`
3. If `freshness` is `volatile` or `live`, do not present the vault as current truth without verification.
4. Verify against the listed source of truth when available.
5. Answer in two sections:
   - **Vault State** - what the vault says and the `verified` date.
   - **Current Verification** - what was checked now, or what could not be checked.

## Freshness Levels

- `stable` - rarely changes; no live check needed for ordinary questions.
- `slow` - changes occasionally; mention verified date.
- `volatile` - changes weekly/daily; verify before saying "current".
- `live` - must be checked at source before answering current status.

## Standard Wording

When not verified live:

> Vault knowledge is current as of `<verified>`. Because this page is `<freshness>`, verify against `<source_of_truth>` before treating it as current truth.

