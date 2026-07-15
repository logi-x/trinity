---
title: "WORKERS V3 ZATCA"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/workers-v3-zatca"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# WORKERS V3 ZATCA

ZATCA looks different — but it’s actually the same pattern

Let’s rewrite your ZATCA access list with ownership highlighted.

ZATCA Reads

zatcaDocument.findUnique → state

invoice.findUnique → input

creditNote.findUnique → input

sellerZatcaProfile.findFirst → configuration

ZATCA Writes

zatcaDocument.update → state transitions

invoice.update → state transitions

creditNote.update → state transitions

So the real question is:

Who should own ZATCA state transitions?

ZATCA is app-owned state (PDF-style, cleaner)

App owns all state, worker is pure execution

This is what you’re asking about — and yes, it’s possible.

How to structure ZATCA like PDF (recommended)
1️⃣ Split ZATCA into 3 explicit layers
modules/
└─ billing/
└─ zatca/
├─ repositories/
│ └─ zatca.repository.ts ← Prisma only
├─ services/
│ └─ zatca.service.ts ← orchestration (app)
├─ domain/
│ └─ zatca.types.ts ← pure types
└─ workers/
└─ zatca.executor.ts ← NO Prisma

2️⃣ Repository layer (Prisma lives here)
// zatca.repository.ts
export async function getZatcaContext(prisma, invoiceId) {
return prisma.invoice.findUnique({
where: { id: invoiceId },
include: { sellerProfile: true, zatcaDocument: true },
});
}

export async function persistZatcaResult(prisma, result) {
await prisma.$transaction([
prisma.zatcaDocument.update(...),
prisma.invoice.update(...),
]);
}

✅ Prisma contained
✅ DB structure hidden

3️⃣ Service layer (APP owns the flow)
// zatca.service.ts
export async function issueZatcaInvoice(invoiceId, requestId) {
const context = await getZatcaContext(prisma, invoiceId);

await enqueueZatcaJob({
invoiceId,
contextSnapshot: mapToZatcaPayload(context),
requestId,
});
}

Key change:

Worker receives a snapshot

No DB reads inside worker

4️⃣ Worker executor (PURE, no Prisma)
// zatca.executor.ts
export async function executeZatca(payload) {
const signed = await signXml(payload.xml, payload.seller);
const reported = await reportToZatca(signed);

return {
invoiceId: payload.invoiceId,
signedXml: signed.xml,
hash: signed.hash,
qrCode: reported.qr,
reportedAt: new Date(),
};
}

✔ No Prisma
✔ No DB
✔ No framework imports
✔ Easy to bundle
✔ Easy to retry
✔ Easy to test

5️⃣ Completion handler (APP persists results)
queueEvents.on("completed", async ({ returnvalue }) => {
await persistZatcaResult(prisma, returnvalue);
});

Same as PDF.

So why did ZATCA feel harder?

Because ZATCA mutates state, while PDF mostly produces artifacts.

But mutation ≠ worker responsibility.

Workers execute. Apps decide.

That’s the architectural rule.

When NOT to do this refactor

Keep Prisma in the worker if:

ZATCA retries must see live DB state

You rely on DB locks / row-level idempotency

You want infra to self-heal without app involvement

That’s a valid tradeoff — just be explicit about it.

Recommendation (based on your system maturity)

Given:

You already fixed PDF perfectly

You already have repositories

You already handle completion events

You care about bundle size & clarity

✅ I recommend Option B

Refactor ZATCA to match PDF’s ownership model

You’ll get:

Smaller workers

Cleaner mental model

One place that owns compliance state

Easier debugging & observability

Final takeaway

Yes, ZATCA can be structured exactly like PDF.
Reads/writes don’t block that — ownership does.
You’re not fighting the system — you’re aligning it.
