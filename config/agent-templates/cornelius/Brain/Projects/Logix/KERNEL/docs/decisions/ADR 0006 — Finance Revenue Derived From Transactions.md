---
title: "ADR 0006 — Finance Revenue Derived From Transactions"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/adr", "topic/finance"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
source_id: "docs/adr/0006-finance-revenue-derived-from-transactions.md"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# ADR 0006: Finance Revenue Derived From Transactions

## Status

Accepted.

## Context

Finance had two disconnected systems. Dashboard analytics read `totalRevenue`/monthly revenue from frozen `RevenueRecord` workbook snapshots (plus unused `FinanceMetricSnapshot`), while live invoicing and payments did not move the numbers. `RevenueRecord.invoiceId` was never populated.

## Decision

Revenue is derived live from transactional data:

- **Invoiced (accrual)** — sum of `total` on invoices not in `draft`, `cancelled`, or `written_off`.
- **Collected (cash)** — sum of `InvoicePayment.amount` on those invoices.
- **Outstanding** — sum of `Invoice.balance` with positive balance (same status filter).
- **Manual income** — `RevenueRecord` with `invoiceId: null` and `type: 'manual'`.
- **`totalRevenue` = Invoiced + Manual**; collected reported separately (no double-count).

Dual-currency amounts normalize to SAR via `convertToSar` and workspace exchange rate (`getFinanceExchangeRate`, default 3.75 SAR/USD). Workbook `type: 'invoice'` rows excluded from manual query to avoid double count with real invoices. `FinanceMetricSnapshot` retired.

## Consequences

Dashboard reflects live invoice/payment activity. Totals may read lower than historical workbook until Phase 3 backfill — expected.

Deferred: full finance CRUD beyond existing surfaces (Phase 2), workbook backfill (Phase 3), distinct Invoiced/Collected/Outstanding UX cards (Phase 4).

**Follow-up:** analytics `query.currency` may not filter `invoicePayments` by currency — revisit when hardening currency scope.
