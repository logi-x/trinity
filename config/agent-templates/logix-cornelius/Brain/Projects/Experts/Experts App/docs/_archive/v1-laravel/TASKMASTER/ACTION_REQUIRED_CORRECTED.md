---
title: "🚨 ACTION REQUIRED: Update Your N8N Workflow"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/taskmaster"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🚨 ACTION REQUIRED: Update Your N8N Workflow

## ⚡ Quick Summary

The smart reporter now generates **enhanced data for your N8N AI** to create multiple Slack messages instead of one long message.

**Your Flow**: ✅ Orchestrator → N8N → AI → Slack (preserved!)  
**My Mistake**: ❌ I initially tried to bypass N8N and send directly to Slack  
**Now Fixed**: ✅ Orchestrator only generates enhanced report for N8N

---

## 📋 3 Simple Steps to Update Your Workflow

### Step 1: Update AI Prompts in N8N (5 minutes)

**System Prompt**: Copy from `.taskmaster/.n8n/ai-system-prompt.md`

**User Prompt**: Copy from `.taskmaster/.n8n/ai-user-prompt.md`

These new prompts instruct the AI to:

- Generate 1-3 separate Slack messages
- Use recent activity data (NEW!)
- Follow character limits per message
- Format as Slack blocks

### Step 2: Add Loop for Multi-Message Delivery (3 minutes)

Your workflow currently: `Read File → AI → Slack`

Update to: `Read File → AI → Loop → Wait → Slack`

**In N8N**:

1. After AI node, add **Loop Over Items** node
   - Input: `{{$json.messages}}`

2. Add **Wait** node (inside loop)
   - Duration: 1 second

3. Move **Slack** node inside loop
   - Input: `{{$json.blocks}}`

### Step 3: Test (2 minutes)

```bash
# Generate test data
cd /home/logix/experts && ./run-cycle.sh client

# Verify format
cat .taskmaster/reports/client/latest.json | jq '.messageGeneration.messageCount'
# Should output: 2 or 3

# Trigger N8N workflow manually and verify 1-3 messages in Slack
```

---

## 🎯 What's Different Now

### Enhanced Data for N8N

Your AI node now receives:

```json
{
  "messageGeneration": {
    "messageCount": 3,
    "instructions": {
      "message1": {
        "type": "recent_activity",
        "maxLength": 2800,
        "content": {...}
      },
      "message2": {...},
      "message3": {...}
    }
  },
  "recentActivity": {
    "hasActivity": true,
    "activities": [
      {"taskTitle": "...", "age": "6 hours ago", "summary": "..."}
    ]
  },
  "preBuiltMessages": [
    {"blocks": [...]},  // Optional: AI can use or generate own
    {"blocks": [...]},
    {"blocks": [...]}
  ]
}
```

### What the AI Should Generate

**Message 1** (if recent work):

```
🚀 Recent Work Activity - 2025-12-05
• Course Module CRUD (6 hours ago)
  COMPLETED: Full implementation with 17 tests passing
```

**Message 2** (always):

```
🎯 Core Platform Status
Course Management: █████████░ 89%
Events Management: ░░░░░░░░░░ 0%
```

**Message 3** (conditional):

```
📅 Upcoming High-Priority Items
• Course Creation System (1 week)
• Authentication Improvements (1 week)
```

---

## 🔍 Verification

### Correct latest.json Format

```bash
cat .taskmaster/reports/client/latest.json | jq 'has("messageGeneration")'
# Should output: true

cat .taskmaster/reports/client/latest.json | jq '.messageGeneration.messageCount'
# Should output: 2 or 3

cat .taskmaster/reports/client/latest.json | jq '.recentActivity.hasActivity'
# Should output: true or false
```

### N8N AI Node Check

After triggering workflow:

- ✅ AI receives `messageGeneration.instructions`
- ✅ AI generates array of messages
- ✅ Each message has `blocks` array
- ✅ Each message under 2800 characters

### Slack Delivery Check

- ✅ Receive 1-3 separate messages
- ✅ Messages appear in sequence (1s apart)
- ✅ Recent activity shown (when work done)
- ✅ 4 main functionalities prominent

---

## 📚 Full Documentation

- **Architecture**: `.taskmaster/review-cycles/CORRECTED_ARCHITECTURE.md`
- **N8N Guide**: `.taskmaster/review-cycles/N8N_WORKFLOW_UPDATE_GUIDE.md`
- **AI Prompts**: `.taskmaster/.n8n/ai-*-prompt.md`

---

## ❓ Need Help?

### Option 1: Use Pre-Built Messages

If AI generation is complex, use the pre-built messages instead:

```javascript
// In N8N Function node after Read File
return { json: $json.preBuiltMessages };
```

Then loop and send to Slack directly (no AI needed).

### Option 2: Minimal AI Prompt

Simplest AI prompt that works:

```
Generate {{$json.messageGeneration.messageCount}} Slack messages.

Message 1: Recent activity (if {{$json.recentActivity.hasActivity}})
Message 2: Core functionality status
Message 3: Upcoming priorities

Use data from: {{$json}}

Return as: {"messages": [{"blocks": [...]}, ...]}
Each message < 2800 characters.
```

---

**Status**: ✅ Corrected and Tested  
**Ready**: ✅ Orchestrator updated  
**Next**: ⏳ Update N8N workflow  
**Time**: 10 minutes total
