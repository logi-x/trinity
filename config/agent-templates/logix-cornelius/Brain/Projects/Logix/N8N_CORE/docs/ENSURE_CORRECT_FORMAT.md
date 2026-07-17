---
title: "🎯 Ensure AI Generates Correct Format Every Time"
date: "2026-04-11"
tags: ["project/logix", "tech/n8n", "topic/ensure-correct-format"]
category: "projects/logix"
updated: "2026-07-15"
---

## Links

- [[Projects/Logix/N8N_CORE/N8N CORE|N8N Core README]]

# 🎯 Ensure AI Generates Correct Format Every Time

## 🔍 Issue Analysis

Both your examples show the AI returning the **same format** - JSON in `message.content` as a string. This is actually **correct** for OpenAI API!

The difference might be in **content quality**, not structure.

## ✅ 3-Layer Validation Strategy

### Layer 1: Strict System Prompt

**File**: `ai-system-prompt-strict.txt`

**Use This Updated Prompt** in your AI Summarization node:

```
You are a JSON-generating API for client project updates. You ONLY return valid JSON.

REQUIRED OUTPUT:
{
  "messages": [
    {"blocks": [...]},
    {"blocks": [...]}
  ]
}

FORBIDDEN:
- Plain text
- Explanations
- Anything except JSON

If you return anything other than valid JSON, you have failed.
```

**Why**: Makes it crystal clear - JSON only, no exceptions.

---

### Layer 2: JSON Mode (If Available)

**In AI Summarization Node:**

Check if there's an **"Options"** or **"Additional Fields"** section:

- Look for **"Response Format"** or **"JSON Mode"**
- If available, set to: `json_object` or `JSON`
- This forces OpenAI to return valid JSON

**Example** (if available in your N8N version):

```json
{
  "response_format": {
    "type": "json_object"
  }
}
```

---

### Layer 3: Validation Node

**Add BEFORE Extract Messages:**

1. After "AI Summarization", add new **Code** node
2. Name it: **"Validate AI Output"**
3. Paste code from `VALIDATE_AI_OUTPUT_NODE.js`

**What it does**:

- ✅ Validates message.content exists
- ✅ Validates JSON is parseable
- ✅ Validates messages array exists
- ✅ Validates each message has blocks
- ❌ Throws error if validation fails (stops workflow)

**Benefit**: Catches AI format issues immediately, prevents bad data from reaching Slack.

---

## 🔧 Updated Workflow

```
AI Summarization
    ↓
Validate AI Output (NEW!)
    ↓
Extract Messages
    ↓
Loop Over Messages
    ↓
Wait
    ↓
Slack
```

---

## 📋 Implementation Steps

### Step 1: Update AI System Prompt (2 min)

1. Open "AI Summarization" node
2. Replace System message with content from `ai-system-prompt-strict.txt`
3. Save

### Step 2: Enable JSON Mode (1 min - if available)

1. In "AI Summarization" node, check for:
   - "Options" dropdown
   - "Additional Fields"
   - "Response Format" setting
2. If found, set to `json_object`
3. Save

### Step 3: Add Validation Node (2 min)

1. After "AI Summarization", add Code node
2. Name: "Validate AI Output"
3. Paste code from `VALIDATE_AI_OUTPUT_NODE.js`
4. Connect: AI Summarization → Validate → Extract Messages
5. Test

---

## 🧪 Testing

### Test 1: Validation Passes

```
AI Summarization → Validate AI Output (logs)
✅ AI output validation passed
✅ Messages count: 3
✅ Structure: Message 1: 3 blocks, Message 2: 2 blocks, Message 3: 2 blocks
```

### Test 2: Validation Catches Errors

If AI returns bad format:

```
❌ Validation failed:
- AI output validation failed:
- message.content is not valid JSON
```

Workflow stops, you see error in logs.

### Test 3: Messages Delivered

```
Extract Messages → outputs 3 items
Loop → processes each
Slack → delivers all 3 with rich blocks
```

---

## 🎯 Why This Works

### Multiple Safeguards

1. **Strict Prompt**: AI knows ONLY JSON is acceptable
2. **JSON Mode** (if available): Forces OpenAI to return valid JSON
3. **Validation**: Catches any issues before they cause problems
4. **Extract Messages**: Robust parsing with fallbacks

### Result

- ✅ Consistent JSON format
- ✅ Errors caught early
- ✅ Workflow fails gracefully if AI misbehaves
- ✅ Rich blocks always delivered

---

## 📊 Expected AI Output

**Always This Structure**:

```json
{
  "message": {
    "role": "assistant",
    "content": "{\"messages\":[{\"blocks\":[...]},{\"blocks\":[...]}]}"
  }
}
```

**Parse Flow**:

1. Extract: `aiResponse.message.content`
2. Parse: `JSON.parse(content)`
3. Result: `{messages: [{blocks: [...]}, ...]}`
4. Use: `parsed.messages` array

---

## 🚀 Deployment

### Quick (5 min)

1. Update AI system prompt (strict version)
2. Test workflow
3. Verify JSON format

### Complete (10 min)

1. Update AI system prompt
2. Enable JSON mode (if available)
3. Add validation node
4. Test thoroughly
5. Deploy

---

**Files**:

- `ai-system-prompt-strict.txt` - Strict JSON-only prompt
- `VALIDATE_AI_OUTPUT_NODE.js` - Validation code
- `ENSURE_CORRECT_FORMAT.md` - This guide

**Result**: Reliable, consistent JSON generation every time! 🎯
