#!/bin/bash

# Clean up cancelled and failed actions in the Experts repository

# List all cancelled actions
gh run list \
    --repo logi-x/experts \
    --status cancelled \
    --limit 1000 \
    --json databaseId \
    --jq '.[].databaseId' \
  | xargs -P 4 -I {} gh run delete --repo logi-x/experts {}

# # List all failed actions
# gh run list \
#     --repo logi-x/experts \
#     --status failed \
#     --limit 1000 \
#     --json databaseId \
#     --jq '.[].databaseId' \
#   | xargs -P 4 -I {} gh run delete --repo logi-x/experts {}