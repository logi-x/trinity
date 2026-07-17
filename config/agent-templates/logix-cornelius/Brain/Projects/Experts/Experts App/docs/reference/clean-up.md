---
title: "CLEAN UP"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/clean-up"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# CLEAN UP

🧩 Minor Cleanups I Strongly Recommend

These are not required, but they will save you future pain.

1. Make result handlers idempotent

QueueEvents can replay.

Ensure:

persistZatcaResult(prisma, result)

Checks status before updating

Uses WHERE status IN (...)

Is safe if called twice

Same for PDF metadata.

2. Explicit job contracts (types)

You already did most of this, but lock it in:

type ExecuteZatcaJob = {
kind: "EXECUTE_ZATCA";
context: ZatcaContext;
requestId?: string;
};

Never allow:

invoiceId

creditNoteId

zatcaDocumentId

into worker jobs again.

3. Result handlers should start once

Your earlier note was correct:

Next.js App Start
→ initializeQueueCompletionHandlers()
→ setupZatcaResultHandler()
→ setupPdfResultHandler()

Make sure this is:

Guarded with a singleton

Not triggered per request

Not tied to hot reloads in prod

4. Environment rule (critical)

Workers do NOT need .env files.

They need only:

REDIS\_\*

Worker-specific infra vars

ZATCA SDK paths (for ZATCA worker)

All business config must already be baked into the context snapshot.

If a worker needs .env, that’s a smell.

🧪 How to Test This (High-level guidance)

You don’t test “the flow” in one place anymore. You test each boundary:

1. Executor tests (pure)

Given context → returns correct result

No mocks except HTTP/SDK

2. Repository tests

Prisma in / Prisma out

No workers involved

3. Worker tests

Given job → executor called → result returned

Redis mocked

4. Integration smoke test

Enqueue job

Let worker process

Result handler persists

No end-to-end monster tests needed.

🧠 Final Verdict

You are now doing Option 4 correctly.

What you have:

Is scalable

Is debuggable

Is explainable

Has clear ownership boundaries

Matches how large production systems work

The pain you felt earlier was transition pain.
This version is the stable equilibrium.
