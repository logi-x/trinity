---
title: "Smart Reporting System Architecture"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/taskmaster"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Smart Reporting System Architecture

## 🏗️ System Overview

The Smart Client Reporting System is a three-layer architecture that transforms TaskMaster data into intelligent, multi-message Slack notifications with recent activity tracking.

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TASKMASTER DATA LAYER                        │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  tasks.json (12 tags with tasks)                               │ │
│  │  Each task contains:                                            │ │
│  │  • Basic fields (id, title, description, status, priority)     │ │
│  │  • details field with <info added on TIMESTAMP> blocks         │ │
│  │  • subtasks array with nested info blocks                      │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      PROCESSING LAYER                                │
│                                                                      │
│  ┌──────────────────────────┐  ┌────────────────────────────────┐  │
│  │ recent-activity-tracker  │  │ enhanced-client-report          │  │
│  │ .js                      │  │ .js                             │  │
│  └──────────────────────────┘  └────────────────────────────────┘  │
│           │                                    │                     │
│           │ Scans task details                │ Generates full      │
│           │ Extracts <info added>             │ report structure    │
│           │ Filters by timestamp              │ Calculates metrics  │
│           │ Summarizes content                │ Analyzes complexity │
│           │                                    │                     │
│           ▼                                    ▼                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │            Recent Activity JSON                             │   │
│  │  {                                                           │   │
│  │    activities: [...],    // Timestamped updates             │   │
│  │    summaryByDomain: {...}, // Grouped by domain             │   │
│  │    totalUpdates: N       // Count                           │   │
│  │  }                                                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│           │                                                         │
│           └──────────────────┬──────────────────────────────────┘  │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │          smart-client-reporter.js                           │   │
│  │  Combines:                                                   │   │
│  │  • Recent activity data                                      │   │
│  │  • Enhanced report data                                      │   │
│  │  • Character limit logic                                     │   │
│  │  • Message splitting algorithm                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       OUTPUT LAYER                                   │
│                                                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │   Message 1     │  │   Message 2     │  │   Message 3     │     │
│  │                 │  │                 │  │                 │     │
│  │ Recent Activity │  │  Core Status    │  │ Upcoming Work   │     │
│  │ (if any)        │  │  (always)       │  │ (conditional)   │     │
│  │                 │  │                 │  │                 │     │
│  │ < 2800 chars    │  │ < 2000 chars    │  │ < 2500 chars    │     │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘     │
│         │                     │                     │                │
│         └─────────────────────┴─────────────────────┘                │
│                               ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │         automation-orchestrator.js                          │   │
│  │  • Adds 1-second delay between messages                     │   │
│  │  • Logs each message send                                   │   │
│  │  • Handles errors with retries                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                         ┌─────────────┐
                         │    SLACK    │
                         │  (Client    │
                         │   Channel)  │
                         └─────────────┘
```

## 🔄 Data Flow Details

### Step 1: Activity Extraction

**recent-activity-tracker.js**:

```javascript
Input:  tasks.json (all domains)
        ↓
Scan:   All task.details and subtask.details fields
        ↓
Find:   <info added on 2025-12-05T10:30:00Z>...</info>
        ↓
Filter: Only activities from last 48 hours
        ↓
Extract: • Timestamp
         • Task ID & title
         • Content summary
         • Domain
        ↓
Output: Recent activity JSON grouped by domain
```

### Step 2: Report Generation

**enhanced-client-report.js**:

```javascript
Input:  tasks.json + weekly-report (if exists)
        ↓
Process: • Calculate progress metrics
         • Assess complexity (from TaskMaster reports)
         • Identify risks
         • Generate predictions
         • Extract accomplishments
        ↓
Output: Full enhanced report with:
        • rawTaskData (AI-friendly structure)
        • executiveSummary (key insights)
        • progressMetrics (trends)
        • deliveryPredictions (timeline)
        • aiContext (for N8N integration)
```

### Step 3: Smart Message Building

**smart-client-reporter.js**:

```javascript
Input:  • Recent activity JSON
        • Enhanced report data
        ↓
Prioritize: 4 main functionalities:
            1. course-management (CRITICAL)
            2. events-management (HIGH)
            3. community-discussions (HIGH)
            4. community-posts (HIGH)
        ↓
Build Messages:
        ┌────────────────────────────────┐
        │ Message 1: Recent Activity     │
        │ • Only if hasActivity = true   │
        │ • Shows work from last 48h     │
        │ • Priority domains first       │
        │ • Max 2800 characters          │
        └────────────────────────────────┘
        ┌────────────────────────────────┐
        │ Message 2: Core Status         │
        │ • Always sent                  │
        │ • 4 main functionalities       │
        │ • Progress bars                │
        │ • Recent milestones            │
        └────────────────────────────────┘
        ┌────────────────────────────────┐
        │ Message 3: Detailed Progress   │
        │ • If no recent activity OR     │
        │ • If risks detected            │
        │ • High-priority upcoming       │
        │ • Complexity insights          │
        └────────────────────────────────┘
        ↓
