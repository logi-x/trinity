---
title: "Auth pages translation guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v4", "topic/i18n", "topic/auth"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Auth Pages Translation Guide

## How to Add Translations to Auth Pages

### Step 1: Import useTranslations

```typescript
import { useTranslations } from "next-intl";
```

### Step 2: Add hook at component start

```typescript
export default function LoginPage() {
  const t = useTranslations("auth.login");
  // ... rest of code
}
```

### Step 3: Replace hardcoded strings

```typescript
// Before:
<h2>Welcome back</h2>

// After:
<h2>{t('title')}</h2>
```

## Login Page String Replacements

Here are all the strings that need to be replaced in `login/page.tsx`:

```typescript
// Line 96: "Registration successful!"
toast.success(t('registrationSuccess'), {
  description: t('pleaseSignIn'),
});

// Line 117-122: Error messages
const message = error === "oauth_account_linked"
  ? t('errors.oauthLinked', {provider: providerLabel})
  : error === "account_deactivated"
    ? t('errors.accountDeactivated')
    : error === "AccessDenied"
      ? t('errors.accessDenied')
      : t('errors.signInFailed');

// Line 176-178: Deactivated account error
const errorMsg = t('errors.accountDeactivated');
form.setError("root", {message: errorMsg});
toast.error(t('errors.accountDeactivatedTitle'), {description: errorMsg});

// Line 183-186: Invalid credentials
const errorMsg = t('errors.invalidCredentials');
form.setError("root", {message: errorMsg});
toast.error(t('errors.signInFailedTitle'), {description: errorMsg});

// Line 189-190: Welcome back
toast.success(t('welcomeBack'), {
  description: t('redirecting'),
});

// Line 199-202: Login failed
const errorMsg = t('errors.loginFailed');
toast.error(t('errors.signInFailedTitle'), {description: errorMsg});

// Line 221-223: Social login failed
toast.error(t('errors.socialSignInFailedTitle'), {
  description: t('errors.socialSignInFailed', {provider}),
});

// Line 357: Title
<h2>{t('title')}</h2>

// Line 360-366: No account text
<p>
  {t('noAccount')}{" "}
  <Link href="/register">
    {t('createOne')}
  </Link>
</p>

// Line 429: Or continue with
<span>{t('orContinueWith')}</span>

// Line 456-465: Deactivated notice
<div>{t('errors.accountDeactivatedNoticeTitle')}</div>
<p>{t('errors.accountDeactivatedNotice')}</p>
<Link href="/contact">{t('errors.contactSupport')}</Link>

// Line 471-472: Email label
<Label>{t('email')}</Label>

// Line 479: Email placeholder (keep as is or use translation)
placeholder={t('emailPlaceholder') || "name@company.com"}

// Line 502: Password label
<Label>{t('password')}</Label>

// Line 509: Forgot password
<Link>{t('forgotPassword')}</Link>

// Line 517: Password placeholder
placeholder="••••••••" // Keep as is

// Line 550: Redirecting
{t('redirecting')}

// Line 555: Signing in
{t('signingIn')}

// Line 559: Sign in button
<span>{t('signIn')}</span>

// Line 567-574: Terms text
{t('termsText')}{" "}
<Link href="/terms">{t('termsOfService')}</Link>{" "}
{t('and')}{" "}
<Link href="/privacy">{t('privacyPolicy')}</Link>
{t('period')}
```

## Updated Translation Files Needed

Add these keys to `en/auth/login.ts` and `ar/auth/login.ts`:

```typescript
export default {
  // Existing keys
  title: "Welcome back",
  subtitle: "Sign in to continue your learning journey",
  email: "Email",
  emailPlaceholder: "name@company.com",
  password: "Password",
  forgotPassword: "Forgot password?",
  signIn: "Sign In",
  signingIn: "Signing in...",
  redirecting: "Redirecting...",
  noAccount: "Don't have an account?",
  createOne: "Create one",
  orContinueWith: "Or continue with",

  // New keys needed
  registrationSuccess: "Registration successful!",
  pleaseSignIn: "Please sign in with your credentials.",
  welcomeBack: "Welcome back!",
  termsText: "By signing in, you agree to our",
  termsOfService: "Terms of Service",
  and: "and",
  privacyPolicy: "Privacy Policy",
  period: ".",

  // Error messages
  errors: {
    oauthLinked: "That {provider} account is already linked to another user.",
    accountDeactivated:
      "This account is deactivated. Contact support to reactivate.",
    accountDeactivatedTitle: "Account Deactivated",
    accountDeactivatedNoticeTitle: "Account deactivated",
    accountDeactivatedNotice:
      "This account is deactivated. Contact support if you want to reactivate.",
    contactSupport: "Contact support",
    accessDenied:
      "Sign in was blocked. Please try another account or sign in with email.",
    signInFailed: "Sign in failed. Please try again.",
    signInFailedTitle: "Sign In Failed",
    invalidCredentials: "Invalid email or password",
    loginFailed: "Login failed. Please try again.",
    socialSignInFailedTitle: "Social Sign In Failed",
    socialSignInFailed: "Could not connect to {provider}",
  },
};
```
