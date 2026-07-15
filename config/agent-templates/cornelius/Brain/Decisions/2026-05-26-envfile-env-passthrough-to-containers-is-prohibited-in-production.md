---
title: "`env_file: .env` passthrough to containers is prohibited in production and staging; secrets must be injected via Docker "
date: "2026-05-26"
decision: "`env_file: .env` passthrough to containers is prohibited in production and staging; secrets must be injected via Docker secrets (tmpfs-mounted at `/run/secrets/<name>`) or explicit `environment:` entr"
stakeholders: "Logix, Security"
review_by: "2026-08-26"
source: "[[Raw/sources/2026-05-26-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `env_file: .env` passthrough to containers is prohibited in production and staging; secrets must be injected via Docker secrets (tmpfs-mounted at `/run/secrets/<name>`) or explicit `environment:` entries for non-secret config.

**Rationale:** EXP-168. `env_file: .env` passes the entire environment file — including all credentials — to every service, violating least-privilege. Docker secrets are tmpfs-mounted (no disk persistence) and scoped per-service; they are the correct mechanism for credential delivery.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-26-experts-agent-digest.md]]
