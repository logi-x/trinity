---
title: "EXP-279 — **IMMEDIATE**: fix `.github/workflows/experts-app.yml` migration-immutability job to use `env:` block for `${{"
date: "2026-06-02"
owner: "Logix (Ahmed)"
due: "2026-06-03"
priority: "high"
status: "open"
source: "[[Raw/sources/2026-06-02-experts-agent-digest.md]]"
tags: [action, project/experts]
category: "meta"
up: "[[Action-Tracker]]"
updated: "2026-07-15"
---

> ↑ [[Action-Tracker]]

EXP-279 — **IMMEDIATE**: fix `.github/workflows/experts-app.yml` migration-immutability job to use `env:` block for `${{ github.base_ref }}` instead of direct shell interpolation; prevents CI runner command injection from crafted branch names

**Source:** [[Raw/sources/2026-06-02-experts-agent-digest.md]]
