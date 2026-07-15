---
title: "GitHub Actions `run:` steps must never interpolate expression contexts (`${{ github.* }}`, `${{ inputs.* }}`, etc.) dire"
date: "2026-06-02"
decision: "GitHub Actions `run:` steps must never interpolate expression contexts (`${{ github.* }}`, `${{ inputs.* }}`, etc.) directly; use `env:` block indirection and reference the value as a shell variable ("
stakeholders: "Security, CI/CD, Logix"
review_by: "2026-09-02"
source: "[[Raw/sources/2026-06-02-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** GitHub Actions `run:` steps must never interpolate expression contexts (`${{ github.* }}`, `${{ inputs.* }}`, etc.) directly; use `env:` block indirection and reference the value as a shell variable (`$MY_VAR`) instead.

**Rationale:** EXP-279: PR #766 introduced `${{ github.base_ref }}` directly in a `run:` shell step. Any PR from a branch with shell metacharacters in its name can inject arbitrary commands into the CI runner. This class of injection has been a known GitHub Actions attack vector since 2021. The `env:` pattern is the canonical mitigation and is enforced here for all future workflow changes.

**Stakeholders:** Security, CI/CD, Logix

**Source:** [[Raw/sources/2026-06-02-experts-agent-digest.md]]
