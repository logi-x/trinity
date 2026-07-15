---
title: "AI Prompt Modules Guide"
date: "2026-04-11"
tags: ["project/logix", "tech/n8n", "topic/prompt-modules-guide"]
category: "projects/logix"
updated: "2026-07-15"
---

## Links

- [[Projects/Logix/N8N_CORE/N8N CORE|N8N Core README]]

# AI Prompt Modules Guide

## Overview

The N8N Enhanced daily Client Project Update workflow now uses modular prompt files for better maintainability and customization.

## File Structure

```
.n8n/
├── system-prompt.json          # AI system instructions and capabilities
├── user-prompt.json           # User prompt template with data variables
├── ai-prompts-config.json     # Complete configuration with all prompts
└── PROMPT_MODULES_GUIDE.md    # This guide
```

## System Prompt (`system-prompt.json`)

Contains the AI's role definition, capabilities, and general guidelines:

- **Role**: Professional project communication specialist
- **Capabilities**: Transform technical data to client-friendly language
- **Guidelines**: Professional tone, business focus, executive-friendly format
- **Output Requirements**: Markdown format suitable for Slack and email

## User Prompt (`user-prompt.json`)

Contains the specific request template with N8N variable interpolation:

- **Project Context**: Phase, health, progress, communication tone
- **Data Sections**: Achievements, current work, challenges, outlook
- **Format Requirements**: 3-4 paragraphs, business language, clear structure
- **Quality Checklist**: Client-friendly language, metrics, timelines

## Usage in N8N Workflow

### Current Implementation

1. **Read System Prompt** node loads `system-prompt.json`
2. **Parse System Prompt** node converts binary to JSON
3. **AI Summarization** node uses both system and user prompts
4. System prompt is injected via: `{{ JSON.parse($('Parse System Prompt').first().json.data.toString()).content }}`

### Workflow Flow

```
Read System Prompt → Parse System Prompt
                              ↓
Process Data → Analyze Changes → AI Summarization (uses both prompts)
```

## Customization Guide

### Modifying Communication Style

**File**: `system-prompt.json`
**Section**: `"content"` → Communication Guidelines

```json
{
  "content": "...• Use [WARM/FORMAL/CASUAL] but professional language..."
}
```

### Adjusting Data Focus

**File**: `user-prompt.json`
**Section**: `"content_template"` → Specific Requirements

```json
{
  "content_template": "...2. **Content Focus:** Emphasize [BUSINESS_VALUE/TECHNICAL_DETAIL/USER_IMPACT]..."
}
```

### Changing Output Format

**File**: `system-prompt.json`
**Section**: Output Requirements

```json
{
  "content": "...• Format in [MARKDOWN/PLAIN_TEXT/HTML] suitable for [SLACK/EMAIL/REPORTS]..."
}
```

## Template Variables

All N8N template variables are preserved in `user-prompt.json`:

- `{{ $('Process Data').item.json.timeline.currentPhase }}`
- `{{ $json.hasHistory ? ... : ... }}`
- `{{ $('Process Data').item.json.summaryData.* }}`

## Benefits of Modular Approach

### ✅ **Maintainability**

- Easy to update system instructions without touching workflow
- Separate concerns: AI behavior vs. data processing
- Version control for prompt iterations

### ✅ **Flexibility**

- Swap system prompts for different communication styles
- A/B test different prompt approaches
- Client-specific customizations without duplicating workflows

### ✅ **Reusability**

- System prompt can be used across multiple N8N workflows
- Standard prompt templates for consistent communication
- Easy to share prompt configurations between projects

### ✅ **Debugging**

- Clear separation between prompt issues and data processing issues
- Easy to test prompts independently
- Better error tracking and optimization

## Advanced Usage

### Client-Specific Prompts

Create client-specific system prompts:

```
.n8n/
├── system-prompt-client-tech.json     # For technical clients
├── system-prompt-client-business.json # For business-focused clients
├── system-prompt-client-formal.json   # For formal communication
```

Update the workflow to read different system prompts based on client type.

### Multi-Language Support

Extend for international clients:

```
.n8n/
├── system-prompt-en.json  # English
├── system-prompt-ar.json  # Arabic
├── user-prompt-en.json    # English template
├── user-prompt-ar.json    # Arabic template
```

### Prompt Version Control

Track prompt evolution:

```
.n8n/prompts/
├── v1.0/
│   ├── system-prompt.json
│   └── user-prompt.json
├── v1.1/
│   ├── system-prompt.json
│   └── user-prompt.json
└── current/  # symlinks to latest version
```

## Testing Prompts

### Manual Testing

1. Update prompt files
2. Run N8N workflow manually
3. Evaluate AI output quality
4. Iterate on prompt content

### A/B Testing

1. Create prompt variants (A/B)
2. Run workflow with each version
3. Compare output quality and client feedback
4. Deploy best-performing version

## Best Practices

### 🎯 **System Prompt Best Practices**

- Keep role definition clear and specific
- Include concrete examples of desired behavior
- Specify output format requirements explicitly
- Balance guidance with AI flexibility

### 📝 **User Prompt Best Practices**

- Provide rich context about project state
- Include specific formatting requirements
- Give clear instructions for edge cases
- Use consistent variable naming conventions

### 🔄 **Maintenance Best Practices**

- Version control all prompt changes
- Test prompts after modifications
- Document customizations for team knowledge
- Regular review of AI output quality

## Troubleshooting

### Common Issues

**Problem**: AI output doesn't match expected format
**Solution**: Check system prompt output requirements section

**Problem**: N8N can't read prompt file
**Solution**: Verify file path and JSON syntax

**Problem**: Variables not interpolating
**Solution**: Check N8N expression syntax in user prompt

**Problem**: Inconsistent AI behavior
**Solution**: Add more specific guidelines to system prompt

### Support

For issues with prompt modules:

1. Check JSON syntax validity
2. Verify N8N node connections
3. Test with simple static prompts first
4. Review N8N execution logs for errors
