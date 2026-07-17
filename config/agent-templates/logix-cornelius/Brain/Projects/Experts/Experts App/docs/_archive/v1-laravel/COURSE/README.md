---
title: "Course Management System"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/course"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Course Management System

> **Version:** 2.0
> **Status:** Production Ready
> **Last Updated:** October 2025

A modern, composition-based course management system for creating and editing courses with a multi-step wizard interface.

## 📚 Documentation

Complete documentation is available in the following guides:

| Document                                             | Description                                                         |
| ---------------------------------------------------- | ------------------------------------------------------------------- |
| [**PAGE/ARCHITECTURE.md**](./PAGE/ARCHITECTURE.md)   | System architecture, design principles, and component hierarchy     |
| [**API_REFERENCE.md**](./API_REFERENCE.md)           | Complete API documentation for all hooks, components, and utilities |
| [**USAGE_GUIDE.md**](./USAGE_GUIDE.md)               | Practical examples and recipes for common use cases                 |
| [**MIGRATION_GUIDE.md**](./MIGRATION_GUIDE.md)       | Step-by-step guide for migrating from the old system                |
| [**BEST_PRACTICES.md**](./BEST_PRACTICES.md)         | Patterns, conventions, and coding guidelines                        |
| [**TROUBLESHOOTING.md**](./TROUBLESHOOTING.md)       | Solutions to common issues and problems                             |
| [**HOOKS/ARCHITECTURE.md**](./HOOKS/ARCHITECTURE.md) | Hooks Arch                                                          |
| [**HOOKS/README.md**](./HOOKS/README.md)             | Hooks Readme                                                        |

## 🚀 Quick Start

### Creating a Course Page

```typescript
"use client";

import {useEffect, useState} from "react";
import {useCourseFormWithAnalytics} from "@experts/hooks";
import {useBreadcrumbs} from "@experts/providers";
import {CourseFormLayout, CourseStepRenderer, CourseModalsManager} from "@experts/ui";
import {useCourseFormHandlers} from "./shared/hooks/use-course-form-handlers";
import {useCourseStepsConfig} from "./shared/hooks/use-course-steps-config";
import {TOTAL_STEPS, STEP_TITLES, BREADCRUMBS} from "./shared/constants/course-form-config";
import {CoursePreviewContent} from "./shared/components/course-preview-content";
import {ModuleModal, LessonModal, QuizModal, DiscardChangesModal} from "./shared/modals";

export default function CreateCoursePage() {
  const {setBreadcrumbs} = useBreadcrumbs();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setBreadcrumbs(BREADCRUMBS.CREATE);
    setMounted(true);
  }, [setBreadcrumbs]);

  const courseForm = useCourseFormWithAnalytics();
  const {handleSubmit, handleBack, canSaveDraft} = useCourseFormHandlers({...});
  const courseSteps = useCourseStepsConfig({...});

  if (!mounted) return null;

  return (
    <>
      <CourseFormLayout {...layoutProps}>
        <CourseStepRenderer activeStep={courseForm.activeStep} steps={courseSteps} />
      </CourseFormLayout>
      <CourseModalsManager {...courseForm} {...modals} />
    </>
  );
}
```

See [USAGE_GUIDE.md](./USAGE_GUIDE.md) for complete examples.

## ✨ Features

- ✅ **Multi-step Wizard** - 4-step guided course creation
- ✅ **Auto-save** - Automatic draft saving (edit mode)
- ✅ **Live Preview** - Real-time course preview
- ✅ **Drag & Drop** - Reorder modules and lessons
- ✅ **Quiz Builder** - Create and manage quizzes
- ✅ **Image Upload** - Course thumbnail with progress
- ✅ **Form Validation** - Client and server validation
- ✅ **Analytics** - Built-in analytics tracking
- ✅ **Offline Support** - Works offline, syncs when online
- ✅ **Unsaved Changes** - Warns before leaving with unsaved work

## 🏗️ Architecture

The system follows a **composition-based architecture**:

