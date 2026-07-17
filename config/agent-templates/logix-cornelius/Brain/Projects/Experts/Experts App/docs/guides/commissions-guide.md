---
title: "Commissions Guide"
date: "2026-04-11"
tags: ["project/experts", "topic/commissions-guide", "topic/guides"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs/guides/guides-index|Guides index]]

# Commissions Guide

Ok, now I understand.

Now, the client is asking about "course/event creator discount percentage" + "affiliate" I don't fully understand the question, but I think they want to add an option when creating/editing course/event to either promote it or not and set a percentage -> percentage for what exactly I'm not sure, but I think as a cap for what an affiliate earns!!!

Answering to client (providing a detailed affiliate system mechanism docs):
"Also, there’s a misunderstanding of how affiliating system works, you can read more about it here, as it’s explained in details. In short, we can't control what gets promoted and/or by whom simultaneously, think about it…"

Your instinct is correct: the request likely mixes two different concepts that should not be confused:

Affiliate commission rate (what an affiliate earns)

Promotional discount (price reduction for students)

If these are not clearly separated in the product design, the system becomes confusing for instructors and very difficult to manage operationally.

Below is a clear way to explain this to the client while also proposing a workable mechanism.

Clarifying the Affiliate Promotion Mechanism

There appears to be some misunderstanding about how affiliate systems operate in marketplaces.

An affiliate system does not allow the platform or instructor to directly control who promotes a course or event or when it is promoted. Affiliates independently choose what they want to promote based on incentives such as commission rates, popularity, and audience relevance.

Affiliates act as independent marketing partners who bring external traffic to the platform. They decide which courses or events to promote because they earn commission only when a sale occurs.

For this reason, the platform cannot realistically control promotion in the sense of selecting specific affiliates or guaranteeing that a particular course will be promoted.

However, what the platform can control is the incentive structure that makes a course attractive to affiliates.

What the Client Is Likely Asking For

The request for a “course/event creator discount percentage + affiliate” likely refers to allowing instructors to define a promotional setting for their course.

This setting could control either:

the maximum affiliate commission allowed for that course, or

the promotional discount available when affiliates promote it.

Both approaches are valid, but they serve different purposes.

Recommended Implementation Model

A simple and effective structure is to allow instructors to opt-in to affiliate promotion and define a maximum commission percentage.

For example, when creating or editing a course or event, the instructor could configure:

Affiliate Promotion Settings

Allow affiliates to promote this course: Yes / No

Maximum affiliate commission: e.g., 10 percent

If the instructor enables this option, affiliates are allowed to promote the course and receive commission for successful sales.

If disabled, the course simply does not participate in the affiliate program.

This mechanism does not control which affiliate promotes the course, but it defines the incentive available to them.

Why This Works

Affiliates naturally choose what to promote based on the available incentives.

Courses with:

higher commissions

higher conversion rates

better ratings

stronger demand

are more likely to be promoted by affiliates.

Therefore, the instructor’s commission setting indirectly affects promotion without requiring manual control.

Distinguishing Affiliate Commission From Discounts

It is important not to confuse affiliate commission with promotional discounts.

Affiliate commission is a marketing cost paid to the affiliate after a sale occurs.

A discount is a price reduction offered to the student.

These are two separate mechanisms and should be configured independently.

For example, a course could have:

a 10 percent affiliate commission

a 20 percent promotional discount

or neither.

Combining them incorrectly can lead to financial and accounting complications.

Example Scenario

Course price: 1,000 SAR

Instructor enables affiliate promotion with a 10 percent commission.

An affiliate promotes the course and generates a sale.

Affiliate earns:

100 SAR commission

The revenue is then processed according to the platform’s revenue split model.

If a promotional coupon is also used, the discount is applied at checkout and the commission is calculated according to the defined affiliate rule.

Suggested Configuration for Courses and Events

When creating or editing a course or event, instructors could have the following options:

Affiliate Promotion

Allow affiliate promotion: Yes / No

Affiliate commission percentage: configurable within platform limits

Promotional Discounts

Enable promotional coupon: Yes / No

Discount percentage or amount

Who funds the discount: platform or instructor

This keeps the system flexible while remaining understandable.

Key Point to Communicate to the Client

The platform cannot centrally control which affiliates promote specific courses. Affiliates independently decide what to promote based on incentives.

What the platform and instructors can control is:

whether a course participates in the affiliate program

the commission incentive offered to affiliates

whether promotional discounts are available

