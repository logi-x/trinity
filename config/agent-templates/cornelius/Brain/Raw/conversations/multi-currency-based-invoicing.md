---
title: Multi-Currency Based Invoicing
date: 2026-05-18
source: "generated"
source_id: "Raw/conversations/multi-currency-based-invoicing.md"
tags: [multi-currency, invoicing, project/experts, app]
category: "conversation"
---

Q: For the past days, I’ve been working on enabling multi currency for Experts, and landed on

A course/event can be listed in many currencies e.g., EUR, USD, CNY, GBP

Then when a user clicks on pay button, the amount gets converted to SAR based on live FX rate against listed currency-> redirected to noon payment gateway-> pay in SAR with Visa/MC for Intl’ then the rest of the internal processes are left the same stored as SAR reported to ZATCA, invoice issued all in SAR

Now the client is asking, can we issue the invoice in EUR not in SAR ?

---

Technically yes. Legally/accounting-wise, you should separate **the invoice currency** from **the tax reporting currency**.

For Saudi Arabia and ZATCA, the key requirement is that VAT amounts must be represented in SAR for tax purposes, using the applicable exchange rate when the invoice is issued. The invoice itself may be issued in a foreign currency such as EUR. The VAT amount (or at least the VAT equivalent used for tax reporting) must be available in SAR. ZATCA's e-invoice model supports foreign currency invoices. However, all tax reporting to ZATCA remains SAR-based.

For your architecture, that means:

| Item                       | Currency       |
| -------------------------- | -------------- |
| Course/Event listing       | EUR            |
| Checkout displayed to user | EUR            |
| FX conversion at payment   | EUR → SAR      |
| Noon payment               | SAR            |
| Actual collected amount    | SAR            |
| ZATCA reporting            | SAR            |
| Customer invoice           | EUR (possible) |

The bigger question is **what amount should appear on the EUR invoice?**

### Option A — Invoice shows EUR (recommended if client insists)

Store at checkout:

```text
Original Currency: EUR
Original Amount: €500.00

FX Rate:
1 EUR = 4.3500 SAR

Settlement Amount:
SAR 2,175.00
```

Then generate:

```text
Invoice Currency: EUR
Subtotal: €434.78
VAT 15%: €65.22
Total: €500.00
```

while internally keeping:

```text
SAR Total: 2,175.00
SAR VAT: 283.70
```

This is the cleanest model because the invoice matches what the customer saw and agreed to purchase.

---

### Option B — Invoice shows SAR

Current design:

```text
Subtotal: SAR 1,891.30
VAT: SAR 283.70
Total: SAR 2,175.00
```

Simpler and matches payment gateway settlement exactly.

---

### What I would do for Experts

Since you're building a global education/events platform:

1. Keep the **listing currency** as the merchant's chosen currency (EUR, USD, GBP, etc.).
2. Keep the **checkout currency** equal to the listing currency.
3. Store the locked FX rate used during checkout.
4. Generate the customer invoice in the listing currency.
5. Store SAR equivalents for accounting and ZATCA.
6. Continue sending only SAR amounts to Noon.

In other words, add fields such as:

```sql
currency_code         EUR
subtotal_amount       434.78
vat_amount            65.22
total_amount          500.00

sar_subtotal_amount   1891.30
sar_vat_amount        283.70
sar_total_amount      2175.00

fx_rate               4.3500
```

This gives you:

* Correct customer-facing invoice.
* Correct ZATCA compliance.
* Future support for Stripe, Adyen, PayPal, etc.
* No dependence on SAR as the business expands internationally.

One thing I would avoid is generating a EUR invoice **from the SAR amount after payment**. Once you convert EUR → SAR and then later derive EUR again, you introduce rounding differences. Instead, treat the original EUR amount as the source of truth and SAR as the reporting/settlement currency.
