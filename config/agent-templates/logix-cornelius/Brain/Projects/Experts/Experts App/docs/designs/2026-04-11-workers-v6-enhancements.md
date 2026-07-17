---
title: "WORKERS V6 ENHANCEMENTS"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/workers-v6-enhancements"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# WORKERS V6 ENHANCEMENTS

✅ What you got right (core correctness)

Your flow:

Next.js App Starts
↓
Health Check Route Called (or Workers Init Route)
↓
initializeWorkers() called
↓
setupPdfResultHandler()
↓
setupZatcaResultHandler()
↓
Handlers ready

This is architecturally valid because:

Result handlers:

Must live in the app layer

Must have Prisma access

Must not be bundled into workers

Workers:

Execute jobs

Return results

Do not coordinate follow-up actions

So initializing result handlers from the app runtime is correct.

This is exactly the same pattern used in:

queue-driven microservices

webhook processors

background event listeners

✅ You are not “cheating” or hacking around Next.js here.

⚠️ Clarification #1: This is NOT a “health check” concern

Calling it via a health check route is semantically wrong, even if it works.

Health checks must be:

idempotent

side-effect free

safe to call frequently

Initializing queue listeners is none of the above.

❌ Don’t do this:
GET /health
→ initializeWorkers()

Because:

load balancers call health routes repeatedly

multiple instances = duplicate listeners

you’ll get double persistence or race conditions

✅ Better naming (important for future you)

Rename the concept to something explicit:

initializeBackgroundListeners()
initializeQueueCompletionHandlers()
initializeAppWorkers()

And expose it via:

GET /api/internal/workers/init

or better yet — no HTTP at all (see below).

⚠️ Clarification #2: This MUST be singleton-guarded

If your Next.js app runs in:

multiple pods

multiple PM2 workers

or hot-reloads in dev

Then calling setupPdfResultHandler() more than once will cause:

❌ duplicate handlers
❌ double DB writes
❌ phantom retries

You MUST guard initialization:
let initialized = false;

export function initializeWorkers() {
if (initialized) return;
initialized = true;

setupPdfResultHandler();
setupZatcaResultHandler();
}

This is non-negotiable.

✅ Recommended improvement (best practice)
🔥 Best pattern: initialize on server bootstrap, not HTTP

Instead of:

HTTP → init

Prefer:

Option A — App entrypoint (Node runtime only)

If you have a custom server or standalone Next runtime:

// app/bootstrap.ts
initializeWorkers();

Imported once when the app starts.

Option B — Next.js instrumentation hook (BEST)

If you’re on modern Next.js (13+ App Router):

// instrumentation.ts
export async function register() {
if (process.env.NEXT_RUNTIME === "nodejs") {
initializeWorkers();
}
}

This runs:

once per server instance

before handling requests

not during builds

not in edge runtime

This is the cleanest solution.

✅ Final verdict
Your idea is:

✅ Architecturally correct

✅ Production-safe if guarded

⚠️ Poorly named if tied to “health”

⚠️ Dangerous if called multiple times

The corrected, ideal version:
Next.js Server Bootstraps
↓
instrumentation.ts runs
↓
initializeQueueCompletionHandlers()
↓
PDF & ZATCA result handlers active
