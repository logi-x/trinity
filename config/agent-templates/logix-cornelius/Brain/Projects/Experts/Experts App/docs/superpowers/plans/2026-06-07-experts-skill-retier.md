---
title: "2026 06 07 experts skill retier"
date: "2026-06-07"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/plans/2026-06-07-experts-skill-retier.md"
---
# Experts skill-family re-tier — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extract a repo-wide `experts-ship` lifecycle skill and de-duplicate the app-trio (galaxy/constellation/orbit) so each rule lives once, with `.cursor/rules` as the deep-dive tier.

**Architecture:** Four skills at three altitudes — `experts-ship` (repo-wide lifecycle) above the `apps/experts-app` trio: `experts-galaxy` (rules + canonical token note), `experts-constellation` (worked code exemplar), `experts-orbit` (shell). Hybrid own-once-link: galaxy states each principle once; constellation keeps worked code + a one-line rule that links to galaxy; the exhaustive detail lives in `.cursor/rules/*.mdc`, which every skill links via a "Deep dives →" block.

**Tech Stack:** Markdown skill files, `.cursor/rules/*.mdc`, root `CLAUDE.md`, the `03-fix-bugs` routine prompt. No application code. Verification is grep/parse, not tests.

**Spec:** `docs/superpowers/specs/2026-06-07-experts-skill-retier-design.md` (decisions D1–D8).

**Branch:** `refactor/skills-ship-retier` (worktree, off merged `origin/main`). One PR.

> **Faithful refinement of D6 (noted, within latitude):** R3's prompt does **not** currently contain a "follow experts-constellation" line — the writer-facing skill mandate lives in `.claude/agents/frontend-developer.md`, and the R3 orchestrator *encodes* the lifecycle inline rather than loading a skill. So D6 is implemented as: (a) root `CLAUDE.md` mandates `experts-ship` repo-wide; (b) R3 gets a one-line **canonical-source pointer** ("this routine's flow is documented canonically in the `experts-ship` skill — keep them in sync"); (c) `frontend-developer.md` keeps its `experts-constellation` mandate (the writer builds, it doesn't merge, so it does not need ship). Git-edit only; the live CCR `RemoteTrigger` push stays deferred to operator re-enable.

---

## File structure

| Action | Path | Responsibility |
|---|---|---|
| Create | `.claude/skills/experts-ship/SKILL.md` | repo-wide lifecycle: the flow, GitHub-issue identity, gatekeeper hand-off, process tools, deep-dives |
| Modify | `.claude/skills/experts-galaxy/SKILL.md` | own each rule's principle; add canonical token note; mark review-checklist canonical; deep-dives; ship pointer |
| Modify | `.claude/skills/experts-constellation/SKILL.md` | keep code+unique depth; trim duplicated prose→one-line+link; remove §11→ship pointer; anti-patterns→slice-only+link; deep-dives |
| Modify | `.claude/skills/experts-orbit/SKILL.md` | theme-safety→galaxy link; deep-dives |
| Modify | `CLAUDE.md` (root) | ship mandatory repo-wide; constellation mandatory for app; **fix all skill paths to repo-root `.claude/skills/`** |
| Modify | `.claude/routines/03-fix-bugs.prompt.md` | one-line canonical-source pointer to experts-ship |
| Modify | `.cursor/rules/experts-claude-skills.mdc` | add ship + constellation rows; fix paths |
| Modify | `.cursor/rules/experts-galaxy-skill-sync.mdc` | note it keeps Tier-1 (skills) ↔ Tier-2 (.cursor/rules) honest |
| (done) | `docs/superpowers/specs/2026-06-07-experts-skill-retier-design.md` | committed `41bf74f6` |
| (this) | `docs/superpowers/plans/2026-06-07-experts-skill-retier.md` | this plan |

---

## Task 1: Create the `experts-ship` skill

**Files:** Create `.claude/skills/experts-ship/SKILL.md`

- [ ] **Step 1: Write the file** with exactly this content:

