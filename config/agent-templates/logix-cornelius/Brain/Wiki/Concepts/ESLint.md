---
title: "ESLint"
date: "2026-04-10"
updated: "2026-05-29"
tags: ["entity", "topic", "tech/eslint"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/ESLint.md"
---

# ESLint

ESLint is one of the main quality gates in Experts frontend work. In conversations it usually represents codebase conventions, correctness nudges, and the cost of keeping large UI changes aligned with team standards.

## Where it matters

- catching framework misuse early
- enforcing import, hook, and style conventions
- keeping refactors honest
- surfacing project-specific rules that encode team decisions

## Error-disclosure sink rule (EXP-170)

`no-restricted-syntax` (scoped to `app/api/**/route.{ts,tsx}`) keeps a caught error's `.message` out of responses — the class-level guard behind the error-disclosure family:

- **stack** (EXP-132): `MemberExpression[property.name='stack'][object.name=/^(error|err|e)$/]`.
- **sink** (EXP-170): `error.message` anywhere inside a `NextResponse.json(...)` call — catches bare `{error: error.message}` and the `error instanceof Error ? error.message : '…'` ternary.
- **two-step** (EXP-170): capturing it into a `message`/`errorMessage`/`msg`/`errMsg` local (`const message = error.message; … {error: message}`).
- Deliberately excludes server-side logging (`observe`/`logger`) and Zod `validationResult.error.message` (object isn't a bare `error`/`err`/`e` identifier).
- Fix = `safeErrorJson(error, {publicMessage, logContext})`; surface intentional client messages via `DomainError` (it forwards them verbatim, no details/stack).

**Gotcha:** `src/lib/**` is in the global `ignores`, so this rule never fires there — extracting a response builder into `src/lib` evades it (EXP-189; un-ignoring surfaces ~44 unrelated pre-existing lint errors). Flat-config global ignores can't be re-enabled by a later `files` block.

## Related

- [[Wiki/Concepts/Prettier]]
- [[Wiki/Concepts/TypeScript]]
- [[Wiki/Concepts/Testing]]
