---
title: "N8N Workflow Update Guide - Smart Multi-Message Reporting"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/taskmaster"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# N8N Workflow Update Guide - Smart Multi-Message Reporting

## 🎯 Overview

The smart client reporter now generates enhanced data specifically formatted for N8N AI to create **multiple Slack messages** instead of one long message.

## 🔄 Correct Architecture

```
┌──────────────────┐
│  orchestrator.js │
│  (generate only) │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│  latest.json saved   │
│  (enhanced data)     │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  N8N Workflow        │
│  (reads latest.json) │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  AI Node             │
│  (generates messages)│
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  Loop Node           │
│  (send each message) │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  Slack Node(s)       │
│  (post to channel)   │
└──────────────────────┘
```

## Enhanced Data Structure

The `latest.json` file now includes:

```json
{
  "reportDate": "2025-12-05",
  "recentActivity": {
    "hasActivity": true,
    "summary": "3 updates in the last 48 hours",
    "activities": [
      {
        "taskTitle": "Module CRUD Implementation",
        "age": "6 hours ago",
        "summary": "COMPLETED: ModuleController with full CRUD; 17 tests passing",
        "domain": "Course Management System"
      }
    ]
  },
  "messageGeneration": {
    "strategy": "multi-message",
    "messageCount": 3,
    "instructions": {
      "message1": {
        "type": "recent_activity",
        "maxLength": 2800,
        "content": {
          "focusOn": ["course-management", "events-management", ...]
        }
      },
      "message2": { ... },
      "message3": { ... }
    }
  },
  "rawTaskData": { ... },
  "executiveSummary": { ... }
}
```

## 🔧 N8N Workflow Modifications

### Current Workflow Structure

Your "Experts Notifications (clone)" workflow should have:

1. **Webhook/Schedule Trigger** - Triggers workflow
2. **Read File Node** - Reads `.taskmaster/reports/client/latest.json`
3. **AI Node** - Generates summary (needs update!)
4. **Slack Node** - Sends message

### Required Updates

#### Update 1: AI Node Configuration

**Current Prompt**: Single message generation

**New Prompt Structure**:

```javascript
// In AI node, replace the prompt with:
const promptTemplate = `
Based on the enhanced project data, generate {{messageGeneration.messageCount}} separate Slack messages.

INSTRUCTIONS:
${JSON.stringify(messageGeneration.instructions, null, 2)}

RECENT ACTIVITY:
${
  recentActivity.hasActivity
    ? `
${recentActivity.summary}
Recent work:
${recentActivity.activities.map((a) => `• ${a.taskTitle} (${a.age}): ${a.summary}`).join("\n")}
`
    : "No recent activity in last 48 hours"
}

CORE FUNCTIONALITIES:
${Object.entries(executiveSummary.coreFunctionalityStatus)
  .map(
    ([key, status]) => `
• ${status.name}: ${status.progress}% (${status.status})
  ${status.completed} completed | ${status.inProgress} in progress | ${status.pending} planned
`,
  )
  .join("\n")}

Generate Slack block messages according to the instructions.
Return as JSON array of message objects, each with "blocks" array.
Each message must be under 2800 characters.

Format:
{
  "messages": [
    { "blocks": [...] },  // Message 1
    { "blocks": [...] },  // Message 2
    { "blocks": [...] }   // Message 3 (if needed)
  ]
}
`;
```

#### Update 2: Add Loop Node

After the AI node, add a **Loop** node to iterate through messages:

1. **Loop Node** - Configure:
   - Input Expression: `{{$json.messages}}`
   - Loop Type: Items
   - Item Mode: Each item

2. **Slack Node** (inside loop):
   - Input: `{{$item.blocks}}`
   - Mode: Blocks
   - Channel: Your client channel

3. **Wait Node** (between messages):
   - Duration: 1 second
   - To ensure proper message ordering

## 📝 Simplified Update Steps

### Option A: Update Existing Workflow (Recommended)

1. **Open "Experts Notifications (clone)" workflow in N8N**

