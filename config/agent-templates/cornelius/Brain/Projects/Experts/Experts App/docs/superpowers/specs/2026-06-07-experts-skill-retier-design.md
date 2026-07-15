---
title: "2026 06 07 experts skill retier design"
date: "2026-06-07"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/specs/2026-06-07-experts-skill-retier-design.md"
---
# Experts skill-family re-tier — design

- **Date:** 2026-06-07
- **Status:** Approved (brainstorming) → ready for implementation plan
- **Scope:** `.claude/skills/{experts-galaxy,experts-constellation,experts-orbit}` + new `experts-ship`, plus enforcement wiring (root `CLAUDE.md`, the PreToolUse hook, the R3 routine, `.cursor/rules` index + sync rule).
- **Prereq (done):** PR #904 renamed `experts-ecosystem→experts-galaxy` and `experts-textbook→experts-constellation` (pure rename, merged to `main`). PR #903 (textbook MCP/tools + gatekeeper appendix) was closed unmerged; its content is re-homed here.

## Motivation

The skill family had grown two problems:

1. **A lifecycle concern trapped in an app-only skill.** The full ship-it flow (issue → branch → gate → PR → merge → verify → resync) lived in `experts-constellation` §11, but it governs *every* change in the repo. This session's flow-following PRs (#897 routines, #899 hook, #904 rename) were all **non-app** changes that still rode that flow — yet constellation only fires for `apps/experts-app`.
2. **Real duplication.** `constellation` largely restated `galaxy`'s app-wide rules (thin routes, CQRS, `useApiQuery`, camelCase DTO, HeroUI-first, i18n), and the semantic-token / theme-safety note existed in both `orbit` and `constellation`. The review-checklist (galaxy) and anti-patterns (constellation) lists had drifted into near-duplicates.

## The four-skill family (final altitudes)

```
experts-ship          REPO-WIDE. How any change ships. Sits ABOVE the trio.
─────────────────────────────────────────────────────────────────────────
apps/experts-app trio (app-scoped):
  experts-galaxy        the RULES (app-wide principles + canonical token note)
  experts-constellation the WORKED EXEMPLAR (code blocks + one-line rule + links)
  experts-orbit         the SHELL (chrome, layering, surfaces)
```

One line each: **ship = how it ships · galaxy = the rules · constellation = the worked example · orbit = the shell.**

(`experts-cosmos` — the native SwiftUI app skill at `apps/experts-os/` — is unaffected.)

## Decisions (locked in brainstorming)

| # | Decision | Choice |
|---|---|---|
| D1 | `experts-ship` scope | **Repo-wide**, mandated for every change that ships; sits above the app-trio. |
| D2 | galaxy ↔ constellation de-dup | **Hybrid own-once-link**: galaxy owns each rule's principle + why; constellation drops duplicated *prose* but keeps all worked *code* + a one-line rule statement that links to galaxy. Drift-prone lists single-sourced. |
| D3 | Semantic-token / theme-safety home | **galaxy** owns the canonical note; orbit + constellation keep context-specific usage and link to galaxy. |
| D4 | Deep-dive tier | Formalize **3 tiers**: skill (summary) → `.cursor/rules/*.mdc` (exhaustive). Every skill carries a **"Deep dives →"** block linking its matching rules. |
| D5 | Enforcement hook | **No new repo-wide hook.** Keep the existing PreToolUse hook app-path-scoped (constellation). Ship is enforced via root `CLAUDE.md` + R3 + commit discipline. |
| D6 | R3 routine update | Edit the **git-tracked** `.prompt.md` only; **defer** the live CCR `RemoteTrigger` push to operator re-enable (routines are currently disabled). |
| D7 | Path discrepancy | **Fix the links** to repo-root `.claude/skills/...`; do **not** move the skills under `apps/experts-app/` (would risk skill discovery). |
| D8 | Staging | **One PR** for the whole re-tier, clean per-concern commits. |

## Rule-ownership table (the core artifact)

For each overlapping rule: galaxy states the principle once; constellation keeps its worked code + a one-liner linking to galaxy; the deepest detail lives in `.cursor/rules`.

| Rule | Principle owner | Constellation keeps | Deep dive (`.cursor/rules`) |
|---|---|---|---|
| Thin routes / zod / delegate | galaxy | the `GET` route code block + link | `api-architecture`, `api-v1-conventions`, `api-route-eslint-guards` |
| CQRS / domain layout | galaxy | §1 layer table (admin-flavored) + link | `api-architecture` |
| `useApiQuery` + four states | galaxy (the rule) | **§3 in full** — four-states depth is unique | `data-fetching`, `hooks` |
| camelCase DTO, no Prisma leak | galaxy | the DTO code block + one-liner | `naming-conventions`, `prisma-database`, `no-denormalized-user-fields` |
| HeroUI v3 first | galaxy | **§4 MCP-first + compound specifics** unique | `monorepo-heroui`, `ui-components`, `heroui-*` |
| i18n en/ar/es | galaxy (the rule) | **§5 RTL/ICU depth** unique | `arabic-rtl-i18n`, `i18n-routing` |
| Semantic tokens / theme-safety | **galaxy (new canonical note)** | §4 token bullet → link; orbit "Theme safety" → link | `styling-guide` |
| Review checklist ↔ anti-patterns | **galaxy** owns the canonical review checklist | anti-patterns → slice-specific only + link | — |

