---
title: "Course Preview Integration"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/course"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Course Preview Integration

## Overview

The `LiveCoursePreview` component provides two distinct preview modes that integrate with the `CourseFormLayout`:

1. **Compact Preview** - For sidebar (400-480px)
2. **Expanded Preview** - For full modal (up to 1280px)

## Integration Pattern

```tsx
import { CourseFormLayout } from "@experts/ui";
import { LiveCoursePreview } from "./shared/components/live-preview";

export default function CreateCoursePage() {
  const [showPreview, setShowPreview] = useState(true);
  const { formData } = useCourseForm();

  // Preview state for expanded view
  const [selectedLessonIndex, setSelectedLessonIndex] = useState(0);
  const [completedLessons, setCompletedLessons] = useState(new Set<number>());
  // ... other preview state

  return (
    <CourseFormLayout
      title="Create New Course"
      showPreview={showPreview}
      onTogglePreview={() => setShowPreview(!showPreview)}
      // Sidebar: Compact course card
      previewContent={
        <LiveCoursePreview
          formData={formData}
          previewMode="partial" // Renders renderCompactPreview()
          selectedLessonIndex={selectedLessonIndex}
          completedLessons={completedLessons}
          // ... other props
        />
      }
      // Modal: Full interactive lesson viewer
      renderExpandedPreview={() => (
        <LiveCoursePreview
          formData={formData}
          previewMode="expanded" // Renders renderExpandedPreview()
          selectedLessonIndex={selectedLessonIndex}
          completedLessons={completedLessons}
          handleLessonSelect={setSelectedLessonIndex}
          handleCompleteLesson={() => {
            setCompletedLessons(
              new Set([...completedLessons, selectedLessonIndex]),
            );
          }}
          // ... other interactive handlers
        />
      )}
    >
      <YourFormContent />
    </CourseFormLayout>
  );
}
```

## LiveCoursePreview Breakdown

### `renderCompactPreview()` (Lines 599-867)

**Purpose**: Sidebar preview showing course overview

**Content**:

- Course card with thumbnail, title, description, price
- "About This Course" tab with markdown description
- "Course Curriculum" tab with modules/lessons list
- Static, informational view

**Width**: 400-480px
**Performance**: Lightweight, renders on every keystroke

### `renderExpandedPreview()` (Lines 146-597)

**Purpose**: Full interactive learning experience

**Content**:

- **Left sidebar (33% width)**:
  - Course progress indicator
  - Module/lesson tree navigation
  - Completion checkmarks
  - Lesson selection

- **Right content (67% width)**:
  - Lesson header with title, description, duration
  - Video player placeholder
  - Markdown content with syntax highlighting
  - Additional materials
  - Quiz interface with:
    - Multiple choice questions
    - True/false questions
    - Submit functionality
    - Score display
    - Pass/fail feedback

**Width**: Up to 1280px
**Performance**: Heavy, rendered only when modal opens
**Interactivity**: Full lesson navigation, quiz completion, progress tracking

## Key Differences

| Feature        | Compact Preview        | Expanded Preview          |
| -------------- | ---------------------- | ------------------------- |
| **Location**   | Sidebar                | Modal                     |
| **Width**      | 400-480px              | Up to 1280px              |
| **Purpose**    | Quick visual feedback  | Full course experience    |
| **Content**    | Static course overview | Interactive lesson viewer |
| **Updates**    | On every keystroke     | When modal opens          |
| **Navigation** | No lesson selection    | Click lessons to view     |
| **Quiz**       | Not shown              | Fully interactive         |
| **Progress**   | Not tracked            | Lessons can be completed  |

## State Management

### Compact Preview (No State)

```tsx
previewContent={
  <LiveCoursePreview
    formData={formData}
    previewMode="partial"
    // Minimal props - static display only
    selectedLessonIndex={0}
    completedLessons={new Set()}
    handleLessonSelect={() => {}}
    handleCompleteLesson={() => {}}
    // ... other no-op handlers
  />
}
```

### Expanded Preview (Full State)

```tsx
const [selectedLessonIndex, setSelectedLessonIndex] = useState(0);
const [completedLessons, setCompletedLessons] = useState<Set<number>>(new Set());
const [showQuiz, setShowQuiz] = useState(false);
const [quizAnswers, setQuizAnswers] = useState<QuizAnswers>({});
const [quizCompleted, setQuizCompleted] = useState(false);
const [quizScore, setQuizScore] = useState<number | null>(null);

renderExpandedPreview={() => (
  <LiveCoursePreview
    formData={formData}
    previewMode="expanded"
    selectedLessonIndex={selectedLessonIndex}
    completedLessons={completedLessons}
    handleLessonSelect={setSelectedLessonIndex}
    handleCompleteLesson={() => {
      setCompletedLessons(new Set([...completedLessons, selectedLessonIndex]));
      // Auto-advance to next lesson
      if (selectedLessonIndex < allLessons.length - 1) {
        setSelectedLessonIndex(selectedLessonIndex + 1);
      }
    }}
    handleQuizAnswer={(questionId, answer) => {
      setQuizAnswers({...quizAnswers, [questionId]: answer});
    }}
    handleSubmitQuiz={() => {
      // Calculate score
      const currentQuiz = selectedLesson?.quiz;
      if (!currentQuiz) return;

      let correct = 0;
      currentQuiz.questions.forEach((question) => {
        if (quizAnswers[question.uuid] === question.correctAnswer) {
          correct++;
        }
      });

      const score = Math.round((correct / currentQuiz.questions.length) * 100);
      setQuizScore(score);
      setQuizCompleted(true);

      if (score >= (currentQuiz.passingScore || 70)) {
        // Mark lesson as completed
        setCompletedLessons(new Set([...completedLessons, selectedLessonIndex]));
      }
    }}
    showQuiz={showQuiz}
    setShowQuiz={setShowQuiz}
    quizAnswers={quizAnswers}
    setQuizAnswers={setQuizAnswers}
    quizCompleted={quizCompleted}
    setQuizCompleted={setQuizCompleted}
    quizScore={quizScore}
    setQuizScore={setQuizScore}
  />
)}
```

## Benefits of This Pattern

### Separation of Concerns

- **Compact**: Visual feedback during editing
- **Expanded**: Full course experience testing

### Performance

- **Sidebar**: Lightweight, fast updates
- **Modal**: Heavy but only loaded on-demand

### User Experience

- **Editing**: See immediate changes in sidebar
- **Testing**: Experience full course as a student would

### Development

- **Single component**: Reusable for both modes
- **Conditional rendering**: Based on `previewMode` prop
- **State isolation**: Compact has no state, expanded has full state

## Future Enhancements

### Potential Improvements

1. **Persist expanded preview state** across modal open/close
2. **Add preview mode selector** in modal toolbar
3. **Export lesson progress** to share with team
4. **Record video walkthrough** of course preview
5. **Add student view toggle** (enrolled vs. not enrolled)

This pattern ensures optimal performance and user experience throughout the course creation workflow.
