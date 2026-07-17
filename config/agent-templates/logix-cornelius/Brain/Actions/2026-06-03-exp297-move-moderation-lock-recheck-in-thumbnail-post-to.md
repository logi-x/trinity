---
title: "EXP-297 — move moderation lock re-check in thumbnail POST to after `arrayBuffer()`/hash computation (before R2 write); p"
date: "2026-06-03"
owner: "Logix (Ahmed)"
due: "2026-06-10"
priority: "medium"
status: "open"
source: "[[Raw/sources/2026-06-03-experts-agent-digest.md]]"
tags: [action, project/experts]
category: "meta"
up: "[[Action-Tracker]]"
updated: "2026-07-15"
---

> ↑ [[Action-Tracker]]

EXP-297 — move moderation lock re-check in thumbnail POST to after `arrayBuffer()`/hash computation (before R2 write); prevents 50–200ms TOCTOU gap that orphans R2 assets with permanent quota charge

**Source:** [[Raw/sources/2026-06-03-experts-agent-digest.md]]
