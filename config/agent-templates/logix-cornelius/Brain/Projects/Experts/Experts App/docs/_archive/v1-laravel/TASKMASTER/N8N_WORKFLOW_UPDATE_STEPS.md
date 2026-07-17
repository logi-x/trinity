---
title: '🔧 Step-by-Step: Update "Experts Notifications (clone)" Workflow'
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/taskmaster"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🔧 Step-by-Step: Update "Experts Notifications (clone)" Workflow

## ✅ What I've Prepared

I've analyzed your N8N workflow and prepared all the modifications needed. Here's what needs to be updated:

### Current Flow

```
AI Summarization → Send Slack Notification
                 → Store Latest State
                 → Emails
```

### New Flow

```
AI Summarization → Extract Messages → Loop Over Messages → Wait (1s) → Send Slack Notification
                 → Store Latest State                                        ↓
                 → Emails                                            (Loop back)
```

---

## 📋 Update Steps (10 minutes)

### Step 1: Update AI Summarization Prompts (3 minutes)

1. Open "Experts Notifications (clone)" workflow in N8N
2. Click on **"AI Summarization"** node
3. Click on **"Messages"** tab
4. Replace **System Message** with:

````
You are a professional project communication specialist creating multi-message daily client updates for software development projects.

🎯 ROLE & OBJECTIVE:
Your purpose is to transform detailed project data into 1-3 separate, concise Slack messages that communicate progress, actual implementation work, and upcoming priorities. Each message should be independently valuable and scannable.

🧩 YOUR CAPABILITIES

- Translate technical progress into business-oriented impact statements
- Create focused, single-purpose messages that work well in Slack
- Highlight recent implementation work (what was actually built in last 48h)
- Balance progress updates with upcoming priorities
- Maintain professional tone across multiple message sequence

🧭 COMMUNICATION RULES

- Use plain language; avoid developer jargon
- Focus on business outcomes (efficiency, productivity, experience)
- Each message must be self-contained and scannable
- Use Slack mrkdwn formatting (*, ~, >, •)
- Messages must work independently (can be read out of order)

🧱 MULTI-MESSAGE OUTPUT REQUIREMENTS

You will generate 1-3 separate Slack messages based on the messageGeneration instructions:

**MESSAGE 1: Recent Activity** (Only if recentActivity.hasActivity = true)
- Maximum length: 2800 characters
- Focus: What was actually implemented in last 48 hours
- Include: Timestamps, task titles, completion status
- Priority: Show 4 main functionalities first

**MESSAGE 2: Core Functionality Status** (Always generate)
- Maximum length: 2000 characters
- Focus: Progress on 4 main functionalities
- Include: Progress percentages, task counts, recent milestones
- Priority: Course Management System is TOP PRIORITY

**MESSAGE 3: Upcoming Priorities** (Conditional)
- Maximum length: 2500 characters
- Focus: High-priority next deliverables
- Include: Complexity scores, time estimates, business value

**CRITICAL: Output Format**
You MUST return a JSON object with this exact structure:
```json
{
  "messages": [
    { "blocks": [...] },
    { "blocks": [...] }
  ]
}
````

Each message.blocks array must contain valid Slack Block Kit elements.
Each complete message must be under 2800 characters when serialized.

```

5. Replace **User Message** with:

