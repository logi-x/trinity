---
title: "Docker image tags in production and staging compose files must be pinned to a specific version (e.g. `redis:7.2-alpine`)"
date: "2026-05-24"
decision: "Docker image tags in production and staging compose files must be pinned to a specific version (e.g. `redis:7.2-alpine`) or digest (`@sha256:...`); `latest` and mutable tags are prohibited."
stakeholders: "Logix"
review_by: "2026-07-24"
source: "[[Raw/sources/2026-05-24-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Docker image tags in production and staging compose files must be pinned to a specific version (e.g. `redis:7.2-alpine`) or digest (`@sha256:...`); `latest` and mutable tags are prohibited.

**Rationale:** EXP-102. `redis:latest` in production can silently upgrade to a breaking or vulnerable version on next `docker compose pull`. Pinned tags give reproducible deployments and CVE-trackable images.

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-05-24-experts-agent-digest.md]]
