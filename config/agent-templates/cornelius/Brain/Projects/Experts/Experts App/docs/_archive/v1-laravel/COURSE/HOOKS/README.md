---
title: "Course Management Hooks"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/course"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Course Management Hooks

This package provides SWR-based hooks for managing courses in the Experts platform.

## Available Hooks

### `useCourses(filters?)`

Main hook for fetching and managing course listings with pagination and filtering.

```tsx
import { useCourses } from "@experts/hooks";

function CourseList() {
  const {
    courses,
    pagination,
    isLoading,
    error,
    createCourse,
    updateCourse,
    deleteCourse,
  } = useCourses({
    status: "published",
    page: 1,
    per_page: 10,
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      {courses.map((course) => (
        <div key={course.uuid}>
          <h3>{course.title}</h3>
          <p>{course.description}</p>
          <span>Status: {course.status}</span>
        </div>
      ))}
    </div>
  );
}
```

**Features:**

- ✅ Pagination support
- ✅ Filtering by status, category, provider, etc.
- ✅ Optimistic updates for mutations
- ✅ Automatic error handling and retries
- ✅ Loading states for all operations

### `useCourse(uuid)`

Hook for managing a single course.

```tsx
import { useCourse } from "@experts/hooks";

function CourseEdit({ courseUuid }) {
  const {
    course,
    isLoading,
    error,
    updateCourse,
    deleteCourse,
    publishCourse,
  } = useCourse(courseUuid);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!course) return <div>Course not found</div>;

  const handlePublish = () => {
    publishCourse();
  };

  return (
    <div>
      <h1>{course.title}</h1>
      <p>{course.description}</p>
      <button onClick={handlePublish}>
        {course.isPublished ? "Unpublish" : "Publish"}
      </button>
    </div>
  );
}
```

**Features:**

- ✅ Single course data fetching
- ✅ Course mutations (update, delete, publish)
- ✅ Model-based data transformation
- ✅ Business logic getters (isPublished, isDraft, etc.)

### `useCourseModules(courseUuid)`

Hook for managing course modules.

```tsx
import { useCourseModules } from "@experts/hooks";

function ModuleList({ courseUuid }) {
  const { modules, isLoading, createModule, updateModule, deleteModule } =
    useCourseModules(courseUuid);

  const handleCreateModule = () => {
    createModule({
      title: "New Module",
      description: "Module description",
      order: modules.length + 1,
    });
  };

  return (
    <div>
      {modules.map((module) => (
        <div key={module.uuid}>
          <h4>{module.title}</h4>
          <p>{module.description}</p>
        </div>
      ))}
      <button onClick={handleCreateModule}>Add Module</button>
    </div>
  );
}
```

**Features:**

- ✅ Module CRUD operations
- ✅ Automatic cache invalidation
- ✅ Loading states for mutations
- ✅ Pagination support

### `useCourseStats()`

Hook for fetching course statistics.

```tsx
import { useCourseStats } from "@experts/hooks";

function CourseStats() {
  const { stats, isLoading, error } = useCourseStats();

  if (isLoading) return <div>Loading stats...</div>;
  if (error) return <div>Error loading stats</div>;
  if (!stats) return <div>No stats available</div>;

  return (
    <div>
      <h3>Course Statistics</h3>
      <p>Total Courses: {stats.total_courses}</p>
      <p>Published: {stats.published_courses}</p>
      <p>Drafts: {stats.draft_courses}</p>
    </div>
  );
}
```

**Features:**

- ✅ Automatic refresh every 30 seconds
- ✅ Error handling and retries
- ✅ Loading states

## Convenience Hooks

### `usePublishedCourses(filters?)`

Filter courses by published status.

### `useDraftCourses(filters?)`

Filter courses by draft status.

### `useArchivedCourses(filters?)`

Filter courses by archived status.

### `useCoursesByStatus(status, filters?)`

Filter courses by any specific status.

### `useCourseModule(courseUuid, moduleUuid)`

Get a specific module from a course.

## Data Transformation

All hooks automatically transform raw API data into model instances, providing:

- **Type Safety**: Full TypeScript support
- **Business Logic**: Access to computed properties and methods
- **Validation**: Built-in validation methods
- **API Payloads**: Easy serialization for mutations

## Error Handling

Hooks provide comprehensive error handling:

- **Automatic Retries**: Failed requests are retried with exponential backoff
- **Error States**: Clear error indicators and messages
- **Fallback UI**: Graceful degradation when data is unavailable

## Performance Features

- **SWR Caching**: Intelligent caching and revalidation
- **Optimistic Updates**: Immediate UI feedback for mutations
- **Background Sync**: Automatic data synchronization
- **Debounced Requests**: Prevents excessive API calls

## Usage Examples

### Creating a Course

```tsx
const { createCourse, isCreatingCourse } = useCourses();

const handleCreate = async () => {
  try {
    await createCourse({
      title: "New Course",
      description: "Course description",
      instructor: "John Doe",
      category: "Technology",
      price: 99.99,
      status: "draft",
    });
    toast.success("Course created successfully!");
  } catch (error) {
    toast.error("Failed to create course");
  }
};
```

### Updating a Course

```tsx
const { updateCourse, isUpdatingCourse } = useCourse(courseUuid);

const handleUpdate = async () => {
  try {
    await updateCourse({
      title: "Updated Title",
      description: "Updated description",
    });
    toast.success("Course updated successfully!");
  } catch (error) {
    toast.error("Failed to update course");
  }
};
```

### Deleting a Course

```tsx
const { deleteCourse, isDeletingCourse } = useCourse(courseUuid);

const handleDelete = async () => {
  if (confirm("Are you sure you want to delete this course?")) {
    try {
      await deleteCourse();
      router.push("/courses");
      toast.success("Course deleted successfully!");
    } catch (error) {
      toast.error("Failed to delete course");
    }
  }
};
```

## Dependencies

- **SWR**: For data fetching and caching
- **@experts/services**: For API communication
- **@experts/models**: For data transformation and business logic
- **@experts/types**: For TypeScript definitions
