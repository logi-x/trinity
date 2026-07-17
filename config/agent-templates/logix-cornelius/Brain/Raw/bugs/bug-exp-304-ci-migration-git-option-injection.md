---
title: "EXP-304: Residual git option injection in migration-immutability after EXP-279 fix"
date: "2026-06-03"
status: open
resolution: unknown
tags: [bug, security, ci, github-actions, injection, project/experts]
linear_url: "https://linear.app/experts/issue/EXP-304"
agent_fp: "e2fb255d8f59"
severity: medium
area: ci/platform
file: ".github/workflows/experts-app.yml"
symbol: migration-immutability
source: "generated"
source_id: "Raw/bugs/bug-exp-304-ci-migration-git-option-injection.md"
---

# EXP-304: Residual git option injection — `git fetch` missing `--` separator

**Linear:** https://linear.app/experts/issue/EXP-304  
**FP:** `e2fb255d8f59` (R3)  
**Severity:** Medium  
**Filed:** 2026-06-03

## Summary

PR #799 (EXP-279 fix) moved `${{ github.base_ref }}` into a step-level `env:` variable, preventing shell metacharacter injection. However, the `git fetch` command in the same step still uses the variable without a `--` separator:

```bash
git fetch --no-tags origin $GH_BASE_REF
```

A PR from a branch named `--upload-pack=<cmd>` would pass through shell quoting (since `$GH_BASE_REF` is a safe env var expansion) but be parsed by git's own argv parser as an option, not a refspec — enabling a git-level argument injection. GitHub may block branch names starting with `--` at push time, but this is not a guaranteed hard guard.

## Repro

1. Open a PR from a branch named `--upload-pack=malicious-cmd` against `logi-x/experts`.
2. The migration-immutability job runs `git fetch --no-tags origin $GH_BASE_REF`.
3. Git parses `--upload-pack=malicious-cmd` as a git option, not a refspec.

## Fix

Add `--` separator:
```bash
git fetch --no-tags origin -- "$GH_BASE_REF"
```

## Related

- EXP-279: Shell injection via `${{ github.base_ref }}` — fixed in PR #799
- PR #799: Introduced env-block indirection but left git fetch without `--`
- EXP-261: Migration-immutability direct-push bypass — fixed in PR #766

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
