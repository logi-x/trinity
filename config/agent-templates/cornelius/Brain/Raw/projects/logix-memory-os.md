---
title: "logix-memory-os — Project documentation"
date: "2026-06-14"
tags: ["project/logix", "topic/memory-os", "topic/logix-memory-os"]
category: "projects/logix"
---

Yes. For your case, I’d build it as a **small internal AI Memory OS**, not a note-taking app.

The architecture should follow what we discussed earlier: structured agent messages, memory retrieval before response, event logging, and a synthesizer that produces final decisions rather than random agent chatter. Your uploaded AI workforce plan already points in that direction: dispatcher → selected agents → structured messages → event log → synthesizer → final decision. 

Below is the full from-scratch guide.

---

# 0. Target Architecture

```text
logix-memory-os/
│
├── Postgres + pgvector
│   ├── agents
│   ├── memories
│   ├── episodes
│   ├── agent_messages
│   ├── tool_calls
│   └── documents
│
├── Node.js Agent Runtime
│   ├── dispatcher
│   ├── memory retriever
│   ├── agents
│   ├── synthesizer
│   └── tools
│
├── Local/Remote Model
│   ├── LM Studio
│   ├── Ollama
│   └── OpenAI-compatible API
│
└── Optional UI
    ├── Next.js dashboard
    └── memory browser
```

Core principle:

```text
Notes are not memory.
Decisions, lessons, incidents, playbooks, and outcomes are memory.
```

---

# 1. Stack Recommendation

Use:

```text
Backend: Node.js + TypeScript
DB: PostgreSQL
Vector: pgvector
ORM: Prisma
Runtime: tsx
Model API: OpenAI-compatible endpoint
Embeddings: local or OpenAI-compatible embedding model
Optional UI: Next.js later
```

For now, do **not** start with Next.js UI.

Start with a CLI/API runtime.

---

# 2. Create Project

```bash
mkdir logix-memory-os
cd logix-memory-os

pnpm init
pnpm add typescript tsx dotenv zod openai pg @prisma/client
pnpm add -D prisma @types/node
pnpm exec tsc --init
```

Create structure:

```bash
mkdir -p src/{agents,db,memory,runtime,llm,tools,ingest,scripts}
touch .env
```

---

# 3. Docker Postgres + pgvector

Create `docker-compose.yml`:

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg16
    container_name: logix-memory-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: logix
      POSTGRES_PASSWORD: logix
      POSTGRES_DB: logix_memory
    ports:
      - "5439:5432"
    volumes:
      - logix_memory_pg:/var/lib/postgresql/data

volumes:
  logix_memory_pg:
```

Run:

```bash
docker compose up -d
```

`.env`:

```env
DATABASE_URL="postgresql://logix:logix@localhost:5439/logix_memory"

OPENAI_BASE_URL="http://localhost:1234/v1"
OPENAI_API_KEY="lm-studio"

CHAT_MODEL="qwen2.5-3b-instruct"
EMBEDDING_MODEL="text-embedding-nomic-embed-text-v1.5"
```

If LM Studio is on Windows and runtime is in WSL:

```env
OPENAI_BASE_URL="http://172.x.x.x:1234/v1"
```

---

# 4. Prisma Schema

```bash
pnpm exec prisma init
```

Replace `prisma/schema.prisma`:

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

enum MemoryType {
  decision
  architecture
  incident
  playbook
  client
  project
  lesson
  note
}

enum EpisodeType {
  board_meeting
  architecture_review
  pricing_decision
  incident_review
  planning
  general
}

enum MessageType {
  opinion
  decision
  question
  critique
  proposal
  summary
}

enum Priority {
  low
  medium
  high
  critical
}

model Agent {
  id           String   @id
  name         String
  title        String
  department   String
  personality  String
  instructions String
  createdAt    DateTime @default(now())
  updatedAt    DateTime @updatedAt

  messages     AgentMessage[]
}

model Memory {
  id          String     @id @default(cuid())
  type        MemoryType
  title       String
  content     String
  summary     String?
  source      String?
  project     String?
  client      String?
  tags        String[]
  confidence  Float      @default(0.8)
  status      String     @default("active")
  createdAt   DateTime   @default(now())
  updatedAt   DateTime   @updatedAt

  embedding   Unsupported("vector(768)")?

  episodeId   String?
  episode     Episode?   @relation(fields: [episodeId], references: [id])

  @@index([type])
  @@index([project])
  @@index([client])
}

model Episode {
  id            String      @id @default(cuid())
  type          EpisodeType
  title         String
  userRequest   String
  finalDecision String?
  outcome       String?
  participants  String[]
  createdAt     DateTime    @default(now())

  memories      Memory[]
  messages      AgentMessage[]
}

model AgentMessage {
  id          String      @id @default(cuid())
  episodeId   String
  fromAgentId String
  toAgentId   String?
  type        MessageType
  topic       String
  content     String
  confidence  Float
  priority    Priority
  references  String[]
  createdAt   DateTime    @default(now())

  episode     Episode     @relation(fields: [episodeId], references: [id])
  fromAgent   Agent       @relation(fields: [fromAgentId], references: [id])

  @@index([episodeId])
  @@index([fromAgentId])
}

model Document {
  id        String   @id @default(cuid())
  title     String
  path      String?
  content   String
  source    String?
  checksum  String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  embedding Unsupported("vector(768)")?
}

model ToolCall {
  id        String   @id @default(cuid())
  episodeId String?
  toolName  String
  input     Json
  output    Json?
  status    String
  error     String?
  createdAt DateTime @default(now())
}
```

