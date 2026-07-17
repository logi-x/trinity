---
title: Experts — Migration Drift Recovery + Asset Column Reorder + Squash (19 May 2026)
date: 2026-05-19
tags: [project/experts-app, session, prisma, migration, drift, squash, postgres, refactor, attachments, courses, project/experts]
related:
  - "[[Wiki/Concepts/Prisma]]"
  - "[[Wiki/Concepts/Postgres]]"
  - "[[Raw/sources/2026-05-18-experts-schema-naming-and-asset-xor]]"
  - "[[Raw/sources/2026-05-19-experts-uploads-tree-course-scoped]]"
---

# Migration Drift Recovery + Asset Column Reorder + Squash

Fourth in the schema-cleanup arc that started 18 May. Three connected fixes on the local dev DB (`experts` on `experts-dev-postgres`), all data-preserving — no `migrate reset`:

1. Recovered from "migration was modified after applied" drift caused by working-tree edits to three already-applied migration files.
2. Reordered columns on all five `*_assets` tables to a canonical shape (cosmetic; Postgres can't reorder in place).
3. Squashed the entire post-cutoff migration history (29 files → 1) using a **data-preserving concatenation** instead of `prisma migrate diff --script` (which would have rewritten table renames as destructive DROP/CREATE).

## Final state

- 6 migrations remain locally: 5 cutoff-era + 1 squash.
- Cutoff: `20251219011056_add_affiliate_referral_stats` (last Dec 2025 migration kept).
- Squash file: `apps/experts-app/prisma/migrations/20260519040000_squash_after_affiliate_referral_stats/migration.sql` (~108 KB, 29 historical migrations concatenated).
- `prisma migrate status` → `Database schema is up to date`.
- `pnpm db:migrate` → `Already in sync`.
- All `*_assets` row counts preserved (course: 14, lesson: 6, module: 1, quiz_question: 1, exam_question: 1).
- All FKs, indexes, check constraints restored by original name.

## Canonical column order for *_assets tables

```
id, <scope_id>, attachment_id, title, position, kind, role?, url,
is_downloadable, created_at, updated_at
```

`course_assets` has no `role`. All five tables now share this layout in both Postgres and `schema.prisma`. Column order is cosmetic (doesn't change query semantics) but normalizes future DDL and diffs.

## Gotchas captured

### Drift recovery without reset (working-tree edits to applied files)

If `prisma migrate dev` reports "migration was modified after applied" + drift, and you DID NOT actually run a new migration since, the dev DB is fine — the files just drifted from what was applied. Compare each modified file's current sha256 against the `checksum` column in `public._prisma_migrations`. If the **`HEAD` version** matches the recorded checksum, the fix is `git checkout HEAD -- <files>` (or equivalent restore) — no DB changes, no reset.

```
node -e "console.log(require('crypto').createHash('sha256').update(require('fs').readFileSync('<file>')).digest('hex'))"
```

vs:

```sql
SELECT checksum FROM _prisma_migrations WHERE migration_name = '...';
```

### `BEGIN;`/`COMMIT;` inside Prisma migrations can drop the bookkeeping row

A migration whose SQL contains explicit `BEGIN; ... COMMIT;` can apply its DML successfully but leave the `_prisma_migrations` row uninserted — Prisma's outer transaction confuses with the inner explicit commit. Symptom on the *next* `migrate dev`: drift detected, because the shadow replays only recorded migrations (which exclude yours) and diffs against your actual DB.

Recovery: `prisma migrate resolve --applied <migration_name>`. No DB touch needed.

This *can* happen even though other migrations in the same project (`schema_naming_refactor`, `course_asset_xor_inline`) used `BEGIN;`/`COMMIT;` successfully — it's intermittent and not worth debugging deeply.

**Rule:** don't put explicit `BEGIN;`/`COMMIT;` inside Prisma migration SQL. Prisma wraps it for you.

### Postgres can't reorder columns in place

`ALTER TABLE ... ALTER COLUMN ... SET POSITION` doesn't exist. The pattern:

```sql
CREATE TABLE x_new (...desired order...);
INSERT INTO x_new (...cols...) SELECT ...cols... FROM x;
DROP TABLE x;
ALTER TABLE x_new RENAME TO x;
-- restore PK, FKs, checks, indexes by their ORIGINAL names
```

Inbound FKs to `x` must be checked first (`SELECT confrelid::regclass, conname FROM pg_constraint WHERE confrelid='x'::regclass`); if any exist they'd be lost by `DROP TABLE` and must be restored. The four `*_assets` tables had none (verified).

### `prisma migrate diff --script` is destructive for renames

For a squash that must preserve data, `prisma migrate diff --from-migrations <cutoff-set> --to-schema schema.prisma --script` is **not safe**. Diff doesn't understand renames — it produces `DROP TABLE old` + `CREATE TABLE new`, losing all rows. Confirmed against this repo: the auto-generated diff wanted to `DROP TABLE assets`, `DROP TABLE event_agenda`, `DROP TABLE event_location`, `DROP TABLE privacy` — every one of those was actually a rename in the source migration that diff couldn't see.

**Data-preserving squash workflow:** concatenate the original post-cutoff `migration.sql` files in chronological order into one squash file, preserving the original rename/backfill SQL. Then verify equivalence:

```bash
prisma migrate diff \
  --from-migrations <cutoff-set + new squash dir> \
  --to-schema prisma/schema.prisma \
  --exit-code
# expect: "No difference detected."
```

Only after that, delete the superseded folders and `DELETE FROM _prisma_migrations WHERE migration_name > '<cutoff>'`, then `prisma migrate resolve --applied <squash>`.

### Prisma CLI in this repo doesn't accept `--shadow-database-url` on `migrate diff`

The flag exists in docs but this Prisma version reads shadow URL only from `prisma.config.ts`. Use `--to-schema` (not the docs' `--to-schema-datamodel`).

### Node 20 + corepack breaks pnpm against the repo's Prisma

`pnpm db:migrate` fails with `ERR_VM_DYNAMIC_IMPORT_CALLBACK_MISSING` under Node 20. Running with Node 24 in PATH succeeds:

```bash
PATH="$HOME/.nvm/versions/node/v24.11.1/bin:$PATH" pnpm db:migrate
```

Already mentioned in repo `AGENTS.md`; capturing here so future drift-recovery sessions don't waste time on it.

## Prod/staging rollout plan (proposed by user, not yet executed)

For env reset post-squash, user plan is `pg_restore --clean --if-exists` from a fresh staging dump:

```bash
docker exec -i experts-dev-postgres pg_restore \
  --clean --if-exists \
  -U experts -d experts \
  < experts-stg-2026-05-XX.dump
```

Constraint: the dump must be taken **after** the squash is applied somewhere (staging) so that `_prisma_migrations` in the dump reflects the new history. Otherwise prod restores to old history and the squash row would need to be `prisma migrate resolve --applied`'d manually.

Standard restore caveats apply (downtime window, writes lost between dump and restore).

## Files touched this session

| File                                                                                                | Change                                                                          |
| --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `apps/experts-app/prisma/schema.prisma`                                                             | Asset model field order normalized to canonical; `CourseModuleAsset.isDownloadable` default `false` → `true` |
| `apps/experts-app/prisma/migrations/20260519030000_reorder_course_module_assets_columns/`           | New migration (now part of squash)                                              |
| `apps/experts-app/prisma/migrations/20260519033000_reorder_remaining_course_asset_columns/`         | New migration (now part of squash)                                              |
| `apps/experts-app/prisma/migrations/20260519040000_squash_after_affiliate_referral_stats/`          | New squash containing all 29 post-cutoff migrations                             |
| `apps/experts-app/prisma/migrations/<29 post-cutoff folders>`                                       | Deleted (rolled into squash)                                                    |

## Pending

- [x] Take fresh staging dump **after** squashing staging the same way.
- [x] Drop + `pg_restore` prod from that dump.
- [x] If any other dev has a local DB on the old history, they need the same squash treatment or a dump-restore.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
