---
title: "CLI"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/cli"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
source_id: "docs/cli/overview.md"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# CLI (`logix`)

Phase 2 command interface — package `@logix/cli` in `apps/cli`, talks to the Fastify API through `@logix/sdk`. Supports humans, scripts, agents, runners, Obsidian workflows, n8n-style hooks, and MCP tools. Does **not** execute autonomous repository changes.

## Build and link

```bash
npx pnpm@11.9.0 --filter @logix/cli build
npx pnpm@11.9.0 cli:link
logix status --json
```

## Config

File: `~/.config/logix/config.json`

Environment overrides: `LOGIX_BASE_URL`, `LOGIX_TOKEN`, `LOGIX_PROFILE`, `LOGIX_WORKSPACE`, `LOGIX_PROJECT`, `LOGIX_RUNNER`, `LOGIX_OUTPUT`.

Prefer **`--json`** (or `--ndjson` for streams) for agent-facing commands.

Success envelope: `{ "ok": true, "data": {}, "meta": { "profile": "local" } }`  
Error envelope: `{ "ok": false, "error": { "code": "CLI_ERROR", "message": "..." } }`

## Deeper topics (repo only)

Read in the checkout under `docs/cli/` — not mirrored here to avoid drift with implementation plans:

| Repo path | Topic |
| --------- | ----- |
| `docs/cli/human-usage.md` | Operator workflows |
| `docs/cli/agent-usage.md` | Agent/automation patterns |
| `docs/cli/sdk.md` | SDK alignment |
| `docs/cli/runner-protocol.md` | Runner protocol (Phase 3 prep) |
| `docs/cli/obsidian-sync.md` | Vault sync hooks |
| `docs/cli/n8n-hooks.md` | Webhook-style hooks |

See [[Projects/Logix/KERNEL/docs/roadmap/phases-and-tracks|Phases and tracks]] for CLI/MCP parity work (Phase 2.1).
