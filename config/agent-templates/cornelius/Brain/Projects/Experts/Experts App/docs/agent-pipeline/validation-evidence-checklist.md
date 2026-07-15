---
title: "validation evidence checklist"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/agent-pipeline/validation-evidence-checklist.md"
---
# Validation Evidence Checklist

**Outcome:** agents cannot mark work **Done** without evidence. (EXP-46)

This is the gate between "I changed some code" and **Done**. Every finding that produced a change must attach the
evidence below (in the PR body and/or the issue) before it moves to Done. There are two paths — **bug** and **security** —
and the security path is stricter.

## Evidence format

Attach evidence as:

- **Command output** — paste the relevant tail of the actual command (`pnpm experts:check`, vitest summary,
  `pnpm db:check:drift`, `bash -n`, `docker compose config`). State the command and its result, not "tests pass".
- **Test references** — name the test file(s) and the specific cases added, with the pass count.
- **On-`main` evidence** (for already-resolved closes) — `file:line` citations proving the fix already exists, in the
  close comment.
- **Honest negatives** — if a step was skipped or a test could not be written, say so and why. Do not imply coverage that
  does not exist.

## Common checklist (both paths)

- [ ] **Reproduction confirmed or disproven** — the original symptom was reproduced before the fix, or shown not to exist
      (already-resolved / not-a-bug).
- [ ] **Fix validated against the original finding** — the change addresses what the finding actually reported (link the
      finding + fingerprint).
- [ ] **Regression test or rationale** — a test that fails before / passes after, OR an explicit rationale for why a test
      is infeasible.
- [ ] **Typecheck / lint / test output** — `pnpm experts:check` (FORMAT/LINT/TYPECHECK) clean, or scoped
      `typecheck:touched -- <files>` + `vitest run <files>` for narrow changes. Remember vitest/esbuild strips types —
      only `tsc`/`experts:check` catches type errors.
- [ ] **No happy-path regression** — when the fix adds an early-return/rejection or a new guard, a happy-path test proves
      the previously-working flow still works (per-handler coverage ≠ flow coverage).
- [ ] **Deployment / release notes** — for infra/migration/config changes, note what takes effect on next deploy, and any
      ordering (migrations, drift).
- [ ] **Residual risk / follow-up** — anything left undone is filed as a new finding or noted as a known limitation.
- [ ] **GitHub mirror closed** — on Done, the mirrored GitHub issue is closed too (the two-way sync reopens a one-sided
      close).

## Bug path (additional)

- [ ] The failing case is covered by a test at the right layer (unit for pure logic; route/integration for handler
      behavior).
- [ ] For data/DTO changes, narrowing is done at the DB layer (`include` → `select`) where applicable, with `tsc` as
      proof-of-no-consumer (grep cannot prove it).

## Security path (additional — required for `security` findings)

- [ ] **Exploit closed** — re-running the original exploit/proof now fails. Where feasible, a security regression test
      encodes this (e.g. asserts 401/403, asserts PII field is `null`, asserts the injected option is rejected).
- [ ] **TOCTOU-safe** — if enforced on an async/deferred path (verify redirect, webhook, cron), the check reads a signal
      **snapshotted at initiation**, not mutable state re-read at completion.
- [ ] **Sibling surfaces covered** — symmetric copy-paste routes/handlers are fixed in the same diff (don't fix one and
      leave its twin open).
- [ ] **No new disclosure** — the fix does not leak raw errors, secrets, or internal details to clients/logs.
- [ ] **Reviewer/gate** — the R5 gatekeeper (and any required specialist lens) has passed; CI is complete and green.

## Done criteria (explicit)

A finding may move to **Done** only when:

1. its path's checklist (common + bug **or** security) is satisfied with attached evidence, **and**
2. either the change is merged to `main` (sentinel verified on `origin/main`, not just PR state = Merged), **or** it is a
   documented already-resolved-on-`main` close, **and**
3. the GitHub mirror is closed.

If any box is unchecked, the issue stays `In Review` (or returns to `In Progress`) — not Done.

## Acceptance criteria (this document)

- [x] Done criteria are explicit.
- [x] Security and bug validation paths are separate.
- [x] Evidence format is documented.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
