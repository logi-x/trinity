---
title: "All list endpoints must enforce a server-side upper-bound cap on `take`; user-supplied `limit` parameters must be clampe"
date: "2026-05-31"
decision: "All list endpoints must enforce a server-side upper-bound cap on `take`; user-supplied `limit` parameters must be clamped to a per-endpoint maximum; `take: undefined` is prohibited in Prisma queries o"
stakeholders: "Logix / Backend / Platform"
review_by: "2026-08-31"
source: "[[Raw/sources/2026-05-31-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** All list endpoints must enforce a server-side upper-bound cap on `take`; user-supplied `limit` parameters must be clamped to a per-endpoint maximum; `take: undefined` is prohibited in Prisma queries on list routes.

**Rationale:** EXP-242 (`take:undefined` for popular/discussed sort) and EXP-243 (user-supplied `limit` uncapped for recent sort) were filed on the same handler on the same day, indicating a systemic gap. Uncapped list queries can drive unbounded DB scans, memory exhaustion, and unauthenticated DoS at production scale.

**Stakeholders:** Logix / Backend / Platform

**Source:** [[Raw/sources/2026-05-31-experts-agent-digest.md]]
