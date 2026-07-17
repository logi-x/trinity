---
title: "Course Management Troubleshooting Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/course"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Course Management Troubleshooting Guide

> **Version:** 2.0
> **Last Updated:** October 2025

Solutions to common issues when working with the course management system.

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Build & Runtime Errors](#build--runtime-errors)
3. [Form Issues](#form-issues)
4. [Auto-save Issues](#auto-save-issues)
5. [Component Rendering](#component-rendering)
6. [Performance Issues](#performance-issues)
7. [Testing Issues](#testing-issues)
8. [Integration Issues](#integration-issues)

---

## Installation & Setup

### Issue: Module not found '@experts/hooks'

**Error:**

```
Cannot find module '@experts/hooks' or its corresponding type declarations
```

**Solution:**

```bash
# Install missing package
yarn add @experts/hooks@latest

# Or install all dependencies
yarn install

# Clear cache if still failing
rm -rf node_modules .next
yarn install
```

---

### Issue: Type errors after upgrading

**Error:**

```
Property 'nextStep' does not exist on type 'UseCourseFormReturn'
```

**Solution:**

```bash
# Upgrade to latest version
yarn upgrade @experts/hooks@latest @experts/ui@latest @experts/types@latest

# Restart TypeScript server in IDE
# VSCode: Cmd+Shift+P -> "TypeScript: Restart TS Server"

# Clear TypeScript cache
rm -rf node_modules/.cache
```

---

### Issue: Peer dependency warnings

**Warning:**

```
warning "@experts/ui > @experts/hooks@2.0.0" has incorrect peer dependency "react@^18.3.1"
```

**Solution:**

```bash
# Update React and related packages
yarn add react@^18.3.1 react-dom@^18.3.1

# Or use --force to override
yarn install --force
```

---

## Build & Runtime Errors

### Issue: Page shows blank content

**Symptom:**
Page loads but shows nothing.

**Common Causes & Solutions:**

1. **Missing mounted check:**

```typescript
// ❌ Problem
export default function CreateCoursePage() {
  const courseForm = useCourseFormWithAnalytics();
  return <div>...</div>; // SSR/hydration mismatch
}

// ✅ Solution
export default function CreateCoursePage() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const courseForm = useCourseFormWithAnalytics();

  if (!mounted) return null;

  return <div>...</div>;
}
```

2. **Hook called conditionally:**

```typescript
// ❌ Problem
if (isEditMode) {
  const courseForm = useCourseFormWithAnalytics(course);
}

// ✅ Solution
const courseForm = useCourseFormWithAnalytics(isEditMode ? course : undefined);
```

---

### Issue: Cannot read property of undefined

**Error:**

```
TypeError: Cannot read property 'title' of undefined
```

**Solution:**

Add null checks:

```typescript
// ❌ Problem
const title = courseForm.formData.title;

// ✅ Solution
const title = courseForm?.formData?.title || "";
```

Or wait for data to load:

```typescript
const {data: course, isLoading} = useCourse(uuid);

if (isLoading) return <Spinner />;
if (!course) return <div>Course not found</div>;

const courseForm = useCourseFormWithAnalytics(course);
```

---

### Issue: Too many re-renders

**Error:**

```
Error: Too many re-renders. React limits the number of renders to prevent an infinite loop.
```

**Common Causes & Solutions:**

1. **Function in dependency array:**

```typescript
// ❌ Problem
useEffect(() => {
  updateField("title", "value");
}, [updateField]); // New function every render!

// ✅ Solution
const handleUpdate = useCallback(() => {
  updateField("title", "value");
}, []);

useEffect(() => {
  handleUpdate();
}, [handleUpdate]);
```

2. **setState in render:**

```typescript
// ❌ Problem
function Component() {
  setCount(count + 1); // Re-renders infinitely!
  return <div>{count}</div>;
}

// ✅ Solution
function Component() {
  useEffect(() => {
    setCount(count + 1);
  }, []); // Only once
  return <div>{count}</div>;
}
```

---

## Form Issues

### Issue: Form validation not working

**Symptom:**
Form submits even with invalid data.

**Solution:**

Check validation is called:

```typescript
// ❌ Problem
const handleSubmit = async () => {
  await submitForm(); // No validation!
};

// ✅ Solution
const { handleSubmit } = useCourseFormHandlers({
  hasUnsavedChanges,
  validateForm, // Validation included
  submitForm,
  openDiscardModal,
  formData,
});
```

Or validate manually:

```typescript
const handleSubmit = async () => {
  if (!validateForm(formData)) {
    toast.error("Please fix all errors");
    return;
  }
  await submitForm();
};
```

---

### Issue: Form data not updating

**Symptom:**
User types in input but value doesn't change.

**Solution:**

Use `updateField` correctly:

```typescript
// ❌ Problem
<Input
  value={formData.title}
  onChange={(e) => {
    formData.title = e.target.value; // Mutation!
  }}
/>

// ✅ Solution
<Input
  value={formData.title}
  onChange={(e) => {
    updateField("title", e.target.value);
  }}
/>
```

---

### Issue: Form errors not showing

**Symptom:**
Validation fails but no error messages appear.

**Solution:**

Pass errors to inputs:

```typescript
// ❌ Problem
<Input
  value={formData.title}
  onChange={(e) => updateField("title", e.target.value)}
/>

// ✅ Solution
<Input
  value={formData.title}
  onChange={(e) => updateField("title", e.target.value)}
  isInvalid={!!errors.title}
  errorMessage={errors.title}
/>
```

---

### Issue: Step navigation blocked

**Symptom:**
Clicking "Next" does nothing.

**Solution:**

Check step validation:

```typescript
// Validation must pass for current step
console.log(errors); // Check what's failing

// Ensure validation logic is correct
const validateStep = (step: number) => {
  if (step === 1) {
    return formData.title && formData.description;
  }
  // ... other steps
};
```

---

## Auto-save Issues

### Issue: Auto-save not triggering

**Symptom:**
Making changes but auto-save never activates.

**Solution:**

1. **Check if in edit mode:**

```typescript
// Auto-save only works in edit mode
const courseForm = useCourseFormWithAnalytics(existingCourse); // Pass existing course
```

2. **Check if enabled:**

```typescript
console.log(courseForm.isAutoSaveEnabled); // Should be true
```

3. **Check connectivity:**

```typescript
console.log(courseForm.isOnline); // Should be true
```

---

### Issue: Auto-save saves too frequently

**Symptom:**
Every keystroke triggers a save.

**Solution:**

Auto-save is debounced by 2 seconds by default. If saving too often:

```typescript
// Check debounce implementation
// Should use useDebounce with 2000ms delay

const debouncedFormData = useDebounce(formData, 2000);

useEffect(() => {
  if (isAutoSaveEnabled && debouncedFormData) {
    saveToDraft();
  }
}, [debouncedFormData, isAutoSaveEnabled]);
```

---

### Issue: Auto-save indicator stuck

**Symptom:**
"Saving..." indicator never goes away.

**Solution:**

1. **Check API response:**

```typescript
// Ensure API call completes
const saveToDraft = async () => {
  setIsAutoSaving(true);
  try {
    await api.updateCourse(courseUuid, formData);
    setLastAutoSave(new Date());
  } catch (error) {
    console.error("Auto-save failed:", error);
  } finally {
    setIsAutoSaving(false); // Always set to false
  }
};
```

2. **Check for network errors:**

```bash
# Open browser DevTools Network tab
# Look for failed requests
# Check request/response
```

---

## Component Rendering

### Issue: Step component not showing

**Symptom:**
Active step shows blank content.

**Solution:**

1. **Check step configuration:**

```typescript
const courseSteps = useCourseStepsConfig({
  formData,
  errors,
  updateField,
  // ... ensure ALL required props are passed
});

console.log(courseSteps); // Should have 4 steps
console.log(courseSteps[activeStep - 1]); // Should have component
```

2. **Check step renderer:**

```typescript
<CourseStepRenderer
  activeStep={activeStep} // Should be 1-4
  steps={courseSteps}     // Should be array of 4 steps
/>
```

---

### Issue: Preview not updating

**Symptom:**
Making changes but preview doesn't reflect them.

**Solution:**

1. **Check if preview content is passed:**

```typescript
<CourseFormLayout
  previewContent={<CoursePreviewContent {...previewProps} />}
  // ...other props
>
  {children}
</CourseFormLayout>
```

2. **Check preview props:**

```typescript
const previewProps = {
  formData, // Must be current formData
  previewMode,
  selectedLessonIndex,
  // ... all other required props
};
```

3. **Check memoization:**

```typescript
// If memoized, ensure dependencies are correct
const previewContent = useMemo(
  () => <CoursePreviewContent {...previewProps} />,
  [formData, previewMode, selectedLessonIndex] // Update when these change
);
```

---

### Issue: Modals not opening

**Symptom:**
Clicking "Add Module" does nothing.

**Solution:**

1. **Check modal manager:**

```typescript
<CourseModalsManager
  {...courseForm}
  LessonModal={LessonModal}
  ModuleModal={ModuleModal}
  QuizModal={QuizModal}
  DiscardChangesModal={DiscardChangesModal}
/>
```

2. **Check modal state:**

```typescript
console.log(courseForm.isModuleModalOpen); // Should be true when open
```

3. **Check modal components:**

```typescript
// Ensure modals are imported correctly
import { ModuleModal } from "../shared/modals/module-modal";
```

---

### Issue: Drag and drop not working

**Symptom:**
Can't reorder modules or lessons.

**Solution:**

1. **Check sortable components:**

```typescript
// Ensure using correct sortable components
import { SortableList } from "../shared/sortables/sortable-list";
import { ModuleSortableItem } from "../shared/sortables/module-sortable-item";
```

2. **Check reorder handlers:**

```typescript
<SortableList
  items={formData.modules}
  onReorder={courseForm.onReorderModules} // Must be provided
  renderItem={(module) => <ModuleSortableItem module={module} />}
/>
```

---

## Performance Issues

### Issue: Page is slow/laggy

**Symptom:**
Page feels sluggish, especially when typing.

**Solution:**

1. **Check for unnecessary re-renders:**

```bash
# Install React DevTools Profiler
# Record interaction
# Look for components rendering too often
```

2. **Memoize expensive components:**

```typescript
const previewContent = useMemo(
  () => <CoursePreviewContent {...props} />,
  [/* minimal dependencies */]
);
```

3. **Use debounced updates:**

```typescript
const debouncedTitle = useDebounce(title, 300);

useEffect(() => {
  if (debouncedTitle !== formData.title) {
    updateField("title", debouncedTitle);
  }
}, [debouncedTitle]);
```

---

### Issue: Large file uploads freeze UI

**Symptom:**
Uploading image freezes the interface.

**Solution:**

1. **Check upload implementation:**

```typescript
// Should be async and show progress
const handleImageChange = async (file: File) => {
  setIsUploading(true);
  try {
    const url = await uploadWithProgress(file, (progress) => {
      setUploadProgress(progress);
    });
    setPreviewImage(url);
  } finally {
    setIsUploading(false);
  }
};
```

2. **Show progress indicator:**

```typescript
{isUploading && (
  <Progress value={uploadProgress} />
)}
```

---

## Testing Issues

### Issue: Tests failing with "Cannot find module"

**Error:**

```
Cannot find module '@experts/test' from 'page.test.tsx'
```

**Solution:**

```bash
# Install test package
yarn add -D @experts/test@latest

# Clear Jest cache
yarn test --clearCache

# Restart test runner
```

---

### Issue: Mock not working

**Error:**

```
TypeError: useCourseFormWithAnalytics is not a function
```

**Solution:**

Ensure mock is set up correctly:

```typescript
// ❌ Problem
vi.mock("@experts/hooks");

// ✅ Solution
vi.mock("@experts/hooks", async () => {
  const { mockUseCourseFormWithAnalytics } = await import("@experts/test");
  return {
    useCourseFormWithAnalytics: mockUseCourseFormWithAnalytics(),
  };
});
```

---

### Issue: Test times out

**Error:**

```
Test timeout of 5000ms exceeded
```

**Solution:**

1. **Increase timeout:**

```typescript
it("should submit form", async () => {
  // ...test code
}, 10000); // 10 second timeout
```

2. **Use waitFor:**

```typescript
await waitFor(() => {
  expect(screen.getByText(/success/i)).toBeInTheDocument();
});
```

3. **Check for async issues:**

```typescript
// Make sure to await async actions
await fillCourseInformationStep({...});
await submitCourseForm();
```

---

## Integration Issues

### Issue: API returns 403 Forbidden

**Error:**

```
Error: Request failed with status code 403
```

**Solution:**

1. **Check authentication:**

```typescript
// Ensure user is logged in
const {data: session} = useSession();
if (!session) {
  return <div>Please log in</div>;
}
```

2. **Check course ownership:**

```typescript
// Ensure user owns the course (edit mode)
const {data: course, error} = useCourse(uuid);
if (error?.status === 403) {
  return <div>You don't have permission to edit this course</div>;
}
```

---

### Issue: API returns 422 Validation Error

**Error:**

```
{
  "status": 422,
  "errors": {
    "title": "Title is required",
    "price": "Price must be positive"
  }
}
```

**Solution:**

1. **Check validation matches backend:**

```typescript
// Frontend validation should match backend
// Check API documentation for validation rules
```

2. **Display server errors:**

```typescript
try {
  await submitForm();
} catch (error) {
  if (error.status === 422) {
    // Update form errors with server errors
    setErrors(error.errors);
  }
}
```

---

### Issue: Image upload fails

**Error:**

```
Error: File too large
```

**Solution:**

1. **Check file size:**

```typescript
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

if (file.size > MAX_FILE_SIZE) {
  toast.error("Image must be less than 5MB");
  return;
}
```

2. **Check file type:**

```typescript
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"];

if (!ALLOWED_TYPES.includes(file.type)) {
  toast.error("Only JPG, PNG, and WebP images are allowed");
  return;
}
```

3. **Check server configuration:**

```bash
# Check nginx/server upload limits
# nginx.conf
client_max_body_size 10M;
```

---

## Debug Checklist

When encountering an issue:

1. **Check browser console:**
   - Open DevTools (F12)
   - Check Console tab for errors
   - Check Network tab for failed requests

2. **Check component tree:**
   - React DevTools
   - Verify component hierarchy
   - Check props are passed correctly

3. **Check state:**
   - Console log formData
   - Console log errors
   - Check activeStep

4. **Check network:**
   - Network tab in DevTools
   - Check API request/response
   - Verify endpoints are correct

5. **Check dependencies:**
   - Verify all packages are installed
   - Check versions are compatible
   - Clear node_modules and reinstall

6. **Check documentation:**
   - Review [API_REFERENCE.md](./API_REFERENCE.md)
   - Check [USAGE_GUIDE.md](./USAGE_GUIDE.md)
   - See examples in test files

---

## Getting Help

If you can't resolve the issue:

1. **Search existing issues:**
   - Check GitHub issues
   - Check Slack channel history

2. **Create a minimal reproduction:**
   - Simplify to smallest failing case
   - Remove unrelated code
   - Provide complete code example

3. **Gather information:**
   - Error message (full stack trace)
   - Browser and version
   - Package versions
   - Steps to reproduce

4. **Contact support:**
   - Logix Development Team
   - Include all information above
   - Provide reproduction repository if possible

---

## Common Error Reference

| Error                               | Cause                | Solution                                        |
| ----------------------------------- | -------------------- | ----------------------------------------------- |
| Cannot find module '@experts/hooks' | Missing dependency   | `yarn add @experts/hooks`                       |
| Property 'nextStep' does not exist  | Old hook version     | `yarn upgrade @experts/hooks@latest`            |
| Too many re-renders                 | Infinite loop        | Check useEffect dependencies                    |
| Cannot read property of undefined   | Missing null check   | Add `?.` optional chaining                      |
| Form data not updating              | Direct mutation      | Use `updateField`                               |
| Auto-save not working               | Not in edit mode     | Pass existing course to hook                    |
| Step component blank                | Missing props        | Pass all required props to useCourseStepsConfig |
| Modal not opening                   | Modal not in manager | Add modal to CourseModalsManager                |
| Test timeout                        | Async not awaited    | Add `await` to async actions                    |
| 403 Forbidden                       | Not authenticated    | Check user session and permissions              |

---

## See Also

- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture
- [API_REFERENCE.md](./API_REFERENCE.md) - API documentation
- [USAGE_GUIDE.md](./USAGE_GUIDE.md) - Usage examples
- [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) - Migration guide
- [BEST_PRACTICES.md](./BEST_PRACTICES.md) - Best practices
