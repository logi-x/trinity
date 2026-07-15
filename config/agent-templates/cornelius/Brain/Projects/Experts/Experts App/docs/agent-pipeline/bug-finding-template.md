---
title: "bug finding template"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/agent-pipeline/bug-finding-template.md"
---
# Bug Finding Template

**Outcome:** bug findings have enough detail for reproduction, assignment, and validation. (EXP-44)

Use this template for every `bug`-labelled finding (the R2 `02-find-critical-bugs` lane, completeness findings from R7,
and ad-hoc bug reports). It extends the universal [intake contract](./intake-contract.md).

## Template fields

| Field                     | What to write                                                                                                               |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Observed behavior**     | What actually happens (the wrong output, the error, the missing effect).                                                    |
| **Expected behavior**     | What should happen instead.                                                                                                 |
| **Reproduction steps**    | The minimal sequence to trigger it — request, inputs, state. If you cannot reproduce, say so and mark the type accordingly. |
| **Affected area**         | File (with line if known), route, component, module, or service.                                                            |
| **Environment / context** | Where it reproduces (prod/staging/local; which env vars/flags matter; which user role).                                     |
| **Evidence**              | At least one of: error message, stack trace, screenshot, failing test, or log excerpt.                                      |
| **Suspected cause**       | If known — the likely line/logic. Optional.                                                                                 |
| **Validation steps**      | The command/test/check that proves the fix (feeds the [validation checklist](./validation-evidence-checklist.md)).          |
| **Fingerprint**           | Inline-coded `` `<!-- agent-fp: <hash> -->` ``.                                                                             |

## Priority mapping

| Priority   | When                                                                                                             |
| ---------- | ---------------------------------------------------------------------------------------------------------------- |
| `1` Urgent | Active production breakage / data loss / money incorrectness affecting many users now.                           |
| `2` High   | Significant broken behavior or a correctness bug in a critical path (payments, auth, ZATCA), no safe workaround. |
| `3` Medium | Real bug with limited blast radius or an available workaround.                                                   |
| `4` Low    | Minor / cosmetic / edge-case; cleanup; dead code.                                                                |
| `0` None   | Unconfirmed or informational.                                                                                    |

## Duplicate detection

Before filing, check for an existing issue:

1. **Fingerprint match** — search the board for the same `` `<!-- agent-fp: <hash> -->` `` (the routines compute a stable
   hash from the finding's identity). A match means it is already filed; do not re-file.
2. **Asset + symptom match** — search by file/route + the symptom. The board audit (R8 `08-linear-board-audit`) also
   sweeps for duplicates, already-resolved-on-`main` issues, and conflicting open issues.
3. **Already fixed on `main`?** — especially for `[spinoff: …]` findings: read the current code first. Spinoffs are
   frequently already resolved by their parent PR's broader sweep; if so, close as already-resolved with on-`main`
   evidence (file:line) and close the GitHub mirror — do **not** open a redundant PR.
4. If it is a genuine duplicate of an open issue, mark `duplicateOf` rather than filing anew (the board has a finite issue
   budget; the audit prefers consolidation).

## R3 auto-fix eligibility

`03-fix-bugs` (R3) only picks up findings that are **`bug` + `Todo`**. To be auto-fixable a bug must be:

- mechanical and decision-free (no product/operator/design choice required),
- scoped to specific files with a clear validation command,
- not a design-decision refactor (those belong in `Recourses` or `Backlog` with rationale).

If a bug needs a decision first, keep it out of `bug`+`Todo` so R3 does not mechanically "fix" a judgment call.

## Example

```
Title:  [bug] mapEventToListItemDTO emits host email on public GET /events
Labels: bug      Priority: 3 (Medium)      Status: Todo
Observed: unauthenticated GET /api/v1/events returns host email addresses
Expected: public list never exposes host email (PII, CWE-359)
Repro: GET /api/v1/events with no auth → inspect hosts[].user.email
Area: src/lib/events/mappers/event.mapper.ts (mapEventToListItemDTO); src/lib/events/includes/event.include.ts
Evidence: inline host object sets email: h.user.email; eventListInclude selected email
Suspected cause: list mapper bypasses mapUserToDTO (which null-strips email)
Validation: route host through mapUserToDTO; include uses userPublicSelect; assert email null in response
Fingerprint: `<!-- agent-fp: c57ef950be5e -->`
```

## Acceptance criteria (this document)

- [x] Template supports agent-created bug issues.
- [x] Priority mapping is documented.
- [x] Duplicate detection guidance is included.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
