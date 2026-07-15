---
title: "Prisma References Analysis"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/prisma-references"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Prisma References Analysis

## Where Prisma is NEEDED (✅ Correct)

### 1. Repository Layer (✅ Prisma belongs here)

**Location**: `src/modules/billing/invoices/repositories/invoice.repository.ts`

```typescript
// ✅ CORRECT: Repository layer owns Prisma
import type {PrismaClient} from "@/generated/prisma/client";
import {invoicePdfInclude, type InvoicePdfRecord} from "@/lib/billing/includes/invoice-pdf.include";

export async function getInvoiceForPdf(
  prisma: PrismaClient,
  invoiceId: string
): Promise<InvoicePdfRecord> {
  return prisma.invoice.findUnique({
    where: {id: invoiceId},
    include: invoicePdfInclude,
  });
}

export async function upsertInvoicePdfFile(
  prisma: PrismaClient,
  data: {...}
) {
  return prisma.invoiceFile.upsert({...});
}
```

**Purpose**:

- Encapsulates all Prisma operations
- Only place that knows about DB structure
- Called from Service/Orchestration layer

---

### 2. Service/Orchestration Layer (✅ Prisma belongs here)

**Location**: `src/modules/billing/services/invoice-issuance.service.ts`

```typescript
// ✅ CORRECT: Service layer orchestrates, uses repositories
import { prisma } from "@/lib/prisma";
import { getInvoiceForPdf } from "../invoices/repositories/invoice.repository";

export async function issueInvoice(invoiceId: string, requestId?: string) {
  // 1. ZATCA first
  await enqueueInvoiceZatca(invoiceId, requestId);

  // 2. Fetch invoice data using repository
  const invoice = await getInvoiceForPdf(prisma, invoiceId);

  // 3. Enqueue PDF job WITH DATA (not ID)
  await enqueueInvoicePdfGenerationWithData(
    invoiceToPdfDTO(invoice),
    requestId,
  );
}
```

**Purpose**:

- Orchestrates business logic flow
- Calls repositories to fetch/persist data
- Enqueues jobs with data (not IDs)
- Owns what data to fetch and when

---

### 3. ZATCA Service Layer (✅ Prisma belongs here)

**Location**: `src/modules/billing/zatca/zatca.service.ts`

```typescript
// ✅ CORRECT: Service layer uses Prisma for ZATCA operations
import type {PrismaClient} from "@/generated/prisma/client";

export async function processInvoiceZatca(
  prisma: PrismaClient,
  invoiceId: string,
  requestId?: string,
) {
  const invoice = await prisma.invoice.findUnique({...});
  const doc = await prisma.zatcaDocument.upsert({...});
  // ... ZATCA processing logic
}
```

**Purpose**:

- Handles ZATCA business logic
- Uses Prisma to read/write ZATCA documents
- Called from Adapter layer (which provides Prisma)

---

### 4. PDF Completion Handler (✅ Prisma belongs here)

**Location**: `src/modules/billing/services/pdf-result.handler.ts`

```typescript
// ✅ CORRECT: Result handler persists PDF metadata
import {prisma} from "@/lib/prisma";
import {upsertInvoicePdfFile} from "../invoices/repositories/invoice.repository";

export function setupPdfResultHandler() {
  // Listens to job completion events
  queueEvents.on("completed", async ({jobId, returnvalue}) => {
    // Persist PDF metadata using repository
    await upsertInvoicePdfFile(prisma, {...});
  });
}
```

**Purpose**:

- Runs in Next.js app (not in worker)
- Listens to worker completion events
- Persists PDF metadata using Prisma

---

### 5. Application Adapter Layer (✅ Prisma belongs here, but must be externalized)

**Location**: `src/adapters/zatca.adapter.ts`

