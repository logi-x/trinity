---
title: "EXP-239 — wrap `verifyConversation` + `persistAskAiExchange` in `$transaction` with `deleted_at IS NULL` re-check to pre"
date: "2026-05-31"
owner: "Logix (Ahmed)"
due: "2026-06-07"
priority: "medium"
status: "open"
source: "[[Raw/sources/2026-05-31-experts-agent-digest.md]]"
tags: [action, project/experts]
category: "meta"
up: "[[Action-Tracker]]"
updated: "2026-07-15"
---

> ↑ [[Action-Tracker]]

EXP-239 — wrap `verifyConversation` + `persistAskAiExchange` in `$transaction` with `deleted_at IS NULL` re-check to prevent writes to soft-deleted conversations

**Source:** [[Raw/sources/2026-05-31-experts-agent-digest.md]]
