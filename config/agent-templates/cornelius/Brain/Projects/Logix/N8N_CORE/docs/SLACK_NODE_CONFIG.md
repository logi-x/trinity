---
title: "📤 Slack Node Configuration"
date: "2026-04-11"
tags: ["project/logix", "tech/n8n", "topic/slack-node-config"]
category: "projects/logix"
updated: "2026-07-15"
---

## Links

- [[Projects/Logix/N8N_CORE/N8N CORE|N8N Core README]]

# 📤 Slack Node Configuration

## ⚠️ Important: Both Text AND Blocks Required

Slack API requires **both** fields:

1. `text` - Fallback for notifications (plain text)
2. `blocks` - Rich formatting (Block Kit)

## ✅ Correct Configuration

### In "Send Slack Notification" Node

**Message Type**: `block` (NOT `text`)

**Text** field:

```
={{ $json.text }}
```

**Blocks UI** field:

```
={{ $json.blocks }}
```

**NOT** `={{ JSON.stringify($json.blocks) }}` - Already an array!

---

## 🔍 What $json Contains

After the Extract Messages node, each item in the loop has:

```json
{
  "text": "🚀 Recent Work Activity - 2025-12-06",
  "blocks": [
    {"type": "header", ...},
    {"type": "section", ...}
  ],
  "messageIndex": 1,
  "totalMessages": 3
}
```

## 🎯 Slack Node Should Use

- **Text**: `$json.text` (for notification preview)
- **Blocks**: `$json.blocks` (for rich formatting)

**The blocks field is ALREADY an array** - don't stringify it again!

---

## ❌ Common Mistakes

### Mistake 1: Stringifying blocks

```
❌ Blocks UI: ={{ JSON.stringify($json.blocks) }}
✅ Blocks UI: ={{ $json.blocks }}
```

### Mistake 2: Missing text field

```
❌ Text: (empty)
✅ Text: ={{ $json.text }}
```

### Mistake 3: Wrong message type

```
❌ Message Type: text
✅ Message Type: block
```

---

## 🧪 Testing

### Check Extract Messages Output

Click "Extract Messages" node → Output tab:

```json
{
  "text": "🚀 Recent Work Activity - 2025-12-06",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🚀 Recent Work Activity - 2025-12-06"
      }
    },
    { "type": "section", "text": { "type": "mrkdwn", "text": "..." } }
  ],
  "messageIndex": 1,
  "totalMessages": 3
}
```

### Verify Slack Node Receives

Click "Send Slack Notification" → Input tab:

- ✅ Should see `text` field
- ✅ Should see `blocks` array
- ✅ messageIndex and totalMessages for debugging

---

## 📋 Quick Fix Checklist

- [ ] Message Type = `block`
- [ ] Text field = `={{ $json.text }}`
- [ ] Blocks UI field = `={{ $json.blocks }}` (NO JSON.stringify!)
- [ ] Test node execution
- [ ] Verify blocks render in Slack (not just text)

---

**Key Point**: `$json.blocks` is already an array - Slack node expects it as-is, not stringified!
