---
title: "EXP-99 — subscription checkout route missing Tabby KSA eligibility check — non-SA users get 502 instead of 400"
date: "2026-05-24"
status: open
resolution: unknown
tags: [bug, payments, tabby, subscriptions, eligibility, project/experts]
linear: "https://linear.app/experts/issue/EXP-99/bug-subscription-checkout-route-missing-tabby-ksa-eligibility-check"
fingerprint: "984201e58b86"
---

## Summary

`POST /api/v1/commerce/subscriptions/checkout` with `provider: "tabby"` from a non-KSA user is accepted by the route without a KSA eligibility check. The route includes Tabby in its `PAYMENT_PROVIDERS` list but does not call the Tabby eligibility gate. The Tabby gateway rejects the request and returns a 502, with no structured error message surfaced to the caller.

PR #439/#440 (EXP-96) added a KSA eligibility gate to the course/event checkout flow, but the subscription checkout route was not updated.

## Root cause

`apps/experts-app/app/api/v1/commerce/subscriptions/checkout/route.ts` — Tabby is accepted as a valid `provider` value but no eligibility gate (equivalent to the `resolveTabbyEligibility` check added for course/event checkout in EXP-96) is applied before calling the Tabby gateway. Non-SA users reach the gateway, which rejects them with a 502. The fix pattern is established: apply the same KSA eligibility check that was added for course/event checkout.

## Agent fingerprint

`<!-- agent-fp: 984201e58b86 -->`

## Status

`open` — Todo (No priority set). Tabby surface expansion from EXP-96 fix; same eligibility gap on a sibling route. Fix is well-understood (port EXP-96 pattern to subscription checkout route).

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
