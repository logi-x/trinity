---
title: "EXP-261: Migration-immutability CI guard bypassed by direct push to main"
date: "2026-06-01"
status: open
resolution: unknown
tags: [bug, security, ci, migrations, project/experts]
linear: "https://linear.app/experts/issue/EXP-261/security-migration-immutability-ci-guard-bypassed-by-direct-push-to"
fingerprint: "72edaca4cf46"
---

## Summary

The `migration-immutability` job in `.github/workflows/experts-app.yml` runs only on `pull_request` events (`if: github.event_name == 'pull_request'`). Direct pushes to `main` by repository contributors or maintainers bypass the guard entirely. A contributor with write access to `main` can retroactively corrupt applied migrations without triggering the CI check.

## Location

`.github/workflows/experts-app.yml` — `migration-immutability` job condition `if: github.event_name == 'pull_request'`

## Repro Steps

1. Direct-push a commit to `main` that modifies an existing migration file.
2. `migration-immutability` job does not run; no CI failure.

## Agent Fingerprint

`72edaca4cf46` (R3)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
