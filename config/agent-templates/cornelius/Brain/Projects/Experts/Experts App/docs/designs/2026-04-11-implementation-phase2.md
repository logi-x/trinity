---
title: "IMPLEMENTATION PHASE2"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/implementation-phase2"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  🟢 Phase 2 — Solidify Revenue & Payout Model

You already did the hard part by removing ownership confusion.

Now make it executable.

3️⃣ Decide ONE payout truth

Pick one:

✔ revenueShare on CourseInstructor / EventHost

❌ derived percentages in code only

You already chose the correct one.

Now enforce:

SUM(revenueShare) === 100

at publish time.

4️⃣ Define payout timing (critical)

You must answer explicitly:

After event ends?

After refund window?

Monthly batch?

Example (recommended):

Instructor revenue becomes payable only after refund window closes

This determines:

when pending → payable

when payouts can be generated
