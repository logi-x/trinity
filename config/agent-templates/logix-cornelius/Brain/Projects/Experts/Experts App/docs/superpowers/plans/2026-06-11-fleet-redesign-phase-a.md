---
title: "2026 06 11 fleet redesign phase a"
date: "2026-06-11"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/plans/2026-06-11-fleet-redesign-phase-a.md"
---
# Fleet Redesign Phase A: Cost Capture + Repo Restructure — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship migration steps 1–2 of the fleet redesign spec (`docs/superpowers/specs/2026-06-11-fleet-redesign-flight-director-design.md`): per-run cost capture into `costs.jsonl`, then restructure `.claude/loops/` to prompts-only with the runner in `ops/fleet/` and the CCR mirror quarantined in `ops/fleet/ccr/`.

**Architecture:** Two independent PRs. PR 1 extracts the runner's inline result-parsing python into a standalone `summarize-run.py` that also appends a JSON line per run to `.cache/experts-routines/costs.jsonl` (testable with a fixture log). PR 2 is a pure `git mv` + path-fix restructure: no prompt content changes, pulse deleted, every consumer's path updated in the same diff (crontab, pool dispatch, worktree setup, CCR sync, CI gate workflow, prompt cross-references).

**Tech Stack:** bash, python3 (stdlib only), the `claude` CLI's `--output-format json` result object, GNU sed, gh CLI.

**Epic:** #978. Each PR gets its own issue (`gh issue create`), body says `Part of #978` (never `Closes #978`).

**Loop numbering note:** the current 01-sentinel … 08-overwatch numbering is KEPT in this phase. Renumbering to the final 5-loop layout happens in Phase B (scout merge) — renaming twice is churn.

**Spec deviation (intentional):** trigger configs in `ops/fleet/ccr/` keep their `<name>.json` filenames (spec sketch said `*.trigger.json`) because `sync.ts` resolves names by appending `.json` (line 82); keeping the suffix avoids touching its resolution logic.

---

## PR 1 — cost capture

### Task 1: Extract the run summarizer into `_summarize-run.py` with costs.jsonl output

**Files:**

- Create: `.claude/loops/_summarize-run.py`
- (Runner wired in Task 2)

- [ ] **Step 1: Create `.claude/loops/_summarize-run.py`** with this exact content (a port of the inline python in `_run-local.sh:273-338`, plus the JSONL append):

