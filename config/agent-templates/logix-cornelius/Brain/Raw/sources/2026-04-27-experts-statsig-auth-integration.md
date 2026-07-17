---
title: "Experts Statsig Auth Integration"
date: "2026-04-27"
source: "codex-session"
project: "Experts"
tags: ["project/experts", "statsig", "analytics", "auth", "nextjs"]
---

## Summary

Integrated Statsig into `apps/experts-app` using the Next.js App Router provider tree.

## Decision

Statsig should live inside the existing client `Providers` tree, under NextAuth `SessionProvider`, so it can receive real session data without making the root layout server-auth dependent.

## Implementation Notes

- Added `app/my-statsig.tsx` as a client wrapper.
- Added `@statsig/react-bindings`, `@statsig/session-replay`, and `@statsig/web-analytics`.
- Statsig starts with an anonymous/loading user and updates through `useStatsigUser().updateUserAsync()` when `useSession()` resolves.
- Statsig user fields include `userID`, email, locale, username custom ID, roles, primary role, admin/instructor booleans, verification state, profile completion, and account provider.
- Full name is sent as a Statsig `privateAttributes` field rather than targeting metadata.

## Verification

- Touched-file typecheck passed for `app/my-statsig.tsx`, `app/providers.tsx`, and `app/layout.tsx`.
- Prettier check passed.
- Browser smoke test against `http://127.0.0.1:3025/en` returned 200, loaded Statsig, and showed no page errors.
- GitNexus detect-changes reported low risk and 0 affected processes.

## Follow-up Usage

- Wired `experts_home_hero_cta_test` into the homepage hero CTA label.
- Changed the homepage experiment unit type to `stableID` because homepage traffic includes anonymous visitors.
- Added explicit `customIDs.stableID` to the Statsig user object via `StableID.get(clientKey)`.
- Wired `experts_creator_dashboard_beta` into the authenticated creator dashboard. The enabled path renders the same dashboard with a visible `Statsig beta` chip so rollout behavior can be verified safely.

## 2026-05-07 Global Banner Flicker Fix

- `GlobalBanner` uses the `global_banner` dynamic config from Statsig.
- Do not fall back to disabled config during Statsig loading or user refresh after a ready config has been seen.
- Keep the last ready banner config in component state/ref so `updateUserAsync()` or client reloading does not make the banner disappear and reappear.
- A hydration mismatch on `/en` showed a PostHog script occupying the home JSON-LD script slot. The source was the raw `elu.dev` analytics script in `app/layout.tsx` running before hydration, so load it through `next/script` with `strategy="afterInteractive"`.

## 2026-05-12 Statsig Loading State Stabilization

- Apply the same stabilization to `useReadyGateValue`: cache the last ready gate result per gate/auth/user key and reuse it while Statsig is temporarily loading or syncing. This prevents gated UI like Ask AI from flickering false/true during `updateUserAsync()`.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
