---
title: "Networking and API — Experts OS"
date: "2026-04-11"
tags: ["project/experts", "project/experts-os", "topic/api", "topic/auth", "topic/backend-rest", "topic/community", "topic/networking", "topic/urlsession"]
category: "Projects/Experts/Experts OS"
type: "reference"
updated: "2026-07-15"
---

# Networking and API — Experts OS

How [[Entities/Projects/Experts OS]] talks to [[Entities/Projects/Experts OS#experts-app|experts-app]] over **HTTPS** (or **HTTP** for [[local development]]).

#experts-os/networking #topic/urlsession #backend/rest #topic/community #topic/auth

## Client stack

- [[APIClient]] — builds `URLRequest`, sets `Accept`, `Accept-Language`, optional `Authorization: Bearer`, 30s timeout, parses success 2xx, maps errors.
- [[APIEndpoint]] — path segments under `/api/v1/...` plus query items (pagination, filters, locale).
- [[ExpertsAPI]] — app-specific facade: `fetchHome()`, `fetchCourses`, `fetchEvents`, `fetchCommunityPosts`, profile, native auth.

## Endpoints (representative)

| Area            | Path                                       | Role                  |
| --------------- | ------------------------------------------ | --------------------- |
| Stats           | `/api/v1/content/stats`                    | Home headline numbers |
| Courses         | `/api/v1/courses`                          | List + filters        |
| Course detail   | `/api/v1/courses/:id`                      | Detail                |
| Events          | `/api/v1/events`                           | List                  |
| Event detail    | `/api/v1/events/:id`                       | Detail                |
| Community       | `/api/v1/community/posts`                  | List                  |
| Post detail     | `/api/v1/community/posts/:id`              | Detail                |
| Profile         | `/api/v1/user/profile`                     | Authenticated user    |
| Native login    | `POST /api/v1/auth/native/login`           | Email/password        |
| Native register | `POST /api/v1/auth/native/register`        | Sign up               |
| Forgot password | `POST /api/v1/auth/native/forgot-password` | Request reset         |

Locale is passed via query or headers where implemented (`Accept-Language` uses [[LocaleStore]]’s locale identifier).

## See also

- [[Environments and tooling — Experts OS]]
- [[Authentication and session — Experts OS]]

## Links

- [[Entities/Projects/Experts OS]]
