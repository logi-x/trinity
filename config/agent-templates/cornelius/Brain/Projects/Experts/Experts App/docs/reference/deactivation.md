---
title: "DEACTIVATION"
date: "2026-04-11"
tags: ["project/experts", "docs/v4", "topic/accounts", "topic/deactivation"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# DEACTIVATION

1️⃣ First: Clarify the Goal (This Avoids Bad Decisions)

When users ask for “Deactivate account”, they usually mean one of three things:

I want to stop using the product (but keep data)

I want to disappear temporarily

I want my account gone forever

You must support #1 and #2 first.

# 3 (hard delete) is a separate, later concern.

2️⃣ What “Deactivate” Should Mean (Correct Definition)

Deactivate = disable access, preserve data, reversible

Deactivation should:

Prevent login

Disable all auth providers

Hide user-generated content (or mark inactive)

Stop emails / notifications

Preserve billing & audit history

Be reversible by the user or support

Deactivation should NOT:

Delete data

Break foreign keys

Orphan content

Remove invoices / certificates

Delete OAuth links

3️⃣ The Minimal, Correct Data Model
User table
User {
id
status // active | deactivated | suspended
deactivatedAt
deactivationReason
}

That’s it.
Do not cascade deletes.

4️⃣ Backend Enforcement (This Is Critical)

Every auth entry point must check:

if (user.status !== "active") {
throw new Error("account_deactivated");
}

Apply this to:

Email/password login

OAuth callbacks

Token refresh

Session validation

⚠️ Do NOT rely on frontend only.

5️⃣ Auth Providers & Deactivation (Important)

When a user deactivates:

✅ Keep all AuthIdentity records

❌ Do NOT delete OAuth links

❌ Do NOT revoke tokens (unless required)

Why?

If they reactivate, login should “just work”

Revocation is irreversible in some providers

6️⃣ UX Flow (What Users Actually See)
/settings/security → Deactivate account

Step 1: Warning screen

Deactivating your account will:

Disable access immediately

Hide your profile and content

Stop emails and notifications

You can reactivate later by signing in again or contacting support.

Step 2: Confirmation

Require password OR OAuth re-auth

Require checkbox:

“I understand this is reversible”

Step 3: Success

Your account has been deactivated.

Immediately log them out.

7️⃣ Reactivation Flow (Don’t Forget This!)

This is where many teams fail.

Option A — Reactivate on login (recommended)

If a deactivated user logs in:

Your account is deactivated.
Do you want to reactivate it?

One click → status = active.

Option B — Support-assisted reactivation

Use this only if compliance requires it.

8️⃣ Billing & Revenue Rules (Very Important)

When deactivated:

Pause subscriptions

Do NOT delete invoices

Do NOT refund automatically

Do NOT allow new purchases

Billing systems must survive deactivation.

9️⃣ Should You Also Offer “Delete Account”?
❌ Not yet

Unless:

You have GDPR tooling

You have retention policies

You handle invoices legally

You understand content ownership

Deletion is legally and technically hard.

✅ Recommended roadmap

Deactivate (now)

Data export (later)

Hard delete (much later, manual first)

10️⃣ Edge Cases You MUST Handle
A) User with active courses/events

Deactivation hides content

Do NOT delete enrollments

Do NOT break certificates

B) OAuth-only user

Require re-auth via provider to deactivate

No password required

C) Default auth provider

Irrelevant during deactivation

Reactivation should respect previous default

11️⃣ When You Should NOT Allow Deactivation

Block or warn if:

Outstanding payouts

Active enterprise contracts

Legal holds

Compliance requirements

This can be handled with:

canDeactivate = true | false

12️⃣ One-Sentence Rule (Anchor This)

Deactivation is a reversible access switch — not a data operation.

If you follow that rule, you won’t break anything.

13️⃣ Minimal Checklist (Implement This, Nothing More)

✅ user.status flag
✅ Auth checks everywhere
✅ Logout on deactivate
✅ Pause billing
✅ Hide content
✅ Allow reactivation
