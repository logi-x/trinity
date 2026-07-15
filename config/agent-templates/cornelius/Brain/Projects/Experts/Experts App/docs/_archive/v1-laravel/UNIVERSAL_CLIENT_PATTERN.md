---
title: "Universal Client Pattern Implementation"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/universal-client-pattern"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Universal Client Pattern Implementation

## Overview

The Universal Client Pattern provides a standardized way to handle API requests across all frontend applications in the Experts Project, using the generated SDK and automatic authentication.

## Architecture Flow

```
UI Components → Hooks (useApiQuery/useApiMutation) → Repositories → @experts/sdk → Laravel API
```

## Implementation Example: Task Management

### 1. Types (`packages/core/types/src/task.ts`)

```typescript
export interface Task {
  uuid: string;
  title: string;
  status: TaskStatus;
  priority: TaskPriority;
  // ... other fields
}

export interface CreateTaskRequest {
  title: string;
  task_tag_name: string;
  // ... other fields
}
```

### 2. Repository (`packages/models/src/repositories/task-repository.ts`)

```typescript
import { TasksService } from "@experts/sdk";

export class TaskRepository {
  static async getTasks(filters: TaskFilters = {}) {
    return TasksService.listUserTasks(
      filters.tag,
      filters.status,
      filters.priority,
      // ... other parameters
    );
  }

  static async createTask(data: CreateTaskRequest) {
    return TasksService.createANewTask(data);
  }

  // ... other methods
}
```

### 3. Hooks (`packages/hooks/src/tasks/use-tasks.ts`)

```typescript
import { useApiQuery } from "../use-api-query";
import { TaskRepository } from "@experts/models";

export function useTasks(filters: TaskFilters = {}) {
  const { data, error, mutate, isLoading } = useApiQuery(
    ["tasks", filters],
    () => TaskRepository.getTasks(filters),
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
    },
    { requireAuth: true },
  );

  return {
    tasks: (data?.data as Task[]) || [],
    isLoading,
    error,
    mutate,
    refresh: () => mutate(),
  };
}
```

### 4. Mutations (`packages/hooks/src/tasks/use-task-mutations.ts`)

```typescript
import { useApiMutation } from "../use-api-mutation";

export function useTaskMutations() {
  const createTaskMutation = useApiMutation(
    "create-task",
    async (url: string, { arg }: { arg: CreateTaskRequest }) => {
      const result = await TaskRepository.createTask(arg);

      // Invalidate related caches
      mutate(["tasks"]);
      mutate(["tasks", "next"]);

      return result;
    },
  );

  return {
    createTask: createTaskMutation.trigger,
    isLoading: createTaskMutation.isMutating,
    error: createTaskMutation.error,
  };
}
```

### 5. UI Components

```tsx
import { useTasks, useTaskMutations } from "@experts/hooks";
import { toast } from "sonner";

function TaskManagement() {
  const { tasks, isLoading, tokenReady } = useTasks();
  const { createTask, isLoading: isCreating } = useTaskMutations();

  const handleCreateTask = async (taskData) => {
    try {
      await createTask(taskData);
      toast.success("Task created successfully");
    } catch (error) {
      toast.error("Failed to create task");
    }
  };

  if (!tokenReady) return <div>Authenticating...</div>;
  if (isLoading) return <div>Loading tasks...</div>;

  return (
    <div>
      <TaskForm onSubmit={handleCreateTask} isLoading={isCreating} />
      <TaskList tasks={tasks} />
    </div>
  );
}
```

## Benefits

### 1. Automatic Authentication

- No manual token management
- Automatic retry on auth failures
- Consistent auth state handling
- Loading states during authentication

### 2. Type Safety

- Generated types from OpenAPI spec
- Compile-time validation
- IntelliSense support
- Runtime type checking

### 3. Cache Management

- Automatic cache invalidation
- Smart revalidation strategies
- Request deduplication
- Background updates

### 4. Error Handling

