---
title: "N8N Integration Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/taskmaster"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# N8N Integration Guide

## Overview

This guide explains how to integrate the new Taskmaster Review Cycle system with your existing N8N workflow that currently reads `tasks.json` and sends AI-summarized reports to Slack.

## Integration Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Taskmaster    │    │   Review Cycle   │    │      N8N        │
│   tasks.json    │───▶│     System       │──▶│   Workflow      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │ Enhanced Data   │    │ AI Summarization │
                       │ + Predictions   │    │ + Slack Client   │
                       └─────────────────┘    └─────────────────┘
```

## What Changes

### Before (Your Current Setup)

1. N8N reads `tasks.json` weekly
2. AI summarizes task data
3. Sends client-friendly report to Slack

### After (Enhanced Setup)

1. **Daily Internal Reports** - Team accountability via Slack
2. **Weekly Sprint Reviews** - Stakeholder reports with analytics
3. **Enhanced Client Reports** - Your existing workflow gets richer data
4. **Automated Alerts** - Risk detection and velocity monitoring

## N8N Workflow Modifications

### Option A: Webhook Integration (Recommended)

Modify your existing N8N workflow to receive enhanced data via webhook:

1. **Add Webhook Trigger**: Configure to receive POST requests
2. **Enhanced Data Processing**: The system sends structured data including:

   ```json
   {
     "tasksData": "// Clean, AI-friendly task data",
     "context": "// Project context and terminology",
     "insights": "// Pre-calculated metrics and predictions",
     "talkingPoints": "// Suggested positive/challenge/solution points"
   }
   ```

3. **Improved AI Prompts**: Use the context and insights for better summaries

### Option B: File-Based Integration (Fallback)

If webhook setup is not immediately possible:

1. **Enhanced Data Files**: System writes enriched data to:
   - `/home/logix/experts/.taskmaster/reports/client/latest.json`
2. **Modify N8N File Reader**: Point to new location instead of `tasks.json`
3. **Richer AI Context**: Use the enhanced data structure for better summaries

## Enhanced Data Structure

The enhanced client report provides:

### Core Data (Replaces tasks.json)

```json
{
  "tasksData": {
    "domains": {
      "Core Platform Features": {
        "tasks": [
          {
            "title": "User Profile System Implementation",
            "status": "completed",
            "priority": "high",
            "progress": 100,
            "impact": "high",
            "subtasksCompleted": 8,
            "totalSubtasks": 8
          }
        ]
      }
    },
    "overallStats": {
      "totalTasks": 6,
      "completedTasks": 1,
      "inProgressTasks": 2,
      "pendingTasks": 3
    }
  }
}
```

### AI Context (Improves Summaries)

```json
{
  "context": {
    "projectPhase": "development",
    "technicalComplexity": "moderate",
    "clientPriorities": ["user_experience", "performance"],
    "communicationTone": "professional",
    "preferredTerminology": {
      "in_progress": "actively developing",
      "pending": "planned for upcoming sprints"
    }
  }
}
```

### Pre-Calculated Insights

```json
{
  "insights": {
    "progress": "45% complete",
    "health": "good",
    "accomplishments": [
      {
        "title": "User Authentication System",
        "impact": "Enables secure user access"
      }
    ],
    "predictions": {
      "estimatedCompletion": {
        "date": "2025-11-15",
        "confidence": "high"
      }
    },
    "risks": [
      {
        "type": "technical_complexity",
        "level": "medium",
        "description": "Some features require careful technical planning"
      }
    ]
  }
}
```

## Implementation Steps

### Step 1: Setup Review Cycle System

```bash
cd /home/logix/experts/.taskmaster/review-cycles
./setup-cron.sh
```

### Step 2: Configure Environment

Edit `.env` file:

```bash
# Your existing client Slack webhook
SLACK_CLIENT_WEBHOOK="https://hooks.slack.com/services/YOUR/CLIENT/WEBHOOK"

# Optional: N8N webhook for real-time integration
N8N_WEBHOOK_URL="https://your-n8n.com/webhook/taskmaster-enhanced"
```

### Step 3A: Webhook Integration (Recommended)

1. **Create N8N Webhook Node**:
   - URL: `https://your-n8n.com/webhook/taskmaster-enhanced`
   - Method: POST
   - Response: 200 OK

2. **Configure Auto-trigger**:

   ```bash
   # Add to crontab
   0 17 * * 5 /home/logix/experts/.taskmaster/review-cycles/run-cycle.sh client
   ```

