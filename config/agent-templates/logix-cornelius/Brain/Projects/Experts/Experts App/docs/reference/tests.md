---
title: "Tests"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/tests"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Tests

```sh

✓ src/modules/billing/zatca/services/__tests__/zatca-core.e2e.test.ts (3 tests) 9858ms
   ✓ zatca-core-e2e (integration) (3)
     ✓ signs and produces a signed XML (and validates via simulator when enabled)  4091ms
     ✓ is idempotent when run multiple times  3854ms
     ✓ moves to report_failed on failure  1911ms
 ✓ src/modules/billing/zatca/repositories/__tests__/zatca.repository.integration.test.ts (3 tests) 142ms
   ✓ zatca-repository (integration) (3)
     ✓ creates ZATCA document when missing 43ms
     ✓ returns context snapshot for pending document 55ms
     ✓ persists signing results to document and invoice 44ms
 ✓ src/modules/billing/pdf/handlers/__tests__/pdf-result.handler.test.ts (3 tests) 10ms
   ✓ pdf-result-handler (integration) (3)
     ✓ persists PDF metadata and emits completion event 6ms
     ✓ emits storage + domain events on completion 2ms
     ✓ emits failure event with job context when available 2ms
 ✓ src/modules/billing/zatca/repositories/__tests__/zatca.repository.test.ts (8 tests) 2ms
   ✓ zatca-repository (unit) (8)
     ✓ returns null when document is missing 1ms
     ✓ returns null when document already reported 0ms
     ✓ builds context for pending_report invoice 0ms
     ✓ throws when business entity is missing 0ms
     ✓ throws when no seller profile is active 0ms
     ✓ updates invoice when signing completed 0ms
     ✓ updates credit note when reporting completed 0ms
     ✓ creates invoice document when missing 0ms
 ✓ src/modules/billing/zatca/handlers/__tests__/zatca-result.handler.test.ts (2 tests) 6ms
   ✓ zatca-result-handler (integration) (2)
     ✓ persists results, enqueues PDF, and records domain events 4ms
     ✓ handles completed event using job payload 2ms
 ✓ src/modules/billing/zatca/services/__tests__/zatca-queue.service.test.ts (6 tests) 3ms
   ✓ zatca-queue-service (unit) (6)
     ✓ enqueueInvoiceZatca (3)
       ✓ fetches context and enqueues EXECUTE_ZATCA job 1ms
       ✓ skips enqueueing when context is null (already reported) 0ms
       ✓ handles errors gracefully 0ms
     ✓ enqueueCreditNoteZatca (1)
       ✓ fetches context and enqueues EXECUTE_ZATCA job 1ms
     ✓ enqueueZatcaDocument (2)
       ✓ fetches context and enqueues EXECUTE_ZATCA job 1ms
       ✓ skips enqueueing when context is null 0ms
 ✓ app/api/v1/commerce/invoices/[id]/pdf/__tests__/route.test.ts (7 tests) 7ms
   ✓ GET /api/v1/commerce/invoices/[id]/pdf (integration) (7)
     ✓ redirects to HTML preview in development (sync mode) 2ms
     ✓ returns 401 if not authenticated 2ms
     ✓ returns 404 if invoice not found 1ms
     ✓ returns 403 if user doesn\'t own invoice 0ms
     ✓ enqueues PDF generation when queue mode is enabled 1ms
     ✓ generates PDF synchronously in production 1ms
     ✓ allows admin to access any invoice 0ms
 ✓ src/modules/billing/pdf/queue/__tests__/pdf.jobs.test.ts (4 tests) 2ms
   ✓ pdf-jobs (unit) (4)
     ✓ enqueues a PDF job with deterministic jobId 1ms
     ✓ returns existing job when job is active 1ms
     ✓ returns existing job when job is waiting 0ms
     ✓ enqueues new job when existing job is completed 0ms
 ✓ src/modules/billing/zatca/xml/__tests__/build-credit-note-xml.test.ts (1 test) 4ms
   ✓ build-credit-note-xml (unit) (1)
     ✓ matches the golden credit note XML snapshot 4ms
 ✓ src/modules/billing/zatca/processors/__tests__/zatca.processor.test.ts (9 tests) 3ms
   ✓ zatca-processor (integration) (9)
     ✓ Happy paths (4)
       ✓ signs invoice when status = pending_sign 1ms
       ✓ reports already-signed invoice when status = pending_report (simulator) 0ms
       ✓ signs and reports invoice in one go (simulator) 1ms
       ✓ signs credit note when status = pending_sign 0ms
     ✓ Edge cases (5)
       ✓ handles sign failure gracefully 0ms
       ✓ handles report failure gracefully 0ms
       ✓ handles invalid validation result (simulator) 0ms
       ✓ reports to ZATCA API (sandbox/production) 0ms
       ✓ is idempotent - same input produces same output 0ms
 ✓ src/modules/billing/pdf/orchestrators/__tests__/pdf.orchestrator.test.ts (7 tests) 3ms
   ✓ pdf-orchestrator (integration) (7)
     ✓ Happy paths (3)
       ✓ generates and stores invoice PDF (local storage) 1ms
       ✓ generates and stores invoice PDF (R2 storage) 0ms
       ✓ determines correct storage key based on environment 0ms
     ✓ Edge cases (3)
       ✓ handles render failure gracefully 0ms
       ✓ handles storage failure gracefully 0ms
       ✓ handles invoice without full data gracefully 0ms
     ✓ Idempotency (1)
       ✓ produces same storage key for same invoice 0ms
 ✓ src/modules/billing/zatca/queue/__tests__/zatca.jobs.test.ts (2 tests) 1ms
   ✓ zatca-jobs (unit) (2)
     ✓ enqueues ZATCA job with deterministic jobId 1ms
     ✓ uses jobId derived from zatcaDocumentId 0ms
 ✓ src/modules/billing/zatca/xml/__tests__/build-invoice-xml.test.ts (1 test) 2ms
   ✓ build-invoice-xml (unit) (1)
     ✓ matches the golden invoice XML snapshot 1ms
 ✓ src/modules/billing/zatca/__tests__/zatca.config.test.ts (4 tests) 1ms
   ✓ zatca-config (unit) (4)
     ✓ resolves simulator endpoint 0ms
     ✓ resolves sandbox endpoint + uses passed authorization key 0ms
     ✓ resolves production endpoint 0ms
     ✓ throws a clear error when endpoint is missing/invalid 0ms
 ✓ src/modules/billing/invoices/renderers/invoice/__tests__/map-invoice-to-view-model.test.ts (8 tests) 2ms
   ✓ map-invoice-to-view-model (unit) (8)
     ✓ maps invoice to view model 1ms
     ✓ formats seller address correctly 0ms
     ✓ formats buyer address correctly 0ms
     ✓ handles missing business entity 0ms
     ✓ handles missing branding 0ms
     ✓ uses ZATCA QR code if available 0ms
     ✓ calculates totals correctly 0ms
     ✓ maps invoice lines correctly 0ms


 ✓ src/lib/courses/enrollments/handlers/__tests__/course-enroll.integration.test.ts (1 test) 6174ms
   ✓ course-enroll-handler (integration) (1)
     ✓ creates an enrollment in the database  6173ms
 ✓ src/lib/courses/enrollments/handlers/__tests__/course-enrollment-complete.handler.test.ts (3 tests) 3ms
   ✓ course-enrollment-complete-handler (integration) (3)
     ✓ completes enrollment when payment is valid 2ms
     ✓ does not complete enrollment when payment is invalid 0ms
     ✓ does not complete enrollment when invoice is not found 0ms
 ✓ src/lib/courses/enrollments/handlers/__tests__/course-enrollment-refund-request.handler.test.ts (11 tests) 3ms
   ✓ course-enrollment-refund-request-handler (integration) (11)
     ✓ returns 404 when enrollment is missing 0ms
     ✓ rejects free courses 0ms
     ✓ rejects when progress exceeds limit 0ms
     ✓ rejects when a request already exists 0ms
     ✓ rejects when enrollment is already refunded 0ms
     ✓ rejects when refund window has expired 0ms
     ✓ rejects when enrollment does not belong to user 0ms
     ✓ rejects when a certificate exists 0ms
     ✓ rejects when course is archived 0ms
     ✓ returns duplicate error on concurrent request create 0ms
     ✓ creates a refund request when eligible (happy path) 1ms
 ✓ src/lib/courses/enrollments/handlers/__tests__/course-enrollment-refund-admin.handlers.test.ts (9 tests) 2ms
   ✓ course-enrollment-refund-admin-handlers (integration) (9)
     ✓ rejects approval when user is not admin 0ms
     ✓ rejects refund processing when user is not admin 0ms
     ✓ rejects refund rejection when user is not admin 0ms
     ✓ rejects approval when request is not pending 0ms
     ✓ rejects a pending refund request 0ms
     ✓ rejects processing when invoice is missing 0ms
     ✓ auto-rejects stale refund requests 0ms
     ✓ processes an approved refund request and creates a credit note (happy path) 0ms
     ✓ approves a pending refund request (happy path) 0ms
 ✓ src/lib/courses/enrollments/commands/__tests__/course-enrollment-complete.schema.test.ts (2 tests) 1ms
   ✓ course-enrollment-complete-schema (unit) (2)
     ✓ accepts valid input 0ms
     ✓ rejects missing payment 0ms
 ✓ src/lib/courses/curriculum/handlers/__tests__/course-module.handlers.test.ts (8 tests) 2ms
   ✓ course-module-handlers (integration) (8)
     ✓ lists modules for a course 0ms
     ✓ creates a module with next position 0ms
     ✓ returns 404 when module detail is missing 0ms
     ✓ returns module detail when found 0ms
     ✓ updates a module when found 0ms
     ✓ returns 404 when updating a missing module 0ms
     ✓ deletes a module when found 0ms
     ✓ returns 404 when deleting a missing module 0ms
 ✓ src/lib/courses/enrollments/handlers/__tests__/course-enroll.handler.test.ts (5 tests) 1ms
   ✓ course-enroll-handler (integration) (5)
     ✓ throws when user is invalid 0ms
     ✓ returns 404 when course is missing 0ms
     ✓ blocks already completed enrollment 0ms
     ✓ completes free course enrollment 0ms
     ✓ creates payment intent for paid course 0ms
 ✓ src/lib/courses/curriculum/handlers/__tests__/course-lesson.handlers.test.ts (9 tests) 2ms
   ✓ course-lesson-handlers (integration) (9)
     ✓ returns 404 when listing lessons for missing module 0ms
     ✓ lists lessons for a module 0ms
     ✓ creates a lesson with next position 0ms
     ✓ returns 404 when lesson detail is missing 0ms
     ✓ returns lesson detail when found 0ms
     ✓ updates a lesson when found 0ms
     ✓ returns 404 when updating a missing lesson 0ms
     ✓ deletes a lesson when found 0ms
     ✓ returns 404 when deleting a missing lesson 0ms
 ✓ src/lib/courses/enrollments/commands/__tests__/course-enroll.schema.test.ts (4 tests) 1ms
   ✓ course-enroll-schema (unit) (4)
     ✓ accepts valid input 1ms
     ✓ rejects missing course 0ms
     ✓ rejects missing courseId 0ms
     ✓ rejects missing userId 0ms
 ✓ src/modules/billing/invoices/services/__tests__/invoice-issuance.service.test.ts (4 tests) 1ms
   ✓ invoice-issuance-service (unit) (4)
     ✓ enqueueInvoicePdfGenerationWithData (4)
       ✓ enqueues GENERATE_INVOICE_PDF job with invoice data 0ms
       ✓ returns existing job if already in queue 0ms
       ✓ enqueues new job if existing job is completed 0ms
       ✓ uses correct storage key pattern in job data 0ms
 ✓ src/lib/courses/enrollments/handlers/__tests__/course-enrollment-status.handler.test.ts (4 tests) 1ms
   ✓ course-enrollment-status-handler (integration) (4)
     ✓ returns not enrolled when no enrollment exists 0ms
     ✓ returns completed enrollment status 0ms
     ✓ returns pending enrollment status 0ms
     ✓ returns cancelled/refunded flags 0ms
 ✓ src/lib/courses/enrollments/handlers/__tests__/course-enrollment-cancel.handler.test.ts (3 tests) 0ms
   ✓ course-enrollment-cancel-handler (integration) (3)
     ✓ returns updated false when enrollment is missing 0ms
     ✓ skips update when enrollment already cancelled 0ms
     ✓ cancels a pending enrollment 0ms

 Test Files  11 passed (11)
      Tests  59 passed (59)
   Start at  01:42:34
   Duration  9.76s (transform 1.87s, setup 510ms, import 2.08s, tests 6.22s, environment 1ms)

 Test Files  27 passed (27)
      Tests  131 passed (131)
   Start at  01:11:17
   Duration  16.62s

 PASS  Waiting for file changes...
       press h to show help, press q to quit

```
