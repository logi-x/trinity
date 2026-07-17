---
title: "Course Form Architecture"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/course"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Course Form Architecture

## Overview

The course form has been refactored from a monolithic 1550-line hook into a well-structured composition of specialized hooks. The main `useCourseForm` hook now serves as an orchestration layer that delegates specific concerns to focused, reusable hooks.

## Hook Composition

### Main Orchestrator

- **`useCourseForm`** (761 lines, down from 1550)
  - Composes all specialized hooks
  - Handles form submission and draft saving
  - Manages file uploads (images, videos)
  - Provides utility functions for data access
  - Loads and synchronizes course data

### Specialized Hooks

#### 1. Modal Management

- **`useCourseModals`** - Manages all modal states and interactions
  - Lesson modal (create/edit)
  - Module modal (create/edit)
  - Quiz modal (create/edit)
  - Discard changes modal
  - Tracks current editing items and IDs

#### 2. Step Navigation

- **`useCourseSteps`** - Handles multi-step form navigation
  - Step validation using Zod schemas
  - Step completion tracking
  - URL synchronization
  - Navigation controls (next, prev, goToStep)

#### 3. Module CRUD

- **`useModuleCrud`** - Module operations
  - Add, edit, delete, save modules
  - Module reordering
  - Module sorting and finding

#### 4. Lesson CRUD

- **`useLessonCrud`** - Lesson operations
  - Add, edit, delete, save lessons
  - Cross-module lesson management
  - Lesson reordering within and across modules
  - Duration calculation

#### 5. Quiz CRUD

- **`useQuizCrud`** - Quiz and question operations
  - Add, edit, delete, save quizzes
  - Quiz validation (centralized)
  - Question management (add, update, delete)

#### 6. Preview Mode

- **`useCoursePreview`** - Course preview functionality
  - Preview mode toggle (expanded/hidden/partial)
  - Lesson selection and navigation
  - Quiz interactions during preview
  - Lesson completion tracking

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      useCourseForm                          │
│                   (Orchestration Layer)                     │
└─────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  useCourseModals│  │ useCourseSteps  │  │  useModuleCrud  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  useLessonCrud  │  │  useQuizCrud    │  │ useCoursePreview│
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                    │                    │
         └────────────────────┴────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   useFormState  │
                    │  (Form Data)    │
                    └─────────────────┘
```

## Benefits

### 1. Separation of Concerns

Each hook has a single, well-defined responsibility:

- Modals → Modal state management
- Steps → Navigation and validation
- CRUD hooks → Entity-specific operations
- Preview → Preview mode interactions

### 2. Reusability

All specialized hooks can be used independently:

```tsx
// Use just the module operations in another component
const moduleOps = useModuleCrud({ getModules, setModules, courseUuid, modals });
```

### 3. Testability

Each hook can be tested in isolation:

```tsx
// Test module CRUD without the entire form
test("should add module", () => {
  const { result } = renderHook(() => useModuleCrud(config));
  act(() => result.current.addModule());
  expect(result.current.getModules()).toHaveLength(1);
});
```

### 4. Maintainability

- Smaller, focused files (~200-350 lines each)
- Clear boundaries between concerns
- Easy to locate and fix bugs
- Predictable API patterns

### 5. Performance

- Hooks can be memoized independently
- Reduces unnecessary re-renders
- Better code splitting opportunities

## File Structure

```
packages/hooks/src/courses/
├── use-course-form.ts          (761 lines) - Main orchestrator
├── use-course-modals.ts         (181 lines) - Modal management
├── use-course-steps.ts          (302 lines) - Step navigation
├── use-module-crud.ts           (256 lines) - Module CRUD
├── use-lesson-crud.ts           (420 lines) - Lesson CRUD
├── use-quiz-crud.ts             (362 lines) - Quiz CRUD
├── use-preview.ts               (223 lines) - Preview mode
├── use-form-state.ts                        - Form state management
├── actions/
│   ├── use-create-course.ts                 - Course creation API
│   └── use-update-course.ts                 - Course update API
└── index.ts                                 - Public exports
```

## Metrics

### Before Refactoring

- **useCourseForm**: 1550 lines
- **Hooks**: 1 monolithic hook
- **Testability**: Low (everything coupled)
- **Reusability**: None

### After Refactoring

- **useCourseForm**: 761 lines (51% reduction)
- **Total extracted code**: ~1750 lines (in 6 specialized hooks)
- **Hooks**: 7 focused hooks
- **Testability**: High (each hook isolated)
- **Reusability**: High (all hooks reusable)

## Usage Example

```tsx
function CourseEditor({ courseUuid }: { courseUuid?: string }) {
  const courseForm = useCourseForm(courseUuid);

  return (
    <div>
      {/* Step navigation */}
      <StepIndicator
        activeStep={courseForm.activeStep}
        onStepClick={courseForm.goToStep}
      />

      {/* Module management */}
      <button onClick={courseForm.addModule}>Add Module</button>

      {/* Lesson management */}
      <button onClick={() => courseForm.addLesson(moduleUuid)}>
        Add Lesson
      </button>

      {/* Preview mode */}
      <PreviewToggle
        mode={courseForm.previewMode}
        onChange={courseForm.setPreviewMode}
      />

      {/* Form submission */}
      <button onClick={courseForm.submitForm}>Save Course</button>
    </div>
  );
}
```

## Future Improvements

1. **Extract File Upload Hook**
   - `useFileUpload` for image/video handling
   - Reusable across other forms

2. **Extract Auto-save Hook**
   - `useAutoSave` for automatic draft saving
   - Configurable debounce and cooldown

3. **Add Integration Tests**
   - Test hook composition
   - Test data flow between hooks

4. **Performance Optimization**
   - Selective memoization
   - Virtual scrolling for large lists

5. **Type Safety Improvements**
   - Stricter generic types
   - Discriminated unions for state

## Migration Guide

If you're updating code that uses the old `useCourseForm`:

### ✅ No Changes Needed

The public API remains the same. All operations are still available:

```tsx
// Still works exactly the same
courseForm.addModule();
courseForm.addLesson();
courseForm.nextStep();
```

### ⚠️ Internal Changes

If you were accessing internal state directly, update to use the returned values:

```tsx
// Old (if you were doing this)
const modules = courseForm.formState.formData.modules;

// New (recommended)
const modules = courseForm.formData.modules;
```

## Contributing

When adding new features:

1. **Identify the concern**: Does it belong in an existing hook?
2. **Create focused hook**: If it's a new concern, create a new specialized hook
3. **Compose in main hook**: Integrate into `useCourseForm` orchestrator
4. **Follow patterns**: Use the same patterns as existing hooks
5. **Add tests**: Test the hook in isolation
6. **Update docs**: Document the new hook and its API