3. **Update AI Processing**:
   Use the enhanced data structure in your AI prompts:

   ```
   Based on this enhanced project data including context, insights, and predictions,
   create a client-friendly weekly update that highlights progress,
   accomplishments, and upcoming milestones...
   ```

### Step 3B: File Integration (Alternative)

1. **Update N8N File Reader**:
   - Change path from `tasks.json` to:
   - `/home/logix/experts/.taskmaster/reports/client/latest.json`

2. **Schedule Update**:
   - Run client report generation before N8N reads the file
   - Cron: `0 16 * * 5` (4 PM, before your 5 PM N8N run)

## Sample N8N Node Configuration

### Enhanced AI Prompt

```javascript
// N8N Function Node
const enhancedData = $json;

const prompt = `
Project Context: ${enhancedData.context.projectPhase} phase, ${enhancedData.context.technicalComplexity} complexity
Current Progress: ${enhancedData.insights.progress}
Project Health: ${enhancedData.insights.health}

Recent Accomplishments:
${enhancedData.insights.accomplishments.map((a) => `- ${a.title}: ${a.impact}`).join("\n")}

${
  enhancedData.insights.predictions.estimatedCompletion
    ? `Estimated Completion: ${enhancedData.insights.predictions.estimatedCompletion.date} (${enhancedData.insights.predictions.estimatedCompletion.confidence} confidence)`
    : ""
}

${
  enhancedData.insights.risks.length > 0
    ? `Considerations: ${enhancedData.insights.risks.map((r) => r.description).join(", ")}`
    : ""
}

Based on this data, create a professional, client-friendly weekly update that:
1. Celebrates recent accomplishments
2. Provides clear progress visibility
3. Sets expectations for upcoming work
4. Addresses any risks with solutions

Use a ${enhancedData.context.communicationTone} tone and prefer these terms:
${Object.entries(enhancedData.context.preferredTerminology)
  .map(([k, v]) => `${k} = ${v}`)
  .join(", ")}
`;

return { prompt };
```

## Benefits of Enhanced Integration

### For Your Current Workflow

- **Richer Context**: AI gets better project understanding
- **Predictive Insights**: Delivery estimates and risk indicators
- **Consistent Terminology**: Professional, client-appropriate language
- **Structured Data**: Easier to parse and process

### New Capabilities

- **Daily Team Accountability**: Internal Slack reports
- **Weekly Stakeholder Updates**: Detailed analytics and trends
- **Automated Risk Detection**: Proactive issue identification
- **Velocity Tracking**: Performance metrics and predictions

## Testing & Validation

### Test Enhanced Data Generation

```bash
cd /home/logix/experts/.taskmaster/review-cycles
node enhanced-client-report.js
```

### Test Complete Integration

```bash
# Generate enhanced report and trigger N8N
./run-cycle.sh client
```

### Validate Output

Check generated files:

- `/home/logix/experts/.taskmaster/reports/client/client-report-YYYY-MM-DD.json`
- `/home/logix/experts/.taskmaster/logs/cron-client.log`

## Monitoring & Maintenance

### Health Checks

```bash
# Check system status
node automation-orchestrator.js status

# View recent logs
tail -f /home/logix/experts/.taskmaster/logs/orchestrator.log
```

### Configuration Updates

```bash
# View current config
node automation-orchestrator.js config

# Edit environment
vim /home/logix/experts/.taskmaster/review-cycles/.env
```

## Troubleshooting

### Common Issues

1. **N8N Webhook Not Receiving Data**
   - Check webhook URL in `.env`
   - Verify N8N webhook is active
   - Check logs for HTTP errors

2. **Enhanced Data Not Generated**
   - Verify `tasks.json` exists and is readable
   - Check Node.js permissions
   - Review error logs

3. **Cron Jobs Not Running**
   - Verify crontab entries: `crontab -l`
   - Check cron logs: `grep CRON /var/log/syslog`
   - Test manual execution: `./run-cycle.sh client`

### Support

For issues or questions:

1. Check logs in `/home/logix/experts/.taskmaster/logs/`
2. Run `node automation-orchestrator.js status` for health check
3. Test individual components manually before debugging integration

## Migration Timeline

### Week 1: Setup & Testing

- Install review cycle system
- Configure basic automation
- Test enhanced data generation

### Week 2: N8N Integration

- Implement webhook or file integration
- Update AI prompts with enhanced data
- Parallel run with existing system

### Week 3: Full Deployment

- Switch N8N to use enhanced data
- Enable all review cycles
- Monitor and optimize

This integration maintains your existing client communication while adding powerful internal accountability and enhanced insights.
