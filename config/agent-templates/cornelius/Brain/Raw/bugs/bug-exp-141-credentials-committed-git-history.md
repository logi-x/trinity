---
title: "EXP-141: R2 and Redis credentials committed in plaintext to git history"
linear_id: "EXP-141"
agent_fp: "7471e694ff96"
date: "2026-05-26"
severity: "Critical"
status: "open"
resolution: "unknown"
tags: [bug, security, secrets, git-history, r2, redis, project/experts]
category: "bug"
source: "automation"
---

# EXP-141: R2 and Redis credentials committed in plaintext to git history

**Linear:** [EXP-141](https://linear.app/experts/issue/EXP-141) | **Fingerprint:** `<!-- agent-fp: 7471e694ff96 -->` | **Severity: Critical**

## Summary

`docker/workers/docker-compose.yml` was committed to the repository's main branch with R2 API token, R2 secret access key, and Redis password set as inline environment variables in the `pdf-worker` service block. The file was deleted in commit `a422e0c` (PR #503, 2026-05-26), but deletion from the working tree does **not** remove credentials from git history. The credentials remain permanently readable via `git show <parent-commit-sha> -- docker/workers/docker-compose.yml` or any git clone/fetch performed before or after the delete commit.

## Impact

- **Critical**: Production/staging secrets are permanently embedded in the git object store. Every repository clone, CI runner, and GitHub archive retains these credentials indefinitely.
- The R2 API token and R2 secret access key allow full read/write/delete access to the R2 storage bucket (including all user uploads and certification documents).
- The Redis password allows full access to the Redis instance (session data, BullMQ job queues, pub/sub channels).
- Credentials must be **rotated immediately** regardless of the status of any code fix.

## Evidence

`docker/workers/docker-compose.yml` deleted in commit `a422e0c` (2026-05-26). The credentials are readable at the parent commit SHA. Any git clone of the repository has access to this history.

## Required Actions

1. **Rotate R2 API token and secret access key immediately** — revoke the current key pair and generate new credentials. Update all deployment configs (`~/.experts-routines.env`, staging and production environment variable sources).
2. **Rotate Redis password immediately** — update `REDIS_PASSWORD` in all deployment configs and restart Redis services.
3. **Audit git history** for any other plaintext secrets using `git log --all --full-history -- '*.env*' '**docker-compose*'`.
4. **Consider git history rewrite** (BFG Repo Cleaner or `git filter-repo`) to purge the commit from history if the repository is private and all collaborators can accept a forced rewrite. If the repository has been cloned by CI systems, treat the credentials as permanently compromised regardless.
5. **Add pre-commit hook or CI check** (e.g., `git-secrets`, `truffleHog`, `detect-secrets`) to prevent future credential commits.

## Root Cause

A docker-compose file for the workers service was committed with inline environment variables containing production/staging secrets. The 2026-05-22 decision (secrets must not be tracked in version control; only `.env.example` is tracked) was not enforced at commit time for this file.

## Related

- Decision-Log 2026-05-22: secret files not tracked in repository
- EXP-140 (ZATCA debug event — related ZATCA security concern)
- EXP-142 (ZATCA_FORCE flags — related ZATCA issue)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
