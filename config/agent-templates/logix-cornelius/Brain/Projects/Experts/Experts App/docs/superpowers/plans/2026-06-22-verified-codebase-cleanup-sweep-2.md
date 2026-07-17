---
title: "2026 06 22 verified codebase cleanup sweep 2"
date: "2026-06-22"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/plans/2026-06-22-verified-codebase-cleanup-sweep-2.md"
---
# Verified Codebase Cleanup Sweep 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove a second set of code and exports proven to have no callers while avoiding high-blast-radius and product-sensitive refactors.

**Architecture:** Apply three independent cleanup waves: delete zero-caller components, remove zero-caller helpers/constants, then remove redundant default export aliases from LOW-risk components. Run GitNexus impact analysis before each edited symbol and compare the final diff against `main`.

**Tech Stack:** Next.js, React, TypeScript, pnpm, Vitest, Knip, jscpd, GitNexus.

---

### Task 1: Delete zero-caller error components

**Files:**

- Delete: `apps/experts-app/src/components/errors/error.tsx`
- Delete: `apps/experts-app/src/components/errors/user-not-found.tsx`
- Modify: `apps/experts-app/src/components/errors/index.ts`

- [ ] **Step 1: Confirm both components have zero callers**

Run GitNexus upstream impact analysis for `Error` and `UserNotFound`.

Expected: LOW risk, zero direct callers, zero affected processes.

- [ ] **Step 2: Confirm there are no dynamic or direct imports**

```bash
rg -n "components/errors/(error|user-not-found)|\b(UserNotFound)\b" apps/experts-app
```

Expected: definitions and barrel exports only.

- [ ] **Step 3: Delete both files and their barrel exports**

Remove:

```ts
export * from './error'
export * from './user-not-found'
```

- [ ] **Step 4: Run verification**

```bash
pnpm --dir apps/experts-app typecheck
pnpm --dir apps/experts-app test:unit
```

Expected: PASS.

### Task 2: Remove zero-caller helpers and redundant public exports

**Files:**

- Modify: `apps/experts-app/src/lib/logger.ts`
- Modify: `apps/experts-app/src/lib/community/includes/post.include.ts`
- Modify: `apps/experts-app/src/lib/notification-service.ts`
- Modify: `apps/experts-app/src/lib/categories/constants/categories.ts`
- Modify: `apps/experts-app/src/lib/user/address/commands/address-upsert.schema.ts`
- Modify: `apps/experts-app/src/lib/user/profile/commands/profile-update.schema.ts`

- [ ] **Step 1: Remove zero-caller implementations**

Delete:

- `logSection`
- `logSubsection`
- `logTable`
- `postBasicSelect`
- `getUnreadCount`
- `CATEGORY_SLUGS`

- [ ] **Step 2: Internalize schemas that remain implementation details**

Change:

```ts
export const AddressUpsertSchema = ...
export const GenderEnum = ...
```

to:

```ts
const AddressUpsertSchema = ...
const GenderEnum = ...
```

Keep their derived types and validators unchanged.

- [ ] **Step 3: Run verification**

```bash
pnpm --dir apps/experts-app typecheck
pnpm --dir apps/experts-app test:unit
```

Expected: PASS.

### Task 3: Remove redundant LOW-risk default export aliases

**Files:**

- Modify: `apps/experts-app/src/components/profile/activity-feed.tsx`
- Modify: `apps/experts-app/app/(i18n)/_shared/(home)/(sections)/hero-section.tsx`
- Modify: `apps/experts-app/src/components/affiliate/AffiliateLayout.tsx`
- Modify: `apps/experts-app/app/(i18n)/_shared/affiliate/(tabs)/commissions.tsx`
- Modify: `apps/experts-app/app/(i18n)/_shared/admin/payouts/_components/process-payout-dialog.tsx`
- Modify: `apps/experts-app/src/components/ui/slider-fill.tsx`

- [ ] **Step 1: Confirm callers use named imports**

Search each exact module path for default imports.

Expected: no default imports.

- [ ] **Step 2: Remove the redundant aliases**

Delete the trailing `export default <Component>;` statement from each file. Preserve the named component export.

- [ ] **Step 3: Run verification**

```bash
pnpm --dir apps/experts-app typecheck
pnpm --dir apps/experts-app test:unit
```

Expected: PASS.

### Task 4: Final audit and delivery

**Files:**

- Modify only if verification requires it.

- [ ] **Step 1: Re-run Knip and confirm targeted findings decrease**

```bash
pnpm dlx knip --directory apps/experts-app --reporter compact
```

- [ ] **Step 2: Run GitNexus change detection**

```text
detect_changes(scope: "compare", base_ref: "main")
```

Expected: only the targeted components/helpers and their direct flows.

- [ ] **Step 3: Run repository gates**

```bash
pnpm experts:check
pnpm experts:test
git diff --check
```

Expected: lint and typecheck pass, all active tests pass, and formatting differs from baseline only in the three pre-existing test files.

- [ ] **Step 4: Commit, push, and open the PR**

```bash
git commit -m "chore: remove more verified dead code" \
  -m "Co-Authored-By: Codex <codex@openai.com>"
git push -u origin codex/chore-gh-1129-cleanup-sweep-2:codex/chore-gh-1129-cleanup-sweep-2
```

Open a PR with `Closes #1129`.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
