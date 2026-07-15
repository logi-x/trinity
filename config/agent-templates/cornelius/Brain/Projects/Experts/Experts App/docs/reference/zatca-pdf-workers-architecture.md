---
title: "ZATCA/PDF Workers System Architecture"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/zatca-pdf-workers-architecture"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# ZATCA/PDF Workers System Architecture

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture Principles](#architecture-principles)
3. [System Components](#system-components)
4. [Data Flow](#data-flow)
5. [Job Lifecycle](#job-lifecycle)
6. [File Structure](#file-structure)
7. [Configuration](#configuration)
8. [Key Concepts](#key-concepts)

---

## Overview

The ZATCA/PDF workers system is a **distributed background job processing system** built with BullMQ and Redis. It handles:

- **ZATCA Processing**: Invoice/credit note signing and reporting to Saudi Arabia's ZATCA e-invoicing system
- **PDF Generation**: Invoice PDF generation and storage (R2 or local)

### Key Characteristics

- **Separation of Concerns**: Workers are pure (no Prisma/DB), result handlers persist results
- **Framework-Free Workers**: Workers can run in isolated containers without Next.js dependencies
- **Data Snapshot Pattern**: All data needed for processing is included in job payload
- **Event-Driven**: Result handlers listen to queue events and persist results

---

## Architecture Principles

### 1. **Pure Workers (No Prisma/DB Access)**

Workers are **pure functions** that:

- ✅ Accept all data in job payload (no DB queries)
- ✅ Execute business logic (ZATCA signing, PDF generation)
- ✅ Return results (no side effects)
- ❌ **Never** access Prisma or database directly
- ❌ **Never** import Next.js framework code

**Why?** Workers run in isolated containers and can be scaled independently. Keeping them pure allows:

- Smaller Docker images
- Faster cold starts
- Better testability
- Framework-independent execution

### 2. **Result Handlers (Prisma Lives Here)**

Result handlers run in the **Next.js app container** and:

- ✅ Listen to queue completion events via `QueueEvents`
- ✅ Access Prisma and persist results to database
- ✅ Trigger downstream operations (e.g., enqueue PDF after ZATCA completes)
- ✅ Handle errors and observability

**Why?** Separation allows workers to be lightweight while ensuring database operations happen in the app layer with proper transaction handling.

### 3. **Data Snapshot Pattern**

All data needed for processing is **fetched before enqueueing** and included in the job payload:

```typescript
// ✅ CORRECT: Fetch data, then enqueue with context snapshot
const context = await getZatcaContext(prisma, zatcaDocumentId);
await enqueueZatcaJob({ kind: "EXECUTE_ZATCA", context });

// ❌ WRONG: Enqueue ID, worker fetches data
await zatcaQueue.add("EXECUTE_ZATCA", { zatcaDocumentId }); // Worker can't access DB!
```

---

## System Components

### 1. **Queues** (`src/queue/queues.ts`)

BullMQ queues for job management:

```typescript
export const zatcaQueue = new Queue("zatca", {
  connection: redis,
  defaultJobOptions: {
    removeOnComplete: { count: 5000 },
    removeOnFail: { count: 5000 },
  },
});

export const pdfQueue = new Queue("pdf", {
  connection: redis,
  defaultJobOptions: {
    removeOnComplete: { count: 1000 },
    removeOnFail: { count: 500 },
  },
});
```

### 2. **Workers** (`src/workers/`)

Pure worker processes that process jobs:

#### ZATCA Worker (`src/workers/zatca/zatca.worker.ts`)

- Processes ZATCA signing and reporting jobs
- Receives `ZatcaContext` snapshot in job payload
- Calls `executeZatca()` processor (pure function)
- Returns `ZatcaExecutionResult`

#### PDF Worker (`src/workers/pdf/pdf.worker.ts`)

- Processes PDF generation jobs
- Receives `InvoicePdfDTO` in job payload (full invoice data)
- Calls `generateInvoicePdf()` orchestrator (pure function)
- Returns storage metadata (key, size, checksum)

### 3. **Processors/Orchestrators** (`src/modules/billing/zatca/processors/`, `src/modules/billing/pdf/orchestrators/`)

Pure business logic functions (no Prisma, no DB):

- **ZATCA Processor**: `executeZatca(context)` - Signs and reports invoices
- **PDF Orchestrator**: `generateInvoicePdf(invoice, storage)` - Renders and stores PDFs

Related invoice assets live under `src/modules/billing/invoices/`:

- **Invoice renderers**: `src/modules/billing/invoices/renderers/invoice/*`
- **QR helpers**: `src/modules/billing/invoices/qr/*`
- **Invoice DTOs**: `src/modules/billing/invoices/dto/*`

### 4. **Result Handlers** (`src/modules/billing/zatca/handlers/`, `src/modules/billing/pdf/handlers/`)

Event listeners that persist results:

#### ZATCA Result Handler (`src/modules/billing/zatca/handlers/zatca-result.handler.ts`)

- Listens to `zatca` queue completion events
- Persists ZATCA results (signed XML, hash, QR code) via `persistZatcaResult()`
- Enqueues PDF generation job after successful ZATCA reporting (single orchestration source)

#### PDF Result Handler (`src/modules/billing/pdf/handlers/pdf-result.handler.ts`)

- Listens to `pdf` queue completion events
- Persists PDF file metadata via `upsertInvoicePdfFile()`

### 5. **Initialization** (`instrumentation.ts` + `workers-init.ts`)

Result handlers are initialized when the Next.js app starts:

```typescript
// instrumentation.ts (runs on Next.js server startup)
export async function register() {
  if (process.env.NEXT_RUNTIME === "nodejs") {
    const { initializeQueueCompletionHandlers } =
      await import("@/modules/billing/services/workers-init");
    initializeQueueCompletionHandlers(); // Sets up result handlers
  }
}
```

---

## Data Flow

### ZATCA Processing Flow

```
┌─────────────────┐
│  Next.js App    │
│  (API Route)    │
└────────┬────────┘
         │
         │ 1. Fetch context snapshot
         │    getZatcaContext(prisma, zatcaDocumentId)
         │
         ▼
┌─────────────────┐
│  Enqueue Job    │
│  zatcaQueue.add │
│  { context }    │
└────────┬────────┘
         │
         │ 2. Job stored in Redis
         │
         ▼
┌─────────────────┐
│  ZATCA Worker   │
│  (Container)    │
└────────┬────────┘
         │
         │ 3. Process job
         │    executeZatca(context)
         │    - Build unsigned XML
         │    - Sign XML
         │    - Report to ZATCA
         │
         │ 4. Return result
         │    ZatcaExecutionResult
         │
         ▼
┌─────────────────┐
│  QueueEvents    │
│  (Next.js App)  │
└────────┬────────┘
         │
         │ 5. Listen to "completed" event
         │
         ▼
┌─────────────────┐
│ Completion      │
│ Handler         │
└────────┬────────┘
         │
         │ 6. Persist results
         │    persistZatcaResult(prisma, result)
         │    - Save signed XML, hash, QR code
         │    - Save unsigned XML
         │
         │ 7. Enqueue PDF job (if invoice)
         │    enqueueInvoicePdfGenerationWithData(invoiceDTO)
         │
         ▼
┌─────────────────┐
│  PDF Queue      │
└─────────────────┘
```

### PDF Generation Flow

```
┌─────────────────┐
│  ZATCA Handler  │
│  (completion)  │
└────────┬────────┘
         │
         │ 1. Convert context invoice snapshot
         │    invoiceToPdfDTO(context.invoiceDataForPdf)
         │
         │ 2. Enqueue PDF job
         │    pdfQueue.add({ invoice: InvoicePdfDTO })
         │
         ▼
┌─────────────────┐
│  PDF Worker     │
│  (Container)    │
└────────┬────────┘
         │
         │ 3. Process job
         │    generateInvoicePdf(invoice, storage)
         │    - Render PDF (React PDF)
         │    - Upload to R2/local storage
         │
         │ 4. Return metadata
         │    { storageKey, size, checksum }
         │
         ▼
┌─────────────────┐
│  QueueEvents    │
│  (Next.js App)  │
└────────┬────────┘
         │
         │ 5. Listen to "completed" event
         │
         ▼
┌─────────────────┐
│ Completion      │
│ Handler         │
└────────┬────────┘
         │
         │ 6. Persist metadata
         │    upsertInvoicePdfFile(prisma, metadata)
         │    - Save storage key, size, checksum
         │
         ▼
┌─────────────────┐
│  Database       │
│  (Updated)      │
└─────────────────┘
```

---

## Job Lifecycle

### ZATCA Job Lifecycle

1. **Enqueue** (`enqueueInvoiceZatca()`)
   - Fetch context snapshot: `getZatcaContext(prisma, zatcaDocumentId)`
   - Include invoice data for PDF: `invoiceDataForPdf` (optional, for downstream PDF generation)
   - Add job to queue: `enqueueZatcaJob({kind: "EXECUTE_ZATCA", context, requestId})`

2. **Process** (ZATCA Worker)
   - Worker picks up job from Redis
   - Validates job data
   - Calls `executeZatca(context)` processor:
     - Builds unsigned XML (if needed)
     - Signs XML using ZATCA SDK
     - Reports to ZATCA API (if needed)
   - Returns `ZatcaExecutionResult`

3. **Complete** (Result Handler)
   - `QueueEvents` emits "completed" event
   - Handler receives result
   - Converts serialized Date strings back to Date objects
   - Persists to DB: `persistZatcaResult(prisma, result)`
   - If invoice reported successfully: enqueues PDF job

### PDF Job Lifecycle

1. **Enqueue** (`enqueueInvoicePdfGenerationWithData()`)
   - Receives `InvoicePdfDTO` (full invoice data)
   - Checks for existing job (deduplication)
   - Adds job to queue: `pdfQueue.add("generate-invoice-pdf", { invoice, requestId })`

2. **Process** (PDF Worker)
   - Worker picks up job from Redis
   - Validates job has invoice data
   - Calls `generateInvoicePdf(invoice, storage)` orchestrator:
     - Renders PDF using React PDF
     - Uploads to storage (R2 or local)
   - Returns storage metadata

3. **Complete** (Result Handler)
   - `QueueEvents` emits "completed" event
   - Handler receives metadata
   - Persists to DB: `upsertInvoicePdfFile(prisma, metadata)`

---

## File Structure

```
apps/experts-app/
├── src/
│   ├── workers/                          # Worker processes
│   │   ├── zatca/
│   │   │   ├── zatca.worker.ts          # ZATCA worker entry point
│   │   │   └── start-zatca-worker.ts    # Worker startup script
│   │   ├── pdf/
│   │   │   ├── pdf.worker.ts            # PDF worker entry point
│   │   │   └── start-pdf-worker.ts      # Worker startup script
│   │   ├── tsup.config.ts               # Worker build config
│   │   └── tsconfig.workers.json        # Worker TS config
│   │
│   ├── queue/                            # Queue configuration
│   │   ├── queues.ts                    # Queue instances (BullMQ)
│   │   └── redis.ts                     # Redis connection
│   │
│   ├── modules/billing/
│   │   ├── zatca/
│   │   │   ├── processors/
│   │   │   │   └── zatca.processor.ts    # Pure ZATCA processor (no Prisma)
│   │   │   ├── queries/
│   │   │   │   └── zatca.payload.ts      # XML payload queries
│   │   │   ├── repositories/
│   │   │   │   └── zatca.repository.ts  # DB operations (Prisma)
│   │   │   ├── queue/
│   │   │   │   └── zatca.jobs.ts         # ZATCA job types + enqueue wrapper
│   │   │   ├── handlers/
│   │   │   │   └── zatca-result.handler.ts  # Result handler
│   │   │   ├── services/
│   │   │   │   └── zatca-queue.service.ts  # Enqueue functions
│   │   │   ├── sign/                    # XML signing logic
│   │   │   ├── report/                  # ZATCA reporting logic
│   │   │   ├── xml/                     # XML building logic
│   │   │   └── types.ts                 # ZATCA types
│   │   │
│   │   ├── pdf/
│   │   │   ├── orchestrators/
│   │   │   │   └── pdf.orchestrator.ts  # Pure PDF orchestrator (no Prisma)
│   │   │   ├── queue/
│   │   │   │   └── pdf.jobs.ts          # PDF job types
│   │   │   ├── handlers/
│   │   │   │   └── pdf-result.handler.ts  # PDF result handler
│   │   │   └── storage/                 # Storage logic
│   │   │
│   │   ├── invoices/
│   │   │   ├── dto/
│   │   │   │   └── invoice-pdf.dto.ts   # Invoice PDF DTOs
│   │   │   ├── qr/                      # QR helpers
│   │   │   ├── renderers/
│   │   │   │   └── invoice/             # PDF/HTML invoice rendering assets
│   │   │   ├── repositories/
│   │   │   │   └── invoice.repository.ts  # Invoice DB operations
│   │   │   └── services/
│   │   │       └── invoice-issuance.service.ts  # PDF enqueue helpers
│   │   │
│   │   └── services/
│   │       └── workers-init.ts          # Initialize result handlers
│   │
│   └── lib/
│       ├── observability/
│       │   ├── worker-observe.ts        # Worker-safe observability
│       │   └── index.ts                 # App observability
│       └── prisma.ts                    # Prisma client (app only)
│
├── instrumentation.ts                    # Next.js instrumentation hook
└── extra/docs/
    └── ZATCA_PDF_WORKERS_ARCHITECTURE.md  # This file
```

---

## Configuration

### Environment Variables

#### Workers (Container Environment)

```bash
# Redis
REDIS_URL=redis://:password@redis-host:6379
REDIS_HOST=redis-host
REDIS_PORT=6379
REDIS_PASSWORD=password

# Database (for context fetching - workers don't use it)
DATABASE_URL=postgresql://...

# ZATCA Worker
ZATCA_WORKER_CONCURRENCY=2              # Concurrent jobs
FATOORA_HOME=/opt/zatca-sdk/Apps        # ZATCA SDK path
SDK_CONFIG=/opt/zatca-sdk/Configuration/config.json
JAVA_HOME=/opt/java/openjdk

# PDF Worker
PDF_WORKER_CONCURRENCY=2                # Concurrent jobs
R2_INVOICES_FORCE=true                  # Use R2 storage (set in staging/prod)
R2_ENDPOINT=https://...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_INVOICES=invoices
```

#### Next.js App (Result Handlers)

```bash
# Redis (same as workers - shared queue)
REDIS_URL=redis://:password@redis-host:6379

# Database (for persistence)
DATABASE_URL=postgresql://...
```

### Docker Compose Configuration

```yaml
services:
  # ZATCA Worker
  zatca-worker:
    image: loogix/experts:staging-worker
    command: ["node", "dist/zatca/start-zatca-worker.mjs"]
    environment:
      - ZATCA_WORKER_CONCURRENCY=2
      - REDIS_URL=redis://...
      - DATABASE_URL=postgresql://...
    networks:
      - experts-shared-network

  # PDF Worker
  pdf-worker:
    image: loogix/experts:staging-worker
    command: ["node", "dist/pdf/start-pdf-worker.mjs"]
    environment:
      - PDF_WORKER_CONCURRENCY=2
      - R2_INVOICES_FORCE=true
      - REDIS_URL=redis://...
      - R2_ENDPOINT=...
      - R2_ACCESS_KEY_ID=...
      - R2_SECRET_ACCESS_KEY=...
    networks:
      - experts-shared-network

  # Next.js App (runs result handlers)
  experts-app:
    image: loogix/experts:staging
    environment:
      - REDIS_URL=redis://...
      - DATABASE_URL=postgresql://...
    # Result handlers initialized via instrumentation.ts
```

---

## Key Concepts

### 1. **Context Snapshot Pattern**

All data needed for processing is fetched **before enqueueing** and included in the job payload:

```typescript
// ZATCA Context includes everything needed
type ZatcaContext = {
  zatcaDocumentId: string;
  type: "invoice" | "credit_note";
  status: string;
  xmlPayload: ZatcaInvoiceXmlPayload | ZatcaCreditNoteXmlPayload;
  zatcaConfig: ResolvedZatcaConfig;
  invoiceDataForPdf?: InvoiceDataForPdf; // For downstream PDF generation
  // ... other fields
};
```

### 2. **Pure Processors/Orchestrators**

Business logic functions that are **framework-free**:

```typescript
// ✅ Pure processor - no Prisma, no DB
export async function executeZatca(
  context: ZatcaContext,
  requestId?: string
): Promise<ZatcaExecutionResult> {
  // Build XML, sign, report - all pure operations
  // Returns result - caller persists it
}

// ❌ Wrong - accessing Prisma in processor
export async function executeZatca(zatcaDocumentId: string) {
  const doc = await prisma.zatcaDocument.findUnique(...); // NO!
}
```

### 3. **Result Handler Pattern**

Event-driven persistence that runs in the **Next.js app**:

```typescript
// Setup handler (runs in Next.js app via instrumentation.ts)
export function setupZatcaResultHandler() {
  const queueEvents = new QueueEvents("zatca", { connection: redis });

  queueEvents.on("completed", async ({ jobId, returnvalue }) => {
    const result = returnvalue as ZatcaExecutionResult;
    await persistZatcaResult(prisma, result); // Prisma lives here
  });
}
```

### 4. **Job Deduplication**

PDF jobs use deterministic job IDs to prevent duplicates:

```typescript
const jobId = `pdf_invoice_${invoice.id}`;
const existingJob = await pdfQueue.getJob(jobId);
if ((existingJob && (await existingJob.getState()) === "active") || "waiting") {
  return existingJob; // Return existing job, don't create duplicate
}
```

### 5. **Chained Jobs (ZATCA → PDF)**

ZATCA result handler enqueues PDF job after successful reporting:

```typescript
// In ZATCA result handler
if (result.status === "reported" && result.type === "invoice") {
  const invoiceDTO = invoiceToPdfDTO(jobData.context.invoiceDataForPdf);
  await enqueueInvoicePdfGenerationWithData(invoiceDTO, requestId);
}
```

---

## Best Practices

### ✅ DO

- ✅ **Fetch all data before enqueueing** - Include context snapshot in job payload
- ✅ **Keep workers pure** - No Prisma, no DB access, no framework dependencies
- ✅ **Use result handlers for persistence** - Prisma operations in Next.js app
- ✅ **Include invoice data for PDF jobs** - Workers can't fetch from DB
- ✅ **Handle errors gracefully** - Use try-catch and observability
- ✅ **Convert serialized dates** - BullMQ serializes Date objects to strings

### ❌ DON'T

- ❌ **Don't enqueue IDs** - Workers can't fetch data from database
- ❌ **Don't use Prisma in workers** - Workers are framework-free
- ❌ **Don't access DB in processors/orchestrators** - They're pure functions
- ❌ **Don't skip context snapshot** - All data must be in job payload
- ❌ **Don't forget result handlers** - Results won't be persisted

---

## Troubleshooting

### Workers not processing jobs

1. **Check Redis connection** - Workers and app must connect to same Redis
2. **Check worker logs** - Look for connection errors
3. **Verify queues exist** - Check Redis for queue keys
4. **Check worker startup** - Ensure workers are running and listening

### Result handlers not running

1. **Check instrumentation.ts** - Must be called on server startup
2. **Check Redis connection** - Handlers need Redis for QueueEvents
3. **Check logs** - Look for initialization errors
4. **Verify Next.js app is running** - Handlers run in app container, not workers

### Jobs stuck in queue

1. **Check worker status** - Are workers running?
2. **Check worker logs** - Look for processing errors
3. **Check Redis connection** - Workers must connect to Redis
4. **Check job data** - Validate job payload structure

### PDF not being generated after ZATCA

1. **Check ZATCA result handler logs** - Look for PDF enqueue errors
2. **Verify invoiceDataForPdf** - Must be included in ZATCA context
3. **Check PDF queue** - Verify jobs are being added
4. **Check PDF worker logs** - Look for processing errors

---

## Related Documentation

