---
title: "When a `conversationId` is present in an Ask AI request, `buildOpenAiMessages` must source conversation history exclusiv"
date: "2026-05-31"
decision: "When a `conversationId` is present in an Ask AI request, `buildOpenAiMessages` must source conversation history exclusively from the database and discard any client-supplied `history` array; trusting "
stakeholders: "Security / Logix / AI-Feature"
review_by: "2026-08-31"
source: "[[Raw/sources/2026-05-31-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** When a `conversationId` is present in an Ask AI request, `buildOpenAiMessages` must source conversation history exclusively from the database and discard any client-supplied `history` array; trusting client-supplied history is prohibited.

**Rationale:** EXP-232, EXP-237, and EXP-244 — three independent scanner hits on `buildOpenAiMessages` within 12 hours — confirm the pattern is a systemic trust boundary violation. Fabricated `role: "assistant"` turns in client-supplied history allow users to manipulate AI context and simulate non-existent platform policies.

**Stakeholders:** Security / Logix / AI-Feature

**Source:** [[Raw/sources/2026-05-31-experts-agent-digest.md]]
