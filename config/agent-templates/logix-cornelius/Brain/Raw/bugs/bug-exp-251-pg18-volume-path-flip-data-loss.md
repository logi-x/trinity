---
title: "EXP-251: pg18 volume-path flip + deleted migration guide — production data loss on next docker compose up"
linear_id: "EXP-251"
agent_fp: "a3c8e9b2041d"
date: "2026-06-01"
severity: "Critical"
status: "open"
resolution: "unknown"
tags: [bug, infra, docker, postgres, data-loss, project/experts]
category: "bug"
source: "automation"
---

# EXP-251: pg18 volume-path flip — production data loss on next deploy

**Linear:** [EXP-251](https://linear.app/experts/issue/EXP-251/urgent-docker-compose-yml-pg18-volume-path-flip-data-loss-on-next) | **Status:** Backlog

## Summary

PR #724 (`fix(docker): add persistent postgres volume + pg18 upgrade`) made two simultaneous changes to the Postgres service in `docker/production/docker-compose.yml`:

1. Added a named Docker volume `postgres_data` — **correct**.
2. Changed the volume mount target from `/var/lib/postgresql/data` to `/var/lib/postgresql` — **regression**.
3. Deleted `POSTGRES-VOLUME-MIGRATION.md` — removes the operator runbook for safe volume transitions.

## Impact

On the **next** `docker compose up` (or container recreate after image pull):

- Postgres starts with an empty data directory at `/var/lib/postgresql/data` inside the new volume.
- All existing database contents (users, courses, payments, ZATCA invoices, sessions) are **inaccessible** because the volume is either new or mounted at the wrong path.
- This is effectively a full database wipe from the application's perspective.

## Why This Happens

The Postgres image writes data to `/var/lib/postgresql/data` (the `PGDATA` default). Mounting a volume at `/var/lib/postgresql` (one level up) is valid but requires the data directory to already exist at that path from a previous run using the same mount. When a fresh named volume is introduced — as PR #724 does — Postgres initialises a new cluster at `/var/lib/postgresql/data` inside the empty volume, regardless of any data on the host's overlay filesystem.

## Files

- `docker/production/docker-compose.yml` — `services.postgres.volumes` (changed mount target)
- `POSTGRES-VOLUME-MIGRATION.md` — deleted in PR #724 (was: `docker/POSTGRES-VOLUME-MIGRATION.md`)

## Immediate Actions Required

1. **Block or revert PR #724** before next production deploy.
2. **Take a verified `pg_dump`** of the current production database immediately.
3. **Restore `POSTGRES-VOLUME-MIGRATION.md`** from the PR #715 tree.
4. **Re-sequence the change**: land the volume addition (with correct `/var/lib/postgresql/data` mount) as a separate validated PR; apply pg18 upgrade as a subsequent step only after volume migration is confirmed.

## Related

- PR #724 — introduced the regression
- PR #715 — prior infra PR (POSTGRES-VOLUME-MIGRATION.md last step)
- EXP-246 — original Postgres no-volume bug (resolved)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