```python
#!/usr/bin/env python3
"""Parse the final claude-CLI result object out of a run log.

Prints the human-readable footer (cost/turns/duration/issues/PRs/outcome) to
stdout AND appends one JSON line per run to the costs file — the fleet's cost
feed (fleet redesign spec §6).

Usage:
  _summarize-run.py <log> <verbose:0|1> <wall_sec> <exit_code> <costs_file> <loop> <slot> <model>

Never fails the run: any internal error prints a placeholder and exits 0.
"""
import json
import pathlib
import re
import sys
import time


def parse_result(text: str, verbose: bool):
    if verbose:
        # stream-json: scan backwards for the line where type == "result".
        for line in reversed(text.splitlines()):
            if '"type":"result"' in line:
                try:
                    return json.loads(line)
                except Exception:
                    return None
        return None
    # normal mode: stdout is one JSON object appended after the header — find
    # the final top-level "{ and parse from there.
    idx = text.rfind('\n{"')
    if idx < 0:
        return None
    chunk = text[idx + 1 :].strip()
    end = chunk.rfind("}")
    if end < 0:
        return None
    try:
        return json.loads(chunk[: end + 1])
    except Exception:
        return None


def fmt_dur(ms):
    if not ms:
        return "?"
    s = ms // 1000
    return f"{s // 60}m {s % 60}s"


def main() -> int:
    log_path, verbose, wall_sec, exit_code, costs_file, loop, slot, model = sys.argv[1:9]
    verbose = verbose == "1"
    text = pathlib.Path(log_path).read_text(errors="replace")
    result = parse_result(text, verbose) or {}

    cost = result.get("total_cost_usd")
    turns = result.get("num_turns")
    dur_ms = result.get("duration_ms")
    api_ms = result.get("duration_api_ms")
    stop = result.get("stop_reason") or result.get("terminal_reason")
    usage = result.get("usage") or {}
    text_out = (result.get("result") or "").strip()

    issues = sorted(set(re.findall(r"(?:EXP-|#)(\d+)", text_out)))
    prs = sorted(set(re.findall(r"(?:PR #|pull/)(\d+)", text_out)))
    first_line = next((ln.strip() for ln in text_out.splitlines() if ln.strip()), "")
    if len(first_line) > 120:
        first_line = first_line[:117] + "..."

    # --- cost feed: one JSON line per run, append-only ---
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "loop": loop,
        "slot": slot or None,
        "model": model,
        "exit": int(exit_code),
        "wall_sec": int(wall_sec),
        "cost_usd": cost,
        "num_turns": turns,
        "duration_ms": dur_ms,
        "duration_api_ms": api_ms,
        "stop": stop,
        "usage": usage,
        "issues": issues,
        "prs": prs,
        "outcome": first_line,
        "parsed": bool(result),
    }
    try:
        p = pathlib.Path(costs_file)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a") as f:
            f.write(json.dumps(record, separators=(",", ":")) + "\n")
    except Exception as e:  # cost capture must never fail the run
        print(f"(costs.jsonl append failed: {e})", file=sys.stderr)

    # --- human footer (unchanged format from the old inline snippet) ---
    if not result:
        print("(no result object parseable)")
        return 0
    print(f"Cost:    ${cost:.4f}" if cost is not None else "Cost:    ?")
    print(f"Turns:   {turns}" if turns is not None else "Turns:   ?")
    print(f"Duration: {fmt_dur(dur_ms)} ({fmt_dur(api_ms)} API, {wall_sec}s wall)")
    if stop:
        print(f"Stop:    {stop}")
    if issues:
        print(f"Issues:  {', '.join('#' + i for i in issues)}")
    if prs:
        print(f"PRs:     {', '.join('#' + p for p in prs)}")
    if first_line:
        print(f"Outcome: {first_line}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"(summarizer error: {e})", file=sys.stderr)
        sys.exit(0)
```

- [ ] **Step 2: Syntax check**

Run: `python3 -m py_compile .claude/loops/_summarize-run.py && echo OK`
Expected: `OK`

### Task 2: Wire the runner to the summarizer

**Files:**

- Modify: `.claude/loops/_run-local.sh:273-339` (the `RUN_SUMMARY=$(python3 - ... PYEOF` block)

- [ ] **Step 1: Replace the entire inline-python block** (from `RUN_SUMMARY=$(python3 - "$LOG" ...` line 273 through the closing `)` after `PYEOF` line 339) with:

```bash
COSTS_FILE="${ROUTINE_COSTS_FILE:-$HOME/experts/.cache/experts-routines/costs.jsonl}"
RUN_SUMMARY=$(python3 "$HERE/_summarize-run.py" \
  "$LOG" "$VERBOSE" "$RUN_WALL_SEC" "$EXIT" \
  "$COSTS_FILE" "$NAME" "${ROUTINE_SLOT_NAME:-}" "$ROUTINE_MODEL" 2>/dev/null || true)
```

- [ ] **Step 2: Syntax check**

Run: `bash -n .claude/loops/_run-local.sh && echo OK`
Expected: `OK`

- [ ] **Step 3: Dry-run smoke test** (does not invoke claude, proves arg parsing intact)

Run: `bash .claude/loops/_run-local.sh 01-sentinel --dry-run | tail -3`
Expected: prompt head lines + `--- end dry-run ---`, exit 0.

### Task 3: Fixture test for the summarizer

- [ ] **Step 1: Create a fake normal-mode run log and run the summarizer against it**

```bash
TMP=$(mktemp -d)
cat > "$TMP/fake.log" <<'EOF'
============================================================
Routine: 99-fixture
============================================================
{"type":"result","total_cost_usd":0.1234,"num_turns":7,"duration_ms":65000,"duration_api_ms":42000,"result":"Filed issue #123 and PR #456 for the fixture.","usage":{"input_tokens":1000,"output_tokens":2000,"cache_read_input_tokens":50000}}
EOF
python3 .claude/loops/_summarize-run.py "$TMP/fake.log" 0 70 0 "$TMP/costs.jsonl" 99-fixture "" claude-sonnet-4-6
```

