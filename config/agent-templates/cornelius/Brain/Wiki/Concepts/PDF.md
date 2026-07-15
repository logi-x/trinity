---
title: "PDF"
date: "2026-04-10"
updated: "2026-05-10"
tags: ["entity", "topic", "topic/pdf"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/PDF.md"
---

# PDF

PDF generation in Experts is handled as async work for certificates, invoices, credit notes, and other downloadable documents that should not block normal request latency.

## Context in Experts

The main web app runs a dedicated PDF worker from within Experts App. In the monorepo, this is treated as queue-driven infrastructure rather than a separate service.

## Architecture

[[Wiki/Concepts/Monorepo]] documents `pnpm worker:pdf` as one of the worker commands inside `apps/experts-app`. That makes PDF generation part of the same BullMQ + Redis operational model as ZATCA processing.

## Common uses

- Course or event certificates
- Invoice and billing documents
- Credit note generation
- Downloadable admin or learner-facing attachments

## Design principle

PDF work should be retriable and operationally isolated from the main HTTP request path. For billing-related PDFs, the document pipeline also intersects with [[Wiki/Concepts/ZATCA]] and [[Wiki/Concepts/Payments]].

## Known gotchas

- React-PDF font family names must match registered `Font.register()` families exactly. Invoice branding may store CSS/display names such as `Readex Pro` or `DM Sans`, while the registered PDF families are `ReadexPro` and `DMSans`; resolve aliases before passing font names into PDF components.

## Related

- [[Wiki/Concepts/Monorepo]]
- [[Wiki/Concepts/ZATCA]]
- [[Projects/Experts/Experts App/docs/guides/workers]]
