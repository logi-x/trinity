---
title: "Per-entity advisory locks over high-cardinality sets (users, resources) must use `pg_advisory_xact_lock(hashtextextended"
date: "2026-06-05"
decision: "Per-entity advisory locks over high-cardinality sets (users, resources) must use `pg_advisory_xact_lock(hashtextextended('namespace:'"
stakeholders: "Logix, Security"
review_by: "2026-09-05"
source: "[[Raw/sources/2026-06-06-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Per-entity advisory locks over high-cardinality sets (users, resources) must use `pg_advisory_xact_lock(hashtextextended('namespace:'

**Rationale:** id, 0))` (int64, 2^64 keyspace), never the two-arg int32 form.** (EXP-127, PR #857) The two-arg `pg_advisory_xact_lock(namespace_int4, hashtext(id))` form has only 2^32 keyspace; birthday collision at ~55k users causes two unrelated users' locks to serialize, creating intermittent storage-quota DoS. The namespaced int64 form gives negligible collision probability at any realistic scale. Apply to all future per-entity serialization locks.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-06-06-experts-agent-digest.md]]
