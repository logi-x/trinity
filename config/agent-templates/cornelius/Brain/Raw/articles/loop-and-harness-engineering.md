<article class="x-article"><img src="https://pbs.twimg.com/media/HL2SvKHWgAAaZw2.jpg" alt="Cover image">
<p><strong>Most builders fight the loop. The loop is fine. The folder underneath isn't set up.</strong></p>
<p>Open .claude/ in any working Claude Code project and you find roughly seven things doing the actual work: CLAUDE.md, settings.json, hooks/, agents/, skills/, .mcp.json, and a state file like MEMORY.md.</p>
<p>Most builders have opened one of those files. Maybe two. That is why their loops stall on the third iteration.</p>
<p>By the end of this article you will know what each file does, the five loop steps that ride on top, the three failure modes that kill most first attempts, and the single next file to add tonight.</p>
<p>No framework. No subscription. One walkthrough with exact paths and exact contents.</p>
<p>The harness is the floor. Pour it first.</p>
<p>Two layers, one setup</p>
<p>The harness is the .claude/ folder. It does not change between runs.</p>
<p>The loop is what runs inside it: a goal, an action, a verification step, a memory write, and a decision to keep going or stop.</p>
<p>The harness is the kitchen. The loop is the recipe.</p>
<p>Both fail without the other. A kitchen with no recipe is unused space. A recipe with no kitchen is wishful thinking.</p>
<p>Most builders treat the whole thing as one blob ("my agent setup") and miss that failures live in different layers.</p>
<p>Token blowups, prompt fatigue, dropped permissions: harness problems. Loops that never converge, verifications that pass garbage, scheduled runs that drift: loop problems.</p>
<p>Naming the layer fixes the diagnosis. You stop rewriting prompts when the real bug is a missing permission.</p>
<p>I thought building the loop first would teach me which harness files I needed. It was the other way around.</p>
<p>The harness sets what each iteration is allowed to do. Permissions decide whether the loop can write to disk. Subagents decide whether verification runs in a clean context.</p>
<p>Skills decide whether the loop can specialize. Hooks decide whether the loop even gets to fire on the trigger you wanted.</p>
<p>Without those decisions locked in, the loop guesses. When the loop guesses, it fabricates: invented files, invented commands, passing tests that pass nothing.</p>
<p>The harness stops the guessing. So the order is harness first, loop second, always.</p>
<p>The harness, file by file</p>
<h2>CLAUDE.md</h2>
<p>The first file Claude Code reads on every launch. Its contents become standing context for the entire session.</p>
<p>Put the project shape there: directory layout, language and framework, commands that actually work, conventions the agent must respect, and an explicit list of things it must not do.</p>
<p><strong>Lives at repo root, not buried in docs. Minimal working shape:</strong></p>
<pre><code># Project: my-app
Stack: Next.js 14, TypeScript, Postgres, Tailwind.
Layout: `app/` (routes), `lib/` (helpers), `db/migrations/`.

## Commands
- `pnpm dev` - local
- `pnpm test` - vitest
- `pnpm db:migrate` - apply migrations

