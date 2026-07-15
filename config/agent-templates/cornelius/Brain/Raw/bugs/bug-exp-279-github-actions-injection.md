---
title: "EXP-279 — GitHub Actions workflow injection via ${{ github.base_ref }} in migration-immutability job"
date: "2026-06-02"
status: open
resolution: unknown
tags: [bug, security, ci, github-actions, injection, project/experts]
linear: "https://linear.app/experts/issue/EXP-279/security-github-actions-workflow-injection-via-dollar-githubbase-ref"
fingerprint: "612635d18b4f"
---

## Summary

`.github/workflows/experts-app.yml` — `migration-immutability` job, "Block edits to already-merged migrations" step — interpolates `${{ github.base_ref }}` directly into a `run:` shell script. GitHub allows PR branch names containing shell metacharacters (`'`, `;`, `|`, `&`, `$()`). Any contributor who can open a PR against `logi-x/experts` can craft a branch name that injects arbitrary shell commands into the CI runner during migration-immutability checks. This was introduced by PR #766 (which fixed EXP-261).

## Root cause

`.github/workflows/experts-app.yml` — `migration-immutability` job, step using `${{ github.base_ref }}` in a `run:` block. Fix: pass the value through an `env:` variable and reference it as `$MY_VAR` in the shell step (environment variable expansion is not subject to shell injection).

## Agent fingerprint

`<!-- agent-fp: 612635d18b4f -->`

## Status

`open` — Backlog (High). Introduced by PR #766 (merged 2026-06-02T06:22Z). Any PR can exploit this before the fix lands. Requires immediate attention.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
