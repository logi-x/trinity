---
title: "🔍 Debugging analyze-changes.js"
date: "2026-04-11"
tags: ["project/logix", "tech/n8n", "topic/debugging-guide"]
category: "projects/logix"
updated: "2026-07-15"
---

## Links

- [[Projects/Logix/N8N_CORE/N8N CORE|N8N Core README]]

# 🔍 Debugging analyze-changes.js

## Problem

Getting incorrect output:

```json
{"progressChange":-63,"progressDelta":-63,...}
```

This means `currentProgress = 0` instead of `63`, suggesting the data isn't being read correctly.

---

## Quick Fix Steps

### Step 1: Use Debug Version

1. In N8N workflow, temporarily replace the code in the "Analyze Changes" node with the contents of:

   ```
   .taskmaster/.n8n/analyze-changes-DEBUG.js
   ```

2. Run the workflow and check the **console output** in N8N

3. You'll see something like:

   ```
   ═══════════════════════════════════════
   🔍 ANALYZE-CHANGES DEBUG OUTPUT
   ═══════════════════════════════════════

   1️⃣ DATA SOURCE: Process Data1

   2️⃣ CURRENT DATA KEYS: [...]

   3️⃣ CURRENT STRUCTURE:
   {
     "hasStatus": true,
     "statusProgress": "63%",
     ...
   }
   ```

---

### Step 2: Identify the Issue

Common issues:

| Problem             | Debug Output Shows           | Fix                                  |
| ------------------- | ---------------------------- | ------------------------------------ |
| **Wrong node name** | `DATA SOURCE: $input.last()` | Update node name in workflow or code |
| **Missing data**    | `statusProgress: null`       | Check "Process Data" node output     |
| **Wrong structure** | `hasStatus: false`           | Data is nested differently           |

---

### Step 3: Apply Fix

Based on debug output, the fixed `analyze-changes.js` should now handle:

✅ Multiple node name variants (Process Data, Process Data1)
✅ Multiple data structure variants (status.progress, summaryData.status.progress)
✅ Robust extraction with fallbacks

If debug shows the data exists but isn't being extracted, share the debug output.

---

## Manual Quick Check

In N8N, add a **Code node** before "Analyze Changes":

```javascript
const data = $input.first().json;

console.log("Keys:", Object.keys(data));
console.log("Progress:", data.status?.progress || "NOT FOUND");

return $input.all();
```

This will show you exactly what structure is being passed.

---

## Most Likely Issue

The "Process Data" node might have a different name in your workflow (like "Process Data1").

The fixed code now tries:

1. `$("Process Data")`
2. `$("Process Data1")`
3. `$input.last()` (fallback)

If your node has a different name, you can either:

- Rename it to "Process Data" in N8N
- Or update line 3 of analyze-changes.js to match your node name