## Never
- Edit `db/migrations/*` after merge.
- Add deps without justification in the PR body.
- Bypass `lib/auth/` to access user data.</code></pre>
<p>The trap is bloat. The paper <a href="https://arxiv.org/abs/2606.10209">Less Context, Better Agents (arXiv 2606.10209)</a> measured task completion dropping from <strong>91.6%</strong> to <strong>71%</strong> purely from oversized standing context.</p>
<p>Keep it under 300 lines. Prune it weekly. Every added paragraph is a tax on every future turn.</p>
<p>The canonical reference is <a href="https://github.com/centminmod/my-claude-code-setup">centminmod/my-claude-code-setup</a>, which ships three working CLAUDE.md shapes side by side.</p>
<figure><img src="https://pbs.twimg.com/media/HL5U4TbWgAArdOa.jpg" alt=""></figure>
<h2>settings.json</h2>
<p>Where the tool allowlist, environment variables, and hook registrations live.</p>
<p>Two locations matter for daily work: .claude/settings.json at repo root for repo-scoped rules, and ~/.claude/settings.json for your personal defaults.</p>
<p>Scope hierarchy resolves managed &gt; project &gt; local &gt; user, so project always overrides personal.</p>
<p><strong>The first move that pays off in one afternoon is an allow array for read-only Bash and MCP calls:</strong></p>
<pre><code>{
  "permissions": {
    "allow": [
      "Bash(ls:*)",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(cat:*)",
      "Read(*)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(git push --force:*)"
    ]
  }
}</code></pre>
<p>The agent stops blocking on permission prompts for every ls, git status, cat. Destructive ops still gate.</p>
<p>Full key reference: <a href="https://docs.anthropic.com/en/docs/claude-code/settings">Claude Code docs - Settings</a>. Keep secrets in .claude/settings.local.json and gitignore it.</p>
<h2>hooks</h2>
<p>Deterministic scripts that fire on tool events: PreToolUse before a tool runs, PostToolUse after, Stop when the agent finishes a turn.</p>
<p>Registered inside settings.json with a matcher pattern and a shell command. Canonical first hook: a PostToolUse matching Edit|Write that pipes the file through prettier.</p>
<pre><code>{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {"type": "command", "command": "npx prettier --write \"$CLAUDE_FILE_PATH\""}
        ]
      }
    ]
  }
}</code></pre>
<p>Every edit now exits in a known state. This is your policy floor.</p>
<p>Without hooks, every run is a vibe. Keep hooks silent on success, loud only on failure. Reference: <a href="https://docs.anthropic.com/en/docs/claude-code/hooks">Claude Code docs - Hooks</a>.</p>
<h2>subagents</h2>
<p>Live under .claude/agents/ as markdown files with YAML frontmatter. Main agent invokes them through the Task tool. They run in a fresh context window.</p>
<p><strong>Minimal verifier subagent:</strong></p>
<pre><code>---
name: verifier
description: Reviews a diff against the goal spec. Invoke after every code change.
model: haiku
tools: [Read, Grep, Bash]
---

You are a verifier. Read the goal spec in `PROMPT.md`. Read the diff.
Return a JSON verdict: {passes: bool, failures: [{line, reason}]}.
Do not propose fixes. Do not run code. Do not be polite.</code></pre>
<p>The reviewer that lives inside the maker's context always agrees with itself. Pulling review into a fresh context closes the loudest failure mode.</p>
<p>Reference: <a href="https://github.com/wshobson/agents">wshobson/agents</a> (<strong>37K stars</strong>) for 194 ready-made shapes. For an adversarial verifier with 11 named shortcut-checks (relaxed tests, swallowed errors, fake renames), pull <a href="https://github.com/moonrunnerkc/swarm-orchestrator">moonrunnerkc/swarm-orchestrator</a>.</p>
<figure><img src="https://pbs.twimg.com/media/HL5VyAAWwAAZXAX.jpg" alt=""></figure>
<h2>skills</h2>
<p>Live under .claude/skills/ as folders containing SKILL.md with YAML frontmatter.</p>
<p>Load progressively: at session start, only name and description enter context. Full body loads only when the agent decides the trigger matches.</p>
<pre><code>---
name: db-migration-writer
description: Writes Postgres migration files for this repo. Use when the user
  asks to add/alter a table, column, index, or constraint.
when_to_use: schema change requested, new feature requires a new column,
  index missing on a hot query path
---

