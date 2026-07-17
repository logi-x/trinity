---
title: "Design system — Experts OS"
date: "2026-04-11"
tags: ["project/experts", "project/experts-os", "tech/ios", "tech/swift", "tech/swiftui", "topic/design-system", "topic/i18n"]
category: "Projects/Experts/Experts OS"
type: "reference"
updated: "2026-07-15"
---

# Design system — Experts OS

Visual language for [[Entities/Projects/Experts OS]]: **`ExpertsTheme`** static namespace (colors, radii, spacing, shadows) plus [[ThemeManager]] for light/dark.

#experts-os/design #topic/swift #topic/swiftui

## Colors (`ExpertsTheme.ColorPalette`)

- **Primary** blue `#2563EB`, **accent** `#3B82F6`, **pink** `#DB2777`, semantic success/warning.
- Light/dark **card**, **canvas**, **surface**, **border**, **text** pairs for **SwiftUI** `ColorScheme`.

## Shape

- Corner radii: card **18pt**, medium **12pt**, small **8pt**, pill **999**.

## Theme switching

- [[ThemeManager]] — `@StateObject` in `ExpertsApp`, `preferredColorScheme` on root.

## Parity

- Aim for **brand alignment** with [[Entities/Projects/Experts OS#experts-app|experts-app]] / web without pixel-perfect match on v1.

## See also

- [[Localization — Experts OS]]

## Links

- [[Entities/Projects/Experts OS]]
