---
title: "Form State Management with URL Persistence & Auto-Save"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/course"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Form State Management with URL Persistence & Auto-Save

This document explains the new robust form state management system that provides URL persistence and reliable auto-save functionality.

## Overview

The new system consists of two main hooks:

1. `useFormState` - Base hook for any form with URL persistence and auto-save
2. `useCourseForm` - Specialized hook for course creation with additional features

## Features

### ✅ URL State Persistence

- Form state is automatically synced with URL parameters
- Page refresh preserves the current state
- Browser back/forward navigation works correctly
- Shareable URLs with form state

### ✅ Reliable Auto-Save

- Debounced auto-save (2 seconds after changes stop)
- Retry mechanism with exponential backoff
- Offline support with localStorage fallback
- Visual feedback for save status
- Network status monitoring

### ✅ Draft Management

- Server-side draft storage
- Local backup for offline scenarios
- Draft recovery on page load
- Conflict resolution between local and server versions

### ✅ Form Validation

- Real-time validation
- Step-by-step validation
- Error clearing on field changes
- Validation state persistence

## Basic Usage

### Using `useFormState` for any form

```typescript
import { useFormState } from '@experts/hooks';

interface MyFormData {
  title: string;
  description: string;
  category: string;
  isPublished: boolean;
}

function MyForm() {
  const {
    formData,
    errors,
    hasUnsavedChanges,
    isAutoSaving,
    lastAutoSave,
    isOnline,
    updateField,
    validateForm,
    saveDraft,
    submitForm,
  } = useFormState<MyFormData>({
    // URL state configuration
    urlStateKeys: ['title', 'description', 'category'],
    defaultValues: {
      title: '',
      description: '',
      category: '',
      isPublished: false,
    },

    // Auto-save configuration
    autoSaveEnabled: true,
    autoSaveDelay: 2000,
    localStorageKey: 'my-form-draft',

    // Validation
    validate: (data) => {
      const errors: Record<string, string> = {};
      if (!data.title) errors.title = 'Title is required';
      if (!data.description) errors.description = 'Description is required';
      return { isValid: Object.keys(errors).length === 0, errors };
    },

    // Auto-save callback
    onAutoSave: async (data) => {
      await fetch('/api/drafts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
    },
  });

  return (
    <form>
      <input
        value={formData.title}
        onChange={(e) => updateField('title', e.target.value)}
        className={errors.title ? 'border-red-500' : ''}
      />
      {errors.title && <span className="text-red-500">{errors.title}</span>}

      {/* Auto-save status */}
      {isAutoSaving && <span>Auto-saving...</span>}
      {lastAutoSave && <span>Last saved: {lastAutoSave.toLocaleTimeString()}</span>}
      {!isOnline && <span>Offline - changes saved locally</span>}

      <button onClick={saveDraft}>Save Draft</button>
      <button onClick={submitForm}>Submit</button>
    </form>
  );
}
```

### Using `useCourseForm` for course creation

```typescript
import { useCourseForm } from '@experts/hooks';

function CreateCoursePage() {
  const {
    // Form state
    formData,
    errors,
    hasUnsavedChanges,
    isAutoSaving,
    lastAutoSave,
    isOnline,

    // UI state
    activeStep,
    completedSteps,
    previewMode,
    selectedLessonIndex,

    // Modal states
    isLessonModalOpen,
    isQuizModalOpen,

    // Actions
    nextStep,
    prevStep,
    addLesson,
    editLesson,
    deleteLesson,
    saveLesson,
    submitForm,
    setPreviewMode,

    // Form actions
    updateField,
    validateForm,
    saveDraft,
  } = useCourseForm();

  return (
    <div>
      {/* Step indicator */}
      <div className="flex items-center gap-4">
        {['Course Info', 'Details', 'Curriculum', 'Quizzes', 'Review'].map((title, index) => (
          <div key={index} className="flex items-center gap-2">
            <div className={`w-8 h-8 rounded-full ${
              activeStep > index + 1 ? 'bg-green-500' :
              activeStep === index + 1 ? 'bg-blue-500' : 'bg-gray-300'
            }`}>
              {activeStep > index + 1 ? '✓' : index + 1}
            </div>
            <span>{title}</span>
          </div>
        ))}
      </div>

      {/* Auto-save status */}
      <div className="flex items-center gap-2">
        {isAutoSaving && <span>Auto-saving...</span>}
        {lastAutoSave && <span>Last saved: {lastAutoSave.toLocaleTimeString()}</span>}
        {!isOnline && <span>Offline</span>}
      </div>

      {/* Form content based on step */}
      {activeStep === 1 && (
        <div>
          <input
            value={formData.title}
            onChange={(e) => updateField('title', e.target.value)}
            placeholder="Course Title"
          />
          {errors.title && <span className="text-red-500">{errors.title}</span>}
        </div>
      )}

      {/* Navigation */}
      <div className="flex justify-between">
        <button onClick={prevStep} disabled={activeStep === 1}>
          Previous
        </button>
        <button onClick={nextStep} disabled={activeStep === 5}>
          Next
        </button>
      </div>

      {/* Actions */}
      <button onClick={saveDraft}>Save Draft</button>
      <button onClick={submitForm}>Publish Course</button>
    </div>
  );
}
```

