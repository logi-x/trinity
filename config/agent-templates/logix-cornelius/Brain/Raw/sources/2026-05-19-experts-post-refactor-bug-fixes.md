---
title: Experts — Post-Refactor Bug-Fix Sweep + CRUD Rebuild (19 May 2026)
date: 2026-05-19
tags: [project/experts-app, session, refactor, bugfix, uploads, lessons, i18n, tooling, project/experts]
related:
  - "[[Raw/sources/2026-05-18-experts-schema-naming-and-asset-xor]]"
  - "[[Raw/sources/2026-05-19-experts-uploads-tree-course-scoped]]"
  - "[[Raw/sources/2026-05-19-experts-migration-drift-recovery-and-squash]]"
  - "[[Wiki/Concepts/Prisma]]"
---

# Post-Refactor Bug-Fix Sweep

The Courses-domain `course_*` rename + asset XOR + course-scoped upload tree refactors landed on `main` via PRs **#331** (schema) and **#333** (uploads). This session collected the bugs that surfaced during manual browser testing, the gaps the refactor exposed, and the tooling fix that prevented those gaps from being caught earlier.

Branch: `fix/lesson-assets-endpoint-20260519`. Five commits, all gates clean (FORMAT/LINT/real-TSC), 1042/1042 unit tests passing.

## Shipped (branch, unpushed)

| Commit     | Scope                                                                                                   |
| ---------- | ------------------------------------------------------------------------------------------------------- |
| `9a402ffc` | Rebuild lesson-assets CRUD endpoint after `lesson_resources` drop                                       |
| `6b0069bb` | (user) Add `key` to FileRecord-shaped local types in lesson mapper                                      |
| `1b70ed08` | 12 handler tests + lesson mapper now uses the shared `synthesizeLessonResourceDTO` helper               |
| `a5c5a8b9` | Make `pnpm typecheck` actually run `tsc`, not `eslint .`                                                |
| `f1db30e1` | i18n sweep `lesson resource` → `lesson asset`; refresh `upload-public-asset.command.test.ts` fixtures   |

Additionally, **`1d3e5a5a`** landed directly on `main` earlier in the day: mappers emit the direct CDN URL (`R2_PUBLIC_URL + file.key`) for attachment-backed assets instead of `/api/v1/attachments/<id>/content`.

## Bugs surfaced + how

### 1. Lesson resource panel hitting dead route → 404 on every add

User reported `Failed to add resource` with `POST /api/v1/courses/.../lessons/.../resources` returning 404.

Root cause: commit `22d80ee1` (drop `lesson_resources`) removed the entire `.../resources` route tree along with its handlers and commands, but **did not update `lesson-resource-panel.tsx`**, which kept calling the dead endpoint. The course-scoped upload-tree refactor on top of that made the failure mode louder (no fallback path).

Fix: rebuilt the CRUD surface at `/api/v1/creator/courses/:id/modules/:mid/lessons/:lid/lesson-assets` (POST/GET/DELETE), mirroring the `module-assets` pattern. Panel repointed; `LessonResourceType` (`"link"|"file"`) translated to `CourseAssetKind` at the JSON boundary so the panel can stay ignorant of the broader enum.

### 2. Attachment-backed assets showed API content URL instead of CDN URL

User saw `/api/v1/attachments/<id>/content` in DTOs instead of `https://cdn.experts.com.sa/uploads/.../<file>`. The `/api/v1/attachments/[id]/content` route exists for auth-gated streaming, but course assets are uploaded `isPublic=true` and served public — routing them through the app added a needless hop.

Fix: new `buildAttachmentCdnUrl(file: {key})` helper next to `buildAttachmentContentUrl(attachmentId)`. Mappers branch on `row.attachment` (full record, has `file.key`) and emit `${R2_PUBLIC_URL}/${file.key}` directly. The content-URL helper stays for any auth-gated surfaces.

### 3. `pnpm typecheck` was secretly ESLint

The `FileRecord.key` structural mismatch between the helper file and `lesson.mapper.ts`'s local `LessonAssetRecord` slipped through "tsc clean" claims. Discovered the root cause: `apps/experts-app/package.json` had `"typecheck": "eslint ."`, and the `check` orchestrator (FORMAT/LINT/TYPECHECK) used `pnpm typecheck`, so the gate was running ESLint twice and never `tsc`.

Fix: swapped `typecheck` to `tsc -p tsconfig.json --noEmit`, dropped the redundant `typecheck:tsc`. Verified with a deliberate `const x: number = "y"` canary in `src/` — gate now exits 2 with `TS2322`.

## Patterns worth keeping

### Auth + path/URL builder share the same DB traversal — fold them

The `authorizeDomainAccess` function in the upload route was already navigating the entity hierarchy (lesson → module → course) to verify ownership. Adding a `select` for ancestor IDs in the same query — and returning a built `pathPrefix` string from the auth result — beats a separate path-resolution pass. Zero extra DB roundtrips, path-building logic lives where the entity hierarchy is already known. Applies anywhere an authorization check and a hierarchical key/URL share ancestry.

### Synthesize-DTO helper as single source of truth across mapper + endpoints

When a UI consumer reads the same shape from both an embedded relation (`lesson.resources` synthesized by the lesson mapper) and a dedicated endpoint (`GET /lesson-assets`), extract the shape-builder into a shared helper. Both call sites import it. The new endpoint can't drift from what the curriculum tree returns, and the panel never sees two flavours of the same object. `synthesizeLessonResourceDTO(asset, mapped)` does this for lesson assets.

### "What does `pnpm typecheck` actually run?" — audit, don't trust

Aliased scripts can lie about what they do. If a TYPECHECK gate is passing while structural type errors slip through, check `package.json` — the script might be running ESLint or a custom partial checker, not full `tsc`. A canary type error (`const x: number = "string"`) takes 5 seconds to confirm the gate has teeth.

## Pattern *not* to repeat: the dropped-endpoint lag

When a refactor deletes a route tree, the client(s) calling it must be updated in the **same** commit or the same PR. Commit `22d80ee1` deleted the lesson-resources route + handlers cleanly but left the panel client pointing at the dead URL. Result: a latent 404 that only surfaced on browser smoke test, several days later, after multiple subsequent commits had moved on. **Rule for future drops:** grep for callers of the deleted URL pattern (or symbol) and either update or delete them in the same diff.

## Pending

- [ ] Push `fix/lesson-assets-endpoint-20260519` to origin, open PR (awaiting explicit "push now")
- [ ] Out-of-band R2 file move/delete for old `uploads/{course-assets,module-assets,lesson-content,quiz,quiz-questions,exam-questions}/...` keys (separate operational task; due 2026-05-25)
- [ ] `npx gitnexus analyze` — index stale at `a5c5a8b`; hooks are warning on every commit
- [ ] Manual browser smoke test of remaining asset flows (only the lesson-resource panel was retested this session)

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
