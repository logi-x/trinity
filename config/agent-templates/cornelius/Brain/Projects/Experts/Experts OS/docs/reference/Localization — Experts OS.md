---
title: "Localization — Experts OS"
date: "2026-04-11"
tags: ["project/experts", "project/experts-os", "tech/swift", "topic/api", "topic/i18n", "topic/networking", "topic/next-intl", "topic/place-global-audience", "topic/rtl"]
category: "Projects/Experts/Experts OS"
type: "reference"
updated: "2026-07-15"
---

# Localization — Experts OS

[[LocaleStore]] controls **language** and **layout direction** for [[Entities/Projects/Experts OS]].

#experts-os/i18n #topic/rtl #place/global-audience #topic/next-intl #topic/swift #topic/i18n

## Supported languages (`AppLanguage`)

- **English** (`en`)
- **Arabic** (`ar`) — **RTL** (`layoutDirection` right-to-left)
- **Spanish** (`es`)

## Behavior

- Persisted in UserDefaults (`experts.language`).
- `environment(\.locale)` and `environment(\.layoutDirection)` set from [[LocaleStore]] in `ExpertsApp`.
- API requests send `Accept-Language` from current locale (see [[APIClient]]).

## Strings

- Swift `String(localized:)` keys (e.g. `tab.home`, `environment.local`).

## See also

- [[Entities/Projects/Experts OS#Experts platform|Experts platform]] (web uses next-intl; concepts align)
- [[Saudi Arabia]] — primary market context

## Links

- [[Entities/Places/Saudi Arabia]]
- [[Entities/Projects/Experts OS]]
