---
title: "Task Manager API Documentation"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/taskmaster"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Task Manager API Documentation

## Overview

The Task Manager API provides comprehensive task management functionality similar to Taskmaster, including tasks, subtasks, tags, dependencies, and status management.

## Base URL

```
https://api.experts.com.sa/v1
```

## Authentication

All endpoints require authentication via Bearer token:

```
Authorization: Bearer {access_token}
```

## API Endpoints

### Task Tags

#### List Task Tags

```http
GET /task-tags
```

Query Parameters:

- `search` (string, optional): Search tags by name
- `page` (integer, optional): Page number for pagination
- `per_page` (integer, optional): Items per page (default: 15)

#### Create Task Tag

```http
POST /task-tags
```

Body:

```json
{
  "name": "development",
  "description": "Development tasks",
  "color": "#10B981",
  "metadata": {}
}
```

#### Get Task Tag

```http
GET /task-tags/{uuid}
```

#### Update Task Tag

```http
PUT /task-tags/{uuid}
```

#### Delete Task Tag

```http
DELETE /task-tags/{uuid}
```

#### Get Tag Statistics

```http
GET /task-tags/{uuid}/stats
```

### Tasks

#### List Tasks

```http
GET /tasks
```

Query Parameters:

- `tag` (string, optional): Filter by tag name
- `status` (string, optional): Filter by status (comma-separated)
- `priority` (string, optional): Filter by priority
- `type` (string, optional): Filter by type ('top-level' or 'subtasks')
- `search` (string, optional): Search in title and description
- `sort_by` (string, optional): Sort field (default: created_at)
- `sort_direction` (string, optional): Sort direction (asc/desc)

#### Create Task

```http
POST /tasks
```

Body:

```json
{
  "title": "Implement user authentication",
  "description": "Build login and registration system",
  "details": "Detailed implementation notes...",
  "status": "pending",
  "priority": "high",
  "type": "feature",
  "parent_task_uuid": null,
  "assignee": "John Doe",
  "reviewer": "Jane Smith",
  "estimated_hours": 20,
  "complexity": "medium",
  "confidence": "high",
  "due_date": "2025-10-01T00:00:00Z",
  "task_tag_name": "development",
  "acceptance_criteria": [
    "Users can register with email",
    "Users can login with credentials",
    "Password reset functionality works"
  ],
  "test_strategy": {
    "unit_tests": "Test validation and business logic",
    "integration_tests": "Test API endpoints",
    "e2e_tests": "Test complete user flows"
  },
  "technical_details": {
    "files_to_modify": ["UserController.php", "AuthService.php"],
    "apis_affected": ["POST /login", "POST /register"]
  }
}
```

#### Get Task

```http
GET /tasks/{uuid}
```

#### Update Task

```http
PUT /tasks/{uuid}
```

#### Delete Task

```http
DELETE /tasks/{uuid}
```

#### Get Next Available Task

```http
GET /tasks/next
```

Query Parameters:

- `tag` (string, optional): Filter by tag name

#### Bulk Update Tasks

```http
PATCH /tasks/bulk-update
```

Body:

```json
{
  "task_uuids": ["uuid1", "uuid2", "uuid3"],
  "updates": {
    "status": "in_progress",
    "assignee": "John Doe"
  }
}
```

### Task Dependencies

#### Add Dependency

```http
POST /tasks/{uuid}/dependencies
```

Body:

```json
{
  "depends_on_uuid": "other-task-uuid",
  "dependency_type": "blocks"
}
```

#### Remove Dependency

```http
DELETE /tasks/{uuid}/dependencies
```

Body:

```json
{
  "depends_on_uuid": "other-task-uuid"
}
```

## Data Models

### Task Status Values

- `pending` - Not started
- `in_progress` - Currently being worked on
- `done` - Completed
- `blocked` - Cannot proceed
- `cancelled` - No longer needed
- `deferred` - Postponed
- `review` - Under review

### Priority Values

- `low`
- `medium`
- `high`
- `critical`

### Task Types

- `feature` - New feature development
- `bug` - Bug fix
- `task` - General task
- `epic` - Large feature or initiative
- `story` - User story

### Complexity Values

- `simple`
- `medium`
- `complex`
- `very_complex`

### Confidence Values

- `low`
- `medium`
- `high`

## Response Format

