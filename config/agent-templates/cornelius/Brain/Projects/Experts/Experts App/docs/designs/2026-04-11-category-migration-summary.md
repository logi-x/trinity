---
title: "Category System Enhancement - Migration Summary"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/category-migration-summary"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Category System Enhancement - Migration Summary

## ✅ Completed Changes

### 1. Prisma Schema Updates

- **Category Model**: Added `slug` (unique) and `isActive` fields
- **Course Model**: Replaced `category String?` with `categoryId String?` and relation to Category
- **Event Model**: Replaced `category String?` with `categoryId String?` and relation to Category
- Added proper indexes on `categoryId` fields

### 2. API Routes Updated

- **Courses API** (`/api/v1/courses`):
  - GET: Supports both `category` (slug) and `categoryId` query params for backward compatibility
  - POST: Accepts `categoryId` instead of `category` string
  - Includes category relation in responses
- **Events API** (`/api/v1/events`):
  - GET: Supports both `category` (slug) and `categoryId` query params for backward compatibility
  - POST: Accepts both `categoryId` (preferred) and `category` (slug) for backward compatibility
  - Includes category relation in responses

### 3. TypeScript Types

- Updated `types/category.d.ts` to match new schema structure
- Simplified interfaces (removed hierarchy-related fields)

### 4. Seeders

- Updated category seeder to include `slug` and `isActive` fields

### 5. Migration Script

- Created `prisma/migrations/migrate-categories.ts` to:
  - Add slugs to existing categories
  - Create categories for existing course/event category strings
  - Migrate Course.category strings to categoryId
  - Migrate Event.category strings to categoryId

## 📋 Next Steps

### 1. Run the Migration Script

```bash
cd apps/experts-app
npx tsx prisma/migrations/migrate-categories.ts
```

### 2. Create Prisma Migration

After running the migration script, create the database migration:

```bash
pnpm prisma migrate dev --name enhance_categories
```

This will:

- Add `slug` and `is_active` columns to `categories` table
- Add `category_id` columns to `courses` and `events` tables
- Create foreign key constraints
- Add indexes

### 3. Review and Drop Old Columns

After verifying the migration works correctly, you'll need to manually drop the old `category` string columns:

```sql
ALTER TABLE courses DROP COLUMN category;
ALTER TABLE events DROP COLUMN category;
```

Or create a follow-up migration:

```bash
pnpm prisma migrate dev --name drop_old_category_columns
```

### 4. Update Frontend Components

Update any frontend components that:

- Use `category` string field directly
- Need to use `categoryId` or `category.slug` instead

Key files to check:

- `src/components/courses/CourseCard.tsx`
- `src/components/events/EventCard.tsx`
- Course/Event creation/edit forms
- Category filters

### 5. Regenerate Prisma Client

```bash
pnpm prisma generate
```

## 🔄 Backward Compatibility

The API routes maintain backward compatibility by:

- Accepting `category` query param (slug) in addition to `categoryId`
- Resolving category slugs to IDs automatically
- Returning category objects in responses (not just IDs)

## 📝 Key Design Decisions

1. **No Hierarchies**: Categories remain flat (no parent/child relationships)
2. **Slug-based URLs**: Categories use slugs for URL-friendly identifiers
3. **Soft Deletion**: `isActive` flag allows hiding categories without breaking data
4. **Referential Integrity**: Foreign keys ensure data consistency
5. **Backward Compatible**: API supports both old (slug) and new (ID) patterns during transition

## 🎯 Benefits

- ✅ Referential integrity (no typos or inconsistent category names)
- ✅ URL-friendly slugs for category pages
- ✅ Better query performance with indexes
- ✅ Easier category management (admin can activate/deactivate)
- ✅ Type-safe category relationships
- ✅ Foundation for future category features without schema changes