2. **Update AI Node Prompt**:
   - Use the updated prompt from `.taskmaster/.n8n/ai-user-prompt.md`
   - Or use simplified version:

   ```
   Generate {{$json.messageGeneration.messageCount}} Slack messages based on:
   - Recent activity: {{$json.recentActivity}}
   - Instructions: {{$json.messageGeneration.instructions}}
   - Task data: {{$json.rawTaskData}}

   Return as: {"messages": [{"blocks": [...]}, ...]}
   Each message < 2800 characters.
   ```

3. **Add Loop Node** after AI:
   - Loop over: `{{$json.messages}}`

4. **Update Slack Node**:
   - Move inside loop
   - Use: `{{$json.blocks}}` as input

5. **Add 1-Second Wait** between Slack sends

### Option B: Use Pre-Built Messages (Easier)

The smart reporter already generates complete Slack messages. You can:

1. **Skip AI Node** entirely (or use for additional processing)

2. **Use Pre-Built Messages**:

   ```javascript
   // In Function node
   return { json: $input.item.json.slackMessages };
   ```

3. **Loop and Send**:
   - Loop over slackMessages array
   - Send each to Slack directly

## 🧪 Testing the Update

### Test Data Generation

```bash
cd /home/logix/experts

# Generate test report
node .taskmaster/review-cycles/smart-client-reporter.js

# Check output
cat .taskmaster/reports/client/latest.json | jq '.messageGeneration'
```

### Verify N8N Receives Data

1. **Trigger workflow manually** in N8N
2. **Check AI node output** - should see messageGeneration instructions
3. **Verify multi-message generation**
4. **Test Slack delivery** - should see 1-3 messages

## 📊 Expected Output

### Message 1 (Recent Activity - if work done)

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🚀 Recent Work Activity - 2025-12-05"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*3 updates in the last 48 hours*"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*🎯 Course Management System (TOP PRIORITY)*\n\n• Module CRUD Implementation (6 hours ago)\n  COMPLETED: ModuleController with full CRUD; 17 tests passing"
      }
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "📈 Overall Progress: 63% | 12/34 tasks complete"
        }
      ]
    }
  ]
}
```

### Message 2 (Core Status - always)

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🎯 Core Platform Status"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Course Management System (TOP PRIORITY)* 🎉\n█████████░ 89%\n1 completed | 0 in progress | 4 planned"
      }
    }
  ]
}
```

## 🎯 Benefits of This Approach

### For Your Workflow

- ✅ AI still generates messages (your existing setup)
- ✅ Enhanced with recent activity data (NEW)
- ✅ Multi-message support via loop (NEW)
- ✅ Character limits handled automatically
- ✅ Priority-aware content generation

### vs. Direct Slack Sending

- ✅ AI can customize message tone and style
- ✅ AI can adapt to client preferences
- ✅ More flexible than hard-coded messages
- ✅ Maintains your existing workflow pattern

## 🔍 Troubleshooting

### AI Not Generating Multiple Messages

**Check**:

```javascript
// In N8N Function node before AI
console.log("Message count:", $json.messageGeneration.messageCount);
console.log("Has activity:", $json.recentActivity.hasActivity);
```

**Fix**: Update AI prompt to explicitly request array of messages

### Messages Still Single

**Check**: AI node output format

**Fix**: Ensure AI returns:

```json
{
  "messages": [
    { "blocks": [...] },
    { "blocks": [...] }
  ]
}
```

### Character Limits Still Exceeded

**Check**: Each message length in AI output

**Fix**: Add validation node after AI:

```javascript
// Truncate if needed
$json.messages.forEach((msg) => {
  const length = JSON.stringify(msg.blocks).length;
  if (length > 2800) {
    console.warn(`Message exceeds limit: ${length} chars`);
  }
});
```

## 🚀 Quick Start

### Minimal Workflow Update

1. Open "Experts Notifications (clone)" in N8N

2. Update AI prompt with:

   ```
   Generate {{$json.messageGeneration.messageCount}} Slack messages.
   Use instructions from: {{$json.messageGeneration.instructions}}
   Include recent activity if: {{$json.recentActivity.hasActivity}}
   Return as: {"messages": [{"blocks": [...]}, ...]}
   ```

3. Add Loop node after AI

4. Move Slack node inside loop

5. Test!

---

**Updated**: December 5, 2025  
**Compatibility**: Works with existing N8N workflow  
**Complexity**: Low (minimal changes needed)  
**Benefit**: High (multi-message support + recent activity)