These parameters define the attractiveness of the course to affiliates while keeping the system scalable and transparent.

If you'd like, I can also help you add a small section to your existing document titled “Affiliate Promotion Controls for Instructors” so it fits naturally with the rest of the system documentation you already prepared.

Ahaa, now I understand, so with this, the ledger logic becomes clearer, as before affiliate commission were either funded by the platform or shared, but with above, it would be funded by instructor only if the option is enabled, right ?

Also, regarding the percentage CAP, currently the affiliate system "approval flow" admin sets commission percentage upon application approval, how might that work with what proposed, should I disable this behavior and make it as per instructor's set percentage ?

You’re very close, but there are two separate layers that should stay independent, otherwise the system will become hard to control later.

Think of affiliate commission as having two limits:

Affiliate commission rate (set by admin)

Course-level commission cap (set by instructor)

The actual commission used is simply the minimum of the two.

This keeps the system safe while giving instructors control.

1. Who Funds the Affiliate Commission?

With the new proposal (instructor enabling affiliate promotion per course), the most logical interpretation is:

Affiliate commission is funded by the instructor share.

This means:

Revenue split happens first, then affiliate commission is deducted from the instructor portion.

Example:

Course price paid: 1,000
Net ex VAT: 869.57
Gateway: 25

Distributable: 844.57

Split 70 / 30:

Instructor before affiliate:
591.20

Platform before affiliate:
253.37

Affiliate commission (10% of gross = 100):

Instructor final:

591.20 − 100 = 491.20

Platform final:

253.37

So yes — if affiliate promotion is enabled for a course, the instructor funds the commission.

If the instructor disables affiliate promotion, no affiliate commission exists for that course.

This model is clean and easy to explain to instructors:

“If affiliates promote your course, their commission comes from your share.”

1. The Commission Percentage Problem

Right now your system works like this:

Admin approves affiliate
Admin sets affiliate commission rate

Example:

Affiliate A → 10%
Affiliate B → 12%
Affiliate C → 8%

That system is still valuable and should not be removed.

Why?

Because it lets the platform:

reward top affiliates

penalize bad ones

negotiate special partnerships

control marketing costs

1. How to Combine Admin Commission + Instructor Cap

Instead of replacing the admin rate, combine them.

Define:

Affiliate rate = set by admin
Course cap = set by instructor

Actual commission used:

actualCommission = min(affiliateRate, courseCap)

Example:

Affiliate rate: 12%
Instructor cap: 8%

Actual commission = 8%

Another example:

Affiliate rate: 7%
Instructor cap: 10%

Actual commission = 7%

This protects both sides.

1. Instructor Settings for Courses

When creating or editing a course/event:

Affiliate Promotion

Enable affiliate promotion: Yes / No

Maximum commission allowed:
Example: 8%

If disabled → no affiliate commissions apply.

If enabled → affiliates may promote, but only up to that percentage.

1. Why This Model Works

This structure creates a natural market system:

Affiliates prefer promoting courses with higher caps.

Example:

Course A cap: 5%
Course B cap: 12%

Affiliates will likely promote Course B.

So instructors indirectly compete for affiliate promotion.

1. How It Affects Your Ledger

This simplifies your ledger logic.

Before you had cases like:

affiliate funded by platform

affiliate shared

affiliate platform funded

Now it becomes predictable.

Affiliate commission = instructor funded.

Ledger example:

Instructor share (before affiliate)
− affiliate commission
= instructor final

Platform share remains unchanged.

No complex funding splits required.

1. One Important Safety Rule

You should enforce a platform maximum commission.

Example:

Platform maximum affiliate commission = 15%

This prevents instructors from setting something extreme like 50%.

So final rules:

AffiliateRate ≤ PlatformMaxCommission
CourseCap ≤ PlatformMaxCommission

ActualCommission = min(AffiliateRate, CourseCap)

1. Recommended Final Structure

Affiliate application approved by admin

Admin sets base commission rate per affiliate.

Instructor chooses per-course settings:

Enable affiliate promotion: Yes / No
Maximum commission allowed.

Actual commission paid:

Minimum of the affiliate rate and the course cap.

Commission deducted from instructor share after revenue split.

Final Insight

This model creates a marketplace dynamic:

Affiliates choose which courses to promote

Instructors choose how attractive their course is to affiliates

Platform keeps overall control via admin commission rates and maximum caps

And most importantly:

Your ledger stays simple.

Split → affiliate deduction → final payout.
