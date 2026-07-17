---
title: "🧠 Experts Project – Technical Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/guide"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🧠 Experts Project – Technical Guide

## 🏗️ Project Architecture

```md
experts/
├── apps/
│ ├── experts-api/ # Laravel PHP API backend
│ ├── experts-app/ # Next.js App Router, Tailwind, shadcn/ui, heroui
│ ├── experts-auth/ # Next.js OAuth2 UI for login/consent
│ ├── experts-admin/ # Next.js Admin dashboard
│ ├── experts-portal/ # Next.js Instructors portal (studio)
│ ├── experts-server/ # System-level Node.js processes
│ ├── experts-ios/ # iOS app (SwiftUI + ExpertsKit)
│ ├── experts-android/ # Android app (Kotlin)
├── packages/
│ ├── ai/ # AI Packages and utilities (langchain, chromadb, etc)
│ ├── core/ # Core Packages (config/linting, services, theme, types)
│ ├── ui/ # Shared UI components (shadcn/ui, heroui, etc)
│ ├── utilities/ # Shared Utils (i18n, icons, etc)
│ ├── hooks/ # Shared React hooks (use-client, use-server, etc)
│ ├── functions/ # Global shared functions (api, utils, formatter, etc)
├── .github/
│ └── workflows/ # CI/CD GitHub Actions
├── turbo.json # Turborepo configuration
├── tailwind.config.ts # Tailwind configuration
└── tsconfig.base.json # Base TypeScript configuration
```

## 🔧 Technical Stack

### Frontend

- Next.js App Router
- TailwindCSS v4
- shadcn/ui / heroui components
- lucide icons as the default icons library, and @heroicons/react as a fallback
- TypeScript
- React Server Components
- CSS animations using `--animate-*` variables and `@keyframes`
- Theme switching via `next-themes` with cross-subdomain sync

### Data Fetching

The application uses two primary methods for data fetching:

#### SWR (Default)

- Primary data fetching solution for client components
- Built-in caching and revalidation
- Automatic error handling
- Real-time updates support

```typescript
// Example SWR usage
const { data, isLoading, error } = useSWR<PlanHistoryResponse>(
  `/v1/user/planned/history?page=${page}`,
);
```

#### Server Components

- Used for server-side data fetching
- Direct database access when possible
- Improved performance and SEO
- Reduced client-side JavaScript

#### Error Handling

- Consistent error handling with toast notifications
- Server error display using `result?.serverError`
- Success notifications for user feedback

```typescript
// Example error handling
const onSubmit = async (data) => {
  const result = await testAiCustomContentAction({ content: data.message });
  if (result?.serverError) {
    toast.error({
      title: "Error testing email",
      description: result?.serverError || "",
    });
  } else {
    toast.success({ description: "Saved!" });
  }
};
```

### Backend

- Laravel PHP API
- OAuth2 Password Authentication
- Node.js for system processes
- Laravel Passport for authentication
- Mobile deep linking support for iOS/Android

### Laravel API Backend

The Laravel API follows a domain-driven design (DDD) structure with the following key features:

#### Architecture

- Domain-driven design with self-contained modules
- Pure API with no frontend dependencies
- OAuth2 authentication via Laravel Passport
- UUID-based primary keys
- API versioning under `/api/v1/` and the endpoint will be e.g. `https://api.experts.com.sa/v1/users`

#### Directory Structure

```md
experts-api/
├── app/
│ ├── Domains/ # Domain-driven modules
│ │ ├── Users/ # Users domain
│ │ ├── Courses/ # Courses domain
│ │ └── Invoices/ # Invoices domain
│ │ └── Certificates/ # Certificates domain
│ │ └── Payments/ # Payments domain
│ ├── Support/ # Shared support classes
│ └── Http/ # HTTP layer
```

#### Key Features

- Domain-specific Actions for business logic
- API Resources for JSON transformation
- Form Requests for validation
- Custom exception handling
- Comprehensive testing suite
- Docker-based deployment
- CI/CD pipeline with code quality checks

#### Development Guidelines

- Follow PSR-12 coding standards
- Use PHP 8.3+ features
- Implement proper error handling
- Use Laravel's built-in features
- Follow SOLID principles
- Write comprehensive tests
- Document API endpoints

### LMS Platform

The Experts Project includes a comprehensive Learning Management System (LMS) with the following features:

#### Core Modules

