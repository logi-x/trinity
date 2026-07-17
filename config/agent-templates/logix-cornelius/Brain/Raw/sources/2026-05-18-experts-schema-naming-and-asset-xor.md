---
title: Experts — Schema Naming Standardization + CourseAsset XOR Refactor (18 May 2026)
date: 2026-05-18
tags: [project/experts-app, session, prisma, schema, migration, refactor, attachments, courses, project/experts]
related:
  - "[[Wiki/Concepts/Prisma]]"
  - "[[Raw/guides/2026-05-18-schema-naming]]"
---

# Schema Naming + CourseAsset XOR Refactor

Single-session refactor on `refactor/schema-naming-course-prefix-20260518`. Two interlocking goals: apply the `course_*` bounded-context prefix across all Courses-domain tables, and kill CourseAsset's polymorphic-wrapper role in favor of flat XOR (attachmentId, url) on every scope_asset table.

## Shipped (branch, unpushed)

| Commit     | Scope                                                                                           |
| ---------- | ----------------------------------------------------------------------------------------------- |
| `a5c1dd51` | schema: `course_*` naming standardization + unified asset shape                                 |
| `10246a1b` | codemod: rewrite Prisma surface for renamed models (idempotent, multi-pass)                     |
| `22d80ee1` | curriculum: drop `lesson_resources`, consolidate on `course_lesson_assets`                      |
| `16fd1d8b` | quiz/exam: drop legacy `imageUrl`/`fileUrl` reads from question routes                          |
| `ed7e1f7a` | enrollments: restore correct DTO key after over-aggressive codemod                              |
| `c35af38e` | docker: PostgreSQL preflight command for schema naming refactor                                 |
| `fd8898e5` | migrate: rename Postgres enum types + drop columns from renamed `quiz_questions`                |
| `2ac09c6a` | asset: flatten CourseAsset wrapper, scope-asset XOR (attachmentId/url)                          |
| `f7b00771` | asset: rewrite mappers + writes for flat XOR shape                                              |
| `56c20ac8` | asset: finish flat XOR sweep — includes, handlers, seeders, UI                                  |
| `4e8c174c` | test: fix asset/enrollment/upload tests after refactor                                          |
| `cc61a3f9` | style: prettier whitespace cleanup on upload route test                                         |
| `e99f24ac` | schema: `course_quiz_options` → `course_quiz_question_options` (mirror exam structure)          |

Final state: tsc 0 errors, vitest 1030/1030 passing, prisma migrate status in sync (32 migrations including the trailing quiz-options rename).

## Key architectural decisions

### 1. Attachment is file-only; scope tables own usage

User reasoning, verbatim: *"Attachment should be the source of truth for the asset itself, not for how it behaves in each course/lesson/module/question."*

- `Attachment` + `File`: intrinsic file identity (mimeType, size, filename, ownership). No `isDownloadable`, no `kind`, no per-context behavior.
- Each `*_assets` table (`course_assets`, `course_lesson_assets`, `course_module_assets`, `course_quiz_question_assets`, `course_exam_question_assets`) carries `(attachment_id, url, kind, position, isDownloadable)` directly.
- Postgres CHECK constraint enforces `attachment_id XOR url` (exactly one populated).
- onDelete: `Restrict` on scope→attachment (don't orphan attachments referenced by lessons); `Cascade` on scope→parent.

### 2. CourseAsset is now a peer level, not a wrapper

Killed `isCourseLevel` flag. CourseAsset became its own scope alongside lesson/module/question. Stripped fields: `source`, `mimeType`, `size`, `isCourseLevel`. Added: `position`, `isDownloadable`. Source enum (`CourseAssetSource`) dropped — derivable from `(attachmentId, url)` presence.

### 3. Attachment.id gets default UUID

Added `@default(dbgenerated("gen_random_uuid()"))` to `Attachment.id`. Writes no longer need to mint UUIDs client-side.

### 4. `lesson_resources` deleted, not migrated

User instruction: *"drop all things related to lesson resources and keep only the new course lesson assets."* Mappers synthesize a legacy `LessonResourceDTO[]` from `role='resource'` lesson assets for UI back-compat only — no DB table.

## Gotchas captured

### Migration P3018 — NOT NULL on column being NULL'd

First apply of `20260518150000_course_asset_xor_inline` failed because `course_assets.url` was still `NOT NULL` when the migration tried to set it NULL for the one dirty row that had both `attachment_id` AND `url`. Fix: `ALTER COLUMN url DROP NOT NULL` BEFORE the UPDATE that NULLs dirty rows.

### "Migration was modified after applied"

After editing the failed migration, Prisma rejected it. Recovery: `pnpm prisma migrate resolve --rolled-back <name>` then manual `DELETE FROM _prisma_migrations WHERE migration_name = ...` then retry.

### Renamed tables in subsequent migration steps

A later migration tried `DROP COLUMN image_url` on `quiz_questions` — but the rename to `course_quiz_questions` had already executed earlier in the same migration. Always reference the new name after a rename within the same migration file.

### Postgres enum renames need explicit ALTER TYPE

Renaming a model in Prisma does not rename the Postgres enum type backing it. `ALTER TYPE "OldEnum" RENAME TO "NewEnum"` must be in the migration manually.

### tsc green ≠ runtime green when DTOs are hand-written

Initial 0-error tsc count after the schema rewrite was misleading — DTOs were decoupled from Prisma types. Rewriting the DTO surfaced 163 real errors that had been silently masked. **Rule:** when changing Prisma models, force DTOs to import Prisma types so the typechecker actually catches mismatches.

### Codemod triple-rename bug

Ran the codemod three times → `Privacy` → `PrivacySettings` → `PrivacySettingsSettings` → `PrivacySettingsSettingsSettings`. Fix: idempotency guard — skip if the name already starts with any NEW token. **Rule for codemods:** every pass must be safe to re-run on its own output.

### Codemod over-rename on relation fields

The codemod incorrectly renamed Prisma relation field names alongside model renames (e.g. `module:` → `courseModule:`, `enrollment:` → `courseEnrollment:`, `privacy:` → `privacySettings:`). The relation field name and the model name are different identifiers — relation fields are local to the parent model and don't follow the rename. Several test mocks and handler error strings had to be reverted manually.

### `frontend-developer` agent self-committed again

Pattern confirmed (already in memory). The sub-agent committed despite explicit "do NOT commit" briefing. Detected via `git log` post-return. Mitigation: brief defensively + always `git log` after sub-agent returns.

## Pending

- [ ] Push `refactor/schema-naming-course-prefix-20260518` to origin (awaiting explicit "push now")
- [ ] Open PR
- [ ] `npx gitnexus analyze` (index stale at `56c20ac8`)
- [ ] Manual browser smoke test: lesson assets, module assets, quiz/exam question assets, downloads
- [ ] i18n message keys still contain stale "lesson resource" strings (cosmetic followup)
- [ ] `upload-public-asset.command.test.ts` references dead `uploads/lesson-resources/` storage path (cosmetic)

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
