---
title: "Runtime secrets (CRON_SECRET, REDIS_PASSWORD, database credentials) must be delivered to containers via Docker secrets ("
date: "2026-05-28"
decision: "Runtime secrets (CRON_SECRET, REDIS_PASSWORD, database credentials) must be delivered to containers via Docker secrets (tmpfs-mounted files) or explicit `environment:` blocks — never via `env_file:` p"
stakeholders: "Logix, Security"
review_by: "2026-06-11"
source: "[[Raw/sources/2026-05-28-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Runtime secrets (CRON_SECRET, REDIS_PASSWORD, database credentials) must be delivered to containers via Docker secrets (tmpfs-mounted files) or explicit `environment:` blocks — never via `env_file:` passthrough or process argument vectors.

**Rationale:** PRs #566, #568, #577 completed a three-step class-level fix: EXP-152 (CRON_SECRET in curl args), EXP-167 (REDIS_PASSWORD in healthcheck args), EXP-168 (all remaining env_file secrets). `env_file: .env` was removed from all services. Docker secrets are tmpfs-mounted (no disk persistence) and scoped per service. Any future service addition must use explicit `environment:` entries for secrets; use the PR #577 compose structure as reference.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-28-experts-agent-digest.md]]
