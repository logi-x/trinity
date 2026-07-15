---
title: "WORKERS V4 ZATCA"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/workers-v4-zatca"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# WORKERS V4 ZATCA

there is one architectural boundary that’s currently being violated, and that’s what’s causing all the pain and confusion.

our worker is dynamically importing an app-layer adapter that was never built or shipped alongside the worker bundle.

That means:

✔️ Your code logic is correct

❌ Your runtime resolution model is broken

This is not a Prisma problem, and not a BullMQ problem.

It’s a deployment / build boundary mismatch.

The single rule you are breaking (unintentionally)

A worker bundle must never import code that is not guaranteed to exist in its runtime filesystem.

Dynamic imports do not magically pull code from your app container.

They still require:

a real .js/.mjs file

at a real path

present inside the same container / image

Right now, this line is the smoking gun:

const {processZatcaWithInfra} = await import(
"../../modules/billing/zatca/adapters/zatca.adapter"
);

Why this fails

tsup bundles only the worker entry graph

You explicitly externalized the adapter

Therefore:

it is not bundled

it is not emitted to dist/

it does not exist in the worker image

So at runtime Node says:

“Cannot find module …/zatca.adapter”

Which is 100% correct.

Why this feels confusing

Because conceptually you did this:

“Workers don’t bundle Prisma — adapters will handle infra”

But operationally, the worker container has no access to app code.

Containers are isolated.

Dynamic import ≠ cross-container import.

Very important clarification
This statement is correct:

“The adapter is externalized and dynamically imported at runtime, preventing Prisma from being bundled”

But this conclusion is incorrect:

“Therefore workers don’t access the DB”

Reality:

If the adapter runs inside the worker container, it does access the DB

Externalizing only affects bundling, not responsibility

So yes — this still means the worker has DB access, just indirectly.

What’s actually wrong in your current design

You’re trying to support two incompatible execution models in one worker:

✅ New model — pure worker (PDF-style)

❌ Legacy model — infra-aware worker via adapter

That’s what’s causing:

path resolution issues

Prisma leaking

bundling explosions

mental overload

The correct fix (no hand-waving)

You must choose one of these, explicitly.

✅ Option 1 (RECOMMENDED): Kill the adapter path entirely

This is the clean, scalable, future-proof solution.

Rule

Workers only execute pure logic.
Apps own all DB reads/writes.

What to do
1️⃣ Delete this from the worker
// ❌ REMOVE THIS ENTIRE BRANCH
const {processZatcaWithInfra} = await import(
"../../modules/billing/zatca/adapters/zatca.adapter"
);
await processZatcaWithInfra(jobData);

2️⃣ Make ALL ZATCA jobs carry context
type ZatcaJob =
| {
kind: "EXECUTE_ZATCA";
context: ZatcaContextSnapshot;
requestId?: string;
};

3️⃣ App does this (only place with Prisma)
const context = await getZatcaContext(prisma, zatcaDocumentId);

await enqueueZatcaJob({
kind: "EXECUTE_ZATCA",
context,
requestId,
});

4️⃣ Worker stays pure forever
const result = await executeZatca(context, requestId);
return result;

5️⃣ App completion handler persists
queueEvents.on("completed", async ({returnvalue}) => {
await persistZatcaResult(prisma, returnvalue);
});

Result

❌ No adapter in worker

❌ No Prisma in worker

❌ No dynamic imports

❌ No path issues

✅ Same model as PDF

✅ Smaller bundles

✅ Easier testing

✅ Clear ownership

Answering your direct questions
❓ “What’s wrong?”

Nothing is wrong with:

your repositories

your processor

your separation of concerns

What’s wrong is:

importing app-layer adapters from a pure worker runtime

❓ “Is the adapter pattern itself wrong?”

No — it’s correct inside the app, not inside the worker.

Adapters belong here:

Next.js app
├─ repositories (Prisma)
├─ services
├─ adapters ✅
└─ queue enqueue

Not here:

Worker runtime ❌

❓ “Can workers still access the DB?”

In your current setup:

Yes, via adapter

Even if Prisma isn’t bundled

In the recommended setup:

No

Workers literally have no code capable of DB access

The mental model to lock in

Workers are CPUs.
Apps are brains.
Adapters belong to brains, not CPUs.

Once you accept that, everything simplifies.

Final recommendation (very clear)

✔ Remove the adapter import path from the worker
✔ Only support context-based ZATCA jobs
✔ Keep all Prisma usage in app services & repositories
✔ Let completion handlers persist results

You already proved this works with PDF.

ZATCA is just catching up.
