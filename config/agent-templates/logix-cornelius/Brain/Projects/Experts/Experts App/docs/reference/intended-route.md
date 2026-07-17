---
title: "INTENDED ROUTE"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/intended-route"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# INTENDED ROUTE

Q: One of the things I liked about laravel, intended route redirection and how persistent it was, how to do the same in nextjs, without overcomplicating things ?

A: Great question. Laravel’s “intended redirect” feels magical because it’s simple, sticky, and invisible. You can absolutely get the same UX in Next.js without over-engineering.

I’ll give you one clean pattern that works everywhere (pages, actions, middleware, OAuth) and explain why it’s the right equivalent.

The core idea (Laravel → Next.js translation)

Laravel does this internally:

User hits /dashboard
→ not authenticated
→ store intended URL in session
→ redirect to /login
→ after login → redirect back

In Next.js, the clean equivalent is:

Use a callbackUrl (or redirect) query param and let auth handle it

No server-side session hacks required.

✅ The simple, correct pattern (recommended)
1️⃣ When redirecting to login, always attach callbackUrl

From middleware, layouts, or client navigation:

const loginUrl = new URL("/login", request.url);
loginUrl.searchParams.set("callbackUrl", request.nextUrl.pathname);

return NextResponse.redirect(loginUrl);

Example result:

/login?callbackUrl=/dashboard

This is your intended route.

2️⃣ On login success, redirect to callbackUrl

If you’re using NextAuth / Auth.js, this is already built in.

signIn("github", {
callbackUrl: searchParams.get("callbackUrl") ?? "/dashboard",
});

Auth.js will:

persist it through OAuth

survive redirects

work across providers

This is why it feels as smooth as Laravel.

✅ Why this works so well
Property Result
Persistent Survives OAuth redirects
Stateless No server session juggling
Secure Only redirects after auth
Simple One query param
Familiar Same mental model as Laravel

This is the Next.js-native way.

🔒 Prevent open-redirect issues (important)

Always sanitize the callback URL:

function safeCallbackUrl(url?: string) {
if (!url) return "/dashboard";
if (!url.startsWith("/")) return "/dashboard";
return url;
}

Never allow:

callbackUrl=<https://evil.com>

Laravel does this internally — you must do it explicitly.

🧠 Where to apply this (best practice)
Middleware
if (!session?.user) {
return redirectToLoginWithCallback();
}

Protected layouts
redirect(`/login?callbackUrl=${pathname}`);

Buttons / client-side actions
router.push(`/login?callbackUrl=${router.asPath}`);

🧪 What about profile-completion flows?

Same idea.

redirect(
`/complete-profile?callbackUrl=${pathname}`
);

After completion:

router.push(callbackUrl ?? "/dashboard");

Laravel-style, fully preserved.

🟡 Optional enhancement (cookie fallback)

If you really want Laravel-like stickiness across reloads:

cookies().set("intended", pathname);

Then:

read it on login

clear it after redirect

But in 90% of cases, callbackUrl is enough and cleaner.

❌ What NOT to do

❌ Store intended routes in DB

❌ Custom session tables

❌ Global state hacks

❌ Middleware-only magic

❌ Hardcoded redirects after login

Laravel looks magical — but it’s really just this pattern hidden from you.

TL;DR (Laravel → Next.js)
Laravel Next.js
redirect()->intended() callbackUrl
Session storage Query param
Automatic Auth.js handles it
Persistent OAuth-safe

If you use:

/login?callbackUrl=...

you’ve already recreated Laravel’s intended redirect — the right way for Next.js.
