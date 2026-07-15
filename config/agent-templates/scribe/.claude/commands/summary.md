---
description: Create a provenance-preserving executive summary
argument-hint: "[task-id] [source-file]"
allowed-tools: Read, Write, Glob, Bash(mkdir:*), mcp__trinity__*
---

# Summary

1. Verify the source artifact identity and state.
2. Compress it without adding facts, changing numbers, or dropping material qualifications.
3. Preserve claim IDs and citations.
4. Save to `/home/developer/shared-out/deliverables/summaries/{task-id}-deliverable-r{N}.md`.
5. Ask Sentinel to verify fidelity and notify Steward.