```typescript
// ✅ CORRECT: Adapter bridges worker and application
// ⚠️ Uses dynamic imports to avoid bundling Prisma
export async function processZatcaWithInfra(job: ZatcaJobInput) {
  // Dynamic import to avoid bundling Prisma
  const {prisma} = await import("@/lib/prisma");
  const {processInvoiceZatca, ...} = await import("@/modules/billing/zatca/zatca.service");

  return processZatcaJob({
    async processInvoiceZatca(invoiceId: string, requestId?: string) {
      return processInvoiceZatca(prisma, invoiceId, requestId);
    },
    // ...
  }, job);
}
```

**Purpose**:

- Bridges worker (framework-free) with application (has Prisma)
- Uses dynamic imports to avoid bundling Prisma
- Should be externalized in tsup config

---

## Where Prisma is LEAKING (❌ Wrong - Should be fixed)

### 1. Worker Bundle (❌ Prisma should NOT be here)

**Location**: `dist/zatca/start-zatca-worker.mjs`

**Current Issue**:

```javascript
// ❌ WRONG: Prisma runtime bundled in worker
import * as runtime2 from "@prisma/client/runtime/client";
import { PrismaPg } from "@prisma/adapter-pg";
import "@/lib/prisma";
```

**Why it's wrong**:

- Workers should be framework-free
- Prisma runtime adds ~100KB+ to bundle
- Worker should only execute, not access DB

**Solution**:

- ✅ Already using dynamic imports in adapter
- ✅ Already externalized `@/lib/prisma` in tsup config
- ⚠️ Still bundling Prisma runtime - need to investigate why

---

### 2. PDF Worker (✅ Already fixed)

**Location**: `dist/pdf/start-pdf-worker.mjs`

**Status**: ✅ **FIXED** - No Prisma in bundle

**How it was fixed**:

- Removed Prisma from worker execution path
- Worker only receives data, doesn't fetch it
- Service layer enqueues jobs with data (not IDs)
- Result handler persists metadata (not worker)

---

## Architecture Layers and Prisma Boundaries

```
┌─────────────────────────────────────────────────────────┐
│  Next.js Application (Has Prisma)                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │ Service/Orchestration Layer                    │    │
│  │ - Uses Prisma ✅                               │    │
│  │ - Calls repositories                           │    │
│  │ - Enqueues jobs WITH DATA                      │    │
│  └────────────────────────────────────────────────┘    │
│                        │                                 │
│                        ▼                                 │
│  ┌────────────────────────────────────────────────┐    │
│  │ Repository Layer                                │    │
│  │ - Prisma lives here ✅                          │    │
│  │ - Only place that knows DB structure            │    │
│  └────────────────────────────────────────────────┘    │
│                        │                                 │
│                        ▼                                 │
│  ┌────────────────────────────────────────────────┐    │
│  │ Adapter Layer (Dynamic imports)                │    │
│  │ - Bridges worker ↔ application                 │    │
│  │ - Uses Prisma ✅ (but externalized)            │    │
│  └────────────────────────────────────────────────┘    │
│                        │                                 │
└────────────────────────┼─────────────────────────────────┘
                         │
                         ▼ (Job with DATA, not ID)
┌─────────────────────────────────────────────────────────┐
│  Worker (Framework-Free, NO Prisma) ❌                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │ Worker Layer                                    │    │
│  │ - Receives data in job                         │    │
│  │ - Calls adapter functions                      │    │
│  │ - NO Prisma ❌                                  │    │
│  │ - NO DB access ❌                               │    │
│  └────────────────────────────────────────────────┘    │
│                        │                                 │
│                        ▼                                 │
│  ┌────────────────────────────────────────────────┐    │
│  │ Adapter Layer (Pure execution)                 │    │
│  │ - Renders PDF                                  │    │
│  │ - Stores PDF                                   │    │
│  │ - NO Prisma ❌                                  │    │
│  └────────────────────────────────────────────────┘    │
│                        │                                 │
│                        ▼ (Result)                        │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  Completion Handler (Has Prisma) ✅                     │
│  - Listens to job completion events                     │
│  - Persists metadata using Prisma                      │
└─────────────────────────────────────────────────────────┘
```

