Yes — there is a better way.

Do **not** hardcode rules like:

```text
Noura cannot make decisions
```

That will get messy.

Instead, model agents by **capabilities + authority + provenance**.

## Better model

Each agent has:

```text
role
capabilities
authority_scope
can_decide
can_approve
can_store_memory
```

Example:

```json
{
  "id": "noura",
  "role": "chief_of_staff",
  "capabilities": ["dispatch", "coordinate", "summarize"],
  "authority_scope": ["operations_coordination"],
  "can_decide": false
}
```

CTO:

```json
{
  "id": "omar",
  "role": "cto",
  "capabilities": ["architecture_review", "technical_decision"],
  "authority_scope": ["engineering", "infrastructure", "security"],
  "can_decide": true
}
```

Then the system asks:

```text
Can this agent make this type of decision?
```

Not:

```text
Is this agent Noura?
```

---

## Add `decision_scope`

For every decision/memory:

```sql
decision_scope TEXT
decision_owner_agent_id TEXT
approved_by_agent_id TEXT
source_message_id UUID
source_episode_id UUID
```

Example:

```text
decision_scope = "pricing"
decision_owner_agent_id = "cfo"
approved_by_agent_id = "synthesizer"
```

or:

```text
decision_scope = "architecture"
decision_owner_agent_id = "cto"
```

---

## For attribution questions

When user asks:

```text
What was Noura's decision?
```

The system should not run normal RAG first.

It should run a **provenance query**:

```sql
SELECT *
FROM memories
WHERE decision_owner_agent_id = 'noura'
AND type = 'decision';
```

If none:

```text
No decision by Noura was found.
Related decision: ...
Actual owner: Product / CTO / CFO / Synthesizer.
```

---

## The scalable rule

Every memory should answer:

```text
Who said it?
Who decided it?
Who approved it?
What episode did it come from?
What message did it come from?
What scope does it belong to?
```

That scales to 5 agents or 500 agents.

---

## Mental model

Agents are not special-cased people.

They are actors with permissions.

```text
Agent
  ↓
Capability
  ↓
Authority Scope
  ↓
Message
  ↓
Memory
  ↓
Provenance
```

That’s the cleaner system.

Your current flaw is not “Noura can’t decide.”

The flaw is:

```text
memory has content, but no authority metadata
```

Fix that, and adding agents becomes clean.
