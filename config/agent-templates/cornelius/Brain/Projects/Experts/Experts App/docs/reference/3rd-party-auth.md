---
title: "3RD PARTY AUTH"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/3rd-party-auth"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 3RD PARTY AUTH

Login / registration flow (step by step)

Step 1: User clicks “Continue with Google”

You redirect → Google → callback with:

{
"provider": "google",
"providerAccountId": "1234567890",
"email": "<user@gmail.com>",
"name": "John Doe",
"avatar": "..."
}

Step 2: Find account by provider identity
const account = await prisma.account.findUnique({
where: {
provider_providerAccountId: {
provider: "google",
providerAccountId,
},
},
});

Step 3A: Account exists → login
if (account) {
return login(account.userId);
}

Done.

Step 3B: Account does NOT exist → register or link

Now you have two safe paths.

Path A: Auto-register (recommended default)
const user = await prisma.user.create({
data: {
email,
emailVerifiedAt: new Date(),
profile: {
create: {
fullName: name,
avatarUrl: avatar,
},
},
accounts: {
create: {
provider,
providerAccountId,
email,
},
},
},
});

✔ Zero friction
✔ No email verification loop
✔ Very common for consumer platforms

Path B: Account linking (advanced, optional)

If a user is already logged in and adds a provider:

await prisma.account.create({
data: {
userId: session.user.id,
provider,
providerAccountId,
email,
},
});

This allows:

Google + Apple on same account

Email + OAuth

Future flexibility

⚠️ Important: email matching rules (read carefully)
❌ DO NOT auto-link users by email alone

This is how accounts get hijacked.

Bad:

findUserByEmail(email)

Good:

Link only if:

user is already authenticated, OR

you explicitly ask user to confirm

OAuth providers ≠ email authorities.

Apple Sign-In (special notes)

Apple is tricky but manageable:

providerAccountId = sub

Email may be:

private relay

only sent once

Name only sent once

So:

Store everything you get on first login

Never assume email presence

Your schema already handles this perfectly.

Sessions (briefly)

You can:

use JWT

or DB-backed sessions

Either way, session references User, never Account.

How this fits your platform perfectly

One user can:

be a student

become an instructor

host events

join entities

Login methods don’t matter

Roles don’t matter

Content ownership stays clean

TL;DR (pin this)

Separate User from Account

Account = OAuth identity

User = platform identity

Unique (provider, providerAccountId)

Never auto-link by email

Postgres makes this clean and safe

This is how modern auth systems do it
