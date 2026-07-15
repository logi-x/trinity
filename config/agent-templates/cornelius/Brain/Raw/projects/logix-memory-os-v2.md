---
title: "logix-memory-os-v2 — Project documentation"
date: "2026-06-14"
tags: ["project/logix", "topic/memory-os", "topic/logix-memory-os-v2"]
category: "projects/logix"
---

If I were starting today specifically for **Logix AI Workforce**, I would build it like this:

```text
Python (AI Brain)
        +
Postgres + pgvector (Memory)
        +
LM Studio (Models)
        +
Next.js (Dashboard later)
```

Not LangChain.
Not CrewAI.
Not AutoGen.

At least not initially.

Those frameworks tend to add abstraction before you've proven the memory architecture.

---

# Phase 0 — Architecture

```text
┌─────────────────────────┐
│       User Request      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│       Dispatcher        │
└────────────┬────────────┘
             │
     ┌───────┼────────┐
     ▼       ▼        ▼
   CTO      CFO    Product
             │
             ▼
┌─────────────────────────┐
│      Synthesizer        │
└────────────┬────────────┘
             ▼
      Final Decision
             │
             ▼
┌─────────────────────────┐
│ Postgres Memory Store   │
└─────────────────────────┘
```

---

# Phase 1 — Project Structure

```text
logix-memory-os/

├── docker/
│   └── docker-compose.yml
│
├── runtime/
│   ├── agents/
│   ├── memory/
│   ├── llm/
│   ├── tools/
│   ├── episodes/
│   ├── dispatcher/
│   └── api/
│
├── migrations/
│
├── scripts/
│
├── tests/
│
├── pyproject.toml
├── .env
└── README.md
```

---

# Phase 2 — Install Python

I recommend:

```bash
sudo apt install python3.12 python3-pip
```

Then:

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

# Phase 3 — Dependencies

Create:

```bash
pip install \
  fastapi \
  uvicorn \
  pydantic \
  sqlalchemy \
  psycopg[binary] \
  pgvector \
  openai \
  numpy \
  tiktoken \
  python-dotenv \
  alembic
```

Then:

```bash
pip freeze > requirements.txt
```

---

# Phase 4 — PostgreSQL + pgvector

Docker:

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg16

    environment:
      POSTGRES_USER: logix
      POSTGRES_PASSWORD: logix
      POSTGRES_DB: memory

    ports:
      - "5439:5432"

    volumes:
      - postgres:/var/lib/postgresql/data

volumes:
  postgres:
```

Start:

```bash
docker compose up -d
```

Enable vector:

```sql
CREATE EXTENSION vector;
```

---

# Phase 5 — Environment

```env
DATABASE_URL=postgresql://logix:logix@localhost:5439/memory

OPENAI_BASE_URL=http://localhost:1234/v1
OPENAI_API_KEY=lm-studio