Expected stdout (exact):

```
Cost:    $0.1234
Turns:   7
Duration: 1m 5s (0m 42s API, 70s wall)
Issues:  #123, #456
PRs:     #456
Outcome: Filed issue #123 and PR #456 for the fixture.
```

- [ ] **Step 2: Verify the JSONL record**

Run: `python3 -c "import json,sys;r=json.loads(open(sys.argv[1]).readline());assert r['cost_usd']==0.1234 and r['loop']=='99-fixture' and r['usage']['cache_read_input_tokens']==50000 and r['exit']==0;print('JSONL OK')" "$TMP/costs.jsonl"`
Expected: `JSONL OK`

- [ ] **Step 3: Verify the no-result path doesn't crash or skip the record**

```bash
echo "garbage log, claude never produced output" > "$TMP/empty.log"
python3 .claude/loops/_summarize-run.py "$TMP/empty.log" 0 5 1 "$TMP/costs.jsonl" 99-fixture "" claude-sonnet-4-6
python3 -c "import json,sys;lines=open(sys.argv[1]).readlines();r=json.loads(lines[1]);assert r['parsed']==False and r['exit']==1;print('FAIL-PATH OK')" "$TMP/costs.jsonl"
```

Expected: `(no result object parseable)` then `FAIL-PATH OK`. Clean up: `rm -rf "$TMP"`.

### Task 4: Ship PR 1 (follow experts-ship)

- [ ] **Step 1: File the issue**

```bash
gh issue create --repo logi-x/experts \
  --title "fleet step 1: per-run cost capture (costs.jsonl) in the local runner" \
  --body "Part of #978. Extract the runner's result-parsing python into .claude/loops/_summarize-run.py and append one JSON line per run to .cache/experts-routines/costs.jsonl (cost, tokens, turns, duration, outcome). Spec §6."
```

- [ ] **Step 2: Branch off fresh main** — `git checkout main && git pull --ff-only && git checkout -b chore/gh-<N>-fleet-cost-capture` (use the issue number from step 1).
- [ ] **Step 3: Re-run all gates as their own step** — Task 1 Step 2, Task 2 Steps 2–3, Task 3 (all green).
- [ ] **Step 4: Commit** — `git add .claude/loops/_summarize-run.py .claude/loops/_run-local.sh && git commit -m "chore(fleet): per-run cost capture into costs.jsonl ..."` with the `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` trailer.
- [ ] **Step 5: Push explicit branch:branch, verify remote SHA** — `git push -u origin <branch>:<branch> && git ls-remote origin <branch>`.
- [ ] **Step 6: PR with `Closes #<N>` + `Part of #978`, watch checks, squash-merge, sentinel-verify** — `git show origin/main:.claude/loops/_run-local.sh | grep _summarize-run` must hit after merge.

---

## PR 2 — repo restructure (prompts-only `.claude/loops/`, runner → `ops/fleet/`, CCR → `ops/fleet/ccr/`)

### Task 5: Issue, branch, and the moves

- [ ] **Step 1: File the issue**

```bash
gh issue create --repo logi-x/experts \
  --title "fleet step 2: restructure — .claude/loops prompts-only, runner in ops/fleet, CCR mirror in ops/fleet/ccr, delete pulse" \
  --body "Part of #978. Pure git mv + path fixes, no prompt content changes. Spec §7. Also fixes the stale .claude/routines/ paths in the CI enable-gate (broken since the loops rename) and the live crontab paths."
```

- [ ] **Step 2: Branch** — `git checkout main && git pull --ff-only && git checkout -b chore/gh-<N>-fleet-restructure`.

- [ ] **Step 3: Delete pulse** (debug scaffolding, spec §2):

```bash
git rm .claude/loops/00-pulse.json .claude/loops/00-pulse.prompt.md
```

- [ ] **Step 4: Create dirs and move everything** (exact list — run from repo root):

