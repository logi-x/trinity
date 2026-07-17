---
title: "EXP-285 — fix `handleCourseSubmit` TOCTOU race; wrap `findUnique` + `update` in `$transaction`; must fix atomically with"
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

EXP-285 — fix `handleCourseSubmit` TOCTOU race; wrap `findUnique` + `update` in `$transaction`; must fix atomically with EXP-278 to prevent race becoming exploitable once the approval-status guard lands

**Source:** [[Raw/sources/2026-06-02-experts-agent-digest.md]]
