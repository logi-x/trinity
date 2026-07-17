---
title: "`safeErrorJson` is the sole permitted serializer for `NextResponse.json()` error bodies in all API route handlers. Raw `"
date: "2026-05-23"
decision: "`safeErrorJson` is the sole permitted serializer for `NextResponse.json()` error bodies in all API route handlers. Raw `error.message`, `error.stack`, or any caught exception field must never appear d"
stakeholders: "Logix, Security"
review_by: "2026-08-23"
source: "[[Raw/sources/2026-05-23-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `safeErrorJson` is the sole permitted serializer for `NextResponse.json()` error bodies in all API route handlers. Raw `error.message`, `error.stack`, or any caught exception field must never appear directly in a JSON response body. `DomainError` is the mechanism for surfacing intentional client-facing messages.

**Rationale:** EXP-170 class. Prisma/DB error messages, stack traces, and internal identifiers have been routinely leaked to clients. A class-level lint + runtime guard is the only way to prevent recurrence across 100+ route files.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-23-experts-agent-digest.md]]
