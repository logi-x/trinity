---
title: "I18N test summary"
date: "2026-04-11"
tags: ["project/experts", "docs/v4", "topic/i18n", "topic/testing"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# i18n Implementation Test Summary

## ✅ Completed Updates

### 1. Core i18n Infrastructure

**Created/Updated Files:**

- ✅ `proxy.ts` - Integrated locale detection with existing auth/permissions
- ✅ `src/i18n/routing.ts` - Centralized routing configuration
- ✅ `src/i18n/request.ts` - Updated to use URL-based locale
- ✅ `src/i18n/locale.ts` - Updated cookie helpers (UX only)

### 2. Courses Route (Test Case)

**Created/Updated Files:**

- ✅ `app/[locale]/layout.tsx` - Locale-specific layout wrapper
- ✅ `app/[locale]/courses/page.tsx` - Updated with:
  - Locale parameter support
  - `setRequestLocale()` for static rendering
  - SEO metadata with hreflang alternates
  - Localized title/description
- ✅ `app/page.tsx` - Root redirect to locale-prefixed home

### 3. Language Switcher

**Updated:**

- ✅ `src/components/LanguageSwitcher.tsx` - Now uses:
  - URL-based routing (`useRouter`, `usePathname` from `@/i18n/routing`)
  - `useTransition` for smooth navigation
  - Cookie storage for preference (UX only)
  - No page reload - smooth client-side navigation

---

## 🧪 How to Test

### Test 1: Root Redirect

```bash
# Start dev server
pnpm dev

# Open browser to http://localhost:3025/
# Expected: Redirects to /ar or /en based on cookie/default
```

**Expected Behavior:**

- First visit: Redirects to `/ar` (default locale)
- If you previously selected English: Redirects to `/en`

### Test 2: Courses Route with Locale

**Test URLs:**

```
http://localhost:3025/en/courses  ✅ Should work
http://localhost:3025/ar/courses  ✅ Should work
http://localhost:3025/courses     ✅ Should redirect to /ar/courses or /en/courses
```

**Expected Behavior:**

- Page loads with courses content
- URL shows locale prefix (`/en/` or `/ar/`)
- Locale cookie is set automatically
- SEO metadata includes hreflang alternates

### Test 3: Language Switcher

**Steps:**

1. Visit `/en/courses`
2. Click the language switcher (Globe icon)
3. Select "العربية" (Arabic)

**Expected Behavior:**

- ✅ Smooth navigation (no page reload)
- ✅ URL changes to `/ar/courses`
- ✅ Content updates to Arabic
- ✅ Cookie is updated to `locale=ar`
- ✅ Stays on the same page (courses)

### Test 4: Direct URL Access

**Test:**

```bash
# Open in incognito/private window
http://localhost:3025/en/courses
```

**Expected:**

- Page loads in English
- Cookie is set to `locale=en`
- Subsequent visits remember the preference

### Test 5: Proxy Integration

**Test auth-protected routes:**

```
/en/dashboard    ✅ Should redirect to /en/login if not authenticated
/ar/admin        ✅ Should redirect to /ar/login if not authenticated
/en/creator      ✅ Should redirect to /en/login if not authenticated
```

**Expected:**

- Locale is preserved in redirects
- Auth flow works normally
- After login, redirects to original locale-prefixed URL

### Test 6: API Routes (Should NOT have locale)

**Test:**

```
/api/v1/courses    ✅ Should work without locale prefix
```

**Expected:**

- API routes work normally
- No `/en/api` or `/ar/api` prefix

---

## 🔍 Verification Checklist

After testing, verify:

- [ ] `/` redirects to `/ar` or `/en`
- [ ] `/en/courses` loads correctly
- [ ] `/ar/courses` loads correctly
- [ ] `/courses` redirects to locale-prefixed version
- [ ] Language switcher works without reload
- [ ] Cookie is set when visiting locale URLs
- [ ] SEO metadata includes hreflang (check page source)
- [ ] Auth redirects preserve locale
- [ ] API routes work without locale prefix
- [ ] No infinite redirects
- [ ] No console errors

---

## 🐛 Known Issues to Watch For

### Issue: "Cannot find module '@/i18n/routing'"

**Solution:**

```bash
# Restart dev server
pnpm dev
```

### Issue: 404 on locale routes

**Possible causes:**

1. Dev server not restarted after changes
2. Missing `[locale]` directory
3. Proxy.ts not running

**Solution:**

- Restart dev server
- Verify `app/[locale]/` exists
- Check terminal for proxy.ts errors

### Issue: Language switcher doesn't work

**Possible causes:**

1. Still using old `LocaleProvider`
2. Import paths incorrect

**Solution:**

- Verify LanguageSwitcher imports from `@/i18n/routing`
- Check browser console for errors

### Issue: Auth redirects lose locale

**Check:**

- `proxy.ts` `createUrl()` function
- Auth callback URLs

---

## 📊 Current State

### Routes in `[locale]` (Migrated)

- ✅ `/courses` - Fully updated with locale support

### Routes NOT in `[locale]` (Needs Migration)

- ⏳ `(home)` - Still at root `app/(home)/`
- ⏳ `(auth)` - Still at root `app/(auth)/`
- ⏳ `events` - Needs to be moved to `app/[locale]/events`
- ⏳ `community` - Needs to be moved to `app/[locale]/community`
- ⏳ `admin` - Needs to be moved to `app/[locale]/admin`
- ⏳ `creator` - Needs to be moved to `app/[locale]/creator`
- ... (other routes)

### Routes at Root (Correct)

- ✅ `api/` - No locale prefix (correct)
- ✅ `@[username]` - Global profile (no locale)
- ✅ `(console)` - Likely no locale needed
- ✅ `(errors)` - Likely no locale needed

---

## 🚀 Next Steps

### Option A: Continue Manual Migration

Move remaining routes one by one:

```bash
# Move each route and test
mv app/(home) app/[locale]/
mv app/(auth) app/[locale]/
mv app/events app/[locale]/
# etc.
```

### Option B: Bulk Migration

Use the migration script from `I18N-MIGRATION-GUIDE.md`:

```bash
chmod +x scripts/migrate-i18n.sh
./scripts/migrate-i18n.sh
```

### After Full Migration

1. Update all page components with locale parameter
2. Update all `Link` imports to use `@/i18n/routing`
3. Update metadata with hreflang
4. Test all routes
5. Update sitemaps
6. Submit to Google Search Console

---

## 📝 Testing Logs

**Date:** YYYY-MM-DD

| Test              | Status | Notes |
| ----------------- | ------ | ----- |
| Root redirect     | ⏳     |       |
| `/en/courses`     | ⏳     |       |
| `/ar/courses`     | ⏳     |       |
| Language switcher | ⏳     |       |
| Auth redirects    | ⏳     |       |
| API routes        | ⏳     |       |

**Test Results:**

```
# Add your test results here
```

---

## 🔗 Related Documentation

- **Full Migration Guide:** `I18N-MIGRATION-GUIDE.md`
- **Proxy Configuration:** `proxy.ts`
- **Routing Config:** `src/i18n/routing.ts`
- **LOCALE Discussion:** `src/i18n/LOCALE.md`
