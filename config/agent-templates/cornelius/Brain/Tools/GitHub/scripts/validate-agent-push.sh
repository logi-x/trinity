#!/usr/bin/env bash
# EXP-158 agent-push validator for logi-x/brain.
#
# Filters by COMMIT AUTHOR EMAIL, not pusher login. The cloud CCR
# authenticates via the user's OAuth so all pushes appear as the user
# at the GitHub event level. To distinguish, each routine prompt runs
#   git config user.email "agent@routines.experts.local"
#   git config user.name  "routines-agent"
# before committing to brain. Any commit authored by that email is
# subject to the path allowlist; commits with any other author email
# are treated as human and pass unrestricted.
#
# Inputs (env):  PUSHER, BEFORE, AFTER (PUSHER is unused; kept for
#                forward compatibility / debugging).
# Outputs (GITHUB_OUTPUT): violation=true|false,
#                          bad_commits=<sha sha>, detail=<markdown>.

set -euo pipefail

: "${BEFORE:?BEFORE must be set}"
: "${AFTER:?AFTER must be set}"

AGENT_AUTHOR_EMAIL="agent@routines.experts.local"

# Per-routine path allowlist. Update when adding new agent-writing routines.
ALLOW_REGEX='^raw/agent-state/[a-z0-9_-]+\.md$'

bad_commits=()
bad_paths=()

# Handle initial branch creation (BEFORE all zeros) by treating it as
# no prior history.
if [[ "$BEFORE" =~ ^0+$ ]]; then
  commit_range="$AFTER"
else
  commit_range="${BEFORE}..${AFTER}"
fi

agent_commits_seen=0

for sha in $(git rev-list "$commit_range"); do
  author_email=$(git show -s --format='%ae' "$sha")
  # Only enforce on agent-authored commits; humans are free to touch
  # anything in their own pushes.
  if [ "$author_email" != "$AGENT_AUTHOR_EMAIL" ]; then
    continue
  fi
  agent_commits_seen=$((agent_commits_seen + 1))
  while IFS= read -r path; do
    [ -z "$path" ] && continue
    if ! [[ "$path" =~ $ALLOW_REGEX ]]; then
      bad_commits+=("$sha")
      bad_paths+=("${sha:0:7}:$path")
    fi
  done < <(git show --pretty='' --name-only "$sha")
done

if [ ${#bad_commits[@]} -eq 0 ]; then
  echo "violation=false" >> "$GITHUB_OUTPUT"
  if [ "$agent_commits_seen" -eq 0 ]; then
    echo "No agent-authored commits in push range; guard does not apply."
  else
    echo "Agent push (${agent_commits_seen} commit[s]) within allowlist."
  fi
  exit 0
fi

# Dedup bad_commits (a single commit may touch multiple bad paths).
mapfile -t uniq_commits < <(printf "%s\n" "${bad_commits[@]}" | awk '!seen[$0]++')

detail="Agent author: $AGENT_AUTHOR_EMAIL\nPusher (informational): ${PUSHER:-unknown}\nDisallowed paths:\n"
for entry in "${bad_paths[@]}"; do
  detail="${detail}- $entry\n"
done
detail="${detail}\nAllowed only: $ALLOW_REGEX"

{
  echo "violation=true"
  echo "bad_commits=${uniq_commits[*]}"
  echo "detail<<__EOF__"
  printf "%b" "$detail"
  echo
  echo "__EOF__"
} >> "$GITHUB_OUTPUT"