- **Users & Roles**: Admin, Instructor, and Student roles with granular permissions
- **Courses**: Support for online, hybrid, and physical delivery modes
- **Content Management**: Sections, lessons, quizzes, and assignments
- **Enrollment**: Flexible enrollment strategies (free/paid, open/invite-only)
- **Progress Tracking**: Completion tracking, time spent, quiz scores
- **Certification**: Course completion certificates and achievement badges
- **Analytics**: Comprehensive reporting for students, instructors, and admins

#### LMS Key Features

- Course creation and management
- Video and content delivery
- Quiz and assignment system
- Progress tracking and analytics
- Certificate generation
- Payment processing
- Role-based access control
- Communication tools

#### Development Phases

1. **Foundation**: Auth, roles, basic CRUD
2. **Content Delivery**: Course builder, lesson viewer
3. **Monetization**: Payment processing, instructor payouts
4. **Analytics**: Dashboards and reporting
5. **Integrations**: External service connections

### Mobile

- iOS: SwiftUI + ExpertsKit
- Android: Kotlin

## 🎨 Theming & Styling

- TailwindCSS V4 for styling
- CSS variables for animations (`--animate-*`)
- `@keyframes` for custom animations
- Theme switching via `next-themes`
- Cross-subdomain theme sync using shared cookie (.experts.com.sa domain)
- light and dark themes with auto-detection
- RTL support
- Server-side theme persistence with useTheme() hook

## 🔍 Development Standards

### Monorepo Management

- Turborepo for workspace management
- `workspace:*` for cross-app dependencies
- Independent app configurations (Dockerfile, .env, build)
- Shared packages for common functionality
- Yarn workspaces for package management

### Code Quality

- Flat ESLint Config (eslint.config.mjs)
- Shared config in `packages/config`
- TypeScript for type safety
- Import config via: `import config from "@experts/config/eslint.config.mjs"`
- TypeScript for type safety
- ESLint for code style
- Prettier for formatting
- Husky for pre-commit hooks
- Vitest for unit testing
- Cypress for E2E testing

### Authentication & State

- Laravel Passport backend
- OAuth2 login flow via experts-auth
- Mobile deep linking support
- Cookie-based theme persistence
- Cross-domain cookie sharing
- Server-side state handling with Next.js server actions
- Typed cookies API for state management

## 🎯 Future Improvements

1. Centralize UI components in @experts/ui
2. Consolidate configuration in @experts/config
3. Move animation keyframes to global CSS
4. Standardize Docker CI flows across apps
5. Enhance cross-subdomain state management
6. Optimize build and deployment processes

## 📦 Package Management

### Main Shared Packages

- `@experts/ai`: AI packages and utilities
- `@experts/ui`: Shared UI components (shadcn/ui based, fallback to @heroui/react)
- `@experts/core`: Core functionality
- `@experts/config`: Shared configurations
- `@experts/hooks`: Common React hooks
- `@experts/functions`: Utility functions

### Utility Packages

- `@experts/utils`: Pure utility functions (formatDate, truncateText, etc.)
- `@experts/tsconfig`: TypeScript configuration
- `@experts/lint`: ESLint configuration
- `@experts/icons`: Shared icons (lucide-react as fallback)
- `@experts/i18n`: Internationalization utilities
- `@experts/services`: API services and data fetching
- `@experts/types`: Shared TypeScript definitions
- `@experts/theme`: Theme configuration
- `@experts/services/auth`: Authentication utilities

### Package Development Guidelines

1. Focus on reusability across all apps
2. Keep dependencies minimal
3. Ensure proper TypeScript typing
4. Write tests for critical functionality
5. Document the API with JSDoc comments
6. Use named exports for better tree-shaking

## 🎨 UI & Styling

### Component System

- Primary: `@heroui/react`
- Fallback: `@experts/ui` (shadcn/ui based)
- Component composition pattern
- TailwindCSS v4 for styling
- Class-variance-authority (cva) for variants
- Framer Motion for animations

### Typography

- Display text: Poppins (600 weight)
- Body text: Inter (400 weight)
- CSS variables: `--display-family`, `--text-family`
- Font classes: `font-display`, `font-text`

### Color System

- Base colors: 50-1000 scale
- Primary colors: 50-1000 scale
- Secondary colors: 50-1000 scale
- Theme variables for light/dark modes
- CSS custom properties for colors

### Animations

#### Built-in Animations

- Fade: `fade-in`, `fade-out`
- Zoom: `zoom-in`, `zoom-out`
- Slide: `slide-in-from-*`, `slide-out-to-*`
- Spin: `spin-in`, `spin-out`

#### Custom Animations

- Ripple effect
- Rainbow animation
- Shimmer effect
- Spin animation
- Shine effect
- Marquee
- Floating animation

#### Animation Properties