Now create migration:

```bash
pnpm exec prisma migrate dev --name init
```

Enable vector extension manually:

```bash
docker exec -it logix-memory-postgres psql -U logix -d logix_memory
```

Then:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

---

# 5. Add Vector Indexes

Create `prisma/migrations/manual_vector_indexes.sql` or run manually:

```sql
CREATE INDEX IF NOT EXISTS memory_embedding_idx
ON "Memory"
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX IF NOT EXISTS document_embedding_idx
ON "Document"
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

---

# 6. Prisma Client

Create `src/db/prisma.ts`:

```ts
import { PrismaClient } from "@prisma/client";

export const prisma = new PrismaClient();
```

---

# 7. LLM Client

Create `src/llm/client.ts`:

```ts
import OpenAI from "openai";

export const llm = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || "lm-studio",
  baseURL: process.env.OPENAI_BASE_URL || "http://localhost:1234/v1",
});

export const CHAT_MODEL = process.env.CHAT_MODEL || "qwen2.5-3b-instruct";
export const EMBEDDING_MODEL =
  process.env.EMBEDDING_MODEL || "text-embedding-nomic-embed-text-v1.5";
```

---

# 8. Embeddings

Create `src/memory/embed.ts`:

```ts
import { llm, EMBEDDING_MODEL } from "../llm/client";

export async function embedText(text: string): Promise<number[]> {
  const result = await llm.embeddings.create({
    model: EMBEDDING_MODEL,
    input: text.slice(0, 8000),
  });

  return result.data[0].embedding;
}

export function vectorSql(vector: number[]): string {
  return `[${vector.join(",")}]`;
}
```

Important: your embedding dimension must match `vector(768)`. If your embedding model returns 384, 1024, or 1536 dimensions, change the Prisma schema.

---

# 9. Memory Insert

Create `src/memory/create-memory.ts`:

```ts
import { prisma } from "../db/prisma";
import { embedText, vectorSql } from "./embed";
import { MemoryType } from "@prisma/client";

type CreateMemoryInput = {
  type: MemoryType;
  title: string;
  content: string;
  summary?: string;
  project?: string;
  client?: string;
  tags?: string[];
  source?: string;
  confidence?: number;
};

export async function createMemory(input: CreateMemoryInput) {
  const embedding = await embedText(
    `${input.title}\n\n${input.summary ?? ""}\n\n${input.content}`
  );

  const memory = await prisma.memory.create({
    data: {
      type: input.type,
      title: input.title,
      content: input.content,
      summary: input.summary,
      project: input.project,
      client: input.client,
      tags: input.tags ?? [],
      source: input.source,
      confidence: input.confidence ?? 0.8,
    },
  });

  await prisma.$executeRawUnsafe(
    `UPDATE "Memory" SET embedding = $1::vector WHERE id = $2`,
    vectorSql(embedding),
    memory.id
  );

  return memory;
}
```

---

# 10. Memory Retrieval

Create `src/memory/retrieve.ts`:

```ts
import { prisma } from "../db/prisma";
import { embedText, vectorSql } from "./embed";

