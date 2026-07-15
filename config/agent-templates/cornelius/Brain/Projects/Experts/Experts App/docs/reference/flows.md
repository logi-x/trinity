---
title: "ZATCA DATA FLOW (HAPPY PATH)"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/flows"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# ZATCA DATA FLOW (HAPPY PATH)

ZATCA data flow (happy path)

1. Invoice created
   - apps/experts-app/src/lib/billing/handlers/invoice-create.handler.ts
   - Adds DB invoice + lines + payments
2. ZATCA enqueue
   - apps/experts-app/src/queue/zatca.jobs.ts → enqueueInvoiceZatca(invoice.id)
   - Job goes to BullMQ queue zatca
3. Worker picks job
   - apps/experts-app/src/workers/zatca.worker.ts
   - Calls processZatcaJob in apps/experts-app/src/workers/zatca.processor.ts
4. ZATCA service
   - apps/experts-app/src/modules/billing/zatca/zatca.service.ts
   - Creates/updates ZatcaDocument (pending_sign) and calls XML build
5. Payload → XML
   - apps/experts-app/src/modules/billing/zatca/prisma/zatca.payload.ts
   - getInvoiceXmlPayload(prisma, invoiceId)
   - buildInvoiceXml(payload) → renderInvoiceXml(payload)
   - buildInvoiceLines(...) (error “Invoice must have at least one item” comes from here)
