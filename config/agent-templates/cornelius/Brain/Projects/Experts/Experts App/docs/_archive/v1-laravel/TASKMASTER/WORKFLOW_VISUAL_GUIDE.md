---
title: "🎨 Visual Guide: N8N Workflow Update"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/taskmaster"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🎨 Visual Guide: N8N Workflow Update

## 📊 Current Workflow Structure

```
┌─────────────────────┐
│  Cron (Daily 7AM)   │
│  Or Webhook Trigger │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────┐
│  Read Client Report      │
│  (.taskmaster/.../latest)│
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Process Data            │
│  (Transform to summary)  │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  AI Summarization        │
│  (Generate 1 message)    │
└──────────┬───────────────┘
           │
           ├────────────────┐
           │                │
           ▼                ▼
   ┌──────────────┐  ┌────────────┐
   │ Slack Send   │  │ Store Data │
   └──────────────┘  └────────────┘
```

## 🎯 New Workflow Structure (Multi-Message)

```
┌─────────────────────┐
│  Cron (Daily 7AM)   │
│  Or Webhook Trigger │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────┐
│  Read Client Report      │
│  (NOW has recentActivity │
│   and messageGeneration) │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Process Data            │
│  (Transform to summary)  │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  AI Summarization (UPDATED PROMPTS)      │
│  Generates: {"messages": [              │
│    {"blocks": [...]},  // Message 1      │
│    {"blocks": [...]},  // Message 2      │
│    {"blocks": [...]}   // Message 3      │
│  ]}                                      │
└──────────┬─────────────────────────────────┘
           │
           ├─────────────────┐
           │                 │
           ▼                 ▼
   ┌───────────────┐   ┌────────────┐
   │ Store Data    │   │ Emails     │
   └───────────────┘   └────────────┘
           │
           ▼
   ┌────────────────────────────┐
   │ ✨ Extract Messages (NEW)  │
   │ Parse AI JSON response     │
   │ Output: Array of messages  │
   └────────────┬───────────────┘
                │
                ▼
   ┌─────────────────────────────┐
   │ 🔄 Loop Over Messages (NEW) │
   │ Process messages one by one │
   └────────────┬────────────────┘
                │
                ▼
   ┌──────────────────────────────┐
   │ ⏱️ Wait 1 Second (NEW)       │
   │ Delay between messages       │
   └────────────┬─────────────────┘
                │
                ▼
   ┌──────────────────────────────┐
   │ 📤 Send Slack Notification   │
   │ (UPDATED to use $json)       │
   └────────────┬─────────────────┘
                │
                └──────┐
                       │
                       ▼ (Loop back to process next message)
                  ┌─────────────────┐
                  │ Loop Complete?  │
                  └────┬────────┬───┘
                  Yes  │        │ No
                       │        └─────► Back to Loop
                       ▼
                  ┌─────────┐
                  │  Done   │
                  └─────────┘
```

## 🔄 Data Flow Through New Nodes

### 1. Extract Messages Node Output

**Input** (from AI):

```json
{
  "message": {
    "content": "{\"messages\": [{\"blocks\": [...]}, {\"blocks\": [...]}]}"
  }
}
```

**Output** (to Loop):

```json
[
  { "json": { "blocks": [...] } },  // Item 1
  { "json": { "blocks": [...] } },  // Item 2
  { "json": { "blocks": [...] } }   // Item 3
]
```

### 2. Loop Over Messages

**Configuration**:

- Batch Size: 1
- Processes one message at a time

**Output per iteration**:

```json
{
  "blocks": [
    { "type": "header", "text": { "type": "plain_text", "text": "..." } },
    { "type": "section", "text": { "type": "mrkdwn", "text": "..." } }
  ]
}
```

### 3. Slack Node Receives

**Blocks UI**: `={{JSON.stringify($json)}}`

This directly uses the blocks from the current loop iteration.

---

## 📝 Node Configuration Quick Reference

### Extract Messages (Code Node)

```javascript
// Parses AI response and extracts messages array
const aiResponse = $input.first().json;
let messages = [];

// Try multiple parsing strategies
if (aiResponse.messages) {
  messages = aiResponse.messages;
} else if (aiResponse.message?.content) {
  messages = JSON.parse(aiResponse.message.content).messages;
}

// Fallback if parsing fails
if (!messages.length) {
  messages = [{ blocks: [...] }];
}

return messages.map(msg => ({ json: msg }));
```

### Loop Over Messages (Split In Batches)

- **Batch Size**: `1`
- **Options**: Default

### Wait Between Messages (Wait Node)

- **Amount**: `1`
- **Unit**: `seconds`

### Send Slack Notification (Updated)

- **Message Type**: Block
- **Blocks UI**: `={{JSON.stringify($json)}}`

---

## 🎯 What Each Message Contains

### Message 1: Recent Activity (Conditional)

**Triggers**: Only if work done in last 48 hours

**Structure**:

```
🚀 Recent Work Activity - 2025-12-05

[Summary of updates]

🎯 [Domain Name]
• [Task Title] ([Time ago])
  [What was done]

📈 Overall Progress: X% | Y/Z tasks complete
```

**Max Length**: 2800 characters

---

### Message 2: Core Platform Status (Always)

**Triggers**: Always generated

**Structure**:

```
🎯 Core Platform Status

[Functionality Name] [Status Emoji]
[Progress Bar: ██████░░░░] X%
Y completed | Z in progress | W planned

[Repeat for 4 main functionalities]

📋 Recent Milestones:
• [Milestone 1]
• [Milestone 2]
```

**Max Length**: 2000 characters

---

### Message 3: Upcoming Priorities (Conditional)

**Triggers**: If no recent activity OR risks detected

**Structure**:

```
📅 Upcoming High-Priority Items

• [Task Title]
  🎯 [Domain]
  ⏱️ Estimated: [X weeks]
  💡 [User benefit]
  📊 Complexity: [Level] ([Score]/10)

[Repeat for top 4 high-priority items]
```

**Max Length**: 2500 characters

---

## 🧪 Testing Checklist

### After Making Changes

- [ ] Execute workflow manually
- [ ] Check AI node output (should be JSON with messages array)
- [ ] Verify Extract Messages output (array of message objects)
- [ ] Confirm Loop processes each message
- [ ] Check 1-second delay between messages
- [ ] Verify all messages delivered to Slack
- [ ] Confirm messages are properly formatted
- [ ] Check character counts are under limits

### Expected Behavior

1. **Workflow starts** (cron/webhook/manual)
2. **Reads latest.json** with enhanced data
3. **AI generates** 1-3 messages as JSON
4. **Extract parses** JSON into array
5. **Loop begins** processing first message
6. **Wait 1 second**
7. **Slack sends** message 1
8. **Loop back** to process next message
9. **Repeat** until all messages sent
10. **Store data** for next comparison

---

## 💡 Pro Tips

### Debugging

1. **Click each node** and check "Output" tab
2. **Use "Execute Node"** to test individual nodes
3. **Check N8N logs** for errors
4. **Verify Slack webhook** is working

### Fallback Options

If AI generation is problematic:

1. Skip AI customization
2. Use pre-built messages from smart reporter
3. Add Code node after "Process Data":

   ```javascript
   const data = $input.first().json;
   return data.preBuiltMessages.map((msg) => ({ json: msg }));
   ```

### Performance

- 1-second delay ensures proper message ordering
- Slack API rate limits: 1 message/second is safe
- Total workflow time: ~10-15 seconds for 3 messages

---

**Created**: December 5, 2025
**Workflow ID**: 5Fti68qm82fsXxFp
**Status**: Ready to implement
**Time Required**: 10 minutes
