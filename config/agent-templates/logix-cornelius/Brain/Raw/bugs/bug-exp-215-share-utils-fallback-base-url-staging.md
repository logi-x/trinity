---
title: "EXP-215: share-utils getShareUrl() falls back to staging URL when NEXT_PUBLIC_APP_URL unset"
linear_id: "EXP-215"
agent_fp: "auto"
date: "2026-05-30"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, url, config, project/experts]
category: "bug"
source: "automation"
---

# EXP-215: share-utils staging URL fallback

**Linear:** [EXP-215](https://linear.app/experts/issue/EXP-215) | **Status:** Open

## Summary
`getShareUrl()` in `src/lib/utils/share-utils.ts` was missed by the PR #665 canonical-app-URL sweep. It still falls back to `https://staging.experts.com.sa` when `NEXT_PUBLIC_APP_URL` is not set, minting share links that point at the staging environment in production.

## Fix Needed
Replace the staging fallback with a call to `getAppBaseUrl()` from `src/lib/config/app-url.ts`. This will throw in production if `NEXT_PUBLIC_APP_URL` is absent (fail-closed, consistent with the rest of the canonical resolver).

## Related
- EXP-204, EXP-216, EXP-217, EXP-218 — same root cause, resolved by PR #665
- `src/lib/config/app-url.ts` — canonical resolver (PR #665)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
