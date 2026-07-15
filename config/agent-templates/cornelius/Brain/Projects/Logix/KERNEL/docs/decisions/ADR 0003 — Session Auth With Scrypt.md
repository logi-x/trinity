---
title: "ADR 0003 — Session Auth With Scrypt"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/adr"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
source_id: "docs/adr/0003-session-auth-scrypt.md"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# ADR 0003: Session Auth With Scrypt

## Status

Accepted.

## Context

The command center needs revocable browser sessions, portal users, internal roles, and no long-lived bearer tokens in logs.

## Decision

Use scrypt password hashes and opaque random session tokens stored only as SHA-256 token hashes. The browser stores `logix_session` as an httpOnly sameSite cookie.

## Consequences

Sessions can be revoked and audited. Each authenticated request performs a database session lookup, which is acceptable for Phase 1.