---

## Summary

### ✅ Prisma is NEEDED in

1. **Repository Layer** (`src/modules/billing/invoices/repositories/`)
   - Encapsulates all DB operations
   - Only place that knows DB structure

2. **Service/Orchestration Layer** (`src/modules/billing/services/`)
   - Orchestrates business logic
   - Calls repositories
   - Enqueues jobs with data

3. **ZATCA Service** (`src/modules/billing/zatca/zatca.service.ts`)
   - Handles ZATCA business logic
   - Uses Prisma for ZATCA documents

4. **Result Handlers** (`src/modules/billing/services/pdf-result.handler.ts`)
   - Runs in Next.js app
   - Persists metadata after job completion

5. **Application Adapters** (`src/adapters/`)
   - Bridges worker and application
   - Uses dynamic imports to avoid bundling
   - Should be externalized in tsup

### ❌ Prisma is LEAKING to

1. **ZATCA Worker Bundle** (`dist/zatca/start-zatca-worker.mjs`)
   - Currently includes Prisma runtime
   - Should be externalized (using dynamic imports + tsup external)
   - Still investigating why it's being bundled

2. **PDF Worker Bundle** (`dist/pdf/start-pdf-worker.mjs`)
   - ✅ **FIXED** - No Prisma in bundle
   - Worker only receives data, doesn't fetch

---

## Next Steps to Fix ZATCA Worker

1. ✅ Use dynamic imports in adapter
2. ✅ Externalize `@/lib/prisma` and `@/generated/prisma` in tsup config
3. ✅ Replace Prisma type imports with framework-free interfaces in:
   - `src/modules/billing/zatca/zatca.service.ts` - Uses custom `PrismaClient` interface
   - `src/modules/billing/zatca/prisma/zatca.payload.ts` - Uses custom `PrismaClient` interface
   - `src/modules/billing/zatca/types.ts` - Defines `ZatcaDocument` and `ZatcaDocumentStatus` without Prisma

**Result**:

- ✅ 0 references to `@/generated/prisma` or `@/lib/prisma` in worker bundles
- ⚠️ **Remaining Issue**: Prisma runtime imports (`@prisma/client/runtime`, `@prisma/adapter-pg`) still appear in bundle
  - **Answer to "Why Expected?": They are NOT expected!** Workers should have zero Prisma dependencies.
  - **Root Cause**: Prisma's generated code (`src/generated/prisma/internal/class.ts`, `src/generated/prisma/internal/prismaNamespace.ts`) is being bundled, and these files import Prisma runtime
  - **Why They Appear**: Even though we externalized `@prisma/client` in tsup config, tsup is still analyzing the dependency tree and including Prisma's generated internal code files
  - **The Problem**: Prisma generated code contains the entire schema as a string (inline in the bundle) and imports Prisma runtime, which gets bundled into the worker
  - **Why This Happens**: When tsup bundles code, it analyzes ALL imports (even type-only ones) and includes their dependencies if they're not properly externalized. Prisma's generated code imports Prisma runtime, which pulls it in
  - **Current Status**:
    - ✅ Removed `InvoicePdfRecord` type import from `map-invoice-to-view-model.ts` (replaced with framework-free types)
    - ⚠️ Prisma generated internal code still being bundled (lines 169, 195 show `src/generated/prisma/internal/*.ts` files)
    - **Impact**: Import statements remain in bundle, but Prisma packages are externalized (worker requires Prisma in `node_modules` at runtime - defeats the purpose of framework-free workers)
  - **Next Steps**: Need to prevent tsup from bundling `src/generated/prisma/**` files entirely by:
  1. Adding regex patterns to externalize all `src/generated/prisma/**` paths
  2. Or restructuring code to avoid any imports that transitively pull in Prisma generated code

---

**Last Updated**: January 10, 2025
**Status**: PDF worker fixed ✅, ZATCA worker fixed ✅
