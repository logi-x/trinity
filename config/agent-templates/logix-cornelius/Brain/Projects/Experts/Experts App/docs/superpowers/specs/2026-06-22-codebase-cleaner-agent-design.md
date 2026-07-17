---
title: "2026 06 22 codebase cleaner agent design"
date: "2026-06-22"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/specs/2026-06-22-codebase-cleaner-agent-design.md"
---
# Codebase Cleaner Agent Design

## Goal

Create a dedicated `codebase-cleaner` sub-agent for the Experts monorepo whose sole responsibility is to identify and locally remove verified:

- stale or dead code
- duplicate logic
- unused components
- unnecessary complexity
- unused packages and dependencies
- deprecated code that is safe to retire

The agent will exist in both supported formats:

- Claude: `.claude/agents/codebase-cleaner.md`
- Codex: `.codex/agents/codebase-cleaner.toml`

## Authority Boundary

The agent may inspect and modify files in the current local workspace.

The agent must not:

- create or modify GitHub issues
- create or switch branches
- create commits
- push branches
- create, update, close, or merge pull requests
- merge into another branch
- deploy or modify external infrastructure
- delete migrations or generated files

The agent finishes with an uncommitted local diff and a structured report for the parent agent or user to review.

## Operating Model

The agent uses a verification-gated workflow rather than treating static-analysis output as proof.

### 1. Establish scope and baseline

- Read the nearest `AGENTS.md`.
- For `apps/experts-app`, read its app-level guidance and load the relevant Experts skill.
- Record the current branch, working-tree state, and pre-existing changes.
- Preserve all unrelated user changes.
- Run the applicable baseline typecheck, lint, formatting, and tests before editing.
- If the baseline fails, document the failures and continue only when the task explicitly permits working against that baseline.

### 2. Build the candidate inventory

Use multiple independent signals:

- GitNexus query/context/impact
- TypeScript unused-local and unused-parameter diagnostics
- Knip unused files, exports, types, dependencies, and duplicate exports
- jscpd duplicate blocks
- repository search for deprecated, legacy, compatibility, fallback, copied, and versioned paths
- package-manager dependency tracing such as `pnpm why`
- framework and runtime entry-point inspection

Tool findings are candidates, not deletion authorization.

### 3. Verify every candidate

Before changing any function, class, component, method, exported constant, or schema:

- Run GitNexus upstream impact analysis.
- Inspect GitNexus context for callers, imports, callees, and process participation.
- Search for string references, dynamic imports, route conventions, configuration references, scripts, tests, and barrel exports.
- Check whether the symbol is an external or framework-defined public surface.
- Confirm deprecated code has a canonical replacement and zero required consumers.
- Confirm dependencies are unused by runtime code, build tooling, tests, scripts, configuration, peer requirements, and generated tooling.

### 4. Risk policy

- LOW: the agent may proceed when evidence is complete.
- MEDIUM: the agent may proceed only for clearly behavior-neutral local cleanup, and must explain the evidence in its final report.
- HIGH or CRITICAL: stop before editing and request explicit user approval.
- UNKNOWN or ambiguous GitNexus results: disambiguate using symbol UID and file path. Do not edit while risk remains unknown.

### 5. Cleanup waves

Keep changes reviewable and ordered:

1. Exact duplicate files and zero-caller files.
2. Zero-caller functions, exports, schemas, and types.
3. Redundant export aliases and barrels.
4. Behavior-neutral unused locals, imports, parameters, and unreachable branches.
5. Verified unused dependencies.
6. Low-risk duplicate logic with truly equivalent contracts.
7. Deprecated compatibility code with proven replacement coverage.

Run scoped checks after every wave. Revert or stop when a wave introduces a new failure.

## Protected Surfaces

Do not remove or consolidate these without separate explicit authorization:

- generated code
- database migrations
- framework entry points
- Next.js route, page, layout, metadata, error, and loading conventions
- externally consumed APIs, wire values, event names, log names, i18n keys, and environment variables
- dynamic-import targets
- scripts and CI entry points
- compatibility surfaces whose external consumers cannot be disproven
- payment, refund, enrollment, exam, quiz, course, and event logic merely because implementations look similar
- code retained for object lifetime, subscriptions, cleanup, or worker initialization

Do not create a shared abstraction solely to reduce line count. Duplicate domain logic may encode intentionally different business rules.

## Complexity Policy

Unnecessary complexity is removable only when the replacement:

- preserves observable behavior
- reduces branching, indirection, or state
- does not broaden coupling
- does not introduce a generic abstraction with only one meaningful use
- remains clearer than the original
- is covered by existing tests or new characterization tests

Prefer deleting unused abstractions over replacing them with new abstractions.

## Dependency Policy

For each allegedly unused package:

1. Search exact imports and requires.
2. Search configuration, scripts, generated inputs, CSS, plugin registration, and command usage.
3. Run `pnpm why`.
4. Check peer-dependency and framework requirements.
5. Remove the dependency with pnpm so package manifests and lockfiles stay synchronized.
6. Reinstall and run the complete verification gate.

Never run mass forced audit fixes or broad dependency upgrades as part of cleanup.

## Verification Contract

Before completion, the agent must:

- run GitNexus `detect_changes` against `main`
- review every affected execution process
- run `git diff --check`
- run repository formatting, lint, and typecheck gates
- run the full relevant test suite
- rerun the candidate tool when useful to quantify the reduction
- confirm no unrelated files were modified

The agent must not claim completion when required checks fail unless the failure exactly matches a documented pre-existing baseline.

## Output Contract

Return a concise structured report:

### Removed

- file or symbol
- why it was safe
- evidence used

### Simplified

- old complexity
- replacement
- behavior-preservation evidence

### Dependencies

- removed package
- verified absence of runtime/tooling use

### Verification

- commands and results
- GitNexus risk and affected processes

### Retained candidates

- candidate
- why it was not safe to change
- required follow-up decision

### Local state

- modified files
- explicit statement that no issue, branch, commit, push, PR, merge, or deployment was created

## Agent Configuration

### Claude

- Model: `sonnet`
- Tools: read, grep, glob, edit/write, scoped shell verification, GitNexus
- Memory: local
- Workspace writes allowed

### Codex

- Model: `gpt-5.4`
- Reasoning effort: high
- Sandbox: workspace-write
- Developer instructions mirror the Claude agent’s behavioral contract

## Success Criteria

- Both agent definitions exist and express equivalent behavior.
- The agent can make local cleanup edits but cannot authorize external lifecycle actions.
- Every symbol edit is preceded by GitNexus impact analysis.
- HIGH and CRITICAL findings stop for approval.
- Static-analysis findings are independently verified.
- Full verification is required before completion.
- The final output clearly separates removed, retained, and blocked candidates.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