Net: constellation loses duplicated *prose lectures*, keeps **every code block** and all unique depth (four states, kit API, RTL, charts, node-env testing). Still copy-pasteable; nothing explained twice.

## Per-skill changes

### experts-ship (new)
- Frontmatter: `name: experts-ship`; rigid; repo-wide; "how any change ships in `logi-x/experts`."
- Body:
  1. **The flow** — generalized from constellation §11: issue → branch off fresh `main` (named before the PR) → implement → **pre-merge gate** ("the relevant gate for what you touched"; app-specific gate detail stays in galaxy/constellation) → commit → push `branch:branch` + verify remote SHA → PR `Closes #N` → watch CI → squash-merge → sentinel-verify on `origin/main` → post-merge resync (`gitnexus:analyze`, `./g --clean`).
  2. **GitHub-issues identity model** — branch naming, `Closes #N`, label state; points at `.claude/routines/_github-issues-contract.md`.
  3. **Gatekeeper hand-off** (from #903) — re-homed, **un-fenced** (this is the lifecycle skill now). The R3→R5 state machine in condensed form.
  4. **Process tools** (from #903) — gitnexus (impact/detect), superpowers process skills, brain session-close. (heroui-react MCP stays craft, in constellation/galaxy.)
  5. **Deep dives →** `release-changelog`, `documentation-standards` (+ `docker-deployment` for infra).

### experts-galaxy
- Becomes the single owner of the app-wide rule principles (table above).
- **New canonical "Semantic tokens & theme-safety" note** (vocabulary: `bg-card`, `text-foreground`, `border-border`; no hex; no `text-danger`/`text-success`).
- Its "Review expectations" is the **canonical review checklist**.
- Add **"Deep dives →"** block.
- Add a one-line pointer to `experts-ship` for lifecycle.

### experts-constellation
- Keeps all worked **code** + unique depth (§3 four states, §4 MCP-first/kit, §5 RTL/ICU, §7 time, §8 charts, §9 testing, §10 content gate).
- Replaces duplicated prose with one-line rule statements that **link to galaxy**.
- §4 token bullet → link to galaxy's canonical note.
- "Anti-patterns" → slice-specific only + link to galaxy's review checklist.
- §11 (the flow) → **removed**; replaced with a one-line "For the lifecycle every change rides, follow `experts-ship`."
- Add **"Deep dives →"** block.

### experts-orbit
- "Theme safety" → keep shell-surface application, **link to galaxy** for the token vocabulary.
- Add **"Deep dives →"** block (`styling-guide`, `ui-components`, `monorepo-heroui`).

## Enforcement wiring

- **Root `CLAUDE.md`:** `experts-ship` → **mandatory repo-wide** (lifecycle for every shipping change); `experts-constellation` → **mandatory for `apps/experts-app`** (craft); `experts-galaxy` / `experts-orbit` → "use when relevant." Fix all skill-link paths to repo-root `.claude/skills/...` (D7).
- **PreToolUse hook:** unchanged — stays app-path-scoped for constellation (D5).
- **R3 routine** (`.claude/routines/03-fix-bugs.prompt.md`): "follow experts-constellation" → "follow **experts-ship** (lifecycle, always) + **experts-constellation** (if experts-app)." Git edit only; defer `RemoteTrigger` push (D6).
- **`.cursor/rules/experts-claude-skills.mdc`** (routing index): add `experts-ship` + `experts-constellation` rows; fix paths.
- **`.cursor/rules/experts-galaxy-skill-sync.mdc`:** note it now keeps Tier-1 (skills) ↔ Tier-2 (`.cursor/rules`) honest across the family.

## Non-goals / out of scope

- No content/behavior change to the **rules themselves** — only relocation and de-dup.
- Not moving skills under `apps/experts-app/` (D7).
- Not pushing the live R3 CCR trigger (D6 — operator action on re-enable).
- Not touching `experts-cosmos` beyond an existing cross-link if needed.
- No new repo-wide hook (D5).

## Verification

- Every `.cursor/rules/*.mdc` named in a "Deep dives" block exists (grep).
- No rule's principle is stated in two skills (the de-dup holds): galaxy is the only place each principle appears as a "rule"; constellation references it.
- All four skill `name:` frontmatter match their dirs.
- Root `CLAUDE.md` + cursor index skill paths resolve to real files.
- Hook `bash -n` OK; settings.json parses (unchanged).
- `experts-ship` is self-contained and readable without the trio.

## Operator follow-ups (not in this PR)

- On routine re-enable: `RemoteTrigger update` the `03-fix-bugs` trigger so the inlined prompt picks up the experts-ship/constellation reference (D6).

## PR staging

One PR (`refactor/skills-ship-retier`), commits grouped by concern: (1) spec, (2) create experts-ship, (3) galaxy de-dup + token note + deep-dives, (4) constellation trim + links + deep-dives, (5) orbit token-link + deep-dives, (6) enforcement wiring (CLAUDE.md/R3/cursor/path-fix).

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