# Steps
1. Read `db/schema.sql` to confirm current state.
2. Write the migration to `db/migrations/NNN_&lt;verb&gt;_&lt;noun&gt;.sql`.
3. Include both up and down. Test with `pnpm db:migrate --dry`.
4. Never touch existing migration files.</code></pre>
<p>This discipline keeps a fifty-skill library from costing fifty skills' worth of tokens on every prompt.</p>
<p>Canonical pattern: <a href="https://github.com/anthropics/skills">anthropics/skills</a> (<strong>155K stars</strong>). Maximal pre-built kit: <a href="https://github.com/affaan-m/ECC">affaan-m/ECC</a> (<strong>222K stars</strong>).</p>
<figure><img src="https://pbs.twimg.com/media/HL5WWGsW4AAxnSd.jpg" alt=""></figure>
<p>Three skills built when you hit the same task a third time beat fifty skills built speculatively from a tutorial.</p>
<h2>MCP</h2>
<p>Servers declared in .mcp.json at repo root. Model Context Protocol is the spec that lets the loop call out to live external tools.</p>
<p>Three rules: only servers your current work uses, prefer official ones for credentialed tools, never install five "just in case".</p>
<pre><code>{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {"GITHUB_TOKEN": "${GITHUB_TOKEN}"}
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}</code></pre>
<p>Anthropic-maintained set: <a href="https://github.com/modelcontextprotocol/servers">modelcontextprotocol/servers</a> (<strong>87K stars</strong>). 
Code-host integration: <a href="https://github.com/github/github-mcp-server">github/github-mcp-server</a> (<strong>31K stars</strong>).</p>
<p>Live library docs (kills stale-API problems): <a href="https://github.com/upstash/context7">upstash/context7</a> (<strong>58K stars</strong>). 
Discovery index: <a href="https://github.com/punkpeye/awesome-mcp-servers">punkpeye/awesome-mcp-servers</a> (<strong>89K stars</strong>).</p>
<p>The first mistake is enabling a server with write scope before you have a hook that logs every call.</p>
<h2>state and memory</h2>
<p>The seventh piece, the one most people skip until the third project goes sideways.</p>
<p>Shape: a MEMORY.md index file at a known path, plus a vault directory for project canon.</p>
<pre><code>~/.claude/memory/
  MEMORY.md            # index, links to topic files below
  user-prefs.md        # preferences, terse-vs-verbose, voice
  project-decisions.md # "we picked Postgres over Mongo on 2026-03-12, here is why"
  feedback-recent.md   # corrections you keep applying

~/vault/               # project canon (does not change session to session)
  architecture.md
  api-spec.md
  post-mortems/</code></pre>
<p>Memory holds what changes across sessions. Vault holds what does not.</p>
<p>For production-grade session compression (200K-token transcript -&gt; 4K-token recap without losing load-bearing facts): <a href="https://github.com/thedotmack/claude-mem">thedotmack/claude-mem</a> (<strong>84K stars</strong>).</p>
<p>Theory behind why this matters: <a href="https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents">Anthropic engineering on context engineering</a> names the failure mode: context rot.</p>
<p>The first mistake is treating memory as append-only. Prune it every session, or it becomes the rot.</p>
<p>The loop, on top of the harness</p>
<h2>1. Goal spec</h2>
<p>The external contract that says what "done" looks like. Lives on disk, not in the agent's head. The loop re-reads it every iteration.</p>
<p><strong>Name: PROMPT.md, AGENTS.md, or AGENT_SPEC.md. The re-read is what matters.</strong></p>
<pre><code># Goal
Migrate `users.password` from bcrypt to argon2id across the codebase.

# Done when
- All new password writes use argon2id (`lib/auth/hash.ts`).
- Existing bcrypt hashes are rehashed on next successful login.
- Test suite green: `pnpm test auth`.

# Never touch
- `db/migrations/*` already merged.
- Anything under `legacy/`.
- The session cookie format.

# Stop if
- More than 3 files outside `lib/auth/` need edits.
- A test that already passes starts failing.</code></pre>
<p>Without this file the agent drifts after about three iterations. Smallest possible reference: <a href="https://github.com/ghuntley/how-to-ralph-wiggum">ghuntley/how-to-ralph-wiggum</a> (1.7K stars) - PROMPT.md plus an IMPLEMENTATION_PLAN.md state file the loop updates in place.</p>
<p>When the spec is missing, failure looks like progress. Code is written, tests pass, the goal it solved is not yours.</p>
<h2>2. Plan to Act to Verify</h2>
<p>The minimum viable loop is three steps. The agent plans against the goal spec, executes, then a separate verification pass checks the result before the next iteration is allowed to start.</p>
<p>Fresh context each iteration is the Ralph pattern. State lives on disk in the spec file plus a running log.</p>
<pre><code>#!/usr/bin/env bash
# minimal loop runner: fresh context each turn, state on disk
set -euo pipefail

while true; do
  # plan + act in fresh context
  claude -p "Read PROMPT.md, IMPLEMENTATION_PLAN.md. Do the next step. Commit on green."

  # verify in fresh context (different subagent)
  if claude -p "/verify"; then
    echo "iter ok"
  else
    echo "verify failed, will retry"
  fi

  # exit when spec says done
  grep -q "^STATUS: done$" IMPLEMENTATION_PLAN.md &amp;&amp; break
  sleep 5
