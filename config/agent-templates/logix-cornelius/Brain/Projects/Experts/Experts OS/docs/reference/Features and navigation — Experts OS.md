---
title: "Features and navigation — Experts OS"
date: "2026-04-11"
tags: ["project/experts", "project/experts-os", "topic/auth", "topic/community", "topic/design-system", "topic/navigation", "topic/theme-lms"]
category: "Projects/Experts/Experts OS"
type: "reference"
updated: "2026-07-15"
---

# Features and navigation — Experts OS

User-facing areas of [[Entities/Projects/Experts OS]], rooted in [[RootTabView]].

#experts-os/features #theme/lms #topic/navigation #topic/community #topic/auth

## Tabs (`AppTab`)

| Tab       | Root view           | ViewModel            | Focus                                                     |
| --------- | ------------------- | -------------------- | --------------------------------------------------------- |
| Home      | `HomeRootView`      | `HomeViewModel`      | Stats, featured courses, upcoming events, community posts |
| Courses   | `CoursesRootView`   | `CoursesViewModel`   | Browse, search, filters → `CourseDetailView`              |
| Events    | `EventsRootView`    | `EventsViewModel`    | List → `EventDetailView`                                  |
| Community | `CommunityRootView` | `CommunityViewModel` | Posts → `CommunityDetailView`                             |
| Profile   | `ProfileRootView`   | —                    | Account, settings, auth entry                             |

## Auth screens

- `AuthFlowView`, `AuthLandingView`, `LoginView`, `RegisterView`, `ForgotPasswordView` with shared components (`AuthPrimaryButton`, `AuthTextField`, …).

## Shared UI

- `Features/Shared/` — cards, loading/empty states, `AsyncRemoteImage`, section headers.

## See also

- [[Design system — Experts OS]]
- [[Home feed]] (conceptual aggregate)

## Links

- [[Entities/Projects/Experts OS]]
