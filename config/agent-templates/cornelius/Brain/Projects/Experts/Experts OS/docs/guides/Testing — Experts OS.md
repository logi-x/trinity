---
title: "Testing — Experts OS"
date: "2026-04-11"
tags: ["project/experts", "project/experts-os", "tech/xctest", "topic/api", "topic/auth", "topic/gsd", "topic/networking", "topic/planning", "topic/testing"]
category: "Projects/Experts/Experts OS"
type: "reference"
updated: "2026-07-15"
---

# Testing — Experts OS

Automated tests live in **`ExpertsTests`** (Xcode test target, bundle `sa.com.experts.ExpertsTests`).

#experts-os/testing #topic/xctest #topic/testing #topic/gsd

## Existing suites (examples)

- **`APIClientDecodingTests`** — JSON decoding against API shapes.
- **`SessionStoreTests`** — session state transitions.
- **`StorePersistenceTests`** — persistence expectations.

## Practices

- Prefer **deterministic** decoding tests with fixture JSON.
- When changing [[APIEndpoint]] or DTOs.

## See also

- [[Roadmap — Experts OS]] (verification wave)
