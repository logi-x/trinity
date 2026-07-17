---
title: "Prisma"
date: "2026-04-10"
updated: "2026-05-19"
tags: ["entity", "topic", "tech/prisma"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Prisma.md"
---

# Prisma

Prisma is the main database access layer in the Experts App. In this vault, linked conversations usually mean schema design, migrations, relation loading, query bugs, and keeping app behavior aligned with PostgreSQL reality.

## Where it matters most

- auth and account data
- enrollment, course, and event models
- billing and payment records
- admin reporting and filtered views

## Repeated conversation themes

- relation shape causing surprising query results
- schema changes that need both migration safety and product clarity
- overloading Prisma with business logic that belongs in modules
- debugging performance or data correctness issues that look like "Prisma bugs"

## Practical rule

Treat Prisma as the access layer, not the domain model. Business rules should remain readable even if the ORM changes.

## Durable gotchas (learned the hard way)

- **Renaming a Prisma model does NOT rename its backing Postgres enum type.** Add explicit `ALTER TYPE "Old" RENAME TO "New"` to the migration. Same for indexes and constraints carrying the old table name.
- **Within one migration: reference the new table name after a `RENAME TABLE`.** Later steps in the same migration file run against the renamed schema, not the original.
- **Always `ALTER COLUMN ... DROP NOT NULL` BEFORE backfilling NULLs** into a column you plan to relax. Otherwise migration aborts mid-transaction and Prisma marks it failed.
- **Recovering a failed-and-edited migration:** `pnpm prisma migrate resolve --rolled-back <name>` + manual `DELETE FROM _prisma_migrations WHERE migration_name = ...`, then re-apply. Editing an applied migration file directly is rejected.
- **tsc green after a schema rewrite is not safety** if your DTOs are hand-written and decoupled from Prisma types. Force DTOs to import generated Prisma types so the typechecker actually catches mismatches.
- **Relation field names are not model names.** Renaming model `Enrollment` → `CourseEnrollment` does NOT mean every `enrollment:` relation field becomes `courseEnrollment:`. Codemods that conflate the two will break mocks, includes, and selects silently.
- **Codemods must be idempotent.** Every pass must be safe to re-run on its own output (guard: skip if name already starts with the new token). Running a codemod twice should be a no-op, not a double-rename.
- **For polymorphic "asset" patterns, prefer flat XOR over wrapper rows.** Each scope table carries `(attachment_id, url)` directly with a CHECK constraint enforcing exactly one. Lets `Attachment` stay file-only (intrinsic identity) and per-context fields (`kind`, `isDownloadable`, `position`) live where they're actually used. See [[Raw/sources/2026-05-18-experts-schema-naming-and-asset-xor]].
- **Drift after editing applied migration files is recoverable without `migrate reset`.** Compare the current file's sha256 against the recorded `checksum` in `_prisma_migrations`. If `HEAD` matches, `git checkout HEAD -- <files>` restores history without touching the DB. See [[Raw/sources/2026-05-19-experts-migration-drift-recovery-and-squash]].
- **Do NOT put explicit `BEGIN;`/`COMMIT;` inside a Prisma migration `.sql`.** Prisma wraps in its own transaction; an inner explicit commit can leave the migration's bookkeeping row uninserted in `_prisma_migrations` even though the DML applies cleanly. Symptom on the next `migrate dev`: drift between shadow replay and actual DB. Recover with `prisma migrate resolve --applied <name>`.
- **Postgres can't reorder columns in place.** Recreate-and-swap is the pattern: `CREATE TABLE x_new (...desired order...); INSERT SELECT; DROP TABLE x; ALTER TABLE x_new RENAME TO x;` then restore PK/FKs/checks/indexes by **their original names**. Audit inbound FKs first (`SELECT … FROM pg_constraint WHERE confrelid='x'::regclass`) — they'd be lost by `DROP TABLE` and must be re-added.
- **`prisma migrate diff --script` is destructive for renames.** It cannot detect rename intent; it emits `DROP TABLE old` + `CREATE TABLE new`, deleting rows. For a data-preserving squash, **concatenate the original post-cutoff `migration.sql` files in order** into one squash file. Verify equivalence with `prisma migrate diff --from-migrations <cutoff-set + squash> --to-schema schema.prisma --exit-code` (expect "No difference detected"). Only then delete the old folders and update `_prisma_migrations`.
- **Squash workflow (data-preserving), end-to-end:** (1) pick cutoff, (2) concatenate post-cutoff SQL into one squash file, (3) verify with `migrate diff --exit-code`, (4) delete superseded folders, (5) `DELETE FROM _prisma_migrations WHERE migration_name > '<cutoff>'`, (6) `prisma migrate resolve --applied <squash>`, (7) confirm `migrate dev` is `Already in sync`. For other envs: take a fresh dump **after** the squash is on staging so `_prisma_migrations` in the dump reflects the new history; otherwise prod restore needs a manual `resolve --applied` afterward. See [[Raw/sources/2026-05-19-experts-migration-drift-recovery-and-squash]].

## Related

- [[Wiki/Concepts/Postgres]]
- [[Wiki/Concepts/APIs]]
- [[Projects/Experts/DEVELOPER_GUIDE]]
