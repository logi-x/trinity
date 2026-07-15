#!/bin/bash

# Add a label to a GitHub issue or pull request

# Usage: gh-add-label.sh <issue-or-pr-number> <label>

# Example: gh-add-label.sh 1234567890 "bug"

# Get the issue or pull request number from the command line
issue_or_pr_number=$1
# default to gatekeeper-merge-now
label=${2:-"gatekeeper-merge-now"}

# Add the label to the issue or pull request
echo "---add to PR $issue_or_pr_number via REST---";
gh api -X POST repos/logi-x/experts/issues/$issue_or_pr_number/labels -f "labels[]=$label" --jq '[.[].name]'