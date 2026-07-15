---
title: "`getCertificationsBucket()` must fail-closed (throw) when `R2_BUCKET_CERTIFICATIONS` is not set; silent fallback to the "
date: "2026-05-27"
decision: "`getCertificationsBucket()` must fail-closed (throw) when `R2_BUCKET_CERTIFICATIONS` is not set; silent fallback to the static bucket is prohibited."
stakeholders: "Logix"
review_by: "2026-08-27"
source: "[[Raw/sources/2026-05-28-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `getCertificationsBucket()` must fail-closed (throw) when `R2_BUCKET_CERTIFICATIONS` is not set; silent fallback to the static bucket is prohibited.

**Rationale:** EXP-135/EXP-178. Falling back to the static bucket routes certification uploads to the wrong origin and makes the orphan-reaper a risk for deleting static CDN assets. Fail-closed at boot surfaces the misconfiguration before it causes data loss.

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-05-28-experts-agent-digest.md]]
