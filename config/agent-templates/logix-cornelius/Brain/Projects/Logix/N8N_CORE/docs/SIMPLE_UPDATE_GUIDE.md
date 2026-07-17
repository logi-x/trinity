---
title: "✅ Simple N8N Workflow Update (Copy-Paste Method)"
date: "2026-04-11"
tags: ["project/logix", "tech/n8n", "topic/simple-update-guide"]
category: "projects/logix"
updated: "2026-07-15"
---

## Links

- [[Projects/Logix/N8N_CORE/N8N CORE|N8N Core README]]

# ✅ Simple N8N Workflow Update (Copy-Paste Method)

Since importing is tricky, here's a simple **copy-paste** approach that takes 10 minutes.

## 🎯 Goal

Update "Experts Notifications (clone)" to support multi-message delivery with recent activity tracking.

---

## 📋 Step 1: Update AI Prompts (5 minutes)

### 1.1 Open Workflow

1. Go to <https://n8n.dev.logi-x.org>
2. Open "Experts Notifications (clone)" workflow
3. Click on **"AI Summarization"** node

### 1.2 Update System Prompt

**In the Messages tab, System message field, replace with:**

```
You are a professional project communication specialist creating multi-message daily client updates.

🎯 PURPOSE: Transform project data into 1-3 separate Slack messages showing:
- Recent work (last 48h) - what was actually built
- Core functionality status - progress on 4 main features
- Upcoming priorities - next deliverables

🧱 OUTPUT REQUIREMENTS:

Generate 1-3 messages based on data.messageGeneration.messageCount

**MESSAGE 1: Recent Activity** (if data.recentActivity.hasActivity)
- Max 2800 chars
- Show timestamps and task titles
- Focus: Course Management, Events, Discussions, Posts

**MESSAGE 2: Core Status** (always)
- Max 2000 chars
- Progress bars: █ filled, ░ empty
- Course Management = TOP PRIORITY

**MESSAGE 3: Upcoming** (conditional)
- Max 2500 chars
- High-priority deliverables only
- Include complexity and estimates

**CRITICAL OUTPUT FORMAT:**
You MUST return valid JSON:

{
  "messages": [
    { "blocks": [...] },
    { "blocks": [...] }
  ]
}

Each message.blocks = array of Slack Block Kit elements
Each message < 2800 characters total
DO NOT return plain text. ONLY JSON.
```

### 1.3 Update User Prompt

**In the User message field, replace with:**

```
Generate {{ $('Move Binary to JSON').item.json.messageGeneration ? $('Move Binary to JSON').item.json.messageGeneration.messageCount : 1 }} Slack messages.

PROJECT CONTEXT:
- Phase: {{ $('Process Data').item.json.timeline.currentPhase }}
- Health: {{ $('Process Data').item.json.summaryData.status.health }}
- Progress: {{ $('Process Data').item.json.summaryData.status.progress }}

RECENT ACTIVITY (48h):
{{ $('Move Binary to JSON').item.json.recentActivity ? ($('Move Binary to JSON').item.json.recentActivity.hasActivity ? $('Move Binary to JSON').item.json.recentActivity.activities.map(a => '• ' + a.taskTitle + ' (' + a.age + '): ' + a.summary).join('\n') : 'No recent work') : 'Data not available' }}

CURRENT WORK:
{{ $('Process Data').item.json.summaryData.currentWork.map(w => '• ' + w.title + ' (' + w.timeline + ')').join('\n') }}

OUTLOOK:
Est. Completion: {{ $('Process Data').item.json.summaryData.outlook.timeline.date }}
Confidence: {{ $('Process Data').item.json.summaryData.outlook.timeline.confidence }}

---

RETURN JSON ONLY:
{
  "messages": [
    {
      "blocks": [
        {"type": "header", "text": {"type": "plain_text", "text": "🚀 Recent Work - {{ $now.format('yyyy-MM-dd') }}"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": "..."}}
      ]
    }
  ]
}

LIMITS:
- Each message < 2800 chars
- Course Management = TOP PRIORITY
- Use progress bars: █░
```

### 1.4 Save

Click **"Save"** button

---

## 📋 Step 2: Add "Extract Messages" Node (2 minutes)

### 2.1 Add Code Node

1. Click on **"AI Summarization"** node
2. Click the **"+"** icon that appears
3. Search for **"Code"**
4. Click to add
5. Name it: **"Extract Messages"**

### 2.2 Paste Code

**In the JavaScript Code field:**

