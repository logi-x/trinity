---
title: "Markdown to HTML Conversion for n8n Email"
date: "2026-04-11"
tags: ["project/logix", "tech/n8n", "topic/markdown-to-html-inline"]
category: "projects/logix"
updated: "2026-07-15"
---

## Links

- [[Projects/Logix/N8N_CORE/N8N CORE|N8N Core README]]

# Markdown to HTML Conversion for n8n Email

## 🎯 Solutions

### Option 1: Using Code Node (Recommended)

**Add a "Code" node after "AI Summarization":**

Copy the code from `merge-and-convert-markdown.js` into the Code node.

**Then in Email node:**

```javascript
{
  {
    $("Code").item.json.htmlContent;
  }
}
```

---

### Option 2: Inline Expression (Quick & Simple)

**For merging multiple items:**

```javascript
{
  {
    $("AI Summarization")
      .all()
      .map((item) => item.json.message?.content || item.json.content || "")
      .join("\n\n---\n\n")
      .replace(/\n/g, "<br>");
  }
}
```

---

### Option 3: Advanced Inline (Markdown Conversion)

```javascript
{
  {
    // Merge all messages
    const merged = $("AI Summarization")
      .all()
      .map((item) => item.json.message?.content || item.json.content || "")
      .join("\n\n---\n\n");

    // Convert Markdown to HTML
    let html = merged;

    // Headers
    html = html.replace(/^### (.*$)/gim, "<h3>$1</h3>");
    html = html.replace(/^## (.*$)/gim, "<h2>$1</h2>");
    html = html.replace(/^# (.*$)/gim, "<h1>$1</h1>");

    // Bold & Italic
    html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/\*(.+?)\*/g, "<em>$1</em>");

    // Code
    html = html.replace(/`(.+?)`/g, "<code>$1</code>");

    // Links
    html = html.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>');

    // Lists
    html = html.replace(/^[\*\-] (.+)$/gim, "<li>$1</li>");
    html = html.replace(/(<li>.*<\/li>\n?)+/g, "<ul>$&</ul>");

    // Line breaks
    html = html.replace(/\n\n/g, "</p><p>");
    html = html.replace(/\n/g, "<br>");

    return "<p>" + html + "</p>";
  }
}
```

---

### Option 4: Use External Library (Best Quality)

**Install in n8n:**

```bash
npm install marked
```

**In Code node:**

```javascript
const { marked } = require("marked");

// Merge messages
const merged = $input
  .all()
  .map((item) => item.json.message?.content || item.json.content || "")
  .join("\n\n---\n\n");

// Convert to HTML
const html = marked(merged);

return [
  {
    json: {
      htmlContent: html,
      plainText: merged,
    },
  },
];
```

---

## 📧 Email Node Configuration

### Subject

```javascript
Report Generated - {{ $now.format('MMMM DD, YYYY') }}
```

### Body (HTML)

```javascript
{
  {
    $("Code").item.json.htmlContent;
  }
}
```

### Alternative (if using inline)

```javascript
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; }
    h1 { color: #333; }
    h2 { color: #666; }
    code { background: #f4f4f4; padding: 2px 5px; }
  </style>
</head>
<body>
  {{ /* Your inline expression here */ }}
</body>
</html>
```

---

## 🎨 Email Styling Tips

### Inline Styles (Better for Email Clients)

```html
<h1 style="color: #2c3e50; border-bottom: 3px solid #3498db;">Title</h1>
<p style="margin: 15px 0; line-height: 1.6;">Content</p>
```

### Safe Email Fonts

- Arial, Helvetica, sans-serif
- Georgia, serif
- 'Courier New', Courier, monospace
- Tahoma, Verdana, sans-serif

### Color Palette (Professional)

- Primary: `#3498db` (Blue)
- Headers: `#2c3e50` (Dark Blue)
- Text: `#333333` (Dark Gray)
- Background: `#f9f9f9` (Light Gray)
- Borders: `#ecf0f1` (Pale Gray)

---

## 🧪 Testing

Test your HTML email at:

- <https://putsmail.com>
- <https://www.mail-tester.com>
- Send to yourself first!

---

## ⚡ Quick Reference

**Merge only:**

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

**Merge + Basic HTML:**

```javascript
{
  {
    $("AI Summarization")
      .all()
      .map((i) => i.json.message.content)
      .join("<hr>")
      .replace(/\n/g, "<br>");
  }
}
```

**Merge + Styled:**

```html
<div style="max-width: 800px; margin: 0 auto; padding: 20px; background: #fff;">
  {{ $('AI Summarization').all().map(i => i.json.message.content).join('
  <hr style="margin: 30px 0;" />
  ').replace(/\n/g, '<br />') }}
</div>
```
