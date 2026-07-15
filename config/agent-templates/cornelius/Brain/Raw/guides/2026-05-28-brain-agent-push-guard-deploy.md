---
title: Brain agent-push guard — operator deploy guide
date: 2026-05-28
linear: EXP-158
tracker: EXP-156
status: ready-to-deploy
source: "draft"
tags: [brain, guide, agent-push-guard, deploy]
category: "guide"
---

# Brain agent-push guard — operator deploy guide

## Context

EXP-151 flagged that R5/R7/R8 routines all have `allow_unrestricted_git_push: true` on `logi-x/brain` as a source. Each routine legitimately needs to push exactly one file:

| Routine                    | Writes to                                                              |
| -------------------------- | ---------------------------------------------------------------------- |
| R5 (gatekeeper)            | `Raw/agent-state/findings-index.md`, `Raw/agent-state/gatekeeper-*.md` |
| R7 (codebase-completeness) | `Raw/agent-state/findings-index.md`                                    |
| R8 (linear-board-audit)    | `Raw/agent-state/board-audit-log.md`                                   |
| R9 (routines-audit, new)   | `Raw/agent-state/routines-audit-log.md`                                |

The current grant lets a hijacked agent overwrite **any** file in the vault — `Wiki/Concepts/Auth.md`, `Decision-Log.md`, even `.github/workflows/*`. EXP-158 closes that.

## Why this is a workflow, not a git pre-receive hook

EXP-158's original spec asks for a server-side `pre-receive` hook. That is **only available on GitHub Enterprise**, not on github.com hosted repos. The closest enforcement on github.com is **post-hoc**: a workflow runs on `push`, validates changed paths, and on violation:

- Force-reverts the pushing commit(s)
- Posts to Slack `#experts-bug-bots`
- Files a Linear incident issue

This is **detection + auto-rollback**, not prevention. A hijacked agent can still push a bad commit; the workflow has it reverted within ~30s. That's a meaningfully smaller attack window than today's "unrestricted forever" — but it is not equivalent to true pre-receive.

If/when brain moves to GHE or a self-hosted git server, the real pre-receive hook is in §5 below for that future migration.

## Step 1 — Install the workflow

Create the directory and two files in the **brain repo** (`/home/logix/brain`).

```bash
cd /home/logix/brain
mkdir -p .github/workflows .github/scripts
```

### `.github/workflows/agent-push-guard.yml`

````yaml
name: Agent Push Guard

# EXP-158: github.com substitute for a pre-receive hook. Runs on push,
# validates that commits authored by agent service accounts only touch
# Raw/agent-state/<name>.md paths. On violation: force-revert, Slack
# alert, Linear incident issue.

on:
  push:
    branches: [main]

permissions:
  contents: write # needed for revert push
  issues: write # needed for Linear-side mirror (optional)

jobs:
  guard:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Checkout
        uses: actions/checkout@v6
        with:
          fetch-depth: 50
          token: ${{ secrets.GH_REVERT_TOKEN }}

      - name: Validate pushed commits
        id: validate
        env:
          PUSHER: ${{ github.event.pusher.name }}
          BEFORE: ${{ github.event.before }}
          AFTER: ${{ github.event.after }}
        run: bash .github/scripts/validate-agent-push.sh

      - name: Auto-revert violation
        if: steps.validate.outputs.violation == 'true'
        env:
          GH_TOKEN: ${{ secrets.GH_REVERT_TOKEN }}
        run: |
          git config user.email "bot@experts.logi-x"
          git config user.name  "brain-agent-push-guard"
          git revert --no-edit ${{ steps.validate.outputs.bad_commits }}
          git push origin main

      - name: Slack alert
        if: steps.validate.outputs.violation == 'true'
        env:
          SLACK_WEBHOOK_BUG_BOTS: ${{ secrets.SLACK_WEBHOOK_BUG_BOTS }}
          DETAIL: ${{ steps.validate.outputs.detail }}
        run: |
          [ -z "${SLACK_WEBHOOK_BUG_BOTS:-}" ] && { echo "::warning::no Slack webhook"; exit 0; }
          jq -n --arg t ":rotating_light: *brain agent-push guard tripped*" \
                --arg d "${DETAIL}" \
                '{text:$t, blocks:[
                  {type:"section", text:{type:"mrkdwn", text:$t}},
                  {type:"section", text:{type:"mrkdwn", text:("```\n" + $d + "\n```")}}
                ]}' \
          | curl -fsS -X POST -H 'Content-Type: application/json' --data @- "$SLACK_WEBHOOK_BUG_BOTS"

      - name: Pass
        if: steps.validate.outputs.violation != 'true'
        run: echo "All pushed commits within agent path allowlist."
````

### `.github/scripts/validate-agent-push.sh`

See the live file at `.github/scripts/validate-agent-push.sh`. Key design points:

- **Filters by commit author email**, not pusher login. The cloud CCR authenticates via the user's OAuth, so all pushes appear at the GitHub event level as the user. There is no distinct service-account login to filter on.
- Each routine prompt (R1/R2/R3/R5/R7/R8/R9) runs `git config user.email "agent@routines.experts.local"` + `git config user.name "routines-agent"` before committing to brain. The validator treats any commit authored by `agent@routines.experts.local` as agent-origin and enforces the path allowlist; any other author email is treated as human and passes unrestricted.
- A push containing **both** agent and human commits is validated per-commit (agent ones must respect the allowlist; human ones don't).
- Allowed paths: `^Raw/agent-state/[a-z0-9_-]+\.md$`

```bash
chmod +x .github/scripts/validate-agent-push.sh
```

## Step 2 — Provision secrets in the brain repo

```bash
# A PAT with `repo` scope, owned by the operator, used by the workflow
# to force the revert push. Do NOT use the default GITHUB_TOKEN —
# branch protection may block it from pushing to main.
gh secret set GH_REVERT_TOKEN --repo logi-x/brain --body '<your PAT>'

# Same Slack webhook as the experts repo uses (channel C0B4W24T6MU).
gh secret set SLACK_WEBHOOK_BUG_BOTS --repo logi-x/brain --body '<webhook URL>'
```

## Step 3 — Verify the agent identity in routine prompts (already done in EXP-158 follow-up)

The cloud CCR pushes under the user's OAuth identity, so the GitHub `actor.login` on push events is always the user — there is no distinct bot login. The guard distinguishes agent commits from human commits via **commit author email**:

| Identity | Email | Set by |
|---|---|---|
| Agent | `agent@routines.experts.local` | each routine prompt before committing to brain |
| Human | whatever your local `git config` is | manual commits |

Routines that set this identity (verified in `logi-x/experts` `.claude/routines/*.prompt.md`):

- R1 (`01-scan-vulnerabilities.prompt.md`)
- R2 (`02-find-critical-bugs.prompt.md`)
- R3 (`03-fix-bugs.prompt.md`)
- R5 (`05-gatekeeper.prompt.md`)
- R7 (`07-codebase-completeness-audit.prompt.md`)
- R8 (`08-linear-board-audit.prompt.md`)
- R9 (`09-routines-audit.prompt.md`)

If you add a new routine that pushes to brain, add the same two-line `git config` block before its commit step.

> _Historical note._ The validator originally filtered by `PUSHER`/`actor.login`, which doesn't work for OAuth-mediated CCR pushes. Switched to author-email filtering after EXP-158 follow-up audit on 2026-05-28.

## Step 4 — Smoke test

Two test cases. **Run on a feature branch first** (workflow runs on `push: branches: [main]` — test by temporarily adding your test branch name to the trigger then removing it).

### Case A — legitimate push (should pass)

Locally simulate an agent push of an allowed path:

```bash
cd /home/logix/brain
git config user.email "agent@routines.experts.local"
git config user.name  "routines-agent"
echo "smoke test $(date)" >> Raw/agent-state/findings-index.md
git add Raw/agent-state/findings-index.md
git commit -m "chore(agent-state): smoke test A"
git push origin main
# After push, reset your local identity:
git config --unset user.email
git config --unset user.name
```

Expected: workflow runs, logs "Agent push (1 commit[s]) within allowlist", exits 0. Nothing reverted.

### Case B — violation (should auto-revert + alert)

Locally simulate an agent push that touches a forbidden path:

```bash
cd /home/logix/brain
git config user.email "agent@routines.experts.local"
git config user.name  "routines-agent"
mkdir -p Entities/Topics
echo "vandalism $(date)" > Wiki/Concepts/SmokeTestB.md
git add Wiki/Concepts/SmokeTestB.md
git commit -m "chore(agent-state): smoke test B (should be reverted)"
git push origin main
# Reset identity:
git config --unset user.email
git config --unset user.name
```

Expected:

- Workflow detects violation, sets `violation=true`
- Auto-revert step runs, creates a "Revert ..." commit and pushes it
- Slack alert posted to `#experts-bug-bots` with offending paths
- `main` ends up at the post-revert state (`Wiki/Concepts/SmokeTestB.md` unchanged from before)

Then `git pull` locally to sync the revert.

## Step 5 — When brain moves to GHE / self-hosted (future)

Replace the workflow above with a true pre-receive hook on the git server. Pseudocode:

```bash
#!/usr/bin/env bash
# pre-receive hook on logi-x/brain (future GHE/self-hosted)
AGENT_EMAIL="agent@routines.experts.local"
while read oldsha newsha refname; do
  [ "$refname" != "refs/heads/main" ] && continue
  for sha in $(git rev-list "${oldsha}..${newsha}"); do
    author_email=$(git show -s --format='%ae' "$sha")
    [ "$author_email" = "$AGENT_EMAIL" ] || continue
    for path in $(git show --pretty='' --name-only "$sha"); do
      [[ "$path" =~ ^Raw/agent-state/[a-z0-9_-]+\.md$ ]] || {
        echo "ERROR: agent commit $sha cannot touch $path" >&2
        exit 1
      }
    done
  done
done
exit 0
```

True pre-receive **prevents** the bad commit from ever landing — strictly stronger than the post-hoc workflow.

## Operator checklist

- [ ] Files created in brain repo under `.github/`
- [ ] `GH_REVERT_TOKEN` secret set on brain repo
- [ ] `SLACK_WEBHOOK_BUG_BOTS` secret set on brain repo
- [ ] Routine prompts in `logi-x/experts/.claude/routines/*.prompt.md` set `git config user.email "agent@routines.experts.local"` before commit (verified by EXP-158 follow-up)
- [ ] Smoke test Case A — passes
- [ ] Smoke test Case B — reverts + alerts
- [ ] Close EXP-158 with link to merged brain-side PR

## Notes

- The workflow runs on `push: branches: [main]`. If agents push to feature branches that get merged in, the guard fires at merge-into-main time — still effective but the violating commit lives briefly on the feature branch first. Acceptable for an "auto-revert detection" surface; not acceptable as a true gate.
- If the agent push is force-pushed (rewriting history), the `revert` strategy fails. Mitigate by enabling branch protection on `main` to disable force-push from any account. This is recommended regardless of EXP-158.
- The Linear incident-issue side (filing an issue on violation) is intentionally NOT in v1. Slack alert is enough for first signal; promoting to Linear after first false-alarm-free cycle is a small follow-up.
