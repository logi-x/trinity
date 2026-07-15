---
title: "Authentication and session — Experts OS"
date: "2026-04-11"
tags: ["project/experts", "project/experts-os", "topic/api", "topic/auth", "topic/design-system", "topic/gsd", "topic/networking", "topic/oauth", "topic/oauth-like-bearer", "topic/planning", "topic/storage", "topic/theme-trust-and-polish"]
category: "Projects/Experts/Experts OS"
type: "reference"
updated: "2026-07-15"
---

# Authentication and session — Experts OS

Native auth uses **Bearer tokens** returned from [[Entities/Projects/Experts OS#experts-app|experts-app]] native auth routes; [[SessionStore]] persists the token and drives UI state.

#experts-os/auth #topic/oauth-like-bearer #theme/trust-and-polish #topic/storage #topic/auth #topic/gsd #tech/oauth

## Session states

[[SessionStore]].`State`:

- **guest** — not signed in.
- **loading** — login, register, or profile refresh in flight.
- **authenticated** — token valid and profile loaded ([[UserProfile]]).
- **unavailable** — error path (e.g. profile endpoint missing, unexpected failure).

## Storage (current)

- Token in **UserDefaults** (`experts.native.authToken`). _Roadmap item_: migrate to **Keychain** for production hardening (see [[Roadmap — Experts OS]]).

## Flows

- **Login** — `login(using:email:password:)` → `POST /api/v1/auth/native/login` (see [[Networking and API — Experts OS]]) → persist token → authenticated with embedded profile from response.
- **Register** — `register(using:...)` → conflict **409** maps to localized “email taken”.
- **Restore on launch** — If token present, [[ContentView]] calls `refreshProfile` with [[ExpertsAPI]] + [[APIClient]] using stored token.
- **Sign out** — clears token and returns to guest.

## Auth UI

- [[AuthPresentationStore]] toggles full-screen [[AuthFlowView]] (login, register, forgot password screens).
- Entry from ProfileRootView when guest; successful auth dismisses cover.

## Known gaps

- Backend may not expose full parity for every auth screen; align with [[Roadmap — Experts OS]] and repo `.planning/STATE.md` when in doubt.

## See also

- [[Networking and API — Experts OS]]
- [[People — Experts OS]]

## Links

- [[Entities/Projects/Experts OS]]
