---
title: "ImageUpload Component Usage Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/image-upload"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# ImageUpload Component Usage Guide

## Overview

The `ImageUpload` component is a highly reusable, feature-rich image upload component built for the Experts project. It supports drag & drop, file validation, progress tracking, custom upload functions, and multiple customization options.

## Basic Usage

```tsx
import { ImageUpload } from "@experts/ui";

function ProfilePage() {
  const [avatarUrl, setAvatarUrl] = useState("");

  return (
    <ImageUpload
      imageUrl={avatarUrl}
      onImageChange={setAvatarUrl}
      endpoint="/api/profile/avatar"
    />
  );
}
```

## Props Reference

### Core Props

| Prop            | Type                    | Default         | Description                  |
| --------------- | ----------------------- | --------------- | ---------------------------- |
| `imageUrl`      | `string`                | `undefined`     | Current image URL to display |
| `onImageChange` | `(url: string) => void` | **Required**    | Callback when image changes  |
| `endpoint`      | `string`                | `"/api/upload"` | Upload endpoint URL          |
| `isLoading`     | `boolean`               | `false`         | Show loading skeleton        |

### Customization Props

| Prop          | Type                                | Default        | Description                |
| ------------- | ----------------------------------- | -------------- | -------------------------- |
| `size`        | `"sm" \| "md" \| "lg" \| "xl"`      | `"md"`         | Component size             |
| `shape`       | `"circle" \| "rounded" \| "square"` | `"rounded"`    | Upload area shape          |
| `className`   | `string`                            | `""`           | Additional CSS classes     |
| `placeholder` | `React.ReactNode`                   | Default avatar | Custom placeholder content |

### File Validation Props

| Prop           | Type       | Default                                                  | Description                 |
| -------------- | ---------- | -------------------------------------------------------- | --------------------------- |
| `accept`       | `string`   | `"image/*"`                                              | File input accept attribute |
| `maxSize`      | `number`   | `5242880` (5MB)                                          | Maximum file size in bytes  |
| `allowedTypes` | `string[]` | `["image/jpeg", "image/png", "image/webp", "image/gif"]` | Allowed MIME types          |
| `fieldName`    | `string`   | `"image"`                                                | Form field name for upload  |

### Feature Control Props

| Prop               | Type      | Default | Description                  |
| ------------------ | --------- | ------- | ---------------------------- |
| `showProgress`     | `boolean` | `true`  | Show upload progress         |
| `enableDragDrop`   | `boolean` | `true`  | Enable drag and drop         |
| `disabled`         | `boolean` | `false` | Disable upload functionality |
| `showRemoveButton` | `boolean` | `false` | Show remove image button     |

### Custom Handlers

| Prop        | Type                              | Description            |
| ----------- | --------------------------------- | ---------------------- |
| `onUpload`  | `(file: File) => Promise<string>` | Custom upload function |
| `onError`   | `(error: Error) => void`          | Custom error handler   |
| `onSuccess` | `(url: string) => void`           | Custom success handler |

### Accessibility Props

| Prop                  | Type              | Default          | Description                      |
| --------------------- | ----------------- | ---------------- | -------------------------------- |
| `ariaLabel`           | `string`          | `"Upload image"` | ARIA label for upload input      |
| `initials`            | `string`          | `"U"`            | Initials for default placeholder |
| `uploadButtonContent` | `React.ReactNode` | `<Camera />`     | Custom upload button content     |

## Usage Examples

### 1. Profile Avatar Upload

```tsx
function ProfileAvatar() {
  const [avatar, setAvatar] = useState("");

  return (
    <ImageUpload
      imageUrl={avatar}
      onImageChange={setAvatar}
      endpoint="/api/user/avatar"
      size="lg"
      shape="circle"
      showRemoveButton
      initials="JD"
      ariaLabel="Upload profile picture"
    />
  );
}
```

### 2. Course Thumbnail Upload

```tsx
function CourseThumbnail() {
  const [thumbnail, setThumbnail] = useState("");

  return (
    <ImageUpload
      imageUrl={thumbnail}
      onImageChange={setThumbnail}
      endpoint="/api/courses/thumbnail"
      size="xl"
      shape="rounded"
      fieldName="thumbnail"
      maxSize={10 * 1024 * 1024} // 10MB
      placeholder={
        <div className="text-center">
          <Upload className="mx-auto h-12 w-12 text-gray-400" />
          <p className="mt-2 text-sm text-gray-600">Course Thumbnail</p>
        </div>
      }
    />
  );
}
```

### 3. Multiple Image Upload with Custom Handler