```javascript
// Extract messages from AI JSON response
const aiResponse = $input.first().json;
let messages = [];

// Parse AI response
if (aiResponse.messages && Array.isArray(aiResponse.messages)) {
  messages = aiResponse.messages;
} else if (aiResponse.message && aiResponse.message.content) {
  try {
    const parsed =
      typeof aiResponse.message.content === "string"
        ? JSON.parse(aiResponse.message.content)
        : aiResponse.message.content;
    messages = parsed.messages || [];
  } catch (e) {
    console.error("Parse error:", e);
  }
}

// Fallback: single message with standard JS date formatting
if (!messages.length) {
  const now = new Date();
  const dateStr = now.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "2-digit",
    year: "numeric",
  });

  const content = aiResponse.message?.content || "No update available";
  const processData = $("Process Data").item.json;

  messages = [
    {
      blocks: [
        {
          type: "header",
          text: { type: "plain_text", text: "📊 Daily Update - " + dateStr },
        },
        {
          type: "section",
          fields: [
            {
              type: "mrkdwn",
              text:
                "*Progress:*\n" +
                (processData.summaryData?.status?.progress || "..."),
            },
            {
              type: "mrkdwn",
              text:
                "*Health:*\n🟢 " +
                (processData.summaryData?.status?.health || "Good"),
            },
          ],
        },
        { type: "section", text: { type: "mrkdwn", text: content } },
      ],
    },
  ];
}

return messages.map((msg, idx) => ({
  json: { ...msg, messageIndex: idx + 1, totalMessages: messages.length },
}));
```

### 2.3 Test

Click **"Test step"** - should output array of messages

---

## 📋 Step 3: Add Loop Node (1 minute)

### 3.1 Add Split In Batches

1. Click on **"Extract Messages"** node
2. Click **"+"** icon
3. Search for **"Split In Batches"**
4. Name it: **"Loop Over Messages"**

### 3.2 Configure

- **Batch Size**: `1`
- Leave defaults

---

## 📋 Step 4: Add Wait Node (1 minute)

1. Click on **"Loop Over Messages"**
2. Click **"+"** icon
3. Search for **"Wait"**
4. Name it: **"Wait Between Messages"**
5. Configure:
   - **Amount**: `1`
   - **Unit**: `seconds`

---

## 📋 Step 5: Update Slack Node (1 minute)

### 5.1 Remove Old Connection

1. Click on the connection line from **"AI Summarization"** to **"Send Slack Notification"**
2. Press **Delete** key

### 5.2 Connect Wait to Slack

1. Drag from **"Wait Between Messages"** output
2. Connect to **"Send Slack Notification"** input

### 5.3 Add Loop-Back Connection

1. Drag from **"Send Slack Notification"** output
2. Connect back to **"Loop Over Messages"** input
3. This creates the loop for processing all messages

### 5.4 Update Slack Configuration

1. Click on **"Send Slack Notification"** node

2. **Message Type**: Keep as `block`

3. **Text** field (fallback - required by Slack):

   ```
   ={{ $json.text }}
   ```

4. **Blocks UI** field (⚠️ CRITICAL - NO JSON.stringify!):

   ```
   ={{ $json.blocks }}
   ```

**IMPORTANT**:

- Use `$json.blocks` directly - it's already an array!
- DON'T use `JSON.stringify($json.blocks)` - that makes Slack ignore blocks and only show text!

**Note**: Slack requires both `text` (fallback) and `blocks` (rich formatting)

---

## ✅ Step 6: Test Everything (2 minutes)

### 6.1 Execute Workflow

1. Click **"Execute Workflow"** button at top
2. Watch the nodes light up

### 6.2 Expected Flow

```
Read Report → Process → AI (generates JSON)
              ↓
Store State / Emails (parallel)
              ↓
Extract Messages (parse JSON)
              ↓
Loop Over Messages (start iteration)
              ↓
Wait 1 Second
              ↓
Send to Slack → (loop back until all messages sent)
```

### 6.3 Check Slack

You should see **1-3 messages** appear:

- Message 1: Recent work (if any work done in 48h)
- Message 2: Core platform status (always)
- Message 3: Upcoming priorities (conditional)

---

## 🎯 Final Connections Diagram

```
AI Summarization
    ├─→ Store Latest State
    ├─→ Emails
    └─→ Extract Messages
            └─→ Loop Over Messages ←─┐
                    └─→ Wait          │
                        └─→ Slack ────┘
```

---

## 🧪 Verification

After executing:

- [ ] AI node output has `messages` array
- [ ] Extract node outputs multiple items
- [ ] Loop processes one message at a time
- [ ] 1-second delay between Slack posts
- [ ] All messages delivered to Slack channel
- [ ] Messages under 2800 chars each
- [ ] Recent work shown (if applicable)
- [ ] 4 main functionalities prominent

---

## 💡 Quick Troubleshooting

**AI returns text instead of JSON**:

- Check AI model (should be GPT-4/5-mini)
- System prompt emphasizes JSON output
- Extract Messages has fallback

**Loop doesn't work**:

- Verify loop-back connection (Slack → Loop)
- Check batch size = 1

**Slack blocks error**:

- Blocks UI should be: `={{ JSON.stringify($json.blocks) }}`
- Not: `=$json` or `=$json.blocks`

---

**Time**: 10 minutes total
**Difficulty**: Easy (copy-paste)
**Result**: Multi-message Slack delivery with recent activity tracking
