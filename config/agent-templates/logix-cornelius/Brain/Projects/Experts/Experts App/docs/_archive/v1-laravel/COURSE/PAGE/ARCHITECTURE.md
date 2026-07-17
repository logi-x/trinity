---
title: "Course Management System Architecture"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/course"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Course Management System Architecture

> **Version:** 2.0
> **Last Updated:** October 2025
> **Status:** Production Ready

## Table of Contents

1. [Overview](#overview)
2. [Architecture Principles](#architecture-principles)
3. [System Diagram](#system-diagram)
4. [Layer Architecture](#layer-architecture)
5. [Component Hierarchy](#component-hierarchy)
6. [Data Flow](#data-flow)
7. [State Management](#state-management)
8. [File Structure](#file-structure)

---

## Overview

The Course Management System is a comprehensive multi-step form wizard for creating and editing courses. It follows a **composition-based architecture** where complex functionality is built from small, focused, reusable components and hooks.

### Key Features

- ✅ Multi-step wizard (4 steps)
- ✅ Real-time auto-save (edit mode)
- ✅ Live preview with multiple modes
- ✅ Drag-and-drop curriculum builder
- ✅ Quiz creation and management
- ✅ Image upload with progress
- ✅ Form validation
- ✅ Analytics tracking
- ✅ Offline support
- ✅ Unsaved changes protection

### Design Goals

1. **Separation of Concerns**: UI, logic, and data are cleanly separated
2. **Reusability**: Components and hooks can be used across create/edit pages
3. **Testability**: Small units are easy to test in isolation
4. **Maintainability**: Clear structure makes changes predictable
5. **Performance**: Memoization and lazy loading optimize rendering

---

## Architecture Principles

### 1. Component Composition

```
Page (Orchestrator)
  ├── Layout Component (Structure)
  │     ├── Step Renderer (Content)
  │     └── Preview Content (Preview)
  └── Modals Manager (Overlays)
```

### 2. Hook Extraction

Business logic is extracted into custom hooks:

- **useCourseFormWithAnalytics**: Core form state and actions
- **useCourseFormHandlers**: Common handler functions
- **useCourseStepsConfig**: Step configuration and memoization

### 3. Unidirectional Data Flow

```
User Action → Hook Action → State Update → Component Re-render → UI Update
```

### 4. Single Responsibility

Each component/hook has one clear purpose:

- `CourseFormLayout` → Layout and navigation
- `CourseStepRenderer` → Renders active step
- `CourseModalsManager` → Manages all modals
- `CoursePreviewContent` → Preview rendering

---

## System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Course Form Page                         │
│  (CreateCoursePage / EditCoursePage)                        │
└─────────────┬───────────────────────────────────────────────┘
              │
              ├──► useCourseFormWithAnalytics()
              │    ├─► Form State (formData, errors, etc.)
              │    ├─► Step Navigation (nextStep, prevStep)
              │    ├─► CRUD Actions (add, edit, delete)
              │    ├─► Auto-save (edit mode only)
              │    └─► Analytics Tracking
              │
              ├──► useCourseFormHandlers()
              │    ├─► handleSubmit (validation + submission)
              │    ├─► handleBack (unsaved changes check)
              │    └─► canSaveDraft (draft save logic)
              │
              └──► useCourseStepsConfig()
                   └─► Memoized step configuration array
                        ├─► Step 1: Course Information
                        ├─► Step 2: Curriculum & Lessons
                        ├─► Step 3: Quizzes & Assessment
                        └─► Step 4: Review & Publish

┌─────────────────────────────────────────────────────────────┐
│                    Component Composition                     │
└─────────────┬───────────────────────────────────────────────┘
              │
              ├──► CourseFormLayout
              │    ├─► Header (title, breadcrumbs)
              │    ├─► StepIndicator (4 steps)
              │    ├─► Navigation (back, next, save, submit)
              │    ├─► Main Content (children)
              │    └─► Preview Pane (previewContent prop)
              │
              ├──► CourseStepRenderer
              │    └─► Renders step component based on activeStep
              │
              ├──► CoursePreviewContent
              │    ├─► LiveCoursePreview (lesson navigation)
              │    └─► CourseCard (course display)
              │
              └──► CourseModalsManager
                   ├─► ModuleModal
                   ├─► LessonModal
                   ├─► QuizModal
                   └─► DiscardChangesModal
```

---

## Layer Architecture

### Presentation Layer (UI Components)

**Location:** `packages/ui/src/course/*`

- `CourseFormLayout` - Main layout wrapper
- `CourseStepIndicator` - Visual step progress
- `CourseStepRenderer` - Step content renderer
- `CourseModalsManager` - Modal orchestrator
- `CourseCard` - Course display card
- `LiveCoursePreview` - Interactive preview

**Responsibility:** Pure presentation, no business logic

### Business Logic Layer (Hooks)

**Location:** `apps/experts-portal/src/app/(dashboard)/courses/shared/hooks/*`

- `useCourseFormWithAnalytics` - Core form management
- `useCourseFormHandlers` - Handler extraction
- `useCourseStepsConfig` - Step configuration

**Responsibility:** State management, actions, side effects

### Domain Layer (Step Components)

**Location:** `apps/experts-portal/src/app/(dashboard)/courses/shared/steps/*`

- `CourseInformationStep` - Basic course info
- `CourseDetailsStep` - Additional details
- `CourseCurriculumStep` - Modules and lessons
- `CourseQuizzesStep` - Quiz management
- `CourseReviewStep` - Final review

**Responsibility:** Step-specific UI and validation

### Utility Layer (Helpers & Constants)

**Location:** `apps/experts-portal/src/app/(dashboard)/courses/shared/constants/*`

- `course-form-config.ts` - Shared constants

**Responsibility:** Reusable utilities and configuration

---

## Component Hierarchy

```
CreateCoursePage / EditCoursePage
│
├─ CourseFormLayout
│  │
│  ├─ Header Section
│  │  ├─ Title ("Create New Course" / "Edit Course")
│  │  ├─ Breadcrumbs (Dashboard → Courses → Create/Edit)
│  │  └─ Auto-save Toggle (edit only)
│  │
│  ├─ Step Indicator
│  │  ├─ Step 1 Indicator
│  │  ├─ Step 2 Indicator
│  │  ├─ Step 3 Indicator
│  │  └─ Step 4 Indicator
│  │
│  ├─ Main Content Area
│  │  └─ CourseStepRenderer
│  │     ├─ Step 1: CourseInformationStep + CourseDetailsStep
│  │     ├─ Step 2: CourseCurriculumStep
│  │     ├─ Step 3: CourseQuizzesStep
│  │     └─ Step 4: CourseReviewStep
│  │
│  ├─ Preview Pane
│  │  └─ CoursePreviewContent
│  │     ├─ LiveCoursePreview
│  │     └─ CourseCard
│  │
│  └─ Navigation Footer
│     ├─ Back Button
│     ├─ Save Draft Button (if canSaveDraft)
│     ├─ Next Button
│     └─ Submit Button (step 4 only)
│
└─ CourseModalsManager
   ├─ ModuleModal (add/edit modules)
   ├─ LessonModal (add/edit lessons)
   ├─ QuizModal (add/edit quizzes)
   └─ DiscardChangesModal (unsaved changes warning)
```

---

## Data Flow

### 1. Form Initialization

```typescript
// Create Mode
const courseForm = useCourseFormWithAnalytics();
// Form starts with empty formData

// Edit Mode
const { data: course } = useCourse(uuid);
const courseForm = useCourseFormWithAnalytics(course);
// Form pre-populated with existing course data
```

### 2. User Input Flow

```
User types in input field
       ↓
onChange event fired
       ↓
updateField("title", value)
       ↓
formData state updated
       ↓
Component re-renders with new value
       ↓
Auto-save triggered (edit mode, debounced)
```

### 3. Step Navigation Flow

```
User clicks "Next"
       ↓
Validation runs for current step
       ↓
If valid: nextStep() → activeStep incremented
       ↓
If invalid: errors shown, navigation blocked
       ↓
CourseStepRenderer shows new step component
```

### 4. Submission Flow

```
User clicks "Publish Course" / "Update Course"
       ↓
handleSubmit() called
       ↓
validateForm(formData) runs
       ↓
If valid: submitForm() → API call → Success/Error
       ↓
If invalid: toast.error() → Form stays on current step
```

### 5. Modal Flow

```
User clicks "Add Module"
       ↓
openModuleModal() called
       ↓
Modal state updated in courseForm
       ↓
CourseModalsManager detects state change
       ↓
ModuleModal renders
       ↓
User submits modal
       ↓
Module added to formData.modules[]
       ↓
Modal closed
```

---

## State Management

### Primary State Container

**useCourseFormWithAnalytics** manages all form state:

```typescript
{
  // Form Data
  formData: CourseFormData,
  errors: Record<string, string>,
  hasUnsavedChanges: boolean,

  // Step Navigation
  activeStep: number,

  // Auto-save (edit mode)
  isAutoSaving: boolean,
  lastAutoSave: Date | null,
  isAutoSaveEnabled: boolean,

  // Preview
  previewMode: 'partial' | 'expanded' | 'minimized',
  selectedLessonIndex: number,
  completedLessons: Set<string>,

  // Upload
  previewImage: string | null,
  uploadProgress: number,
  isUploading: boolean,

  // Quiz
  showQuiz: boolean,
  quizAnswers: Record<string, string>,
  quizCompleted: boolean,
  quizScore: number,

  // Modals
  isModuleModalOpen: boolean,
  isLessonModalOpen: boolean,
  isQuizModalOpen: boolean,
  isDiscardModalOpen: boolean,
  editingModule: Module | null,
  editingLesson: Lesson | null,
  editingQuiz: Quiz | null,
}
```

### Derived State

**useCourseFormHandlers** provides computed values:

```typescript
{
  handleSubmit: () => Promise<void>,
  handleBack: () => void,
  canSaveDraft: boolean, // Computed from formData + hasUnsavedChanges
}
```

### Memoized Configuration

**useCourseStepsConfig** returns memoized step array:

```typescript
[
  { step: 1, title: "Course Information", component: <Step1 /> },
  { step: 2, title: "Curriculum & Lessons", component: <Step2 /> },
  { step: 3, title: "Quizzes & Assessment", component: <Step3 /> },
  { step: 4, title: "Review & Publish", component: <Step4 /> },
]
```

### State Updates

All state updates go through hook actions:

```typescript
// ✅ Correct
updateField("title", "New Title");
nextStep();
openModuleModal();

// ❌ Incorrect (direct state mutation)
formData.title = "New Title";
activeStep++;
```

---

## File Structure

```
apps/experts-portal/src/app/(dashboard)/courses/
│
├── create/
│   ├── page.tsx                    # Create page (172 lines)
│   └── __tests__/
│       └── page.test.tsx           # Integration tests
│
├── [uuid]/
│   ├── edit/
│   │   ├── page.tsx                # Edit page (235 lines)
│   │   └── __tests__/
│   │       └── page.test.tsx       # Integration tests
│   └── preview/
│       └── page.tsx                # Preview page
│
├── shared/
│   ├── components/
│   │   ├── course-preview-content.tsx  # Preview composition
│   │   ├── live-preview.tsx
│   │   └── __tests__/
│   │       └── course-preview-content.test.tsx
│   │
│   ├── constants/
│   │   └── course-form-config.ts   # Shared constants
│   │
│   ├── hooks/
│   │   ├── use-course-form-handlers.ts     # Handler extraction
│   │   ├── use-course-steps-config.tsx     # Step configuration
│   │   └── __tests__/
│   │       ├── use-course-form-handlers.test.ts
│   │       └── use-course-steps-config.test.tsx
│   │
│   ├── modals/
│   │   ├── module-modal.tsx
│   │   ├── lesson-modal.tsx
│   │   ├── quiz-modal.tsx
│   │   └── discard-changes-modal.tsx
│   │
│   ├── steps/
│   │   ├── course-information-step.tsx
│   │   ├── course-details-step.tsx
│   │   ├── course-curriculum-step.tsx
│   │   ├── course-quizzes-step.tsx
│   │   └── course-review-step.tsx
│   │
│   └── sortables/
│       ├── sortable-list.tsx
│       ├── module-sortable-item.tsx
│       └── lesson-sortable-item.tsx
│
└── page.tsx                        # Courses list page
```

---

## Performance Optimizations

### 1. Memoization

```typescript
// Step config is memoized to prevent recreation
const courseSteps = useCourseStepsConfig({ ...props });
// Only recreates when dependencies change
```

### 2. Lazy Loading

```typescript
// Modals are only rendered when needed
{isModuleModalOpen && <ModuleModal {...props} />}
```

### 3. Debounced Auto-save

```typescript
// Auto-save waits 2 seconds after last change
useDebounce(formData, 2000);
```

### 4. Optimistic Updates

```typescript
// UI updates immediately, API call happens async
addModule(newModule); // Updates state immediately
await saveToServer(newModule); // Background save
```

### 5. Code Splitting

```typescript
// Large components loaded on-demand
const QuizEditor = lazy(() => import("./quiz-editor"));
```

---

## Security Considerations

### 1. Input Validation

- Client-side validation in `validateForm()`
- Server-side validation in API
- XSS protection via React's built-in escaping

### 2. Authorization

- Edit pages check course ownership
- API endpoints verify user permissions
- 403/404 errors handled gracefully

### 3. Data Sanitization

- File uploads validated (type, size)
- URLs validated and sanitized
- Rich text content sanitized

---

## Error Handling

### 1. Form Validation Errors

```typescript
errors: {
  title: "Title is required",
  price: "Price must be a positive number"
}
```

### 2. Network Errors

```typescript
try {
  await submitForm();
} catch (error) {
  toast.error("Failed to save course");
}
```

### 3. Loading States

```typescript
{isLoading && <Spinner />}
{error && <ErrorMessage error={error} />}
{data && <CourseForm data={data} />}
```

---

## Accessibility

### 1. Keyboard Navigation

- All interactive elements keyboard accessible
- Step navigation via Tab/Enter
- Modal focus trapping

### 2. Screen Reader Support

- ARIA labels on all inputs
- Step indicator announces progress
- Error messages announced

### 3. Focus Management

- Focus moves to errors on validation
- Modal focuses first input on open
- Focus returns to trigger on modal close

---

## Browser Support

- **Chrome/Edge**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Mobile Safari**: 14+
- **Chrome Android**: 90+

---

## Dependencies

### Core Dependencies

- **React**: ^18.3.1 (UI framework)
- **Next.js**: 15.0.0 (Framework)
- **TypeScript**: ^5.7.2 (Type safety)

### UI Dependencies

- **@nextui-org/react**: ^2.6.10 (Component library)
- **framer-motion**: ^11.15.0 (Animations)
- **react-beautiful-dnd**: Drag and drop

### Form Dependencies

- **zod**: Validation schemas
- **sonner**: Toast notifications

### Utilities

- **swr**: Data fetching
- **lodash**: Utility functions

---

## Next Steps

1. Read [API_REFERENCE.md](../API_REFERENCE.md) for detailed hook/component APIs
2. Read [USAGE_GUIDE.md](../USAGE_GUIDE.md) for practical examples
3. Read [MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md) if migrating from old system
4. Read [BEST_PRACTICES.md](../BEST_PRACTICES.md) for patterns and conventions
5. Read [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) for common issues

---

## Contributing

When modifying the course form system:

1. Maintain separation of concerns
2. Add tests for new features
3. Update documentation
4. Follow existing patterns
5. Consider performance implications

---

**Questions?** Contact the Logix Development Team
