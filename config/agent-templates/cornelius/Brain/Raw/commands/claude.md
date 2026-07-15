brain-vault plugin

Location: ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/brain-vault/

7 commands, auto-loaded on next session:

┌────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Command │ What it does │
├────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ /brain <cmd> │ Raw CLI passthrough — any obsidian command, or natural language routing │
├────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ /brain-search <query> │ Full-text search with context lines, grouped by file │
├────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ /brain-daily [read|add|tasks|prepend] │ Today's daily note — read, append, or list tasks │
├────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ /brain-tasks [todo|done|file=|toggle] │ Tasks across the vault with line-number refs for toggling │
├────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ /brain-ingest <source> │ Full 6-step ingest: read source → write summary → update entities → update Index.md → append │
│ │ Log.md │
├────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ /brain-query <question> │ Search + synthesize with `WikiLink` citations, offer to file the result │
├────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ /brain-lint │ Vault health check — orphans, broken links, stale content, missing cross-refs │
│ [full|orphans|unresolved|stale] │ │
└────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────┘

The skill /obsidian (created earlier) remains as a general-purpose vault interaction tool. The new plugin commands are more opinionated — they know
the vault structure, follow the CLAUDE.md workflows (ingest, query, lint), and handle the multi-step operations automatically.

Note: The new commands will appear after restarting Claude Code (the plugin directory is scanned at session start).