- Duration: `duration-*`
- Delay: `delay-*`
- Repeat: `repeat-*`
- Direction: `direction-*`
- Fill Mode: `fill-mode-*`
- Play State: `running`, `paused`

## 🧪 Testing & Quality

### Component Testing

- Unit tests for logic
- Visual regression tests
- Accessibility (a11y) compliance
- Integration tests for complex components

## 🌐 Internationalization

### i18n Features

- Multi-language support
- RTL/LTR handling
- Locale-based formatting
- Translation management
- Dynamic language switching

### i18n Usage

```typescript
import { getTranslations, getDirection } from "@experts/i18n";
const translations = await getTranslations("ar");
const direction = getDirection("ar"); // "rtl"
```

## 🔐 Authentication

### Features

- OAuth2 with Laravel Passport
- Token-based authentication
- Refresh token mechanism
- Role-based access control
- Session management

### Authentication Usage

```typescript
import { useAuth } from "@experts/services/auth";
const { user, isAuthenticated } = useAuth();
```

## 📱 Mobile Development

### iOS (SwiftUI + ExpertsKit)

- Native UI components
- SwiftUI for modern UI
- ExpertsKit for shared logic
- Deep linking support

### Android (Kotlin)

- Material Design components
- Kotlin Coroutines
- Jetpack Compose
- Deep linking support

## 🚀 Performance Optimization

1. Code splitting
2. Lazy loading
3. Image optimization
4. Caching strategies
5. Bundle size optimization
6. Server-side rendering
7. Static site generation

## 🔄 State Management

### Client-side

- React hooks for local state
- Context API for global state
- Custom hooks for shared logic

### Server-side

- Next.js server actions
- API routes
- Server components
- Typed cookies API

## 📚 Documentation

### Code Documentation

- JSDoc comments
- TypeScript types
- README files
- API documentation
- Component stories

### Development Guides

- Setup instructions
- Contribution guidelines
- Coding standards
- Architecture decisions
- Best practices

## 🔄 CI/CD

- GitHub Actions for automation
- Platform-specific workflows
- Matrix jobs for parallel processing
- Shared caching for faster builds
- Slack notifications for job status

## 🚀 Best Practices

1. Use shared packages for common functionality
2. Maintain consistent theming across apps
3. Follow TypeScript best practices
4. Implement proper error handling
5. Write comprehensive tests
6. Document code changes
7. Follow security best practices

## 📚 Examples

### Importing a component

```tsx

import { Button, Textarea, Input } from "heroui/react";

<Button variant="light" onPress={onLessonModalClose}>
    Cancel
</Button>
<Button color="primary" onPress={saveLesson}>
    {editingLessonId ? "Update Lesson" : "Add Lesson"}
</Button>

<Textarea
    placeholder="Add links to additional materials, resources, or reading materials (one per line)"
    value={currentLesson?.materials?.join("\n") || ""}
    onChange={(e) =>
        setCurrentLesson((prev) => ({
        ...prev,
        materials: e.target.value.split("\n").filter((m) => m.trim()),
        }))
    }
    variant="bordered"
    minRows={4}
/>

<Input
    label="Quiz Title"
    value={currentQuiz?.title || ""}
    onChange={(e) => setCurrentQuiz((prev) => ({...prev, title: e.target.value}))}
    variant="bordered"
    labelPlacement="outside"
    placeholder="Enter quiz title"
/>

```

### Importing a hook

```tsx
import { useTheme } from "@experts/ui";

const { theme, setTheme } = useTheme();
```

### Importing a function

```tsx
import { formatDate } from "@experts/functions";

const formattedDate = formatDate(new Date());
```

### Importing a service

```tsx
import { getUser } from "@experts/services";

const user = getUser(1);
```

```tsx
// packages/core/types/src/course.ts

import type { CourseFormData, Lesson, Quiz } from "@experts/types";

export default function CreateCoursePage() {
  const router = useRouter();
  const {providers, createCourse} = useCourses();
  const [loading, setLoading] = React.useState(false);
  const [previewImage, setPreviewImage] = React.useState<string | null>(null);
  const [activeStep, setActiveStep] = React.useState(1);
  const [formData, setFormData] = React.useState<Partial<CourseFormData>>({
    lessons: [],
    totalDuration: 0,
  });
  const [errors, setErrors] = React.useState<FormErrors>({});
  const [currentLesson, setCurrentLesson] = React.useState<Partial<Lesson> | null>(null);
  const [currentQuiz, setCurrentQuiz] = React.useState<Partial<Quiz> | null>(null);
  const [editingLessonId, setEditingLessonId] = React.useState<string | null>(null);

```
