---
title: "EXP-287 — move `auth()` + `getUserPermissions()` back inside `try` block in GET /api/v1/community/posts/[id]; regression"
date: "2026-06-02"
owner: "Logix (Ahmed)"
due: "2026-06-09"
priority: "medium"
status: "open"
source: "[[Raw/sources/2026-06-02-experts-agent-digest.md]]"
tags: [action, project/experts]
category: "meta"
up: "[[Action-Tracker]]"
updated: "2026-07-15"
---

> ↑ [[Action-Tracker]]

EXP-287 — move `auth()` + `getUserPermissions()` back inside `try` block in GET /api/v1/community/posts/[id]; regression from EXP-254 fix (commit 3b55692) placed auth outside try, so auth exceptions bypass `safeErrorJson`

**Source:** [[Raw/sources/2026-06-02-experts-agent-digest.md]]
