---
title: "Affiliate System"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "topic/affiliate-system", "affiliate"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Affiliate System.md"
---

# Affiliate System

Affiliate and referral mechanics inside the Experts billing model: attribution, commission calculation, and how affiliate payouts interact with instructor revenue share.

## Context in Experts

The affiliate system is part of the broader commerce stack for Experts. It sits next to coupons, subscriptions, instructor payouts, and payment gateways rather than existing as a standalone marketing feature.

## What it touches

- Payment initiation and invoice creation
- Coupon and referral attribution
- Commission calculations during billing
- Payout reporting for instructors and affiliates

## Why it matters

Ahmed's project notes describe Experts as using a flexible pricing and commission engine that supports both affiliates and instructors. That makes affiliate logic a billing concern first and a growth feature second.

## Typical rules

- Attribution needs to be captured before payment confirmation
- Commission logic must stay auditable alongside invoices and payouts
- Affiliate incentives should not bypass instructor payout rules or refund rules

## Related

- [[Wiki/Concepts/Payments]]
- [[Wiki/Concepts/Processing Fees]]

