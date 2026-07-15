---
title: "SwiftUI"
date: "2026-04-11"
updated: "2026-04-13"
tags: ["entity", "topic", "swiftui", "ios", "design-system", "topic/swiftui", "platform-ios", "platform-macos"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/SwiftUI.md"
---

# SwiftUI

SwiftUI is the native UI framework behind Experts OS, the Apple client for Experts.

## Context in Experts OS

The native app is iPhone-first with shared macOS support in the same codebase. The vault's Experts OS hub describes SwiftUI as the presentation layer over the same product domains already served by the web app and `/api/v1/*` backend.

## Main concepts in this vault

- `ExpertsApp` as the app entry point
- `ContentView` and `RootTabView` as key composition points
- Environment-driven theme, locale, and session handling
- Native parity with web where it helps trust and product consistency

## Architectural stance

SwiftUI in this workspace is intentionally thin on business logic. The device renders and orchestrates client state, while the server remains authoritative for domain rules.

## Best entry points

- [[Projects/Experts/Experts OS/docs/reference/Glossary — Experts OS]]
- [[Projects/Experts/Experts OS/docs/Roadmap — Experts OS|Roadmap — Experts OS]]

## Related

- [[Wiki/Concepts/i18n]]
- [[Wiki/Concepts/Auth]]
