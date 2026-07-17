---
title: "EXP-176 — CI set -a exports all bake-env credentials when EXPERTS_APP_DATABASE_URL absent"
date: "2026-05-28"
status: open
resolution: unknown
tags: [bug, security, ci, credentials, docker, project/experts]
linear: "https://linear.app/experts/issue/EXP-176"
fingerprint: "9ed3e9c5ca1e"
---

## Summary
`.github/ci/docker-app-release.sh` uses `set -a` (export all variables) before sourcing the bake-env file. When `EXPERTS_APP_DATABASE_URL` is absent from the environment, the early-exit guard is skipped and all variables sourced from the bake-env file — including any credentials — are exported into the shell environment. These exported variables can propagate into child processes (docker buildx bake) and may appear in CI logs or build caches.

## Root cause
`set -a` is scoped too broadly: it exports every variable defined after the command, including sensitive values. The fix is to either remove `set -a` and explicitly export only the required variables, or gate the export block behind the `EXPERTS_APP_DATABASE_URL` presence check.

## Agent fingerprint
`<!-- agent-fp: 9ed3e9c5ca1e -->`

## Status
`open` — Backlog (Medium). Credentials leak path active in CI; no immediate production exposure, but credentials may appear in build logs.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
