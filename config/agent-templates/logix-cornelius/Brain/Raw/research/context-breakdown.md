I have a clear picture. The 64,256 tokens is not your codebase — it's the fixed "preamble" the harness injects before your first message. Here's the breakdown.

Where the 64K comes from

┌───────────────────────────────────────────────────────────────────────────┬───────────┬───────────────────────────────────────────────────────┐
│ Component │ Est. │ Source │
│ │ tokens │ │
├───────────────────────────────────────────────────────────────────────────┼───────────┼───────────────────────────────────────────────────────┤
│ Built-in tool schemas (Bash, Read, Edit, Agent, Workflow, ScheduleWakeup, │ ~14–18K │ The Workflow tool alone is ~6K; these ship with │
│ AskUserQuestion…) │ │ Claude Code │
├───────────────────────────────────────────────────────────────────────────┼───────────┼───────────────────────────────────────────────────────┤
│ Deferred MCP tool-name list (the giant CronCreate…mcp\_\_st│ MCP_DOCKER gateway + http servers │
echo "=== agent .md definitions (count + size) ==="
find /home/logix/experts/.claude/agents ~/.claude/agents -nl
cat /home/logix/experts/.claude/agents/_.md ~/.claude/agents/_.md 2>/dev/null | wc -c)
Approx token contributions (chars/4):

SessionStart hook (superpowers using-superpowers SKILL.m

Where the 64K comes from

┌───────────────────────────────────────────────────────────────────────────┬───────────┬───────────────────────────────────────────────────────┐
│ Component │ Est. │ Source │
│ │ │
├──────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────┤
│ Built-in tool schemas (Bash, Read, Edit, Agent, Workflow, ScheduleWakeup, │ ~14–18K │ The Workflow tool alone is ~6K; these ship with │
│ AskUserQuestion…) │ │ Claude Code │
├───────────────────────────────────────────────────────────────────────────┼───────────┼───────────────────────────────────────────────────────┤
│ Deferred MCP tool-name list (the giant CronCreate…mcp\_\_st│ MCP_DOCKER gateway + http servers │
│ ~1.5K │ superpowers plugin auto-injects on every session │
├───────────────────────────────────────────────────────────────────────────┼───────────┼───────────────────────────────────────────────────────┤
│ MEMORY.md (auto-memory index, ~80 lines) │ ~4K │ ~/.claude/projects/.../memory/MEMORY.md │
├───────────────────────────────────────────────────────────────────────────┼───────────┼───────────────────────────────────────────────────────┤
│ Base system prompt + env + CLAUDE.md + rules │ ~6–8K │ Harness + your config │
└──────────────────────────────────────────────────────────┴───────────────────────────────────────────────────────┘

The dominant, non-fixed levers are the MCP tool catalog, the 99 agent definitions, the skills catalog, and MEMORY.md — everything driven by your plugin/MCP config in ~/.claude/settings.json.

Combined with 23 enabled plugins, you're loading the catalog for a lot of capability you rarely use in a given session.

What you can trim (and roughly how much)

1. Prune MCP_DOCKER profile — biggest win. The default proft to what you actually use (gitnexus, codegraph, github,linear) → saves ~4–6K plus their agents/skills.
2. Disable unused plugins in ~/.claude/settings.json enableps, mcp-tunnels, ralph-loop if idle → each plugin's
3. Trim MEMORY.md — it's ~4K and growing (~80 one-liners). Archive stale project\_\* entries (shipped epics like #966, #1101, #1040) into a non-loaded file → saves ~1.5–2K.
4. Set enableAllProjectMcpServers: false and list only the servers you need per project.

Want me to (a) measure exact per-component token counts prerim — e.g. archive the shipped-epic memories and propose anarrower MCP/plugin set? I'd recommend (b) starting with MEMORY.md and the plugin list since those are safe and reversible.
