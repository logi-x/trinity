---
title: "JavaScript"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "tech/javascript"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/JavaScript.md"
---

# JavaScript

JavaScript in this vault usually means application behavior in the Experts web stack rather than generic language theory: route handlers, client components, UI interactions, browser events, and integration glue around TypeScript-heavy code.

## Where it shows up most

- Next.js page and component behavior
- browser-side event handling and form state
- integration code around auth, payments, and realtime
- scripts and build tooling in the monorepo

## Practical conventions

- Prefer clear data flow over clever abstractions.
- Keep server/client boundaries explicit in app-router code.
- Push shared business rules into reusable helpers instead of duplicating inline conditions.
- Treat JavaScript-heavy files as a smell when they should really be typed with [[Wiki/Concepts/TypeScript]].

## Vault context

Conversation links to this page usually indicate frontend implementation work around the Experts app: UI behavior, route logic, validation flows, or codegen/tooling questions that were tagged broadly as JavaScript.

## Relationship to TypeScript

Most active product code is TypeScript-first. JavaScript still matters in:

- config files
- third-party examples
- copied snippets from conversations
- legacy utility code and package scripts

So this topic is best read as "runtime/frontend scripting concerns" rather than "plain JS as a strategic choice."

## Related

- [[Wiki/Concepts/TypeScript]]
- [[Wiki/Concepts/Node.js]]
- [[Wiki/Concepts/Testing]]
- [[Projects/Experts/Experts App/STRUCTURE]]
