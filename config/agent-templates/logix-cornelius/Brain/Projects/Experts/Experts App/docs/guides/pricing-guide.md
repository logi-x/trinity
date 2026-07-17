---
title: "Pricing Guide"
date: "2026-04-11"
tags: ["project/experts", "topic/guides", "topic/pricing-guide"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs/guides/guides-index|Guides index]]

# Pricing Guide

Publishing locks structural changes to protect learner progress and grading fairness.

why pricing is locked as well in this case, can't instructor change course/event price after publishing ?

Good question. The short answer is: pricing is usually locked after publishing to protect transactional fairness, not just course structure.

But it depends on what exactly you want to protect. Let’s break it down.

Why Pricing Is Often Locked After Publishing

When a course or event is published and enrollments begin, price changes can create fairness and accounting issues.

1. Prevents Pricing Disputes

Imagine this situation:

Student A buys course for 500 SAR

Instructor changes price to 300 SAR

Student B buys it cheaper

Student A may request a partial refund or complain about unfair pricing.

Most platforms avoid this by locking pricing once the course is live or once the first purchase happens.

1. Protects Affiliate Agreements

Your platform supports affiliate commissions.

Example:

Affiliate promotes course at 500 SAR

Commission calculated on that price

Instructor later drops price to 200 SAR

Now:

Affiliate marketing funnel breaks

Commission expectations change

Campaign analytics become invalid

Locking price protects affiliate campaigns.

1. Protects Promotional Campaigns

If the platform runs:

platform coupons

seasonal discounts

bundles

affiliate promotions

Changing the base price can distort the promotion logic.

Example:

Course price = 500 SAR
Coupon = 20%

If instructor changes base price to 700, the same coupon suddenly gives a much larger discount.

1. Accounting and VAT Consistency

You already designed a ledger pipeline.

Price changes mid-sale create accounting complexity:

multiple price tiers

VAT calculations per cohort

refund logic complexity

financial reporting inconsistencies

Keeping the base price stable simplifies the ledger.

However — Price Does NOT Need to Be Permanently Locked

Most platforms use one of these rules instead.

Rule A (Most Common)

Instructor can change price anytime, but:

change only affects future purchases

previous purchases stay unchanged

This is simple and safe.

Rule B (More Controlled)

Price can change only if no enrollments exist yet.

After first enrollment:

price locked

instructor must create new course version if needed

Rule C (Marketplace Friendly)

Price editable anytime, but with restrictions:

cooldown period (e.g., once every 7 days)

cannot change during active promotions

cannot go below platform minimum price

Recommended Policy for Experts

Given your system (affiliates, coupons, ledger, certification), the cleanest rule is:

Instructor may change price anytime

But:

Change applies only to future purchases

Cannot change price during active platform promotions

Cannot change price more than once every 7 days (optional)

Existing enrollments keep the original purchase price

This keeps:

accounting simple

instructors flexible

students protected

affiliates stable

What Actually Should Be Locked After Publishing

Instead of price, these things are usually locked:

Structural content

lesson order

grading rules

certificate requirements

Because changes there affect learner progress and fairness.

Clean Rule Summary for Documentation

Publishing locks structural changes that affect learner progress and grading fairness.

Pricing may still be adjusted by the instructor, but price changes only apply to future purchases and do not affect existing enrollments.

---

here’s a clean implementation guide for Rule A + hybrid pricing safeguards for Experts.

Goal

Allow instructors to change a published course/event price, but safely:

price change affects future purchases only

existing enrollments keep their original purchase price

optional cooldown, e.g. once every 7 days

cannot go below platform minimum, e.g. 120 SAR

optionally block changes during active promotions

This gives flexibility without breaking fairness, accounting, or promotions.

1. Core policy
   Rule A

A published course or event may change price after publishing, but the new price applies only to future purchases.

So:

Student A bought at 500 SAR → stays 500 SAR

Student B buys later after price change to 450 SAR → pays 450 SAR

No retroactive changes.

Hybrid safeguards

Add these platform rules:

instructor can change price only once every 7 days

price cannot go below 120 SAR

optional: price cannot change while an active promotion/campaign exists

optional: price cannot change if there are pending admin approvals for pricing-sensitive campaigns

1. Recommended data model

Do not overwrite price blindly on the main course/event record without history.

Use:

current published price on the course/event

separate price history table

order/enrollment stores the purchase snapshot

Course/Event

Keep the currently active price on the content record.

Example:

model Course {
id String @id @default(cuid())
title String
priceAmount Decimal @db.Decimal(10, 2)
priceCurrency String @default("SAR")
publishedAt DateTime?
lastPriceChangedAt DateTime?
pricingLockedUntil DateTime?
hasActivePromotion Boolean @default(false)

priceVersions CoursePriceVersion[]
}

You can mirror the same pattern for Event.

Price history

Track every change.

model CoursePriceVersion {
id String @id @default(cuid())
courseId String

oldPriceAmount Decimal? @db.Decimal(10, 2)
newPriceAmount Decimal @db.Decimal(10, 2)
currency String @default("SAR")

changedById String
reason String?
effectiveAt DateTime @default(now())

createdAt DateTime @default(now())

course Course @relation(fields: [courseId], references: [id], onDelete: Cascade)
}
Enrollment / order snapshot

Every purchase must store the exact price used at checkout.

model CourseEnrollment left as is

This is what protects historical fairness.

1. Business rules to enforce
   Minimum price

Platform minimum published price:

const PLATFORM_MIN_PRICE_SAR = 120;

Validation:

if (newPrice < PLATFORM_MIN_PRICE_SAR) {
throw new Error("Price cannot be lower than 120 SAR.");
}
Cooldown period

