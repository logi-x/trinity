# Agent template catalog (Logix)

Ready-made starting points for deploying an agent on this Trinity instance.

**Logix consulting agents** (Scout, Sage, Scribe, Atlas) are maintained as GitHub repos under [`logi-x`](https://github.com/logi-x) and checked out at `/home/logix/logix-agents/`. Prefer:

```text
github:logi-x/logix-scout | logix-sage | logix-scribe | logix-atlas
```

via `/trinity:onboard` / sync — not hand-editing this catalog. Thin `local:scout|sage|scribe|atlas` copies exist as bootstrap mirrors only; they can lag the repos.

> Agent entry point: [`AGENTS.md`](../../AGENTS.md) → [Deploy an agent](../../AGENTS.md#deploy-an-agent-to-trinity). Full schema: [`docs/TRINITY_COMPATIBLE_AGENT_GUIDE.md`](../../docs/TRINITY_COMPATIBLE_AGENT_GUIDE.md).

## How to use a template

- **Logix consulting agents** — work in `/home/logix/logix-agents/<repo>`, push, `/trinity:sync`.
- **From a checkout** — copy a template directory, edit, deploy: `cd <copy>/ && trinity deploy .`
- **From the web UI** — *Create Agent* → pick a template by `name`.
- **Fleet recipe (optional)** — `config/manifests/logix-consulting.yaml` (greenfield/DR only; not a living roster).

## Starter templates

### Single-purpose (local mirrors)

| `name` | Canonical repo | Role |
|--------|----------------|------|
| `scout` | `github:logi-x/logix-scout` | Market research (GCC / product / client briefs) |
| `sage` | `github:logi-x/logix-sage` | Strategy from Scout (+ Cornelius) |
| `scribe` | `github:logi-x/logix-scribe` | Client deliverables from Scout + Sage |
| `atlas` | `github:logi-x/logix-atlas` | General assistant / orchestrator |
| `cornelius` | `local:cornelius` | Second brain / KB |

Deployed agent names are typically `logix-scout`, `logix-sage`, `logix-scribe`, `logix-atlas`. Link each to `cornelius` for scoped answers.

### Due-diligence suite (coordinated multi-agent)

Logix investment / diligence pipeline: `dd-intake` parses a pitch deck, nine specialists assess one dimension each, and `dd-lead` synthesizes a risk score and recommendation.

| `name` | Dimension |
|--------|-----------|
| `dd-intake` | Parse pitch decks → structured data for the specialists |
| `dd-lead` | Synthesize all findings → risk score + go/no-go |
| `dd-market` | TAM/SAM/SOM, growth, market headwinds |
| `dd-tech` | Technology, scalability, IP |
| `dd-founder` | Background checks, track record, controversy |
| `dd-traction` | Growth metrics, financial health, data accuracy |
| `dd-bizmodel` | Revenue model, unit economics, path to profitability |
| `dd-captable` | Equity structure, dilution, investor reputation |
| `dd-competitor` | Competitive landscape, market share, threats |
| `dd-compliance` | Regulatory landscape, compliance, market entry |
| `dd-legal` | Corporate structure, IP ownership, contracts |

## Not starting points

These directories are **excluded from the user-facing catalog** (`hidden: true`). They stay deployable by id for tests and demos.

- **Test/canary fixtures** — `test-echo`, `test-counter`, `test-delegator`, `test-codex`, `test-gemini`, `test-leak-hook`, `sleep-echo`. Do **not** deploy `test-leak-hook` in production.
- **Demo fixtures** — `demo-researcher`, `demo-analyst`. Logix research-network pair (`config/manifests/research-network.yaml`).
- **Platform agent** — `logix-system`. Auto-deployed and deletion-protected; not something you create yourself.

Adding a new fixture? Set `hidden: true` in its `template.yaml` (guarded by `tests/unit/test_local_templates_listing.py`).
