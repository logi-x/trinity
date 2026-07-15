---
title: "WORKERS GUIDE"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/workers"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# WORKERS GUIDE

what you did in @apps/experts-app/src/adapters negates the whole idea of "I isolated the worker and made it dumb."

Meaning:
Worker should not own DB knowledge
Worker should not decide what to load or persist
Worker should just execute work

What you did means:
The adapter:
Knows what to load
Knows how to persist
Knows business relationships
The adapter is domain + persistence aware

👉 This is not a dumb adapter
👉 This is a repository + service combined

You didn’t make the worker dumb.
You made the worker compile independently.

Those are different things.
Isolation ≠ dumbness
Isolation just removed Next.js
Dumbness requires data ownership to move up

Correct mental model (very important)

Think in three layers, not two.

1️⃣ Repository layer (DB-only)
invoice.repository.ts

export async function fetchInvoiceForPdf(
prisma: PrismaClient,
invoiceId: string
): Promise<InvoicePdfRecord> {
return prisma.invoice.findUnique({
where: { id: invoiceId },
include: invoicePdfInclude,
});
}

export async function saveInvoicePdfFile(
prisma: PrismaClient,
data: InvoiceFileInput
) {
return prisma.invoiceFile.upsert({ ... });
}

Prisma lives here
No rendering
No workers

2️⃣ Application / orchestration layer (API / app)
invoice-pdf.service.ts

const invoice = await fetchInvoiceForPdf(prisma, invoiceId);

queuePdfJob({
invoice,
storage: { provider: "r2", bucket: "invoices" },
});

Owns:
What data is fetched
What job payload contains
Still Prisma-aware
Still business-aware

3️⃣ Worker layer (pure)
pdf.orchestrator.ts

export async function renderAndStorePdf(
invoice: InvoicePdfRecord,
storage: StorageConfig
) {
const pdf = await renderPdf(invoice);
await storePdf(pdf, storage);
}
❌ No Prisma
❌ No DB
✅ Deterministic
✅ Stateless
✅ Easily scalable

### Follow up

Below is a solid, scalable structure that matches:

what you already have,

your ZATCA + PDF shared flow,

dumb workers,

Prisma isolation,

and your existing mental model.

I’ll explain why each piece lives where it lives, not just where.

The guiding rule (keep this in your head)

Repositories talk to Prisma
Services orchestrate flows
Adapters transform / execute
Workers only call adapters

Everything below follows that rule.

Proposed high-level structure (billing domain)
src/
├── modules/
│ └── billing/
│ ├── invoices/
│ │ ├── repositories/
│ │ │ └── invoice.repository.ts
│ │ ├── includes/
│ │ │ └── invoice-pdf.include.ts
│ │ ├── dto/
│ │ │ └── invoice-pdf.dto.ts
│ │ └── types/
│ │ └── invoice.types.ts
│ │
│ ├── pdf/
│ │ ├── adapters/
│ │ │ └── pdf.orchestrator.ts
│ │ ├── renderers/
│ │ │ └── invoice-pdf.renderer.tsx
│ │ └── storage/
│ │ ├── r2.storage.ts
│ │ └── local.storage.ts
│ │
│ ├── zatca/
│ │ ├── repositories/
│ │ │ └── zatca.repository.ts
│ │ ├── services/
│ │ │ └── zatca.service.ts
│ │ └── dto/
│ │ └── zatca.dto.ts
│ │
│ └── services/
│ └── invoice-issuance.service.ts

Now let’s map this directly to what you asked.

1️⃣ invoice.repository.ts (Prisma lives here)

📍 Location

src/modules/billing/invoices/repositories/invoice.repository.ts

📌 Responsibilities

Fetch invoice data

Persist invoice artifacts (PDF, ZATCA docs)

Zero orchestration

Zero workers

Zero queues

import type { PrismaClient } from "@/generated/prisma/client";
import { invoicePdfInclude } from "../includes/invoice-pdf.include";

export async function getInvoiceForPdf(
prisma: PrismaClient,
invoiceId: string
) {
return prisma.invoice.findUniqueOrThrow({
where: { id: invoiceId },
include: invoicePdfInclude,
});
}

export async function upsertInvoicePdfFile(
prisma: PrismaClient,
data: {
invoiceId: string;
provider: "r2" | "local";
key: string;
size: number;
checksum: string;
}
) {
return prisma.invoiceFile.upsert({
where: { invoiceId: data.invoiceId },
create: data,
update: data,
});
}

✅ Prisma here is correct and expected
❌ Workers must never import this

2️⃣ invoice-issuance.service.ts (the orchestrator)

This is the missing center of gravity you were feeling.

📍 Location

src/modules/billing/services/invoice-issuance.service.ts

📌 Responsibilities

Coordinates ZATCA + PDF

Owns when to do what

Talks to repositories

Enqueues jobs

No rendering

No Prisma schema knowledge leaks

import { prisma } from "@/lib/prisma";
import { getInvoiceForPdf } from "../invoices/repositories/invoice.repository";
import { enqueuePdfJob } from "@/queue/pdf.jobs";
import { enqueueZatcaJob } from "@/queue/zatca.jobs";

export async function issueInvoice(invoiceId: string) {
// 1. ZATCA first
await enqueueZatcaJob({ invoiceId });

// 2. Fetch once, pass data
const invoice = await getInvoiceForPdf(prisma, invoiceId);

// 3. PDF job with data, not DB access
await enqueuePdfJob({
invoice,
storage: { provider: "r2" },
});
}

💡 This replaces tight coupling with intentional orchestration

3️⃣ zatca.service.ts (already exists — good)

You already have:

src/modules/billing/zatca/zatca.service.ts

That’s correct 👍
Just make sure it:

Calls repositories

Does not enqueue PDF directly

Returns results or events

It should not import workers.

4️⃣ pdf.orchestrator.ts (pure execution)

📍 Location

src/modules/billing/pdf/orchestrators/pdf.orchestrator.ts

📌 Responsibilities

Accepts data, not IDs

No Prisma

No queue

No domain logic

import type { InvoicePdfDTO } from "../../invoices/dto/invoice-pdf.dto";
import { renderInvoicePdf } from "../renderers/invoice-pdf.renderer";
import { storePdf } from "../storage";

export async function generateInvoicePdf(
invoice: InvoicePdfDTO,
storage: StorageConfig
) {
const pdf = await renderInvoicePdf(invoice);
return storePdf(pdf, storage);
}

If Prisma shows up here → architecture regression

5️⃣ Worker becomes trivial (as it should)

📍 src/workers/pdf/pdf.worker.ts

import { generateInvoicePdf } from "@/modules/billing/pdf/orchestrators/pdf.orchestrator";

export async function processPdfJob(job: PdfJob) {
return generateInvoicePdf(job.invoice, job.storage);
}

That’s it.

No Prisma.
No schema imports.
No deep module chains.

Why this structure works (and scales)

✅ Prisma versioning isolated

✅ Workers are dumb & portable

✅ ZATCA + PDF share orchestration cleanly

✅ Testing is easy at every layer

✅ Future microservice split is trivial

Final reassurance (important)

You didn’t over-engineer.
You discovered where the real boundaries are.
