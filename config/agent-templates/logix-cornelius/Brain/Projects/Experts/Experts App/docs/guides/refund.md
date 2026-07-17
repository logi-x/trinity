---
title: "REFUND GUIDE"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/refund"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# REFUND GUIDE

The key is to design refunds as a controlled exception, not a happy-path feature.

Below is a clean, defensible refund model that works for both courses and events, aligns with payments, and scales legally and operationally.

Core principle (lock this in)

Refunds are allowed, but never frictionless.

That means:

technically possible

clearly bounded

intentionally slower than enrollment

visible consequences

This discourages “try & refund” behavior without harming legitimate users.

1️⃣ Refund eligibility rules (the backbone)
🎓 Courses (self-paced)

Recommended rules

Condition Refund Allowed? Why
Within X days (e.g. 7) ✅ Consumer trust
Progress ≤ Y% (e.g. 10–20%) ✅ Prevent content consumption abuse
Certificate issued ❌ Value already delivered
Course completed ❌ Obvious
Free course ❌ Nothing to refund

Key idea

Progress gates refunds

Time gates refunds

Certificates are final

🎟 Events
Condition Refund Allowed? Why
Event not started ✅ Standard practice
Within cancellation window (e.g. 48h before) ✅ Operational fairness
Event started / attended ❌ Seat consumed
Recording already delivered ❌ Value delivered
No-show ❌ Abuse prevention
2️⃣ Refund is a request, not an action

This is important psychologically and architecturally.

Flow
User clicks “Request refund”
↓
RefundRequest created (pending)
↓
Admin / system evaluates
↓
Approved → refund processed
Rejected → enrollment stays

Why this works

slows abuse

creates audit trail

avoids chargeback chaos

gives support leverage

3️⃣ Refund states (simple & powerful)

Create a RefundRequest entity:

enum RefundStatus {
requested
approved
rejected
processed
}

model RefundRequest {
id UUID
userId UUID
enrollmentId UUID
reason String?
status RefundStatus
requestedAt DateTime
resolvedAt DateTime?
}

Do NOT auto-delete enrollments.
Refunds are historical events, not erasures.

4️⃣ What happens when a refund is approved
Courses

Enrollment → refunded

Access revoked immediately

Progress frozen (not deleted)

Certificate invalidated (if exists)

Invoice → credit note issued (ZATCA compliant)

Events

Registration → refunded

Seat released (if applicable)

Calendar access revoked

Recording access revoked

5️⃣ UX: “Allowed but not encouraged”
Where the refund CTA lives

❌ Not on course page
❌ Not on lesson page
❌ Not next to “Resume”

✅ Account → My Courses → Course → “Need help?”

This alone reduces abuse dramatically.

Copy matters (very important)

Bad:

“Refund available”

Good:

“You may request a refund if you’re eligible. Refunds are reviewed manually.”

This framing:

signals seriousness

sets expectations

discourages casual attempts

6️⃣ Technical guardrails (anti-abuse)
Hard checks in handler

progress threshold

time window

certificate existence

prior refund attempts

Soft checks (optional, later)

frequent refund flag on user

account age

payment method risk score

7️⃣ Why NOT auto-refund

Auto-refunds:

encourage content scraping

increase payment processor risk

break trust with instructors

create legal exposure

Manual or semi-automatic refunds:

are slower

feel intentional

are safer

This is especially important in Saudi / ZATCA context.

8️⃣ Events vs Courses — same concept, different knobs

The beauty of this design:

same refund engine

different eligibility rules

shared admin tooling

You can reuse:

RefundRequest

status machine

credit note logic

audit logs

9️⃣ One-sentence policy (this is gold)

Refunds are available when value has not been substantially consumed, and are subject to review.

That sentence alone protects you legally, technically, and ethically.

Final recommendation (clear & confident)

✔ Allow refunds
✔ Require eligibility
✔ Make it a request
✔ Apply friction intentionally
✔ Never erase history

This keeps:

users respected

instructors protected

platform safe

regulators happy
