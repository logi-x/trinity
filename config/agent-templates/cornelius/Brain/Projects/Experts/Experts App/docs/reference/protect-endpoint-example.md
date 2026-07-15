---
title: "Example: protecting an endpoint from P2007 errors"
date: "2026-04-11"
tags: ["project/experts", "docs/v4", "topic/api", "topic/prisma", "topic/examples"]
category: "docs/experts-reference"
type: "example"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Example: Protecting an Endpoint from P2007 Errors

This example shows how to protect the course enrollment endpoint using the new validation utilities.

## Before (Vulnerable to P2007)

```typescript
// app/api/v1/courses/[id]/enroll/route.ts
import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const session = await auth();
    const { id: courseId } = await params;
    const body = await request.json();

    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // ⚠️ PROBLEM: No UUID validation!
    // If courseId = "opengraph-image1", Prisma throws P2007
    const enrollment = await prisma.enrollment.create({
      data: {
        userId: session.user.id,
        courseId, // Invalid UUID causes P2007!
        ...body,
      },
    });

    return NextResponse.json(enrollment);
  } catch (error: unknown) {
    // ❌ Generic error - user gets 500 for invalid UUID
    console.error("Enrollment error:", error);
    return NextResponse.json({ error: "Failed to enroll" }, { status: 500 });
  }
}
```

**Problem**:

- Visiting `/courses/invalid-id/enroll` returns 500
- P2007 error logged in console
- Poor user experience

## After: Option 1 - Route Wrapper (Recommended)

```typescript
// app/api/v1/courses/[id]/enroll/route.ts
import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { withApiRoute } from "@/lib/common/api/route-wrapper";

export const POST = withApiRoute(
  async (request: NextRequest, { validatedId: courseId }) => {
    const session = await auth();
    const body = await request.json();

    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // ✅ courseId is guaranteed to be a valid UUID
    const enrollment = await prisma.enrollment.create({
      data: {
        userId: session.user.id,
        courseId,
        ...body,
      },
    });

    return NextResponse.json(enrollment);
  },
  "Course Enrollment",
);
```

**Benefits**:

- ✅ Automatic UUID validation
- ✅ Automatic Prisma error handling
- ✅ Returns 400 for invalid UUIDs
- ✅ Less boilerplate code
- ✅ Consistent error responses

## After: Option 2 - Manual Validation

```typescript
// app/api/v1/courses/[id]/enroll/route.ts
import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { routeParamsWithIdSchema } from "@/lib/common/validation/uuid.validation";
import { handlePrismaError } from "@/lib/common/errors/prisma-error.handler";
import { z } from "zod";

// Create schema for enrollment data
const EnrollmentSchema = z.object({
  courseId: z.string().uuid("Invalid course ID"),
  userId: z.string().uuid("Invalid user ID"),
  paymentIntentId: z.string().optional(),
  enrollmentType: z.enum(["paid", "free"]),
});

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const session = await auth();

    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

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

    const body = await request.json();

    // Step 2: Validate enrollment data
    const dataValidation = EnrollmentSchema.safeParse({
      courseId,
      userId: session.user.id,
      ...body,
    });

    if (!dataValidation.success) {
      return NextResponse.json(
        {
          error: "Invalid enrollment data",
          details: dataValidation.error.format(),
        },
        { status: 400 },
      );
    }

    // Step 3: Create enrollment with validated data
    const enrollment = await prisma.enrollment.create({
      data: dataValidation.data,
    });

    return NextResponse.json(enrollment);
  } catch (error: unknown) {
    // Step 4: Handle Prisma errors
    console.error("[Course Enrollment] Error:", error);
    return handlePrismaError(error, "Course Enrollment");
  }
}
```

**Benefits**:

- ✅ Full control over validation logic
- ✅ Multiple validation steps
- ✅ Custom error messages
- ✅ Validates all input data

## Testing the Fix

### Manual Test

```bash
# Before: Returns 500
curl -X POST http://localhost:3025/api/v1/courses/invalid-id/enroll

# After: Returns 400
curl -X POST http://localhost:3025/api/v1/courses/invalid-id/enroll
# Response: {"error":"Invalid course ID format",...}
```

### Automated Test

```typescript
// app/api/v1/courses/[id]/enroll/__tests__/route.test.ts
import { describe, it, expect, vi } from "vitest";
import { POST } from "../route";

describe("POST /api/v1/courses/[id]/enroll", () => {
  it("should return 400 for invalid UUID", async () => {
    const request = new NextRequest(
      "http://localhost:3025/api/v1/courses/invalid-id/enroll",
      { method: "POST" },
    );
    const params = Promise.resolve({ id: "invalid-id" });

    const response = await POST(request, { params });

    expect(response.status).toBe(400);
    const data = await response.json();
    expect(data.error).toContain("Invalid");
  });

  it("should accept valid UUID", async () => {
    const validId = "123e4567-e89b-12d3-a456-426614174000";
    const request = new NextRequest(
      `http://localhost:3025/api/v1/courses/${validId}/enroll`,
      {
        method: "POST",
        body: JSON.stringify({ enrollmentType: "free" }),
      },
    );
    const params = Promise.resolve({ id: validId });

    const response = await POST(request, { params });

    expect(response.status).not.toBe(400);
  });
});
```

## When to Use Which Option

### Use Route Wrapper When:

- ✅ Simple endpoint with single ID parameter
- ✅ Want minimal boilerplate
- ✅ Standard error handling is sufficient
- ✅ New endpoint being created

### Use Manual Validation When:

- ✅ Complex validation logic needed
- ✅ Multiple parameters to validate
- ✅ Custom error messages required
- ✅ Need fine-grained control

## Quick Checklist

Apply this checklist when protecting an endpoint:

- [ ] Import validation utilities
- [ ] Validate route params before Prisma query
- [ ] Wrap in try-catch with Prisma error handler
- [ ] Add context to error logs
- [ ] Return 400 for validation errors
- [ ] Test with invalid UUID
- [ ] Test with valid UUID that doesn't exist
- [ ] Update documentation

## Common Mistakes to Avoid

### ❌ Don't validate after the query

```typescript
// Wrong!
const course = await prisma.course.findUnique({ where: { id: courseId } });
if (!isValidUuid(courseId)) {
  // Too late! P2007 already thrown
}
```

### ❌ Don't skip error handling

```typescript
// Wrong!
export const GET = withApiRoute(async (request, { validatedId }) => {
  const course = await prisma.course.findUnique({ where: { id: validatedId } });
  // Missing error handling for other Prisma errors (P2025, etc.)
});
```

### ❌ Don't ignore validation errors

```typescript
// Wrong!
const validation = routeParamsWithIdSchema.safeParse({ id: courseId });
// Continuing without checking validation.success
const course = await prisma.course.findUnique({ where: { id: courseId } });
```

### ✅ Do it correctly

```typescript
// Correct!
export const GET = withApiRoute(async (request, { validatedId }) => {
  const course = await prisma.course.findUnique({
    where: { id: validatedId },
  });

  if (!course) {
    return NextResponse.json({ error: "Course not found" }, { status: 404 });
  }

  return NextResponse.json(course);
}, "Course Detail");
```

## Summary

**Before**: 500 errors, P2007 exceptions, poor UX
**After**: 400 errors, helpful messages, great UX

Choose your protection method and apply to all endpoints with `[id]` parameters!
