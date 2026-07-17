---
title: "Mobile Architecture Recommendationmd"
date: "2026-04-20"
tags: [plan, project/experts]
category: "plan"
---

# Mobile Architecture Recommendation for Experts

## Summary

Recommendation: continue **full native** for mobile, not Expo, with an **iOS-first rollout** and a later **native Android** build.

Why this fits the current repo and your stated constraints:

- `apps/experts-os` is already a real SwiftUI app, not a prototype. It has app shell, feature roots, typed networking, auth flow, localization, environment switching, and tests.
- `apps/experts-app` already exposes a versioned `api/v1` surface plus native auth endpoints, so mobile can consume stable backend contracts without sharing UI code.
- Your preferences point away from Expo: best iOS quality, strong native staffing, and early need for heavy native features. That combination removes Expo’s main advantage, which is faster delivery with a JS-heavy team.

## Key Changes / Direction

- Treat `apps/experts-app` as the **backend and mobile contract owner**, not as something to reuse for mobile UI.
- Treat `apps/experts-os` as the **production iOS app** and deepen that path instead of restarting in Expo.
- Plan **Android as a separate native app** once the iOS contract and feature set stabilize. Do not force a shared cross-platform UI layer just for symmetry.
- Use the current iOS app to prove:
  - mobile API coverage
  - auth/session flows
  - discovery/navigation patterns
  - mobile-specific gaps in payloads and endpoint ergonomics
- Only reconsider Expo if one of these changes materially:
  - the team becomes mostly TS/JS
  - Android parity becomes urgent before iOS stabilizes
  - the mobile scope shrinks to mostly thin CRUD/content surfaces

## Public APIs / Interfaces

The key architecture work is at the API-contract layer, not a new shared mobile framework:

- Keep `app/api/v1/...` as the mobile-facing contract.
- Keep and harden native auth routes already present:
  - `/api/v1/auth/native/login`
  - `/api/v1/auth/native/register`
  - `/api/v1/auth/native/forgot-password`
- Formalize mobile DTO stability for the surfaces already consumed in iOS:
  - home/content stats
  - courses
  - events
  - community posts
  - user profile
- Add contract discipline before Android starts:
  - avoid web-only response assumptions
  - document required fields for native clients
  - add tests for response-shape stability on mobile-consumed endpoints

## Test Plan

- Keep expanding native verification in `apps/experts-os` with focused Swift tests around:
  - decoding
  - session persistence
  - auth error handling
  - environment switching
- Add/keep backend route tests in `apps/experts-app` for all mobile-auth and mobile-consumed endpoints.
- Add a lightweight mobile contract checklist before Android work begins:
  - auth works on local/staging/production
  - core feeds decode without app-specific transforms
  - detail screens do not rely on web-only fields
  - localization and RTL data hold up on mobile payloads

## Assumptions

- Default chosen: **iOS first**, then **native Android**.
- Assumes you are willing to maintain two native clients once Android begins.
- Assumes the first mobile release will include meaningful platform-specific work, not just a wrapped content app.
- Assumes the web app remains the system of record for business logic and API delivery.

Net: for this repo and your constraints, **Expo would be a pivot away from existing momentum**, while **native builds on what you already have** and matches the product ambition better.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
