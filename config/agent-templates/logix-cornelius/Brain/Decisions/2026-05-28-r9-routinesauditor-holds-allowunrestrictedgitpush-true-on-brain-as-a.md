---
title: "R9 routines-auditor holds `allow_unrestricted_git_push: true` on brain as a temporary grant; this grant must be revoked "
date: "2026-05-28"
decision: "R9 routines-auditor holds `allow_unrestricted_git_push: true` on brain as a temporary grant; this grant must be revoked or narrowed once EXP-173's server-side push guard is deployed. Treat as a time-l"
stakeholders: "Logix, Security"
review_by: "2026-06-04"
source: "[[Raw/sources/2026-05-28-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** R9 routines-auditor holds `allow_unrestricted_git_push: true` on brain as a temporary grant; this grant must be revoked or narrowed once EXP-173's server-side push guard is deployed. Treat as a time-limited exception, not a permanent pattern.

**Rationale:** EXP-173: R9 was added with broad push access before a server-side guard exists. The tool-grant CI gate (PR #548) prevents adding new grants without human approval, but does not retroactively constrain already-merged agent configs. Until the brain-side enforcement workflow is deployed, R9 has unguarded write access to the brain vault.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-28-experts-agent-digest.md]]
