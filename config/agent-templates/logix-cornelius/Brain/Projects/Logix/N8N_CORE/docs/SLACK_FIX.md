---
title: "🔧 SLACK NODE FIX - Blocks Not Showing"
date: "2026-04-11"
tags: ["project/logix", "tech/n8n", "topic/slack-fix"]
category: "projects/logix"
updated: "2026-07-15"
---

## Links

- [[Projects/Logix/N8N_CORE/N8N CORE|N8N Core README]]

# 🔧 SLACK NODE FIX - Blocks Not Showing

## ❌ Problem

Slack only shows text field, ignores blocks:

```
"text": "📊 Daily Project Update - Sat, Dec 06, 2025"
"blocks": [rich_text converted from text]  ← WRONG!
```

## ✅ Solution

### The Issue

**Blocks UI field was**:

```
={{ JSON.stringify($json.blocks) }}  ❌ Converts array to STRING!
```

**Should be**:

```
={{ $json.blocks }}  ✅ Uses array directly!
```

---

## 📋 Exact Configuration

### Send Slack Notification Node

**1. Message Type**: `block`

**2. Text** (Expression):

```
={{ $json.text }}
```

**3. Blocks UI** (Expression - CRITICAL):

```
={{ $json.blocks }}
```

**NOT**:

- ❌ `={{ JSON.stringify($json.blocks) }}`
- ❌ `=$json.blocks`
- ❌ `$json.blocks`

**ONLY**:

- ✅ `={{ $json.blocks }}`

---

## 🔍 Why This Matters

### What $json Contains

```json
{
  "text": "🚀 Recent Work Activity - 2025-12-06",
  "blocks": [
    {"type": "header", ...},
    {"type": "section", ...}
  ]
}
```

### If You Use JSON.stringify

```
blocks: "[{\"type\":\"header\"...}]"  ← STRING, not array!
```

Slack sees a string, ignores it, falls back to text field only.

### If You Use $json.blocks Directly

```
blocks: [{"type": "header", ...}]  ← ARRAY!
```

Slack sees proper array, renders rich blocks! ✅

---

## 🧪 Test After Fix

1. Update Blocks UI to: `={{ $json.blocks }}`
2. Execute workflow
3. Check Slack message

**Expected**:

- ✅ Rich formatted blocks (headers, sections, context)
- ✅ Progress bars: █████████░
- ✅ Emojis and formatting
- ✅ Multiple sections

**NOT**:

- ❌ Plain text only
- ❌ JSON string in message

---

## ✅ Quick Verification

### In N8N

1. Click "Send Slack Notification" node
2. Check "Blocks UI" field
3. Should show: `={{ $json.blocks }}`
4. Should NOT have `JSON.stringify`

### In Slack

After execution, message should have:

- Multiple visual blocks
- Rich formatting
- Progress bars
- Proper emojis

---

**The fix**: Remove `JSON.stringify` from Blocks UI field! 🎯