CHAT_MODEL=qwen2.5-3b-instruct
EMBED_MODEL=nomic-embed-text-v1.5
```

---

# Phase 6 — Database Schema

Forget notes.

Store knowledge.

## Agents

```sql
CREATE TABLE agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    title TEXT NOT NULL,
    department TEXT NOT NULL,
    instructions TEXT NOT NULL,
    personality TEXT NOT NULL
);
```

---

## Episodes

Episodes are meetings.

```sql
CREATE TABLE episodes (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,

    user_request TEXT NOT NULL,

    final_decision TEXT,

    outcome TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Messages

Agent communication.

```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY,

    episode_id UUID NOT NULL,

    from_agent TEXT NOT NULL,

    type TEXT NOT NULL,

    topic TEXT NOT NULL,

    content TEXT NOT NULL,

    confidence FLOAT NOT NULL,

    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Memory

Most important table.

```sql
CREATE TABLE memories (
    id UUID PRIMARY KEY,

    type TEXT NOT NULL,

    title TEXT NOT NULL,

    content TEXT NOT NULL,

    summary TEXT,

    tags TEXT[],

    embedding VECTOR(768),

    created_at TIMESTAMP DEFAULT NOW()
);
```

---

# Phase 7 — LLM Client

`runtime/llm/client.py`

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)
```

Test:

```python
response = client.chat.completions.create(
    model="qwen2.5-3b-instruct",
    messages=[
        {
            "role": "user",
            "content": "hello"
        }
    ]
)
```

---

# Phase 8 — Embeddings

`runtime/memory/embed.py`

```python
from runtime.llm.client import client

def embed(text: str):

    result = client.embeddings.create(
        model="nomic-embed-text-v1.5",
        input=text
    )

    return result.data[0].embedding
```

---

# Phase 9 — Memory Insert

```python
memory = {
    "type": "decision",

    "title": "FX Strategy",

    "content": """
Display EUR.
Settle SAR.
Use cached rates.
"""
}
```

Generate embedding.

Store.

Done.

---

# Phase 10 — Retrieval

Before every agent runs:

```python
query = embed(user_request)
```

Then:

```sql
ORDER BY embedding <=> query
LIMIT 10
```

Return:

```text
Decision:
Display EUR.

Incident:
Runner 05 instability.

Playbook:
Staging deployment.
```

---

# Phase 11 — Agent Runtime

Each agent:

```python
class Agent:

    id: str

    title: str

    personality: str

    instructions: str
```

Example:

```python
CTO
```

```text
Avoid complexity.
Prefer reliability.
Question scalability claims.
```

---

# Phase 12 — Dispatcher

Dispatcher decides:

```text
Need CTO?
Need CFO?
Need Product?
Need DevOps?
```

Example:

```text
Question:
Should Experts support EUR?

Selected:
CTO
CFO
Product
```

---

# Phase 13 — Agent Protocol

Every response:

```python
class AgentMessage(BaseModel):

    type: str

    topic: str

    content: str

    confidence: float

    references: list[str]
```

Exactly like the architecture we discussed previously.

---

# Phase 14 — Synthesizer

Reads:

```text
CTO Opinion

CFO Opinion

Product Opinion
```

Produces:

```json
{
  "decision": "...",
  "risks": [],
  "next_actions": []
}
```

Then stores:

```text
Decision Memory
```

back into Postgres.

---

# Phase 15 — FastAPI

Create:

```python
app = FastAPI()
```

Endpoint:

```python
POST /episodes
```

Request:

```json
{
  "input": "Should Experts support EUR?"
}
```

Response:

```json
{
  "episode_id": "...",
  "decision": "...",
  "agents": [
    "cto",
    "cfo",
    "product"
  ]
}
```

---

# Phase 16 — Tools

After memory works.

Add tools.

```python
read_file
```

```python
search_repo
```

```python
git_status
```

```python
docker_ps
```

```python
postgres_query
```

```python
read_logs
```

Agents call tools.

Never shell directly.

Exactly the "Agent → MCP → Tool" pattern from the earlier design.

---

# Phase 17 — Memory Sources

The first memories I would import are:

```text
Experts Architecture
```

```text
FX Decisions
```

```text
Git Workflow
```

```text
ZATCA Architecture
```

```text
Deployment Playbooks
```

```text
Postmortems
```

Do not import:

```text
Daily Notes
```

yet.

---

# Phase 18 — Obsidian Integration Later

Eventually:

```text
Obsidian
    ↓
Markdown Importer
    ↓
Document Store
    ↓
Knowledge Extractor
    ↓
Memory Store
```

Notice:

```text
Obsidian
```

is no longer the memory.

It's merely a source.

---

# Phase 19 — Model Strategy

For your current infrastructure:

```text
VPS
2 vCPU
4 GB RAM
```

Do NOT run the model there.

Run:

```text
LM Studio
```

on your workstation.

Then:

```text
Python Runtime (VPS)
      ↓
LM Studio API
```

This gives you:

```text
Cheap VPS
Powerful model
Central memory
```

without needing GPU resources on the server.

---

# Phase 20 — What I'd Actually Build This Week

Week 1:

```text
Postgres
pgvector
FastAPI
Memory table
Insert memory
Retrieve memory
```

Week 2:

```text
Dispatcher
CTO
CFO
Product
Synthesizer
Episode storage
```

Week 3:

```text
Git tools
Repository search
Log tools
```

Week 4:

```text
Next.js dashboard
Memory browser
Episode viewer
```

Only after all of that would I even think about:

```text
CrewAI
AutoGen
LangGraph
Fine-tuning
MCP servers
```

because by then you'll already have the hard part solved:

> A persistent organizational memory system that remembers decisions, retrieves them before reasoning, and continuously improves itself through new episodes.
