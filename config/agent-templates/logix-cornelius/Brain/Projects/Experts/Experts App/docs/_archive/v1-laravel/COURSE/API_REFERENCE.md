---
title: "Course Management API Reference"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/course"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Course Management API Reference

> **Version:** 2.0
> **Last Updated:** October 2025

Complete API documentation for all hooks, components, and utilities in the course management system.

## Table of Contents

1. [Hooks](#hooks)
   - [useCourseFormWithAnalytics](#usecourseformwithanalytics)
   - [useCourseFormHandlers](#usecourseformhandlers)
   - [useCourseStepsConfig](#usecoursestepsconfig)
2. [Components](#components)
   - [CourseFormLayout](#courseformlayout)
   - [CourseStepRenderer](#coursesteprenderer)
   - [CourseModalsManager](#coursemodalsmanager)
   - [CoursePreviewContent](#coursepreviewcontent)
3. [Constants](#constants)
4. [Types](#types)

---

## Hooks

### useCourseFormWithAnalytics

**Location:** `@experts/hooks`

The primary hook for managing course form state and actions. Handles form data, validation, step navigation, auto-save (edit mode), and analytics tracking.

#### Signature

```typescript
function useCourseFormWithAnalytics(
  initialCourse?: Course,
): UseCourseFormWithAnalyticsReturn;
```

#### Parameters

| Parameter       | Type                  | Required | Description                                             |
| --------------- | --------------------- | -------- | ------------------------------------------------------- |
| `initialCourse` | `Course \| undefined` | No       | Pre-populate form with existing course data (edit mode) |

#### Return Value

Returns an object with the following properties and methods:

##### Form State

| Property            | Type                     | Description                      |
| ------------------- | ------------------------ | -------------------------------- |
| `formData`          | `CourseFormData`         | Current form data                |
| `errors`            | `Record<string, string>` | Validation errors by field name  |
| `hasUnsavedChanges` | `boolean`                | Whether form has unsaved changes |
| `courseUuid`        | `string \| null`         | Course UUID (edit mode only)     |

##### Step Navigation

| Property     | Type                     | Description               |
| ------------ | ------------------------ | ------------------------- |
| `activeStep` | `number`                 | Current step (1-4)        |
| `nextStep`   | `() => void`             | Navigate to next step     |
| `prevStep`   | `() => void`             | Navigate to previous step |
| `goToStep`   | `(step: number) => void` | Jump to specific step     |

##### Auto-save (Edit Mode)

| Property            | Type           | Description                            |
| ------------------- | -------------- | -------------------------------------- |
| `isAutoSaving`      | `boolean`      | Whether auto-save is in progress       |
| `lastAutoSave`      | `Date \| null` | Timestamp of last successful auto-save |
| `isAutoSaveEnabled` | `boolean`      | Whether auto-save is enabled           |
| `isOnline`          | `boolean`      | Network connectivity status            |
| `toggleAutoSave`    | `() => void`   | Toggle auto-save on/off                |

##### Preview State

| Property               | Type                                     | Description                         |
| ---------------------- | ---------------------------------------- | ----------------------------------- |
| `previewMode`          | `'partial' \| 'expanded' \| 'minimized'` | Current preview mode                |
| `selectedLessonIndex`  | `number`                                 | Index of selected lesson in preview |
| `completedLessons`     | `Set<string>`                            | Set of completed lesson IDs         |
| `setPreviewMode`       | `(mode) => void`                         | Update preview mode                 |
| `handleLessonSelect`   | `(index: number) => void`                | Select lesson in preview            |
| `handleCompleteLesson` | `(lessonId: string) => void`             | Mark lesson as completed            |

##### Upload State

| Property            | Type                            | Description                   |
| ------------------- | ------------------------------- | ----------------------------- |
| `previewImage`      | `string \| null`                | Preview URL of uploaded image |
| `uploadProgress`    | `number`                        | Upload progress (0-100)       |
| `isUploading`       | `boolean`                       | Whether upload is in progress |
| `setPreviewImage`   | `(url: string \| null) => void` | Update preview image          |
| `handleImageChange` | `(file: File) => Promise<void>` | Handle image upload           |

##### Quiz State

| Property           | Type                                           | Description               |
| ------------------ | ---------------------------------------------- | ------------------------- |
| `showQuiz`         | `boolean`                                      | Whether quiz is visible   |
| `quizAnswers`      | `Record<string, string>`                       | User's quiz answers       |
| `quizCompleted`    | `boolean`                                      | Whether quiz is completed |
| `quizScore`        | `number`                                       | Quiz score (0-100)        |
| `setShowQuiz`      | `(show: boolean) => void`                      | Toggle quiz visibility    |
| `setQuizAnswers`   | `(answers) => void`                            | Update quiz answers       |
| `setQuizCompleted` | `(completed: boolean) => void`                 | Mark quiz as completed    |
| `setQuizScore`     | `(score: number) => void`                      | Update quiz score         |
| `handleQuizAnswer` | `(questionId: string, answer: string) => void` | Record quiz answer        |
| `handleSubmitQuiz` | `() => void`                                   | Submit quiz for grading   |

##### Form Actions

| Property          | Type                                                                           | Description                    |
| ----------------- | ------------------------------------------------------------------------------ | ------------------------------ |
| `updateField`     | `<K extends keyof CourseFormData>(field: K, value: CourseFormData[K]) => void` | Update a form field            |
| `validateForm`    | `(data?: CourseFormData) => boolean`                                           | Validate form data             |
| `submitForm`      | `() => Promise<void>`                                                          | Submit form (create or update) |
| `handleSaveDraft` | `() => Promise<void>`                                                          | Save as draft                  |
| `handleCopyLink`  | `() => void`                                                                   | Copy course link to clipboard  |

##### Module Actions

| Property           | Type                          | Description                |
| ------------------ | ----------------------------- | -------------------------- |
| `openModuleModal`  | `() => void`                  | Open module creation modal |
| `editModule`       | `(module: Module) => void`    | Edit existing module       |
| `deleteModule`     | `(moduleId: string) => void`  | Delete module              |
| `onReorderModules` | `(modules: Module[]) => void` | Reorder modules            |

##### Lesson Actions

| Property           | Type                                                 | Description                     |
| ------------------ | ---------------------------------------------------- | ------------------------------- |
| `addLesson`        | `(moduleId: string) => void`                         | Add lesson to module            |
| `editLesson`       | `(lesson: Lesson) => void`                           | Edit existing lesson            |
| `deleteLesson`     | `(lessonId: string) => void`                         | Delete lesson                   |
| `onReorderLessons` | `(moduleId: string, lessons: Lesson[]) => void`      | Reorder lessons within module   |
| `onMoveLesson`     | `(lessonId: string, targetModuleId: string) => void` | Move lesson to different module |

##### Quiz Actions

| Property          | Type                         | Description        |
| ----------------- | ---------------------------- | ------------------ |
| `editQuiz`        | `(quiz: Quiz) => void`       | Edit existing quiz |
| `deleteQuiz`      | `(quizId: string) => void`   | Delete quiz        |
| `addQuizToLesson` | `(lessonId: string) => void` | Add quiz to lesson |

##### Modal State

| Property             | Type             | Description                               |
| -------------------- | ---------------- | ----------------------------------------- |
| `isModuleModalOpen`  | `boolean`        | Module modal open state                   |
| `isLessonModalOpen`  | `boolean`        | Lesson modal open state                   |
| `isQuizModalOpen`    | `boolean`        | Quiz modal open state                     |
| `isDiscardModalOpen` | `boolean`        | Discard changes modal open state          |
| `editingModule`      | `Module \| null` | Module being edited (null = creating new) |
| `editingLesson`      | `Lesson \| null` | Lesson being edited (null = creating new) |
| `editingQuiz`        | `Quiz \| null`   | Quiz being edited (null = creating new)   |
| `openDiscardModal`   | `() => void`     | Open discard changes modal                |
| `closeDiscardModal`  | `() => void`     | Close discard changes modal               |

#### Usage Example

```typescript
import {useCourseFormWithAnalytics} from "@experts/hooks";

function CreateCoursePage() {
  // Create mode - empty form
  const courseForm = useCourseFormWithAnalytics();

  // Access form data
  const {formData, errors, activeStep} = courseForm;

  // Update field
  courseForm.updateField("title", "My New Course");

  // Navigate steps
  courseForm.nextStep();

  // Submit
  await courseForm.submitForm();
}

function EditCoursePage({courseId}: {courseId: string}) {
  const {data: course} = useCourse(courseId);

  // Edit mode - pre-populated form
  const courseForm = useCourseFormWithAnalytics(course);

  // Auto-save is automatically enabled in edit mode
  const {isAutoSaving, lastAutoSave, toggleAutoSave} = courseForm;

  return (
    <div>
      {isAutoSaving && <Spinner />}
      {lastAutoSave && <span>Last saved: {lastAutoSave.toLocaleTimeString()}</span>}
      <Switch checked={courseForm.isAutoSaveEnabled} onChange={toggleAutoSave} />
    </div>
  );
}
```

---

### useCourseFormHandlers

**Location:** `apps/experts-portal/src/app/(dashboard)/courses/shared/hooks/use-course-form-handlers.ts`

Extracts common handler functions used by both create and edit pages. Reduces code duplication and provides consistent behavior.

#### Signature

```typescript
function useCourseFormHandlers({
  hasUnsavedChanges,
  validateForm,
  submitForm,
  openDiscardModal,
  formData,
}: UseCourseFormHandlersProps): UseCourseFormHandlersReturn;
```

#### Parameters

| Parameter           | Type                                 | Required | Description                      |
| ------------------- | ------------------------------------ | -------- | -------------------------------- |
| `hasUnsavedChanges` | `boolean`                            | Yes      | Whether form has unsaved changes |
| `validateForm`      | `(data?: CourseFormData) => boolean` | Yes      | Form validation function         |
| `submitForm`        | `() => Promise<void>`                | Yes      | Form submission function         |
| `openDiscardModal`  | `() => void`                         | Yes      | Function to open discard modal   |
| `formData`          | `CourseFormData`                     | Yes      | Current form data                |

#### Return Value

| Property       | Type                  | Description                                                       |
| -------------- | --------------------- | ----------------------------------------------------------------- |
| `handleSubmit` | `() => Promise<void>` | Validates and submits form, shows error toast if invalid          |
| `handleBack`   | `() => void`          | Navigates back, opens discard modal if unsaved changes            |
| `canSaveDraft` | `boolean`             | Whether draft can be saved (has changes + required fields filled) |

#### Usage Example

```typescript
import {useCourseFormHandlers} from "../shared/hooks/use-course-form-handlers";

function CoursePage() {
  const courseForm = useCourseFormWithAnalytics();
  const {
    hasUnsavedChanges,
    validateForm,
    submitForm,
    openDiscardModal,
    formData,
  } = courseForm;

  const {handleSubmit, handleBack, canSaveDraft} = useCourseFormHandlers({
    hasUnsavedChanges,
    validateForm,
    submitForm,
    openDiscardModal,
    formData,
  });

  return (
    <div>
      <Button onClick={handleBack}>Back</Button>
      <Button onClick={handleSubmit} disabled={!canSaveDraft}>
        Save Draft
      </Button>
    </div>
  );
}
```

---

### useCourseStepsConfig

**Location:** `apps/experts-portal/src/app/(dashboard)/courses/shared/hooks/use-course-steps-config.tsx`

Generates memoized step configuration for the course form wizard. Encapsulates complex step setup logic and prevents unnecessary re-renders.

#### Signature

```typescript
function useCourseStepsConfig({
  formData,
  errors,
  updateField,
  previewImage,
  setPreviewImage,
  isUploading,
  uploadProgress,
  handleImageChange,
  onReorderModules,
  onReorderLessons,
  onMoveLesson,
  editModule,
  deleteModule,
  editLesson,
  deleteLesson,
  addLesson,
  openModuleModal,
  editQuiz,
  deleteQuiz,
  addQuizToLesson,
  goToStep,
}: UseCourseStepsConfigProps): CourseStepConfig[];
```

#### Parameters

All parameters from `useCourseFormWithAnalytics` needed by step components.

#### Return Value

Returns an array of 4 step configurations:

```typescript
interface CourseStepConfig {
  step: number; // Step number (1-4)
  title: string; // Step title
  component: ReactNode; // Step component to render
}
```

#### Usage Example

```typescript
import {useCourseStepsConfig} from "../shared/hooks/use-course-steps-config";

function CoursePage() {
  const courseForm = useCourseFormWithAnalytics();

  const courseSteps = useCourseStepsConfig({
    formData: courseForm.formData,
    errors: courseForm.errors,
    updateField: courseForm.updateField,
    // ... all other required props
  });

  // courseSteps is memoized - only recreates when dependencies change
  return <CourseStepRenderer activeStep={courseForm.activeStep} steps={courseSteps} />;
}
```

---

## Components

### CourseFormLayout

**Location:** `@experts/ui`

Main layout wrapper for course forms. Provides structure, step indicator, navigation controls, and preview pane.

#### Props

| Prop                  | Type                | Required | Description                                      |
| --------------------- | ------------------- | -------- | ------------------------------------------------ |
| `title`               | `string`            | Yes      | Page title ("Create New Course" / "Edit Course") |
| `totalSteps`          | `number`            | Yes      | Total number of steps (4)                        |
| `activeStep`          | `number`            | Yes      | Current active step (1-4)                        |
| `stepTitles`          | `readonly string[]` | Yes      | Array of step titles                             |
| `onNext`              | `() => void`        | Yes      | Next button click handler                        |
| `onPrevious`          | `() => void`        | Yes      | Previous button click handler                    |
| `onSaveDraft`         | `() => void`        | No       | Save draft button click handler                  |
| `onSubmit`            | `() => void`        | Yes      | Submit button click handler (step 4)             |
| `onBack`              | `() => void`        | Yes      | Back button click handler                        |
| `canNavigatePrevious` | `boolean`           | Yes      | Whether previous button is enabled               |
| `canNavigateNext`     | `boolean`           | Yes      | Whether next button is enabled                   |
| `canSaveDraft`        | `boolean`           | No       | Whether save draft button is shown               |
| `isSubmitting`        | `boolean`           | Yes      | Whether submission is in progress                |
| `submitButtonText`    | `string`            | Yes      | Submit button text                               |
| `children`            | `ReactNode`         | Yes      | Main content (CourseStepRenderer)                |
| `previewContent`      | `ReactNode`         | No       | Preview pane content                             |
| `showAutoSaveToggle`  | `boolean`           | No       | Show auto-save toggle (edit mode)                |
| `isAutoSaveEnabled`   | `boolean`           | No       | Auto-save toggle state                           |
| `onToggleAutoSave`    | `() => void`        | No       | Auto-save toggle handler                         |
| `isAutoSaving`        | `boolean`           | No       | Auto-save in progress indicator                  |
| `lastAutoSave`        | `Date \| null`      | No       | Last auto-save timestamp                         |
| `showPreviewButton`   | `boolean`           | No       | Show preview page button (edit mode)             |
| `onPreviewClick`      | `() => void`        | No       | Preview button click handler                     |

#### Usage Example

```typescript
<CourseFormLayout
  title="Create New Course"
  totalSteps={TOTAL_STEPS}
  activeStep={activeStep}
  stepTitles={STEP_TITLES}
  onNext={nextStep}
  onPrevious={prevStep}
  onSaveDraft={canSaveDraft ? handleSaveDraft : undefined}
  onSubmit={handleSubmit}
  onBack={handleBack}
  canNavigatePrevious={activeStep > 1}
  canNavigateNext={activeStep < TOTAL_STEPS}
  canSaveDraft={canSaveDraft}
  isSubmitting={isSubmitting}
  submitButtonText="Publish Course"
  previewContent={<CoursePreviewContent {...previewProps} />}
>
  <CourseStepRenderer activeStep={activeStep} steps={courseSteps} />
</CourseFormLayout>
```

---

### CourseStepRenderer

**Location:** `@experts/ui`

Renders the active step component based on current step number.

#### Props

| Prop         | Type                 | Required | Description                  |
| ------------ | -------------------- | -------- | ---------------------------- |
| `activeStep` | `number`             | Yes      | Current active step (1-4)    |
| `steps`      | `CourseStepConfig[]` | Yes      | Array of step configurations |

#### Usage Example

```typescript
<CourseStepRenderer
  activeStep={activeStep}
  steps={courseSteps}
/>
```

---

### CourseModalsManager

**Location:** `@experts/ui`

Manages all modals used in the course form. Handles open/close state and editing context.

#### Props

All props from `useCourseFormWithAnalytics` plus:

| Prop                  | Type            | Required | Description                     |
| --------------------- | --------------- | -------- | ------------------------------- |
| `ModuleModal`         | `ComponentType` | Yes      | Module modal component          |
| `LessonModal`         | `ComponentType` | Yes      | Lesson modal component          |
| `QuizModal`           | `ComponentType` | Yes      | Quiz modal component            |
| `DiscardChangesModal` | `ComponentType` | Yes      | Discard changes modal component |

#### Usage Example

```typescript
<CourseModalsManager
  {...courseForm}
  LessonModal={LessonModal}
  ModuleModal={ModuleModal}
  QuizModal={QuizModal}
  DiscardChangesModal={DiscardChangesModal}
/>
```

---

### CoursePreviewContent

**Location:** `apps/experts-portal/src/app/(dashboard)/courses/shared/components/course-preview-content.tsx`

Renders the preview pane content, including live course preview and course card.

#### Props

All preview-related props from `useCourseFormWithAnalytics`:

| Prop                   | Type                                     | Required | Description               |
| ---------------------- | ---------------------------------------- | -------- | ------------------------- |
| `formData`             | `CourseFormData`                         | Yes      | Current form data         |
| `previewMode`          | `'partial' \| 'expanded' \| 'minimized'` | Yes      | Preview mode              |
| `selectedLessonIndex`  | `number`                                 | Yes      | Selected lesson index     |
| `completedLessons`     | `Set<string>`                            | Yes      | Completed lesson IDs      |
| `handleLessonSelect`   | `(index: number) => void`                | Yes      | Lesson selection handler  |
| `handleCompleteLesson` | `(lessonId: string) => void`             | Yes      | Lesson completion handler |
| `handleQuizAnswer`     | `(qId: string, ans: string) => void`     | Yes      | Quiz answer handler       |
| `handleSubmitQuiz`     | `() => void`                             | Yes      | Quiz submission handler   |
| `showQuiz`             | `boolean`                                | Yes      | Quiz visibility state     |
| `setShowQuiz`          | `(show: boolean) => void`                | Yes      | Quiz visibility setter    |
| `quizAnswers`          | `Record<string, string>`                 | Yes      | Quiz answers              |
| `setQuizAnswers`       | `(answers) => void`                      | Yes      | Quiz answers setter       |
| `quizCompleted`        | `boolean`                                | Yes      | Quiz completion state     |
| `setQuizCompleted`     | `(completed: boolean) => void`           | Yes      | Quiz completion setter    |
| `quizScore`            | `number`                                 | Yes      | Quiz score                |
| `setQuizScore`         | `(score: number) => void`                | Yes      | Quiz score setter         |
| `setPreviewMode`       | `(mode) => void`                         | Yes      | Preview mode setter       |

#### Usage Example

```typescript
<CoursePreviewContent
  formData={formData}
  previewMode={previewMode}
  selectedLessonIndex={selectedLessonIndex}
  completedLessons={completedLessons}
  handleLessonSelect={handleLessonSelect}
  handleCompleteLesson={handleCompleteLesson}
  handleQuizAnswer={handleQuizAnswer}
  handleSubmitQuiz={handleSubmitQuiz}
  showQuiz={showQuiz}
  setShowQuiz={setShowQuiz}
  quizAnswers={quizAnswers}
  setQuizAnswers={setQuizAnswers}
  quizCompleted={quizCompleted}
  setQuizCompleted={setQuizCompleted}
  quizScore={quizScore}
  setQuizScore={setQuizScore}
  setPreviewMode={setPreviewMode}
/>
```

---

## Constants

### TOTAL_STEPS

**Location:** `apps/experts-portal/src/app/(dashboard)/courses/shared/constants/course-form-config.ts`

```typescript
export const TOTAL_STEPS = 4;
```

### STEP_TITLES

```typescript
export const STEP_TITLES = [
  "Course Information",
  "Curriculum & Lessons",
  "Quizzes & Assessment",
  "Review & Publish",
] as const;
```

### BREADCRUMBS

```typescript
export const BREADCRUMBS = {
  CREATE: [
    { label: "Dashboard", href: "/" },
    { label: "Courses", href: "/courses" },
    { label: "Create Course" },
  ],
  EDIT: (courseTitle: string) => [
    { label: "Dashboard", href: "/" },
    { label: "Courses", href: "/courses" },
    { label: courseTitle },
  ],
} as const;
```

### DELIVERY_MODE_OPTIONS

```typescript
export const DELIVERY_MODE_OPTIONS = [
  { value: "self-paced", label: "Self-Paced" },
  { value: "instructor-led", label: "Instructor-Led" },
  { value: "in-person", label: "In-Person" },
] as const;
```

### STATUS_OPTIONS

```typescript
export const STATUS_OPTIONS = [
  { value: "draft", label: "Draft" },
  { value: "published", label: "Published" },
  { value: "archived", label: "Archived" },
] as const;
```

---

## Types

### CourseFormData

```typescript
interface CourseFormData {
  // Basic Information
  title: string;
  description: string;
  category: string;
  tags: string[];
  instructor: string;

  // Details
  price: number;
  currency: string;
  duration: number; // in hours
  level: "beginner" | "intermediate" | "advanced";
  language: string;
  deliveryMode: "self-paced" | "instructor-led" | "in-person";
  status: "draft" | "published" | "archived";

  // Media
  thumbnail: string | null;
  previewVideo: string | null;

  // Curriculum
  modules: Module[];

  // Quizzes
  quizzes: Quiz[];

  // Metadata
  requirements: string[];
  learningOutcomes: string[];
  targetAudience: string;
}
```

### Module

```typescript
interface Module {
  id: string;
  title: string;
  description: string;
  order: number;
  lessons: Lesson[];
}
```

### Lesson

```typescript
interface Lesson {
  id: string;
  title: string;
  description: string;
  content: string;
  type: "video" | "text" | "quiz" | "assignment";
  order: number;
  duration: number; // in minutes
  videoUrl?: string;
  quizId?: string;
}
```

### Quiz

```typescript
interface Quiz {
  id: string;
  title: string;
  description: string;
  questions: Question[];
  passingScore: number;
  timeLimit?: number; // in minutes
}
```

### Question

```typescript
interface Question {
  id: string;
  text: string;
  type: "multiple-choice" | "true-false" | "short-answer";
  options?: string[];
  correctAnswer: string | string[];
  points: number;
  explanation?: string;
}
```

---

## Error Handling

### Validation Errors

Validation errors are returned as a record of field names to error messages:

```typescript
{
  title: "Title is required",
  price: "Price must be a positive number",
  "modules.0.title": "Module 1 title is required"
}
```

### API Errors

API errors include status codes and messages:

```typescript
{
  status: 404,
  message: "Course not found"
}
```

Common status codes:

- `400` - Bad Request (validation error)
- `401` - Unauthorized (not logged in)
- `403` - Forbidden (no permission)
- `404` - Not Found (course doesn't exist)
- `500` - Server Error

---

## Performance Notes

### Memoization

The `useCourseStepsConfig` hook uses `useMemo` to prevent unnecessary re-creation of step components. Dependencies are carefully managed to balance performance and reactivity.

### Auto-save Debouncing

Auto-save is debounced by 2 seconds to prevent excessive API calls. Only the last change in a 2-second window triggers a save.

### Optimistic Updates

UI updates happen immediately (optimistic) while API calls happen in the background. If API call fails, state is rolled back and user is notified.

---

## See Also

- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture overview
- [USAGE_GUIDE.md](./USAGE_GUIDE.md) - Practical usage examples
- [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) - Migration from old system
- [BEST_PRACTICES.md](./BEST_PRACTICES.md) - Patterns and conventions
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - Common issues and solutions