Output: Array of 1-3 Slack message objects
```

### Step 4: Delivery Orchestration

**automation-orchestrator.js**:

```javascript
Input:  Smart report with slackMessages array
        ↓
Process: For each message in array:
         1. Send to Slack webhook
         2. Wait 1 second
         3. Log success/failure
         4. Continue to next
        ↓
Output: Sequenced delivery to Slack
        Comprehensive logs
        N8N webhook trigger (parallel)
```

## 🧩 Component Breakdown

### Recent Activity Tracker

**Purpose**: Extract recent work from task details

**Key Functions**:

- `extractRecentActivity(hoursBack)` - Main extraction logic
- `extractInfoBlocks(detailsText, ...)` - Parse <info added> blocks
- `summarizeInfoBlock(content)` - Create concise summaries
- `formatForSlack(recentActivity, maxLength)` - Slack formatting

**Output Format**:

```json
{
  "timestamp": "2025-12-05T21:00:00Z",
  "hoursScanned": 48,
  "totalUpdates": 3,
  "activities": [
    {
      "type": "info_update",
      "taskId": "1.2",
      "taskTitle": "Extend Course API",
      "domain": "course-management",
      "timestamp": "2025-12-05T10:00:00Z",
      "content": "COMPLETED: Module CRUD; 17 tests passing",
      "age": "11 hours ago"
    }
  ],
  "summaryByDomain": {
    "course-management": {
      "domain": "Course Management System",
      "activities": [...],
      "count": 2
    }
  }
}
```

### Smart Client Reporter

**Purpose**: Combine recent activity with enhanced report and create smart messages

**Key Functions**:

- `generateSmartReport()` - Main orchestration
- `createSmartSlackMessages(...)` - Build message sequence
- `createRecentActivityMessage(...)` - Message 1
- `createCoreFunctionalityMessage(...)` - Message 2
- `createDetailedProgressMessage(...)` - Message 3 (conditional)

**Message Decision Logic**:

```javascript
hasRecentActivity = recentActivity.totalUpdates > 0
hasRisks = baseReport.riskIndicators.length > 1

Messages = []

if (hasRecentActivity) {
  Messages.push(RecentActivityMessage)
}

Messages.push(CoreFunctionalityMessage) // Always

if (!hasRecentActivity OR hasRisks) {
  Messages.push(DetailedProgressMessage)
}

return Messages // 1-3 messages
```

### Enhanced Client Reporter

**Purpose**: Generate comprehensive report data with predictions

**Key Functions**:

- `generateEnhancedClientReport()` - Main report generation
- `prepareRawDataForAI(tasks)` - Clean data for AI
- `generateExecutiveSummary(...)` - Key insights
- `generateProgressMetrics(...)` - Trend analysis
- `generateDeliveryPredictions(...)` - Timeline estimates
- `getTaskComplexity(taskId, tag)` - From complexity reports

**Complexity Integration**:

```javascript
// Reads TaskMaster complexity reports
.taskmaster/reports/task-complexity-report_TAGNAME.json

// Extracts:
{
  score: 8,              // 1-10 complexity
  recommendedSubtasks: 6, // Suggested breakdown
  reasoning: "...",      // Why this score
  estimatedWeeks: 4      // Time estimate
}
```

### Automation Orchestrator

**Purpose**: Coordinate all review cycles and integrations

**Key Functions**:

- `runEnhancedClientReport()` - Client reporting
- `runDailyStandup()` - Team standups
- `runWeeklyReview()` - Sprint reviews
- `sendSmartSlackMessages(report)` - Multi-message delivery
- `sendToN8N(enhancedData)` - N8N webhook trigger

**Error Handling**:

```javascript
try {
  for (message in messages) {
    await sendToSlack(webhook, message);
    log("✅ Message sent");
    await sleep(1000); // Prevent rate limiting
  }
} catch (error) {
  log("❌ Failed to send message");
  throw error; // Propagate for cron monitoring
}
```

## 🎯 Character Limit Strategy

### The 3000-Character Problem

**Slack Limit**: 3000 characters per message
**Our Limit**: 2800 characters (safety buffer)

### Solution: Intelligent Splitting

```
┌────────────────────────────────────────┐
│  Total Content: 5,500 characters       │
└────────────────────────────────────────┘
                 │
                 ▼
      ┌──────────────────┐
      │ Priority Sorting  │
      └──────────────────┘
                 │
                 ▼
   ┌─────────────────────────────┐
   │ 1. Recent Activity (if any) │ ← 1,842 chars ✅
   │ 2. Core Functionality       │ ← 1,653 chars ✅
   │ 3. Detailed Progress        │ ← 2,107 chars ✅
   └─────────────────────────────┘