export async function retrieveMemories(query: string, limit = 8) {
  const embedding = await embedText(query);

  const rows = await prisma.$queryRawUnsafe<any[]>(
    `
    SELECT
      id,
      type,
      title,
      summary,
      content,
      project,
      client,
      tags,
      confidence,
      1 - (embedding <=> $1::vector) AS similarity
    FROM "Memory"
    WHERE embedding IS NOT NULL
      AND status = 'active'
    ORDER BY embedding <=> $1::vector
    LIMIT $2
    `,
    vectorSql(embedding),
    limit
  );

  return rows;
}
```

---

# 11. Define Agents

Create `src/agents/seed-agents.ts`:

```ts
import { prisma } from "../db/prisma";

const agents = [
  {
    id: "dispatcher",
    name: "Noura",
    title: "Chief of Staff",
    department: "Operations",
    personality:
      "Clear, direct, organized, avoids unnecessary complexity.",
    instructions:
      "Route requests to the right agents. Prefer minimal agent selection. Always consider company memory.",
  },
  {
    id: "cto",
    name: "Omar",
    title: "Chief Technology Officer",
    department: "Engineering",
    personality:
      "Pragmatic, technical, skeptical of overengineering, prefers simple reliable systems.",
    instructions:
      "Evaluate architecture, infrastructure, code quality, scalability, security, and maintainability.",
  },
  {
    id: "cfo",
    name: "Salman",
    title: "Chief Financial Officer",
    department: "Finance",
    personality:
      "ROI-focused, cautious, cost-aware, asks whether the work is worth doing.",
    instructions:
      "Evaluate cost, pricing, revenue, margin, financial risk, and operational efficiency.",
  },
  {
    id: "product",
    name: "Lina",
    title: "Head of Product",
    department: "Product",
    personality:
      "User-focused, practical, prioritizes clarity and shipping.",
    instructions:
      "Evaluate product value, UX impact, user journeys, prioritization, and launch readiness.",
  },
  {
    id: "devops",
    name: "Faris",
    title: "DevOps Lead",
    department: "Infrastructure",
    personality:
      "Calm, operational, reliability-focused, thinks in failure modes.",
    instructions:
      "Evaluate deployment, CI/CD, monitoring, servers, containers, networking, and incident risk.",
  },
  {
    id: "synthesizer",
    name: "Maha",
    title: "Executive Synthesizer",
    department: "Leadership",
    personality:
      "Concise, decisive, balanced, turns debate into action.",
    instructions:
      "Read all agent messages and produce the final decision, tradeoffs, risks, and next actions.",
  },
];

async function main() {
  for (const agent of agents) {
    await prisma.agent.upsert({
      where: { id: agent.id },
      update: agent,
      create: agent,
    });
  }

  console.log("Seeded agents");
}

main().finally(() => prisma.$disconnect());
```

Run:

```bash
pnpm tsx src/agents/seed-agents.ts
```

---

# 12. Dispatcher

Create `src/runtime/dispatcher.ts`:

```ts
import { llm, CHAT_MODEL } from "../llm/client";
import { z } from "zod";

const DispatchSchema = z.object({
  agents: z.array(z.string()),
  reason: z.string(),
});

export async function dispatchAgents(userRequest: string): Promise<string[]> {
  const response = await llm.chat.completions.create({
    model: CHAT_MODEL,
    temperature: 0.1,
    messages: [
      {
        role: "system",
        content: `
You are the dispatcher for Logix Memory OS.

Available agents:
- cto: architecture, code, engineering decisions
- cfo: cost, pricing, revenue, ROI
- product: UX, features, roadmap, customer value
- devops: deployment, infrastructure, CI/CD, reliability

Select 1-3 agents only.
Return JSON only:
{
  "agents": ["cto"],
  "reason": "..."
}
`,
      },
      {
        role: "user",
        content: userRequest,
      },
    ],
  });

  const raw = response.choices[0].message.content ?? "{}";
  const parsed = DispatchSchema.safeParse(JSON.parse(raw));

  if (!parsed.success) return ["cto"];

  return parsed.data.agents.filter((id) =>
    ["cto", "cfo", "product", "devops"].includes(id)
  );
}
```

---

# 13. Agent Runner

Create `src/runtime/run-agent.ts`:

```ts
import { prisma } from "../db/prisma";
import { llm, CHAT_MODEL } from "../llm/client";
import { retrieveMemories } from "../memory/retrieve";
import { MessageType, Priority } from "@prisma/client";

