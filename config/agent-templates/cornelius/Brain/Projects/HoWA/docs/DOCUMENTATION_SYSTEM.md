---
title: "📚 Documentation System"
date: "2026-04-11"
tags: ["project/howa", "docs/howa"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# 📚 Documentation System

## Quick Access

- **Documentation Portal:** `/docs`
- **ETF Documentation:** `/etf/docs`
- **Refund Guide:** `/docs/refund-overview`
- **Quick Reference:** `/docs/quick-reference`

---

## Architecture

```
User clicks /docs
    ↓
DocsController::index()
    ↓
Renders: docs/index.tsx
    └─ Search & browse docs

User clicks doc card
    ↓
DocsController::show($slug)
    ↓
Renders: docs/show.tsx
    ├─ Loads content from content/{slug}.ts
    └─ Passes to doc-page.tsx
        ├─ MarkdownPreview renders content
        └─ useHashNavigation() handles scrolling
```

---

## Components

### 1. Reusable Hook

**`use-hash-navigation.tsx`** (80 lines)

- Used by ALL documentation pages
- Handles smooth scrolling
- No code duplication

### 2. Documentation Index

**`docs/index.tsx`** (180 lines)

- Categorized docs
- Search functionality
- Responsive cards

### 3. Document Template

**`docs/doc-page.tsx`** (90 lines)

- Markdown rendering
- Theme support
- Consistent layout

### 4. Content Library

**`docs/content/*.ts`** (6 files, ~1,300 lines)

- Client-friendly markdown
- No technical jargon
- Real examples

---

## Adding New Documentation

**3 Simple Steps:**

1. Create content file:

   ```typescript
   // content/my-doc.ts
   export const myDocContent = `# Title...`;
   ```

2. Import in show.tsx:

   ```typescript
   import { myDocContent } from "./content/my-doc";
   const contentMap = {
     "my-doc": myDocContent,
   };
   ```

3. Add to DocsController.php:
   ```php
   'my-doc' => [
     'title' => 'My Doc',
     'description' => 'Description',
     'component' => 'my-doc',
   ],
   ```

**Done!** Your doc is live at `/docs/my-doc`

---

## Current Documentation

### ETF System (3 docs)

- ETF Overview
- Real Data Integration
- Auto-Update System (planned)

### Refund System (3 docs)

- Refund Overview
- Dashboard Integration
- Processing Guide

### Reference (1 doc)

- Quick Reference

**Total: 6 comprehensive documentation pages**

---

**Status: ✅ Production Ready**
**Deployment: Ready to use**
**Scalability: Add unlimited docs easily**