````markdown
---
name: experts-ship
description: >
    The repo-wide lifecycle skill for logi-x/experts — how ANY change ships, start to finish,
    whether it touches apps/experts-app, the routines, docker, .claude, or infra. Covers picking/
    filing the GitHub issue, branching off fresh main, the own-step pre-merge gate, commit + push
    branch:branch + remote-SHA verify, the PR with Closes #N, CI watch, squash-merge, sentinel-verify
    on origin/main, and the post-merge resync (gitnexus:analyze, ./g --clean). Also documents the
    agent-PR gatekeeper hand-off (R3→R5) and the process tools the lifecycle leans on (gitnexus,
    superpowers, brain). Sits ABOVE the apps/experts-app trio: pair with experts-galaxy (rules),
    experts-constellation (worked exemplar), and experts-orbit (shell) for WHAT a change should look
    like — the flow here is the same for everything. Rigid: follow it exactly; deviations need a
    stated reason.
---

# Experts Ship

How any change ships in `logi-x/experts`. The app-trio (galaxy/constellation/orbit) tells you what a
change should *look like*; this skill is the *lifecycle* every change rides — app or not.

**Announce:** "Using experts-ship to follow the repo lifecycle."

This is a **rigid** skill. Run all commands from the repo root. Do not reorder verify → commit → push.

## The flow — every change, start to finish (always)

### Before you write code

1. **Pick or file the issue first.** Work is tracked as a GitHub issue in `logi-x/experts`. Have the issue number before you branch — the branch name and the PR's `Closes #N` both need it.
2. **Branch off fresh `main`, named _before_ the PR exists:**
    ```bash
    git checkout main && git pull --ff-only
    git checkout -b fix/gh-<issue>-<slug>      # chore/… or refactor/… for non-bug work
    ```
    Renaming a branch after the PR is open **closes** it (GitHub's rename API doesn't retarget), so get the name right up front.

### Implement

