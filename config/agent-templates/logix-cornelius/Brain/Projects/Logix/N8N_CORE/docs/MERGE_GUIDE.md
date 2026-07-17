---
title: "Merging Split Messages in n8n"
date: "2026-04-11"
tags: ["project/logix", "tech/n8n", "topic/merge-guide"]
category: "projects/logix"
updated: "2026-07-15"
---

## Links

- [[Projects/Logix/N8N_CORE/N8N CORE|N8N Core README]]

# Merging Split Messages in n8n

## 🎯 Goal

Merge multiple split messages from "AI Summarization" node into a single message for "Markdown to HTML" plugin.

## ⚠️ Important: Slack Blocks Format

If your AI Summarization returns **Slack blocks format** (JSON with `messages`, `blocks`, etc.), you need to **extract the markdown first** before passing to Markdown to HTML plugin.

**Use the Code node with `extract-slack-markdown.js`** to convert Slack blocks to clean Markdown.

---

## ✅ Solution 1: Extract Slack Blocks to Markdown (For Your Case)

**Your AI Summarization returns Slack blocks format**, so you need to extract markdown first.

**Add a "Code" node between "AI Summarization" and "Markdown to HTML":**

1. Copy code from `extract-slack-markdown.js`
2. Paste into Code node
3. This will:
   - Extract markdown from all Slack blocks
   - Convert Slack markdown (`<em>`, `<code>`) to standard Markdown (`*`, `` ` ``)
   - Merge all messages
   - Output clean markdown

**Then in Markdown to HTML node:**

```javascript
{
  {
    $("Code").item.json.markdown;
  }
}
```

---

## ✅ Solution 2: Code Node (For Direct Markdown)

**Add a "Code" node between "AI Summarization" and "Markdown to HTML":**

```javascript
// Merge all message contents
const mergedContent = $input
  .all()
  .map((item) => item.json.message?.content || item.json.content || "")
  .filter((content) => content.length > 0)
  .join("\n\n---\n\n"); // Separator between parts

return [
  {
    json: {
      content: mergedContent,
    },
  },
];
```

**Then in Markdown to HTML node:**

```javascript
{
  {
    $("Code").item.json.content;
  }
}
```

---

## ✅ Solution 2: Inline Expression (Quick)

**Directly in the Markdown to HTML node:**

### Without Separator

```javascript
{
  {
    $("AI Summarization")
      .all()
      .map((i) => i.json.message?.content || i.json.content || "")
      .filter((c) => c)
      .join("\n\n");
  }
}
```

### With Separator

```javascript
{
  {
    $("AI Summarization")
      .all()
      .map((i) => i.json.message?.content || i.json.content || "")
      .filter((c) => c)
      .join("\n\n---\n\n");
  }
}
```

### With Page Break

```javascript
{
  {
    $("AI Summarization")
      .all()
      .map((i) => i.json.message.content)
      .join('\n\n<div style="page-break-after: always;"></div>\n\n');
  }
}
```

---

## ✅ Solution 3: Loop Node (For Large Messages)

If messages are extremely large, use "Loop Over Items" node:

1. **Loop Over Items** → Input: "AI Summarization"
2. **Set** node inside loop:
   - Append to variable: `{{ $vars.mergedContent || '' }} + {{ $json.message.content }} + '\n\n---\n\n'`
3. **Markdown to HTML** → After loop
   - Input: `{{ $vars.mergedContent }}`

---

## 📋 Workflow Structure

### For Slack Blocks Format (Your Case)

```
┌─────────────────────┐
│ AI Summarization    │ (Multiple items with Slack blocks)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Code: Extract       │ (Extract markdown from blocks)
│ extract-slack-      │ Output: clean markdown
│ markdown.js         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Markdown to HTML    │ (Converts markdown to HTML)
│ Input: {{ $('Code').item.json.markdown }}
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Send Email          │ (Use HTML output)
└─────────────────────┘
```

### For Direct Markdown Format

```
┌─────────────────────┐
│ AI Summarization    │ (Multiple items with markdown)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Markdown to HTML    │ (Merge + Convert)
│ Input: {{ $('AI Summarization').all().map(i => i.json.message.content).join('\n\n---\n\n') }}
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Send Email          │ (Use HTML output)
└─────────────────────┘
```

---

## 🎯 Quick Reference

### Merge with Newlines

```javascript
{
  {
    $("AI Summarization")
      .all()
      .map((i) => i.json.message.content)
      .join("\n\n");
  }
}
```

### Merge with Horizontal Rule

```javascript
{
  {
    $("AI Summarization")
      .all()
      .map((i) => i.json.message.content)
      .join("\n\n---\n\n");
  }
}
```

### Merge with Custom Separator

```javascript
{
  {
    $("AI Summarization")
      .all()
      .map((i) => i.json.message.content)
      .join("\n\n========== MESSAGE BREAK ==========\n\n");
  }
}
```

### Access Merged Content After Code Node

```javascript
{
  {
    $("Code").item.json.content;
  }
}
```

---

## ✅ Recommendation

Use **Code Node** approach for:

- ✅ Better debugging
- ✅ Easier to modify
- ✅ Can add logging
- ✅ Can handle errors
- ✅ Can truncate if needed

Use **Inline Expression** for:

- ⚡ Quick prototypes
- ⚡ Simple merges
- ⚡ No processing needed

---

## 🐛 Troubleshooting

### Problem: Output contains JSON instead of Markdown

**Symptoms:**

- Markdown to HTML shows: `<p>{"messages": [{"blocks": [...]}]}</p>`
- Code node output has JSON structure

**Solution:**

1. **Check Input Structure:**
   - Temporarily use `debug-input-structure.js` in Code node
   - See what AI Summarization is actually sending
   - Verify it contains `messages` or `blocks` structure

2. **Use V2 Version:**
   - Try `extract-slack-markdown-v2.js` which handles more edge cases
   - It automatically detects and parses JSON strings

3. **Verify Code Node Output:**
   - Check the `markdown` field in Code node output
   - Should be pure text starting with `#` or regular text
   - Should NOT start with `{` or `[`

4. **Check Node Name:**
   - Make sure Markdown to HTML references correct node name:

   ```javascript
   {
     {
       $("Extract Markdown").item.json.markdown;
     }
   }
   ```

   - Replace `'Extract Markdown'` with your actual Code node name

### Problem: Empty or No Output

**Check:**

- Does AI Summarization output have `messages` array?
- Does it have `blocks` array?
- Try the debug script to see structure

### Expected Output Format

**Good (Pure Markdown):**

```markdown
# 🚀 Recent Work Activity

_Key wins in the last 48 hours..._

• _Monolithic Architecture Migration_ — completed
• 76% size reduction...
```

**Bad (JSON):**

```json
{"messages": [{"blocks": [...]}]}
```

If you see JSON, the extraction didn't work - check input structure!
