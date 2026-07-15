---
title: "EXP-129: Tabby verify/webhook paths bypass KSA geo-restriction entirely"
linear_id: "EXP-129"
agent_fp: "eda48e2b7a57"
date: "2026-05-25"
severity: "High"
status: "Backlog"
tags: [bug, security, tabby, payment, geo-restriction, ksa, project/experts]
category: "bug"
source: "automation"
---

# EXP-129: Tabby verify/webhook paths bypass KSA geo-restriction entirely

**Linear:** EXP-129 | **Fingerprint:** `<!-- agent-fp: eda48e2b7a57 -->` | **Severity: High**

## Summary

Tabby is a KSA-only (Saudi Arabia) buy-now-pay-later provider. The checkout eligibility check enforces KSA geo-restriction using `CF-IPCountry` + `CF_ORIGIN_SECRET` verification. However, the `verify` and `webhook` paths for Tabby do **not** apply this geo-restriction check. An attacker from outside KSA can POST to these endpoints to:

1. Forge a payment completion event (via the `verify` path) for an existing Tabby session ID.
2. Inject forged webhook events (via the `webhook` path) that mark orders as paid.

## Impact

- **Payment bypass**: Forged `verify` or `webhook` POSTs from non-KSA IPs can mark orders as completed without real payment.
- **Financial loss**: Every forged completion represents an order fulfilled without payment.
- **High severity** — direct financial impact; affects the payment processing flow.

## Root Cause

The KSA geo-restriction was added to the **checkout eligibility** route (Tabby availability check) but was not propagated to the **fulfillment routes** (`verify`, `webhook`). The assumption was that only KSA users would attempt checkout; this ignores that fulfillment paths are also externally accessible.

Note: `verify` may be called by the user's browser after a Tabby redirect, while `webhook` is called by Tabby's servers. For the webhook path specifically, the fix should validate Tabby's HMAC signature (`TABBY_WEBHOOK_SECRET`) rather than rely on geo-restriction — Tabby's servers may not originate from KSA IPs.

## Fix

**For `verify` path (browser-facing):**
Apply the same CF-IPCountry + CF_ORIGIN_SECRET check as the checkout eligibility route.

**For `webhook` path (Tabby-server-facing):**
Validate the HMAC signature using `TABBY_WEBHOOK_SECRET` (per the 2026-05-13 decision: payment webhook providers must fail-closed in production when signing secret is unset). Do NOT rely on geo-restriction for server-to-server webhooks.

Additionally, consider validating the `sessionId` in the `verify` body against a pending Tabby order in the DB to prevent replay of expired or foreign session IDs.

## Related

- EXP-99 (Tabby eligibility pre-check — where geo-restriction was first added)
- EXP-100 (CF-IPCountry spoofing — root fix)
- EXP-123 (CF_ORIGIN_SECRET absent on non-prod)
- Decision-Log: payment webhook providers fail closed (2026-05-13)
- Decision-Log: CF-IPCountry as display-only hint (2026-05-24)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
