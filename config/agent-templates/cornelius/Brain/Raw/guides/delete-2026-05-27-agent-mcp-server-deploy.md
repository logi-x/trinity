---
title: "experts-agent-mcp — deploy + claude.ai connector registration"
status: operator-action-required
created: 2026-05-27
relates_to: "EXP-157 (parent: EXP-156)"
source: "draft"
tags: [project/experts, guide, agent-mcp, deploy]
category: "guide"
owner: "Ahmed Sulaimani"
---

# experts-agent-mcp deploy guide

The `experts-agent-mcp` service (built in PR `feat/exp-157-agent-mcp-server`) exposes arg-validated `rg` / `git log` / `gh` tools so the autonomous Claude routine agents (R5, R7, R8) can stop carrying `Bash` in their `allowed_tools`. The code, tests, and docker-compose wiring landed in the repo. What's left is **infrastructure I cannot do from the codebase**.

This guide walks the four operator-side steps in order. Each one is independently verifiable; complete them top-to-bottom and verify the smoke test at the end.

---

## Step 1 — DNS

Add two A (or AAAA) records pointing at the existing experts VPS public IP:

| Host                     | Type | Target                    |
| ------------------------ | ---- | ------------------------- |
| `mcp.experts.com.sa`     | A    | _existing experts VPS IP_ |
| `mcp.stg.experts.com.sa` | A    | _existing experts VPS IP_ |

Or, if you front everything via Cloudflare, add two CNAMEs pointing at the existing experts hostnames.

**Verify:**

```bash
dig +short mcp.experts.com.sa
dig +short mcp.stg.experts.com.sa
# both should return the VPS IP
```

Traefik's existing `experts` cert resolver (Let's Encrypt or ZeroSSL — whichever you have wired) will pick up the new hosts on first request after the compose pull. Nothing more on Traefik's side; the labels in the new docker-compose blocks handle the router config.

---

## Step 2 — Generate the two secrets

Both environments need their own values. Store them per-environment in the corresponding `.env` file.

### `MCP_API_TOKEN`

A high-entropy random string. Used by the cloud CCR triggers to authenticate to your server via `Authorization: Bearer <token>`. Constant-time comparison server-side.

```bash
# 32 bytes hex = 64-char string. Generate once per environment.
openssl rand -hex 32
```

Put each value into:

- `docker/production/.env` as `MCP_API_TOKEN=<value>`
- `docker/staging/.env` as `MCP_API_TOKEN=<different-value>`

### `MCP_GH_TOKEN`

A GitHub fine-grained PAT scoped to **read-only on `logi-x/experts` and `logi-x/brain`**. The `gh` wrapper uses this; under no circumstances should it have write scopes (the wrapper itself rejects mutating subcommands, but defence in depth).

1. https://github.com/settings/personal-access-tokens/new
2. Resource owner: `logi-x` (the org)
3. Repository access: **Only select repositories** → `logi-x/experts`, `logi-x/brain`
4. Permissions → Repository permissions:
   - Contents: **Read-only**
   - Issues: **Read-only**
   - Metadata: **Read-only** (default)
   - Pull requests: **Read-only**
   - (everything else: No access)
5. Expiry: 90 days. Note the rotation date in your calendar.
6. Generate, copy. Paste once.

Put each value into:

- `docker/production/.env` as `MCP_GH_TOKEN=<token>`
- `docker/staging/.env` as `MCP_GH_TOKEN=<token>` (can be same or different — same is fine if you trust both equally)

**Verify the PAT is read-only** before saving:

```bash
GH_TOKEN=<paste> gh api -X POST repos/logi-x/experts/issues -f title=test
# Must return 403 / "Resource not accessible by personal access token"
GH_TOKEN=<paste> gh api repos/logi-x/experts/commits --paginate=false
# Must return 200 + commit list
```

---

## Step 3 — Build + deploy the container

After PR `feat/exp-157-agent-mcp-server` merges to main:

```bash
# On the VPS, in the experts repo root:
cd docker/production
docker compose build experts-prd-agent-mcp
docker compose up -d experts-prd-agent-mcp

# Verify healthcheck flips to "healthy" within ~30s:
docker ps --filter name=experts-prd-agent-mcp --format '{{.Names}}\t{{.Status}}'
# expected: experts-prd-agent-mcp ... Up X seconds (healthy)

# Verify the public endpoint responds (no auth on /health):
curl -fsS https://mcp.experts.com.sa/health
# expected: {"status":"ok"}
```

Repeat for staging if/when you want it there too:

```bash
cd docker/staging && docker compose build experts-stg-agent-mcp && docker compose up -d experts-stg-agent-mcp
curl -fsS https://mcp.stg.experts.com.sa/health
```

### The `/repo` mount

The container expects `/repo` to be a checked-out copy of `logi-x/experts` (the wrappers `cd` into it for `git log`, `rg`, etc.). The compose file bind-mounts `/opt/experts-repo` from the host. Set this up once per host:

