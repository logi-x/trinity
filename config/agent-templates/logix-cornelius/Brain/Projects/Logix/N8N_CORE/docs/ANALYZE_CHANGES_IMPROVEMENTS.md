---
title: "📊 Analyze Changes Enhancement"
date: "2026-04-11"
tags: ["project/logix", "tech/n8n", "topic/analyze-changes-improvements"]
category: "projects/logix"
updated: "2026-07-15"
---

## Links

- [[Projects/Logix/N8N_CORE/N8N CORE|N8N Core README]]

# 📊 Analyze Changes Enhancement

## What Changed

Simplified the change detection logic from **155 lines** to **~80 lines** of cleaner, more maintainable code.

---

## Key Improvements

### 1. **Simplified Data Access**

**Before:**

```javascript
const raw_data = JSON.parse($input.last().json.raw_data);
const previousProgress = parseFloat(
  raw_data.insights?.progress?.replace("% complete", "") || 0,
);
const previousAccomplishments =
  raw_data?.summaryData?.achievements?.map((a) => a.title) || [];
```

**After:**

```javascript
const previousRow = $input.first().json;
const previousProgress = parseFloat(previousRow.overall_progress * 100 || 0);
const previousAccomplishments = parseList(previousRow.accomplishments);
```

✅ Direct access to Google Sheets columns (no deep nesting)

---

### 2. **Clearer Change Detection**

```javascript
// Progress (numeric comparison)
const progressDelta = currentProgress - previousProgress;
changes.progressDelta = progressDelta;

// Accomplishments (array diff)
changes.newAccomplishments = currentAccomplishments.filter(
  (title) => !previousAccomplishments.includes(title)
);

// Status changes (simple equality)
if (currentHealth !== previousHealth) {
  changes.statusChanges.push({...});
}
```

✅ Clear, predictable comparison logic

---

### 3. **Significance Threshold**

```javascript
changes.hasSignificantChanges =
  Math.abs(progressDelta) >= 1 || // 1%+ progress
  changes.newAccomplishments.length > 0 || // New work delivered
  changes.statusChanges.length > 0; // Status shifts
```

✅ Only flag meaningful updates (reduces noise)

---

### 4. **AI-Ready Summary**

```javascript
comparisonSummary: "1 new accomplishment(s), 2.0% progress change, 2 status change(s)";
```

✅ Human-readable change context for AI prompts

---

## Example Output

### Scenario: Progress + New Accomplishments + Timeline Shift

```json
{
  "changes": {
    "progressChange": 2,
    "progressDelta": 2,
    "newAccomplishments": ["Smart Client Reporting System"],
    "statusChanges": [
      {
        "type": "momentum",
        "from": "strong",
        "to": "accelerating",
        "label": "Development Momentum"
      },
      {
        "type": "timeline",
        "from": "2025-12-15",
        "to": "2025-12-12",
        "label": "Estimated Completion"
      }
    ],
    "hasSignificantChanges": true
  },
  "comparisonSummary": "1 new accomplishment(s), 2.0% progress change, 2 status change(s)"
}
```

---

## What Gets Detected

| Change Type         | Threshold      | Example                    |
| ------------------- | -------------- | -------------------------- |
| **Progress**        | ≥1% change     | 63% → 65% ✅               |
| **Accomplishments** | Any new        | "Smart Reporting" added ✅ |
| **Health**          | Any change     | good → excellent ✅        |
| **Momentum**        | Any change     | steady → accelerating ✅   |
| **Timeline**        | Any date shift | 2025-12-15 → 2025-12-12 ✅ |

---

## Benefits

1. ✅ **Clearer**: Direct column access, no deep nesting
2. ✅ **Faster**: No repeated JSON parsing
3. ✅ **Maintainable**: Simple comparison logic
4. ✅ **Reliable**: Works with actual Google Sheets structure
5. ✅ **AI-Friendly**: Provides context-rich summaries

---

**Updated**: 2025-12-06
**Status**: ✅ Tested and working