```bash
mkdir -p ops/fleet/contracts ops/fleet/ccr
# runner + local infra
git mv .claude/loops/_run-local.sh        ops/fleet/run-local.sh
git mv .claude/loops/_summarize-run.py    ops/fleet/summarize-run.py
git mv .claude/loops/_pool-dispatch.sh    ops/fleet/pool-dispatch.sh
git mv .claude/loops/_setup-worktrees.sh  ops/fleet/setup-worktrees.sh
git mv .claude/loops/_crontab.txt         ops/fleet/crontab.txt
git mv .claude/loops/_settings.json       ops/fleet/settings.json
# shared behavioral contracts
git mv .claude/loops/_dedup-protocol.md          ops/fleet/contracts/dedup-protocol.md
git mv .claude/loops/_github-issues-contract.md  ops/fleet/contracts/github-issues-contract.md
# CCR mirror (configs keep <name>.json — see spec-deviation note)
for f in .claude/loops/0*.json; do git mv "$f" "ops/fleet/ccr/$(basename "$f")"; done
git mv .claude/loops/_index.json  ops/fleet/ccr/index.json
git mv .claude/loops/_sync.ts     ops/fleet/ccr/sync.ts
git mv .claude/loops/package.json ops/fleet/ccr/package.json
```

- [ ] **Step 5: Verify the end state**

Run: `ls .claude/loops/ && ls ops/fleet/ ops/fleet/contracts/ ops/fleet/ccr/`
Expected `.claude/loops/`: exactly `01-sentinel.prompt.md … 08-overwatch.prompt.md` (8 files, no `00-pulse*`) + `README.md`.

### Task 6: Path updates — every consumer in the same diff

**Files:**

- Modify: `ops/fleet/run-local.sh`, `ops/fleet/pool-dispatch.sh`, `ops/fleet/setup-worktrees.sh`, `ops/fleet/crontab.txt`, `ops/fleet/ccr/sync.ts`
- Modify: `.github/workflows/routine-enable-gate.yml`, `.github/scripts/detect-routine-enable-flip.sh`
- Modify: `.claude/loops/01-sentinel.prompt.md`, `.claude/loops/03-rover.prompt.md`, `.claude/loops/06-salvage.prompt.md` (contract references only)

- [ ] **Step 1: `ops/fleet/run-local.sh`** — four edits:

(a) `REPO_ROOT` (old line 39): `"$HERE/../.."` still resolves correctly (`ops/fleet` → root). No change. **Verify, don't assume:** after Step 1 run `bash -c 'HERE=ops/fleet; cd $HERE/../.. && pwd'` → repo root.

(b) Prompt path (old line 40):

```bash
# old: PROMPT="$HERE/${NAME}.prompt.md"
PROMPT="$REPO_ROOT/.claude/loops/${NAME}.prompt.md"
```

Note: `$REPO_ROOT` is defined on the line above `PROMPT` — keep that order.

(c) Settings resolution (old lines 93–96):

```bash
# old: ROUTINE_SETTINGS_FILE="$HERE/${NAME}.settings.json"  / fallback "$HERE/_settings.json"
ROUTINE_SETTINGS_FILE="$HERE/${NAME}.settings.json"
if [ ! -f "$ROUTINE_SETTINGS_FILE" ]; then
  ROUTINE_SETTINGS_FILE="$HERE/settings.json"
fi
```

(only the fallback filename changes: `_settings.json` → `settings.json`; per-loop overrides now live next to the runner, documented in the header comment).

(d) Summarizer path (from Task 2): `"$HERE/_summarize-run.py"` → `"$HERE/summarize-run.py"`.

(e) Header comments (old lines 2–12): replace every `.claude/routines/_run-local.sh` with `ops/fleet/run-local.sh`.

- [ ] **Step 2: `ops/fleet/pool-dispatch.sh`** — `sed -i 's|\.claude/routines/_run-local\.sh|ops/fleet/run-local.sh|g; s|\.claude/routines/_pool-dispatch\.sh|ops/fleet/pool-dispatch.sh|g' ops/fleet/pool-dispatch.sh`, then hand-check the slot-runner line (old line 73) reads:

```bash
slot_runner="${slot_dir%/}/ops/fleet/run-local.sh"
```

