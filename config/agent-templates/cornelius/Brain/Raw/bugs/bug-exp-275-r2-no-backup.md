---
title: "EXP-275 — R2 has no automated backup/replication — object/bucket deletion is unrecoverable (no versioning)"
date: "2026-06-02"
status: open
resolution: unknown
tags: [bug, security, infrastructure, r2, backup, zatca, compliance, project/experts]
linear: "https://linear.app/experts/issue/EXP-275/infra-r2-has-no-automated-backupreplication-objectbucket-deletion-is"
fingerprint: "dad0348c3622"
---

## Summary

Cloudflare R2 is the authoritative store for user uploads, course media, certifications, and **legally-immutable ZATCA invoices**. R2 has no built-in object versioning or undelete. There is no automated backup script, no cross-region replication, and no disaster-recovery runbook. A single `DeleteObject`, lifecycle misconfiguration, leaked credential, or CI cleanup script is unrecoverable — including the ZATCA invoices which are legally required to be retained for 6 years under Saudi regulations.

## Root cause

`docker/production/docker-compose.yml` — no `r2-backup` or replication service defined. No `rclone copy` cron, no dated PITR prefix scheme, no restore script, no runbook.

Fix: implement `rclone copy` script with dated prefixes for PITR, a restore script, a cron service, and a runbook. Off-provider/retention is an operator follow-up.

## Agent fingerprint

`<!-- agent-fp: dad0348c3622 -->`

## Status

`open` — Backlog (High). ZATCA legal exposure. R3-shippable for the rclone script + cron service; off-provider/retention is operator-gated.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
