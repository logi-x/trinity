<article class="x-article"><img src="https://pbs.twimg.com/media/HLb2P3ta4AAwPri.jpg" alt="Cover image">
<p>Half your feed is suddenly saying the same thing. Stop prompting your agents, start engineering loops.</p>
<p>Boris Cherny, the person who built Claude Code, said it plainly: "I don't prompt Claude anymore. I have loops that are running. My job is to write loops."</p>
<p>The person who builds one of the most popular coding agents on earth doesn't prompt it. So what is he doing instead?</p>
<p>That's the whole idea behind loop engineering. Now let's break down why it's harder than it looks.</p>
<p>First, the loop itself</p>
<p>An agent isn't a magic box. At its core, it's a plain loop:</p>
<pre><code class="language-python" data-lang="python">while True:
    response = model(context)
    if response.has_tool_calls():
        results = run_tools(response.tool_calls)
        context += results
    else:
        break
</code></pre>
<p>The model reads the context. It asks to call a tool. You run the tool and feed the result back. The model reads again, and this repeats until it stops asking for tools.</p>
<p><strong>Model → tools → context → repeat.</strong></p>
<p>Here's the part that surprises people. <strong>This loop is already solved.</strong> Every serious agent framework lands on roughly these six lines. Nobody is competing on the while statement.</p>
<p>So if the loop is trivial, what is everyone actually engineering?</p>
<p>The work moved outside the model</p>
<p>The center of gravity in AI keeps drifting away from the model itself.</p>
<ul><li><strong>Prompt engineering.</strong> The words you send.</li><li><strong>Context engineering.</strong> Everything the model sees, not just your instructions.</li><li><strong>Harness engineering.</strong> The code around the model that runs tools, tracks state, and handles errors.</li><li><strong>Loop engineering.</strong> The autonomous cycle that drives the whole thing toward a goal.</li></ul>
<p>Each layer wraps the one before it. You didn't stop caring about prompts. You just realized the prompt is one small piece of a much bigger system.</p>
<p>LangChain puts it cleanly. <strong>Agent = Model + Harness. If you're not the model, you're the harness.</strong></p>
<p>And here's the finding that should reorder your priorities. <strong>The harness now matters more than the model.</strong> Teams have kept the model fixed, changed only the code around it, and jumped from the middle of a benchmark into the top five. Same brain, different loop.</p>
<p>Loop engineering is the discipline of building everything that brain runs inside. Let me show you the parts that actually break.</p>
<p>Hard part 1: knowing when to stop</p>
<p>This is the problem nobody warns you about.</p>
<p>When an agent stops asking for tools, it has ended its turn. That is not the same as finishing the job.</p>
<p>Picture a coding agent. It writes some code, glances around, sees that progress was made, and announces it's done. The tests still fail. It declared victory anyway.</p>
<p><strong>A terminal message ends the turn, not the task.</strong> Confusing those two is the most common way loops go wrong.</p>
<p>Good loops stop for the right reasons, so you layer several brakes:</p>
<ul><li><strong>Max iterations.</strong> A hard cap so a stuck agent can't run forever.</li><li><strong>Budget and time limits.</strong> A ceiling on tokens, money, and seconds.</li><li><strong>No-progress detection.</strong> If it repeats the same call with the same arguments, it's spinning.</li><li><strong>A real completion check.</strong> An automated condition proving the job is done.</li></ul>
<p>That last one carries the weight. "Done" should mean the tests pass, not the agent feeling good about its work.</p>
<p>Hard part 2: keeping the context clean</p>
<p>Long loops rot from the inside.</p>
<p>The more turns an agent takes, the more junk piles into its context, like old tool outputs, dead ends, and stale reasoning. Model performance drops as that pile grows. The field calls it <strong>context rot.</strong></p>
<p>A loop makes it spiral. A rotted context produces a worse decision, which adds more noise, which rots the context further. People call this the doom loop, and you've felt it. The agent gets dumber the longer it runs.</p>
<p>You fight it by treating context as a budget, not a bucket:</p>
<ul><li><strong>Compaction.</strong> Summarize the conversation when it gets long, then continue from the summary.</li><li><strong>Offloading.</strong> Push huge outputs to a file and keep only the slice you need.</li><li><strong>Sub-agents.</strong> Hand a messy subtask to a separate agent and let only its clean result return.</li></ul>
<p>The instinct is to keep everything, just in case. The skill is knowing what to throw away.</p>
<p>Hard part 3: tools the agent can actually use</p>
<p>A loop is only as good as the tools inside it.</p>
<p>Pile on a hundred tools and the agent loses track of which one to reach for. A tight set of focused, non-overlapping tools wins. Anthropic's rule of thumb is sharp. If a human engineer can't say for certain which tool fits, the agent has no chance.</p>
<p>Two things matter more than people expect:</p>
<ul><li><strong>Make writes safe to repeat.</strong> Loops retry, and if a retried "create customer" call makes a second customer, you'll wake up to duplicate records and double billing. Anything that changes state has to be safe to call twice.</li><li><strong>Write error messages for the agent, not the human.</strong> A good error tells the agent what to do next. Before a tool ships, ask whether an LLM reading its error would know the next move.</li></ul>
<p>In a loop, an error isn't a dead end. It's the next instruction.</p>
<p>Hard part 4: something that can say no</p>
<p>Autonomous loops have a quiet failure mode. An agent left alone tends to agree with itself.</p>
<p>The sharpest comment in the whole debate nailed it. Designing the loop is half the job, and the other half is putting something in the loop that can say no, like a test, a type check, or a real error.</p>
<p><strong>A loop with no critic is just an agent nodding along to its own work.</strong></p>
<p>The fix is to separate the maker from the checker. One model does the work. A different check, often a separate model or a hard test, grades it. The worker doesn't grade its own homework.</p>
<p>The actual shift</p>
<p>Now Cherny's quote makes sense.</p>
<p>Prompting is you steering the agent move by move. Loop engineering is you building the system that steers it, then stepping back.</p>
<p>Your job changes from giving instructions to designing three things:</p>
<p><strong>The goal,</strong> written as success criteria the agent can check itself against.</p>
<p><strong>The loop,</strong> with sane brakes so it stops well.</p>
<p><strong>The verifier,</strong> so "done" is proven, not claimed.</p>
<p>Andrej Karpathy captures the mindset. Don't tell the model what to do, give it success criteria and watch it go. He runs research loops overnight that tweak a script, test it, keep what works, and discard what doesn't, with himself nowhere in the loop. He arranges it once and hits go.</p>
<p>That's the whole move. You stop being the hands and become the person who designs the machine.</p>
<p>Where to start</p>
<p>You don't need an overnight autonomous agent on day one. Build up to it:</p>
<p><strong>Start with the basic loop,</strong> and add a max-iteration cap, a timeout, and a cost ceiling right away.</p>
<p><strong>Define "done" as an automated check</strong> before you begin, not a vibe afterward.</p>
<p><strong>Protect the context.</strong> Compact long runs, offload big outputs, isolate messy subtasks.</p>
<p><strong>Audit your tools.</strong> Keep them few and focused, make writes safe to repeat, and rewrite errors so an agent can act on them.</p>
<p><strong>Put a critic in the loop.</strong> Only go fully hands-off once you trust the thing that says no.</p>
<p>The takeaway</p>
<p>Loop engineering isn't a framework or a tool you install. It's a shift in where you aim your effort.</p>
<p>The model is becoming a commodity. The loop around it is where the real engineering lives now.</p>
<p>The best builders stopped asking "what should I tell the agent to do?" They started asking "what system would do this without me?"</p>
<p>Answer that one well, and you'll stop prompting too.</p>
<p>Here's a summary of</p>
<figure><img src="https://pbs.twimg.com/media/HLb7qMjacAAddIh.jpg" alt="Key takeaways in loop engineering."><figcaption>Key takeaways in loop engineering.</figcaption></figure>
<p>Thanks for reading!</p>
<p>Cheers :)
Akshay.</p></article>