export async function runAgent(params: {
  episodeId: string;
  agentId: string;
  userRequest: string;
}) {
  const agent = await prisma.agent.findUniqueOrThrow({
    where: { id: params.agentId },
  });

  const memories = await retrieveMemories(params.userRequest, 6);

  const memoryContext = memories
    .map(
      (m, i) => `
[Memory ${i + 1}]
id: ${m.id}
type: ${m.type}
title: ${m.title}
summary: ${m.summary ?? ""}
content: ${m.content.slice(0, 1000)}
similarity: ${m.similarity}
`
    )
    .join("\n");

  const response = await llm.chat.completions.create({
    model: CHAT_MODEL,
    temperature: 0.2,
    messages: [
      {
        role: "system",
        content: `
You are ${agent.name}, ${agent.title} at Logix.

Department:
${agent.department}

Personality:
${agent.personality}

Instructions:
${agent.instructions}

You must respond as a structured internal agent.
Return JSON only:
{
  "type": "opinion" | "decision" | "question" | "critique" | "proposal",
  "topic": "short topic",
  "content": "your detailed response",
  "confidence": 0.0,
  "priority": "low" | "medium" | "high" | "critical",
  "references": ["memory_id"]
}
`,
      },
      {
        role: "user",
        content: `
User request:
${params.userRequest}

Relevant company memory:
${memoryContext}
`,
      },
    ],
  });

  const raw = response.choices[0].message.content ?? "{}";
  const parsed = JSON.parse(raw);

  return prisma.agentMessage.create({
    data: {
      episodeId: params.episodeId,
      fromAgentId: params.agentId,
      type: parsed.type as MessageType,
      topic: parsed.topic,
      content: parsed.content,
      confidence: parsed.confidence ?? 0.7,
      priority: parsed.priority as Priority,
      references: parsed.references ?? [],
    },
  });
}
```

---

# 14. Synthesizer

Create `src/runtime/synthesizer.ts`:

```ts
import { prisma } from "../db/prisma";
import { llm, CHAT_MODEL } from "../llm/client";

export async function synthesizeEpisode(episodeId: string) {
  const episode = await prisma.episode.findUniqueOrThrow({
    where: { id: episodeId },
    include: {
      messages: {
        include: {
          fromAgent: true,
        },
      },
    },
  });

  const transcript = episode.messages
    .map(
      (m) => `
${m.fromAgent.title} (${m.fromAgent.name})
Type: ${m.type}
Priority: ${m.priority}
Confidence: ${m.confidence}
Content:
${m.content}
`
    )
    .join("\n---\n");

  const response = await llm.chat.completions.create({
    model: CHAT_MODEL,
    temperature: 0.15,
    messages: [
      {
        role: "system",
        content: `
You are the executive synthesizer for Logix.

You turn agent discussion into a final answer.

Return JSON only:
{
  "finalDecision": "clear final decision",
  "rationale": "why",
  "risks": ["risk"],
  "nextActions": ["action"],
  "memoryCandidates": [
    {
      "type": "decision" | "architecture" | "incident" | "playbook" | "client" | "project" | "lesson" | "note",
      "title": "memory title",
      "content": "memory content",
      "summary": "short summary",
      "tags": ["tag"]
    }
  ]
}
`,
      },
      {
        role: "user",
        content: `
Original user request:
${episode.userRequest}

Agent messages:
${transcript}
`,
      },
    ],
  });

  const raw = response.choices[0].message.content ?? "{}";
  const parsed = JSON.parse(raw);

  await prisma.episode.update({
    where: { id: episodeId },
    data: {
      finalDecision: parsed.finalDecision,
      outcome: "completed",
    },
  });

  return parsed;
}
```

---

# 15. Store Synthesized Memories

Create `src/runtime/store-memory-candidates.ts`:

```ts
import { createMemory } from "../memory/create-memory";
import { MemoryType } from "@prisma/client";