3. Build the smallest correct change. Update **every** caller of any symbol / route / wire-value you touch in the same diff (grep the wire value, not just the symbol — `tsc` won't catch a hardcoded URL/string). For *what the change should look like* in `apps/experts-app`, follow `experts-constellation` (+ `experts-galaxy` for the rules, `experts-orbit` for shell).

### Pre-merge gate — its OWN step, never batched with the commit

Run **the gate relevant to what you touched**, from the repo root:

- **apps/experts-app code** → `pnpm experts:test` (full suite; **not** `pnpm test`) **and** `pnpm experts:check` (FORMAT + LINT + TYPECHECK). If `experts:check` reports fixable issues: `pnpm experts:check:fix`, re-run `pnpm experts:check`, confirm it touched only your files. (Detail: `experts-constellation` §10, `experts-galaxy`.)
- **docker / shell scripts** → `bash -n <script>` and `docker compose -f <file> config`.
- **JSON / TOML / YAML config** → parse it (`node -e "require('./x.json')"`, `python3 -c "import tomllib,sys;tomllib.load(open(sys.argv[1],'rb'))" x.toml`).
- **prose / docs** → every link and referenced path resolves.

The gate runs as its **own tool step** — never in the same block as `git commit`/`git push`, or it fires too late and broken work ships.

### Commit · push · PR

4. Commit with the `Co-Authored-By` trailer. Re-confirm `git branch --show-current` immediately before pushing (parallel agents / IDE ops can switch the branch under you).
5. **Push explicit `branch:branch`** — never `HEAD`:
    ```bash
    git push -u origin <branch>:<branch>
    git ls-remote origin <branch>          # remote SHA must equal local HEAD
    ```
6. `gh pr create` — body carries `Closes #<issue>`. Use the PR number `gh pr create` actually returns.
7. Watch CI: `gh pr checks <PR> --watch`. Green (and any required label) before merge.

### Merge — then verify it actually landed

8. `gh pr merge <PR> --squash --delete-branch`.
9. **Verify the change is on `origin/main` — do not trust `state=MERGED` alone.** A squash-merge can squash a stale PR head and silently drop a just-pushed commit. Grep a sentinel:
    ```bash
    git fetch origin main
    git show origin/main:<a-file-you-changed> | grep <a-sentinel-from-your-diff>
    ```

### Post-merge resync — after switching back to `main`

```bash
git checkout main && git pull --ff-only
```

- `pnpm gitnexus:analyze` — re-index so `gitnexus_impact`/`codegraph` reflect merged **code**. (Skip for docs/config-only changes — no symbols moved.)
- `./g --clean` — prune merged/gone branches (skips protected `main`/`development`/`staging`). Skip if another agent shares the working tree (force-pruning can disrupt them).

## Issue & branch identity (GitHub)

- Branch: `fix/gh-<n>-<slug>` (bug) / `chore/…` / `refactor/…`.
- PR body: `Closes #N` auto-closes the issue on merge; one `Closes #X` line per collateral issue.
- Label state model + the full detect→file→fix→gatekeep contract: `.claude/routines/_github-issues-contract.md`.

## Appendix: the agent-PR gatekeeper hand-off (R3 → R5)

Applies to **agent-generated PRs** in the routine pipeline. If you merge your own PR by hand, the flow above is all you need.

**R3 ships, R5 merges — never the same actor, never the same run.**

- **R3 (fix-bot)** opens the PR (`Closes #N`, markers `<!-- agent-pr: true -->` / `<!-- fix-attempt: N -->`, label `agent-generated`), moves the issue to `in-review`, and **exits — never merges, never polls CI.**
- **R5 (gatekeeper)** runs hourly as a *fresh, cold* session and walks a per-PR state machine (sticky markers + head-SHA-tied verdict make it idempotent):
    - CI incomplete → skip; CI failed → `<!-- gatekeeper-ci-failed -->`, ping, pause.
    - CI green + no verdict for the current head SHA → independent review (cold `code-reviewer` + `qa-tester` [+ `security-auditor`]) → posts `<!-- gatekeeper-verdict: PASS|BLOCK -->` + `<!-- gatekeeper-head-sha: … -->`.
        - **BLOCK** → `gh pr close` (branch preserved), issue → `needs-rework` (or `needs-human` + `agent-exhausted` at attempt ≥3), `<!-- next-fix-attempt: N+1 -->`; R3 retries with a fresh PR.
        - **PASS** → **wait** (no same-run merge) — the hour to the next run is the human-interception window.
    - CI green + a PASS verdict from a *prior* run + no human `REQUEST_CHANGES` → `gh pr merge --squash --delete-branch`; `Closes #N` auto-closes the issue (class-anchor close-guard + collateral sweep).
- **Fast-track:** label `gatekeeper-merge-now` → merge in the same run as the PASS verdict.
- The two-pass property (verdict one run, merge a later run) is the safety seam that lets a human catch a bad agent PR before it lands.

## Tools the lifecycle leans on

- **`gitnexus` MCP** (mandated by root `CLAUDE.md`): `gitnexus_impact({target, direction: "upstream"})` **before editing a symbol** (report blast radius), `gitnexus_detect_changes()` **before committing**. Navigate with `gitnexus_query`/`gitnexus_context` instead of grepping.
- **`superpowers` skills** (process-first): `brainstorming` before building something new, `systematic-debugging` for a bug, `test-driven-development` where it fits.
- **`brain`** (`~/brain`): product-rule context before touching Auth/Payments/ZATCA/i18n/Access Control; write decisions/gotchas back at session close (root `CLAUDE.md` → "Session Close").

## Deep dives →

- `.cursor/rules/release-changelog.mdc` — changelog/version conventions.
- `.cursor/rules/documentation-standards.mdc` — doc structure.
- `.cursor/rules/docker-deployment.mdc`, `docker-rules.mdc` — when the change is infra.
````

- [ ] **Step 2: Verify frontmatter name + structure**

Run: `head -3 .claude/skills/experts-ship/SKILL.md | grep -q 'name: experts-ship' && grep -c '^## ' .claude/skills/experts-ship/SKILL.md`
Expected: prints `6` (six `##` sections: flow, identity, gatekeeper, tools, deep-dives… count is informational — any non-error is fine).

- [ ] **Step 3: Verify every deep-dive rule it names exists**

Run: `for r in release-changelog documentation-standards docker-deployment docker-rules; do test -f .cursor/rules/$r.mdc && echo "ok $r" || echo "MISSING $r"; done`
Expected: four `ok` lines.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/experts-ship/SKILL.md
git commit -m "feat(skills): add experts-ship repo-wide lifecycle skill

Extracts the ship-it flow (was experts-constellation §11) generalized to any
change, plus the GitHub-issue identity model, the R3→R5 gatekeeper hand-off
(from closed PR #903), and the process tools (gitnexus/superpowers/brain).
Deep-dives into .cursor/rules.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: Galaxy — own the principles, add canonical token note, deep-dives

**Files:** Modify `.claude/skills/experts-galaxy/SKILL.md`

- [ ] **Step 1: Add the canonical semantic-token / theme-safety note.** Under the `### UI and product behavior` section, after the `Build product UI with Tailwind CSS v4.` bullet, insert:

```markdown
- **Semantic tokens & theme-safety (canonical — orbit & constellation link here).** Use semantic tokens only: `bg-background`, `bg-card`, `bg-muted`, `text-foreground`, `text-muted-foreground`, `border-border`, `text-destructive`, `text-primary`. Positive deltas use `text-emerald-600 dark:text-emerald-400` (there is no `--success` token). **Never** `text-danger`/`text-success`/`text-secondary` or raw hex in components. Add `dark:` only where a semantic token isn't enough. This vocabulary is shared by shell surfaces (experts-orbit) and component content (experts-constellation §4).
```

- [ ] **Step 2: Mark the review checklist canonical.** Change the `### Review expectations` heading line to:

```markdown
### Review expectations (canonical checklist — constellation anti-patterns link here)
```

- [ ] **Step 3: Add the "Deep dives →" block + ship pointer.** Immediately before the `## When local rules disagree` section, insert:

```markdown
## Deep dives →

The exhaustive per-topic detail lives in `.cursor/rules/*.mdc` (Tier 2); this skill is the portable summary (Tier 1).

- API & domain: `.cursor/rules/{api-architecture,api-v1-conventions,api-route-eslint-guards}.mdc`
- Data & DTOs: `.cursor/rules/{prisma-database,naming-conventions,no-denormalized-user-fields,global-types}.mdc`
- Client fetching: `.cursor/rules/{data-fetching,hooks}.mdc`
- In-app AI: `.cursor/rules/in-app-ai.mdc`

## Lifecycle

For how a change ships (branch → gate → PR → merge → verify → resync), follow **experts-ship**. This skill is *what the code must be*, not *how it ships*.
```

- [ ] **Step 4: Verify the named deep-dive rules exist + tokens note present**

Run: `for r in api-architecture api-v1-conventions api-route-eslint-guards prisma-database naming-conventions no-denormalized-user-fields global-types data-fetching hooks in-app-ai; do test -f .cursor/rules/$r.mdc || echo "MISSING $r"; done; grep -q 'Semantic tokens & theme-safety (canonical' .claude/skills/experts-galaxy/SKILL.md && echo "token-note ok"`
Expected: no `MISSING` lines; `token-note ok`.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/experts-galaxy/SKILL.md
git commit -m "refactor(skills): galaxy owns canonical token note + review checklist + deep-dives

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: Constellation — trim duplicated prose, remove §11, add links + deep-dives

**Files:** Modify `.claude/skills/experts-constellation/SKILL.md`

> Keep ALL code blocks and the unique depth (§3 four-states, §4 MCP-first/kit, §5 RTL/ICU, §7 time, §8 charts, §9 testing, §10 content gate). Only remove duplicated *prose lectures* and §11; add one-line rule + galaxy links.

- [ ] **Step 1: Token bullet → galaxy link (§4).** In the `## 4. UI: kit + HeroUI + tokens` "Rules:" list, replace the bullet that begins `- **Semantic tokens only**:` (the full bullet through `…raw hex in components.`) with:

```markdown
- **Semantic tokens only** — `bg-card`, `text-foreground`, `text-muted-foreground`, `border-border`, `text-destructive`, `text-primary`; positive deltas `text-emerald-600 dark:text-emerald-400`; never `text-danger`/`text-success`/raw hex. (Canonical vocabulary + rationale: **experts-galaxy → Semantic tokens & theme-safety**.)
```

- [ ] **Step 2: Companion section → add galaxy/ship altitude note.** In the `### Companion skills` list, replace the `experts-galaxy` bullet with:

```markdown
- **`experts-galaxy`** — the **rules** this exemplar implements (CQRS, DTO/camelCase, `useApiQuery`, i18n, SAR, the canonical token note, the review checklist). When this skill states a rule in one line, galaxy is where the principle + why live.
- **`experts-ship`** — the **lifecycle** every change rides (branch → gate → PR → merge → verify). This skill is *what the code looks like*; ship is *how it ships*.
```

- [ ] **Step 3: Anti-patterns → slice-specific + link.** Replace the intro of `## Anti-patterns (instant rejections)` (the heading line) with:

```markdown
## Anti-patterns (slice-specific instant rejections)

> The app-wide review checklist is canonical in **experts-galaxy → Review expectations**. Below are the rejections specific to the constellation slice pattern:
```

(Leave the existing bullet list beneath it unchanged — they are slice-specific.)

- [ ] **Step 4: Remove §11, replace with a ship pointer.** Delete the entire `## 11. The flow — every change, start to finish (always)` section (from that heading through the end of its `### Post-merge checklist` block, i.e. everything up to but not including `## Anti-patterns`). Replace it with:

```markdown
## 11. Lifecycle → experts-ship

The Definition of Done (top) is the *content* gate. For the *process* gate — branch → pre-merge gate → commit → push → PR → squash-merge → sentinel-verify → post-merge resync, with exact commands — follow **experts-ship** (the repo-wide lifecycle skill). It is the same flow for every change; it is not duplicated here.
```

Also update the Definition of Done footer pointer (the `> This list is the **pre-commit content gate**…` line that references "**§11. The flow**") to read:

```markdown
> This list is the **pre-commit content gate**. For the full process — branch → verify → commit → push → PR → merge → resync, with exact commands — follow the **experts-ship** skill.
```

- [ ] **Step 5: Add "Deep dives →" block.** Immediately before `## Reference files (the constellation itself)`, insert:

```markdown
## Deep dives →

Exhaustive per-topic detail (Tier 2) lives in `.cursor/rules/*.mdc`:

- UI: `.cursor/rules/{front-end-cursor-rules,styling-guide,ui-components,monorepo-heroui}.mdc`, `heroui-*.mdc`
- Pages & structure: `.cursor/rules/page-structure.mdc`
- i18n / RTL: `.cursor/rules/{arabic-rtl-i18n,i18n-routing}.mdc`
- Testing: `.cursor/rules/testing.mdc`
```

- [ ] **Step 6: Update frontmatter description** — remove the `§11` lifecycle clause. Replace the description sentence fragment `the commit gate, and the full\n    lifecycle flow (§11) — pre-merge ... ./g --clean.` with: `the commit gate. For the ship-it lifecycle, see experts-ship.` (Keep the rest of the description intact.)

- [ ] **Step 7: Verify §11 flow gone, pointer present, deep-dives rules exist**

Run: `grep -q 'git push -u origin' .claude/skills/experts-constellation/SKILL.md && echo "LEAK: flow still present" || echo "flow removed ok"; grep -q 'Lifecycle → experts-ship' .claude/skills/experts-constellation/SKILL.md && echo "pointer ok"; for r in front-end-cursor-rules styling-guide ui-components monorepo-heroui page-structure arabic-rtl-i18n i18n-routing testing; do test -f .cursor/rules/$r.mdc || echo "MISSING $r"; done`
Expected: `flow removed ok`, `pointer ok`, no `MISSING`.

- [ ] **Step 8: Commit**

```bash
git add .claude/skills/experts-constellation/SKILL.md
git commit -m "refactor(skills): constellation trims duplicated prose, drops §11→experts-ship, adds deep-dives

Keeps all worked code + unique depth; rules now link to galaxy; lifecycle lives
in experts-ship.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 4: Orbit — theme-safety → galaxy link, deep-dives

**Files:** Modify `.claude/skills/experts-orbit/SKILL.md`

- [ ] **Step 1: Theme safety → galaxy link.** In the `### Theme safety` subsection, after the `Prefer semantic tokens and theme-aware classes:` line and its token bullet list, append:

```markdown
The semantic-token vocabulary is canonical in **experts-galaxy → Semantic tokens & theme-safety** — this section is the shell-surface *application* of it (shadows, translucent layers, hero gradients, search/input contrast, inactive nav text).
```

- [ ] **Step 2: Add "Deep dives →" block.** Before the `## Review checklist` section, insert:

```markdown
## Deep dives →

- Styling & components: `.cursor/rules/{styling-guide,ui-components,monorepo-heroui}.mdc`
- App-wide rules: see **experts-galaxy**; ship-it lifecycle: see **experts-ship**.
```

- [ ] **Step 3: Verify**

Run: `grep -q 'Semantic tokens & theme-safety' .claude/skills/experts-orbit/SKILL.md && echo "galaxy-link ok"; for r in styling-guide ui-components monorepo-heroui; do test -f .cursor/rules/$r.mdc || echo "MISSING $r"; done`
Expected: `galaxy-link ok`, no `MISSING`.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/experts-orbit/SKILL.md
git commit -m "refactor(skills): orbit theme-safety links to galaxy canonical tokens + deep-dives

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 5: Enforcement wiring (root CLAUDE.md, R3 pointer, cursor index, sync rule)

**Files:** Modify `CLAUDE.md`, `.claude/routines/03-fix-bugs.prompt.md`, `.cursor/rules/experts-claude-skills.mdc`, `.cursor/rules/experts-galaxy-skill-sync.mdc`

- [ ] **Step 1: Root `CLAUDE.md` — add ship mandate + fix paths.** In the `## Skills` section, replace the `**MANDATORY …**` block + the `Use these when the task matches them:` list with:

```markdown
**MANDATORY — lifecycle (every change, repo-wide):**

- **experts-ship**: `.claude/skills/experts-ship/SKILL.md` — how ANY change ships: branch → pre-merge gate → commit → push → PR `Closes #N` → squash-merge → sentinel-verify → post-merge resync, plus the agent-PR gatekeeper hand-off. Follow it for every change you intend to merge.

**MANDATORY for any `apps/experts-app` change:**

- **experts-constellation**: `.claude/skills/experts-constellation/SKILL.md` — the canonical "how an enhancement must look" worked exemplar (vertical slice, kit + HeroUI, RTL/i18n, states, a11y, tests, content gate). Invoke before writing code and again before committing **every time** you touch experts-app.

Use these when the task matches them:

- **experts-galaxy**: `.claude/skills/experts-galaxy/SKILL.md` — app-wide rules (the principles experts-constellation implements).
- **experts-orbit**: `.claude/skills/experts-orbit/SKILL.md` — workspace-shell / admin-chrome surfaces.
- **experts-cosmos**: `apps/experts-os/.claude/skills/experts-cosmos/SKILL.md` — native SwiftUI app.
```

(This both adds the ship mandate AND fixes the path discrepancy — galaxy/orbit/constellation now point at repo-root `.claude/skills/`, where they actually live. `experts-cosmos` correctly stays under `apps/experts-os/`.)

- [ ] **Step 2: R3 canonical-source pointer.** In `.claude/routines/03-fix-bugs.prompt.md`, after line 1 (the `You are an automated fix-bot …` paragraph), insert a new line:

```markdown
> The lifecycle this routine encodes (branch → gate → PR `Closes #N` → markers → gatekeeper hand-off) is documented canonically in the `experts-ship` skill (`.claude/skills/experts-ship/SKILL.md`). If you change the flow here, update that skill too — they must not drift.
```

- [ ] **Step 3: Cursor index — add ship + constellation rows, fix paths.** In `.cursor/rules/experts-claude-skills.mdc`, in the skills table, add two rows (and keep galaxy/orbit, fixing their paths to repo-root if they point at `apps/experts-app/.claude/skills/`):

```markdown
| **experts-ship** | `.claude/skills/experts-ship/SKILL.md` | **Repo-wide lifecycle:** branch → gate → PR → squash-merge → sentinel-verify → resync; agent-PR gatekeeper hand-off. Every change that ships. |
| **experts-constellation** | `.claude/skills/experts-constellation/SKILL.md` | **Worked exemplar for apps/experts-app:** the DTO→…→component slice, four states, kit/HeroUI, RTL/i18n, tests. Pairs with experts-galaxy (rules) + experts-orbit (shell). |
```

Also update the `description:` frontmatter line to include `experts-ship` and `experts-constellation` in the skill list, and fix any `apps/experts-app/.claude/skills/experts-{galaxy,orbit}` paths to `.claude/skills/experts-{galaxy,orbit}`.

- [ ] **Step 4: Sync rule note.** In `.cursor/rules/experts-galaxy-skill-sync.mdc`, add a short note near the top:

```markdown
> This rule keeps Tier 1 (the `experts-*` skills) ↔ Tier 2 (`.cursor/rules/*.mdc`) honest. When a skill's "Deep dives →" block points at a rule, that rule is the exhaustive source; the skill is the portable summary. Update both together.
```

- [ ] **Step 5: Verify paths resolve + no stale app-path skill links**

Run: `grep -nE 'apps/experts-app/\.claude/skills/experts-(galaxy|orbit|constellation|ship)' CLAUDE.md .cursor/rules/experts-claude-skills.mdc && echo "STALE PATHS FOUND" || echo "paths ok"; for s in ship galaxy orbit constellation; do test -f .claude/skills/experts-$s/SKILL.md || echo "MISSING skill experts-$s"; done; grep -q 'experts-ship' CLAUDE.md && echo "ship mandated ok"`
Expected: `paths ok`, no `MISSING`, `ship mandated ok`.

- [ ] **Step 6: Commit**

```bash
git add CLAUDE.md .claude/routines/03-fix-bugs.prompt.md .cursor/rules/experts-claude-skills.mdc .cursor/rules/experts-galaxy-skill-sync.mdc
git commit -m "chore(skills): wire experts-ship enforcement + fix skill-path discrepancy

Root CLAUDE.md mandates experts-ship repo-wide + constellation for app and
points all app-skill links at the real repo-root .claude/skills/. R3 gets a
canonical-source pointer to experts-ship (git only; live CCR trigger push
deferred to re-enable). Cursor index + sync rule updated.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 6: Final verification + ship the PR (dogfood experts-ship)

**Files:** none (verification + git/gh)

- [ ] **Step 1: De-dup invariant — no principle stated as a "rule" in two skills.** Spot-check that the token vocabulary's canonical phrasing appears once:

Run: `grep -rl 'there is no \`--success\` token\|there is no --success token' .claude/skills/ | sort`
Expected: only `.claude/skills/experts-galaxy/SKILL.md` (constellation/orbit reference it, don't restate the rationale).

- [ ] **Step 2: All four skill names match dirs**

Run: `for s in ship galaxy orbit constellation; do grep -m1 '^name:' .claude/skills/experts-$s/SKILL.md; done`
Expected: `name: experts-ship`, `experts-galaxy`, `experts-orbit`, `experts-constellation`.

- [ ] **Step 3: Every `.cursor/rules` rule named in any "Deep dives" block exists**

Run: `grep -rhoE '\.cursor/rules/[a-z0-9-]+\.mdc|\.cursor/rules/\{[a-z0-9,-]+\}' .claude/skills/ | sort -u` — then eyeball each named rule against `ls .cursor/rules/`. (Brace-expansions like `{a,b}.mdc` list multiple; confirm each member exists.)
Expected: every named rule resolves to a real file.

- [ ] **Step 4: Pre-merge gate (docs gate per experts-ship).** Confirm no broken markdown links to skill paths and JSON/settings unchanged:

Run: `git diff --stat origin/main && bash -n .claude/hooks/experts-constellation-reminder.sh && node -e "require('./.claude/settings.json')" && echo "gate ok"`
Expected: stat lists only the intended files; `gate ok`.

- [ ] **Step 5: Push branch:branch + verify SHA**

```bash
git branch --show-current        # must be refactor/skills-ship-retier
git push -u origin refactor/skills-ship-retier:refactor/skills-ship-retier
git ls-remote origin refactor/skills-ship-retier   # remote SHA == local HEAD
```

- [ ] **Step 6: Open the PR** with `gh pr create --base main`, body summarizing the 4-skill family, decisions D1–D8, and "Closes" nothing (no issue filed; refactor). Title: `refactor(skills): extract experts-ship + de-dup galaxy/constellation (plan B re-tier)`.

- [ ] **Step 7: Watch CI to green** (`gh pr checks <PR> --watch`), then **STOP — do not merge.** Hand the PR to the user for review (per the session's "eyeball before merge" cadence). Sentinel-verify + post-merge resync happen after the user approves the merge.

---

## Self-review (run against the spec)

- **Spec coverage:** D1 ship repo-wide → Task 1 + Task 5 Step 1. D2 hybrid de-dup → Tasks 2–3. D3 galaxy owns tokens → Task 2 Step 1 + Task 3 Step 1 + Task 4 Step 1. D4 deep-dives → Tasks 1–4. D5 no new hook → (no task; explicitly nothing touches the hook beyond the unchanged reference). D6 R3 git-only/defer → Task 5 Step 2 + header note. D7 fix-links → Task 5 Step 1 + Step 3. D8 one PR → Task 6. ✅ all covered.
- **Placeholder scan:** none — all content is literal; trims quote the anchor text.
- **Type/name consistency:** skill ids (`experts-ship`/`-galaxy`/`-orbit`/`-constellation`) and section names ("Semantic tokens & theme-safety", "Review expectations", "Deep dives →", "Lifecycle → experts-ship") are used identically across tasks.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