```bash
# On the VPS:
sudo git clone https://github.com/logi-x/experts.git /opt/experts-repo
sudo chown -R $(id -u):$(id -g) /opt/experts-repo
```

Then keep it fresh — recommended via cron every 15 minutes:

```bash
# /etc/cron.d/experts-mcp-repo-sync
*/15 * * * * logix cd /opt/experts-repo && git fetch --quiet origin && git reset --hard origin/main 2>&1 | logger -t experts-mcp-repo-sync
```

Rationale: bind-mount instead of in-image clone avoids rebuilding the image on every code change. The `--hard origin/main` is intentional — the mount is read-only inside the container, so local divergence is impossible from the server side; this just protects against host-side accidental edits.

---

## Step 4 — Register the MCP connector in claude.ai

This step has no CLI — it's a web UI flow in claude.ai workspace settings.

1. Open https://claude.ai/settings/connectors (Workspace owner only)
2. Click **Add Connector** → **Add custom connector**
3. Fill in:
   - **Name:** `Experts Agent MCP` (matches the connector_uuid we'll wire into the trigger configs)
   - **URL:** `https://mcp.experts.com.sa/mcp`
   - **Authentication:** Custom header (or "API key" if presented that way)
     - Header name: `Authorization`
     - Header value: `Bearer <the MCP_API_TOKEN you generated for production>`
4. Save. claude.ai will probe the URL; you should see "3 tools discovered: agent_rg, agent_git_log, agent_gh". If discovery fails, check:
   - DNS resolves
   - Traefik issued a cert (check Traefik logs)
   - Container is `(healthy)`
   - Token matches exactly
5. **Copy the connector UUID** that claude.ai assigns. It looks like `82fb2281-bcd6-4abc-b2a7-74601b085bf6` (similar to the existing Linear/Slack connector UUIDs). Paste it into this guide below for the next step:

```
# Fill these in after registering:
CONNECTOR_UUID_AGENT_MCP_PRD = ______________________________________________
CONNECTOR_UUID_AGENT_MCP_STG = ______________________________________________  # only if you registered staging
```

If you want the staging server discoverable from claude.ai too, repeat with `https://mcp.stg.experts.com.sa/mcp` and the staging token. Typically only production is needed — staging is for your own pre-deploy validation.

---

## Step 5 — Wire the connector into R5 / R7 / R8 triggers + drop `Bash`

Once Step 4 gives you a `CONNECTOR_UUID_AGENT_MCP_PRD`, ping me (Claude) in chat and I'll do the cloud trigger updates via the `RemoteTrigger` MCP tool. The pattern per trigger:

1. Add a new entry to `mcp_connections` referencing the new `connector_uuid` with `permitted_tools: ["agent_rg", "agent_git_log", "agent_gh"]`.
2. Drop `"Bash"` from `allowed_tools` (and `"WebFetch"` while we're there, for R5 — it was already dropped from R7).
3. Update the prompt to instruct: "Use the `agent_rg` / `agent_git_log` / `agent_gh` MCP tools instead of `Bash` for grep, git history, and gh CLI invocations. Bash is no longer granted."

Same for the local routine JSONs in `.claude/routines/` so cloud + local stay in sync.

I'll also update both `.claude/agents/codebase-completeness-auditor.md` and `.claude/agents/linear-board-auditor.md` to drop `Bash` from their `tools:` lines and add the three new tool names.

---

## Verify end-to-end

After the wiring lands and the first scheduled R7 or R8 run fires:

1. Tail Slack `#experts-bug-bots` for the run summary.
2. `docker logs experts-prd-agent-mcp --tail 100 | grep call_id` — you should see JSON lines for each tool call from the routine, with `ms` and `output_bytes`.
3. Try a deliberate injection: file a test Linear comment with `Closes EXP-9999; rm -rf /` and wait for R8's next run. The validator should reject the embedded shell metacharacters; you'll see a `validation_rejected` log line.

---

## Outstanding actions for credential lifecycle

- [ ] Calendar reminder 80 days from `MCP_GH_TOKEN` creation — rotate the PAT.
- [ ] Calendar reminder 180 days from `MCP_API_TOKEN` creation — rotate the bearer.
- [ ] When rotating either: update the `.env`, `docker compose up -d --no-deps experts-prd-agent-mcp` to restart, and update the claude.ai connector header value.

## Related

- Linear EXP-157 — this server's tracking issue
- Linear EXP-156 — parent tracker (Agent autonomy hardening)
- Linear EXP-143, EXP-151 — close when EXP-157 ships + the routine grants are flipped
- Repo: `apps/experts-agent-mcp/` — source, tests, Dockerfile, README
- Compose: `docker/production/docker-compose.yml` + `docker/staging/docker-compose.yml` — service blocks added in same PR
