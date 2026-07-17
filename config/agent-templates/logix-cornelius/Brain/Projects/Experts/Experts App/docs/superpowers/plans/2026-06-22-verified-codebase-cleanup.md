---
title: "2026 06 22 verified codebase cleanup"
date: "2026-06-22"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/plans/2026-06-22-verified-codebase-cleanup.md"
---
# Verified Codebase Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to execute this plan.

**Goal:** Remove only code proven to be unused or redundant, reduce low-risk duplication, and leave risky domain symmetry intact unless tests prove a safe shared abstraction.

**Architecture:** Work in small verification-gated waves. Before changing any symbol, run GitNexus upstream impact analysis and inspect its context. After each wave, run scoped checks. Before committing, compare changed symbols and execution flows against `main` with GitNexus `detect_changes`.

**Tech Stack:** Next.js, React, TypeScript, pnpm, Vitest, Prisma, Knip, jscpd, GitNexus.

## Baseline

The untouched `origin/main` baseline at `627c00d6a` currently has:

- Passing lint and TypeScript checks.
- A formatting failure in three test files:
    - `apps/experts-app/src/modules/billing/pdf/handlers/__tests__/pdf-result.handler.test.ts`
    - `apps/experts-app/src/modules/billing/pdf/notifications/__tests__/send-purchase-invoice-email.test.ts`
    - `apps/experts-app/src/notifications/__tests__/notification.service.test.ts`
- Passing test suite: 435 test files passed, 2 skipped; 3,223 tests passed, 14 skipped, and 5 todo.

These failures must be treated as the documented baseline, not attributed to cleanup changes.

## Task 1: Remove exact duplicate and unreferenced component files

**Candidate files:**

- `apps/experts-app/src/lib/events/detail/sections/event-detail-dates copy.tsx`
- `apps/experts-app/app/(i18n)/_shared/admin/(dashboard)/(sections)/OperationsPanel.tsx`
- `apps/experts-app/app/(i18n)/_shared/admin/(dashboard)/(sections)/OverviewCards.tsx`
- `apps/experts-app/app/(i18n)/_shared/courses/[id]/learn/sections/progress-card.tsx`
- `apps/experts-app/app/(i18n)/_shared/creator/courses/[id]/curriculum/sections/curriculum-modules.tsx`

1. For every exported component in each file, run GitNexus `impact` with `direction: upstream`.
2. Stop and report before editing if any result is HIGH or CRITICAL risk.
3. Run GitNexus `context` for each component and confirm there are no callers or execution flows.
4. Search for dynamic imports, string references, and case-variant paths with `rg`.
5. Confirm `event-detail-dates copy.tsx` is byte-for-byte equivalent to `event-detail-dates.tsx`.
6. Delete only candidates with zero verified callers.
7. Run:

```bash
cd apps/experts-app
pnpm typecheck
pnpm test:unit
```

8. Commit the wave:

```bash
git add apps/experts-app
git commit -m "chore: remove verified unused components"
```

## Task 2: Remove behavior-neutral unused locals and imports

**Initial files to inspect:**

- `apps/experts-app/app/(i18n)/_shared/(content)/hashtag/[hashtag]/page.tsx`
- `apps/experts-app/app/(i18n)/_shared/admin/(dashboard)/(sections)/CategoriesPanel.tsx`
- `apps/experts-app/src/components/ui/expandable.tsx`
- `apps/experts-app/src/lib/community/mappers/post.mapper.ts`
- `apps/experts-app/src/lib/logger.ts`
- `apps/experts-app/src/lib/realtime/polling-transport.ts`
- `apps/experts-app/src/modules/billing/pdf/handlers/pdf-result.handler.ts`
- `apps/experts-app/src/modules/billing/pdf/pdf-orchestrator.ts`
- `apps/experts-app/src/modules/zatca/processor/zatca.processor.ts`
- `apps/experts-app/src/modules/zatca/reporting/report-to-zatca.ts`

1. Reproduce each candidate with:

```bash
cd apps/experts-app
pnpm exec tsc -p tsconfig.json --noEmit --noUnusedLocals --noUnusedParameters
```

