---
title: "Course Management Usage Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/course"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Course Management Usage Guide

> **Version:** 2.0
> **Last Updated:** October 2025

Practical examples and recipes for using the course management system.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Creating a Course Form Page](#creating-a-course-form-page)
3. [Working with Form Data](#working-with-form-data)
4. [Managing Curriculum](#managing-curriculum)
5. [Handling Auto-save](#handling-auto-save)
6. [Customizing Preview](#customizing-preview)
7. [Form Validation](#form-validation)
8. [Error Handling](#error-handling)
9. [Advanced Patterns](#advanced-patterns)

---

## Quick Start

### Basic Create Page

The simplest course creation page:

```typescript
"use client";

import {useEffect, useState} from "react";
import {useCourseFormWithAnalytics} from "@experts/hooks";
import {useBreadcrumbs} from "@experts/providers";
import {CourseFormLayout, CourseStepRenderer, CourseModalsManager} from "@experts/ui";
import {useCourseFormHandlers} from "../shared/hooks/use-course-form-handlers";
import {useCourseStepsConfig} from "../shared/hooks/use-course-steps-config";
import {TOTAL_STEPS, STEP_TITLES, BREADCRUMBS} from "../shared/constants/course-form-config";
import {CoursePreviewContent} from "../shared/components/course-preview-content";
import {ModuleModal, LessonModal, QuizModal, DiscardChangesModal} from "../shared/modals";

export default function CreateCoursePage() {
  const {setBreadcrumbs} = useBreadcrumbs();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setBreadcrumbs(BREADCRUMBS.CREATE);
    setMounted(true);
  }, [setBreadcrumbs]);

  const courseForm = useCourseFormWithAnalytics();
  const {handleSubmit, handleBack, canSaveDraft} = useCourseFormHandlers({
    hasUnsavedChanges: courseForm.hasUnsavedChanges,
    validateForm: courseForm.validateForm,
    submitForm: courseForm.submitForm,
    openDiscardModal: courseForm.openDiscardModal,
    formData: courseForm.formData,
  });

  const courseSteps = useCourseStepsConfig({
    formData: courseForm.formData,
    errors: courseForm.errors,
    updateField: courseForm.updateField,
    previewImage: courseForm.previewImage,
    setPreviewImage: courseForm.setPreviewImage,
    isUploading: courseForm.isUploading,
    uploadProgress: courseForm.uploadProgress,
    handleImageChange: courseForm.handleImageChange,
    onReorderModules: courseForm.onReorderModules,
    onReorderLessons: courseForm.onReorderLessons,
    onMoveLesson: courseForm.onMoveLesson,
    editModule: courseForm.editModule,
    deleteModule: courseForm.deleteModule,
    editLesson: courseForm.editLesson,
    deleteLesson: courseForm.deleteLesson,
    addLesson: courseForm.addLesson,
    openModuleModal: courseForm.openModuleModal,
    editQuiz: courseForm.editQuiz,
    deleteQuiz: courseForm.deleteQuiz,
    addQuizToLesson: courseForm.addQuizToLesson,
  });

  if (!mounted) return null;

  return (
    <>
      <CourseFormLayout
        title="Create New Course"
        totalSteps={TOTAL_STEPS}
        activeStep={courseForm.activeStep}
        stepTitles={STEP_TITLES}
        onNext={courseForm.nextStep}
        onPrevious={courseForm.prevStep}
        onSaveDraft={canSaveDraft ? courseForm.handleSaveDraft : undefined}
        onSubmit={handleSubmit}
        onBack={handleBack}
        canNavigatePrevious={courseForm.activeStep > 1}
        canNavigateNext={courseForm.activeStep < TOTAL_STEPS}
        canSaveDraft={canSaveDraft}
        isSubmitting={false}
        submitButtonText="Publish Course"
        previewContent={
          <CoursePreviewContent
            formData={courseForm.formData}
            previewMode={courseForm.previewMode}
            selectedLessonIndex={courseForm.selectedLessonIndex}
            completedLessons={courseForm.completedLessons}
            handleLessonSelect={courseForm.handleLessonSelect}
            handleCompleteLesson={courseForm.handleCompleteLesson}
            handleQuizAnswer={courseForm.handleQuizAnswer}
            handleSubmitQuiz={courseForm.handleSubmitQuiz}
            showQuiz={courseForm.showQuiz}
            setShowQuiz={courseForm.setShowQuiz}
            quizAnswers={courseForm.quizAnswers}
            setQuizAnswers={courseForm.setQuizAnswers}
            quizCompleted={courseForm.quizCompleted}
            setQuizCompleted={courseForm.setQuizCompleted}
            quizScore={courseForm.quizScore}
            setQuizScore={courseForm.setQuizScore}
            setPreviewMode={courseForm.setPreviewMode}
          />
        }
      >
        <CourseStepRenderer activeStep={courseForm.activeStep} steps={courseSteps} />
      </CourseFormLayout>

      <CourseModalsManager
        {...courseForm}
        LessonModal={LessonModal}
        ModuleModal={ModuleModal}
        QuizModal={QuizModal}
        DiscardChangesModal={DiscardChangesModal}
      />
    </>
  );
}
```

### Basic Edit Page

Edit page with auto-save:

```typescript
"use client";

import {useEffect, useState} from "react";
import {useParams, useRouter} from "next/navigation";
import {useCourse, useCourseFormWithAnalytics} from "@experts/hooks";
import {useBreadcrumbs} from "@experts/providers";
import {CourseFormLayout, CourseStepRenderer, CourseModalsManager} from "@experts/ui";
import {useCourseFormHandlers} from "../shared/hooks/use-course-form-handlers";
import {useCourseStepsConfig} from "../shared/hooks/use-course-steps-config";
import {TOTAL_STEPS, STEP_TITLES, BREADCRUMBS} from "../shared/constants/course-form-config";
import {CoursePreviewContent} from "../shared/components/course-preview-content";
import {ModuleModal, LessonModal, QuizModal, DiscardChangesModal} from "../shared/modals";

export default function EditCoursePage() {
  const router = useRouter();
  const params = useParams();
  const uuid = params.uuid as string;

  const {setBreadcrumbs} = useBreadcrumbs();
  const [mounted, setMounted] = useState(false);

  const {data: course, isLoading, error} = useCourse(uuid);

  useEffect(() => {
    if (course) {
      setBreadcrumbs(BREADCRUMBS.EDIT(course.title));
    }
    setMounted(true);
  }, [course, setBreadcrumbs]);

  const courseForm = useCourseFormWithAnalytics(course);
  const {handleSubmit, handleBack, canSaveDraft} = useCourseFormHandlers({
    hasUnsavedChanges: courseForm.hasUnsavedChanges,
    validateForm: courseForm.validateForm,
    submitForm: courseForm.submitForm,
    openDiscardModal: courseForm.openDiscardModal,
    formData: courseForm.formData,
  });

  const courseSteps = useCourseStepsConfig({
    // Same as create page, plus:
    goToStep: courseForm.goToStep, // Edit-specific feature
    // ... all other props
  });

  if (!mounted) return null;
  if (isLoading) return <div>Loading...</div>;
  if (error?.status === 404) return <div>Course not found</div>;
  if (error?.status === 403) return <div>Access denied</div>;
  if (error) return <div>Failed to load course</div>;

  return (
    <>
      <CourseFormLayout
        title="Edit Course"
        totalSteps={TOTAL_STEPS}
        activeStep={courseForm.activeStep}
        stepTitles={STEP_TITLES}
        onNext={courseForm.nextStep}
        onPrevious={courseForm.prevStep}
        onSaveDraft={canSaveDraft ? courseForm.handleSaveDraft : undefined}
        onSubmit={handleSubmit}
        onBack={handleBack}
        canNavigatePrevious={courseForm.activeStep > 1}
        canNavigateNext={courseForm.activeStep < TOTAL_STEPS}
        canSaveDraft={canSaveDraft}
        isSubmitting={false}
        submitButtonText="Update Course"
        // Edit-specific props
        showAutoSaveToggle={true}
        isAutoSaveEnabled={courseForm.isAutoSaveEnabled}
        onToggleAutoSave={courseForm.toggleAutoSave}
        isAutoSaving={courseForm.isAutoSaving}
        lastAutoSave={courseForm.lastAutoSave}
        showPreviewButton={true}
        onPreviewClick={() => router.push(`/courses/${uuid}/preview`)}
        previewContent={<CoursePreviewContent {...previewProps} />}
      >
        <CourseStepRenderer activeStep={courseForm.activeStep} steps={courseSteps} />
      </CourseFormLayout>

      <CourseModalsManager {...courseForm} {...modals} />
    </>
  );
}
```

---

## Working with Form Data

### Updating Form Fields

```typescript
const courseForm = useCourseFormWithAnalytics();

// Update a single field
courseForm.updateField("title", "Introduction to React");

// Update multiple fields
courseForm.updateField("title", "React Course");
courseForm.updateField("description", "Learn React from scratch");
courseForm.updateField("price", 99.99);

// Update nested fields
courseForm.updateField("tags", ["react", "javascript", "frontend"]);

// Type-safe updates
courseForm.updateField<"level">("level", "intermediate");
```

### Reading Form Data

```typescript
const { formData, errors } = courseForm;

// Access form values
console.log(formData.title); // "Introduction to React"
console.log(formData.price); // 99.99
console.log(formData.modules); // Module[]

// Check for errors
if (errors.title) {
  console.log("Title error:", errors.title);
}

// Check if form is valid
const isValid = Object.keys(errors).length === 0;
```

### Form Validation

```typescript
// Validate entire form
const isValid = courseForm.validateForm();

if (isValid) {
  await courseForm.submitForm();
} else {
  console.log("Errors:", courseForm.errors);
}

// Validate specific data
const customData = { ...courseForm.formData, title: "New Title" };
const isValidCustom = courseForm.validateForm(customData);
```

---

## Managing Curriculum

### Adding Modules

```typescript
// Open modal to create new module
courseForm.openModuleModal();

// The modal handles creation and automatically:
// 1. Adds module to formData.modules[]
// 2. Updates order
// 3. Closes modal
```

### Editing Modules

```typescript
const module = courseForm.formData.modules[0];

// Open modal with existing module
courseForm.editModule(module);

// Modal pre-populated with module data
// Saves update to formData on submit
```

### Deleting Modules

```typescript
const moduleId = "module-123";

// Delete module (with confirmation)
courseForm.deleteModule(moduleId);

// Also removes all lessons in module
```

### Reordering Modules

```typescript
// After drag-and-drop
const reorderedModules = [
  courseForm.formData.modules[1],
  courseForm.formData.modules[0],
  courseForm.formData.modules[2],
];

courseForm.onReorderModules(reorderedModules);

// Order property updated automatically
```

### Managing Lessons

```typescript
// Add lesson to specific module
const moduleId = "module-123";
courseForm.addLesson(moduleId);

// Edit lesson
const lesson = module.lessons[0];
courseForm.editLesson(lesson);

// Delete lesson
courseForm.deleteLesson("lesson-456");

// Reorder lessons within module
courseForm.onReorderLessons(moduleId, reorderedLessons);

// Move lesson to different module
courseForm.onMoveLesson("lesson-456", "module-789");
```

---

## Handling Auto-save

### Enable/Disable Auto-save

```typescript
const courseForm = useCourseFormWithAnalytics(existingCourse);

// Auto-save is enabled by default in edit mode
console.log(courseForm.isAutoSaveEnabled); // true

// Toggle auto-save
courseForm.toggleAutoSave();
console.log(courseForm.isAutoSaveEnabled); // false

// Toggle again
courseForm.toggleAutoSave();
console.log(courseForm.isAutoSaveEnabled); // true
```

### Auto-save State

```typescript
// Check if auto-save is in progress
if (courseForm.isAutoSaving) {
  console.log("Saving...");
}

// Get last auto-save time
if (courseForm.lastAutoSave) {
  const timeAgo = Date.now() - courseForm.lastAutoSave.getTime();
  console.log(`Last saved ${timeAgo}ms ago`);
}

// Check network connectivity
if (!courseForm.isOnline) {
  console.log("Offline - auto-save paused");
}
```

### Manual Save

```typescript
// Save draft manually (even with auto-save enabled)
if (canSaveDraft) {
  await courseForm.handleSaveDraft();
}
```

### Auto-save UI Indicators

```typescript
<div>
  {courseForm.isAutoSaving && (
    <span>
      <Spinner size="sm" /> Saving...
    </span>
  )}

  {!courseForm.isAutoSaving && courseForm.lastAutoSave && (
    <span>
      Last saved {courseForm.lastAutoSave.toLocaleTimeString()}
    </span>
  )}

  {!courseForm.isOnline && (
    <span>
      <Icon name="offline" /> Offline - changes will save when reconnected
    </span>
  )}
</div>
```

---

## Customizing Preview

### Preview Modes

```typescript
// Set preview mode
courseForm.setPreviewMode("partial"); // Default
courseForm.setPreviewMode("expanded"); // Full screen
courseForm.setPreviewMode("minimized"); // Hidden

// Get current mode
console.log(courseForm.previewMode); // "partial"
```

### Lesson Selection

```typescript
// Select lesson in preview
courseForm.handleLessonSelect(2); // Select 3rd lesson

// Get selected lesson
const selectedLesson =
  courseForm.formData.modules[0].lessons[courseForm.selectedLessonIndex];

// Mark lesson as completed
courseForm.handleCompleteLesson("lesson-123");

// Check if lesson is completed
const isCompleted = courseForm.completedLessons.has("lesson-123");

// Get all completed lessons
const completedArray = Array.from(courseForm.completedLessons);
```

### Quiz Preview

```typescript
// Show quiz
courseForm.setShowQuiz(true);

// Record answer
courseForm.handleQuizAnswer("question-1", "Option A");

// Get current answers
console.log(courseForm.quizAnswers); // {"question-1": "Option A"}

// Submit quiz
courseForm.handleSubmitQuiz();

// Check results
if (courseForm.quizCompleted) {
  console.log(`Score: ${courseForm.quizScore}%`);
}

// Reset quiz
courseForm.setQuizCompleted(false);
courseForm.setQuizScore(0);
courseForm.setQuizAnswers({});
```

---

## Form Validation

### Validation Rules

```typescript
// Validation happens automatically on:
// 1. Step navigation (nextStep)
// 2. Form submission (submitForm)
// 3. Manual validation (validateForm)

// Example validation rules (implemented in hook):
const rules = {
  title: {
    required: true,
    minLength: 3,
    maxLength: 100,
  },
  price: {
    required: true,
    min: 0,
    type: "number",
  },
  modules: {
    required: true,
    minLength: 1,
    message: "At least one module is required",
  },
};
```

### Handling Validation Errors

```typescript
// Check for errors
if (courseForm.errors.title) {
  console.log("Title error:", courseForm.errors.title);
}

// Display errors in UI
<Input
  label="Title"
  value={courseForm.formData.title}
  onChange={(e) => courseForm.updateField("title", e.target.value)}
  isInvalid={!!courseForm.errors.title}
  errorMessage={courseForm.errors.title}
/>

// Clear errors (happens automatically on updateField)
courseForm.updateField("title", "Valid Title");
console.log(courseForm.errors.title); // undefined
```

### Step-specific Validation

```typescript
// Validation is step-aware
// Step 1: Basic info (title, description, category)
// Step 2: Curriculum (modules, lessons)
// Step 3: Quizzes
// Step 4: Final review (all fields)

// Try to move to next step
courseForm.nextStep();

// If validation fails, stays on current step
// errors object populated with relevant errors
```

---

## Error Handling

### API Errors

```typescript
try {
  await courseForm.submitForm();
  toast.success("Course created successfully!");
} catch (error) {
  if (error.status === 400) {
    toast.error("Invalid course data");
  } else if (error.status === 403) {
    toast.error("You don't have permission to create courses");
  } else if (error.status === 500) {
    toast.error("Server error. Please try again later.");
  } else {
    toast.error("Failed to create course");
  }
}
```

### Upload Errors

```typescript
try {
  await courseForm.handleImageChange(file);
} catch (error) {
  if (error.message === "File too large") {
    toast.error("Image must be less than 5MB");
  } else if (error.message === "Invalid file type") {
    toast.error("Only JPG, PNG, and WebP images are allowed");
  } else {
    toast.error("Failed to upload image");
  }
}
```

### Network Errors

```typescript
// Auto-save handles network errors gracefully
if (!courseForm.isOnline) {
  // Changes are queued
  // Will auto-save when connection restored
  toast.info("Offline - changes will save when reconnected");
}
```

---

## Advanced Patterns

### Custom Step Configuration

```typescript
// You can customize step components
const customSteps = useCourseStepsConfig({
  ...courseFormProps,
  // Add custom props
  customProp: "value",
});

// Or create your own steps array
const customSteps: CourseStepConfig[] = [
  {
    step: 1,
    title: "Custom Step 1",
    component: <CustomStep1 {...props} />,
  },
  // ... more steps
];
```

### Conditional Step Rendering

```typescript
// Show different steps based on course type
const courseSteps = useMemo(() => {
  const baseSteps = useCourseStepsConfig(props);

  if (courseForm.formData.deliveryMode === "self-paced") {
    // Remove instructor-led specific steps
    return baseSteps.filter((step) => step.step !== 5);
  }

  return baseSteps;
}, [courseForm.formData.deliveryMode /* other deps */]);
```

### Custom Handlers

```typescript
// Extend default handlers
const { handleSubmit, handleBack, canSaveDraft } = useCourseFormHandlers({
  hasUnsavedChanges: courseForm.hasUnsavedChanges,
  validateForm: courseForm.validateForm,
  submitForm: async () => {
    // Custom pre-submit logic
    trackEvent("course_submit_started");

    await courseForm.submitForm();

    // Custom post-submit logic
    trackEvent("course_submit_completed");
    router.push("/courses");
  },
  openDiscardModal: courseForm.openDiscardModal,
  formData: courseForm.formData,
});
```

### Custom Preview Content

```typescript
// Create your own preview component
function CustomPreviewContent(props) {
  return (
    <div>
      <h3>Custom Preview</h3>
      <CourseCard course={props.formData} />
      {/* Add custom preview features */}
      <div>Estimated completion time: {calculateTime(props.formData)}</div>
    </div>
  );
}

// Use in layout
<CourseFormLayout
  previewContent={<CustomPreviewContent formData={courseForm.formData} />}
  {...otherProps}
/>
```

### Optimistic Updates

```typescript
// Update UI immediately, save in background
const handleAddModule = async (module: Module) => {
  // Optimistic: Add to UI immediately
  const optimisticModules = [...courseForm.formData.modules, module];
  courseForm.updateField("modules", optimisticModules);

  try {
    // Background: Save to server
    await saveModuleToServer(module);
  } catch (error) {
    // Rollback on error
    courseForm.updateField("modules", courseForm.formData.modules);
    toast.error("Failed to add module");
  }
};
```

### Debounced Field Updates

```typescript
import {useDebounce} from "@experts/hooks";

function CourseInformationStep({formData, updateField}) {
  const [localTitle, setLocalTitle] = useState(formData.title);
  const debouncedTitle = useDebounce(localTitle, 500);

  useEffect(() => {
    if (debouncedTitle !== formData.title) {
      updateField("title", debouncedTitle);
    }
  }, [debouncedTitle]);

  return (
    <Input
      value={localTitle}
      onChange={(e) => setLocalTitle(e.target.value)}
      label="Course Title"
    />
  );
}
```

### Analytics Integration

```typescript
// useCourseFormWithAnalytics automatically tracks:
// - Step changes
// - Form submissions
// - Auto-saves
// - Errors

// Add custom tracking
useEffect(() => {
  trackEvent("course_form_opened", {
    mode: courseForm.courseUuid ? "edit" : "create",
    step: courseForm.activeStep,
  });
}, [courseForm.activeStep]);

// Track specific actions
const handleModuleAdd = () => {
  trackEvent("module_added", {
    moduleCount: courseForm.formData.modules.length + 1,
  });
  courseForm.openModuleModal();
};
```

---

## Performance Tips

### 1. Memoize Preview Content

```typescript
const previewContent = useMemo(
  () => (
    <CoursePreviewContent
      formData={courseForm.formData}
      // ... other props
    />
  ),
  [
    courseForm.formData,
    courseForm.previewMode,
    courseForm.selectedLessonIndex,
    // Only dependencies that affect preview
  ]
);
```

### 2. Lazy Load Heavy Components

```typescript
const QuizEditor = lazy(() => import("./quiz-editor"));

// Render only when needed
{courseForm.showQuiz && (
  <Suspense fallback={<Spinner />}>
    <QuizEditor {...props} />
  </Suspense>
)}
```

### 3. Optimize Reorders

```typescript
// Use callback refs to prevent re-renders
const handleReorderModules = useCallback(
  (modules: Module[]) => {
    courseForm.onReorderModules(modules);
  },
  [courseForm.onReorderModules],
);
```

---

## See Also

- [API_REFERENCE.md](./API_REFERENCE.md) - Complete API documentation
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture
- [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) - Migration guide
- [BEST_PRACTICES.md](./BEST_PRACTICES.md) - Best practices
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - Troubleshooting guide
