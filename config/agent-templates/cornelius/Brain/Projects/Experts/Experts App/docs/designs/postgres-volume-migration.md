---
title: "postgres volume migration"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/designs/postgres-volume-migration.md"
---
# Postgres persistent-volume migration runbook

## Why this exists

Until this change, the Postgres services in every environment had **no data volume** —
`PGDATA` lived in the container's ephemeral writable layer. Any recreate of the
container (image change, version upgrade, config edit, `docker compose down`, or a
`pull` + recreate) **destroyed the entire database**. Production survived only
because its container had never been recreated since the data was loaded.

This change adds a named volume per environment so the data lives on the host and
survives container recreation:

| Env              | Service                | Volume               |
| ---------------- | ---------------------- | -------------------- |
| production       | `experts-prd-postgres` | `experts-prd-pgdata` |
| staging          | `experts-stg-postgres` | `experts-stg-pgdata` |
| data (local/dev) | `experts-dev-postgres` | `experts-dev-pgdata` |

> ⚠️ **A volume is durability against container loss — it is NOT a backup.** It does
> not protect against disk failure, host loss, corruption, or `DROP TABLE`. Keep a
> separate `pg_dump`/WAL backup with offsite retention (mandatory for ZATCA records).

---

## ⛔ The trap

Mounting a fresh (empty) named volume at `/var/lib/postgresql/data` and recreating the
container makes Postgres **initialise a new EMPTY cluster**. The existing data — still
sitting in the old container's soon-to-be-deleted layer — is orphaned and lost.

So you **must extract the current data first** and load it into the new volume.
**Never deploy this to production with a blind `docker compose up -d`.**

---

## Production / data env: safe migration (run in a maintenance window)

Replace `<ENV>` with `production`, `<C>` with `experts-prd-postgres`, `<VOL>` with
`experts-prd-pgdata`, and `experts`/`experts` with your `POSTGRES_USER`/`POSTGRES_DB`.

```bash
cd docker/<ENV>

# 0. Announce maintenance / stop write traffic (scale app + workers to 0, or take
#    the app offline). The DB must be quiescent for a consistent dump.
docker compose stop experts-prd-app experts-prd-pdf-worker experts-prd-zatca-worker

# 1. VERIFIED logical backup of the CURRENT (ephemeral) cluster — to the host.
docker exec -t experts-prd-postgres pg_dumpall -U experts > /root/pg-backup-$(date +%F).sql
#    Sanity-check it is non-empty and ends with a complete dump:
tail -n 3 /root/pg-backup-*.sql        # expect "PostgreSQL database dump complete"
ls -lh /root/pg-backup-*.sql           # expect a sane size, not a few bytes

# 2. (Belt & suspenders) also copy the raw data dir out of the running container:
docker cp experts-prd-postgres:/var/lib/postgresql/data /root/pgdata-rawcopy-$(date +%F)

# 3. Pull the new compose (with the volume) and recreate ONLY postgres. The new
#    named volume is created empty → fresh cluster boots.
git pull
docker compose up -d --force-recreate experts-prd-postgres
docker compose exec experts-prd-postgres pg_isready -U experts   # wait for ready

# 4. Restore the dump into the now-persistent volume.
cat /root/pg-backup-$(date +%F).sql | docker compose exec -T experts-prd-postgres \
  psql -U experts -d postgres

# 5. VERIFY before resuming traffic — row counts on critical tables must match
#    pre-migration. Examples (adjust to your schema):
docker compose exec experts-prd-postgres psql -U experts -d experts -c \
  "SELECT 'users', count(*) FROM users
   UNION ALL SELECT 'invoices', count(*) FROM \"ZatcaInvoice\"
   UNION ALL SELECT 'posts', count(*) FROM \"Post\";"
#    Confirm the data dir now resolves to the host volume:
docker volume inspect experts-prd-pgdata --format '{{.Mountpoint}}'

# 6. Resume traffic.
docker compose start experts-prd-app experts-prd-pdf-worker experts-prd-zatca-worker

# 7. Keep /root/pg-backup-*.sql and the raw copy for a few days, then remove.
```

### Rollback

If verification (step 5) fails, do **not** resume traffic. Revert the compose change
(`git checkout` the previous docker-compose.yml), recreate postgres **without** the
volume to land back on the original ephemeral container — but note that recreating
already destroyed the original layer, so the authoritative source of truth is the
**backup from step 1/2**. This is why step 1 must be verified before step 3.

---

## Staging / data (disposable): no preservation needed

Staging and local-dev data is disposable. Just recreate — a fresh cluster is fine;
migrations + seed re-run on deploy.

```bash
cd docker/staging   # or docker/data
docker compose up -d --force-recreate experts-stg-postgres
# (re-run migrations/seed per your normal staging deploy flow)
```

---

## After the volume is in place

Only **after** every env has a persistent volume should the Postgres image be pinned
by digest (the pin forces a recreate; with the volume that recreate is now data-safe).
Track that as the follow-up to this change.

## Follow-ups worth doing

- **Real backups:** scheduled `pg_dump`/WAL archiving to offsite storage with retention
  (separate from the volume — the volume is not a backup).
- **Redis durability:** Redis here runs cache + BullMQ queues with no persistence. Job
  loss on recreate is usually tolerable, but decide explicitly if queues must survive.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
