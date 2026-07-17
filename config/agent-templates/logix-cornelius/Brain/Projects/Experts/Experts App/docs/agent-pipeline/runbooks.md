---
title: "runbooks"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/agent-pipeline/runbooks.md"
---
# Agent / Subagent Runbooks

**Outcome:** automated agents and subagents have unambiguous operating guidance for using this Linear pipeline. (EXP-47)

Each runbook below names its **inputs**, **outputs**, the **routing** decision, and the **manual-intervention** points
(where an agent must stop and defer to a human/operator). They compose the lifecycle described in the
[README](./README.md): produce → triage → handoff → implement → validate → close.

## 1. Intake & triage

- **Inputs:** a candidate finding (scan output, review observation). **Owner:** R1/R2/R7 or an ad-hoc agent.
- **Steps:**
    1. Turn the candidate into a structured finding per the [intake contract](./intake-contract.md). If the required fields
       cannot be filled, it is not a finding — do not file raw notes.
    2. Run duplicate detection (fingerprint, asset+symptom, already-fixed-on-`main`, board audit). De-dupe via `duplicateOf`
       rather than re-filing.
    3. Classify type → apply label → choose template → set priority and a readiness-accurate status.
    4. Add the inline-coded `` `<!-- agent-fp: <hash> -->` `` fingerprint.
- **Output:** a filed, labelled, prioritized finding (or a `duplicateOf` link, or nothing if already resolved).
- **Manual intervention:** ambiguous type/severity, or anything implying a product/operator decision → file as `Recourses`
  / `Backlog` with the decision needed, not `Todo`.

## 2. Security finding handling

- **Inputs:** a `security` candidate. **Template:** [vulnerability](./vulnerability-finding-template.md).
- **Steps:** fill the vuln template (class, trust boundary, preconditions, exploit path/proof, severity rationale);
  map severity → priority; specify the required security validation.
- **Output:** a `security`-labelled finding with an exploit path and a remediation direction.
- **Manual intervention:** if a live secret/credential is observed in the working tree or logs, **do not** treat it as a
  routine finding — stop, flag for rotation, and never paste the secret value into Linear/PRs. Confirm `git ls-files` /
  `git check-ignore` before claiming a file is "committed".

## 3. Bug finding handling

- **Inputs:** a `bug` candidate. **Template:** [bug](./bug-finding-template.md).
- **Steps:** fill the bug template (observed/expected/repro/area/evidence); map priority; run duplicate detection; decide
  R3 auto-fix eligibility (`bug`+`Todo` only for mechanical, decision-free fixes).
- **Output:** a `bug`-labelled finding, `Todo` if R3-shippable else `Backlog`/`Recourses`.
- **Manual intervention:** flaky/nondeterministic or design-decision bugs → keep out of `bug`+`Todo`.

## 4. Implementation handoff

- **Inputs:** a triaged finding. **Contract:** [implementation handoff](./implementation-handoff-contract.md).
- **Steps:** enrich to the handoff fields (scope, non-goals, expected behavior, files+siblings, validation command,
  rollback risk, gate); move to `In Progress`; branch `feature/exp-NNN-…` before the PR; map issues→files to decide bundle
  vs fan-out.
- **Output:** a branch + PR implementing exactly the scoped change, or an already-resolved close with on-`main` evidence.
- **Manual intervention:** a finding that reaches this lane without handoff fields goes back to triage, not guessed.

## 5. Validation & closure

- **Inputs:** an implemented change. **Gate:** [validation evidence checklist](./validation-evidence-checklist.md).
- **Steps:** run the appropriate path (bug/security); attach evidence (command output, tests, pass counts); let CI + the
  R5 gatekeeper complete; on green, squash-merge.
- **Post-merge:** verify the change is on `origin/main` (grep a sentinel — PR state = Merged is not sufficient), set the
  Linear issue `Done`, **close the GitHub mirror**, list collateral ids as plain text, delete/prune the branch.
- **Output:** `Done` issue + merged change + closed mirror.
- **Manual intervention:** any unchecked validation box → stays `In Review`. A gatekeeper `BLOCK` closes the PR; open a
  fresh replacement rather than force-pushing past it.

## 6. Escalation rules

Stop and defer to a human/operator when:

- the fix requires a **product/business decision** (e.g. refund vs. void vs. support-queue);
- it requires an **operator/infra decision** (resource sizing, rollout cadence, a prod data sweep, enabling a cron);
- it touches **money correctness, ZATCA immutability, auth, or data deletion** in a non-mechanical way;
- a **live secret** is exposed (rotation is an operator action);
- the change is **high/critical blast radius** per impact analysis, or CI/gatekeeper cannot be satisfied without a design
  change.

Escalation output is an issue parked in `Recourses`/`Backlog` (or a Slack note to `#experts-bug-bots`) stating exactly
the decision required — never a silent guess.

## 7. Status & comment conventions

- **Status reflects reality:** `Backlog` (real, not actionable) · `Recourses` (parked on a decision) · `Todo`
  (R3-shippable now) · `In Progress` (being worked) · `In Review` (PR open / validating) · `Done` (merged + evidence +
  mirror closed) · `Duplicate`/`Canceled` (terminal).
- **Markers survive edits:** keep `` `<!-- agent-fp: <hash> -->` `` inline-coded (Linear strips leading bare HTML
  comments on update).
- **Comments are evidence, not chatter:** a status change to Done carries the validation evidence or the on-`main`
  citation. An already-resolved close states the file:line proof.
- **Mirror discipline:** close the GitHub mirror whenever closing the Linear issue; verify the status stuck (~60s) since
  the two-way sync can reopen a one-sided close.
- **Collateral:** list collateral issue ids as plain text in the PR body so the auto-close regex matches.

## Acceptance criteria (this document)

- [x] Each runbook names required inputs and outputs.
- [x] Pipeline routing is unambiguous (type → label → template → lane → gate).
- [x] Manual intervention points are documented (per runbook + the escalation rules).

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