```

Based on the provided project data, generate {{$json.messageGeneration ? $json.messageGeneration.messageCount : 1}} separate Slack messages for the client update.

_MULTI-MESSAGE STRATEGY:_
Generate messages according to the messageGeneration.instructions provided in the data.
Each message should be a complete, standalone Slack blocks array.
Return as JSON object: {"messages": [{"blocks": [...]}, {"blocks": [...]}]}

_PROJECT CONTEXT:_
Project Phase: {{$json.aiContext ? $json.aiContext.projectPhase : $('Process Data').item.json.timeline.currentPhase}}
Project Health: {{$json.executiveSummary ? $json.executiveSummary.projectHealth : $('Process Data').item.json.summaryData.status.health}}
Overall Progress: {{$json.progressMetrics ? $json.progressMetrics.overallProgress + '%' : $('Process Data').item.json.summaryData.status.progress}}

_RECENT ACTIVITY (LAST 48 HOURS):_
{{$json.recentActivity ? ($json.recentActivity.hasActivity ? $json.recentActivity.summary + '\n\nTop Recent Work:\n' + $json.recentActivity.activities.map(a => '• ' + a.taskTitle + ' (' + a.age + ') - ' + a.summary).join('\n') : 'No recent activity detected in the last 48 hours') : 'Recent activity data not available'}}

_CORE FUNCTIONALITIES STATUS:_
{{$json.executiveSummary ? $json.executiveSummary.coreFunctionalityStatus.map(f => '• ' + f.name + ': ' + f.progress + '% (' + f.status + ')\n  - Completed: ' + f.completed + ' | In Progress: ' + f.inProgress + ' | Planned: ' + f.pending).join('\n') : 'Using legacy data format'}}

_DELIVERY OUTLOOK:_
Estimated Completion: {{$json.deliveryPredictions ? $json.deliveryPredictions.estimatedCompletion.date : $('Process Data').item.json.summaryData.outlook.timeline.date}}
Confidence: {{$json.deliveryPredictions ? $json.deliveryPredictions.estimatedCompletion.confidence : $('Process Data').item.json.summaryData.outlook.timeline.confidence}}

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

Generate professional, executive-friendly Slack messages that the client can easily scan and understand.

````

6. Click **"Save"**

---

### Step 2: Add "Extract Messages" Node (2 minutes)

1. Click on **"AI Summarization"** node
2. Click the **"+"** button on the right side
3. Search for **"Code"** node
4. Name it: **"Extract Messages"**
5. Paste this JavaScript code:

```javascript
// Extract messages array from AI response
const aiResponse = $input.first().json;

// Handle both direct messages array and nested in message.content
let messages = [];

