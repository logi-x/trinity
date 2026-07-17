---
title: "Secrets must never appear in process arguments (curl `-H Authorization:...`, `redis-cli -a ...`); use environment variab"
date: "2026-05-26"
decision: "Secrets must never appear in process arguments (curl `-H Authorization:...`, `redis-cli -a ...`); use environment variables (`REDISCLI_AUTH`) or file-based secrets (`--pass-file`) instead. `/proc/<pid"
stakeholders: "Logix, Security"
review_by: "2026-08-26"
source: "[[Raw/sources/2026-05-26-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Secrets must never appear in process arguments (curl `-H Authorization:...`, `redis-cli -a ...`); use environment variables (`REDISCLI_AUTH`) or file-based secrets (`--pass-file`) instead. `/proc/<pid>/cmdline` is world-readable on Linux; process arguments are visible to any user on the host, including container-escape attackers.

**Rationale:** EXP-152/EXP-167. CRON_SECRET was passed via `curl -H Authorization` in cron sidecar; Redis password via `redis-cli -a` in healthcheck. Both are readable from `/proc` during execution.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-26-experts-agent-digest.md]]
