---
title: "EXP-191 — add sliding-window rate limit to `GET /api/v1/internal/realtime/sync`; sized to the ~3s client poll cadence; p"
date: "2026-05-29"
owner: "Logix (Ahmed)"
due: "2026-06-12"
priority: "medium"
status: "open"
source: "[[Raw/sources/2026-05-29-experts-agent-digest.md]]"
tags: [action, project/experts]
category: "meta"
up: "[[Action-Tracker]]"
updated: "2026-07-15"
---

> ↑ [[Action-Tracker]]

EXP-191 — add sliding-window rate limit to `GET /api/v1/internal/realtime/sync`; sized to the ~3s client poll cadence; prevents enumeration / abuse burst. EXP-174 follow-up deferred from IDOR PR to avoid throttling normal sync.

**Source:** [[Raw/sources/2026-05-29-experts-agent-digest.md]]
