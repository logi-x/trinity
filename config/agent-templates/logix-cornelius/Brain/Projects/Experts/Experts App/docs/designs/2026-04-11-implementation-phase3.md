---
title: "IMPLEMENTATION PHASE3"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/implementation-phase3"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  🟢 Phase 3 — Align with your ZATCA / invoicing flow

You’ve already built a lot here — now connect it cleanly.

5️⃣ One invariant (never break this)

Invoices are issued ONLY by BusinessEntity

Never by:

User

Instructor

Host

So ensure:

invoice references eventId | courseId

entityId is always derived from content

This keeps you compliant forever.