done</code></pre>
<p>Canonical patterns and CLI starters: <a href="https://github.com/cobusgreyling/loop-engineering">cobusgreyling/loop-engineering</a> (3K stars).</p>
<p>Production TypeScript reference with verifyCompletion: <a href="https://github.com/vercel-labs/ralph-loop-agent">vercel-labs/ralph-loop-agent</a> (805 stars).</p>
<p>Full installable Plan-to-Work-to-Review-to-Release cycle: <a href="https://github.com/Chachamaru127/claude-code-harness">Chachamaru127/claude-code-harness</a> (2.9K stars).</p>
<p>Drop the verify step and confident garbage compounds. Every wrong output becomes the next iteration's input.</p>
<h2>3. Sub-agent fan-out</h2>
<p>When one goal branches into many independent sub-jobs (analyze 10 articles, fix 5 files, search 8 sources), the loop spawns parallel subagents. Orchestrator synthesizes.</p>
<p><strong>One bloated context cannot do this. Ten small ones can.</strong></p>
<pre><code># claude-agent-sdk-python style fan-out
from claude_agent_sdk import Agent, run_parallel

orchestrator = Agent.load(".claude/agents/orchestrator.md")
workers = [Agent.load(".claude/agents/researcher.md") for _ in range(8)]

results = run_parallel([
    w.run(source=src) for w, src in zip(workers, sources)
])

synthesis = orchestrator.run(inputs=results)</code></pre>
<p><a href="https://www.anthropic.com/engineering/built-multi-agent-research-system">Anthropic engineering on multi-agent research</a> measured <strong>+90.2%</strong> on their internal eval against a single-agent baseline.</p>
<p>Official SDK: <a href="https://github.com/anthropics/claude-agent-sdk-python">anthropics/claude-agent-sdk-python</a> (7.4K stars). Heaviest public fan-out kit (60+ agent types, 314 MCP tools): <a href="https://github.com/ruvnet/ruflo">ruvnet/ruflo</a> (61K stars).</p>
<p>Skip the fan-out and the orchestrator drowns. One context loaded with ten jobs' worth of source material is the exact shape that triggers context rot.</p>
<h2>4. Scheduler and persistence</h2>
<p>What triggers the loop when you are not in the chair. cron, launchctl, systemd, a queue runner.</p>
<p>The scheduler is deliberately dumber than the agent. If the scheduler tries to think (branch on state, decide whether to skip), it fails silently for days.</p>
<pre><code># crontab: run the loop every 30 min, log to disk
*/30 * * * * cd ~/my-loop &amp;&amp; ./run.sh &gt;&gt; logs/$(date +\%Y-\%m-\%d).log 2&gt;&amp;1</code></pre>
<p><strong>Or as a launchd plist on macOS:</strong></p>
<pre><code>&lt;key&gt;StartCalendarInterval&lt;/key&gt;
&lt;dict&gt;
  &lt;key&gt;Minute&lt;/key&gt;&lt;integer&gt;0&lt;/integer&gt;
