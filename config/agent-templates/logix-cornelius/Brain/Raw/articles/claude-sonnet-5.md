<article class="x-article"><img src="https://pbs.twimg.com/media/HMIjo6xXsAANZ1p.jpg" alt="Cover image">
<p>Claude Sonnet 5 dropped yesterday at near-Opus quality for 60% less. Most people will just switch models and leave the real savings on the table.</p>
<p>The wins are in the config: effort control, model routing, and the intro-price window before it closes on August 31.</p>
<p>Set it up right and you get Opus-level results on most tasks while spending a fraction of what you did last week.</p>
<p><strong>Here's the full setup �</strong>�</p>
<p>Before we dive in, I share daily notes on AI &amp; vibe coding in my Telegram channel: <strong><a href="https://t.me/zodchixquant">https://t.me/zodchixquant</a></strong>🧠</p>
<figure><img src="https://pbs.twimg.com/media/HMIMbdjXsAAxn6q.jpg" alt=""></figure>
<h2>Why this launch matters for your bill</h2>
<p>Sonnet 5 lands close to Opus 4.8 on agentic coding and actually edges it on knowledge work, while costing far less. Standard pricing is about 40% cheaper per token than Opus, and during the intro window it's roughly 60% cheaper.</p>
<p>That changes the math. Tasks you used to send to Opus for quality can now go to Sonnet 5 and come back nearly as good for a fraction of the cost. The trick is setting it up so the savings are automatic, not something you think about each time.</p>
<p>Three pieces do that: effort control, smart routing, and locking in the intro price. </p>
<p>Here's each.</p>
<figure><img src="https://pbs.twimg.com/media/HMINJQ8WQAAnNh6.jpg" alt=""></figure>
<h2>1. Effort control: pay for thinking only when it helps</h2>
<p>The biggest new lever is effort level. Sonnet 5 lets you dial how hard it thinks, and Anthropic raised the rate limits so you can push it when a task deserves it. </p>
<p>Low effort is cheap and fast for simple work. High effort costs more but rivals Opus on hard tasks.</p>
<p>The mistake is running everything at one level. Set a sensible default and let hard tasks opt up. <strong>In your settings.json:</strong></p>
<pre><code class="language-json" data-lang="json">{
  "model": "claude-sonnet-5",
  "effort": "medium"
}
</code></pre>
<p>Then, in CLAUDE.md, tell Claude when to spend more:</p>
<pre><code class="language-markdown" data-lang="markdown">## Effort policy
- Default to medium effort for normal work.
- Use high effort only for: tricky debugging, multi-file
  refactors, architecture decisions.
- Use low effort for: formatting, renames, simple edits,
  boilerplate.

Match the effort to the task. Don't burn high effort on trivial work.</code></pre>
<p>Now you pay for deep thinking on the 20% of tasks that need it, and stay cheap on the 80% that don't. </p>
<p>That single split is where most of the savings live.</p>
<figure><img src="https://pbs.twimg.com/media/HMIMiRjX0AAVP3q.jpg" alt=""></figure>
<h2>2. Route the hard stuff to Opus, keep the rest on Sonnet 5</h2>
<p>Sonnet 5 handles most work at near-Opus quality, but Opus 4.8 still wins on the very hardest reasoning. </p>
<p>The cost-optimal setup isn't "Sonnet 5 for everything," it's Sonnet 5 as the default with a clear rule for when to reach for Opus.</p>
<p>Put the routing rule in CLAUDE.md so it's automatic:</p>
<pre><code class="language-markdown" data-lang="markdown">## Model routing
Default: Claude Sonnet 5. Use it for coding, tool use,
refactors, and day-to-day work.

Escalate to Opus 4.8 only when:
- Sonnet 5 has failed the same task twice, or
- the task needs the deepest reasoning (complex system
  design, subtle correctness proofs).

Start on Sonnet 5. Escalate on evidence, not by default.</code></pre>
<p>This keeps 90% of your work on the cheaper model and spends Opus money only where it actually changes the outcome. Most people overpay by defaulting to the biggest model out of habit. </p>
<p>The rule fixes that without you thinking about it.</p>
<h2>3. Lock in the intro price before August 31</h2>
<p>Here's the time-sensitive part. </p>
<p>Sonnet 5 launched at $2 per million input tokens and $10 per million output, but that intro pricing ends August 31, 2026, after which it rises to $3 and $15. That's a 50% jump on both.</p>
<p><strong>A simple move: </strong>if you have large one-time jobs on the roadmap, like a big migration, a codebase-wide refactor, or bulk generation, pull them into the intro window instead of pushing them past it. Same work, up to a third less cost, purely on timing.</p>
<figure><img src="https://pbs.twimg.com/media/HMIRuNCXQAA0b4S.png" alt=""></figure>
<h2>The full config, ready to copy</h2>
<p>Here's everything together. In settings.json:</p>
<pre><code>{
  "model": "claude-sonnet-5",
  "effort": "medium"
}
</code></pre>
<p>In CLAUDE.md:</p>
<pre><code>## Effort policy
- Medium by default.
- High only for: hard debugging, multi-file refactors,
  architecture calls.
