---
title: "affiliate"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/affiliate"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  1️⃣ High-level “correct” affiliate flow (mental model)

Think in 4 phases, each with clear ownership:

Attribution (click → identity)

Conversion (identity → revenue)

Commission lifecycle (revenue → payable)

Payout lifecycle (payable → paid)

Your schema mostly covers (2–4).
The biggest gaps are in (1) attribution and edge-rules in (3).

2️⃣ Phase 1 — Attribution (THIS is what feels missing)
What you have

ref code in URL

Referral row with IP, UA, expiresAt

30-day cookie logic implied

What’s missing conceptually

You’re mixing attribution and conversion too early.

Right now:

Referral = click + maybe user

Status jumps from pending → registered → converted

In reality, you want two layers:

✅ Missing concept: AffiliateClick (or AttributionSession)

Why?

You need last-click wins

You need multiple visits before signup

You need to handle anonymous → logged-in linking

You need to defend against fraud

Recommended addition (lightweight)
model AffiliateClick {
id String @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
affiliateId String @db.Uuid
referralCode String @db.VarChar(20)
ipAddress String?
userAgent String?
landingPage String?
utmSource String?
utmMedium String?
utmCampaign String?
createdAt DateTime @default(now()) @db.Timestamptz
expiresAt DateTime

referralId String? @db.Uuid
}

Flow

Every visit with ref= creates a click

Cookie stores click_id

Signup links click → referral

Purchase links click → referral → commission

This solves:

Overwriting referrals

Multi-tab / multi-device

Last-click attribution

Auditing disputes

This is likely the “missing piece” you’re feeling.

3️⃣ Phase 2 — Referral lifecycle (small tweak)

Your Referral model is good, but rename status semantics:

Current
pending → registered → converted → expired

Cleaner semantics
pending // click happened
registered // user created account
qualified // eligible (passed fraud + refund window)
converted // commission generated
expired

Why?

Conversion ≠ payable

Refund window matters (especially for courses/events)

Add:

qualifiedAt DateTime?

4️⃣ Phase 3 — Commission lifecycle (important rules missing)

Your Commission table is solid, but rules are implicit instead of explicit.

What’s missing
A) Holding / cooling period

You need to delay approval until:

Refund window passes

Payment is captured

Fraud checks pass

Add:

holdUntil DateTime?

Then your states become meaningful:

pending → approved → paid
↘ cancelled

B) Snapshot commission rate (good job!)

You already store:

commissionRate

commissionAmount

✅ This is correct and important.

C) Attribution type (optional but powerful)
attributionType String // first_click | last_click | manual

5️⃣ Phase 4 — Payouts (almost perfect)

Your AffiliatePayout model is excellent.

Two minor improvements:

A) Add payout period
periodStart DateTime
periodEnd DateTime

B) Immutable snapshot

Never recalc payout totals dynamically.

6️⃣ UTM + Affiliate coexistence (you did this right)

This part is correct and should not change:

Non-affiliate marketing → UTMs only

Affiliate → UTMs + ref

Just make one rule explicit:

Affiliate ref always overrides UTM attribution

That prevents double counting.

7️⃣ What I’d NOT change (you did these right)

✅ Separate schemas (billing)
✅ Snapshot monetary values
✅ Separate commissions from payouts
✅ Status fields instead of booleans
✅ Nullable referredUserId
✅ Indexing strategy

8️⃣ The “golden” end-to-end flow (TL;DR)

Visitor clicks ?ref=ADNANI2025

Create AffiliateClick

Store click_id cookie (30 days)

User signs up → create Referral

User purchases → create Commission (pending)

After refund window → approve commission

Monthly job → create AffiliatePayout

Mark commissions as paid

9️⃣ Final verdict

Your schema is 80–85% there.
The missing feeling comes from:

❌ No explicit click / attribution entity

❌ Conversion vs eligibility not clearly separated

❌ No cooling-off logic baked into the data model

Add one small table + one date field, and this becomes a very serious, scalable affiliate system.
