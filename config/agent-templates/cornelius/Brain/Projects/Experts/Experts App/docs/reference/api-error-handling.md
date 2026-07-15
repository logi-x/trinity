---
title: "API error handling and validation"
date: "2026-04-11"
tags: ["project/experts", "docs/v4", "topic/api", "topic/prisma", "topic/validation"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# API Error Handling & Validation

## Overview

This document describes the error handling and validation patterns for protecting API endpoints against invalid inputs, especially Prisma P2007 errors caused by invalid UUID formats.

## The Problem

When users access invalid URLs like `/courses/opengraph-image1` or `/courses/wrong-id`, API endpoints may receive non-UUID values that cause Prisma to throw P2007 errors:

```
Error [PrismaClientKnownRequestError]:
Invalid input value: invalid input syntax for type uuid: "opengraph-image1"
code: 'P2007'
```

## Solution Architecture

### 1. UUID Validation Utilities

**Location**: `src/lib/common/validation/uuid.validation.ts`

Provides utilities for validating UUID formats before passing to Prisma:

```typescript
import {
  isValidUuid,
  uuidSchema,
  routeParamsWithIdSchema,
} from "@/lib/common/validation/uuid.validation";

// Check if string is valid UUID
if (!isValidUuid(courseId)) {
  return NextResponse.json({ error: "Invalid UUID" }, { status: 400 });
}

// Validate with Zod schema
const result = routeParamsWithIdSchema.safeParse({ id: courseId });
if (!result.success) {
  return NextResponse.json({ error: "Invalid ID" }, { status: 400 });
}
```

### 2. Prisma Error Handler

**Location**: `src/lib/common/errors/prisma-error.handler.ts`

Centralized error handling for all Prisma errors:

```typescript
import { handlePrismaError } from "@/lib/common/errors/prisma-error.handler";

try {
  const course = await prisma.course.findUnique({ where: { id } });
  return NextResponse.json(course);
} catch (error) {
  return handlePrismaError(error, "Course Detail");
}
```

**Handles these Prisma error codes**:

- `P2007`: Invalid input value (UUID format)
- `P2025`: Record not found
- `P2002`: Unique constraint violation
- `P2003`: Foreign key constraint violation
- `P2012`: Required field missing

### 3. Route Wrappers (Recommended)

**Location**: `src/lib/common/api/route-wrapper.ts`

Simplify API routes with pre-built validation and error handling:

```typescript
import { withApiRoute } from "@/lib/common/api/route-wrapper";

// Automatic UUID validation + error handling
export const GET = withApiRoute(async (request, { validatedId }) => {
  const course = await prisma.course.findUnique({
    where: { id: validatedId }, // Already validated!
  });

  return NextResponse.json(course);
}, "Course Detail");
```

## Implementation Patterns

### Pattern 1: Using Route Wrapper (Recommended)

**Best for**: New endpoints or major refactors

```typescript
// app/api/v1/courses/[id]/route.ts
import { withApiRoute } from "@/lib/common/api/route-wrapper";
import { prisma } from "@/lib/prisma";

export const GET = withApiRoute(async (request, { validatedId }) => {
  // validatedId is guaranteed to be a valid UUID
  const course = await prisma.course.findUnique({
    where: { id: validatedId },
  });

  if (!course) {
    return NextResponse.json({ error: "Course not found" }, { status: 404 });
  }

  return NextResponse.json(course);
}, "Course Detail");
```

### Pattern 2: Manual Validation

**Best for**: Existing endpoints with complex logic

```typescript
// app/api/v1/courses/[id]/enrollments/route.ts
import { routeParamsWithIdSchema } from "@/lib/common/validation/uuid.validation";
import { handlePrismaError } from "@/lib/common/errors/prisma-error.handler";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id: courseId } = await params;

    // Step 1: Validate route params
    const paramsValidation = routeParamsWithIdSchema.safeParse({
      id: courseId,
    });

    if (!paramsValidation.success) {
      return NextResponse.json(
        {
          error: "Invalid course ID format",
          details: paramsValidation.error.format(),
        },
        { status: 400 },
      );
    }

    // Step 2: Use validated ID in Prisma query
    const enrollment = await prisma.enrollment.findUnique({
      where: { userId_courseId: { userId, courseId } },
    });

    return NextResponse.json(enrollment);
  } catch (error: unknown) {
    // Step 3: Handle Prisma errors
    return handlePrismaError(error, "Enrollments");
  }
}
```

### Pattern 3: Command Schema Validation

**Best for**: Endpoints with complex input validation

```typescript
// Create schema for the command
// src/lib/courses/enrollments/commands/course-enrollment-status.schema.ts
import { z } from "zod";

export const CourseEnrollmentStatusSchema = z.object({
  userId: z.string().uuid("Invalid user ID format"),
  courseId: z.string().uuid("Invalid course ID format"),
});

// Use in API route
import { CourseEnrollmentStatusSchema } from "@/lib/courses/enrollments/commands/course-enrollment-status.schema";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id: courseId } = await params;
    const session = await auth();

    // Validate all inputs together
    const validation = CourseEnrollmentStatusSchema.safeParse({
      userId: session.user.id,
      courseId,
    });

    if (!validation.success) {
      return NextResponse.json(
        {
          error: "Invalid request parameters",
          details: validation.error.format(),
        },
        { status: 400 },
      );
    }

    const result = await handleCourseEnrollmentStatus(validation.data);
    return NextResponse.json(result);
  } catch (error) {
    return handlePrismaError(error, "Enrollments");
  }
}
```

## Protected Endpoints

The following endpoints have been protected against P2007 errors:

### Courses

- ✅ `GET /api/v1/courses/[id]` - Course detail
- ✅ `PUT /api/v1/courses/[id]` - Course update
- ✅ `DELETE /api/v1/courses/[id]` - Course delete
- ✅ `GET /api/v1/courses/[id]/enrollments` - Enrollment status

### TODO: Endpoints to Protect

Run this command to find all course endpoints with `[id]` parameter:

```bash
find app/api/v1/courses -name "route.ts" -path "*/\[id\]/*" | sort
```

Priority endpoints to protect:

- `POST /api/v1/courses/[id]/enroll`
- `GET /api/v1/courses/[id]/progress`
- `GET /api/v1/courses/[id]/modules/[moduleId]/*`
- `GET /api/v1/courses/[id]/modules/[moduleId]/lessons/[lessonId]/*`

## Error Response Examples

### Invalid UUID Format (400)

Request: `GET /api/v1/courses/opengraph-image1/enrollments`

```json
{
  "error": "Invalid course ID format",
  "details": {
    "_errors": [],
    "id": {
      "_errors": ["Invalid UUID format"]
    }
  }
}
```

### Prisma P2007 - Invalid Input (400)

If validation is missed and Prisma receives invalid UUID:

```json
{
  "error": "Invalid ID format. Expected a valid UUID."
}
```

### Record Not Found (404)

Request: `GET /api/v1/courses/00000000-0000-0000-0000-000000000000`

```json
{
  "error": "Resource not found"
}
```

### Unique Constraint Violation (409)

```json
{
  "error": "Duplicate entry for: userId, courseId"
}
```

## Testing

### Manual Testing

```bash
# Test invalid UUID format
curl -i http://localhost:3025/api/v1/courses/invalid-id/enrollments

# Should return 400 Bad Request with validation error

# Test valid UUID that doesn't exist
curl -i http://localhost:3025/api/v1/courses/00000000-0000-0000-0000-000000000000/enrollments

# Should return 404 Not Found or 200 with empty result
```

### Unit Testing

```typescript
// __tests__/api/courses/[id]/route.test.ts
import { GET } from "@/app/api/v1/courses/[id]/route";

describe("GET /api/v1/courses/[id]", () => {
  it("should return 400 for invalid UUID", async () => {
    const request = new NextRequest(
      "http://localhost:3025/api/v1/courses/invalid-id",
    );
    const params = Promise.resolve({ id: "invalid-id" });

    const response = await GET(request, { params });

    expect(response.status).toBe(400);
    const data = await response.json();
    expect(data.error).toContain("Invalid");
  });

  it("should handle valid UUID", async () => {
    const validId = "123e4567-e89b-12d3-a456-426614174000";
    const request = new NextRequest(
      `http://localhost:3025/api/v1/courses/${validId}`,
    );
    const params = Promise.resolve({ id: validId });

    const response = await GET(request, { params });

    expect(response.status).not.toBe(400);
  });
});
```

## Best Practices

### ✅ DO

1. **Validate UUIDs early** - Before any database queries
2. **Use Zod schemas** - For consistent validation
3. **Use route wrappers** - For new endpoints (less boilerplate)
4. **Log errors with context** - Include endpoint name in logs
5. **Return helpful errors** - Include validation details in response
6. **Test edge cases** - Invalid UUIDs, non-existent IDs, malformed input

### ❌ DON'T

1. **Don't skip validation** - Even if it "should never happen"
2. **Don't expose internal errors** - Use generic messages for 500 errors
3. **Don't validate in handlers** - Validate in route layer
4. **Don't ignore Prisma errors** - Always catch and handle properly
5. **Don't return stack traces** - Log them, but return safe messages

## Migration Checklist

To protect an existing endpoint:

- [ ] Add UUID validation using `routeParamsWithIdSchema`
- [ ] Wrap try-catch with `handlePrismaError`
- [ ] Add error logging with context
- [ ] Create Zod schema for command if complex
- [ ] Test with invalid UUID inputs
- [ ] Test with valid but non-existent UUIDs
- [ ] Update endpoint documentation

## Performance Considerations

- UUID validation is **very fast** (regex match)
- Zod validation adds **< 1ms** overhead
- Error handling has **no overhead** when no errors occur
- Overall impact: **negligible** (~0.1% slower)

**Recommendation**: The security and stability benefits far outweigh the minimal performance cost.

## References

- [Prisma Error Reference](https://www.prisma.io/docs/reference/api-reference/error-reference)
- [Zod Documentation](https://zod.dev/)
- [Next.js API Routes](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)
- [UUID Format Specification](https://datatracker.ietf.org/doc/html/rfc4122)
