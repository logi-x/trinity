---
title: "Logix Kernel"
date: "2026-07-05"
updated: "2026-07-05"
status: "active"
freshness: "volatile"
verified: "2026-07-05"
source_of_truth: "/home/logix/logix-kernel"
verify_with:
  - "git log"
  - "local repo status"
tags: ["project/logix", "project/logix-kernel"]
category: "entity/project"
source: "generated"
source_id: "Entities/Projects/Logix Kernel.md"
repo_root: "/home/logix/logix-kernel"
---

## Overview

Logix Kernel is the Phase 1 foundation for **Logix Command Center**: internal OS for Logix, Inc. — command-center web app, Fastify API, Prisma/Postgres, worker queue, typed SDK, permissions, audit, client portal, vault, proposals, invoices, requests, agents, memory, repositories, workflows, search, and dashboard. Phases 1–2 are implemented in the current branch; finance (1.1), maturity (2.1), agent runtime (3+), integrations, and autopilot are planned.

## Links

- [[Entities/Projects/Logix|Logix (umbrella)]]
- [[Projects/Logix/KERNEL/Logix Kernel|Project hub note]]
- [[Projects/Logix/KERNEL/docs|Curated docs index]]

## Repo

- Checkout: `/home/logix/logix-kernel` (`repo_root` in frontmatter)
- Canonical product README lives in the git repo; vault note is the entry surface for agents and graph routing.

---

Test AI generic questions:

What’s our launch date?

We are targeting a launch date of July 15th, 2026.

What’s the status of the project?

The project is currently in the planning phase.

How much did this project cost to build ?

What's the content of brand-colors.txt ?

What colors/fonts are used in this project ?

How does the affiliate program work ?

Why didn't we implement affiliate discounts yet ?

What's the average salary of a software engineer in Saudi Arabia ?

What's the average cost for running a campaign on Logix ?

What's the average cost for running a campaign on Meta Ads ?


---

**Discovery Call Prep – Affiliate Discounts**

| Item | Detail |
|------|--------|
| **Primary Goal** | Understand Logix’s current stance on affiliate‑discount features and identify blockers to implementation. |
| **Key Questions** | 1. What business value do we expect from offering discounts to affiliates? <br>2. How would discount logic interact with existing commission, refund, and settlement flows? <br>3. Are there regulatory or accounting constraints (e.g., VAT, ZATCA reporting) that prevent us from applying discounts? <br>4. What is the expected impact on instructor revenue and platform earnings? <br>5. Do we have a clear product‑owner or stakeholder who can champion this feature? |
| **Anticipated Objections** | • *“Discounts could erode instructor margins.”* – We’ll need to model margin impacts and possibly tie discounts to commission caps. <br>• *“Adding discount logic will complicate the settlement pipeline.”* – Highlight that we can reuse existing price‑order hooks and extend the `priceOrder` flow without breaking current guarantees. |
| **Single Success Outcome** | The call ends with a signed‑off “Affiliate Discount Feasibility” document that lists: <br>• Business justification, <br>• Technical dependencies (e.g., new DB fields, API endpoints), <br>• Regulatory checks, and <br>• A prioritized roadmap item. |
## LLM Entry Points

- Status: Internal OS / command center project hub.
- Start here: this entity hub, then the project-local docs below.
- [[Projects/Logix/KERNEL/Logix Kernel]]
- [[Projects/Logix/KERNEL/docs]]
- Actions: [[Actions/Action-Tracker]]
- Decisions: [[Decisions/Decision-Log]]

## Update Rules

- Keep this hub concise and durable.
- Put detailed working context under `Projects/`.
- Put reusable ideas under [[Concepts]].
- Put source-derived summaries under [[Summaries]].
