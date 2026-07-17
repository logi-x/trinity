---
title: "Architecture — Experts OS"
date: "2026-04-11"
tags: ["project/experts", "project/experts-os", "tech/ios", "tech/nextjs", "tech/swift", "tech/swiftui", "topic/api", "topic/async-await", "topic/auth", "topic/design-system", "topic/navigation", "topic/networking"]
category: "Projects/Experts/Experts OS"
type: "architecture"
updated: "2026-07-15"
---

# Architecture — Experts OS

High-level structure of [[Entities/Projects/Experts OS]]: **SwiftUI** views, **`ObservableObject`** stores, and **async** networking against [[Entities/Projects/Experts OS#experts-app|experts-app]].

#experts-os/architecture #topic/swiftui #topic/async-await #topic/navigation #topic/swift #topic/auth #tech/next-js

## Layers

1. **App shell** — `ExpertsApp` wires global state ([[ThemeManager]], [[LocaleStore]], [[SessionStore]], [[AppEnvironmentStore]], [[AuthPresentationStore]]) into [[ContentView]].
2. **Navigation** — [[RootTabView]] hosts five tabs (see [[Features and navigation — Experts OS]]).
3. **Feature modules** — `Features/<Area>/` with `*RootView`, `*ViewModel`, detail views, and shared UI under `Features/Shared/`.
4. **Services** — [[ExpertsAPI]] composes high-level calls; [[APIClient]] performs HTTP with JSON encode/decode.
5. **Models** — `Models/*.swift` Codable types matching `/api/v1` payloads.

## State management

- Global session: [[SessionStore]] (`guest` | `loading` | `authenticated` | `unavailable`).
- Environment selection: [[AppEnvironmentStore]] (local / staging / production base URLs).
- Auth UI coordination: [[AuthPresentationStore]] (full-screen auth flow).

## Design choices

- **No** separate repository layer yet — view models call [[ExpertsAPI]] directly (acceptable for v1; extract if complexity grows).
- **JSONDecoder** with camelCase keys (`JSONDecoder.experts`).

## See also

- [[Networking and API — Experts OS]]
- [[Authentication and session — Experts OS]]
- Next.js (server counterpart)

## Links

- [[Entities/Projects/Experts OS]]
