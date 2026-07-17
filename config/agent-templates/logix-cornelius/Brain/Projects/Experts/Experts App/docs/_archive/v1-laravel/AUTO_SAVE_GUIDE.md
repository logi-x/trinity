---
title: "Auto-Save and Draft Management Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/auto-save-guide"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Auto-Save and Draft Management Guide

This guide covers the robust auto-save and draft management system implemented in the Experts platform.

## Features

### 1. Auto-Save Functionality

- **Debounced Auto-Save**: Automatically saves form data every 2 seconds after changes stop
- **Retry Mechanism**: Implements exponential backoff for failed auto-save attempts
- **Offline Support**: Falls back to localStorage when offline
- **Visual Feedback**: Shows auto-save status with loading indicators

### 2. Draft Management

- **Server-Side Drafts**: Utilizes the course revisions table for persistent draft storage
- **Local Backup**: Maintains localStorage backup for offline scenarios
- **Draft Recovery**: Automatically detects and offers to restore unsaved drafts
- **Conflict Resolution**: Handles conflicts between local and server versions

### 3. Data Integrity

- **Version Control**: Tracks form versions to prevent overwrites
- **Timestamp Tracking**: Maintains creation and modification timestamps
- **Cleanup**: Automatically removes stale localStorage data

## Implementation Details

### Auto-Save Hook

```typescript
const useAutoSave = (
  courseId: string | null,
  formData: CourseFormData,
  hasUnsavedChanges: boolean,
  setLastAutoSave: (date: Date | null) => void,
  setHasUnsavedChanges: (value: boolean) => void,
) => {
  // Debounced form data to prevent excessive API calls
  const [debouncedFormData] = useDebounce(formData, 2000);

  // Network status monitoring
  const [isOnline, setIsOnline] = React.useState(true);

  // Retry mechanism with exponential backoff
  const [retryCount, setRetryCount] = React.useState(0);

  // Auto-save implementation with error handling
  // ...
};
```
