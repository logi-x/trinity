---
title: "Course moderation model is risk-based, not a blanket pre-publish queue: (1) normal instructor courses publish instantly "
date: "2026-06-04"
decision: "Course moderation model is risk-based, not a blanket pre-publish queue: (1) normal instructor courses publish instantly (lifecycle collapses to `draft → published`); (2) reactive post-publish moderati"
stakeholders: "Logix, Product"
review_by: "2026-09-04"
source: "[[Raw/sources/2026-06-03-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Course moderation model is risk-based, not a blanket pre-publish queue: (1) normal instructor courses publish instantly (lifecycle collapses to `draft → published`); (2) reactive post-publish moderation via `adminLockedAt` admin takedown is the primary safety net; (3) real pre-publish `submit → pending → approve` review is reserved for `recognitionType: ACADEMIC` certification-bearing courses only.

**Rationale:** EXP-292. Experts is marketplace-shaped (shared catalog/search/recs + certification claims) but runs creator-storefront speed; the prior ambiguous half-state (dead submit/pending machinery bypassed by create-time auto-approve) caused the EXP-318 create→build 409 regression. Risk-based moderation reuses existing primitives (`adminLockedAt` takedown from EXP-280/295, `recognitionType` cert guard) and matches Udemy/Skillshare-class gating — review the high-stakes slice, react on the rest. EXP-278/235 re-scoped to the cert lane. EXP-292 is the implementation tracker.

**Stakeholders:** Logix, Product

**Source:** [[Raw/sources/2026-06-03-experts-agent-digest.md]]
