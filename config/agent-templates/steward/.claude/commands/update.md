---
description: Append a task event and update current state
argument-hint: "[task-id] [event]"
allowed-tools: Read, Write, Glob, mcp__trinity__*
---

# Update

1. Read the existing ledger and verify the event belongs to the task.
2. Append timestamp, actor, event, artifact/verdict reference, and resulting state.
3. Do not erase or silently rewrite prior history.
4. Return current state, blocker if any, and next action.
