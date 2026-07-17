---
title: "All external-dependency upgrades (pnpm, Node, Docker base images, Prisma) require a corresponding update to CI workflows"
date: "2026-05-28"
decision: "All external-dependency upgrades (pnpm, Node, Docker base images, Prisma) require a corresponding update to CI workflows, Dockerfile `FROM` pins, and developer onboarding docs before the PR can merge."
stakeholders: "Logix"
review_by: "2026-06-11"
source: "[[Raw/sources/2026-05-28-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** All external-dependency upgrades (pnpm, Node, Docker base images, Prisma) require a corresponding update to CI workflows, Dockerfile `FROM` pins, and developer onboarding docs before the PR can merge. Partial upgrades that leave CI or Docker on a stale version are a build-stability liability.

**Rationale:** PR #617 bumped pnpm to 11.5.0. CI and Docker build images were not co-updated in the same PR, creating a build-environment drift window.

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-05-28-experts-agent-digest.md]]
