---
title: "Environments and tooling — Experts OS"
date: "2026-04-11"
tags: ["project/experts", "project/experts-os", "tech/pnpm", "tech/xcode", "topic/api", "topic/auth", "topic/gsd", "topic/monorepo", "topic/networking", "topic/planning"]
category: "Projects/Experts/Experts OS"
type: "reference"
updated: "2026-07-15"
---

# Environments and tooling — Experts OS

How to point [[Entities/Projects/Experts OS]] at the right [[Entities/Projects/Experts OS#experts-app|experts-app]] instance and build in Xcode.

#experts-os/tooling #topic/xcode #topic/monorepo #topic/auth #topic/gsd #tech/pnpm

## `AppEnvironment`

Enum in code: **local**, **staging**, **production** ([[AppEnvironmentStore]]).

| Environment | Default base URL                                               |
| ----------- | -------------------------------------------------------------- |
| local       | `http://127.0.0.1:3025` (overridable string for custom LAN IP) |
| staging     | `https://app.stg.experts.com.sa`                               |
| production  | `https://app.experts.com.sa`                                   |

- Persisted: `experts.environment`, `experts.environment.localBaseURL`.

## Web dev server

- From monorepo root: `pnpm experts:dev` or `cd apps/experts-app && pnpm dev` — typically port **3025** ([[Entities/Projects/Experts OS#Experts monorepo|Experts monorepo]]).

## Xcode project

- Project: `apps/experts-os/Experts.xcodeproj`
- **Multiplatform**: iOS Simulator, device, and **macOS**
- **Bundle ID**: `sa.com.experts.lms`
- **Deployment targets** (as configured in project): iOS / macOS **26.x** (matches current SDK; update this note if you lower deployment for wider OS support)

## Diagnostics

- When data looks wrong, verify environment + token ([[Authentication and session — Experts OS]]) and compare with staging seed quality (known gap documented under [[Roadmap — Experts OS]]).

## See also

- [[Networking and API — Experts OS]]

## Links

- [[Entities/Projects/Experts OS]]
