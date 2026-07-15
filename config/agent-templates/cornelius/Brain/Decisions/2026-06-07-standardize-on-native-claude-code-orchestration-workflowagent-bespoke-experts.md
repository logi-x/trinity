---
title: "Standardize on native Claude Code orchestration (Workflow/Agent) + bespoke Experts agents + gitnexus; drop the ruflo/cla"
date: "2026-06-07"
decision: "Standardize on native Claude Code orchestration (Workflow/Agent) + bespoke Experts agents + gitnexus; drop the ruflo/claude-flow agent + skill pack. Keep exactly one Experts-specific `browser-agent.md"
stakeholders: "Logix"
review_by: "2026-09-07"
source: "[[Raw/sources/2026-06-07-experts-decision-blocked-five]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Standardize on native Claude Code orchestration (Workflow/Agent) + bespoke Experts agents + gitnexus; drop the ruflo/claude-flow agent + skill pack. Keep exactly one Experts-specific `browser-agent.md` (Claude Code `.md` agent wired to the agent-browser skill + Playwright MCP), not the ruflo browser YAML.

**Rationale:** The ruflo/claude-flow agents and skills are generic, runtime-coupled (`npx claude-flow@v3alpha` hooks), carry no Experts knowledge, over-grant tools, and duplicate native features; `agentdb-vector-search` etc. contradict the real pgvector stack. The bespoke top-level agents encode project ground-truth (HeroUI v3 MCP, React-19 rules, `experts:check`, commit discipline), and the native `Workflow` tool already gives swarm/SPARC-style fan-out without the alpha-runtime dependency. gitnexus is the only genuine, indexed, repo-grounded code-intel tool. **Execution:** `browser-agent.md` created; 17 ruflo skills already deleted (uncommitted); the 6 agent subdirs + 13 ruflo skill dirs flagged for removal (not yet committed).

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-06-07-experts-decision-blocked-five]]