```tsx
function GalleryUpload() {
  const [images, setImages] = useState<string[]>([]);

  const handleCustomUpload = async (file: File): Promise<string> => {
    // Custom upload logic (e.g., to AWS S3)
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/api/upload-to-s3", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    return result.url;
  };

  const addImage = (url: string) => {
    setImages((prev) => [...prev, url]);
  };

  return (
    <div className="grid grid-cols-3 gap-4">
      {images.map((url, index) => (
        <ImageUpload
          key={index}
          imageUrl={url}
          onImageChange={(newUrl) => {
            setImages((prev) =>
              prev.map((img, i) => (i === index ? newUrl : img)),
            );
          }}
          onUpload={handleCustomUpload}
          size="md"
          showRemoveButton
        />
      ))}
      <ImageUpload
        imageUrl=""
        onImageChange={addImage}
        onUpload={handleCustomUpload}
        size="md"
        placeholder={
          <div className="text-center">
            <Plus className="mx-auto h-8 w-8 text-gray-400" />
            <p className="text-xs text-gray-500">Add Image</p>
          </div>
        }
      />
    </div>
  );
}
```

### 4. Document Upload with Custom Validation

```tsx
function DocumentUpload() {
  const [docUrl, setDocUrl] = useState("");

  const handleError = (error: Error) => {
    console.error("Upload failed:", error);
    toast.error("Upload Failed", {
      description: error.message,
    });
  };

  const handleSuccess = (url: string) => {
    toast.success("Document uploaded successfully!");
    // Additional success logic
  };

  return (
    <ImageUpload
      imageUrl={docUrl}
      onImageChange={setDocUrl}
      endpoint="/api/documents/upload"
      accept=".pdf,.doc,.docx,image/*"
      allowedTypes={[
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "image/jpeg",
        "image/png",
      ]}
      maxSize={20 * 1024 * 1024} // 20MB
      onError={handleError}
      onSuccess={handleSuccess}
      fieldName="document"
      placeholder={
        <div className="text-center">
          <FileText className="mx-auto h-8 w-8 text-gray-400" />
          <p className="text-xs text-gray-500">Upload Document</p>
        </div>
      }
    />
  );
}
```

### 5. Disabled State with Custom Styling

```tsx
function ReadOnlyImage() {
  return (
    <ImageUpload
      imageUrl="/path/to/image.jpg"
      onImageChange={() => {}} // No-op
      disabled
      size="md"
      className="opacity-75"
      ariaLabel="Read-only image display"
    />
  );
}
```

### 6. Compact Size with Minimal UI

```tsx
function CompactUpload() {
  const [image, setImage] = useState("");

  return (
    <ImageUpload
      imageUrl={image}
      onImageChange={setImage}
      size="sm"
      shape="circle"
      showProgress={false}
      enableDragDrop={false}
      uploadButtonContent={<Plus className="h-3 w-3" />}
    />
  );
}
```

## Advanced Integration

### With React Hook Form

```tsx
import { useController } from "react-hook-form";

function FormImageUpload({ control, name, ...props }) {
  const {
    field: { onChange, value },
    fieldState: { error },
  } = useController({
    name,
    control,
    rules: { required: "Image is required" },
  });

  return (
    <div>
      <ImageUpload imageUrl={value} onImageChange={onChange} {...props} />
      {error && <p className="text-red-500 text-sm mt-1">{error.message}</p>}
    </div>
  );
}
```

### With SWR for Data Fetching

```tsx
import useSWR from "swr";

function UserProfile({ userId }) {
  const { data: user, mutate } = useSWR(`/api/users/${userId}`);

  const handleAvatarChange = async (newUrl: string) => {
    // Optimistic update
    mutate({ ...user, avatar: newUrl }, false);

    // Update on server
    await fetch(`/api/users/${userId}`, {
      method: "PATCH",
      body: JSON.stringify({ avatar: newUrl }),
    });

    // Revalidate
    mutate();
  };

  return (
    <ImageUpload
      imageUrl={user?.avatar}
      onImageChange={handleAvatarChange}
      endpoint="/api/upload/avatar"
    />
  );
}
```

## Styling Customization

The component uses Tailwind classes and can be customized through:

1. **Size variants**: `sm`, `md`, `lg`, `xl`
2. **Shape variants**: `circle`, `rounded`, `square`
3. **Custom className**: Additional styling
4. **CSS variables**: For theme-based customization

## Best Practices

1. **Always provide meaningful aria labels** for accessibility
2. **Set appropriate file size limits** based on your use case
3. **Handle errors gracefully** with custom error handlers
4. **Use optimistic updates** for better UX
5. **Validate file types** on both client and server
6. **Provide loading states** for better feedback
7. **Test with different file sizes** and types

## TypeScript Support

The component is fully typed with TypeScript, providing excellent IntelliSense and type safety. All props are properly typed with detailed JSDoc comments.