&lt;/dict&gt;
&lt;key&gt;WorkingDirectory&lt;/key&gt;&lt;string&gt;/Users/me/my-loop&lt;/string&gt;
&lt;key&gt;ProgramArguments&lt;/key&gt;
&lt;array&gt;&lt;string&gt;/bin/bash&lt;/string&gt;&lt;string&gt;run.sh&lt;/string&gt;&lt;/array&gt;</code></pre>
<p>Persistence is the other half. Every iteration must serialize what it did, what it tried, what is next. Otherwise the scheduler wakes up to an agent that forgot the goal.</p>
<p>Pattern for promoting ad-hoc sessions into scheduled runs: <a href="https://github.com/Kanevry/session-orchestrator">Kanevry/session-orchestrator</a>.</p>
<h2>5. Failure modes</h2>
<p>Three failure modes kill almost every first attempt:</p>
<p>(a) Confident garbage. Verify step missing or weak. Wrong outputs pass and compound across iterations.</p>
<p>(b) Context rot. Single long context where the model degrades past a threshold (Anthropic's term). Accuracy collapses around 200K tokens of accumulated history.</p>
<p>(c) Ralph Wiggum loops. Same iteration repeats because state on disk did not capture progress. The agent re-plans the step it already finished.</p>
<p>The <a href="https://arxiv.org/abs/2606.10209">Less Context, Better Agents paper (arXiv 2606.10209)</a> measured full-history at <strong>71%</strong> task completion versus prune-and-summarize at <strong>91.6%</strong>, on a fraction of the tokens.</p>
<figure><img src="https://pbs.twimg.com/media/HL5ZlSkXgAA09wS.png" alt=""></figure>
<pre><code>before: single-context loop, 1.48M tokens, 71% completion, three hidden hallucinations per run
after:  prune-and-summarize loop with verifier subagent, 553K tokens, 91.6% completion, every figure traced</code></pre>
<p><a href="https://github.com/moonrunnerkc/swarm-orchestrator">moonrunnerkc/swarm-orchestrator</a> catalogs the 11 shortcuts agents take to fake done: relaxed tests, swallowed errors, fake renames, stub returns, comment-deletion-as-fix.</p>
<p><strong>Memorize the names. You will recognize them in your own logs.</strong>

A complete minimal setup wires all seven harness files into a working loop. The shape of a project directory looks like this:</p>
<pre><code>my-loop/
├── .claude/
│   ├── CLAUDE.md            # standing context for every session
│   ├── settings.json        # allow array + PostToolUse prettier hook
│   ├── agents/
│   │   └── verifier.md      # Haiku, reviews diffs in fresh context
│   └── skills/
│       └── db-migration-writer/
│           └── SKILL.md     # one skill, used three+ times
├── .mcp.json                # github MCP, context7 MCP
├── PROMPT.md                # goal spec (loop reads each iteration)
├── IMPLEMENTATION_PLAN.md   # state file (loop writes each iteration)
├── MEMORY.md                # cross-session preferences
├── run.sh                   # the loop runner (Plan -&gt; Act -&gt; Verify)
└── logs/                    # persistence, one file per cron tick</code></pre>
<p>The wiring is one-directional. The harness defines the rules, the loop runs inside them, the state file connects iteration N to iteration N+1.</p>
<p>A single iteration walks the seven harness files and the five loop pieces in this order: cron fires <a href="https://x.com/ArchiveExplorer/status/run.sh">run.sh</a>, which calls claude -p. Claude Code reads CLAUDE.md and settings.json (harness 1, 2), applies the PostToolUse hook on every edit (harness 3), reads PROMPT.md and IMPLEMENTATION_PLAN.md (loop step 1), plans and acts (loop step 2), dispatches the verifier subagent in a fresh context (harness 4 + loop step 2 verify), writes the result back to IMPLEMENTATION_PLAN.md (loop step 3), updates MEMORY.md if a new preference was learned (harness 7), exits. Cron waits for the next tick (loop step 4).</p>
<p>If any of the seven harness files is missing, a specific loop step degrades. No CLAUDE.md and the planner re-derives the project shape every iteration. No verifier subagent and the verify step happens in the main context and always passes. No MEMORY.md and the same correction gets re-applied every Tuesday.</p>
<p>Build the seven harness files once. The loop runs forever.</p>
<p>What to do tonight</p>
<p><strong>Open your .claude/ folder. Run:</strong></p>
<pre><code>ls -la .claude/</code></pre>
<p><strong>Count the files.</strong></p>
<p>If you see nothing or only settings.json, start with CLAUDE.md. Keep it under 300 lines. Copy a shape from <a href="https://github.com/centminmod/my-claude-code-setup">centminmod/my-claude-code-setup</a>.</p>
<p>If you have CLAUDE.md and settings.json but no agents/, add a verifier subagent next. Pull review out of the main context. Shape: <a href="https://github.com/wshobson/agents">wshobson/agents</a>.</p>
<p>If you have agents/ but no skills/, promote one frequent task to a skill. The prompt you have copy-pasted three times this week. Read three SKILL.md files from <a href="https://github.com/anthropics/skills">anthropics/skills</a> before you write your first one.</p>
<p>If you have all seven harness files but no loop running, pick one repeating job, write its goal spec, and put a Plan-Act-Verify loop on top. Closest installable starting point: <a href="https://github.com/Chachamaru127/claude-code-harness">Chachamaru127/claude-code-harness</a>.</p>
<p>After choosing, do one thing: open the matching repo in a new tab and clone it.</p>
<p><strong>The harness is the floor. Without it, every loop runs over a hole.</strong></p></article>
