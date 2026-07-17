---
title: "intake contract"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/agent-pipeline/intake-contract.md"
---
# Agent Finding Intake Contract

**Outcome:** automated agents and subagents create findings that are immediately triageable — no human has to
reverse-engineer what the agent meant. (EXP-42)

A "finding" is a Linear issue on the Experts team created by an agent. This contract is the **minimum** every finding must
satisfy before it enters the board. A finding that does not satisfy it is not ready and must not be filed as-is.

## Raw notes are not findings

Scan output, a stack-trace dump, a "might be a problem here" hunch, or a paste of logs is **not** a finding. Raw notes
must be turned into a structured finding (below) before they touch the board, or kept out of Linear entirely. Filing raw
notes pollutes triage and breaks dedup. If an agent cannot fill the required contract for something, it does not yet have
a finding.

## Required contract (every finding)

Every agent-created finding MUST carry:

| Field                         | Meaning                                                                                                                                                          |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Finding source**            | The agent/subagent name, the run ID if available, and the scan type (e.g. `01-scan-vulnerabilities` / R1, `07-codebase-completeness-audit` / R7, ad-hoc review). |
| **Finding type**              | One of: `vulnerability`, `bug`, `regression`, `flaky test`, `docs/config`, `unknown`.                                                                            |
| **Affected asset**            | The concrete target: file (with line if known), route, component, API endpoint, package, config, or service.                                                     |
| **Evidence**                  | At least one of: reproduction steps, stack trace, exploit proof, screenshot, failing test, or scan output. A finding with no evidence is `unknown` at best.      |
| **Impact**                    | User / security / data / business impact — what breaks and for whom.                                                                                             |
| **Suggested owner or domain** | If known (e.g. payments, realtime, billing/ZATCA, i18n). Optional but speeds routing.                                                                            |
| **Suggested validation step** | How a fix would be proven (the command, the test, the manual check).                                                                                             |
| **Fingerprint**               | An inline-coded dedup marker `` `<!-- agent-fp: <hash> -->` `` (inline code so Linear does not strip it on edit).                                                |

## Filing requirements

- **Title:** `[<domain or type>] <concise problem>` — e.g. `[security] <X> bypasses <Y>`, `[bug] <X> returns wrong <Y>`,
  `[completeness] <env> declared but never read`.
- **Labels:** apply `security` for vulnerabilities, `bug` for bugs/regressions, `completeness` for completeness-audit
  findings. Labels drive routing (below).
- **Priority:** map severity → Linear priority per the type-specific template
  ([vuln](./vulnerability-finding-template.md), [bug](./bug-finding-template.md)). Do not default everything to None.
- **Status at filing** reflects readiness, not caution:
    - `Todo` — self-contained and R3-shippable now.
    - `In Progress` — partially done / actively being worked.
    - `Backlog` — real but not yet actionable.
    - `Recourses` — parked pending a design/product/operator decision (a holding state, not "ready").
- **Fingerprint** is mandatory for dedup, digest, and the board audit (R8). Keep it inline-coded so subsequent edits do
  not drop it.

## Routing rules

| Finding type     | Label                   | Template                                                              | Lane                                                    |
| ---------------- | ----------------------- | --------------------------------------------------------------------- | ------------------------------------------------------- |
| vulnerability    | `security`              | [vulnerability-finding-template](./vulnerability-finding-template.md) | Security Findings → triage → handoff                    |
| bug / regression | `bug`                   | [bug-finding-template](./bug-finding-template.md)                     | Bug Findings → (if `bug`+`Todo`) auto-fixable by R3     |
| flaky test       | `bug`                   | bug template (note the nondeterminism)                                | Bug Findings; usually not R3-auto (needs investigation) |
| docs/config      | (none) / `completeness` | bug template (lightweight)                                            | docs digest / completeness lane                         |
| completeness     | `completeness`          | bug template                                                          | Codebase Completeness lane (R7)                         |
| unknown          | —                       | not fileable until upgraded to a concrete type                        | quarantine; do not file raw                             |

**R3 auto-fix gating:** only `bug` + `Todo` findings are picked up by `03-fix-bugs`. A design-decision refactor, anything
needing product/operator input, or anything ambiguous must NOT be `bug`+`Todo` — park it in `Recourses` or leave it
`Backlog` with the rationale, so R3 does not try to mechanically "fix" a decision.

**Symmetric siblings:** if a finding affects one of a set of copy-paste sibling surfaces (e.g. the course / event /
subscription verify routes), say so explicitly so the fix covers all siblings in one diff rather than spawning N spinoffs.

## Example — vulnerability finding (abbreviated)

```
Title:  [security] Tabby verify routes: no auth() allows completing another user's enrollment
Labels: security, bug      Priority: 3 (Medium)      Status: Todo
Source: ad-hoc review of the EXP-129 completion paths
Type:   vulnerability
Asset:  app/api/v1/courses/[id]/enroll/verify/route.ts (Tabby branch); + sibling events register/verify
Evidence: enrollment looked up solely by Tabby payment_id; no auth()/ownership check before completion side-effects
Impact:  any holder of another user's payment_id can drive that user's enrollment to completion
Validation: add auth()+ownership; tests asserting 401 (no session) / 403 (non-owner); existing happy path still 200
Fingerprint: `<!-- agent-fp: f83653187ae8 -->`
```

## Example — bug finding (abbreviated)

```
Title:  [bug] Subscription checkout returns English for all non-Arabic locales (Spanish unreachable)
Labels: bug      Priority: 4 (Low)      Status: Todo
Source: spinoff of EXP-100 review
Type:   bug
Asset:  app/api/v1/commerce/subscriptions/checkout/route.ts (locale derivation)
Evidence: locale = startsWith("ar") ? "ar" : "en" — "es" never reached; tabbyKsaOnlyMessage("es") branch is dead
Impact:  Spanish users always get the English Tabby KSA-only message
Validation: add optional locale + es-aware header derivation; test asserts es renders Spanish
Fingerprint: `<!-- agent-fp: cf338029514a -->`
```

## Acceptance criteria (this document)

- [x] Intake template is documented (required contract + filing requirements).
- [x] Routing rules are documented (type → label → template → lane, incl. R3 auto-fix gating).
- [x] Example vulnerability and bug findings are included.
- [x] Raw notes are explicitly disallowed outside intake.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
