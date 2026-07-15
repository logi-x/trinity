---
title: "Taskmaster Sync System"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/taskmaster"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Taskmaster Sync System

## Overview

The Taskmaster Sync System automatically synchronizes tasks from the external Taskmaster `.taskmaster/tasks/tasks.json` file into the Laravel database, making them available in the admin dashboard for monitoring and reporting.

## Features

- ✅ **Automatic Sync**: Parse and import tasks from Taskmaster JSON format
- ✅ **Tag Management**: Create and organize tasks by tags/contexts
- ✅ **Hierarchical Tasks**: Support for parent tasks and subtasks
- ✅ **Dependencies**: Import task dependencies with circular prevention
- ✅ **Status Mapping**: Convert Taskmaster statuses to Laravel equivalents
- ✅ **Admin Dashboard**: Rich dashboard with analytics and visualizations
- ✅ **File Watching**: Automatic sync when tasks.json changes
- ✅ **CLI Management**: Manual sync commands with statistics

## Commands

### Manual Sync

```bash
# Sync tasks from Taskmaster
php artisan taskmaster:sync

# Show sync statistics
php artisan taskmaster:sync --stats

# Dry run (show what would be synced)
php artisan taskmaster:sync --dry-run

# Force sync even if no changes detected
php artisan taskmaster:sync --force
```

### File Watcher

```bash
# Start file watcher (continuous)
php artisan taskmaster:watch

# Check once and exit
php artisan taskmaster:watch --once

# Custom check interval (default: 5 seconds)
php artisan taskmaster:watch --interval=10
```

## API Endpoints

### Admin Dashboard

All endpoints require authentication (`auth:api` middleware):

#### Overview Statistics

```http
GET /v1/admin/tasks/overview
```

Response:

```json
{
  "success": true,
  "data": {
    "stats": {
      "total_tasks": 88,
      "completed_tasks": 51,
      "in_progress_tasks": 0,
      "pending_tasks": 14,
      "blocked_tasks": 0,
      "overdue_tasks": 0,
      "total_tags": 9,
      "completion_percentage": 57.95
    },
    "recent_tasks": [...],
    "tag_stats": [...]
  }
}
```

#### Tasks by Tag

```http
GET /v1/admin/tasks/by-tag?tag={tagName}&status={status}&priority={priority}
```

#### Gantt Chart Data

```http
GET /v1/admin/tasks/gantt?tag={tagName}
```

#### Project Timeline

```http
GET /v1/admin/tasks/timeline?tag={tagName}
```

#### Sync Status

```http
GET /v1/admin/tasks/sync-status
```

#### Perform Sync

```http
POST /v1/admin/tasks/sync
```

## Data Mapping

### Status Mapping

| Taskmaster           | Laravel       |
| -------------------- | ------------- |
| `not-started`        | `pending`     |
| `in-progress`        | `in_progress` |
| `completed` / `done` | `done`        |
| `blocked`            | `blocked`     |
| `cancelled`          | `cancelled`   |
| `deferred`           | `deferred`    |
| `review`             | `review`      |

### Priority Mapping

| Taskmaster | Laravel    |
| ---------- | ---------- |
| `critical` | `critical` |
| `high`     | `high`     |
| `medium`   | `medium`   |
| `low`      | `low`      |

### Tag Colors

Default colors are assigned based on tag names:

- `core-platform`: #3B82F6 (Blue)
- `authentication`: #EF4444 (Red)
- `billing-and-membership`: #F59E0B (Orange)
- `courses-management`: #10B981 (Green)
- `infrastructure`: #8B5CF6 (Purple)
- `feature-api-unification`: #06B6D4 (Cyan)
- `organizations`: #6366F1 (Indigo)
- `analytics-tracking`: #F97316 (Orange)
- `testing`: #84CC16 (Lime)

## Database Schema

The sync system uses the same database schema as the regular Task Manager:

- `task_tags` - Project contexts/tags
- `tasks` - Main tasks with metadata including `taskmaster_id`
- `task_dependencies` - Task relationships

