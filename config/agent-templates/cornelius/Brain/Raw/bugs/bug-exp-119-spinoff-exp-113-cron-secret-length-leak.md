---
title: "EXP-119: CRON_SECRET comparison length leak via timing side-channel"
linear_id: "EXP-119"
agent_fp: "bcefb2624c8b"
spinoff_of: "EXP-113"
date: "2026-05-25"
severity: "Medium"
status: "Todo"
tags: [bug, security, cron, timing, project/experts]
category: "bug"
source: "automation"
---

# EXP-119: CRON_SECRET comparison length leak via timing side-channel

**Linear:** EXP-119 | **Fingerprint:** `<!-- agent-fp: bcefb2624c8b -->` | **Spinoff of:** EXP-113

## Summary

The `CRON_SECRET` comparison in the route associated with `checkAndSendStorageAlerts` leaks the secret's byte length via a timing side-channel. `timingSafeEqual` requires that the two buffers being compared have equal length; if the implementation checks `provided.length !== secret.length` before calling `timingSafeEqual`, the early exit leaks the secret length.

## Impact

- An attacker can determine the exact byte-length of `CRON_SECRET` by observing whether requests with different-length Authorization headers receive an immediate vs. slightly-delayed rejection.
- Knowing the length reduces the brute-force search space from O(charset^N) to O(charset^known_N).
- Moderate severity: useful only in combination with the timing oracle from EXP-111/EXP-115/EXP-116.

## Root Cause

Naive "guard with length check first, then `timingSafeEqual`" pattern. The length check short-circuits before the constant-time comparison.

## Fix

Pad both buffers to the same length before comparison, or always compare at the length of the secret using a HMAC-based approach:

```ts
// Correct approach — never early-exit on length
const secretBuf = Buffer.alloc(64);
Buffer.from(secret).copy(secretBuf);
const providedBuf = Buffer.alloc(64);
Buffer.from(provided.slice(0, 64)).copy(providedBuf);
if (!timingSafeEqual(secretBuf, providedBuf)) { ... }
```

Or use HMAC comparison (zero-allocates the length leak entirely).

## Related

- EXP-113 (parent), EXP-111 (reaper routes), EXP-116 (admin cron — same pattern)
- Decision-Log: `timingSafeEqual` cron auth invariant (2026-05-25)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
