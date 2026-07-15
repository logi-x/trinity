---
description: Create a stable task and lifecycle record
argument-hint: "[goal]"
allowed-tools: Read, Write, Glob, Bash(mkdir:*), mcp__trinity__*
---

# Intake

1. Check active ledgers for a duplicate outcome.
2. Assign a stable task ID; capture goal, engagement, requester, acceptance criteria, owner, constraints, priority, and due date only when known.
3. Record stages, agents, dependencies, and Sentinel gates.
4. Write `/home/developer/shared-out/operations/tasks/{task-id}.md` and append the intake event.
5. Return the task ID, state, owner, next action, and ledger path.