If last change was within 7 days, reject.

const PRICE_CHANGE_COOLDOWN_DAYS = 7;

Validation idea:

if (course.pricingLockedUntil && now < course.pricingLockedUntil) {
throw new Error("Price can only be changed once every 7 days.");
}
Future purchases only

Never mutate historical purchase rows.

Only update:

course.priceAmount

new CoursePriceVersion

Historical orders remain untouched.

Promotion lock

Recommended rule:

if (course.hasActivePromotion) {
throw new Error("Price cannot be changed while an active promotion is running.");
}

Better later:

check actual promotions table, not just boolean

1. Recommended API/service flow

Create one centralized service for price updates.

Example service contract
type UpdatePublishedPriceInput = {
courseId: string;
actorId: string;
newPriceAmount: number;
reason?: string;
};
Service flow
Step 1

Load course/event and ownership.

Step 2

Ensure it is published.

Step 3

Validate minimum price.

Step 4

Validate cooldown.

Step 5

Validate no active promotions.

Step 6

If unchanged, no-op.

Step 7

Store price history row.

Step 8

Update current price and next cooldown timestamp.

1. Example TypeScript service logic
   const PLATFORM_MIN_PRICE_SAR = 120;
   const PRICE_CHANGE_COOLDOWN_DAYS = 7;

function addDays(date: Date, days: number): Date {
const copy = new Date(date);
copy.setDate(copy.getDate() + days);
return copy;
}

async function updatePublishedCoursePrice(input: {
courseId: string;
actorId: string;
newPriceAmount: number;
reason?: string;
}) {
const now = new Date();

const course = await prisma.course.findUnique({
where: { id: input.courseId },
select: {
id: true,
ownerId: true,
publishedAt: true,
priceAmount: true,
priceCurrency: true,
pricingLockedUntil: true,
hasActivePromotion: true,
},
});

if (!course) {
throw new Error("Course not found.");
}

if (course.ownerId !== input.actorId) {
throw new Error("You do not have permission to update this course price.");
}

if (!course.publishedAt) {
throw new Error("Only published courses use this pricing rule.");
}

if (input.newPriceAmount < PLATFORM_MIN_PRICE_SAR) {
throw new Error("Price cannot be lower than 120 SAR.");
}

if (
course.pricingLockedUntil &&
new Date(course.pricingLockedUntil).getTime() > now.getTime()
) {
throw new Error("Price can only be changed once every 7 days.");
}

if (course.hasActivePromotion) {
throw new Error("Price cannot be changed while an active promotion is active.");
}

if (Number(course.priceAmount) === input.newPriceAmount) {
return { success: true, noChanges: true };
}

await prisma.$transaction(async (tx) => {
await tx.coursePriceVersion.create({
data: {
courseId: course.id,
oldPriceAmount: course.priceAmount,
newPriceAmount: input.newPriceAmount,
currency: course.priceCurrency,
changedById: input.actorId,
reason: input.reason ?? null,
effectiveAt: now,
},
});

    await tx.course.update({
      where: { id: course.id },
      data: {
        priceAmount: input.newPriceAmount,
        lastPriceChangedAt: now,
        pricingLockedUntil: addDays(now, PRICE_CHANGE_COOLDOWN_DAYS),
      },
    });

});

return { success: true };
} 6. UI behavior
In creator dashboard

Show current price editor, but include policy hints:

Changes apply only to future purchases

Minimum price is 120 SAR

Price may be changed once every 7 days

Price cannot be changed during active promotions

If cooldown active

Disable input and show:

You can change the price again on 22 March 2026.

If promotion active

Disable input and show:

Price changes are unavailable while this course is part of an active promotion.

1. Recommended validation messages

Use clear messages:

“Price cannot be lower than 120 SAR.”

“Published course prices can only be updated once every 7 days.”

“This price change will affect future purchases only.”

“Price cannot be changed while an active promotion is running.”

1. What happens to previous enrollments/orders?

Nothing changes.

That is the whole point of Rule A.

Every enrollment/order stores:

purchase price

currency

purchase timestamp

So:

refunds use original purchase price

invoices use original purchase price

affiliate and ledger logic remain stable per transaction

Do not try to “sync” old orders to new prices.

1. Ledger/accounting impact

This model works well with your current revenue logic.

Each transaction is calculated from its own purchase snapshot:

gross paid

VAT

gateway fee

distributable

split

affiliate

payout

So if price changes later, older ledger entries remain correct.

That is one of the biggest reasons this approach is strong.

1. Optional refinement: scheduled price changes

Not needed for v1, but later you may want:

set new price now

effective from a future date

Example use case:

Ramadan sale starts next week

event early-bird price ends in 3 days

That would use:

scheduledPriceAmount Decimal?
scheduledPriceAt DateTime?

But I would keep this out of v1.

1. Recommended v1 policy for Experts

Use this exact rule set:

Published course/event pricing

Instructors may update price after publishing

New price applies only to future purchases

Existing enrollments keep their original price

Minimum price is 120 SAR

Price can be changed once every 7 days

Price cannot be changed during active platform promotions

That is simple, fair, and implementable.

1. Suggested acceptance criteria
   Backend

cannot set price below 120 SAR

cannot change price within cooldown period

cannot change price during active promotion

every price change creates history row

historical orders remain unchanged

Frontend

shows current price

shows cooldown or lock reason

shows policy note that change affects future purchases only

shows next available edit date if locked

1. Recommended future extension

Later, you can split pricing policy by content type:

Courses

7-day cooldown

Events

maybe stricter, e.g. no change within 72 hours of event start

Because events are more time-sensitive than evergreen courses.