## URL State Management

### How it works

1. **Initialization**: Form state is initialized from URL parameters first, then localStorage, then defaults
2. **Sync**: When form data changes, URL is automatically updated
3. **Persistence**: URL parameters persist across page refreshes and navigation

### URL Parameters

The form state is stored in URL parameters like this:

```
/courses/create?step=2&title=My%20Course&category=Programming&preview_mode=expanded
```

### Supported Data Types

- **Strings**: Stored as-is
- **Numbers**: Stored as strings, parsed back to numbers
- **Booleans**: Stored as "true"/"false" strings
- **Objects**: JSON stringified and stored
- **Arrays**: JSON stringified and stored

### Configuration

```typescript
const formConfig = {
  urlStateKeys: ["title", "description", "category", "isPublished"], // Only these fields sync to URL
  defaultValues: {
    /* ... */
  },
  // ... other config
};
```

## Auto-Save System

### How it works

1. **Debouncing**: Changes are debounced for 2 seconds (configurable)
2. **Network Check**: Only saves when online
3. **Retry Logic**: Failed saves retry with exponential backoff
4. **Local Backup**: Always saves to localStorage as backup
5. **Visual Feedback**: Shows save status to user

### Configuration

```typescript
const formConfig = {
  autoSaveEnabled: true, // Enable/disable auto-save
  autoSaveDelay: 2000, // Debounce delay in milliseconds
  localStorageKey: "form-draft", // localStorage key for backup
  onAutoSave: async (data) => {
    // Custom save function
    await saveToServer(data);
  },
};
```

### Auto-Save States

- **Saving**: `isAutoSaving = true`
- **Saved**: `lastAutoSave = Date`
- **Failed**: Error toast + localStorage backup
- **Offline**: Local storage only + warning

## Draft Management

### Server-Side Drafts

Drafts are saved to the server using the `onAutoSave` callback:

```typescript
const handleAutoSave = async (data: FormData) => {
  if (!draftId) {
    // Create new draft
    const response = await fetch("/api/drafts", {
      method: "POST",
      body: JSON.stringify(data),
    });
    const result = await response.json();
    setDraftId(result.id);
  } else {
    // Update existing draft
    await fetch(`/api/drafts/${draftId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }
};
```

### Local Storage Backup

Every auto-save also creates a local backup:

```typescript
// Automatically handled by the hook
localStorage.setItem(
  "form-draft",
  JSON.stringify({
    timestamp: Date.now(),
    data: formData,
    version: Date.now(),
  }),
);
```

### Draft Recovery

On page load, the system checks for existing drafts:

```typescript
// Automatically handled by the hook
const localData = getInitialDataFromLocalStorage("form-draft");
if (localData && isRecent(localData.timestamp)) {
  // Offer to restore draft
  showRestorePrompt(localData);
}
```

## Validation System

### Real-time Validation

Validation runs automatically when fields change:

```typescript
const validateForm = (data: FormData) => {
  const errors: Record<string, string> = {};

  if (!data.title?.trim()) {
    errors.title = "Title is required";
  }

  if (data.description && data.description.length < 50) {
    errors.description = "Description must be at least 50 characters";
  }

  return { isValid: Object.keys(errors).length === 0, errors };
};
```

### Step Validation

For multi-step forms, validation can be step-specific:

```typescript
const validateStep = (step: number, data: FormData) => {
  const errors: Record<string, string> = {};

  switch (step) {
    case 1:
      if (!data.title) errors.title = "Title is required";
      if (!data.description) errors.description = "Description is required";
      break;
    case 2:
      if (!data.category) errors.category = "Category is required";
      if (!data.price) errors.price = "Price is required";
      break;
  }

  return { isValid: Object.keys(errors).length === 0, errors };
};
```

## Error Handling

### Network Errors

```typescript
// Auto-save errors are handled automatically
const handleAutoSave = async (data: FormData) => {
  try {
    await saveToServer(data);
  } catch (error) {
    // Error is handled by the hook
    // - Shows error toast
    // - Saves to localStorage as backup
    // - Retries with exponential backoff
  }
};
```

### Validation Errors

```typescript
// Validation errors are displayed inline
<input
  value={formData.title}
  onChange={(e) => updateField('title', e.target.value)}
  className={errors.title ? 'border-red-500' : ''}
