---
description: Route and supervise a multi-agent task
argument-hint: "[goal]"
allowed-tools: Read, Write, Glob, mcp__trinity__*
---

# Orchestrate

Coordinate: **$ARGUMENTS**

## Steps

1. Ask `logix-steward` to create or return a stable task ID, acceptance criteria, owner, and lifecycle record.
2. Decompose work into independent stages. Route research to Scout, evidence review to Sentinel, strategy to Sage, product/solution definition to Forge, and client writing to Scribe.
3. Include the task ID, expected artifact stage, inputs, and acceptance criteria in every delegation.
4. Never duplicate a still-running request. On failure, diagnose and retry at most once.
5. Require Sentinel verification before evidence-bearing research reaches strategy and before a deliverable is described as client-ready.
6. Notify Steward on every dispatch, block, handoff, verification result, approval, and closeout.
7. Return one assembled result with artifact paths, verification states, unresolved questions, and next action.
