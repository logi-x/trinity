---
title: "AUTH — Google account linking edge case"
date: "2026-04-11"
tags: ["project/experts", "docs/v4", "topic/auth", "topic/oauth"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  Q: There's a very specific edge case, where when a user A have registers with <example-a@gmail.com>, and user B have registers with <example-b@gmail.com> both with email provider, then user A from /settings/security where the user has options to connect 3rd party accounts links google account with <example-c@gmail.com> email for that google account

current behavior, which I think is wrong (real-edge-case):

<sarah.chen@example.com> registered with this email and as email provider
later on, she went to /settings/security "Connected Accounts"

Email & Password Default/Connected
Sign in with your email and password

Google
Use your Google account
Connect Button -> clicks connects e.g. <sarah.chen@gmail.com>

redirects back to /settings/security -> session refreshes

Email & Password
Sign in with your email and password
Connect Button "Not Connected anymore"

Google Default/Connected
Use your Google account

A: 1️⃣ What’s Happening Today (Restated Clearly)
Current flow (problematic)

User registers with Email & Password

<sarah.chen@example.com>
provider: email

Later, in /settings/security → Connected Accounts,
she clicks Connect Google

Google account used:

<sarah.chen@gmail.com>

After redirect:

Google becomes Default / Connected

Email & Password becomes Not Connected

👉 The system replaces the primary auth method instead of linking an additional identity.

2️⃣ Why This Is Wrong (Very Important)
❌ Identity ≠ Authentication Method

An account can have:

Multiple authentication methods

Multiple email addresses

Multiple identity providers

But it must have:

One canonical user

One stable userId

Multiple linked credentials

Your system is currently collapsing identity into provider, which is incorrect.

❌ Dangerous Side Effects

This behavior can cause:

Account lockout

User disconnects Google later

Email login is gone → user can’t log in

Silent credential switching

User didn’t consent to changing primary login

Huge UX violation

Security confusion

Which email is “the account email”?

Which email receives notifications?

Which identity owns billing?

Impossible downgrade flows

What happens if Google account is deleted?

3️⃣ The Correct Mental Model (This Is the Fix)

A user has ONE account and MANY login methods.

Never replace one with another automatically.

4️⃣ Correct Expected Behavior (What Should Happen)
After connecting Google:
Email & Password Connected
<sarah.chen@example.com>

Google Connected
<sarah.chen@gmail.com>

Optional (explicit action only):

Primary login method: Email & Password

or

Primary login method: Google

But this must be:

Explicit

User-controlled

Reversible

5️⃣ Correct UX Rules (Non-Negotiable)
✅ Rule 1: Linking ≠ Switching

Clicking Connect Google means:

“Add another way to log in”

It does NOT mean:

“Replace my login”

✅ Rule 2: Never Auto-Disconnect Credentials

A credential should only be removed if:

User explicitly clicks Disconnect

AND another login method exists

✅ Rule 3: Email Addresses Are Attributes, Not Identity

You may have:

account_email (canonical)

provider_email (Google / Apple / etc.)

They are not interchangeable.

6️⃣ How This Should Look in the UI
/settings/security → Connected Accounts
Email & Password Connected
<sarah.chen@example.com>

Google Connected
<sarah.chen@gmail.com>

[Optional]
Primary sign-in method: Email & Password
(Change)

If they try to disconnect Email:

“You must keep at least one login method connected.”

7️⃣ How This Should Look in the Data Model (High-Level)

You want one user, many auth identities.

User {
id
email // canonical / notification email
}

AuthIdentity {
id
userId
provider // email | google | apple
providerUserId
providerEmail
isPrimary // optional
}

8️⃣ Special Case: Email Mismatch (Your Exact Scenario)

This is totally OK:

Account email: <sarah.chen@example.com>
Google email: <sarah.chen@gmail.com>

They are:

Two identities

One user

Zero conflict

❗ Do NOT auto-sync or replace the account email unless the user explicitly chooses to.

9️⃣ One Simple Rule That Prevents All of This

Never delete or disable an auth method as a side effect of adding another.

Everything else flows naturally from this.

10️⃣ What You Should Change Right Now
Backend

Treat providers as linked identities

Never “switch provider” automatically

Enforce “at least one login method”

Frontend

Rename “Default” → “Connected”

Add optional “Set as primary” (later)

Make disconnect explicit and guarded
