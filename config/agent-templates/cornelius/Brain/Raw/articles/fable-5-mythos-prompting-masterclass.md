<article class="x-article"><img src="https://pbs.twimg.com/media/HKeVA4na0AA6Uog.jpg" alt="Cover image">
<p><strong>TLDR: </strong>Anthropic just published the official playbook for prompting the most powerful AI model on earth - I translated it.</p>
<p>Most people won't read this guide (it's buried in the API docs), which is written for developers, and the average Claude user will bounce off it in 30 seconds due to its density. </p>
<p>This article is the plain English version.</p>
<p>Claude Fable 5, also known as Mythos, is a fundamentally different model from everything Anthropic has shipped before. The way you think about prompting structure needs to completely change.</p>
<p>Here's everything that you need to know.</p>
<p><strong>Table of Contents</strong></p>
<p><strong>I: What Makes Fable 5 (Mythos) Different </strong></p>
<p><strong>II: How to Prompt Fable Properly </strong></p>
<p><strong>III: Optimal Prompting Structure for Fable 5 (+/loops)</strong></p>
<p><strong>IV: What to Watch Out For (caveats)</strong></p>
<p>For reference, this is the playbook I've translated. Feel free to review it in-depth and verify my analysis:</p>
<figure><img src="https://pbs.twimg.com/media/HKeWuJaa4AAslGM.jpg" alt="Prompting Fable 5 by Anthropic (playbook)"><figcaption>Prompting Fable 5 by Anthropic (playbook)</figcaption></figure>
<p><strong><a href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5">https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5</a></strong></p>
<h2>What Makes Fable 5 (Mythos) Different </h2>
<p>A brief overview of the fundamental changes in Fable 5 (Mythos) - important context</p>
<p><strong>Run Time</strong></p>
<p>Every Claude model before Fable 5 worked in relatively short bursts.</p>
<p>Claude Fable 5 is meant to sustain output over extended periods to complete multi-day, goal-directed tasks.</p>
<p>This is one of the biggest shifts. Fable 5 is meant for fully autonomous work (paired with /goal or /loop). </p>
<p><strong>2.     It Gets Things Right First Time</strong></p>
<p>One of the most reported early observations from people using Fable 5 is how rarely they need to iterate. Early testers reported single-pass implementations of systems that previously took days of iteration.</p>
<p><strong>3.     Clarifying Questions</strong></p>
<p>To execute autonomous work loops accurately, Fable 5 may ask a series of clarifying questions before it kicks off its autonomous run. </p>
<p><strong>4.     Agent Management </strong></p>
<p>Fable 5 is built to manage multiple parallel subagents at once (spinning up 50+ agents for complex tasks).</p>
<p><strong>5.     It "Sees" Better</strong></p>
<p>Claude Fable 5 interprets dense technical images, web applications, and detailed screenshots with substantially higher accuracy.</p>
<p>For anyone using Claude to analyse charts, screenshots, documents, or visual data, the improvement here is meaningful.</p>
<p>6.     <strong>Coding + Security Audits </strong></p>
<p>It's no secret that Fable is a coding genius. This new model is especially powerful for codebase review and debugging. </p>
<figure><img src="https://pbs.twimg.com/media/HKeYp4QakAAY6lv.jpg" alt="Fable 5 improvements and fundamental changes "><figcaption>Fable 5 improvements and fundamental changes </figcaption></figure>
<p><strong>TLDR: </strong>You need to think of Fable as a collaboration/consultant partner that leads your work. It is meant to be a genius. </p>
<h2>II: How to Prompt Fable Properly</h2>
<p><strong>Match Your Effort Level to the Task</strong></p>
<p>Effort is the primary control for the trade-off between intelligence, latency, and cost on Claude Fable 5. </p>
<p>It is recommended to use <strong>high</strong> as the default for most tasks, with xhigh for the most capability-sensitive work.</p>
<p>Think of it like hiring a consultant. You don't need them running at full capacity to answer a simple question. </p>
<p>The practical guide:</p>
<ul><li><strong>Low or medium:</strong> Quick questions, simple rewrites, basic research, anything conversational</li><li><strong>High:</strong> Default</li><li><strong>Xhigh:</strong> Your hardest problems. Complex builds, multi-step analysis, anything where quality is non-negotiable</li><li><strong>Ultracode:</strong> Full autonomous orchestration with Dynamic Workflows (more on this later)</li></ul>
<p>2.     <strong>Tell It Why, Not Just What</strong></p>
<p>Fable 5 cannot perform solely on instructions, unlike other models. It needs the "why" behind things, which is why it asks many clarifying questions. </p>
<p>Context lets it connect the task to relevant information rather than inferring intent on its own. </p>
<p>The formula Anthropic recommends:</p>
<p><strong>PROMPT STRUCTURE</strong></p>
<p>"I'm working on [the larger task] for [who it's for]. They need [what the output enables]. With that in mind: [your actual request]."</p>
<p>3.     <strong>Keep Instructions Short</strong></p>
<p>This feels counterintuitive, but it's one of the most important adjustments to make when moving to Fable 5. </p>
<p>A short brevity instruction is as effective as listing each pattern. Over-engineering your prompts on Fable 5 can actually degrade output quality because you're constraining a model that would have figured out the right approach on its own. </p>
<p>4.     <strong>Tell It When to Stop and Check In</strong></p>
<p>Fable 5 is built to run autonomously. Which means if you don't define the checkpoints, it will define them itself. Sometimes that's fine. For important or sensitive work, you want to set the boundaries explicitly.</p>
<p>Use this instruction when you want Fable 5 to run autonomously but stop at the right moments:</p>
<p><strong>CHECKPOINT PROMPT</strong></p>
<p>"Pause for me only when the work genuinely requires my input: a destructive or irreversible action, a real scope change, or something only I can provide. Otherwise, keep going and report back when done."</p>
<p>5.     <strong>Build It a Memory System</strong></p>
<p>Claude Fable 5 performs particularly well when it can record lessons from previous runs and reference them. Provide a place to write notes, as simple as a markdown file. </p>
<p>The instruction Anthropic recommends for your memory file:</p>
<p><strong>MEMORY INSTRUCTION</strong></p>
<p>"Store one lesson per file with a one-line summary at the top. Record corrections and confirmed approaches alike, including why they mattered. Don't save what the repo or chat history already records. Update an existing note rather than creating a duplicate. Delete notes that turn out to be wrong."</p>
<h2>Optimal Prompting Structure for Fable 5 (+/loops)</h2>
<p>The exact framework you should use for most prompts (combining all the tips above)</p>
<p><strong>General Structure</strong></p>
<p>Every high-quality Fable 5 prompt has four components:</p>
<p><strong>1. Context: </strong>Files, data, and so on.</p>
<p><strong>2. Request: </strong>What you actually want done. </p>
<p><strong>3. Output format: </strong>Exactly how you want the result delivered.</p>
<p><strong>4. Constraints: </strong>What Fable 5 must not assume on its own</p>
<p><strong>Put together</strong>,<strong> it looks like this:</strong></p>
<pre><code>OPTIMAL PROMPT STRUCTURE
"I'm working on [the larger task] for [who it's for]. 
They need [what the output enables].
Request: [your specific ask in one clear sentence]
Output format: [exactly how you want the result 
structured and delivered]
Constraints: [what must not happen on 
the way to the result]"</code></pre>
<p><strong>/loops </strong></p>
<p>/loop is one of the most powerful ways to use this new model.</p>
<p>If you're unfamiliar, setting a /loop just allows your AI to work without manual intervention.</p>
<p>You should structure your /loop prompts like this:</p>
<pre><code>/loop &lt;time interval&gt; + goal
</code></pre>
<p><strong>Example</strong>: /loop 15 minutes, check if my build is passing, and notify me if it fails.</p>
<p>To stop a loop:</p>
<p>/loop stop [loop name]</p>
<h2>What to Watch Out For</h2>
<p>Some things to keep in mind when using Fable 5</p>
<ul><li><strong>It Runs Longer Than You Expect</strong></li></ul>
<p>This is one of the largest shifts teams encounter when adjusting to Claude Fable 5. Individual requests for hard tasks can run for many minutes at higher-effort settings. </p>
<ul><li><strong>It Can Go Beyond What You Asked For</strong></li></ul>
<p>Fable 5 is proactive by design. Claude Fable 5 can occasionally take unrequested actions. Use check-ins/loops to combat this.</p>
<ul><li><strong>Your Old Prompts May Work Against You</strong></li></ul>
<p>If you have saved skills or project instructions built for other models like Claude Opus 4.8 or earlier, they may actually produce worse results on Fable 5 than a simple fresh prompt would. Start fresh.</p>
<ul><li><strong>Decline Cybersecurity and Life Sciences Requests (and more)</strong></li></ul>
<p>Fable may hallucinate, and decline prompts you think are "safe." </p>
<ul><li><strong>It Can Occasionally Stop Early</strong></li></ul>
<p>If this happens, a simple "go ahead and do it end-to-end" is enough to get it moving again.</p>
<ul><li><strong>Token Costs Are Higher</strong></li></ul>
<p>And of course, this is an insanely expensive model. Available on paid plans until June 22; after that, all access will be via API costs. </p>
<h2>Closing </h2>
<p>If you found this useful, be sure to follow me <a href="https://x.com/aiedge_">@aiedge_</a>.</p>
<p>I post AI articles like this 2-3x/week, breaking down the hottest AI topics.</p>
<p>If you enjoy written AI content, feel free to subscribe to my free AI newsletter, where I focus on teaching you AI workflows.</p>
<p><strong><a href="https://www.aiedgehq.co/">https://www.aiedgehq.co/</a></strong></p>
<figure><img src="https://pbs.twimg.com/media/HKefk8laIAApsL6.jpg" alt="https://www.aiedgehq.co/"><figcaption>https://www.aiedgehq.co/</figcaption></figure>
<p>No spam ever, 100% &amp; unsub anytime</p>
<p>Lastly, if this helped you, please Like and Repost so others can find it. 💙</p></article>
