---
title: "`src/lib/auth/` is the canonical auth package; no `src/lib/auth.ts` file may coexist at the same tree level."
date: "2026-05-30"
decision: "`src/lib/auth/` is the canonical auth package; no `src/lib/auth.ts` file may coexist at the same tree level."
stakeholders: "Logix"
review_by: "2026-08-30"
source: "[[Raw/sources/2026-05-28-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `src/lib/auth/` is the canonical auth package; no `src/lib/auth.ts` file may coexist at the same tree level.

**Rationale:** PR #629 (EXP-200) consolidated three orphaned auth utilities (`auth.ts`, `auth-context.tsx`, `auth-utils.ts`) into the existing `src/lib/auth/` package. The prior coexistence of a file and a directory with the same base name (`auth.ts` vs `auth/`) caused import ambiguity and compiler confusion across 73 import sites. Any new auth utility must be created inside `src/lib/auth/`; the bare `src/lib/auth.ts` path is prohibited.

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-05-28-experts-agent-digest.md]]
