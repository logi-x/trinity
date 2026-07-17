---
title: "All Docker service ports that are not intended to be publicly reachable must be bound to `127.0.0.1` (loopback) in `dock"
date: "2026-05-24"
decision: "All Docker service ports that are not intended to be publicly reachable must be bound to `127.0.0.1` (loopback) in `docker-compose.yml`; Docker's iptables injection bypasses UFW/OS firewall rules, so "
stakeholders: "Logix, Security"
review_by: "2026-06-24"
source: "[[Raw/sources/2026-05-24-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** All Docker service ports that are not intended to be publicly reachable must be bound to `127.0.0.1` (loopback) in `docker-compose.yml`; Docker's iptables injection bypasses UFW/OS firewall rules, so binding to `0.0.0.0` exposes services to the internet regardless of firewall rules.

**Rationale:** EXP-101. Production PostgreSQL (5432) and Redis (6379) were bound to `0.0.0.0`, reachable from the public internet via Docker iptables. UFW rules had no effect. The fix is a one-line change per service in compose; the risk of the unfixed state is complete database exposure.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-24-experts-agent-digest.md]]
