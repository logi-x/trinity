---
title: "EXP-114: storage-janitor CRON_SECRET fail-open (plain !== check)"
linear_id: "EXP-114"
agent_fp: "424dfaf70d53"
spinoff_of: "EXP-111"
date: "2026-05-25"
severity: "High"
status: "Backlog"
tags: [bug, security, cron, project/experts]
category: "bug"
source: "automation"
---

# EXP-114: storage-janitor CRON_SECRET fail-open (plain !== check)

**Linear:** EXP-114 | **Fingerprint:** `<!-- agent-fp: 424dfaf70d53 -->` | **Spinoff of:** EXP-111

## Summary

The `storage-janitor` cron route compares `CRON_SECRET` using plain `!==` string comparison. If `CRON_SECRET` is absent from the environment, the check short-circuits to `false` (or `undefined !== undefined` → `false`), making the route fail-open: any caller who sends an empty or missing Authorization header can trigger the janitor.

## Impact

- Any request reaching the internal cron endpoint can trigger storage janitor execution without authentication.
- Fail-open on missing secret means a misconfigured deployment (missing env var) silently removes security entirely.
- Janitor may compact or delete storage artifacts, so uncontrolled invocation is destructive.

## Root Cause

Identical root cause to EXP-111. The `timingSafeEqual` pattern introduced in PR #470 (`reservation-cleanup`) was not backported to the `storage-janitor` route. Plain `!==` is both timing-unsafe and fail-open.

## Fix

Replace the comparison with:

```ts
import { timingSafeEqual } from "crypto";

const secret = process.env.CRON_SECRET;
if (!secret) return new Response("Forbidden", { status: 403 });
const provided = req.headers.get("Authorization")?.replace("Bearer ", "") ?? "";
if (!timingSafeEqual(Buffer.from(secret), Buffer.from(provided))) {
  return new Response("Forbidden", { status: 403 });
}
```

## Related

- EXP-111 (parent — reaper routes), EXP-115 (ai/embeddings/sync), EXP-116 (admin cron routes)
- Decision-Log: `timingSafeEqual` cron auth invariant (2026-05-25)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