/>
{errors.title && <span className="text-red-500">{errors.title}</span>}
```

## Best Practices

### 1. Configure URL State Keys

Only sync important fields to URL to avoid long URLs:

```typescript
urlStateKeys: ['title', 'category', 'step'], // Don't include large objects
```

### 2. Handle Large Data

For large form data, use localStorage for backup but not URL:

```typescript
const formConfig = {
  urlStateKeys: ["step", "previewMode"], // Small state only
  localStorageKey: "large-form-data", // Full data backup
};
```

### 3. Custom Auto-Save Logic

Implement custom auto-save for your specific needs:

```typescript
const handleAutoSave = async (data: FormData) => {
  // Only save if user has made significant changes
  if (hasSignificantChanges(data)) {
    await saveToServer(data);
  }
};
```

### 4. Conflict Resolution

Handle conflicts between local and server data:

```typescript
const handleConflict = (localData: FormData, serverData: FormData) => {
  // Show conflict resolution UI
  showConflictModal({
    localData,
    serverData,
    onUseLocal: () => setFormData(localData),
    onUseServer: () => setFormData(serverData),
  });
};
```

### 5. Performance Optimization

For large forms, optimize performance:

```typescript
const formConfig = {
  autoSaveDelay: 3000, // Longer delay for large forms
  urlStateKeys: ["step"], // Minimal URL state
  validate: debounce(validateForm, 500), // Debounce validation
};
```

## Migration Guide

### From Old System

1. **Replace useState with useFormState**:

```typescript
// Old
const [formData, setFormData] = useState(defaultData);
const [errors, setErrors] = useState({});

// New
const { formData, errors, updateField } = useFormState(config);
```

2. **Replace manual auto-save with hook**:

```typescript
// Old
useEffect(() => {
  const timer = setTimeout(() => saveToServer(formData), 2000);
  return () => clearTimeout(timer);
}, [formData]);

// New
const formConfig = {
  onAutoSave: saveToServer,
  autoSaveDelay: 2000,
};
```

3. **Replace manual URL sync with hook**:

```typescript
// Old
useEffect(() => {
  const params = new URLSearchParams();
  params.set("step", activeStep.toString());
  router.replace(`?${params.toString()}`);
}, [activeStep]);

// New
const formConfig = {
  urlStateKeys: ["step"],
};
```

## Troubleshooting

### Common Issues

1. **URL too long**: Reduce `urlStateKeys` to only essential fields
2. **Auto-save not working**: Check network status and `onAutoSave` callback
3. **State not persisting**: Verify `localStorageKey` is set correctly
4. **Validation errors**: Ensure validation function returns correct format

### Debug Mode

Enable debug logging:

```typescript
const formConfig = {
  debug: true, // Enable console logging
  // ... other config
};
```

### Performance Issues

- Increase `autoSaveDelay` for large forms
- Reduce `urlStateKeys` to minimum
- Debounce validation function
- Use `useMemo` for expensive computations

## API Reference

### useFormState

```typescript
function useFormState<T>(config: FormStateConfig<T>): FormStateReturn<T>;
```

#### Config Options

- `urlStateKeys`: Array of field names to sync to URL
- `defaultValues`: Initial form data
- `autoSaveEnabled`: Enable/disable auto-save (default: true)
- `autoSaveDelay`: Debounce delay in ms (default: 2000)
- `localStorageKey`: Key for localStorage backup
- `validate`: Validation function
- `onAutoSave`: Auto-save callback
- `onStateChange`: Field change callback
- `onConflict`: Conflict resolution callback

#### Return Values

- `formData`: Current form data
- `errors`: Validation errors
- `hasUnsavedChanges`: Whether form has unsaved changes
- `isAutoSaving`: Whether auto-save is in progress
- `lastAutoSave`: Timestamp of last successful save
- `isOnline`: Network connectivity status
- `updateField`: Update a single field
- `setFormData`: Update multiple fields
- `validateForm`: Run validation
- `saveDraft`: Manually save draft
- `submitForm`: Submit the form

### useCourseForm

```typescript
function useCourseForm(courseId?: number): CourseFormState & CourseFormActions;
```

#### Additional Features

- Step navigation (`nextStep`, `prevStep`, `goToStep`)
- Lesson management (`addLesson`, `editLesson`, `deleteLesson`)
- Quiz management (`addQuiz`, `editQuiz`, `deleteQuiz`)
- Modal controls (`openLessonModal`, `closeLessonModal`)
- Preview controls (`setPreviewMode`, `selectLesson`)

## Examples

See the example implementation in `apps/experts-portal/src/app/(main)/courses/create/page-with-hooks.tsx` for a complete working example.
