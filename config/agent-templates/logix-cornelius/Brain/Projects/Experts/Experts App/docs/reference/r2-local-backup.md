---
title: R2 Local Backup and Restore
date: 2026-07-11
status: active
tags:
  - experts
  - operations
  - r2
  - backup
  - disaster-recovery
category: docs/experts-reference
aliases:
  - R2 Backup
  - R2 Restore
  - R2 Local Snapshots
updated: "2026-07-15"
---

# R2 Local Backup and Restore

**Scope:** production object-storage recovery on the Experts VPS. Related: [[Projects/Experts/Experts App/docs|Experts App Docs]], [[Projects/Experts/Experts App/docs/reference/cdn-hardening|CDN & Edge Hardening]].

Cloudflare R2 is the authoritative store for user uploads, course media, certifications, and legally immutable ZATCA
invoices. R2 does not provide object versioning or undelete. The production host keeps local, dated copies of selected
R2 buckets so an accidental object deletion can be recovered without duplicating all data into an R2 `backups` bucket.

> [!warning] Recovery scope
> Local snapshots protect against logical R2 deletion and corruption. They are not disaster recovery: VPS loss,
> compromise, or disk failure can remove the only backup copy. Maintain and periodically test an off-host copy for
> irreplaceable invoices and certifications.

## Current Design

- `/home/logix/backups/r2-backup.sh` copies R2 objects to dated local snapshots at
  `/home/logix/backups/r2/<YYYY-MM-DD>/<bucket>/`.
- `/home/logix/backups/r2-restore.sh` restores one local snapshot to an R2 target bucket. It is dry-run by default.
- The default source buckets are `invoices` and `certifications`. Add `files` or `media` only after confirming the VPS
  disk and retention budget can hold their snapshots.
- `rclone copy` is used, never `rclone sync`; source-side deletion cannot delete a completed local snapshot.

The previous `experts-prd-r2-backup` Compose service and its R2-to-R2 `backups` bucket snapshots were retired. Docker
does not manage this backup job.

## Rclone Configuration

The production host stores the R2 remote at `/home/logix/.config/rclone/rclone.conf`. It must be readable only by the
`logix` user:

```bash
chmod 600 /home/logix/.config/rclone/rclone.conf
```

The R2 endpoint is the account root, not a bucket URL:

```ini
[r2]
type = s3
provider = Cloudflare
access_key_id = <R2_ACCESS_KEY_ID>
secret_access_key = <R2_SECRET_ACCESS_KEY>
endpoint = https://<ACCOUNT_ID>.r2.cloudflarestorage.com
region = auto
acl = private
```

Use an R2 token with read access to every bucket being backed up. Restoring needs write access to the target bucket;
prefer a separate, tightly scoped restore credential for that operation.

Verify the remote before scheduling backups:

```bash
RCLONE_CONFIG=/home/logix/.config/rclone/rclone.conf rclone listremotes
RCLONE_CONFIG=/home/logix/.config/rclone/rclone.conf /home/logix/backups/r2-backup.sh --dry-run
```

## Backup Operation

The backup script defaults to `invoices,certifications` and retains dated local snapshots for 14 days.

```bash
RCLONE_CONFIG=/home/logix/.config/rclone/rclone.conf \
R2_BACKUP_EXCLUDES='invoices/experts-dev/**' \
/home/logix/backups/r2-backup.sh --dry-run
```

`R2_BACKUP_EXCLUDES` accepts comma-separated bucket-qualified rclone patterns:

```text
invoices/experts-dev/**,media/tmp/**
```

To opt into additional buckets or adjust retention:

```bash
R2_BACKUP_BUCKETS='invoices,certifications,files' RETENTION_DAYS=7 \
  /home/logix/backups/r2-backup.sh
```

Daily cron for the `logix` user:

```cron
0 2 * * * /usr/bin/flock -n /home/logix/r2-backup.lock /bin/bash -lc "RCLONE_CONFIG=/home/logix/.config/rclone/rclone.conf R2_BACKUP_EXCLUDES='invoices/experts-dev/**' /home/logix/backups/r2-backup.sh" >> /home/logix/logs/r2-backup.log 2>&1
```

> [!note] Capacity planning
> Dated snapshots duplicate the selected source data. With 14-day retention, reserve roughly 14 times the current size
> of each selected bucket, plus VPS disk headroom.

## Restore Procedure

Never restore directly into a production bucket first. Start with a recovery bucket, verify the result, then make an
explicit in-place restore only when necessary.

```bash
# Preview: no R2 writes.
RCLONE_CONFIG=/home/logix/.config/rclone/rclone.conf \
  /home/logix/backups/r2-restore.sh \
  --date 2026-07-11 --bucket invoices --target invoices-recovery

# Restore to an isolated recovery bucket and verify every source object by size.
RCLONE_CONFIG=/home/logix/.config/rclone/rclone.conf \
  /home/logix/backups/r2-restore.sh \
  --date 2026-07-11 --bucket invoices --target invoices-recovery --apply --verify

# Restore in place only after verifying the recovery bucket.
RCLONE_CONFIG=/home/logix/.config/rclone/rclone.conf \
  /home/logix/backups/r2-restore.sh \
  --date 2026-07-11 --bucket invoices --target invoices --allow-in-place --apply
```

`rclone copy` never deletes destination objects, but it can overwrite a destination object when the local snapshot
differs. Keep the recovery bucket until the production restore is confirmed.

## Incident Checklist

1. Restore the latest known-good local snapshot into a recovery bucket.
2. Verify the recovery bucket before any in-place write.
3. Investigate Cloudflare Audit Logs, R2 token activity, CI/IaC activity, and shared credentials that could have deleted
   data.
4. Rotate credentials that may have been involved and record the incident alongside [[Projects/Experts/Experts App/docs/reference/cdn-hardening|edge and storage hardening]] work.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App Docs]]
