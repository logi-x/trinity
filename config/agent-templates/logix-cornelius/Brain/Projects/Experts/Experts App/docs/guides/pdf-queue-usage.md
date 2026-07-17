---
title: "PDF Queue Usage Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/pdf-queue-usage"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# PDF Queue Usage Guide

This guide explains how to use the queue-based PDF generation system.

## Overview

The PDF generation system supports two modes:

1. **Synchronous** (default) - Generates PDF immediately in the API route
2. **Queue-based** - Enqueues job for background processing

## Queue-Based Generation

### Enqueue a PDF Generation Job

```typescript
import { enqueueInvoicePdfGeneration } from "@/queue/pdf.jobs";

// Enqueue PDF generation
const job = await enqueueInvoicePdfGeneration("invoice-id-123");

console.log("Job ID:", job.id);
console.log("Job status:", await job.getState());
```

### Using the API Route with Queue Mode

```bash
# Add ?queue=true parameter
curl http://localhost:3025/api/invoices/[invoice-id]/pdf?queue=true

# Or set environment variable
PDF_USE_QUEUE=true curl http://localhost:3025/api/invoices/[invoice-id]/pdf
```

**Response (202 Accepted):**

```json
{
  "message": "PDF generation queued",
  "jobId": "pdf:invoice:invoice-id-123",
  "invoiceId": "invoice-id-123",
  "invoiceNumber": "INV-001",
  "status": "queued"
}
```

### Starting the Worker

```bash
# Start PDF worker
pnpm worker:pdf

# Or directly
tsx src/workers/start-pdf-worker.ts
```

The worker will:

- Process jobs from the `pdf` queue
- Generate PDFs and save them to `storage/invoices/[invoice-number].pdf`
- Handle retries on failure (3 attempts with exponential backoff)
- Log all job events

### Worker Configuration

Environment variables:

- `PDF_WORKER_CONCURRENCY` - Number of concurrent jobs (default: 2)
- `REDIS_URL` - Redis connection URL (required)

### Checking Job Status

```typescript
import { pdfQueue } from "@/queue/queues";

const job = await pdfQueue.getJob("pdf:invoice:invoice-id-123");

if (job) {
  const state = await job.getState();
  const progress = job.progress;
  const returnValue = job.returnvalue;

  console.log("State:", state); // "completed", "failed", "active", etc.
  console.log("Progress:", progress);
  console.log("Result:", returnValue);
}
```

### Example: Complete Flow

```typescript
import { enqueueInvoicePdfGeneration } from "@/queue/pdf.jobs";
import { pdfQueue } from "@/queue/queues";

// 1. Enqueue the job
const job = await enqueueInvoicePdfGeneration("invoice-id-123");

// 2. Wait for completion (optional)
await job.waitUntilFinished(pdfQueue);

// 3. Check result
const state = await job.getState();
if (state === "completed") {
  console.log("PDF generated successfully!");
  // PDF is saved to: storage/invoices/[invoice-number].pdf
} else if (state === "failed") {
  console.error("PDF generation failed:", job.failedReason);
}
```

## When to Use Queue Mode

**Use queue mode when:**

- ✅ PDF generation is slow and you want to return immediately
- ✅ You need to process many PDFs in batch
- ✅ You want to retry failed generations automatically
- ✅ You want to scale PDF generation independently

**Use synchronous mode when:**

- ✅ You need the PDF immediately
- ✅ Low traffic (no performance concerns)
- ✅ Simple use case (no retry logic needed)

## File Locations

- **Generated PDFs**: `storage/invoices/[invoice-number].pdf`
- **Queue jobs**: Stored in Redis
- **Worker logs**: Check application logs for `pdf-worker` service

## Monitoring

Check worker status:

```typescript
import { pdfQueue } from "@/queue/queues";

// Get queue stats
const waiting = await pdfQueue.getWaitingCount();
const active = await pdfQueue.getActiveCount();
const completed = await pdfQueue.getCompletedCount();
const failed = await pdfQueue.getFailedCount();

console.log({
  waiting,
  active,
  completed,
  failed,
});
```

## Troubleshooting

### Worker not processing jobs

1. Check if worker is running: `pnpm worker:pdf`
2. Check Redis connection: Ensure `REDIS_URL` is set
3. Check logs for errors

### PDF not generated

1. Check job status: `await job.getState()`
2. Check job logs: `await job.logs()`
3. Check worker logs for errors

### Jobs stuck in queue

1. Check worker is running
2. Check Redis is accessible
3. Restart worker if needed
