---
title: "Smart Client Reporting - Quick Reference Card"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/taskmaster"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Smart Client Reporting - Quick Reference Card

## 🚀 One Command to Rule Them All

```bash
./run-cycle.sh client
```

That's it! Everything else is automatic.

---

## 📊 What Gets Sent to Slack

### Message 1: Recent Activity (if work done in last 48h)

```
🚀 Recent Work Activity - [Date]
X updates in the last 48 hours

🎯 [Priority Domain]
• Task Title (X hours ago)
  Summary of what was implemented...

📈 Overall Progress: X% | Y/Z tasks complete
```

### Message 2: Core Status (always sent)

```
🎯 Core Platform Status

Course Management System (TOP PRIORITY) 🎉
██████████ 89%
1 completed | 0 in progress | 4 planned

[3 other main functionalities...]

✅ Recent Milestones:
• Completed feature 1
• Completed feature 2
```

### Message 3: Upcoming Work (conditional)

```
📅 Upcoming High-Priority Items

Task Title
🎯 Domain Name
⏱️ Estimated: X weeks
💡 User benefit
📊 Complexity: Level (score/10)

[3 more high-priority items...]
```

---

## 🛠️ Quick Commands

### Generate Reports

```bash
# Smart report (recommended)
./run-cycle.sh client

# Preview Slack messages
OUTPUT=slack node smart-client-reporter.js | less

# Check recent activity
FORMAT=summary node recent-activity-tracker.js 48
```

### Test & Debug

```bash
# Run full test suite
./test-smart-reporter.sh

# Check logs
tail -f .taskmaster/logs/cron-client.log

# View status
node automation-orchestrator.js status
```

### Update Tasks

```bash
# Completion update (shows in reports!)
task-master update-subtask --id=X.Y --prompt="COMPLETED: Feature ABC
- Implementation details
- Test status"

# Progress update
task-master update-subtask --id=X.Y --prompt="Progress: Feature 75% done"

# Status only (won't show recent activity!)
task-master set-status --id=X.Y --status=done
```

---

## 📋 Checklist

### Setup

- [ ] Slack webhook configured in `config.json`
- [ ] Cron job scheduled (`crontab -l`)
- [ ] Test run successful
- [ ] First automated report sent

### Daily Usage

- [ ] Update tasks with `update-subtask` (not just status changes)
- [ ] Include "COMPLETED" or "Progress" keywords
- [ ] Add implementation details
- [ ] Mention test status and files modified

### Monitoring

- [ ] Check logs weekly: `tail .taskmaster/logs/cron-client.log`
- [ ] Verify Slack messages arrive
- [ ] Confirm character limits respected
- [ ] Recent activity showing correctly

---

## 🎯 The 4 Main Functionalities (Priority Order)

Reports always emphasize these in order:

1. **Course Management System** (TOP PRIORITY) - Currently 89% complete
2. **Events Management Platform** (HIGH) - Currently 0% complete
3. **Community Discussion Forums** (HIGH) - Currently 0% complete
4. **Content & Posts Management** (HIGH) - Currently 0% complete

Work on these shows up **prominently** in reports!

---

## 📏 Character Limits

| Message              | Max Chars | Typical |
| -------------------- | --------- | ------- |
| Message 1 (Activity) | 2800      | ~1800   |
| Message 2 (Status)   | 2800      | ~1600   |
| Message 3 (Upcoming) | 2800      | ~2100   |

**Slack Limit**: 3000 characters
**Our Buffer**: 2800 characters
**Overflow**: Automatically creates new message

---

## 🔧 Configuration

### Edit Settings

```bash
# Main config
vim .taskmaster/review-cycles/config.json

# Environment variables
vim .taskmaster/review-cycles/.env
```

### Key Settings

```json
{
  "clientReport": {
    "useSmartReporter": true, // Enable smart reporter
    "recentActivityHours": 48, // Activity window (24-168)
    "enabled": true // Enable/disable
  }
}
```

---

## 🆘 Emergency Commands

### Something's wrong? Check these

```bash
# 1. Are cron jobs running?
crontab -l

# 2. Any errors in logs?
tail -20 .taskmaster/logs/cron-client.log

# 3. Can it generate report?
node smart-client-reporter.js

# 4. Is webhook valid?
grep webhook .taskmaster/review-cycles/config.json

# 5. Test webhook
curl -X POST YOUR_WEBHOOK -H 'Content-Type: application/json' -d '{"text":"Test"}'
```

### Restart fresh

```bash
# Regenerate report
node smart-client-reporter.js

# Verify it worked
ls -lh .taskmaster/reports/client/latest.json

# Test Slack delivery (check your channel)
OUTPUT=slack node smart-client-reporter.js
```

---

## 📞 Get Help

### Documentation

- **Quick Setup**: [QUICKSTART.md](./QUICKSTART.md)
- **Full Guide**: [SMART_REPORTING_GUIDE.md](./SMART_REPORTING_GUIDE.md)
- **Examples**: [BEFORE_AFTER_COMPARISON.md](./BEFORE_AFTER_COMPARISON.md)
- **Architecture**: [ARCHITECTURE.md](./ARCHITECTURE.md)

### Test Everything

```bash
./test-smart-reporter.sh
```

Should show: `✅ All tests passed! (22/22)`

---

## 💡 Pro Tips

### Get More Recent Activity

```bash
# Update multiple tasks at once
task-master update-subtask --id=1.1 --prompt="COMPLETED: Feature A"
task-master update-subtask --id=1.2 --prompt="Progress: Feature B at 80%"
task-master update-subtask --id=2.1 --prompt="Started work on Feature C"

# Next report will show all 3!
```

### Preview Before Sending

```bash
# See exactly what client will receive
OUTPUT=slack node smart-client-reporter.js | \
  jq -r '.blocks[] | select(.type=="section") | .text.text'
```

### Check Activity Age

```bash
# What's in the last 24 hours?
FORMAT=summary node recent-activity-tracker.js 24

# Last week?
FORMAT=summary node recent-activity-tracker.js 168
```

---

**Last Updated**: December 5, 2025
**System Status**: ✅ Fully Operational
**Tests**: ✅ 22/22 Passing
**Ready**: 🚀 Production Use

Print this page for your desk! 📄
