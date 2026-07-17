---
title: "EXP-296 — fix TOCTOU in PUT /posts/[id] moderation lock: replace read-check-write with atomic `prisma.post.update({ wher"
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

EXP-296 — fix TOCTOU in PUT /posts/[id] moderation lock: replace read-check-write with atomic `prisma.post.update({ where: { id, adminLockedAt: null }, data: ... })`; fix together with EXP-295 in one PR

**Source:** [[Raw/sources/2026-06-03-experts-agent-digest.md]]
