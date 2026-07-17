---
title: "CI workflows must (a) move all `${{ github.* }}` context values to `env:` block variables before use in `run:` steps; (b"
date: "2026-06-05"
decision: "CI workflows must (a) move all `${{ github.* }}` context values to `env:` block variables before use in `run:` steps; (b) pass `--` before user-controlled refspecs in all git CLI calls; (c) source `.e"
stakeholders: "Platform, Security"
review_by: "2026-09-05"
source: "[[Raw/sources/2026-06-06-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** CI workflows must (a) move all `${{ github.* }}` context values to `env:` block variables before use in `run:` steps; (b) pass `--` before user-controlled refspecs in all git CLI calls; (c) source `.env` credentials in a subshell rather than with `set -a; . .env` so exports die with the subshell. (EXP-304 + EXP-176, PR #866)

**Rationale:** (a) Unquoted context values in `run:` shells are direct code injection: a branch named `; rm -rf /` executes on the runner. (b) Git parses `--upload-pack=cmd` as an option before `--` — a branch name can become a git option even after shell-quoting. (c) `set -a; . .env` exports every secret into the build environment; a missing var causes the whole file to source with partial state, leaking unrelated credentials.

**Stakeholders:** Platform, Security

**Source:** [[Raw/sources/2026-06-06-experts-agent-digest.md]]
