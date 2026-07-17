---
title: "Quick Start: Smart Client Reporting"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/taskmaster"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Quick Start: Smart Client Reporting

## 🚀 5-Minute Setup

### 1. Install (Already Done ✅)

The smart client reporter is already installed and integrated with your system.

### 2. Configure Slack Webhook

Edit `.taskmaster/review-cycles/config.json`:

```json
{
  "slack": {
    "client": {
      "webhook": "https://hooks.slack.com/services/YOUR/WEBHOOK/HERE",
      "enabled": true
    }
  }
}
```

Get your Slack webhook from: <https://api.slack.com/messaging/webhooks>

### 3. Test Locally

```bash
cd /home/logix/experts

# Test report generation
node .taskmaster/review-cycles/smart-client-reporter.js

# Preview Slack messages
OUTPUT=slack node .taskmaster/review-cycles/smart-client-reporter.js | head -100

# Check recent activity
FORMAT=summary node .taskmaster/review-cycles/recent-activity-tracker.js 48
```

### 4. Enable Automation

The cron job is already configured. To verify:

```bash
crontab -l | grep "run-cycle.sh client"
```

Should show:

```
30 6 * * 1-5 /home/logix/experts/.taskmaster/review-cycles/run-cycle.sh client
```

### 5. Verify It Works

After making task updates, verify they appear in reports:

```bash
# 1. Update a task (example)
task-master update-subtask --id=1.1 --prompt="Completed API endpoint implementation. All tests passing."

# 2. Check recent activity
FORMAT=summary node .taskmaster/review-cycles/recent-activity-tracker.js 48

# 3. Generate report
node .taskmaster/review-cycles/smart-client-reporter.js

# 4. Preview first Slack message
OUTPUT=slack node .taskmaster/review-cycles/smart-client-reporter.js | grep -A 30 "Message 1"
```

## 📊 What You Get

### Multiple Smart Messages

**Message 1: Recent Activity** (only if work done in last 48h)

- Shows actual implementation progress
- Extracts from task info blocks
- Timestamps: "X hours ago"
- Prioritizes 4 main functionalities

**Message 2: Core Status** (always sent)

- Progress bars for 4 main areas
- Task counts (completed/in progress/planned)
- Recent milestones
- Visual indicators

**Message 3: Upcoming Work** (conditional)

- High-priority next items
- Complexity scores
- Time estimates
- Risk indicators

### Character Limit Handling

Each message stays under **2800 characters** automatically:

- Smart content prioritization
- Automatic truncation
- Multi-message splitting when needed

## 🎯 Best Practices

### Update Tasks Regularly

```bash
# When you complete work on a subtask
task-master update-subtask --id=X.Y --prompt="COMPLETED: Feature description

What was implemented:
- Backend implementation details
- Frontend changes
- Test coverage

Files modified: X files
All tests passing."

# When making progress
task-master update-subtask --id=X.Y --prompt="Progress update: Working on feature XYZ. Implemented component A and B. Next: Component C."
```

### Info Block Format

Use clear, structured updates:

```markdown
<info added on [AUTO-TIMESTAMP]>
COMPLETED: [Feature Name]

What was implemented:

- Key achievement 1
- Key achievement 2
- Key achievement 3

Files modified:

- path/to/file1.ts
- path/to/file2.tsx

Status: [All tests passing | In progress | Blocked by X]
</info added on [AUTO-TIMESTAMP]>
```

Keywords the system recognizes:

- `COMPLETED` - Completion summaries
- `Progress` - Progress updates
- `Implementation` - Technical details
- `Files modified` - File change tracking

## 🔧 Common Commands

```bash
# Generate client report
./run-cycle.sh client

# Check recent activity (last 24h)
FORMAT=summary node recent-activity-tracker.js 24

# Check recent activity (last week)
FORMAT=summary node recent-activity-tracker.js 168

# Preview Slack messages
OUTPUT=slack node smart-client-reporter.js | less

# Check automation status
node automation-orchestrator.js status

# View logs
tail -f .taskmaster/logs/cron-client.log
```

## 📱 MCP Tools (Cursor/Claude Code)

```bash
# Generate smart report
run_smart_client_report(test_mode: false, output_format: "slack")

# Extract recent activity
run_recent_activity_tracker(hours_back: 48, format: "summary")

# Run full automation
run_automation_orchestrator(action: "client", test_mode: false)
```

## ✅ Verification Checklist

- [ ] Slack webhook configured in config.json
- [ ] Test report generates successfully
- [ ] Recent activity appears when you update tasks
- [ ] Cron job scheduled (30 6 \*\* 1-5)
- [ ] Logs show successful execution
- [ ] Slack messages arrive in correct channel
- [ ] Messages are under 3000 characters
- [ ] 4 main functionalities prominently featured

## 🚨 Troubleshooting

### No recent activity showing

**Check**:

```bash
# Verify task updates have recent timestamps
task-master show 14.10 | grep "info added"

# Check what the tracker sees
node recent-activity-tracker.js 48 | jq '.activities'
```

**Fix**: Ensure you're using `task-master update-subtask` or `update-task` to add timestamped info.

### Messages truncated

**Check**:

```bash
# See message lengths
OUTPUT=slack node smart-client-reporter.js | jq '.blocks[].text.text | length'
```

**Fix**: Adjust `MAX_SLACK_LENGTH` in smart-client-reporter.js (line 13).

### Slack messages not arriving

**Check**:

```bash
# Verify webhook is set
cat .taskmaster/review-cycles/config.json | jq '.slack.client'

# Test webhook directly
curl -X POST YOUR_WEBHOOK_URL -H 'Content-Type: application/json' -d '{"text":"Test"}'
```

## 📚 Documentation

- **[SMART_REPORTING_GUIDE.md](./SMART_REPORTING_GUIDE.md)** - Complete guide with architecture and examples
- **[README.md](./README.md)** - Overview and architecture
- **[N8N_INTEGRATION_GUIDE.md](./N8N_INTEGRATION_GUIDE.md)** - N8N workflow integration

## 🎓 Next Steps

1. Configure your Slack webhook
2. Test report generation
3. Make some task updates
4. Verify recent activity appears
5. Monitor automated reports
6. Adjust `recentActivityHours` if needed

---

**Setup Time**: 5 minutes
**Complexity**: Low
**Maintenance**: Automatic via cron
**Dependencies**: Node.js, TaskMaster, Slack webhook
