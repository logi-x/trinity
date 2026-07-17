---
title: "Course Management Best Practices"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/course"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Course Management Best Practices

> **Version:** 2.0
> **Last Updated:** October 2025

Guidelines and best practices for working with the course management system.

## Table of Contents

1. [Component Design](#component-design)
2. [Hook Usage](#hook-usage)
3. [State Management](#state-management)
4. [Performance](#performance)
5. [Testing](#testing)
6. [Error Handling](#error-handling)
7. [Accessibility](#accessibility)
8. [Code Organization](#code-organization)

---

## Component Design

### ✅ DO: Keep Components Focused

Each component should have a single responsibility:

```typescript
// ✅ Good: Focused component
function CourseTitle({title, onTitleChange, error}) {
  return (
    <Input
      label="Course Title"
      value={title}
      onChange={(e) => onTitleChange(e.target.value)}
      isInvalid={!!error}
      errorMessage={error}
    />
  );
}

// ❌ Bad: Too many responsibilities
function CourseForm({onSubmit}) {
  // Handles title, description, pricing, modules, validation, etc.
  // 500+ lines of code
}
```

### ✅ DO: Use Composition Over Inheritance

```typescript
// ✅ Good: Composition
<CourseFormLayout
  title="Create Course"
  previewContent={<CoursePreviewContent {...props} />}
>
  <CourseStepRenderer steps={steps} activeStep={activeStep} />
</CourseFormLayout>

// ❌ Bad: Inheritance
class CreateCoursePage extends BaseCoursePage {
  // Tight coupling, hard to modify
}
```

### ✅ DO: Extract Reusable Components

```typescript
// ✅ Good: Reusable component
function ModuleList({modules, onEdit, onDelete}) {
  return modules.map(module => (
    <ModuleCard
      key={module.id}
      module={module}
      onEdit={() => onEdit(module)}
      onDelete={() => onDelete(module.id)}
    />
  ));
}

// Use in multiple places
<ModuleList modules={formData.modules} {...handlers} />
```

### ❌ DON'T: Duplicate Component Logic

```typescript
// ❌ Bad: Duplicated logic
function CreateCoursePage() {
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});
  // 100+ lines of duplicated logic
}

function EditCoursePage() {
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});
  // Same 100+ lines duplicated
}

// ✅ Good: Extract to hook
function useCoursePage() {
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});
  // Logic once, used everywhere
  return { formData, errors /* ... */ };
}
```

---

## Hook Usage

### ✅ DO: Use Provided Hooks

Always use the provided hooks instead of recreating logic:

```typescript
// ✅ Good: Use provided hook
const courseForm = useCourseFormWithAnalytics();
const {handleSubmit, canSaveDraft} = useCourseFormHandlers({...});

// ❌ Bad: Recreate logic
const [formData, setFormData] = useState({});
const handleSubmit = async () => {
  // Duplicate validation, submission logic
};
```

### ✅ DO: Destructure Only What You Need

```typescript
// ✅ Good: Destructure specific properties
const {formData, errors, updateField, nextStep} = courseForm;

// ❌ Bad: Use entire object everywhere
<Input onChange={(e) => courseForm.updateField("title", e.target.value)} />
```

### ✅ DO: Memoize Expensive Computations

```typescript
// ✅ Good: Memoized config
const courseSteps = useCourseStepsConfig({
  formData,
  errors,
  updateField,
  // ... props
});

// ❌ Bad: Recreate on every render
const courseSteps = [
  {step: 1, component: <Step1 />},
  {step: 2, component: <Step2 />},
]; // New array every render!
```

### ❌ DON'T: Call Hooks Conditionally

```typescript
// ❌ Bad: Conditional hook
if (isEditMode) {
  const courseForm = useCourseFormWithAnalytics(course);
}

// ✅ Good: Always call, use conditionally
const courseForm = useCourseFormWithAnalytics(isEditMode ? course : undefined);
```

---

## State Management

### ✅ DO: Use Hook State, Not Local State

```typescript
// ✅ Good: Use hook state
const { formData, updateField } = courseForm;
updateField("title", "New Title");

// ❌ Bad: Duplicate state
const [localTitle, setLocalTitle] = useState(formData.title);
// Now you have two sources of truth!
```

### ✅ DO: Update State Through Actions

```typescript
// ✅ Good: Use provided actions
courseForm.addModule(newModule);
courseForm.deleteLesson(lessonId);
courseForm.nextStep();

// ❌ Bad: Direct mutation
formData.modules.push(newModule); // Mutation!
activeStep++; // Direct state change!
```

### ✅ DO: Keep State Minimal

```typescript
// ✅ Good: Derive from source state
const hasErrors = Object.keys(errors).length > 0;
const isStepValid = !hasErrors;
const canProceed = isStepValid && !isSubmitting;

// ❌ Bad: Duplicate derived state
const [hasErrors, setHasErrors] = useState(false);
const [isStepValid, setIsStepValid] = useState(true);
const [canProceed, setCanProceed] = useState(false);
// Now you need to keep all 3 in sync!
```

### ✅ DO: Batch Related Updates

```typescript
// ✅ Good: Single update
updateField("pricing", {
  price: 99.99,
  currency: "USD",
  discount: 10,
});

// ❌ Bad: Multiple updates
updateField("price", 99.99);
updateField("currency", "USD");
updateField("discount", 10);
// 3 re-renders!
```

---

## Performance

### ✅ DO: Memoize Expensive Components

```typescript
// ✅ Good: Memoized preview
const previewContent = useMemo(
  () => <CoursePreviewContent formData={formData} {...previewProps} />,
  [formData, previewMode, selectedLessonIndex]
);

// ❌ Bad: New component every render
const previewContent = <CoursePreviewContent formData={formData} {...previewProps} />;
```

### ✅ DO: Use Callback Refs

```typescript
// ✅ Good: Stable callback
const handleModuleAdd = useCallback(
  (module: Module) => {
    courseForm.addModule(module);
  },
  [courseForm.addModule],
);

// ❌ Bad: New function every render
const handleModuleAdd = (module: Module) => {
  courseForm.addModule(module);
}; // New reference every render!
```

### ✅ DO: Lazy Load Heavy Components

```typescript
// ✅ Good: Lazy load
const QuizEditor = lazy(() => import("./quiz-editor"));

function QuizStep() {
  return (
    <Suspense fallback={<Spinner />}>
      {showQuiz && <QuizEditor {...props} />}
    </Suspense>
  );
}

// ❌ Bad: Always load
import {QuizEditor} from "./quiz-editor";
// Loaded even if never shown
```

### ✅ DO: Optimize Re-renders

```typescript
// ✅ Good: Only update when needed
const StepComponent = React.memo(({formData, errors, updateField}) => {
  // Only re-renders when props actually change
  return <div>...</div>;
});

// ❌ Bad: Re-render on every parent update
const StepComponent = ({formData, errors, updateField}) => {
  // Re-renders whenever parent re-renders
  return <div>...</div>;
};
```

---

## Testing

### ✅ DO: Test User Behavior

```typescript
// ✅ Good: Test what users do
it("should create a course", async () => {
  render(<CreateCoursePage />);

  await fillCourseInformationStep({
    title: "React Course",
    description: "Learn React",
  });

  await submitCourseForm();

  expect(screen.getByText(/success/i)).toBeInTheDocument();
});

// ❌ Bad: Test implementation details
it("should call updateField", () => {
  const updateField = vi.fn();
  render(<Step {...props} updateField={updateField} />);

  fireEvent.change(input, {target: {value: "test"}});

  expect(updateField).toHaveBeenCalledWith("title", "test");
});
```

### ✅ DO: Use Testing Utilities

```typescript
// ✅ Good: Use provided utilities
import {
  createMockCourseForm,
  fillCourseInformationStep,
  addModule,
} from "@experts/test";

const mockForm = createMockCourseForm({
  formData: { title: "Test Course" },
});

// ❌ Bad: Manual setup
const mockForm = {
  formData: { title: "Test Course" },
  errors: {},
  updateField: vi.fn(),
  nextStep: vi.fn(),
  // ... 40+ more properties to mock
};
```

### ✅ DO: Test Edge Cases

```typescript
// ✅ Good: Test edge cases
describe("CourseForm", () => {
  it("should handle empty title", () => {
    // Test validation with empty string
  });

  it("should handle very long title", () => {
    // Test with 1000 character title
  });

  it("should handle special characters", () => {
    // Test with emojis, unicode, etc.
  });

  it("should handle network errors", () => {
    // Test with failed API call
  });
});
```

### ✅ DO: Test Accessibility

```typescript
// ✅ Good: Test a11y
it("should be keyboard navigable", () => {
  render(<CourseForm />);

  const titleInput = screen.getByLabelText(/title/i);
  titleInput.focus();

  userEvent.tab();

  expect(screen.getByLabelText(/description/i)).toHaveFocus();
});

it("should announce errors to screen readers", () => {
  render(<CourseForm />);

  const errorMessage = screen.getByRole("alert");
  expect(errorMessage).toHaveTextContent("Title is required");
});
```

---

## Error Handling

### ✅ DO: Handle All Error Cases

```typescript
// ✅ Good: Comprehensive error handling
try {
  await courseForm.submitForm();
  toast.success("Course created!");
} catch (error) {
  if (error.status === 400) {
    toast.error("Invalid course data");
  } else if (error.status === 403) {
    toast.error("Permission denied");
  } else if (error.status === 500) {
    toast.error("Server error. Please try again.");
  } else {
    toast.error("An unexpected error occurred");
  }
}

// ❌ Bad: Generic error handling
try {
  await courseForm.submitForm();
} catch (error) {
  toast.error("Error");
}
```

### ✅ DO: Show User-Friendly Messages

```typescript
// ✅ Good: User-friendly message
toast.error("Title must be between 3 and 100 characters");

// ❌ Bad: Technical message
toast.error("ValidationError: title.length < 3 || title.length > 100");
```

### ✅ DO: Validate Early

```typescript
// ✅ Good: Validate on blur/change
<Input
  value={formData.title}
  onChange={(e) => {
    updateField("title", e.target.value);
    // Validate immediately
  }}
  isInvalid={!!errors.title}
  errorMessage={errors.title}
/>

// ❌ Bad: Only validate on submit
// User doesn't know about errors until submit
```

### ✅ DO: Provide Recovery Options

```typescript
// ✅ Good: Provide action
toast.error(
  <div>
    Auto-save failed. <Button onClick={retry}>Retry</Button>
  </div>,
  {duration: Infinity}
);

// ❌ Bad: Just show error
toast.error("Auto-save failed");
// User doesn't know what to do
```

---

## Accessibility

### ✅ DO: Use Semantic HTML

```typescript
// ✅ Good: Semantic elements
<form onSubmit={handleSubmit}>
  <fieldset>
    <legend>Course Information</legend>
    <label htmlFor="title">Title</label>
    <input id="title" type="text" />
  </fieldset>
</form>

// ❌ Bad: Div soup
<div onClick={handleSubmit}>
  <div>
    <div>Course Information</div>
    <div>Title</div>
    <div contentEditable />
  </div>
</div>
```

### ✅ DO: Provide ARIA Labels

```typescript
// ✅ Good: Accessible labels
<button aria-label="Add new module">
  <PlusIcon />
</button>

<div role="alert" aria-live="polite">
  {errors.title}
</div>

// ❌ Bad: No labels
<button>
  <PlusIcon />
</button>

<div>{errors.title}</div>
```

### ✅ DO: Manage Focus

```typescript
// ✅ Good: Focus management
function ModuleModal({isOpen, onClose}) {
  const firstInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      firstInputRef.current?.focus();
    }
  }, [isOpen]);

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <input ref={firstInputRef} />
    </Modal>
  );
}

// ❌ Bad: No focus management
// Modal opens, focus stays on trigger button
```

### ✅ DO: Test with Keyboard

```typescript
// ✅ Good: Keyboard accessible
<button
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === "Enter" || e.key === " ") {
      handleClick();
    }
  }}
>
  Click me
</button>

// ❌ Bad: Only mouse accessible
<div onClick={handleClick}>Click me</div>
```

---

## Code Organization

### ✅ DO: Follow File Structure

```
courses/
├── shared/              # Shared resources
│   ├── components/      # Shared components
│   ├── constants/       # Constants
│   ├── hooks/          # Custom hooks
│   ├── modals/         # Modal components
│   ├── steps/          # Step components
│   └── sortables/      # Drag-drop components
├── create/
│   ├── page.tsx        # Create page
│   └── __tests__/      # Tests
└── [uuid]/edit/
    ├── page.tsx        # Edit page
    └── __tests__/      # Tests
```

### ✅ DO: Use Consistent Naming

```typescript
// ✅ Good: Consistent naming
useCourseFormWithAnalytics;
useCourseFormHandlers;
useCourseStepsConfig;

CourseFormLayout;
CourseStepRenderer;
CourseModalsManager;
CoursePreviewContent;

TOTAL_STEPS;
STEP_TITLES;
BREADCRUMBS;

// ❌ Bad: Inconsistent naming
useCourseForm;
courseFormHandlers;
StepsConfig;

Layout;
Renderer;
ModalsController;
Preview;

totalSteps;
stepNames;
breadcrumbs;
```

### ✅ DO: Group Related Code

```typescript
// ✅ Good: Grouped imports
// React
import { useState, useEffect, useMemo } from "react";

// Next.js
import { useRouter, useParams } from "next/navigation";

// Internal hooks
import { useCourseFormWithAnalytics } from "@experts/hooks";
import { useBreadcrumbs } from "@experts/providers";

// Components
import { CourseFormLayout, CourseStepRenderer } from "@experts/ui";

// Local
import { useCourseFormHandlers } from "../shared/hooks";

// ❌ Bad: Random order
import { CourseFormLayout } from "@experts/ui";
import { useState } from "react";
import { useBreadcrumbs } from "@experts/providers";
import { useRouter } from "next/navigation";
```

### ✅ DO: Extract Magic Numbers

```typescript
// ✅ Good: Named constants
const DEBOUNCE_DELAY_MS = 2000;
const MAX_FILE_SIZE_MB = 5;
const MIN_TITLE_LENGTH = 3;
const MAX_TITLE_LENGTH = 100;

// ❌ Bad: Magic numbers
useDebounce(formData, 2000);
if (file.size > 5 * 1024 * 1024) {
  /* ... */
}
if (title.length < 3 || title.length > 100) {
  /* ... */
}
```

### ✅ DO: Add JSDoc Comments

````typescript
// ✅ Good: Documented API
/**
 * Manages course form state and actions.
 *
 * @param initialCourse - Pre-populate form (edit mode)
 * @returns Course form state and actions
 *
 * @example
 * ```tsx
 * const courseForm = useCourseFormWithAnalytics();
 * courseForm.updateField("title", "New Course");
 * await courseForm.submitForm();
 * ```
 */
export function useCourseFormWithAnalytics(
  initialCourse?: Course,
): UseCourseFormWithAnalyticsReturn {
  // Implementation
}

// ❌ Bad: No documentation
export function useCourseFormWithAnalytics(initialCourse?: Course) {
  // What does this do? How do I use it?
}
````

---

## Security

### ✅ DO: Sanitize User Input

```typescript
// ✅ Good: Sanitize HTML
import DOMPurify from "dompurify";

const cleanDescription = DOMPurify.sanitize(formData.description);

// ❌ Bad: Unsafe HTML
<div dangerouslySetInnerHTML={{__html: formData.description}} />
```

### ✅ DO: Validate File Uploads

```typescript
// ✅ Good: Validate files
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"];
const MAX_SIZE_MB = 5;

function validateFile(file: File) {
  if (!ALLOWED_TYPES.includes(file.type)) {
    throw new Error("Invalid file type");
  }
  if (file.size > MAX_SIZE_MB * 1024 * 1024) {
    throw new Error("File too large");
  }
}

// ❌ Bad: No validation
async function handleFileUpload(file: File) {
  await uploadToServer(file); // Uploads anything!
}
```

### ✅ DO: Check Permissions

```typescript
// ✅ Good: Check ownership
const {data: course, error} = useCourse(uuid);

if (error?.status === 403) {
  return <div>Access denied</div>;
}

// ❌ Bad: Assume permission
const {data: course} = useCourse(uuid);
// Allow editing anyone's course!
```

---

## Version Control

### ✅ DO: Write Descriptive Commits

```bash
# ✅ Good: Descriptive commit
git commit -m "feat(courses): Add auto-save to edit page

- Debounce form updates by 2 seconds
- Show save indicator in header
- Add toggle to enable/disable auto-save
- Fixes #DEV-160"

# ❌ Bad: Vague commit
git commit -m "fix stuff"
```

### ✅ DO: Keep Commits Focused

```bash
# ✅ Good: One concern per commit
git commit -m "refactor: Extract useCourseFormHandlers hook"
git commit -m "test: Add tests for useCourseFormHandlers"
git commit -m "docs: Update API documentation"

# ❌ Bad: Everything in one commit
git commit -m "update everything"
# 50 files changed, 2000+ additions/deletions
```

---

## Documentation

### ✅ DO: Document Public APIs

```typescript
// ✅ Good: Documented hook
/**
 * Hook for managing course form handlers.
 *
 * @param props - Handler configuration
 * @returns Submit handler, back handler, and save draft flag
 */
export function useCourseFormHandlers(props: Props): Return {
  // ...
}
```

### ✅ DO: Update Documentation

When you change code, update the docs:

1. Update API_REFERENCE.md if APIs changed
2. Update USAGE_GUIDE.md if usage patterns changed
3. Update MIGRATION_GUIDE.md if breaking changes
4. Update TROUBLESHOOTING.md if new issues discovered

### ✅ DO: Add Examples

````typescript
/**
 * @example
 * ```tsx
 * const {handleSubmit, canSaveDraft} = useCourseFormHandlers({
 *   hasUnsavedChanges: true,
 *   validateForm: (data) => true,
 *   submitForm: async () => { /* ... */ },
 *   openDiscardModal: () => { /* ... */ },
 *   formData: { /* ... */ },
 * });
 *
 * if (canSaveDraft) {
 *   await handleSaveDraft();
 * }
 * ```
 */
````

---

## Review Checklist

Before submitting code for review:

- [ ] Code follows established patterns
- [ ] Tests are comprehensive
- [ ] Documentation is updated
- [ ] Performance is optimized
- [ ] Accessibility is considered
- [ ] Error handling is robust
- [ ] Security is validated
- [ ] Types are correct
- [ ] Commits are descriptive
- [ ] No console.log statements

---

## See Also

- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture
- [API_REFERENCE.md](./API_REFERENCE.md) - API documentation
- [USAGE_GUIDE.md](./USAGE_GUIDE.md) - Usage examples
- [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) - Migration guide
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - Troubleshooting guide