```
Page (Orchestrator)
  ├── useCourseFormWithAnalytics (State Management)
  ├── useCourseFormHandlers (Handler Logic)
  ├── useCourseStepsConfig (Step Configuration)
  │
  ├── CourseFormLayout (Structure)
  │     ├── StepIndicator
  │     ├── Navigation
  │     └── Preview Pane
  │
  ├── CourseStepRenderer (Content)
  │     ├── Step 1: Course Information
  │     ├── Step 2: Curriculum & Lessons
  │     ├── Step 3: Quizzes & Assessment
  │     └── Step 4: Review & Publish
  │
  └── CourseModalsManager (Modals)
        ├── ModuleModal
        ├── LessonModal
        ├── QuizModal
        └── DiscardChangesModal
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed architecture documentation.

## 📊 Metrics

**Code Reduction:**

- Create page: 720 → 172 lines (76% reduction)
- Edit page: 720 → 235 lines (67% reduction)
- Total: 461 lines eliminated

**Test Coverage:**

- 5 test files
- 1,609 lines of test code
- 175+ individual tests
- 85%+ coverage

**Performance:**

- Memoized step configuration
- Debounced auto-save (2s)
- Lazy-loaded heavy components
- Optimized re-renders

## 🛠️ Technology Stack

- **React** 18.3.1 - UI framework
- **Next.js** 15.0.0 - React framework
- **TypeScript** 5.7.2 - Type safety
- **NextUI** 2.6.10 - Component library
- **Framer Motion** 11.15.0 - Animations
- **Vitest** - Testing framework

## 📦 Project Structure

```
courses/
├── README.md                    # This file
├── ARCHITECTURE.md              # Architecture documentation
├── API_REFERENCE.md             # API documentation
├── USAGE_GUIDE.md               # Usage examples
├── MIGRATION_GUIDE.md           # Migration guide
├── BEST_PRACTICES.md            # Best practices
├── TROUBLESHOOTING.md           # Troubleshooting guide
│
├── shared/                      # Shared resources
│   ├── components/
│   │   ├── course-preview-content.tsx
│   │   └── __tests__/
│   ├── constants/
│   │   └── course-form-config.ts
│   ├── hooks/
│   │   ├── use-course-form-handlers.ts
│   │   ├── use-course-steps-config.tsx
│   │   └── __tests__/
│   ├── modals/
│   │   ├── module-modal.tsx
│   │   ├── lesson-modal.tsx
│   │   ├── quiz-modal.tsx
│   │   └── discard-changes-modal.tsx
│   ├── steps/
│   │   ├── course-information-step.tsx
│   │   ├── course-details-step.tsx
│   │   ├── course-curriculum-step.tsx
│   │   ├── course-quizzes-step.tsx
│   │   └── course-review-step.tsx
│   └── sortables/
│       ├── sortable-list.tsx
│       ├── module-sortable-item.tsx
│       └── lesson-sortable-item.tsx
│
├── create/
│   ├── page.tsx                 # Create page (172 lines)
│   └── __tests__/
│       └── page.test.tsx
│
├── [uuid]/
│   ├── edit/
│   │   ├── page.tsx             # Edit page (235 lines)
│   │   └── __tests__/
│   │       └── page.test.tsx
│   └── preview/
│       └── page.tsx             # Preview page
│
└── page.tsx                     # Courses list page
```

## 🧪 Testing

Run tests:

```bash
# All course tests
yarn test apps/experts-portal/src/app/(dashboard)/courses

# Specific test file
yarn test create/page.test.tsx

# With coverage
yarn test --coverage
```

Test utilities available in `@experts/test`:

```typescript
import {
  createMockCourseForm,
  fillCourseInformationStep,
  addModule,
  submitCourseForm,
  expectStepToBeActive,
} from "@experts/test";
```

See [COURSE_TESTING.md (monorepo)](https://github.com/logi-x/experts/blob/main/packages/test/docs/COURSE_TESTING.md) for testing guide.

## 🔄 Migration

Migrating from the old system? See [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) for:

- Step-by-step migration instructions
- Before/after code comparison
- Common migration issues
- Rollback strategies

## 🐛 Troubleshooting

Having issues? Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for solutions to:

- Installation & setup issues
- Build & runtime errors
- Form and validation problems
- Auto-save issues
- Component rendering problems
- Performance issues
- Testing problems

## 📖 Learning Path

Recommended reading order for new developers:

1. **README.md** (this file) - Overview and quick start
2. **ARCHITECTURE.md** - Understand the system design
3. **USAGE_GUIDE.md** - Learn through examples
4. **API_REFERENCE.md** - Reference for all APIs
5. **BEST_PRACTICES.md** - Learn patterns and conventions
6. **TROUBLESHOOTING.md** - Know how to solve problems

For migration:

1. **MIGRATION_GUIDE.md** - Step-by-step migration
2. **API_REFERENCE.md** - New API reference
3. **TROUBLESHOOTING.md** - Common migration issues

## 🤝 Contributing

When modifying the course management system:

1. **Follow established patterns** - See [BEST_PRACTICES.md](./BEST_PRACTICES.md)
2. **Add tests** - Maintain 80%+ coverage
3. **Update documentation** - Keep docs current
4. **Test thoroughly** - Manual and automated testing
5. **Review checklist** - See [BEST_PRACTICES.md#review-checklist](./BEST_PRACTICES.md#review-checklist)

## 📝 License

Internal use only - Experts Platform by Logix Development Team

## 👥 Support

- **Documentation:** See files above
- **Issues:** Create GitHub issue
- **Questions:** Contact Logix Development Team
- **Slack:** #experts-dev channel

## 🔗 Related Packages

- **@experts/hooks** - Course form hooks
- **@experts/ui** - Course UI components
- **@experts/providers** - React providers
- **@experts/types** - TypeScript types
- **@experts/test** - Testing utilities

## 📈 Changelog

### v2.0.0 (October 2025)

- ✨ Complete architecture refactor
- ✨ Composition-based design
- ✨ 76% code reduction
- ✨ 85%+ test coverage
- ✨ Comprehensive documentation
- ✨ Auto-save for edit mode
- ✨ Enhanced performance

### v1.x

- Legacy monolithic implementation
- 720-line create/edit pages
- Limited test coverage
- Minimal documentation

---

**Version:** 2.0
**Maintained by:** Logix Development Team
**Last Updated:** October 2025
