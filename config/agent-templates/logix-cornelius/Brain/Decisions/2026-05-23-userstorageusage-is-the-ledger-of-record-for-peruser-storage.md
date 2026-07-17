---
title: "`UserStorageUsage` is the ledger of record for per-user storage; atomic advisory-lock reservation (`reserveStorageBytes`"
date: "2026-05-23"
decision: "`UserStorageUsage` is the ledger of record for per-user storage; atomic advisory-lock reservation (`reserveStorageBytes` → `promoteReservation` → `releaseStorageBytes`) is the only permitted way to mo"
stakeholders: "Logix"
review_by: "2026-08-23"
source: "[[Raw/sources/2026-05-23-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `UserStorageUsage` is the ledger of record for per-user storage; atomic advisory-lock reservation (`reserveStorageBytes` → `promoteReservation` → `releaseStorageBytes`) is the only permitted way to modify it. Direct `UPDATE user_storage_usage SET used_bytes = ...` without the advisory lock is prohibited.

**Rationale:** EXP-80. Race conditions on direct updates allow quota bypass under concurrent uploads. The advisory lock serializes per-user writes without a global lock.

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-05-23-experts-agent-digest.md]]