if (aiResponse.messages && Array.isArray(aiResponse.messages)) {
  messages = aiResponse.messages;
} else if (aiResponse.message && aiResponse.message.content) {
  try {
    const parsed = JSON.parse(aiResponse.message.content);
    if (parsed.messages && Array.isArray(parsed.messages)) {
      messages = parsed.messages;
    }
  } catch (e) {
    console.error('Failed to parse AI response:', e);
    // Fallback: use existing single message format
    messages = [{
      blocks: [
        {"type": "header", "text": {"type": "plain_text", "text": "📊 Daily Project Update"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": aiResponse.message?.content || "No update available"}}
      ]
    }];
  }
}

// If no messages found, create single message fallback
if (messages.length === 0) {
  const content = aiResponse.message?.content || 'No update available';
  messages = [{
    blocks: [
      {"type": "header", "text": {"type": "plain_text", "text": "📊 Daily Project Update"}},
      {"type": "section", "text": {"type": "mrkdwn", "text": content}}
    ]
  }];
}

// Return each message as separate item for loop processing
return messages.map(msg => ({ json: msg }));
````

6. Click **"Execute Node"** to test
7. Verify output shows array of messages

---

### Step 3: Add "Loop Over Messages" Node (2 minutes)

1. Click on **"Extract Messages"** node
2. Click the **"+"** button
3. Search for **"Split In Batches"** node
4. Name it: **"Loop Over Messages"**
5. Configure:
   - **Batch Size**: `1`
   - Leave other options default
6. Click **"Execute Node"** to test

---

### Step 4: Add "Wait Between Messages" Node (1 minute)

1. Click on **"Loop Over Messages"** node
2. Click the **"+"** button
3. Search for **"Wait"** node
4. Name it: **"Wait Between Messages"**
5. Configure:
   - **Amount**: `1`
   - **Unit**: `seconds`
6. Click **"Execute Node"** to test

---

### Step 5: Update "Send Slack Notification" Node (2 minutes)

1. **Disconnect** existing connection from "AI Summarization" to "Send Slack Notification"
   - Click on the connection line
   - Press **Delete** key

2. **Connect** "Wait Between Messages" to "Send Slack Notification"
   - Drag from "Wait Between Messages" output to "Send Slack Notification" input

3. Click on **"Send Slack Notification"** node

4. Update **"Blocks UI"** field to:

   ```
   ={{JSON.stringify($json)}}
   ```

5. Click **"Execute Node"** to test

6. **Important**: Add loop-back connection
   - Drag from "Send Slack Notification" output back to "Loop Over Messages" input
   - This allows processing all messages in the batch

---

### Step 6: Keep Other Connections (1 minute)

Make sure these connections remain:

- ✅ AI Summarization → Store Latest State
- ✅ AI Summarization → Emails

These handle data storage and email notifications separately.

---

## 🧪 Testing the Updated Workflow

### Test 1: Manual Execution

1. Click **"Execute Workflow"** button
2. Watch the flow:
   - AI Summarization generates messages
   - Extract Messages parses the response
   - Loop processes each message
   - Wait adds 1-second delay
   - Slack sends each message
3. Check Slack channel - should see 1-3 messages

### Test 2: Check Message Quality

Each message should:

- ✅ Be under 2800 characters
- ✅ Have proper Slack blocks format
- ✅ Be independently readable
- ✅ Focus on specific topic (Recent Work, Core Status, or Upcoming)

### Test 3: Verify Data Flow

1. Click on each node
2. Check "Output" tab
3. Verify data structure matches expectations

---

## 📊 Expected Results

### If Recent Work Done (3 messages)

**Message 1**:

```
🚀 Recent Work Activity - 2025-12-05

3 updates in the last 48 hours

🎯 Course Management System (TOP PRIORITY)
• Module CRUD Implementation (6 hours ago)
  COMPLETED: Full implementation with 17 tests passing

📈 Overall Progress: 63% | 12/34 tasks complete
```

**Message 2**:

```
🎯 Core Platform Status

Course Management System (TOP PRIORITY) 🎉
█████████░ 89%
1 completed | 0 in progress | 4 planned

Events Management Platform 📋
░░░░░░░░░░ 0%
0 completed | 0 in progress | 2 planned
```

**Message 3**:

```
📅 Upcoming High-Priority Items

• Course Creation System
  🎯 Course Management System (TOP PRIORITY)
  ⏱️ Estimated: 1 week
  💡 Enable instructors to publish offerings
  📊 Complexity: Medium (5/10)
```

### If No Recent Work (2 messages)

- Message 1: Core Platform Status
- Message 2: Upcoming High-Priority Items

---

## 🔍 Troubleshooting

### Issue: AI returns single text instead of JSON

**Fix**: The system prompt explicitly requests JSON format. If this happens:

1. Check AI node model settings (should be GPT-4 or GPT-5-mini)
2. Verify system prompt is copied correctly
3. The Extract Messages node has fallback handling

### Issue: Messages not looping

**Fix**: Verify connections:

1. Extract Messages → Loop Over Messages
2. Loop → Wait
3. Wait → Slack
4. Slack → Loop (loop-back)

### Issue: Slack blocks error

**Fix**: Check Slack node configuration:

- Message Type: **Block**
- Blocks UI: `={{JSON.stringify($json)}}`

---

## ✅ Verification Checklist

- [ ] AI prompts updated with new system/user messages
- [ ] Extract Messages node added and tested
- [ ] Loop Over Messages node added (batch size = 1)
- [ ] Wait Between Messages node added (1 second)
- [ ] Slack node updated to use `$json` from loop
- [ ] Loop-back connection added (Slack → Loop)
- [ ] Other connections preserved (Store State, Emails)
- [ ] Test execution successful
- [ ] 1-3 messages delivered to Slack
- [ ] Messages under character limits
- [ ] Messages properly formatted

---

## 📚 Alternative: Use Pre-Built Messages

If AI generation is too complex, you can skip AI and use pre-built messages:

1. After "Extract Messages", add a Code node:

```javascript
// Use pre-built messages from smart reporter
const data = $("Move Binary to JSON").first().json;
return data.preBuiltMessages.map((msg) => ({ json: msg }));
```

2. Connect directly to Loop node
3. This bypasses AI customization but guarantees working messages

---

**Status**: Ready to implement
**Time**: ~10 minutes
**Complexity**: Low (mostly copy-paste)
**Benefit**: Multi-message support with recent activity tracking