(Slot worktrees track main; the new path exists in them after this PR merges — note in PR body: run `ops/fleet/setup-worktrees.sh cleanup` once after merge so slots fast-forward.)

- [ ] **Step 3: `ops/fleet/setup-worktrees.sh`** — same sed for both script paths, plus fix the stale example (old line 225):

```bash
# old: echo "Test a slot: bash .claude/routines/_pool-dispatch.sh 03-fix-bugs"
echo "Test a slot: bash ops/fleet/pool-dispatch.sh 03-rover"
```

- [ ] **Step 4: `ops/fleet/crontab.txt`** — replace every `/home/logix/experts/.claude/routines/_run-local.sh` with `/home/logix/experts/ops/fleet/run-local.sh` (5 entries + comment lines). These paths have been stale since the routines→loops rename (cron currently fails silently) — the PR body must carry the operator step: `crontab -l` to back up, then paste the new file.

- [ ] **Step 5: `ops/fleet/ccr/sync.ts`** — three edits:

(a) After the `HERE` constant (old line 27), add:

```typescript
const REPO_ROOT = join(HERE, '..', '..', '..')
const PROMPTS_DIR = join(REPO_ROOT, '.claude', 'loops')
```

(b) Index filename (old lines 46, 182): `join(HERE, "_index.json")` → `join(HERE, "index.json")`; the two log strings mentioning `_index.json` → `index.json`.

(c) `@prompt:` resolution baseDir (old lines 85 and 158): `resolve(raw, HERE)` → `resolve(raw, PROMPTS_DIR)` in both places. Usage comments: `.claude/routines/_sync.ts` → `ops/fleet/ccr/sync.ts`.

- [ ] **Step 6: CI gate paths** — in `.github/workflows/routine-enable-gate.yml` (lines 14–16) and `.github/scripts/detect-routine-enable-flip.sh` (lines 16–18) replace `.claude/routines/0X-*.json` with:

```
ops/fleet/ccr/06-salvage.json
ops/fleet/ccr/07-observatory.json
ops/fleet/ccr/08-overwatch.json
```

(numbers are the post-loops-rename ones — salvage is 06, observatory 07, overwatch 08; the old `07/08/09` in those files are doubly stale).

- [ ] **Step 7: Contract references inside prompts** —

```bash
sed -i 's|`_github-issues-contract\.md`|`ops/fleet/contracts/github-issues-contract.md`|g; s|`_dedup-protocol\.md`|`ops/fleet/contracts/dedup-protocol.md`|g' \
  .claude/loops/01-sentinel.prompt.md .claude/loops/03-rover.prompt.md .claude/loops/06-salvage.prompt.md
```

- [ ] **Step 8: Leftover scan** — `grep -rn "claude/routines\|_run-local\|_pool-dispatch\|_setup-worktrees\|_crontab\|_settings\.json\|_index\.json\|_sync\.ts\|_dedup-protocol\|_github-issues-contract\|00-pulse" .claude/loops ops .github CLAUDE.md AGENTS.md docs/superpowers/specs/2026-06-11-* 2>/dev/null | grep -v worktrees`
      Expected: zero hits (fix any stragglers — including `CLAUDE.md`/`AGENTS.md` if they mention old paths).

### Task 7: Rewrite `.claude/loops/README.md` as the one-page index

- [ ] **Step 1: Replace the full file content with:**

