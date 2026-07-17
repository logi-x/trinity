---
title: "Upload route outer catch must return 503+Retry-After on DB transient errors (Prisma P1001/P1002/P1008/P1017 and connecti"
date: "2026-06-01"
decision: "Upload route outer catch must return 503+Retry-After on DB transient errors (Prisma P1001/P1002/P1008/P1017 and connection-pool exhaustion); swallowing Prisma errors and returning 403 Forbidden is pro"
stakeholders: "Backend, API consumers"
review_by: "2026-06-15"
source: "[[Raw/sources/2026-06-01-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Upload route outer catch must return 503+Retry-After on DB transient errors (Prisma P1001/P1002/P1008/P1017 and connection-pool exhaustion); swallowing Prisma errors and returning 403 Forbidden is prohibited.

**Rationale:** DB timeouts were silently reported as permission denials; on staging this made a DB outage look like an auth bug and blocked legitimate uploads for the duration of the outage. A 503 is the correct HTTP signal for a retriable infrastructure fault.

**Stakeholders:** Backend, API consumers

**Source:** [[Raw/sources/2026-06-01-experts-agent-digest.md]]