```

### Character Budget Allocation

**Message 1: Recent Activity**

- Header: 50 chars
- Summary line: 50 chars
- Per domain (up to 4): ~600 chars each
- Footer context: 100 chars
- **Total Budget**: ~2,500 chars

**Message 2: Core Status**

- Header: 30 chars
- Per functionality (4): ~250 chars each
- Milestones section: ~500 chars
- **Total Budget**: ~1,500 chars

**Message 3: Detailed Progress**

- Header: 40 chars
- Per deliverable (4): ~500 chars each
- **Total Budget**: ~2,000 chars

## 🔍 Content Prioritization

### Domain Priority Order

```javascript
Priority 1 (CRITICAL):
  - course-management

Priority 2 (HIGH):
  - events-management
  - community-discussions
  - community-posts

Priority 3 (MEDIUM):
  - All other domains
```

### Activity Selection

Within each domain:

1. **Most Recent First**: Sort by timestamp descending
2. **Completions Over Progress**: "COMPLETED" keyword prioritized
3. **Limit Per Domain**: Max 2 activities to prevent domination
4. **Smart Truncation**: 120 chars per activity summary

### Overflow Handling

```javascript
If (currentLength + newBlock > MAX_LENGTH) {
  If (currentMessage has content) {
    messages.push(currentMessage)  // Save current
    currentMessage = new Message() // Start new
  }
  If (newBlock > MAX_LENGTH) {
    Truncate newBlock to fit       // Extreme case
  }
  Add newBlock to currentMessage
}
```

## 📁 File Structure

```
.taskmaster/review-cycles/
├── smart-client-reporter.js       # 🆕 Main smart reporter
├── recent-activity-tracker.js     # 🆕 Activity extraction
├── enhanced-client-report.js      # 📊 Enhanced report generator
├── automation-orchestrator.js     # 🔄 Coordination layer (UPDATED)
├── daily-standup.js               # 📅 Daily reports (EXISTING)
├── weekly-sprint-review.js        # 📈 Weekly analysis (EXISTING)
├── sync-complexity-reports.js     # ⚙️ Complexity sync (EXISTING)
├── run-cycle.sh                   # 🚀 Cron wrapper (EXISTING)
├── config.json                    # ⚙️ Configuration (UPDATED)
├── SMART_REPORTING_GUIDE.md       # 📖 Complete guide (NEW)
├── QUICKSTART.md                  # 🚀 5-min setup (NEW)
├── BEFORE_AFTER_COMPARISON.md     # 📊 Visual comparison (NEW)
├── ARCHITECTURE.md                # 🏗️ This file (NEW)
└── README.md                      # 📝 Overview (UPDATED)
```

## 🔐 Security & Privacy

### Sensitive Data Handling

**Webhook URLs**:

- Stored in `config.json` (gitignored)
- Can use environment variables
- Never logged to files

**Task Content**:

- Only extracts from TaskMaster data (already trusted)
- No external API calls for content
- Client sees same data they approved in tasks

### Error Handling

**Graceful Degradation**:

```javascript
try {
  recentActivity = extractRecentActivity();
} catch (error) {
  log("Activity extraction failed, continuing with static report");
  recentActivity = { totalUpdates: 0, activities: [] };
}
```

**Slack API Failures**:

```javascript
try {
  await sendToSlack(webhook, message);
} catch (error) {
  log("Failed to send message, saving for manual review");
  saveFailedMessage(message);
  throw error; // Alert cron monitoring
}
```

## 📊 Performance Characteristics

### Execution Time

| Component                | Time       | Notes              |
| ------------------------ | ---------- | ------------------ |
| Load tasks.json          | ~50ms      | Single file read   |
| Extract recent activity  | ~100ms     | Regex parsing      |
| Generate enhanced report | ~200ms     | Complexity lookups |
| Build smart messages     | ~50ms      | Format logic       |
| Send to Slack            | ~500ms/msg | Network I/O        |
| **Total**                | **~1.4s**  | For 3 messages     |

### Memory Usage

| Component           | Memory   | Notes              |
| ------------------- | -------- | ------------------ |
| tasks.json parsed   | ~2MB     | Full task tree     |
| Complexity reports  | ~500KB   | All 12 tags        |
| Activity extraction | ~100KB   | Recent only        |
| Report generation   | ~500KB   | Structured data    |
| **Peak**            | **~3MB** | Well within limits |

### Scalability

**Current Load**:

- 34 tasks across 12 domains
- ~100 subtasks total
- ~50 info blocks to scan

**Scaling Limits**:

- Tasks: ~1,000 (< 1s processing)
- Info blocks: ~500 (< 500ms regex)
- Activity window: 7 days max recommended

## 🔧 Configuration Options

### config.json Structure

```json
{
  "schedule": {
    "clientReport": {
      "enabled": true,
      "frequency": "daily",
      "time": "06:30",
      "useSmartReporter": true, // 🆕 Enable smart reporter
      "recentActivityHours": 48, // 🆕 Activity window
      "maxMessagesPerReport": 3, // 🆕 Message limit
      "characterLimit": 2800 // 🆕 Per-message limit
    }
  },
  "slack": {
    "client": {
      "webhook": "...",
      "enabled": true,
      "retryAttempts": 3, // 🆕 Retry config
      "retryDelayMs": 1000 // 🆕 Retry delay
    }
  }
}
```

### Environment Variables

```bash
# Override config.json settings
SLACK_CLIENT_WEBHOOK="https://hooks.slack.com/..."
N8N_WEBHOOK_URL="https://n8n.dev.experts.com.sa/webhook/..."
PROJECT_ROOT="/home/logix/experts"
NODE_ENV="production"