export async function storeMemoryCandidates(
  episodeId: string,
  candidates: any[]
) {
  const stored = [];

  for (const candidate of candidates ?? []) {
    const memory = await createMemory({
      type: candidate.type as MemoryType,
      title: candidate.title,
      content: candidate.content,
      summary: candidate.summary,
      tags: candidate.tags ?? [],
      source: `episode:${episodeId}`,
    });

    stored.push(memory);
  }

  return stored;
}
```

---

# 16. Main Runtime

Create `src/runtime/run-episode.ts`:

```ts
import { prisma } from "../db/prisma";
import { dispatchAgents } from "./dispatcher";
import { runAgent } from "./run-agent";
import { synthesizeEpisode } from "./synthesizer";
import { storeMemoryCandidates } from "./store-memory-candidates";

export async function runEpisode(userRequest: string) {
  const selectedAgents = await dispatchAgents(userRequest);

  const episode = await prisma.episode.create({
    data: {
      type: "general",
      title: userRequest.slice(0, 80),
      userRequest,
      participants: selectedAgents,
    },
  });

  for (const agentId of selectedAgents) {
    await runAgent({
      episodeId: episode.id,
      agentId,
      userRequest,
    });
  }

  const synthesis = await synthesizeEpisode(episode.id);

  const memories = await storeMemoryCandidates(
    episode.id,
    synthesis.memoryCandidates ?? []
  );

  return {
    episodeId: episode.id,
    selectedAgents,
    synthesis,
    storedMemories: memories.map((m) => ({
      id: m.id,
      title: m.title,
      type: m.type,
    })),
  };
}
```

---

# 17. CLI Entrypoint

Create `src/index.ts`:

```ts
import "dotenv/config";
import { runEpisode } from "./runtime/run-episode";

