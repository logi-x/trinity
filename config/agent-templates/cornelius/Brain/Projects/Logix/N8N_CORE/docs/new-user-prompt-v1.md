---
title: "new user prompt v1"
date: "2026-04-11"
tags: ["project/logix", "tech/n8n", "topic/new-user-prompt-v1"]
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
Emphasis Instructions: {{ $('Process Data').item.json.context.aiContext.clientFocusMessage.emphasisInstructions }}

_CHANGES SINCE LAST UPDATE:_
{{ $json.hasHistory ? 'Progress Change: ' + ($json.changes.progressChange > 0 ? '+' + $json.changes.progressChange + '%' : $json.changes.progressChange + '%') : 'First report - establishing baseline' }}
{{ $json.changes.newAccomplishments.length > 0 ? 'New Completions: ' + $json.changes.newAccomplishments.join(', ') : 'No new completions since last update' }}

_RECENT ACHIEVEMENTS:_
{{ $('Process Data').item.json.summaryData.achievements.map(a => '• ' + a.title + ': ' + a.impact).join('\n') }}

_CURRENT FOCUS AREAS:_
{{ $('Process Data').item.json.summaryData.currentWork.map(w => '• ' + w.title + ' (Timeline: ' + w.timeline + ')').join('\n') }}

_UPCOMING MILESTONES:_
{{ $('Process Data').item.json.summaryData.outlook.upcomingMilestones.map(m => '• ' + (m.goal || m.title || m)).join('\n') }}

_CHALLENGES & MITIGATION:_
{{ $('Process Data').item.json.summaryData.challenges.length > 0 ? $('Process Data').item.json.summaryData.challenges.map(c => '• ' + c.area + ' (' + c.level + ' priority): ' + c.mitigation).join('\n') : 'No significant challenges identified' }}

_DELIVERY OUTLOOK:_
{{ $('Process Data').item.json.summaryData.outlook.timeline ? 'Estimated Completion: ' + $('Process Data').item.json.summaryData.outlook.timeline.date + ' (Confidence: ' + $('Process Data').item.json.summaryData.outlook.timeline.confidence + ')' : 'Timeline being refined based on current progress' }}

_RECOMMENDED TERMINOLOGY:_
{{ Object.entries($('Process Data').item.json.summaryData.communication.terminology).map(([key, value]) => key + " -> " + value).join('\n') }}

_SPECIFIC REQUIREMENTS:_

1. _Structure:_ Open with the recommended tone, highlight progress and achievements, explain current work with timelines, address challenges with solutions, provide realistic future expectations, close with project confidence message
2. _Content Focus:_ Emphasize business value and user impact over technical implementation, use client-preferred terminology, include specific progress metrics, be transparent about challenges while emphasizing solutions
3. _Format:_ Create 3-4 well-structured paragraphs that can be read in under 2 minutes, use markdown formatting suitable for both Slack and email, include clear section breaks for executive scanning
4. _Tone:_ Use professional but warm language, avoid technical jargon, focus on outcomes and benefits, maintain optimism while being realistic about timelines

Try to extract newly added tasks from Raw Task Data (JSON) below, most likely it will be marked as (NEW) at the end of the title of the task, or can be found in metadata and include it in the final response in achievements and operational updates section if it's status was done.

Raw Task Data (JSON):
{{ JSON.stringify($('Process Data').item.json.context.taskData) }}

Main Functionalities (JSON):
{{ JSON.stringify($('Process Data').item.json.rawdata.mainFunctionalities) }}

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
- Focus on what’s done, what’s next, and why it matters
- Keep tone confident and forward-looking
- Use Slack mrkdwn for formatting
- End with a next update schedule line

🧩 STRUCTURE EXPECTED

- Opening & quick summary
- Core focus area (Course Management progress)
- Achievements & immediate milestones
- Upcoming tasks
- Challenges & mitigation
- Delivery outlook & closing
