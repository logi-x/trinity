---
title: "ai user prompt old"
date: "2026-04-11"
tags: ["project/logix", "tech/n8n", "topic/ai-user-prompt-old"]
category: "projects/logix"
updated: "2026-07-15"
---

## Links

- [[Projects/Logix/N8N_CORE/N8N CORE|N8N Core README]]

Create a comprehensive yet accessible daily project update for a client using the provided project data.

_CONTEXT & GUIDANCE:_
Project Phase: {{ $('Process Data').item.json.timeline.currentPhase }}
Project Health: {{ $('Process Data').item.json.summaryData.status.health }}
Overall Progress: {{ $('Process Data').item.json.summaryData.status.progress }}
Communication Tone: {{ $('Process Data').item.json.summaryData.communication.tone }}
Recommended Opening: {{ $('Process Data').item.json.summaryData.communication.openingTone }}, or suggest a new opening tone.
Core Priority: {{ $('Process Data').item.json.context.aiContext.clientFocusMessage.corePriority }}

_CURRENT FOCUS AREAS:_
{{ $('Process Data').item.json.summaryData.currentWork.map(w => '• ' + w.title + ' (Timeline: ' + w.timeline + ')').join('\n') }}

_DELIVERY OUTLOOK:_
{{ $('Process Data').item.json.summaryData.outlook.timeline ? 'Estimated Completion: ' + $('Process Data').item.json.summaryData.outlook.timeline.date + ' (Confidence: ' + $('Process Data').item.json.summaryData.outlook.timeline.confidence + ')' : 'Timeline being refined based on current progress' }}

_RECOMMENDED TERMINOLOGY:_
{{ Object.entries($('Process Data').item.json.summaryData.communication.terminology).map(([key, value]) => key + " -> " + value).join('\n') }}

Raw Task Data (JSON):
{{ JSON.stringify($('Process Data').item.json.context.taskData) }}

Recent Changes (JSON):
{{ JSON.stringify($json.changes) }}

🎯 PRIORITY INSTRUCTIONS

- Lead with Course Management System (primary focus).
- Mention secondary functionalities (Events, Community Discussions, Content & Posts) after core progress.
- Show progress percentages and clear business value.
- Limit Quick summary to ≤350 characters.
- Limit Estimated completion section to ≤250 characters.
- Include 2 most recent Achievements and Upcoming Tasks only, (most recent tasks from metadata).
- If new tasks (marked as “NEW”) are completed, list them in Achievements.

💬 OUTPUT STYLE

- Write for executive stakeholders (not engineers)
- Focus on what’s done, what’s in-progress, what’s next, and why it matters
- Keep tone confident and forward-looking
- Use Slack mrkdwn for formatting
- End with a next update schedule line

🧩 STRUCTURE EXPECTED

- Opening & quick summary
- Core focus area (Course Management progress)
- Currently working on
- Achievements & immediate milestones
- Upcoming tasks

IMPORTANT: include any NEW tasks as (recent-progress) even by replacing main functionalities...