async function main() {
  const userRequest = process.argv.slice(2).join(" ");

  if (!userRequest) {
    console.error("Usage: pnpm ai \"your request\"");
    process.exit(1);
  }

  const result = await runEpisode(userRequest);

  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```

Add to `package.json`:

```json
{
  "scripts": {
    "ai": "tsx src/index.ts",
    "seed:agents": "tsx src/agents/seed-agents.ts"
  }
}
```

Run:

```bash
pnpm seed:agents
pnpm ai "Should Experts support invoices in EUR for the Italian client?"
```

---

# 18. What Happens Now

The flow becomes:

```text
User request
  ↓
Dispatcher picks CTO + CFO + Product
  ↓
Each agent retrieves relevant memories
  ↓
Each agent writes structured message
  ↓
Synthesizer creates final decision
  ↓
System stores new memory candidates
```

This is the “stateful simulated organization with memory, tools, and decision logs” idea from your earlier AI workforce architecture. 

---

# 19. Add Manual Memory Ingestion

Create `src/scripts/add-memory.ts`:

```ts
import "dotenv/config";
import { createMemory } from "../memory/create-memory";

async function main() {
  const title = process.argv[2];
  const type = process.argv[3] as any;
  const content = process.argv.slice(4).join(" ");

  if (!title || !type || !content) {
    console.error(
      `Usage: pnpm tsx src/scripts/add-memory.ts "Title" decision "Content"`
    );
    process.exit(1);
  }

  const memory = await createMemory({
    title,
    type,
    content,
    summary: content.slice(0, 240),
    tags: [],
  });

  console.log(memory);
}

main();
```

Example:

```bash
pnpm tsx src/scripts/add-memory.ts \
  "Experts FX Strategy" \
  decision \
  "Experts should display EUR for foreign clients but settle payments in SAR until payment providers support EUR directly."
```

---

# 20. Add Markdown Import Later

You can ingest Obsidian later as raw documents, but don’t let raw daily notes pollute memory.

Use this rule:

```text
Raw notes → Documents
Extracted knowledge → Memories
```

So:

```text
Document:
2026-06-13 daily note

Memory:
Decision: Display EUR, settle SAR
```

Do not store every daily note as a memory.

---

# 21. Suggested Memory Types

Use these strictly:

```text
decision
```

For anything approved or rejected.

```text
architecture
```

For technical design.

```text
incident
```

For outages, bugs, production issues.

```text
playbook
```

For repeatable procedures.

```text
client
```

For client-specific preferences and constraints.

```text
project
```

For project context.

```text
lesson
```

For things learned after mistakes.

```text
note
```

Use rarely.

---

# 22. Example Good Memories

### Decision

```text
Title:
Experts Multi-Currency Checkout Strategy

Content:
Experts may display prices in EUR for foreign clients, but checkout settlement remains SAR while Noon Payments is the payment provider. FX rates should be cached server-side and shown clearly to buyers.

Tags:
experts, fx, payments, checkout
```

### Playbook

```text
Title:
Clean Stale Git Worktrees

Content:
Run git fetch --all --prune, inspect git worktree list --porcelain, remove worktrees whose branches no longer exist on origin, and protect main/development/staging.

Tags:
git, worktree, cleanup
```

### Incident

```text
Title:
GitHub Runner logix-ci-05 Auto-Stopping

Content:
Runner logix-ci-05 repeatedly becomes inactive while logix-ci-01..04 remain stable. Treat newly created runner instances with the same issue as evidence of shared configuration or systemd registration problem.

Tags:
github-actions, runner, ci, devops
```

---

# 23. Add Tools Layer

Do this after memory works.

Create tool interface:

```ts
export type ToolDefinition = {
  name: string;
  description: string;
  execute: (input: unknown) => Promise<unknown>;
};
```

Example `src/tools/git-status.ts`:

```ts
import { exec } from "node:child_process";
import { promisify } from "node:util";

const execAsync = promisify(exec);

export const gitStatusTool = {
  name: "git_status",
  description: "Get git status for a repository path",
  async execute(input: any) {
    const repoPath = input.repoPath;

    if (!repoPath || !repoPath.startsWith("/home/logix/")) {
      throw new Error("Invalid repo path");
    }

    const { stdout } = await execAsync("git status --short --branch", {
      cwd: repoPath,
    });

    return { stdout };
  },
};
```

Important: tools need strict boundaries.

Agents should not freely run shell commands.

---

# 24. Add API Server Later

Once CLI works, add Fastify:

```bash
pnpm add fastify
```

Create `src/server.ts`:

```ts
import "dotenv/config";
import Fastify from "fastify";
import { runEpisode } from "./runtime/run-episode";

const app = Fastify();

app.post("/episodes", async (request, reply) => {
  const body = request.body as { input: string };

  if (!body.input) {
    return reply.code(400).send({ error: "input is required" });
  }

  const result = await runEpisode(body.input);

  return result;
});

app.listen({ port: 3030, host: "0.0.0.0" }).then(() => {
  console.log("Logix Memory OS running on :3030");
});
```

---

# 25. Roadmap

## Phase 2.1 — Working Memory OS

Build:

```text
Postgres
pgvector
agents
dispatcher
memory retrieval
episodes
synthesizer
CLI
```

This is what the guide above gives you.

## Phase 2.2 — Ingestion

Add:

```text
Markdown importer
GitHub issue importer
Chat transcript importer
ADR importer
```

## Phase 2.3 — Tools

Add safe tools:

```text
read_file
search_repo
git_status
list_branches
read_logs
query_database
```

## Phase 2.4 — UI

Add dashboard:

```text
Episodes
Memories
Decisions
Agent messages
Tool calls
```

## Phase 2.5 — Automation

Use n8n only for external triggers:

```text
New GitHub issue → memory episode
New deployment failure → DevOps episode
New client note → client memory
```

As your earlier plan said, n8n is useful for external workflows, but it should not be the reasoning or memory core. 

---

# My Opinionated Recommendation

Start with this exact order:

```text
1. DB schema
2. Agent seed
3. Manual memory insert
4. Memory retrieval test
5. Run one episode
6. Store synthesized memories
7. Add tools
8. Add UI
```

Do **not** start with:

```text
UI
Obsidian sync
MCP
n8n
fine-tuning
```

Those are distractions until the core loop works.

Your MVP success test is simple:

```bash
pnpm ai "What did we decide about FX pricing for Experts?"
```

If the system retrieves the old FX decision, lets the CFO/CTO/Product agents reason from it, and stores an updated decision, then you no longer have an archive.

You have organizational memory.
