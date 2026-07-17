---
title: "EXP-194 — add `take:` bounds to Section 3 `prisma.post.findMany` (`realtime/sync/route.ts:~281`) and `prisma.comment.fin"
date: "2026-05-29"
owner: "Logix (Ahmed)"
due: "2026-06-12"
priority: "high"
status: "open"
source: "[[Raw/sources/2026-05-29-experts-agent-digest.md]]"
tags: [action, project/experts]
category: "meta"
up: "[[Action-Tracker]]"
updated: "2026-07-15"
---

> ↑ [[Action-Tracker]]

EXP-194 — add `take:` bounds to Section 3 `prisma.post.findMany` (`realtime/sync/route.ts:~281`) and `prisma.comment.findMany` (`:~288`); user with 1 000+ posts/comments drives unbounded DB round-trips on every 3s poll tick — hot-path DoS amplifier.

**Source:** [[Raw/sources/2026-05-29-experts-agent-digest.md]]
