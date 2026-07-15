---
title: "Migration Guide: Old to New Course Form System"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/course"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Migration Guide: Old to New Course Form System

> **Version:** From 1.x to 2.0
> **Last Updated:** October 2025

Complete guide for migrating from the old monolithic course form to the new composition-based architecture.

## Table of Contents

1. [Overview](#overview)
2. [Breaking Changes](#breaking-changes)
3. [Migration Path](#migration-path)
4. [Before & After Comparison](#before--after-comparison)
5. [Step-by-Step Migration](#step-by-step-migration)
6. [Common Migration Issues](#common-migration-issues)
7. [Testing After Migration](#testing-after-migration)

---

## Overview

### What Changed?

**Old System (v1.x):**

- ❌ Monolithic 720-line pages
- ❌ Duplicated logic between create/edit
- ❌ Hard to test
- ❌ Difficult to maintain
- ❌ Poor reusability

**New System (v2.0):**

- ✅ Composition-based architecture
- ✅ 172-line create page, 235-line edit page
- ✅ Shared hooks and components
- ✅ Fully tested (85%+ coverage)
- ✅ Maintainable and extensible

### Why Migrate?

1. **Reduced Code**: 461 lines eliminated through extraction
2. **Better Testing**: Comprehensive test utilities and coverage
3. **Improved DX**: Clear separation of concerns
4. **Future-proof**: Easy to extend and modify
5. **Performance**: Better memoization and optimization

---

## Breaking Changes

### Removed Dependencies

```diff
- import {useCourseForm} from "../hooks/use-course-form"
+ import {useCourseFormWithAnalytics} from "@experts/hooks"

- import {CourseLayout} from "../components/course-layout"
+ import {CourseFormLayout} from "@experts/ui"

- import {StepRenderer} from "../components/step-renderer"
+ import {CourseStepRenderer} from "@experts/ui"
```

### API Changes

#### Hook Return Values

```diff
// Old
const {
-  form,
-  isLoading,
-  handleNext,
-  handlePrevious,
} = useCourseForm();

// New
const courseForm = useCourseFormWithAnalytics();
const {
+  formData,
+  errors,
+  nextStep,
+  prevStep,
+  // ... 40+ more properties
} = courseForm;
```

#### Component Props

```diff
// Old
<CourseLayout
-  form={form}
-  onNext={handleNext}
+  title="Create New Course"
+  totalSteps={4}
+  activeStep={activeStep}
+  stepTitles={STEP_TITLES}
+  onNext={nextStep}
+  onPrevious={prevStep}
+  // ... more explicit props
/>
```

### File Structure Changes

```diff
apps/experts-portal/src/app/(dashboard)/courses/
├── create/
-│   ├── components/          # Removed
-│   ├── hooks/               # Removed
│   └── page.tsx              # Simplified (720 → 172 lines)
│
├── [uuid]/edit/
│   └── page.tsx              # Simplified (720 → 235 lines)
│
+├── shared/                  # NEW: Shared resources
+│   ├── components/
+│   ├── constants/
+│   ├── hooks/
+│   ├── modals/
+│   ├── steps/
+│   └── sortables/
```

---

## Migration Path

### Quick Migration (30 minutes)

For simple course forms with minimal customization:

1. Replace page component with new template
2. Update imports
3. Test functionality
4. Done!

### Careful Migration (2-4 hours)

For heavily customized course forms:

1. Audit custom logic
2. Extract custom features to hooks
3. Migrate step components
4. Update modals
5. Add comprehensive tests
6. QA testing
7. Deploy

---

## Before & After Comparison

### Old Create Page (720 lines)

```typescript
"use client";

import React, {useState, useEffect, useMemo} from "react";
import {useCourseForm} from "../hooks/use-course-form";
import {CourseLayout} from "../components/course-layout";
import {CourseInformationStep} from "../steps/course-information-step";
import {CourseCurriculumStep} from "../steps/course-curriculum-step";
import {CourseQuizzesStep} from "../steps/course-quizzes-step";
import {CourseReviewStep} from "../steps/course-review-step";
import {ModuleModal} from "../modals/module-modal";
import {LessonModal} from "../modals/lesson-modal";
import {QuizModal} from "../modals/quiz-modal";

export default function CreateCoursePage() {
  const [mounted, setMounted] = useState(false);
  const [activeStep, setActiveStep] = useState(1);
  const [formData, setFormData] = useState({/* 100+ lines of initial state */});
  const [errors, setErrors] = useState({});
  const [isModuleModalOpen, setIsModuleModalOpen] = useState(false);
  const [isLessonModalOpen, setIsLessonModalOpen] = useState(false);
  const [isQuizModalOpen, setIsQuizModalOpen] = useState(false);
  // ... 50+ more useState declarations

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleNext = () => {
    // 30 lines of validation logic
    if (validateStep(activeStep)) {
      setActiveStep(activeStep + 1);
    }
  };

  const handlePrevious = () => {
    setActiveStep(activeStep - 1);
  };

  const handleSubmit = async () => {
    // 40 lines of submission logic
    try {
      const response = await fetch("/api/courses", {
        method: "POST",
        body: JSON.stringify(formData),
      });
      // ... error handling
    } catch (error) {
      // ... error handling
    }
  };

  const validateStep = (step: number) => {
    // 80 lines of validation logic
    const newErrors = {};
    switch (step) {
      case 1:
        if (!formData.title) newErrors.title = "Title required";
        // ... 20+ more validations
        break;
      // ... cases for steps 2-4
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleAddModule = () => {
    setIsModuleModalOpen(true);
  };

  const handleSaveModule = (module) => {
    // 30 lines of module save logic
    setFormData({
      ...formData,
      modules: [...formData.modules, module],
    });
    setIsModuleModalOpen(false);
  };

  // ... 300+ more lines of handlers and logic
  // ... 100+ lines of step rendering
  // ... 50+ lines of modal rendering

  if (!mounted) return null;

  return (
    <div>
      <CourseLayout
        activeStep={activeStep}
        onNext={handleNext}
        onPrevious={handlePrevious}
      >
        {activeStep === 1 && (
          <CourseInformationStep
            formData={formData}
            errors={errors}
            onChange={(field, value) => {
              setFormData({...formData, [field]: value});
              setErrors({...errors, [field]: undefined});
            }}
          />
        )}
        {/* ... 100+ more lines for other steps */}
      </CourseLayout>

      {isModuleModalOpen && (
        <ModuleModal
          isOpen={isModuleModalOpen}
          onClose={() => setIsModuleModalOpen(false)}
          onSave={handleSaveModule}
        />
      )}
      {/* ... more modals */}
    </div>
  );
}
```

### New Create Page (172 lines)

```typescript
"use client";

import React, {useEffect, useState} from "react";
import {useCourseFormWithAnalytics} from "@experts/hooks";
import {useBreadcrumbs} from "@experts/providers";
import {CourseFormLayout, CourseStepRenderer, CourseModalsManager} from "@experts/ui";
import {QuizModal, LessonModal, ModuleModal, DiscardChangesModal} from "../shared/modals";
import {CoursePreviewContent} from "../shared/components/course-preview-content";
import {useCourseFormHandlers} from "../shared/hooks/use-course-form-handlers";
import {useCourseStepsConfig} from "../shared/hooks/use-course-steps-config";
import {TOTAL_STEPS, STEP_TITLES, BREADCRUMBS} from "../shared/constants/course-form-config";

export default function CreateCoursePage() {
  const {setBreadcrumbs} = useBreadcrumbs();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setBreadcrumbs(BREADCRUMBS.CREATE);
  }, [setBreadcrumbs]);

  useEffect(() => {
    setMounted(true);
  }, []);

  const courseForm = useCourseFormWithAnalytics();
  const {
    formData,
    errors,
    hasUnsavedChanges,
    activeStep,
    // ... destructure 40+ more properties in ~50 lines
  } = courseForm;

  const {handleSubmit, handleBack, canSaveDraft} = useCourseFormHandlers({
    hasUnsavedChanges,
    validateForm,
    submitForm,
    openDiscardModal,
    formData,
  });

  const courseSteps = useCourseStepsConfig({
    formData,
    errors,
    updateField,
    // ... all step config props in ~20 lines
  });

  if (!mounted) return null;

  return (
    <>
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
        isSubmitting={false}
        submitButtonText="Publish Course"
        previewContent={<CoursePreviewContent {...previewProps} />}
      >
        <CourseStepRenderer activeStep={activeStep} steps={courseSteps} />
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

**Reduction:** 720 → 172 lines (76% reduction!)

---

## Step-by-Step Migration

### Step 1: Install Dependencies

Ensure you have the latest versions:

```bash
# Update shared packages
yarn upgrade @experts/hooks@latest
yarn upgrade @experts/ui@latest
yarn upgrade @experts/providers@latest
yarn upgrade @experts/test@latest
```

### Step 2: Create Shared Directory

```bash
cd apps/experts-portal/src/app/(dashboard)/courses
mkdir -p shared/{components,constants,hooks,modals,steps,sortables}
```

### Step 3: Move Shared Constants

Create `shared/constants/course-form-config.ts`:

```typescript
export const TOTAL_STEPS = 4;

export const STEP_TITLES = [
  "Course Information",
  "Curriculum & Lessons",
  "Quizzes & Assessment",
  "Review & Publish",
] as const;

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

export const DELIVERY_MODE_OPTIONS = [
  { value: "self-paced", label: "Self-Paced" },
  { value: "instructor-led", label: "Instructor-Led" },
  { value: "hybrid", label: "Hybrid" },
] as const;

export const STATUS_OPTIONS = [
  { value: "draft", label: "Draft" },
  { value: "published", label: "Published" },
  { value: "archived", label: "Archived" },
] as const;
```

### Step 4: Move Step Components

Move your step components to `shared/steps/`:

```bash
mv create/steps/*.tsx shared/steps/
```

Update imports in step files:

```diff
- import {Input} from "../../components/input"
+ import {Input} from "@nextui-org/react"
```

### Step 5: Move Modal Components

Move modals to `shared/modals/`:

```bash
mv create/modals/*.tsx shared/modals/
```

### Step 6: Create Handler Hook

Create `shared/hooks/use-course-form-handlers.ts`:

```typescript
import { toast } from "sonner";
import type { CourseFormData } from "@experts/types";

interface UseCourseFormHandlersProps {
  hasUnsavedChanges: boolean;
  validateForm: (data?: CourseFormData) => boolean;
  submitForm: () => Promise<void>;
  openDiscardModal: () => void;
  formData: CourseFormData;
}

export function useCourseFormHandlers({
  hasUnsavedChanges,
  validateForm,
  submitForm,
  openDiscardModal,
  formData,
}: UseCourseFormHandlersProps) {
  const handleSubmit = async () => {
    if (!validateForm(formData)) {
      toast.error("Please fix all errors before submitting");
      return;
    }
    await submitForm();
  };

  const handleBack = () => {
    if (hasUnsavedChanges) {
      openDiscardModal();
    } else {
      window.history.back();
    }
  };

  const canSaveDraft =
    hasUnsavedChanges &&
    formData.category &&
    formData.title &&
    formData.description &&
    formData.instructor;

  return { handleSubmit, handleBack, canSaveDraft };
}
```

### Step 7: Create Steps Config Hook

Create `shared/hooks/use-course-steps-config.tsx`:

```typescript
import React, {useMemo} from "react";
import {Divider} from "@nextui-org/react";
import {CourseInformationStep} from "../steps/course-information-step";
import {CourseDetailsStep} from "../steps/course-details-step";
import {CourseCurriculumStep} from "../steps/course-curriculum-step";
import {CourseQuizzesStep} from "../steps/course-quizzes-step";
import {CourseReviewStep} from "../steps/course-review-step";

export function useCourseStepsConfig({
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
}: UseCourseStepsConfigProps) {
  return useMemo(
    () => [
      {
        step: 1,
        title: "Course Information",
        component: (
          <>
            <CourseInformationStep
              formData={formData}
              errors={errors}
              updateField={updateField}
              previewImage={previewImage}
              setPreviewImage={setPreviewImage}
              isUploading={isUploading}
              uploadProgress={uploadProgress}
              handleImageChange={handleImageChange}
            />
            <Divider className="my-8" />
            <CourseDetailsStep formData={formData} errors={errors} updateField={updateField} />
          </>
        ),
      },
      {
        step: 2,
        title: "Curriculum & Lessons",
        component: (
          <CourseCurriculumStep
            formData={formData}
            errors={errors}
            onReorderModules={onReorderModules}
            onReorderLessons={onReorderLessons}
            onMoveLesson={onMoveLesson}
            editModule={editModule}
            deleteModule={deleteModule}
            editLesson={editLesson}
            deleteLesson={deleteLesson}
            addLesson={addLesson}
            openModuleModal={openModuleModal}
          />
        ),
      },
      {
        step: 3,
        title: "Quizzes & Assessment",
        component: (
          <CourseQuizzesStep
            formData={formData}
            errors={errors}
            editQuiz={editQuiz}
            deleteQuiz={deleteQuiz}
            addQuizToLesson={addQuizToLesson}
            goToStep={goToStep}
          />
        ),
      },
      {
        step: 4,
        title: "Review & Publish",
        component: <CourseReviewStep formData={formData} previewImage={previewImage} />,
      },
    ],
    [
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
    ]
  );
}
```

### Step 8: Create Preview Content Component

Create `shared/components/course-preview-content.tsx`:

```typescript
import React from "react";
import {CourseCard, LiveCoursePreview, CourseRibbon, CourseCardHeader} from "@experts/ui";
import type {CourseFormData} from "@experts/types";

interface CoursePreviewContentProps {
  formData: CourseFormData;
  previewMode: "partial" | "expanded" | "minimized";
  selectedLessonIndex: number;
  completedLessons: Set<string>;
  handleLessonSelect: (index: number) => void;
  handleCompleteLesson: (lessonId: string) => void;
  handleQuizAnswer: (questionId: string, answer: string) => void;
  handleSubmitQuiz: () => void;
  showQuiz: boolean;
  setShowQuiz: (show: boolean) => void;
  quizAnswers: Record<string, string>;
  setQuizAnswers: (answers: Record<string, string>) => void;
  quizCompleted: boolean;
  setQuizCompleted: (completed: boolean) => void;
  quizScore: number;
  setQuizScore: (score: number) => void;
  setPreviewMode: (mode: "partial" | "expanded" | "minimized") => void;
}

export function CoursePreviewContent({
  formData,
  previewMode,
  selectedLessonIndex,
  completedLessons,
  handleLessonSelect,
  handleCompleteLesson,
  handleQuizAnswer,
  handleSubmitQuiz,
  showQuiz,
  setShowQuiz,
  quizAnswers,
  setQuizAnswers,
  quizCompleted,
  setQuizCompleted,
  quizScore,
  setQuizScore,
  setPreviewMode,
}: CoursePreviewContentProps) {
  return (
    <>
      <LiveCoursePreview
        course={formData}
        mode={previewMode}
        selectedLessonIndex={selectedLessonIndex}
        completedLessons={completedLessons}
        onLessonSelect={handleLessonSelect}
        onCompleteLesson={handleCompleteLesson}
        onQuizAnswer={handleQuizAnswer}
        onSubmitQuiz={handleSubmitQuiz}
        showQuiz={showQuiz}
        setShowQuiz={setShowQuiz}
        quizAnswers={quizAnswers}
        setQuizAnswers={setQuizAnswers}
        quizCompleted={quizCompleted}
        setQuizCompleted={setQuizCompleted}
        quizScore={quizScore}
        setQuizScore={setQuizScore}
        onRefresh={() => setPreviewMode("partial")}
      />

      <CourseCard status="published" size="md" course={formData} showShareButton showView showPreview>
        <CourseRibbon isFeatured />
        <CourseCardHeader>
          {/* Card content */}
        </CourseCardHeader>
      </CourseCard>
    </>
  );
}
```

### Step 9: Update Create Page

Replace `create/page.tsx` with new implementation (see "New Create Page" above).

### Step 10: Update Edit Page

Replace `[uuid]/edit/page.tsx` with new implementation including auto-save features.

### Step 11: Remove Old Files

```bash
# Remove old hook files
rm -rf create/hooks
rm -rf create/components

# Remove duplicates
rm -rf [uuid]/edit/hooks
rm -rf [uuid]/edit/components
```

### Step 12: Update Tests

Create tests using new `@experts/test` utilities:

```typescript
import {
  render,
  screen,
  createMockCourseForm,
  fillCourseInformationStep,
  submitCourseForm,
} from "@experts/test";

describe("CreateCoursePage", () => {
  it("should create a course", async () => {
    render(<CreateCoursePage />);

    await fillCourseInformationStep({
      title: "New Course",
      description: "Course description",
      category: "programming",
    });

    await submitCourseForm();

    expect(screen.getByText(/success/i)).toBeInTheDocument();
  });
});
```

---

## Common Migration Issues

### Issue 1: Import Errors

**Problem:**

```
Cannot find module '@experts/hooks' or its corresponding type declarations
```

**Solution:**

```bash
yarn install
# or
yarn upgrade @experts/hooks@latest
```

### Issue 2: Type Errors

**Problem:**

```
Property 'nextStep' does not exist on type 'UseCourseFormReturn'
```

**Solution:**
Update to `useCourseFormWithAnalytics`:

```diff
- const form = useCourseForm();
+ const courseForm = useCourseFormWithAnalytics();
- form.handleNext();
+ courseForm.nextStep();
```

### Issue 3: Missing Props

**Problem:**

```
Property 'totalSteps' is missing in type
```

**Solution:**
Add all required props to CourseFormLayout:

```typescript
<CourseFormLayout
  title="Create New Course"
+ totalSteps={TOTAL_STEPS}
+ activeStep={activeStep}
+ stepTitles={STEP_TITLES}
  // ... all other required props
/>
```

### Issue 4: Step Components Not Rendering

**Problem:**
Steps show blank content.

**Solution:**
Ensure `useCourseStepsConfig` dependencies are correct:

```typescript
const courseSteps = useCourseStepsConfig({
  formData, // Required
  errors, // Required
  updateField, // Required
  // ... all other props
});
```

### Issue 5: Modals Not Opening

**Problem:**
Clicking "Add Module" does nothing.

**Solution:**
Pass modal components to CourseModalsManager:

```typescript
<CourseModalsManager
  {...courseForm}
+ LessonModal={LessonModal}
+ ModuleModal={ModuleModal}
+ QuizModal={QuizModal}
+ DiscardChangesModal={DiscardChangesModal}
/>
```

---

## Testing After Migration

### Manual Testing Checklist

- [ ] Create new course works
- [ ] Edit existing course works
- [ ] Step navigation works
- [ ] Form validation shows errors
- [ ] Module add/edit/delete works
- [ ] Lesson add/edit/delete works
- [ ] Quiz add/edit/delete works
- [ ] Drag-and-drop reordering works
- [ ] Image upload works
- [ ] Auto-save works (edit mode)
- [ ] Form submission works
- [ ] Unsaved changes warning works
- [ ] Preview pane updates correctly
- [ ] All modals open/close correctly

### Automated Testing

Run the test suite:

```bash
# Run all course tests
yarn test apps/experts-portal/src/app/(dashboard)/courses

# Run specific test files
yarn test create/page.test.tsx
yarn test edit/page.test.tsx
```

### Visual Regression Testing

Compare before/after screenshots:

```bash
# Take screenshots of old version
yarn test:visual --update-snapshots

# Migrate code

# Compare with new version
yarn test:visual
```

---

## Rollback Plan

If migration fails, you can rollback:

### Option 1: Git Revert

```bash
git revert HEAD
git push
```

### Option 2: Feature Flag

Keep both implementations and toggle:

```typescript
const USE_NEW_SYSTEM = process.env.NEXT_PUBLIC_USE_NEW_COURSE_FORM === "true";

export default function CreateCoursePage() {
  if (USE_NEW_SYSTEM) {
    return <NewCreateCoursePage />;
  }
  return <OldCreateCoursePage />;
}
```

---

## Getting Help

If you encounter issues during migration:

1. Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
2. Review [API_REFERENCE.md](./API_REFERENCE.md)
3. Check test files for examples
4. Contact Logix Development Team

---

## Post-Migration

After successful migration:

1. Delete old code
2. Update documentation
3. Train team on new patterns
4. Monitor production for issues
5. Collect feedback for improvements

---

**Migration Support:** Contact the Logix Development Team for assistance.
