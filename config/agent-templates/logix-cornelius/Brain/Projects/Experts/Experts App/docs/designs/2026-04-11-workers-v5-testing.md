---
title: "WORKERS V5 TESTING"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/workers-v5-testing"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# WORKERS V5 TESTING

The 4 test layers you should have (and nothing more)

You do NOT need to test everything everywhere. Each layer has a specific contract.

1️⃣ Pure Processor Tests (MOST IMPORTANT)
What this tests

Business correctness, zero infrastructure.

Scope

zatca.processor.ts
(and similar for PDF processor)

Input

ZatcaContext snapshot

optional requestId

Output

ZatcaExecutionResult

What to test ✅
Happy paths

Signs invoice when status = pending_sign

Reports invoice when status = pending_report

Handles already-signed documents correctly

Handles already-reported documents correctly

Edge cases

Invalid invoice totals

Missing seller profile

Invalid VAT number

Network error from ZATCA API (mocked)

Idempotency (same input → same output)

What NOT to test ❌

Prisma

Redis

Queues

Database state

Example
describe("executeZatca", () => {
it("signs and reports an invoice", async () => {
const context = createZatcaContext({ status: "pending_sign" });

    const result = await executeZatca(context, "req-1");

    expect(result.status).toBe("reported");
    expect(result.signedXml).toBeDefined();
    expect(result.qrCode).toBeDefined();

});
});

👉 If these tests pass, your core logic is correct forever.

2️⃣ Repository Tests (Prisma correctness)
What this tests

Database correctness, nothing else.

Scope

zatca.repository.ts

Uses

Test database (real Prisma)

prisma migrate deploy before tests

What to test ✅

ensureZatcaDocument

creates when missing

returns existing one when present

getZatcaContext

returns full snapshot

returns null when already reported

persistZatcaResult

updates document status

stores signed XML / hash / QR

updates invoice or credit note fields

What NOT to test ❌

ZATCA APIs

Worker execution

Queue behavior

Example
it("fetches ZATCA context snapshot", async () => {
const ctx = await getZatcaContext(prisma, zatcaDocumentId);

expect(ctx.invoice.id).toBeDefined();
expect(ctx.seller.vatNumber).toBeDefined();
});

👉 This ensures schema changes won’t silently break execution.

3️⃣ Queue Service Tests (Boundary tests)
What this tests

Correct data is enqueued, not execution.

Scope

zatca-queue.service.ts

Mock

Prisma (or use test DB)

Queue enqueue function

What to test ✅

enqueueInvoiceZatca

fetches context

enqueues EXECUTE_ZATCA job

payload contains snapshot, not IDs

Correct job name

Correct dedupe / requestId behavior

Example
it("enqueues EXECUTE_ZATCA job with context snapshot", async () => {
await enqueueInvoiceZatca(invoiceId, "req-123");

expect(queue.add).toHaveBeenCalledWith(
"EXECUTE_ZATCA",
expect.objectContaining({
context: expect.any(Object),
})
);
});

👉 This prevents accidental regression back to “ID-based jobs”.

4️⃣ End-to-End Flow Test (ONE only)
What this tests

The full happy path, once.

Scope

Test DB

Real queue (or fake in-memory queue)

Real worker executor

Result handler enabled

What to test ✅

Invoice created

ZATCA job enqueued

Worker executes

Result handler persists result

Invoice status updated

PDF job optionally enqueued

What NOT to test ❌

All edge cases

All failure modes

You only need one or two E2E tests.

Example assertion
expect(invoice.zatcaStatus).toBe("reported");
expect(zatcaDocument.hash).toBeDefined();

🧪 What NOT to test (very important)

Do NOT:

test Prisma inside worker tests

test executor + repository together

test Redis internals

test BullMQ internals

snapshot-test huge payloads

Those create brittle, slow tests.

🧠 How this scales to PDF

PDF follows the same exact matrix:

Layer PDF Equivalent
Executor renderInvoicePdf()
Repository invoice.repository.ts
Queue service enqueueInvoicePdfGenerationWithData()
Result handler pdf-result.handler.ts
Worker no tests needed (executor already tested)
🧩 Final mental checklist

When asking “Should I test this?”, ask:

❓ Does this layer own logic or just delegate?

Owns logic → test it

Delegates → mock it

Coordinates → test once

Summary (print this)

✅ Executor tests → most important

✅ Repository tests → schema safety

✅ Queue service tests → contract safety

✅ 1 E2E test → confidence

❌ No DB tests in workers

❌ No Prisma in executor tests
