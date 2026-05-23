# CLAUDE.md Review - Agent System Prompt Best Practices
**Date:** 2026-05-11
**Reviewed by:** Cornelius (claude-sonnet-4-6)

---

## Summary

The current CLAUDE.md is a solid developer onboarding document but reads more like a reference manual than an agent system prompt. Three structural issues reduce its effectiveness: no character/identity layer, inverted section ordering (security warnings before identity), and imperative rules without constitutive reasoning. The fixes are low-effort and high-impact.

**Priority changes:**

| Priority | Change | Effort |
|----------|--------|--------|
| High | Add character/identity layer at top | 5 min |
| High | Reorder: Character → Knowledge → Rules → Reference | 15 min |
| High | Add autonomy boundary section | 5 min |
| Medium | Add "why" to each Rule of Engagement | 10 min |
| Medium | Compress security section, move checklist to `docs/SECURITY.md` | 10 min |
| Low | Extract commands/structure to @-referenced files | 20 min |
| Low | Consolidate "Important Notes" into relevant sections | 15 min |

---

## Recommendation 1: Fix the Layer Ordering (Highest Impact)

**Principle:** Character → Knowledge → Rules → Output format (Karpathy 2025, Layered System Prompt Architecture).

Right now the file opens with 40+ lines of security warnings before the agent knows what it is. The security section is important but belongs in Rules, not as the opening frame.

**Current order:**
1. Security warning (40+ lines)
2. Project overview
3. Remote agent
4. SDLC
5. Rules of Engagement
6. Memory files
7. Commands / structure / notes / auth / quick reference

**Recommended order:**
1. Identity/Purpose - who this agent is, what it owns
2. Core decision philosophy - 2-3 constitutive principles
3. Knowledge context - architecture, memory files, key files
4. Rules of Engagement (including security)
5. Quick reference - or @-reference to a separate file

---

## Recommendation 2: Add a Character Layer - Currently Missing

**Principle:** Identity is "who", skills are "how". Mixing them corrupts both. (Practical Agent Design framework)

There is no character layer in the current file. A one-paragraph agent identity at the top conditions how the model interprets everything below it. Without a self-model, the agent has operational procedures but no framework for resolving ambiguity.

**Suggested addition at the top:**

```markdown
## Agent Identity

You are the primary developer and maintainer of the Trinity platform - an autonomous agent
orchestration system. Your job is to move Trinity forward: shipping P0 issues, maintaining
architecture integrity, and keeping the codebase clean for public consumption. You make
implementation decisions independently within the scope of a given issue; you confirm before
destructive operations or scope changes that go beyond the current issue.
```

---

## Recommendation 3: Convert Imperative Rules to Constitutive Rules

**Principle:** Constitutive design (explaining reasoning) is more robust than imperative rules because the agent can apply the reasoning to edge cases it has never seen. (The Claude Soul Document - Constitutive Identity Spec vs Imperative Rules)

Every rule in the Rules of Engagement is currently a bare assertion. Adding a brief "why" unlocks generalization to novel situations.

**Example transformation:**

Before (imperative):
> Update `docs/memory/requirements.md` BEFORE implementing new features

After (constitutive):
> Update `docs/memory/requirements.md` BEFORE implementing - this is the source of truth. Without a requirements entry, there's no way to verify the feature is complete or audit what was built. An implementation without a requirements trace is effectively invisible to the roadmap.

One phrase per rule is sufficient. The goal is not longer rules, but reasoned ones.

---

## Recommendation 4: Define the Autonomy Boundary Explicitly

**Principle:** "Responsibility Framing (assistant vs decision-maker clarity)" is a required element of real agents. Ambiguity here causes either over-cautiousness or over-reach. (Six Elements of Real Agents framework)

The current file is silent on when the agent should act vs. when it should confirm. For an autonomous dev agent, this is critical.

**Suggested section:**

```markdown
## Autonomy Boundaries

**Act independently on:**
- P0/P1 bug fixes within the current issue's scope
- Code changes, tests, documentation updates
- Standard refactors explicitly part of the task
- Running builds, tests, linters, diagnostics

**Confirm before:**
- Destructive DB operations (DROP, truncate, schema migrations)
- Architectural pattern changes
- Force-pushing or resetting branches
- Closing/reopening issues beyond current scope
- Any action that affects shared infrastructure or other agents
```

---

## Recommendation 5: Compress the Security Section

**Principle:** Information density matters more than completeness. Context rot is a real failure mode - LLM performance degrades when the context window is filled with low-density reference material. (Context Engineering is a First-Class Discipline)

The `⚠️ PUBLIC OPEN SOURCE REPOSITORY` block is 35+ lines, mostly checklist content that doesn't shape behavioral decisions. The essential constraint is two sentences:

> **Public repo:** Never commit credentials, internal URLs, real emails, or IP addresses. Use placeholders everywhere, and run `git diff` before every commit.

Move the full checklist to `docs/SECURITY.md` and @-reference it:

```markdown
@docs/SECURITY.md
```

The security rules belong in the codebase, but not consuming prime context real estate before the agent is oriented to its purpose.

---

## Recommendation 6: Extract Pure-Reference Material via @-includes

**Principle:** Context engineering means designing what the AI sees, optimizing for decision-making density, not completeness.

The following sections are pure reference - they answer "where do I find X?" but don't shape behavior:
- Development Commands
- Local URLs
- Project Structure tree
- Quick Reference (Creating an Agent, Agent Container Labels, Credential Pattern)
- Authentication (detailed curl examples)

Move these to dedicated files and @-reference:

```markdown
@docs/QUICK_REFERENCE.md
@docs/PROJECT_STRUCTURE.md
```

Keep only the commands genuinely needed for routine workflow (start/stop/logs) inline.

---

## Recommendation 7: Consolidate "Important Notes for Claude Code"

The 10 numbered items at the bottom are a mixed bag: architectural constraints (#2 Docker socket), runtime gotchas (#8 re-login), and workflow reminders (#10 clean working directory). Ungrouped lists at the end of a system prompt tend to be under-weighted.

**Distribute them into relevant sections:**
- Architectural constraints (#2 Docker socket, #3 port conflicts, #4 data persistence) → Architecture section or Key Files
- Runtime gotchas (#8 re-login, #9 MCP reconnection) → a brief "Runtime Notes" subsection in Development Commands
- Workflow reminders (#10 clean working directory, #1 credential security) → Rules of Engagement

---

## What's Already Working Well

- Clear project identity statement ("autonomous agent orchestration platform")
- Strong SDLC structure with explicit Todo → In Progress → Review → Done lifecycle
- Memory files table is well-organized and clear
- Skills table in Rules of Engagement is useful and actionable
- Related Repositories section is excellent - clear delineation of what lives where
- The active planning doc reference (`ORCHESTRATION_RELIABILITY_2026-04.md`) with specific issue numbers is a good pattern
- Architectural Invariants reference with validation command is solid