All API responses follow this structure:

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully",
  "meta": {
    "pagination": { ... }
  }
}
```

### Error Response

```json
{
  "success": false,
  "message": "Error description",
  "errors": {
    "field": ["validation error message"]
  }
}
```

## Features

### Task Management

- ✅ Create, read, update, delete tasks
- ✅ Task status tracking with automatic timestamps
- ✅ Priority and complexity management
- ✅ Assignee and reviewer tracking
- ✅ Effort estimation and tracking

### Subtasks

- ✅ Hierarchical task structure
- ✅ Parent-child relationships
- ✅ Automatic parent completion when all subtasks done
- ✅ Sort ordering within parent tasks

### Dependencies

- ✅ Task dependency management
- ✅ Circular dependency prevention
- ✅ Dependency type support (blocks, related)
- ✅ Available task detection based on dependencies

### Tags

- ✅ Organize tasks by context/project
- ✅ Tag-based filtering
- ✅ Tag statistics and progress tracking
- ✅ Color coding for visual organization

### Advanced Features

- ✅ Next available task recommendation
- ✅ Bulk task updates
- ✅ Progress tracking and completion percentages
- ✅ Overdue task detection
- ✅ Search functionality
- ✅ Comprehensive filtering and sorting

### Data Integrity

- ✅ UUID-based public identifiers
- ✅ User ownership enforcement
- ✅ Validation rules and error handling
- ✅ Database constraints and indexes
- ✅ Comprehensive test coverage

## Usage Examples

### Creating a Development Workflow

1. **Create a tag for your project:**

```bash
curl -X POST https://api.experts.com.sa/v1/task-tags \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"name": "web-app", "description": "Web application development", "color": "#3B82F6"}'
```

2. **Create a main task:**

```bash
curl -X POST https://api.experts.com.sa/v1/tasks \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Build User Authentication",
    "description": "Complete authentication system",
    "priority": "high",
    "task_tag_name": "web-app",
    "estimated_hours": 40
  }'
```

3. **Create subtasks:**

```bash
curl -X POST https://api.experts.com.sa/v1/tasks \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Create login form",
    "parent_task_uuid": "{parent-uuid}",
    "task_tag_name": "web-app",
    "estimated_hours": 8
  }'
```

4. **Get next task to work on:**

```bash
curl -X GET https://api.experts.com.sa/v1/tasks/next?tag=web-app \
  -H "Authorization: Bearer {token}"
```

5. **Update task status:**

```bash
curl -X PUT https://api.experts.com.sa/v1/tasks/{uuid} \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

## Database Schema

### task_tags

- `id` (bigint, primary)
- `uuid` (varchar, unique)
- `name` (varchar, unique)
- `description` (text, nullable)
- `color` (varchar, default: #3B82F6)
- `metadata` (json, nullable)
- `created_at`, `updated_at`

### tasks

- `id` (bigint, primary)
- `uuid` (varchar, unique)
- `title` (varchar)
- `description` (text, nullable)
- `details` (longtext, nullable)
- `status` (enum)
- `priority` (enum)
- `type` (enum)
- `parent_task_id` (bigint, nullable, self-referencing)
- `sort_order` (integer)
- `user_id` (bigint, foreign key)
- `task_tag_id` (bigint, foreign key)
- `assignee`, `reviewer` (varchar, nullable)
- `estimated_hours`, `actual_hours` (integer, nullable)
- `complexity` (enum, nullable)
- `confidence` (enum)
- `due_date`, `started_at`, `completed_at` (timestamp, nullable)
- `acceptance_criteria` (json, nullable)
- `test_strategy` (json, nullable)
- `technical_details` (json, nullable)
- `metadata` (json, nullable)
- `created_at`, `updated_at`

### task_dependencies

- `id` (bigint, primary)
- `task_id` (bigint, foreign key)
- `depends_on_task_id` (bigint, foreign key)
- `dependency_type` (enum: blocks, related)
- `created_at`, `updated_at`

## Testing

Run the test suite:

```bash
php artisan test --filter=TaskTagTest
php artisan test --filter=TaskTest
```

All tests are passing with comprehensive coverage of:

- CRUD operations for tasks and tags
- Relationship management
- Dependency handling with circular prevention
- User ownership enforcement
- Filtering and search functionality
- Bulk operations
- Error handling and validation