2. Run GitNexus upstream impact and context on every function, method, or component to be edited.
3. Remove unused imports, destructured fields, locals, and parameters only when they do not preserve side effects or framework-required signatures.
4. Do not remove worker queue references solely because they are unread; retained references may control object lifetime.
5. Run touched-file type checking, then the closest unit test for each edited module:

```bash
pnpm typecheck:touched -- <edited-files>
pnpm test:unit
```

6. Commit the wave:

```bash
git add apps/experts-app
git commit -m "chore: remove behavior-neutral unused code"
```

## Task 3: Resolve redundant exports without breaking public imports

1. Review all 25 Knip duplicate-export findings.
2. For each duplicate export, identify every import path with GitNexus context and `rg`.
3. Select one canonical export path; update imports before removing aliases.
4. Do not remove framework entry-point exports or package-level compatibility exports without proving they are private.
5. Run:

```bash
cd apps/experts-app
pnpm typecheck
pnpm test:unit
```

6. Commit only if the wave produces meaningful simplification:

```bash
git add apps/experts-app
git commit -m "refactor: consolidate redundant internal exports"
```

## Task 4: Audit deprecated compatibility code

**Candidates:**

- `apps/experts-app/src/i18n/locale.ts`
- Deprecated Redis publish helpers in `apps/experts-app/src/lib/redis.ts`
- Deprecated methods in `apps/experts-app/src/lib/realtime/websocket-transport.ts`
- Deprecated aliases in `apps/experts-app/src/lib/certifications/commands/certification-submit.schema.ts`
- Legacy community like route compatibility.

1. Run GitNexus impact and context for each deprecated symbol.
2. Search application code, tests, scripts, API clients, and runtime string references.
3. Keep compatibility surfaces if external callers cannot be disproven.
4. Remove only symbols with no internal or documented external contract.
5. Add or update tests proving canonical replacements still work.
6. Run relevant unit and integration tests.
7. Commit:

```bash
git add apps/experts-app
git commit -m "chore: remove obsolete internal compatibility code"
```

## Task 5: Verify dependency findings

1. Treat Knip dependency output as candidates, not proof.
2. For every allegedly unused dependency, check:

```bash
rg -n "\"<package>\"|' <package>'|from ['\"]<package>['\"]|require\\(['\"]<package>['\"]\\)" .
pnpm why <package>
```

3. Check config files, scripts, dynamic imports, generated code, and peer-dependency requirements.
4. Remove only dependencies with no verified runtime, build, test, or tooling use.
5. Add `estree` explicitly if `eslint-rules/experts-ui.mjs` directly imports it and no existing package intentionally supplies it.
6. Reinstall and run:

```bash
pnpm install
pnpm experts:check
pnpm experts:test
```

7. Commit:

```bash
git add package.json pnpm-lock.yaml apps/experts-app/package.json
git commit -m "chore: align dependencies with verified usage"
```

## Task 6: Separate safe duplicate abstractions from intentional domain symmetry

1. Review jscpd clone groups in this order:
    - Share pages for courses, events, and posts.
    - Metadata builders.
    - Auth-page shells.
    - Worker bootstrap code.
2. For each group, run GitNexus impact/context on all participating symbols.
3. Extract shared code only when inputs, error behavior, authorization, and observability are equivalent.
4. Do not mechanically merge payment, refund, enrollment, exam/quiz, or course/event workflows. Their similarity may encode distinct business rules.
5. Put any non-trivial domain abstraction into a separate PR linked to issue `#1125`.

## Task 7: Final verification and pull request

1. Run GitNexus:

```text
detect_changes(scope: "compare", base_ref: "main")
```

2. Confirm only expected symbols and flows changed.
3. Run:

```bash
pnpm experts:check
pnpm experts:test
git diff --check
git status --short
```

4. Compare failures with the documented baseline and investigate every new failure.
5. Push `codex/chore-gh-1125-cleanup-audit`.
6. Open a focused PR linked to `#1125`, listing:
    - Proven removals.
    - Verification performed.
    - Baseline failures that predate the branch.
    - Deferred risky duplication groups and why they remain.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
