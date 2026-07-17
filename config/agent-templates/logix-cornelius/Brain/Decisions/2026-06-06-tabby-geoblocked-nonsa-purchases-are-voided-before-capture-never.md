---
title: "Tabby geo-blocked (non-SA) purchases are voided BEFORE capture, never auto-refunded. The webhook geo-gate moved ahead of"
date: "2026-06-06"
decision: "Tabby geo-blocked (non-SA) purchases are voided BEFORE capture, never auto-refunded. The webhook geo-gate moved ahead of `captureTabbyPayment`; `closeTabbyPayment` cancels the authorization so funds a"
stakeholders: "Logix, Payments"
review_by: "2026-09-07"
source: "[[Raw/sources/2026-06-07-experts-decision-blocked-five]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Tabby geo-blocked (non-SA) purchases are voided BEFORE capture, never auto-refunded. The webhook geo-gate moved ahead of `captureTabbyPayment`; `closeTabbyPayment` cancels the authorization so funds are never taken; an already-captured race is left to the admin RefundRequest flow with an `error`-level alert. (EXP-305 / PR #881)

**Rationale:** Voiding before capture eliminates the money-without-fulfillment case for the common path, so an automated refund path — with its fee, settlement delay, and ledger/ZATCA complications — is unnecessary. **No invoice is created for a blocked purchase** (completion never runs), so there is nothing to reverse. The rare already-captured race is low-volume and better handled by a human via the existing admin refund mechanism.

**Stakeholders:** Logix, Payments

**Source:** [[Raw/sources/2026-06-07-experts-decision-blocked-five]]
