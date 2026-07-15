---
title: "EXP-106 — [spinoff: EXP-82] Wire storage warning/limit notification emails"
date: "2026-05-24"
status: resolved
resolution: "PR #461: wired StorageWarningNotification (80% threshold) and StorageLimitNotification (100% threshold) into the notification dispatcher. Both fire from the post-upload quota check hook."
tags: [bug, storage, notifications, email, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-106"
fingerprint: "agent-fp:R5-exp82-wire-notifications-001"
---

## Summary

`StorageWarningNotification` and `StorageLimitNotification` email templates existed but were never wired into the notification dispatcher. Users would hit storage limits without any email warning.

## Root cause

EXP-82 created the notification template classes but the dispatch calls were omitted. The templates were in scope for the admin dashboard PR but the triggering logic was not implemented.

## Agent fingerprint

`<!-- agent-fp:R5-exp82-wire-notifications-001 -->`

## Status

Resolved — PR #461 merged 2026-05-24.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
