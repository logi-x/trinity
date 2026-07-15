---
title: "Sitemap structure"
date: "2026-04-11"
tags: ["project/experts", "docs/v4", "topic/seo", "topic/sitemap"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Multi-Language Sitemap Structure

## Overview

The sitemap is now structured to support multiple languages (English and Arabic) with proper hreflang alternates for optimal SEO.

## File Structure

```
app/
├── sitemap.xml/
│   └── route.ts           # Sitemap Index (/sitemap.xml)
├── sitemap-en.xml/
│   └── route.ts           # English sitemap (/sitemap-en.xml)
├── sitemap-ar.xml/
│   └── route.ts           # Arabic sitemap (/sitemap-ar.xml)
├── sitemap-profiles.xml/
│   └── route.ts           # Profiles sitemap (/sitemap-profiles.xml)
└── robots.ts              # robots.txt (points to sitemap index)

src/lib/sitemap/
└── sitemap-utils.ts       # Shared utilities for sitemap generation
```

## How It Works

### 1. Sitemap Index (`/sitemap.xml`)

The main sitemap that search engines discover first. It points to all sitemaps:

```xml
<sitemapindex>
  <sitemap>
    <loc>https://app.stg.experts.com.sa/sitemap-en.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://app.stg.experts.com.sa/sitemap-ar.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://app.stg.experts.com.sa/sitemap-profiles.xml</loc>
  </sitemap>
</sitemapindex>
```

### 2. Locale-Specific Sitemaps

#### English Sitemap (`/sitemap-en.xml`)

Contains all English URLs with `/en` prefix and hreflang alternates:

```xml
<url>
  <loc>https://app.stg.experts.com.sa/en/courses</loc>
  <xhtml:link rel="alternate" hreflang="en" href="https://app.stg.experts.com.sa/en/courses"/>
  <xhtml:link rel="alternate" hreflang="ar" href="https://app.stg.experts.com.sa/ar/courses"/>
  <changefreq>daily</changefreq>
  <priority>0.9</priority>
</url>
```

#### Arabic Sitemap (`/sitemap-ar.xml`)

Contains all Arabic URLs with `/ar` prefix and hreflang alternates:

```xml
<url>
  <loc>https://app.stg.experts.com.sa/ar/courses</loc>
  <xhtml:link rel="alternate" hreflang="en" href="https://app.stg.experts.com.sa/en/courses"/>
  <xhtml:link rel="alternate" hreflang="ar" href="https://app.stg.experts.com.sa/ar/courses"/>
  <changefreq>daily</changefreq>
  <priority>0.9</priority>
</url>
```

#### Profiles Sitemap (`/sitemap-profiles.xml`)

Contains all public user profiles with `/@username` URLs:

```xml
<url>
  <loc>https://app.stg.experts.com.sa/@john-doe</loc>
  <lastmod>2026-02-01T10:00:00.000Z</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.6</priority>
</url>
```

**Note**: Profiles are language-agnostic (no hreflang alternates) and are accessible at `/@username` without locale prefix.

## Content Included

### Static Routes

- Home page (`/en`, `/ar`)
- Courses listing (`/en/courses`, `/ar/courses`)
- Events listing (`/en/events`, `/ar/events`)
- Community (`/en/community`, `/ar/community`)
- Pricing (`/en/pricing`, `/ar/pricing`)
- About, Contact, FAQ, Features, Support
- Legal pages (Privacy, Terms, Cookies)

### Dynamic Routes

Fetched from database:

- **Courses**: All published courses (`/en/courses/[id]`, `/ar/courses/[id]`)
- **Events**: All published events (`/en/events/[id]`, `/ar/events/[id]`)
- **Posts**: All published community posts (`/en/community/[id]`, `/ar/community/[id]`)

## SEO Benefits

### 1. Hreflang Implementation

Each URL includes hreflang alternates pointing to language equivalents:

- Prevents duplicate content issues
- Helps Google serve correct language version to users
- Improves international SEO

### 2. Organized Structure

Splitting sitemaps by locale:

- Easier for search engines to crawl
- Better crawl budget allocation
- Clearer content organization

### 3. Proper Metadata

Each entry includes:

- `lastModified`: When content was last updated
- `changeFrequency`: How often content changes
- `priority`: Relative importance (0.0 - 1.0)
- `images`: Thumbnail URLs for rich results

## Priority Guidelines

| Priority | Pages                                      |
| -------- | ------------------------------------------ |
| 1.0      | Homepage (`/en`, `/ar`)                    |
| 0.9      | Main listings (courses, events, community) |
| 0.8      | Individual courses, events, pricing        |
| 0.7      | Individual posts, informational pages      |
| 0.3      | Legal pages (privacy, terms, cookies)      |

## Change Frequency Guidelines

| Frequency | Pages                                      |
| --------- | ------------------------------------------ |
| daily     | Homepage, main listings                    |
| weekly    | Individual courses, events, pricing        |
| monthly   | Informational pages (about, contact, etc.) |
| yearly    | Legal pages                                |

## Excluded from Sitemap

Routes **NOT** included (noindex or private):

- `/dashboard/*` - User dashboard
- `/admin/*` - Admin panel
- `/creator/*` - Creator dashboard
- `/affiliate/*` - Affiliate panel
- `/api/*` - API routes
- `/share/*` - Share tracking pages (redirect only)
- `/login`, `/register` - Auth pages
- `/@username` - Profile pages (separate indexing strategy)

## robots.txt Configuration

```txt
User-agent: *
Allow: /
Disallow: /dashboard
Disallow: /admin
Disallow: /creator
Disallow: /affiliate
Disallow: /api

Sitemap: https://app.stg.experts.com.sa/sitemap.xml
```

## Testing

### Local Testing

Visit these URLs in development:

- `http://localhost:3025/sitemap.xml` - Sitemap index
- `http://localhost:3025/sitemap-en.xml` - English sitemap
- `http://localhost:3025/sitemap-ar.xml` - Arabic sitemap
- `http://localhost:3025/sitemap-profiles.xml` - Profiles sitemap
- `http://localhost:3025/robots.txt` - robots.txt

### Production Testing

- `https://app.experts.com.sa/sitemap.xml`
- `https://app.experts.com.sa/sitemap-en.xml`
- `https://app.experts.com.sa/sitemap-ar.xml`
- `https://app.experts.com.sa/sitemap-profiles.xml`

### Google Search Console

1. Submit sitemap index: `https://app.experts.com.sa/sitemap.xml`
2. Google will auto-discover locale-specific sitemaps
3. Monitor coverage in Search Console

## Maintenance

### Adding New Static Routes

Edit `src/lib/sitemap/sitemap-utils.ts`:

```typescript
export function getStaticRoutes(
  locale: Locale,
  baseUrl: string,
): SitemapEntry[] {
  return [
    // ... existing routes
    {
      url: `${baseUrl}/${locale}/new-page`,
      changeFrequency: "weekly",
      priority: 0.8,
    },
  ];
}
```

### Adding New Dynamic Content Types

Edit `getDynamicEntries` in `src/lib/sitemap/sitemap-utils.ts`:

```typescript
export async function getDynamicEntries(
  locale: Locale,
  baseUrl: string,
): Promise<SitemapEntry[]> {
  const [courses, events, posts, newType] = await Promise.all([
    // ... existing queries
    prisma.newType.findMany({
      where: { published: true },
      select: { id: true, thumbnailUrl: true, updatedAt: true },
    }),
  ]);

  entries.push(
    // ... existing entries
    ...newType.map((item) => ({
      url: `${baseUrl}/${locale}/new-type/${item.id}`,
      lastModified: item.updatedAt,
      changeFrequency: "weekly" as const,
      priority: 0.7,
    })),
  );
}
```

## Best Practices

1. **Always include locale prefix** in URLs (`/en/...`, `/ar/...`)
2. **Add hreflang alternates** for all URLs with language equivalents
3. **Keep priorities realistic** - Not everything can be 1.0
4. **Update change frequency** based on actual content update patterns
5. **Exclude private/auth routes** - They should not be indexed
6. **Test after changes** - Ensure XML is valid and URLs are correct

## Resources

- [Google Search Central - Sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview)
- [Google Search Central - Hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Next.js Sitemap Documentation](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap)
