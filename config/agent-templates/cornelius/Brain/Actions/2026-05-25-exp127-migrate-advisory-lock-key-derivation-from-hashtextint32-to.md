---
title: "EXP-127 — migrate advisory lock key derivation from hashtext()::int32 to full 64-bit key (e.g. ('x'  md5(userId))::bit(6"
date: "2026-05-25"
owner: "Logix (Ahmed)"
due: "2026-06-15"
priority: "medium"
status: "open"
source: "Agent-Filed Issues — 25 May 2026"
tags: [action, project/experts]
category: "meta"
up: "[[Action-Tracker]]"
updated: "2026-07-15"
---

> ↑ [[Action-Tracker]]

EXP-127 — migrate advisory lock key derivation from hashtext()::int32 to full 64-bit key (e.g. ('x'  md5(userId))::bit(64)::bigint) to eliminate birthday collision at ~55k users

**Source:** Agent-Filed Issues — 25 May 2026