```markdown
# Agent loops

Prompts only — one file per loop, like `.claude/skills/` and `.claude/agents/`.
Everything else lives elsewhere:

| What                        | Where                                                   |
| --------------------------- | ------------------------------------------------------- |
| Local runner + cron         | `ops/fleet/` (`run-local.sh`, `crontab.txt`)            |
| Worktree pool (rover slots) | `ops/fleet/` (`pool-dispatch.sh`, `setup-worktrees.sh`) |
| Shared behavioral contracts | `ops/fleet/contracts/`                                  |
| Cloud (CCR) mirror          | `ops/fleet/ccr/` — optional, deletable as a unit        |
| Cost feed + run logs        | `.cache/experts-routines/` (never committed)            |
| Fleet memory (lessons)      | `~/brain/fleet/lessons.md`                              |

## The loops (design: docs/superpowers/specs/2026-06-11-fleet-redesign-flight-director-design.md)

| Prompt                     | Phase          | Job                                                 |
| -------------------------- | -------------- | --------------------------------------------------- |
| `01-sentinel.prompt.md`    | Discover       | security scan (merging into scout in Phase B)       |
| `02-radar.prompt.md`       | Discover       | correctness scan (merging into scout)               |
| `03-rover.prompt.md`       | Plan + Execute | pick one agent-filed issue, ship one PR             |
| `04-telemetry.prompt.md`   | Memory         | docs digest (becomes memory loop in Phase C)        |
| `05-airlock.prompt.md`     | Verify         | review + merge agent PRs                            |
| `06-salvage.prompt.md`     | Discover       | completeness audit (merging into scout)             |
| `07-observatory.prompt.md` | Iterate        | board audit (absorbed by flight-director, Phase C)  |
| `08-overwatch.prompt.md`   | Verify         | fleet drift audit (becomes airlock rubric, Phase C) |

## Run one locally

    bash ops/fleet/run-local.sh 05-airlock [--dry-run] [--verbose]

Install the cron: see `ops/fleet/crontab.txt`. Maker≠checker: rover ships,
airlock merges — never the same session (see `experts-ship` skill, gatekeeper
appendix).
```

### Task 8: Gates, ship, operator steps

- [ ] **Step 1: Gates, each as its own step:**

```bash
bash -n ops/fleet/run-local.sh && bash -n ops/fleet/pool-dispatch.sh && bash -n ops/fleet/setup-worktrees.sh && echo SHELL-OK
for j in ops/fleet/ccr/*.json ops/fleet/settings.json; do node -e "JSON.parse(require('fs').readFileSync('$j','utf8'))" || echo "FAIL $j"; done; echo JSON-OK
python3 -m py_compile ops/fleet/summarize-run.py && echo PY-OK
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/routine-enable-gate.yml'))" && echo YAML-OK
bash ops/fleet/run-local.sh 01-sentinel --dry-run | tail -2   # proves prompt resolution from the new layout
npx tsc --noEmit --module nodenext --moduleResolution nodenext ops/fleet/ccr/sync.ts 2>&1 | head -5 || true  # informational; sync.ts has no tsconfig — eyeball errors are import-path only
```

- [ ] **Step 2: Commit** (one commit, it's one logical move) with trailer; **Step 3: push branch:branch + verify SHA; Step 4: PR** — body carries `Closes #<N>`, `Part of #978`, the spec-deviation note, and **Operator steps after merge:**
    1. Reinstall the crontab from `ops/fleet/crontab.txt` (current installed crontab points at `.claude/routines/` — already dead).
    2. Run `bash ops/fleet/setup-worktrees.sh cleanup` so rover slots fast-forward to the new layout.
    3. Disable the cloud `00-pulse` trigger (claude.ai UI or `RemoteTrigger`) — its repo files are gone.
- [ ] **Step 5: Watch CI** — note the enable-gate workflow itself is modified here; it triggers on its own paths, expect it to run and pass (no `enabled` flips in this diff). The `tool-grant-alert` gate may fire for `.claude/loops` moves — if it does, the human applies `tool-grant-approved` (do NOT re-run the stale failed run; toggle the label).
- [ ] **Step 6: Squash-merge, sentinel-verify** — `git show origin/main:ops/fleet/run-local.sh | grep "claude/loops" | head -2` must show the new PROMPT path; `git ls-tree origin/main .claude/loops/ | wc -l` → 9 (8 prompts + README).
- [ ] **Step 7: Post-merge resync** — `git checkout main && git pull --ff-only`. Skip `gitnexus:analyze` (no app code symbols moved).

---

## Out of scope for Phase A (later plans)

- Phase B: scout merge (sentinel+radar+salvage → `01-scout.prompt.md`), `preflight.sh` zero-token gates, renumber to the final 5, re-enable pipeline.
- Phase C: telemetry → memory loop (`~/brain/fleet/lessons.md` seed + runner lessons injection + read-side truncation), flight-director prompt + airlock fleet-config rubric + CI path-guard.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
