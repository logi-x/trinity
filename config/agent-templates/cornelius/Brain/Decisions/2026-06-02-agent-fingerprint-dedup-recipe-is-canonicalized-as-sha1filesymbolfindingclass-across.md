---
title: "Agent fingerprint dedup recipe is canonicalized as `sha1(file:symbol:finding_class)` across all issue-filing routines (R"
date: "2026-06-02"
decision: "Agent fingerprint dedup recipe is canonicalized as `sha1(file:symbol:finding_class)` across all issue-filing routines (R01, R02, R07); severity and routine-of-origin are excluded from the salt. Cross-"
stakeholders: "Platform, Agents, Logix"
review_by: "2026-09-02"
source: "[[Raw/sources/2026-06-02-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Agent fingerprint dedup recipe is canonicalized as `sha1(file:symbol:finding_class)` across all issue-filing routines (R01, R02, R07); severity and routine-of-origin are excluded from the salt. Cross-type findings-index scan and near-match link-don't-fork gate prevent duplicate filings across routine boundaries.

**Rationale:** PR #759. EXP-269/270 duplicate filing shape confirmed the prior per-routine FP salting caused cross-routine dedup failures. Canonical recipe is documented in `_dedup-protocol.md`; inlined into all three routine prompt files.

**Stakeholders:** Platform, Agents, Logix

**Source:** [[Raw/sources/2026-06-02-experts-agent-digest.md]]