- Low for: formatting, renames, boilerplate.

## Model routing
- Default to Sonnet 5 for everything.
- Escalate to Opus 4.8 only after two failed Sonnet attempts,
  or for the deepest reasoning tasks.

## Cost note
- Intro pricing ($2/$10) ends Aug 31, 2026. Run large batch
  jobs before then where possible.</code></pre>
<p>Drop that in and your setup defaults to cheap, spends on quality only when the task earns it, and uses the intro window on purpose.</p>
<h2>Where Sonnet 5 beats Opus, and where it doesn't</h2>
<p>This is the part the announcement glosses over, and it's what actually decides your routing. Sonnet 5 isn't uniformly "almost Opus." It beats Opus on some work, trails it on others, and knowing which is which is the whole game.</p>
<p>Route by task type:</p>
<ul><li><strong>Knowledge work → Sonnet 5, always.</strong> Research, analysis, summarizing messy sources, drafting docs. It actually edges out Opus here, at a fraction of the cost. No reason to pay Opus rates.</li><li><strong>Everyday coding → Sonnet 5.</strong> It's strongest on brownfield code, the race conditions and hidden tests nobody wants to touch, tracing bugs to the root instead of patching symptoms.</li><li><strong>Hardest multi-step coding → watch the gap.</strong> Sonnet 5 scores ~63% on agentic coding where Opus hits ~69%. Invisible on daily work, real on the toughest changes.</li><li><strong>Deep reasoning + anything cyber → Opus.</strong> Anthropic deliberately held Sonnet 5's cyber capability down, so security-sensitive and proof-heavy work still belongs on Opus.</li></ul>
<p>Route by task type, not by a vague sense of "important," and you'll spend correctly almost every time.</p>
<h2>Two lifehacks the launch posts won't tell you</h2>
<p><strong>The high-effort trap.</strong> It's tempting to crank Sonnet 5 to its highest effort for max quality. Don't, without checking the math first.</p>
<p>At its maxed-out setting, Sonnet 5 can cost more to run than Opus 4.8 at a comparable level of reasoning. So "just set it to high" can quietly make you pay more than Opus, for slightly less quality.</p>
<p>The rule: if you're reaching for max effort on a truly hard task, that's your signal to check whether Opus at medium is both cheaper and better. High effort is for the middle band, not the ceiling.</p>
<p><strong>The 10-minute self-test.</strong> Don't trust benchmarks for your own work. Test it.</p>
<p>Take five real tasks you'd normally give Opus. Run each on Sonnet 5 at medium, then on Opus, and compare side by side:</p>
<pre><code class="language-markdown" data-lang="markdown">## My routing test
For each of 5 real tasks:
1. Run on Sonnet 5, medium effort. Save the result.
2. Run the same task on Opus 4.8.
3. Score both: did Sonnet 5 match? If yes, that task
   type routes to Sonnet 5 from now on.

After 5 tasks you'll know exactly which of your work
can drop to the cheaper model. Usually it's most of it.</code></pre>
<p>Ten minutes of testing tells you more about your real savings than any benchmark chart, because it's measured on the work you actually do.</p>
<h2>Common mistakes</h2>
<p><strong>Running everything at high effort.</strong> High effort is where Sonnet 5 rivals Opus, but also where it costs most. Reserve it for hard tasks, or you've just rebuilt an expensive model out of a cheap one.</p>
<p><strong>Defaulting to Opus out of habit.</strong> Sonnet 5 covers most work at near-Opus quality now. Sending everything to Opus "to be safe" is how bills stay high for no gain. Default down, escalate on evidence.</p>
<p><strong>Ignoring the intro window.</strong> The price rises 50% on September 1. Token-heavy work costs the same to run, so timing large jobs before the deadline is free savings you only get once.</p>
<p><strong>Treating effort and routing as manual choices.</strong> If you decide per task, you'll forget and overspend. Put both rules in CLAUDE.md so the cheap path is the default path.</p>
<h2>The 10-minute setup</h2>
<p>2 minutes: set claude-sonnet-5 and medium effort in settings.json.</p>
<p>3 minutes: add the effort policy to CLAUDE.md so hard tasks opt up and easy ones stay cheap.</p>
<p>3 minutes: add the routing rule so Opus is used only on evidence, not by default.</p>
<p>2 minutes: check your roadmap for big batch jobs and pull them into the intro window.</p>
<p>The model didn't just get cheaper. You built a setup that spends like the cheap model and performs like the expensive one, which is the whole point of Sonnet 5.</p>
<p>Thanks for reading!</p>
<p>I share daily notes on AI, finance, and vibe coding in my Telegram channel: <strong><a href="https://t.me/zodchixquant">https://t.me/zodchixquant</a></strong></p>
<figure><img src="https://pbs.twimg.com/media/HMIUB5TWwAAW7rR.jpg" alt=""></figure></article>
