---
title: "Realtime sync polling endpoint security model: channel authorization must use `authorizedPostIds` gate (`isPublished OR "
date: "2026-05-29"
decision: "Realtime sync polling endpoint security model: channel authorization must use `authorizedPostIds` gate (`isPublished OR owner`); `MAX_CHANNELS=20` cap; UUID-shape guard on all caller-supplied post IDs"
stakeholders: "Logix, Security"
review_by: "2026-06-12"
source: "[[Raw/sources/2026-05-28-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Realtime sync polling endpoint security model: channel authorization must use `authorizedPostIds` gate (`isPublished OR owner`); `MAX_CHANNELS=20` cap; UUID-shape guard on all caller-supplied post IDs; `take:` bounds on all downstream queries (`take:500` total, `take:50` per Section 2/3); `isChannelRequested(channel)` strict match at all emit sites — no coarse-gate short-circuit.

**Rationale:** PRs #612 (EXP-174 IDOR), #613 (EXP-192 Section 2 take: bound), #614 (EXP-193 channel isolation) establish the security invariants for `/api/v1/internal/realtime/sync`. Anonymous access to published-post channels is permitted (public activity). Authenticated users are bounded to owned or published posts via `authorizedPostIds`. Remaining open spinoffs: EXP-191 (rate limiting), EXP-194 (Section 3 unbounded Prisma queries — DoS at 3s poll cadence), EXP-195 (liker PII in public-post events).

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-28-experts-agent-digest.md]]
