---
title: "Experts Creator Loading Flicker"
date: "2026-05-09"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts creator loading flicker

Date: 2026-05-09
Project: Experts

## Summary

Reduced repeated loading flicker in the creator shell and nested creator pages.

## Root causes

- `AuthProvider.loading` included profile refresh state. Every profile refetch made creator chrome and auth-gated page queries think auth was loading again.
- `CreatorSidebarShell` rendered a full-page `CreatorLoader` while reading persisted sidebar state from localStorage, unmounting the whole creator shell on initial client render.
- The creator course enrollments page returned `CreatorLoader` directly before `CreatorLayout`, so it dropped creator chrome during auth loading/redirect windows.

## Fix

- `useAuth().loading` now tracks session initialization only; profile refresh is exposed separately as `profileLoading`.
- `CreatorSidebarShell` renders immediately and reads stored sidebar state in a layout effect without a full shell replacement.
- Creator page-level loading now uses an internal content loader that keeps navbar/sidebar mounted.
- Creator course enrollments loading now goes through `CreatorLayout.loading` instead of returning `CreatorLoader`.

## Verification

- `pnpm exec prettier --write app/(i18n)/_shared/creator/courses/enrollments/page.tsx src/lib/auth-context.tsx src/components/creator/creator-sidebar-shell.tsx`
- `pnpm typecheck:touched -- src/lib/auth-context.tsx src/components/creator/creator-sidebar-shell.tsx app/(i18n)/_shared/creator/courses/enrollments/page.tsx src/hooks/use-api-query.ts src/components/creator/creator-navbar.tsx src/components/creator/creator-layout.tsx`
- `npx gitnexus detect-changes -r experts`

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
