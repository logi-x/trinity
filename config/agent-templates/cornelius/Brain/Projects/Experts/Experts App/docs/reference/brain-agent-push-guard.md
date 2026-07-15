---
title: Brain agent-push guard
date: 2026-06-01
linear: EXP-158
tracker: EXP-156
status: ready-to-deploy
category: "docs/experts-reference"
source: experts-app
source_id: Projects/Experts/Experts App/docs/security/brain-agent-push-guard.md
tags: [security, project/experts, app]
updated: "2026-07-15"
---

# brain agent-push guard

Cross-repo enforcement surface for EXP-158. The actual workflow + script live on `logi-x/brain`; this doc explains the experts-side context and links to the brain-side deploy.

## Why this exists

The R5 / R7 / R8 / R9 cloud triggers list `https://github.com/logi-x/brain` as a source with `allow_unrestricted_git_push: true`. Each routine legitimately writes one file under `Raw/agent-state/`. The grant is necessarily broad on the cloud-trigger side (CCR offers no path-scoped push grant). The narrow allowlist is enforced **on the brain repo's receive side**.

## Where the enforcement lives

| Layer                                    | Repo           | File                                                                                                |
| ---------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------- |
| Cloud trigger source declaration         | (CCR cloud)    | per routine JSON in `.claude/routines/*.json`                                                       |
| Receive-side path validator (this guard) | `logi-x/brain` | `.github/workflows/agent-push-guard.yml` + `.github/scripts/validate-agent-push.sh`                 |
| Allowed paths                            | `logi-x/brain` | regex `^Raw/agent-state/[a-z0-9_-]+\.md$` in the validator script                                   |
| Agent identity (commit author email)     | both repos     | `agent@routines.experts.local` — set by each routine prompt before commit; matched by the validator |

## Deploy

Operator deploys per `~/brain-v2/Raw/guides/2026-05-28-brain-agent-push-guard-deploy.md` (not in this repo — it's the brain-side runbook).

## Limitations

GitHub.com does not support `pre-receive` hooks (GHE-only). The guard runs **post-hoc** via a `push`-triggered workflow that auto-reverts violations and posts to Slack `#experts-bug-bots`. This is **detection + auto-rollback within ~30s**, not true prevention. When brain moves to GHE/self-hosted, replace with the pre-receive hook drafted in the guide §5.

## How agent commits are distinguished

The cloud CCR authenticates via the user's OAuth, so all pushes appear as the user at the GitHub event level. The guard differentiates via **commit author email**:

- Each routine prompt (R1/R2/R3/R5/R7/R8/R9) runs `git config user.email "agent@routines.experts.local"` + `git config user.name "routines-agent"` before committing to brain.
- The validator enforces the path allowlist on commits authored by `agent@routines.experts.local`. Any other author email passes unrestricted.
- A push containing both agent and human commits is validated per-commit (agent ones must respect the allowlist; human ones don't).

## Routine path allowlist (canonical)

When adding a new agent-writing routine, update **both**:

1. The routine's prompt to (a) set the agent identity via `git config` and (b) write only to `Raw/agent-state/<name>.md`
2. The brain validator's allowlist regex (if the file pattern doesn't match)

Currently the regex covers all files matching `^Raw/agent-state/[a-z0-9_-]+\.md$` so per-routine updates are usually unnecessary.

| Routine                    | Path                                                                   |
| -------------------------- | ---------------------------------------------------------------------- |
| R5 (gatekeeper)            | `Raw/agent-state/findings-index.md`, `Raw/agent-state/gatekeeper-*.md` |
| R7 (codebase-completeness) | `Raw/agent-state/findings-index.md`                                    |
| R8 (linear-board-audit)    | `Raw/agent-state/board-audit-log.md`                                   |
| R9 (routines-audit)        | `Raw/agent-state/routines-audit-log.md`                                |

## Linear

- EXP-158 — this guard
- EXP-156 — autonomy hardening tracker (parent)
- EXP-151 — original `allow_unrestricted_git_push` finding

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
