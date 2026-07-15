---
title: "IMPLEMENTATION PHASE4"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/implementation-phase4"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  🟢 Phase 4 — Permissions & UX (don’t skip this)

Now that backend is clean, design UX rules.

6️⃣ Instructor dashboard permissions

Instructor can:

create draft

edit draft

submit for approval

see revenue (read-only)

see payouts

Instructor cannot:

publish

change entity after publish

edit pricing post-publish

7️⃣ Entity admin dashboard

Entity admin can:

review submissions

approve / reject

feature content

see total revenue

generate payouts

This maps cleanly to BusinessMembership.
