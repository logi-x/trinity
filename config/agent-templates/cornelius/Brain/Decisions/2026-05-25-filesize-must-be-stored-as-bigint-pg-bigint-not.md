---
title: "`File.size` must be stored as `BigInt` (PG `BIGINT`) not `Int` (PG `INTEGER`); 32-bit int overflow at ~2.1 GB silently w"
date: "2026-05-25"
decision: "`File.size` must be stored as `BigInt` (PG `BIGINT`) not `Int` (PG `INTEGER`); 32-bit int overflow at ~2.1 GB silently wraps and corrupts the storage ledger, enabling quota bypass. Migration must land"
stakeholders: "Logix"
review_by: "2026-06-06"
source: "[[Raw/sources/2026-05-25-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `File.size` must be stored as `BigInt` (PG `BIGINT`) not `Int` (PG `INTEGER`); 32-bit int overflow at ~2.1 GB silently wraps and corrupts the storage ledger, enabling quota bypass. Migration must land before any user approaches 2 GB total storage.

**Rationale:** EXP-87. `_sum` aggregation on `Int` columns wraps at 2^31–1 bytes; a user with exactly 2.1 GB of files would appear to have negative usage to the quota guard.

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-05-25-experts-agent-digest.md]]
