---
title: "Ask AI branding and training guide"
date: "2026-04-29"
tags: ["project/experts", "ai", "ask-ai", "branding", "rag", "openai"]
category: "guide"
source: "codex"
source_id: "2026-04-29-ask-ai-branding-training-guide"
---

# Ask AI branding and training guide

## Short answer

Do not treat Ask AI as something we "train" directly from the OpenAI Assistants page.

For new work, prefer the **Responses API / Prompts** direction. OpenAI's docs say the older Assistants API is deprecated and scheduled to shut down on **2026-08-26**. The dashboard can still be useful for managing prompt-style configuration, but the Experts product should keep the important business knowledge, branding, retrieval, access control, and feedback loop inside our own app.

## What OpenAI controls

OpenAI can control:

- model choice;
- system/developer instructions;
- prompt objects / reusable prompt configuration;
- built-in tools such as file search or web search when enabled;
- response format and tool declarations;
- stateful response/conversation behavior if we choose to use it.

Good OpenAI-side instruction examples:

```text
You are Ask AI, an internal assistant for the Experts platform.
Use a professional, clear, Saudi-market-aware tone.
Do not overpromise. If context is missing, say what is missing.
For pricing, policy, availability, and legal claims, answer only from approved context.
```

## What Experts should control

Experts should control:

- admin-only access;
- Statsig rollout gate;
- company profile and brand guidelines;
- approved claims and forbidden claims;
- product/service plan facts;
- course, event, community, and pricing retrieval;
- user/admin feedback;
- audit logs;
- answer sources;
- escalation rules;
- whether answers can be saved back into the knowledge base.

This keeps the assistant safe and maintainable. We should not rely on a dashboard prompt as the only source of business truth.

## Recommended architecture

Use four layers:

1. **Stable assistant instructions**
   - Role, tone, refusal rules, answer style, and safety boundaries.
   - Can be stored as a prompt in OpenAI or as a versioned prompt file/config in the app.

2. **Company and brand profile**
   - Mission, audience, tone, services, product positioning, supported languages, allowed terms, and forbidden claims.
   - Store in Experts DB or a versioned knowledge document.
   - Inject into Ask AI as high-priority context.

3. **Retrieval / RAG**
   - Embed and retrieve approved knowledge:
     - courses,
     - events,
     - posts,
     - plans,
     - policies,
     - feature pages,
     - FAQ/support docs,
     - company profile,
     - brand guidelines.
   - The assistant should answer from retrieved context and cite internal source IDs.

4. **Feedback loop**
   - Capture admin question, answer, retrieved sources, thumbs up/down, correction, and "save as approved answer".
   - Use feedback to improve retrieval, fill documentation gaps, and eventually prepare fine-tuning data.

## Branding profile fields

Suggested `CompanyAIProfile` fields:

```ts
type CompanyAIProfile = {
  companyName: string;
  mission: string;
  audience: string[];
  positioning: string;
  tone: string[];
  languageRules: {
    en: string;
    ar: string;
    es: string;
  };
  approvedClaims: string[];
  forbiddenClaims: string[];
  productCategories: string[];
  services: Array<{
    name: string;
    description: string;
    audience: string;
    availability: string;
  }>;
  policyNotes: string[];
  escalationRules: string[];
};
```

## User input learning

Raw user/admin questions should not automatically retrain the assistant.

Instead:

- store questions as analytics signals;
- classify the intent;
- track retrieved sources;
- collect feedback;
- allow admins to save corrected answers;
- periodically promote approved answers into the knowledge base.

This creates controlled learning without letting one bad prompt corrupt the assistant.

## What not to do

- Do not let every user question become permanent knowledge.
- Do not put secrets, private user data, API keys, or payment credentials into system instructions.
- Do not hardcode business claims only in OpenAI dashboard prompts.
- Do not fine-tune before we have a clean set of approved examples.
- Do not let Ask AI answer legal, accreditation, pricing, refund, or availability questions without approved context.

## When to fine-tune

Fine-tuning is later-stage.

Use fine-tuning only if:

- RAG already retrieves the right facts;
- prompts are stable;
- brand profile is clear;
- we have many reviewed examples;
- the model still fails on repeatable style, structure, or classification tasks.

Fine-tuning is not the right tool for fast-changing facts like courses, events, prices, policies, or company pages. Those should stay in retrieval.

## Practical implementation plan for Experts

### Phase 1: current branch

- Ask AI is admin-only.
- UI is gated by Statsig gate `ask_ai_global_assistant`.
- API is protected by server-side admin permission.
- Context is compact DB context from published courses, events, posts, active plans, and business notes.

### Phase 2: company profile

- Add an editable admin-only Company AI Profile.
- Include brand voice, approved claims, forbidden claims, product/service descriptions, and escalation rules.
- Inject this profile into every Ask AI request.

### Phase 3: knowledge base documents

- Add `KnowledgeBaseDocument` / `KnowledgeBaseChunk`.
- Embed approved docs with pgvector.
- Retrieve top matching chunks for each question.
- Include source IDs in Ask AI responses.

### Phase 4: feedback

- Add thumbs up/down.
- Add "mark incorrect".
- Add "save corrected answer".
- Add "add to knowledge base".
- Review low-confidence or downvoted answers weekly.

### Phase 5: OpenAI prompt management

- If useful, move the stable assistant instruction into an OpenAI Prompt object.
- Keep dynamic context, brand profile, retrieval, permissions, and audit trail in Experts.
- Do not build new work on the deprecated Assistants API unless there is a specific short-term migration reason.

## Suggested system instruction

```text
You are Ask AI, an internal admin assistant for Experts.

Experts is a Saudi-market-aware learning marketplace and LMS for courses, live events, creators, learners, community content, subscriptions, payments, certificates, and admin operations.

Use the provided company profile, brand guidelines, and retrieved platform context as the source of truth.

Tone:
- professional,
- clear,
- practical,
- concise,
- helpful without hype.

Rules:
- Do not invent exact prices, dates, policies, legal claims, accreditation claims, or availability.
- If context is missing, say what is missing and suggest where an admin should check.
- Prefer actionable answers with short bullets.
- Keep sensitive operational details internal.
- For learner-facing copy, avoid overpromising outcomes.
- For AI/assessment topics, do not encourage cheating or replacing formal assessments.
```

## References

- OpenAI Assistants migration guide: <https://platform.openai.com/docs/assistants/how-it-works>
- OpenAI Responses migration guide: <https://platform.openai.com/docs/guides/migrate-to-responses>
- OpenAI tools guide: <https://platform.openai.com/docs/guides/tools?api-mode=responses>