- Consistent error patterns
- Automatic retry mechanisms
- Network error handling
- Authentication error recovery

### 5. Performance

- Request batching
- Background revalidation
- Optimistic updates
- Memory efficiency

## Authentication Flow

```typescript
// useApiQuery automatically handles:
1. Check if user is authenticated
2. Wait for token to be available
3. Include Bearer token in requests
4. Handle token refresh
5. Retry failed auth requests
6. Provide loading states

// Example with requireAuth: true
const { data, tokenReady, isAuthLoading } = useApiQuery(
  'tasks',
  () => TaskRepository.getTasks(),
  {},
  { requireAuth: true }
);

// Component handles auth states
if (isAuthLoading) return <div>Authenticating...</div>;
if (!tokenReady) return <div>Please log in</div>;
```

## Cache Invalidation Strategy

### Smart Cache Keys

```typescript
// Hierarchical cache keys for efficient invalidation
["tasks"][("tasks", filters)][("task", uuid)][("tasks", "next")]["task-tags"][ // All tasks // Filtered tasks // Specific task // Next available task // All tags
  ("task-tag", uuid)
]["admin-tasks-overview"]; // Specific tag // Dashboard overview
```

### Invalidation Rules

```typescript
// After creating a task:
mutate(["tasks"]); // Refresh task lists
mutate(["tasks", "next"]); // Update next task
mutate(["task-tags"]); // Update tag stats

// After updating a task:
mutate(["task", uuid]); // Refresh specific task
mutate(["tasks"]); // Refresh lists
mutate(["tasks", "next"]); // Update next task (if dependencies changed)

// After adding dependency:
mutate(["task", taskUuid]); // Both involved tasks
mutate(["task", dependsOnUuid]);
mutate(["tasks", "next"]); // Next task recommendations
```

## Error Recovery

### Network Errors

```typescript
// Automatic retry with exponential backoff
const { data, error } = useApiQuery("tasks", () => TaskRepository.getTasks(), {
  errorRetryCount: 3,
  errorRetryInterval: 1000,
});
```

### Authentication Errors

```typescript
// Automatic token refresh and retry
const { data, tokenReady } = useApiQuery(
  'tasks',
  () => TaskRepository.getTasks(),
  {},
  { requireAuth: true }
);

// Component handles auth recovery
if (!tokenReady) {
  return <LoginPrompt />;
}
```

## Testing

### Mock Repositories

```typescript
// Test with mocked repositories
jest.mock("@experts/models", () => ({
  TaskRepository: {
    getTasks: jest.fn(),
    createTask: jest.fn(),
  },
}));
```

### Mock Hooks

```typescript
// Test components with mocked hooks
jest.mock("@experts/hooks", () => ({
  useTasks: () => ({
    tasks: mockTasks,
    isLoading: false,
    error: null,
  }),
}));
```

## Migration Guide

### From Direct Fetch

```typescript
// Before
const response = await fetch("/api/tasks", {
  headers: { Authorization: `Bearer ${token}` },
});

// After
const { tasks } = useTasks();
```

### From createAuthenticatedServerApiClient

```typescript
// Before
const apiClient = await createAuthenticatedServerApiClient();
const response = await apiClient.get("/tasks");

// After
import { TaskRepository } from "@experts/models";
const response = await TaskRepository.getTasks();
```

### From Direct SWR

```typescript
// Before
const { data } = useSWR("tasks", () => fetch("/api/tasks"));

// After
const { tasks } = useTasks();
```

## Standards

### Repository Pattern

- Static methods for all operations
- Consistent parameter patterns
- Error handling at repository level
- Type-safe inputs and outputs

### Hook Pattern

- Use `useApiQuery` for data fetching
- Use `useApiMutation` for mutations
- Consistent return interface
- Automatic cache management

### Error Handling

- Consistent error interfaces
- Automatic retry mechanisms
- User-friendly error messages
- Graceful degradation

This pattern ensures consistency, type safety, and automatic authentication across all task management operations in the Experts Project.
