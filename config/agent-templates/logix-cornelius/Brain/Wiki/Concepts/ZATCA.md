---
title: "ZATCA"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "topic/zatca"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/ZATCA.md"
---

# ZATCA — Saudi E-Invoicing Compliance

Saudi Arabia's Zakat, Tax and Customs Authority (ZATCA) Phase 2 e-invoicing mandate. All B2B invoices must be signed, reported, and archived in a compliant XML format.

## Context in Experts

Experts LMS generates invoices for course enrollments, event registrations, and subscriptions. Every invoice must pass through the ZATCA pipeline before it can be considered final. This is a hard compliance requirement for operating in Saudi Arabia.

## Architecture — The Pipeline

ZATCA processing is fully asynchronous via BullMQ. The app never blocks a payment response waiting for ZATCA.

```
Invoice created
  └─ invoice-create.handler.ts          adds DB invoice + lines + payments
       └─ enqueueInvoiceZatca(id)        zatca.jobs.ts → BullMQ queue "zatca"
            └─ zatca.worker.ts           picks job
                 └─ zatca.processor.ts  calls processZatcaJob()
                      └─ zatca.service.ts
                           ├─ creates/updates ZatcaDocument (status: pending_sign)
                           ├─ getInvoiceXmlPayload(prisma, invoiceId)
                           ├─ buildInvoiceXml(payload) → renderInvoiceXml(payload)
                           ├─ buildInvoiceLines(...)    ← "must have at least one item"
                           └─ signs XML → reports to ZATCA → stores signed doc
```

## Key Files (relative to `apps/experts-app/`)

| File                                                 | Role                                              |
| ---------------------------------------------------- | ------------------------------------------------- |
| `src/lib/billing/handlers/invoice-create.handler.ts` | Creates invoice, enqueues ZATCA job               |
| `src/queue/zatca.jobs.ts`                            | Enqueue helper — `enqueueInvoiceZatca(invoiceId)` |
| `src/workers/zatca.worker.ts`                        | BullMQ worker entry point                         |
| `src/workers/zatca.processor.ts`                     | Job processing orchestration                      |
| `src/modules/billing/zatca/zatca.service.ts`         | ZATCA business logic — XML + signing              |
| `src/modules/billing/zatca/prisma/zatca.payload.ts`  | Prisma query → XML payload shape                  |
| `pnpm worker:zatca` / `worker:zatca:test`            | Dev commands to run the worker                    |

## Worker Architecture Principle

Workers are intentionally dumb — they execute, not decide. Data ownership follows a 3-layer model:

1. **Repository layer** — Prisma queries only (`zatca.payload.ts`)
2. **Application layer** — API/handler fetches data, assembles job payload
3. **Worker layer** — receives payload, runs signing + reporting, writes result

The worker does not own DB knowledge. The handler owns what data goes into the job.

## ZatcaDocument States

| Status         | Meaning                            |
| -------------- | ---------------------------------- |
| `pending_sign` | XML built, awaiting signing        |
| `signed`       | Signed, awaiting ZATCA report      |
| `reported`     | Submitted to ZATCA clearance API   |
| `failed`       | Error in pipeline — job will retry |

## Known Gotcha

`buildInvoiceLines(...)` throws `"Invoice must have at least one item"` if the invoice has no line items. This is a valid guard — invoices with no lines should never reach the ZATCA pipeline.

## Related

- [[Wiki/Concepts/Payments]]
- [[Projects/Experts/Experts App/docs/reference/flows]]
- [[Projects/Experts/Experts App/docs/guides/workers]]
