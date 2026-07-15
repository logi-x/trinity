---
title: "Node.js"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "tech/node-js"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Node.js.md"
---

# Node.js

Node.js is the runtime foundation for most Experts web and tooling work: Next.js app execution, package scripts, local dev tooling, and build/test orchestration inside the monorepo.

## Main uses in this vault

- running the Experts App locally
- API route execution in Next.js
- package scripts for lint, test, build, and content generation
- developer tooling around Prisma, NextAuth, and monorepo tasks

## Operational concerns

- environment consistency across macOS, Linux, WSL, and containerized dev setups
- memory or build-time instability on large Next.js tasks
- package-manager alignment with [[Wiki/Concepts/pnpm]] or [[Wiki/Concepts/Yarn]]
- making local scripts work even when absolute paths differ by machine

## What linked conversations usually discuss

When this page is linked from conversations, it usually points to runtime/debugging concerns rather than language-level Node.js design:

- server startup issues
- build errors
- dependency resolution
- local tooling behavior
- environment-specific differences

## Why it matters

Node is the execution layer that ties frontend work, route handlers, and dev tooling together. Many "React" or "Next.js" problems in practice are really Node runtime, package, or environment problems.

## Related

- [[Wiki/Concepts/JavaScript]]
- [[Wiki/Concepts/Next.js]]
- [[Wiki/Concepts/Monorepo]]
- [[Wiki/Concepts/Testing]]
