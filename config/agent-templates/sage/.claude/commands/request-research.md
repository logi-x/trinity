---
description: Ask Scout to research a specific topic
argument-hint: "[topic]"
allowed-tools: mcp__trinity__*
---

# Request Research

Ask Scout to research: **$ARGUMENTS**

```
mcp__trinity__chat_with_agent(
  agent_name="logix-scout",
  message="/research $ARGUMENTS",
  parallel=true,
  async=true
)
```

If `list_agents()` shows a different Scout name, use that. Report the execution_id / acknowledgment to the user. Do not invent Scout's findings - wait for or poll the result when needed.
