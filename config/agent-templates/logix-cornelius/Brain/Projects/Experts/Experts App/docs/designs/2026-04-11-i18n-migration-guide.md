---
title: "i18n migration guide: cookie-based → URL-based"
date: "2026-04-11"
tags: ["project/experts", "docs/v4", "topic/i18n", "topic/nextjs"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# i18n Migration Guide: Cookie-based → URL-based

This guide explains how to migrate from cookie-based to URL-based internationalization.

## Architecture Overview

### Before (Cookie-based)

```
/courses         ← language from cookie
/events
/[username]/
```

### After (URL-based)

```
/en/courses      ← English
/ar/courses      ← Arabic
/@username       ← Global profile (not language-scoped)
```

## Benefits

✅ **SEO**: Each language is uniquely indexable
✅ **Sitemaps**: Clean separation (`sitemap-en.xml`, `sitemap-ar.xml`)
✅ **hreflang**: Proper language alternates
✅ **Better UX**: Shareable URLs with correct language
✅ **Cookie = UX only**: Still remembers user preference

---

// Before
import Link from "next/link";
import {useRouter, usePathname} from "next/navigation";

// After
import {Link, useRouter, usePathname} from "@/i18n/routing";

1. Footer.tsx

// Before
import Link from "next/link";

// After
import {Link} from "@/i18n/routing";

1. GlobalSearch.tsx

// Before
import {useRouter} from "next/navigation";

// After
import {useRouter} from "@/i18n/routing";

## Migration Steps

### 1. App Directory Restructure

**Target structure:**

```
app/
├── [locale]/              ← NEW: Locale-scoped routes
│   ├── (home)/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── opengraph-image.tsx
│   ├── (auth)/
│   │   ├── login/
│   │   ├── register/
│   │   └── ...
│   ├── courses/
│   │   ├── page.tsx
│   │   ├── [id]/
│   │   └── opengraph-image.tsx
│   ├── events/
│   ├── community/
│   ├── admin/
│   ├── creator/
│   ├── dashboard/
│   ├── pricing/
│   ├── layout.tsx         ← Locale-specific layout
│   └── ...
│
├── @[username]/           ← RENAMED: Global profiles
│   ├── page.tsx
│   ├── layout.tsx
│   ├── (tabs)/
│   │   ├── about/
│   │   ├── courses/
│   │   ├── events/
│   │   └── ...
│   └── ...
│
├── api/                   ← NO CHANGE: API routes
│   └── v1/
│       └── ...
│
├── layout.tsx             ← Root layout
├── page.tsx               ← NEW: Root redirect page
├── robots.ts
├── sitemap.ts
└── ...
```

### 2. Migration Commands

#### Option A: Manual Migration (Recommended for safety)

```bash
# 1. Create [locale] directory
mkdir -p app/[locale]

# 2. Move route groups into [locale]
mv app/(home) app/[locale]/
mv app/(auth) app/[locale]/
mv app/(content) app/[locale]/
mv app/(user) app/[locale]/

# 3. Move feature routes into [locale]
mv app/courses app/[locale]/
mv app/events app/[locale]/
mv app/community app/[locale]/
mv app/admin app/[locale]/
mv app/creator app/[locale]/
mv app/pricing app/[locale]/
mv app/affiliate app/[locale]/
mv app/invoice app/[locale]/
mv app/invoices app/[locale]/

# 4. Rename [username] to @[username]
mv app/[username] app/@[username]

# 5. Keep these at root level (NO locale prefix)
# - api/
# - (console)/
# - (errors)/
# - og-live/ (or move if it should be localized)
```

#### Option B: Automated Script

Create `scripts/migrate-i18n.sh`:

```bash
#!/bin/bash

# Create locale directory
mkdir -p app/[locale]

# Move locale-scoped routes
LOCALE_ROUTES=(
  "(home)" "(auth)" "(content)" "(user)"
  "courses" "events" "community" "admin"
  "creator" "pricing" "affiliate" "invoice" "invoices"
)

for route in "${LOCALE_ROUTES[@]}"; do
  if [ -d "app/$route" ]; then
    mv "app/$route" "app/[locale]/"
    echo "✓ Moved $route"
  fi
done

# Rename username route
if [ -d "app/[username]" ]; then
  mv "app/[username]" "app/@[username]"
  echo "✓ Renamed [username] → @[username]"
fi

echo "✓ Migration complete!"
```

Run with:

```bash
chmod +x scripts/migrate-i18n.sh
./scripts/migrate-i18n.sh
```

### 3. Update Root Layout

**File: `app/layout.tsx`**

```typescript
import {NextIntlClientProvider} from "next-intl";
import {getMessages} from "next-intl/server";

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Get messages for the current locale
  const messages = await getMessages();

  return (
    <html suppressHydrationWarning>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
```

### 4. Create Locale Layout

**File: `app/[locale]/layout.tsx`**

```typescript
import {notFound} from "next/navigation";
import {setRequestLocale} from "next-intl/server";
import {locales} from "@/i18n/config";

type Props = {
  children: React.ReactNode;
  params: Promise<{locale: string}>;
};

export function generateStaticParams() {
  return locales.map((locale) => ({locale}));
}

export default async function LocaleLayout({children, params}: Props) {
  const {locale} = await params;

  // Validate locale
  if (!locales.includes(locale as any)) {
    notFound();
  }

  // Enable static rendering
  setRequestLocale(locale);

  return <>{children}</>;
}
```

### 5. Create Root Redirect Page

**File: `app/page.tsx`**

```typescript
import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import { defaultLocale, type Locale, locales } from "@/i18n/config";

export default async function RootPage() {
  // Get locale preference from cookie
  const cookieStore = await cookies();
  const localeCookie = cookieStore.get("locale")?.value;

  // Determine locale
  const locale: Locale =
    localeCookie && locales.includes(localeCookie as Locale)
      ? (localeCookie as Locale)
      : defaultLocale;

  // Redirect to locale-prefixed home
  redirect(`/${locale}`);
}
```

### 6. Update All Page Components

Add locale parameter to all pages in `[locale]/`:

**Before:**

```typescript
export default function CoursesPage() {
  // ...
}
```

**After:**

```typescript
import { setRequestLocale } from "next-intl/server";

type Props = {
  params: Promise<{ locale: string }>;
};

export default async function CoursesPage({ params }: Props) {
  const { locale } = await params;
  setRequestLocale(locale);

  // ... rest of component
}
```

### 7. Update Navigation Links

**Before:**

```typescript
import Link from "next/link";

<Link href="/courses">Courses</Link>
```

**After:**

```typescript
import {Link} from "@/i18n/routing";

<Link href="/courses">Courses</Link>
```

The `Link` component from `@/i18n/routing` automatically prefixes the locale!

### 8. Language Switcher Component

**File: `src/components/language-switcher.tsx`**

```typescript
"use client";

import {useLocale} from "next-intl";
import {usePathname, useRouter} from "@/i18n/routing";
import {locales, localeNames} from "@/i18n/config";
import {setUserLocale} from "@/i18n/locale";

export function LanguageSwitcher() {
  const locale = useLocale();
  const pathname = usePathname();
  const router = useRouter();

  const handleLocaleChange = async (newLocale: string) => {
    // Save preference to cookie
    await setUserLocale(newLocale as any);

    // Navigate to same page in new locale
    router.replace(pathname, {locale: newLocale});
  };

  return (
    <select value={locale} onChange={(e) => handleLocaleChange(e.target.value)}>
      {locales.map((loc) => (
        <option key={loc} value={loc}>
          {localeNames[loc]}
        </option>
      ))}
    </select>
  );
}
```

### 9. Update Sitemaps

**File: `app/sitemap.ts`** (index)

```typescript
import { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || "https://experts.com.sa";

  return [
    {
      url: `${baseUrl}/sitemap-en.xml`,
      lastModified: new Date(),
    },
    {
      url: `${baseUrl}/sitemap-ar.xml`,
      lastModified: new Date(),
    },
    {
      url: `${baseUrl}/sitemap-profiles.xml`,
      lastModified: new Date(),
    },
  ];
}
```

**File: `app/sitemap-en.xml/route.ts`**

```typescript
import { MetadataRoute } from "next";
import { prisma } from "@/lib/prisma";

export async function GET() {
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || "https://experts.com.sa";

  const courses = await prisma.course.findMany({
    where: { published: true },
    select: { id: true, updatedAt: true },
  });

  const sitemap: MetadataRoute.Sitemap = [
    {
      url: `${baseUrl}/en`,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 1.0,
    },
    {
      url: `${baseUrl}/en/courses`,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 0.9,
    },
    ...courses.map((course) => ({
      url: `${baseUrl}/en/courses/${course.id}`,
      lastModified: course.updatedAt,
      changeFrequency: "weekly" as const,
      priority: 0.8,
    })),
  ];

  return new Response(generateSitemapXML(sitemap), {
    headers: {
      "Content-Type": "application/xml",
    },
  });
}

function generateSitemapXML(sitemap: MetadataRoute.Sitemap): string {
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${sitemap
  .map(
    (item) => `
  <url>
    <loc>${item.url}</loc>
    <lastmod>${item.lastModified?.toISOString()}</lastmod>
    <changefreq>${item.changeFrequency || "weekly"}</changefreq>
    <priority>${item.priority || 0.5}</priority>
  </url>`,
  )
  .join("")}
</urlset>`;
}
```

Create similar `app/sitemap-ar.xml/route.ts` for Arabic.

**File: `app/sitemap-profiles.xml/route.ts`**

```typescript
import { MetadataRoute } from "next";
import { prisma } from "@/lib/prisma";

