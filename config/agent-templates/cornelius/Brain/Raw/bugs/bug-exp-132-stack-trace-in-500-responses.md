---
title: "EXP-132: Stack trace unconditionally exposed in lesson video route error responses"
linear_id: "EXP-132"
agent_fp: "e9da01839dd5"
date: "2026-05-26"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, information-disclosure, video, project/experts]
category: "bug"
source: "automation"
---

# EXP-132: Stack trace unconditionally exposed in lesson video route error responses

**Linear:** [EXP-132](https://linear.app/experts/issue/EXP-132) | **Fingerprint:** `<!-- agent-fp: e9da01839dd5 -->` | **Severity: Medium**

## Summary

Both the `POST` (video upload) and `DELETE` (video removal) handlers in the lesson video route include a `stack` field in their 500-error JSON responses **without** an environment guard. Any authenticated instructor or admin who can trigger a server error on these routes receives the full stack trace, exposing internal file paths, module names, and dependency versions.

## Impact

- **Information disclosure**: Full server-side stack traces exposed to any authenticated user who can trigger a 500 on the video upload or delete route. Provides attackers with internal path layout, framework versions, and error origin for targeted exploitation.
- **Inconsistency**: The `detail` field in the same handlers is guarded by `APP_ENV !== 'production'`; `stack` is not. The guard exists but is applied to the wrong field.

## Root Cause

In both the POST and DELETE catch blocks:

```typescript
return NextResponse.json({ error: '...', stack: err.stack }, { status: 500 });
```

The `stack` field is included unconditionally. The `detail` field in the same handler is conditionally included based on `APP_ENV !== 'production'`, but no such guard exists for `stack`.

## Fix

Wrap `stack` in the same environment guard applied to `detail`:

```typescript
return NextResponse.json({
  error: 'Internal server error',
  ...(process.env.APP_ENV !== 'production' && { detail: err.message, stack: err.stack }),
}, { status: 500 });
```

Apply to both the POST and DELETE handlers.

## Related

- EXP-131 (video DELETE removes R2 before DB — related handler)
- EXP-130 (video upload+delete quota issue — related handler)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
