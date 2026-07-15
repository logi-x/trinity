---
title: "EXP-99 — Subscription checkout missing Tabby eligibility pre-check"
date: "2026-05-24"
status: resolved
resolution: "PR #455: call Tabby eligibility API before rendering the checkout button; surface a localised error if the user's locale/cart is ineligible rather than failing at payment confirmation."
tags: [bug, payments, tabby, subscriptions, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-99"
fingerprint: "agent-fp:R2-tabby-checkout-001"
---

## Summary

The subscription checkout flow rendered the Tabby instalment payment button without first verifying eligibility. Users in unsupported locales or with ineligible cart values would proceed to the Tabby SDK only to receive an opaque rejection.

## Root cause

Tabby requires an eligibility pre-check (`POST /checkout`) before presenting the payment button. This call was performed by the course checkout flow but was missing from the subscription checkout path.

## Agent fingerprint

`<!-- agent-fp:R2-tabby-checkout-001 -->`

## Status

Resolved — PR #455 merged 2026-05-24.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