# Output control
OUTPUT="slack"     # slack | json | summary
FORMAT="summary"   # For recent-activity-tracker
```

## 🧪 Testing Architecture

### Unit Tests

```bash
# Test activity extraction
node recent-activity-tracker.js 24
# Verify: Correct activities, timestamps, summaries

# Test report generation
node smart-client-reporter.js
# Verify: Messages count, character limits, structure
```

### Integration Tests

```bash
# Test full flow
node automation-orchestrator.js client
# Verify: Logs, Slack delivery, N8N trigger

# Test with different activity windows
FORMAT=summary node recent-activity-tracker.js 168
# Verify: One week of activity
```

### Manual Verification

```bash
# 1. Add test activity
task-master update-subtask --id=X.Y --prompt="Test update"

# 2. Verify extraction
FORMAT=summary node recent-activity-tracker.js 1

# 3. Check message content
OUTPUT=slack node smart-client-reporter.js | jq '.blocks'

# 4. Verify character counts
OUTPUT=slack node smart-client-reporter.js | jq '.blocks[].text.text | length'
```

## 🔄 Update Cycle

### Frequency Options

**Daily** (Recommended):

- Cron: `30 6 * * 1-5`
- Shows consistent progress
- Client gets regular updates
- Best for active development

**Weekly**:

- Cron: `0 17 * * 5`
- Less noise for client
- Better for maintenance phase
- Aligns with sprint cycles

**Custom**:

```bash
# Twice per week (Tuesday, Friday)
30 6 * * 2,5 /home/logix/experts/.taskmaster/review-cycles/run-cycle.sh client

# After each TaskMaster update (manual trigger)
./run-cycle.sh client
```

## 🎯 Success Metrics

### System Health Indicators

✅ **Healthy System**:

- Recent activity detected most days
- Messages stay under 2800 chars
- All 3 messages deliver successfully
- Logs show no errors
- Client engagement high

⚠️ **Needs Attention**:

- No recent activity for > 3 days
- Messages truncated despite splitting
- Slack delivery failures
- Client asking for clarification
- Cron job not executing

### Monitoring Commands

```bash
# Check last 10 report runs
tail -20 .taskmaster/logs/cron-client.log

# Verify recent activity detection
FORMAT=summary node recent-activity-tracker.js 168 | jq '.totalUpdates'

# Check message sizes
OUTPUT=slack node smart-client-reporter.js | \
  jq '.blocks[].text.text | length' | \
  awk '{sum+=$1; if($1>max) max=$1} END {print "Avg:",sum/NR,"Max:",max}'

# Verify cron is running
grep "run-cycle.sh client" .taskmaster/logs/cron-client.log | tail -5
```

## 🚀 Deployment Checklist

- [ ] All files created and executable
- [ ] config.json configured with Slack webhook
- [ ] Test generation successful
- [ ] Slack messages preview looks good
- [ ] Cron job added to crontab
- [ ] First automated run successful
- [ ] Logs show proper execution
- [ ] Client confirms messages received
- [ ] Character limits verified (all < 2800)
- [ ] Recent activity detection working
- [ ] N8N integration preserved (if used)

## 📚 Further Reading

- **[SMART_REPORTING_GUIDE.md](./SMART_REPORTING_GUIDE.md)** - Comprehensive guide
- **[QUICKSTART.md](./QUICKSTART.md)** - 5-minute setup
- **[BEFORE_AFTER_COMPARISON.md](./BEFORE_AFTER_COMPARISON.md)** - Visual examples
- **[N8N_INTEGRATION_GUIDE.md](./N8N_INTEGRATION_GUIDE.md)** - N8N workflow integration

---

**Architecture Version**: 2.0
**Last Updated**: December 5, 2025
**Stability**: Production Ready
**Backward Compatibility**: ✅ Full