### Special Fields

- `metadata->taskmaster_id`: Original Taskmaster task ID
- `metadata->synced_from_taskmaster`: Sync flag
- `user_id`: References the "Taskmaster System" user

## Usage Examples

### Basic Sync Workflow

1. **Initial Setup**: Run the first sync to import all tasks

```bash
php artisan taskmaster:sync
```

2. **Start File Watcher**: Monitor for changes automatically

```bash
php artisan taskmaster:watch
```

3. **View in Dashboard**: Access admin endpoints to see imported tasks

```bash
curl -H "Authorization: Bearer {token}" \
  https://api.experts.com.sa/v1/admin/tasks/overview
```

### Development Workflow

1. **Make changes in Taskmaster**: Update tasks, add new ones, change statuses
2. **Automatic Sync**: File watcher detects changes and syncs automatically
3. **View Updates**: Check admin dashboard to see updated data
4. **Monitor Progress**: Use timeline and gantt views for project tracking

## Configuration

### File Paths

- Taskmaster JSON: `../../.taskmaster/tasks/tasks.json` (relative to Laravel root)
- Can be customized in `TaskmasterSyncService` constructor

### Default User

The sync creates a system user for task ownership:

- Email: `taskmaster@experts.com.sa`
- Name: `Taskmaster System`
- Phone: `+966500000000`

## Error Handling

The sync system includes comprehensive error handling:

- **File Not Found**: Clear error message with file path
- **Invalid JSON**: JSON parsing error details
- **Database Errors**: Transaction rollback with error logging
- **Partial Failures**: Continue processing other tags/tasks
- **Circular Dependencies**: Automatic detection and prevention

## Performance Considerations

- **Database Transactions**: All operations wrapped in transactions
- **Batch Processing**: Efficient bulk operations
- **Memory Management**: Streams large JSON files
- **Indexing**: Proper database indexes for fast lookups
- **Caching**: Service-level caching for repeated operations

## Monitoring and Debugging

### Logs

All sync operations are logged to Laravel's default log:

```bash
tail -f storage/logs/laravel.log | grep TaskmasterSync
```

### Statistics

Check sync health with statistics:

```bash
php artisan taskmaster:sync --stats
```

### Debug Mode

Enable verbose logging in `.env`:

```
LOG_LEVEL=debug
```

## Troubleshooting

### Common Issues

1. **File Not Found**
   - Verify Taskmaster is installed and initialized
   - Check file path in `TaskmasterSyncService`

2. **Permission Errors**
   - Ensure Laravel has read access to Taskmaster directory
   - Check file ownership and permissions

3. **JSON Parse Errors**
   - Validate Taskmaster JSON syntax
   - Check for encoding issues

4. **Database Errors**
   - Verify migrations are up to date
   - Check database connection and permissions

5. **Authentication Errors**
   - Ensure API endpoints have proper authentication
   - Verify Passport configuration

### Recovery

If sync fails or data becomes inconsistent:

1. **Clear Taskmaster Data**:

```bash
# Remove all synced tasks
php artisan tinker --execute="
App\Domains\Tasks\Models\Task::whereNotNull('metadata->taskmaster_id')->delete();
App\Domains\Tasks\Models\TaskTag::whereIn('name', [
  'core-platform', 'authentication', 'billing-and-membership',
  'courses-management', 'infrastructure', 'feature-api-unification',
  'organizations', 'analytics-tracking', 'testing'
])->delete();
"
```

2. **Fresh Sync**:

```bash
php artisan taskmaster:sync
```

## Integration with Admin Dashboard

The synced tasks appear in the admin dashboard with:

- **Project Overview**: Completion statistics and progress tracking
- **Tag-based Views**: Tasks organized by context/project
- **Gantt Charts**: Timeline visualization with dependencies
- **Resource Allocation**: Assignee workload and capacity planning
- **Progress Tracking**: Completion forecasts and critical path analysis

This provides project managers and stakeholders with real-time visibility into development progress without requiring direct access to Taskmaster files.