export async function GET() {
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || "https://experts.com.sa";

  const users = await prisma.user.findMany({
    where: {
      username: { not: null },
      status: "active",
    },
    select: { username: true, updatedAt: true },
  });

  const sitemap: MetadataRoute.Sitemap = users.map((user) => ({
    url: `${baseUrl}/@${user.username}`,
    lastModified: user.updatedAt,
    changeFrequency: "weekly",
    priority: 0.6,
  }));

  return new Response(generateSitemapXML(sitemap), {
    headers: {
      "Content-Type": "application/xml",
    },
  });
}

// ... same generateSitemapXML function
```

### 10. Update Metadata for hreflang

**File: `app/[locale]/courses/page.tsx`**

```typescript
import { Metadata } from "next";

type Props = {
  params: Promise<{ locale: string }>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || "https://experts.com.sa";

  return {
    title: locale === "ar" ? "الدورات" : "Courses",
    alternates: {
      canonical: `${baseUrl}/${locale}/courses`,
      languages: {
        en: `${baseUrl}/en/courses`,
        ar: `${baseUrl}/ar/courses`,
      },
    },
  };
}

export default async function CoursesPage({ params }: Props) {
  // ...
}
```

---

## Testing Checklist

After migration, test:

- [ ] `/` redirects to `/en` or `/ar` based on preference
- [ ] `/en/courses` loads correctly
- [ ] `/ar/courses` loads correctly
- [ ] `/@ahmed` loads (profile route)
- [ ] Language switcher works
- [ ] Cookie is set when visiting locale URLs
- [ ] API routes still work (`/api/...`)
- [ ] Sitemap files generate correctly
- [ ] OG images still work
- [ ] Build succeeds: `pnpm build`
- [ ] No hydration errors

---

## Rollback Plan

If you need to rollback:

```bash
# Move routes back to root
mv app/[locale]/(home) app/
mv app/[locale]/(auth) app/
mv app/[locale]/courses app/
# ... repeat for all routes

# Rename username back
mv app/@[username] app/[username]

# Remove [locale] directory
rm -rf app/[locale]

# Restore old files
git restore proxy.ts
git restore src/i18n/request.ts
git restore src/i18n/locale.ts
rm src/i18n/routing.ts  # Remove new file
```

---

## Common Issues

### Issue: "Cannot find module '@/i18n/routing'"

**Solution**: Restart dev server after creating routing.ts

### Issue: 404 on locale routes

**Solution**: Ensure [locale] directory exists and proxy.ts is running

### Issue: Infinite redirect

**Solution**: Check proxy.ts matcher config, ensure API routes are excluded

### Issue: Profile routes not working

**Solution**: Verify `@[username]` directory name (must have `@` prefix)

---

## Next Steps

After migration:

1. Update all internal `Link` components to use `@/i18n/routing`
2. Add language switcher to navigation
3. Test all routes manually
4. Monitor server logs for redirect loops
5. Submit updated sitemap to Google Search Console
