---
title: "Freshness Dashboard"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["dashboard", "freshness", "meta"]
category: "wiki/dashboard"
source: "generated"
source_id: "Wiki/Freshness.md"
---

# Freshness Dashboard

High-value pages where staleness matters.

| Page | Freshness | Verified | Source of truth | Verify with |
| ---- | --------- | -------- | --------------- | ----------- |
| [[Entities/Projects/Experts App]] | volatile | 2026-06-11 | `/home/logix/experts` | git log, GitHub issues/PRs, Linear |
| [[Entities/Projects/Experts]] | volatile | 2026-06-11 | `/home/logix/experts` | git log, GitHub issues/PRs, Linear |
| [[Entities/Projects/Experts OS]] | volatile | 2026-06-11 | `/home/logix/experts` | git log, GitHub issues/PRs |
| [[Entities/Projects/Logix Kernel]] | volatile | 2026-07-05 | `/home/logix/logix-kernel` | git log, local repo |
| [[Actions/Action-Tracker]] | live | 2026-07-15 | `Actions/` and issue trackers | vault lint, GitHub/Linear when available |
| [[Decisions/Decision-Log]] | slow | 2026-07-15 | `Decisions/` | review dated decision notes |

When answering current-state questions from any volatile or live page, follow [[Tools/Ops/verify-current]].

