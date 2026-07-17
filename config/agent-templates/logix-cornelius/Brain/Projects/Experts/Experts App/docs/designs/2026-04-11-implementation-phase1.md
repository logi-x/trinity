---
title: "IMPLEMENTATION PHASE1"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/implementation-phase1"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  🟢 Phase 1 — Lock the Publishing Lifecycle

(Do this first — everything depends on it)

You already hinted at this with publishingStatus.

1️⃣ Finalize publishing states (authoritative)
enum PublishingStatus {
draft
submitted
approved
rejected
published
archived
}

Rules to enforce:

draft → instructor only

submitted → entity admins review

approved → system-only transition

published → immutable processingEntityId

archived → read-only

👉 This prevents 80% of future bugs.

2️⃣ Implement approval boundaries (code-level)

Create one service (not scattered logic):

canSubmit(user, course)
canApprove(user, course)
canPublish(course)

If this feels boring → it’s exactly right.
Boring here = safe later.
