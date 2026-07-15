---
title: "🗄️ Vault Testing Strategy"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/vault-testing"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🗄️ Vault Testing Strategy

This document outlines the comprehensive testing strategy for the vault functionality in the Experts Portal.

## 🎯 Overview

The vault system handles file uploads, storage, and management for course content including:

- **Course thumbnails** (images)
- **Lesson videos** (MP4, WebM, MOV)
- **Course materials** (PDFs, documents, ZIP files)
- **Asset management** (upload, download, delete, list)

## 🧪 Testing Architecture

### 1. **API Route Tests** (`src/app/api/courses/upload/route.test.ts`)

Tests the Next.js API route that handles file uploads and proxies to Laravel.

**Coverage:**

- ✅ File validation (type, size, format)
- ✅ Authentication and authorization
- ✅ Plan-based file size limits
- ✅ Error handling and edge cases
- ✅ CORS preflight requests

**Key Test Scenarios:**

```typescript
// File type validation
it("should reject invalid file types for video", async () => {
  // Test that .txt files are rejected for video uploads
});

// Plan-based limits
it("should apply plan-specific file size limits", async () => {
  // Test enterprise vs free plan limits
});

// Error handling
it("should handle vault upload failures gracefully", async () => {
  // Test Laravel API failures
});
```

### 2. **Vault API Tests** (`src/__tests__/server/api/vault/route.test.ts`)

Tests the expected behavior of vault API endpoints that would proxy to Laravel.

**Coverage:**

- ✅ Asset listing and pagination
- ✅ Individual asset retrieval
- ✅ File upload to vault
- ✅ Asset deletion
- ✅ Storage statistics
- ✅ Download URL generation

### 3. **Component Tests** (`packages/ui/src/__tests__/dropzone.test.tsx`)

Tests the reusable `DropZoneInput` component used throughout the portal.

**Coverage:**

- ✅ Drag & drop functionality
- ✅ File validation and filtering
- ✅ Multiple file handling
- ✅ File size limits
- ✅ File type restrictions
- ✅ File removal and replacement

**Key Test Scenarios:**

```typescript
// File acceptance
it("should accept single file when maxFiles is 1", async () => {
  // Test single file upload
});

// File filtering
it("should filter files by accepted types", async () => {
  // Test only images are accepted for image uploads
});

// Size validation
it("should validate file size limits", async () => {
  // Test oversized files are rejected
});
```

### 4. **Integration Tests** (`src/__tests__/client/integration/vault/CourseMediaUpload.test.tsx`)

Tests vault functionality within the course creation workflow.

**Coverage:**

- ✅ Course thumbnail uploads
- ✅ Lesson video uploads
- ✅ Course materials uploads
- ✅ Mixed media handling
- ✅ Error scenarios and recovery

## 🚀 Running Tests

### **All Vault Tests**

```bash
npm run test:vault
```

### **Watch Mode (Development)**

```bash
npm run test:vault:watch
```

### **Specific Test Categories**

```bash
# API tests only
npm run test:api

# Component tests only
npm run test:components

# All tests with coverage
npm run test:coverage
```

### **Individual Test Files**

```bash
# Test specific API route
npm run test src/app/api/courses/upload/route.test.ts

# Test specific component
npm run test packages/ui/src/__tests__/dropzone.test.tsx

# Test specific integration
npm run test src/__tests__/client/integration/vault/CourseMediaUpload.test.tsx
```

## 🔧 Test Configuration

### **Vault-Specific Config** (`vitest.vault.config.ts`)

Specialized configuration for vault testing with:

- Custom test patterns
- Extended timeouts for file operations
- Coverage reporting
- Path aliases for @experts packages

### **Test Setup** (`src/__tests__/setup.ts`)

Global test configuration including:

- DOM testing library setup
- Mock implementations for file APIs
- Authentication mocks
- Browser API mocks

## 📊 Test Coverage Goals

| Category           | Target | Current        |
| ------------------ | ------ | -------------- |
| **API Routes**     | 95%+   | 🟡 In Progress |
| **Components**     | 90%+   | 🟡 In Progress |
| **Integration**    | 85%+   | 🟡 In Progress |
| **Error Handling** | 90%+   | 🟡 In Progress |
| **Edge Cases**     | 80%+   | 🟡 In Progress |

## 🧩 Test Data & Mocking

### **File Mocks**

```typescript
// Create test files with specific properties
const testFile = new File(["test content"], "test.txt", {
  type: "text/plain",
});

const largeFile = new File(["x".repeat(100 * 1024 * 1024)], "large.mp4", {
  type: "video/mp4",
});
```

### **API Response Mocks**

```typescript
// Mock successful upload
mockApiClient.post.mockResolvedValue({
  status: 201,
  data: {
    success: true,
    data: { uuid: "asset-123", path: "/vault/file.txt" },
  },
});

// Mock error responses
mockApiClient.post.mockRejectedValue({
  response: { status: 422, data: { message: "Validation failed" } },
});
```

## 🚨 Common Test Patterns

### **File Upload Testing**

```typescript
// 1. Create test file
const file = new File(["content"], "test.txt", { type: "text/plain" });

// 2. Simulate drop event
fireEvent.drop(dropzone, {
  dataTransfer: { files: [file] },
});

// 3. Verify callback
await waitFor(() => {
  expect(mockOnAddFiles).toHaveBeenCalledWith(file);
});
```

### **Error Handling Testing**

```typescript
// 1. Mock API failure
mockApiClient.post.mockRejectedValue(new Error("Upload failed"));

// 2. Perform action
fireEvent.drop(dropzone, { dataTransfer: { files: [file] } });

// 3. Verify error handling
await waitFor(() => {
  expect(screen.getByText("Upload failed")).toBeInTheDocument();
});
```

## 🔍 Debugging Tests

### **Verbose Output**

```bash
npm run test:vault -- --reporter=verbose
```

### **Debug Mode**

```bash
npm run test:vault -- --reporter=verbose --no-coverage
```

### **Single Test Debug**

```bash
npm run test:vault -- --reporter=verbose --grep="should upload course thumbnail successfully"
```

## 📈 Continuous Integration

### **Pre-commit Hooks**

- Run vault tests before committing
- Ensure minimum coverage thresholds
- Validate test file structure

### **CI Pipeline**

- Run all vault tests on PR
- Generate coverage reports
- Fail builds on test failures

## 🎯 Future Enhancements

### **Performance Testing**

- Large file upload performance
- Concurrent upload handling
- Memory usage optimization

### **Security Testing**

- File type spoofing prevention
- Malicious file detection
- Upload rate limiting

### **Accessibility Testing**

- Screen reader compatibility
- Keyboard navigation
- Color contrast validation

## 🤝 Contributing

### **Adding New Tests**

1. Follow existing test patterns
2. Use descriptive test names
3. Include edge case coverage
4. Add to appropriate test category

### **Test Naming Convention**

```typescript
describe("ComponentName", () => {
  it("should [expected behavior] when [condition]", async () => {
    // Test implementation
  });
});
```

### **Mock Strategy**

- Mock external dependencies
- Use realistic test data
- Avoid over-mocking
- Test actual component behavior

---

**Last Updated:** December 2024  
**Maintainer:** Development Team  
**Status:** 🟡 In Progress
