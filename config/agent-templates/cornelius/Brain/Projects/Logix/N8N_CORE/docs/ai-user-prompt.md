---
title: "ai user prompt"
date: "2026-04-11"
tags: ["project/logix", "tech/n8n", "topic/ai-user-prompt"]
category: "projects/logix"
updated: "2026-07-15"
---

## Links

- [[Projects/Logix/N8N_CORE/N8N CORE|N8N Core README]]

Based on the provided project data, generate {{$json.messageGeneration.messageCount}} separate Slack messages for the client update.

_MULTI-MESSAGE STRATEGY:_
Generate messages according to the messageGeneration.instructions provided in the data.
Each message should be a complete, standalone Slack blocks array.
Return as JSON array: [message1_blocks, message2_blocks, message3_blocks]

_PROJECT CONTEXT:_
Project Phase: {{$json.aiContext.projectPhase}}
Project Health: {{$json.executiveSummary.projectHealth}}
Overall Progress: {{$json.progressMetrics.overallProgress}}% complete
Communication Tone: {{$json.aiContext.communicationTone}}

_RECENT ACTIVITY (LAST 48 HOURS):_
{{#if $json.recentActivity.hasActivity}}
Activity Detected: {{$json.recentActivity.summary}}
Recent Updates: {{$json.recentActivity.activities.length}} implementation updates

Top Recent Work:
{{#each $json.recentActivity.activities}}
• {{this.taskTitle}} ({{this.age}}) - {{this.summary}}
{{/each}}
{{else}}
No recent activity detected in the last 48 hours
{{/if}}

_CORE FUNCTIONALITIES STATUS:_
{{#each $json.executiveSummary.coreFunctionalityStatus}}
• {{this.name}}: {{this.progress}}% ({{this.status}})

- Completed: {{this.completed}} | In Progress: {{this.inProgress}} | Planned: {{this.pending}}
  {{/each}}

_DELIVERY OUTLOOK:_
Estimated Completion: {{$json.deliveryPredictions.estimatedCompletion.date}}
Confidence: {{$json.deliveryPredictions.estimatedCompletion.confidence}}

---

_MESSAGE 1 INSTRUCTIONS (Recent Activity):_
{{#if $json.messageGeneration.instructions.message1}}
Type: {{$json.messageGeneration.instructions.message1.type}}
Title: {{$json.messageGeneration.instructions.message1.title}}
Max Length: {{$json.messageGeneration.instructions.message1.maxLength}} characters
Content Requirements:

- Header: "🚀 {{$json.messageGeneration.instructions.message1.title}}"
- Show {{$json.recentActivity.summary}}
- Display recent work from priority domains first: {{$json.messageGeneration.instructions.message1.content.focusOn}}
- Include timestamps and task titles
- Add progress footer: "📈 Overall Progress: {{$json.progressMetrics.overallProgress}}% | {{$json.rawTaskData.overallStats.completedTasks}}/{{$json.rawTaskData.overallStats.totalTasks}} tasks complete"

Generate Slack blocks format with:

- type: "header" with title
- type: "section" for each domain's recent work
- type: "context" for footer

{{else}}
SKIP Message 1 - No recent activity detected
{{/if}}

_MESSAGE 2 INSTRUCTIONS (Core Functionality):_
Type: {{$json.messageGeneration.instructions.message2.type}}
Title: {{$json.messageGeneration.instructions.message2.title}}
Max Length: {{$json.messageGeneration.instructions.message2.maxLength}} characters
Content Requirements:

- Header: "🎯 {{$json.messageGeneration.instructions.message2.title}}"
- Show progress for each of the 4 main functionalities
- Use progress bars: █ for filled, ░ for empty (10 chars total)
- Examples:

```
  90% = █████████░
  50% = █████░░░░░
   0% = ░░░░░░░░░░
```

- Add status emoji: 🎉 near_completion, ⚡ active_development, 🔨 in_progress, 📋 planned
- Include task counts: "X completed | Y in progress | Z planned"
- Show top 3 recent milestones from {{$json.executiveSummary.keyAccomplishments}}

Generate Slack blocks format with:

- type: "header" with title
- type: "section" for each functionality (4 total)
- type: "section" for milestones list

_MESSAGE 3 INSTRUCTIONS (Upcoming Priorities):_
Type: {{$json.messageGeneration.instructions.message3.type}}
Title: {{$json.messageGeneration.instructions.message3.title}}
Max Length: {{$json.messageGeneration.instructions.message3.maxLength}} characters
Condition: {{$json.messageGeneration.instructions.message3.condition}}
Content Requirements:

- Header: "📅 {{$json.messageGeneration.instructions.message3.title}}"
- Show high-priority upcoming deliverables (businessValue >= {{$json.messageGeneration.instructions.message3.content.businessValueThreshold}})
- For each deliverable include:
  - Task title
  - 🎯 Domain name
  - ⏱️ Estimated: X weeks
  - 💡 User benefit
  - 📊 Complexity: Level (score/10)
- Limit to {{$json.messageGeneration.instructions.message3.content.maxItems}} items

Generate Slack blocks format with:

- type: "header" with title
- type: "section" for each deliverable

---

_OUTPUT FORMAT:_
Return a JSON object with structure:

```json
{
  "messages": [
    {
      "blocks": [
        { "type": "header", "text": { "type": "plain_text", "text": "..." } },
        { "type": "section", "text": { "type": "mrkdwn", "text": "..." } }
      ]
    }
  ]
}
```

_CHARACTER LIMIT ENFORCEMENT:_

- Each message MUST be under 2800 characters
- If content exceeds limit, prioritize and truncate appropriately
- NEVER exceed 3000 characters per message

_PRIORITY ORDER:_

1. Course Management System (TOP PRIORITY)
2. Events Management Platform
3. Community Discussion Forums
4. Content & Posts Management
5. Other domains only if space permits

Generate professional, executive-friendly Slack messages that the client can easily scan and understand.
