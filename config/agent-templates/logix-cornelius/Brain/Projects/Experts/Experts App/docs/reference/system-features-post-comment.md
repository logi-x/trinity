---
title: "system features post comment"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/system-features-post-comment"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

### ✨ Platform Features

Some hidden (powerful) features

---

#### 🌐 Community & Social

Sharable filters

- Courses Example [https://app.stg.experts.com.sa/courses?search=Full](https://app.stg.experts.com.sa/courses?search=Full)
- Events Example [https://app.stg.experts.com.sa/events?search=div](https://app.stg.experts.com.sa/events?search=div)

It can also work affiliate reference links

> e.g. <https://app.stg.experts.com.sa/events?search=div&ref=AHMED2024&utm_medium=social&utm_campaign=event-share>

any user enrolls in a course, registers for an event, or subscribe in a plan using an affiliate link with `?ref=<affiliate_code>` "affiliate" will get a commission, more on that below...

#### Other social features

| Feature                      | Description                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------------- |
| **Global Social Reactions**  | Like, comment, share functionality                                                    |
| **Comments Internal Embeds** | Copy/share course/event/post and embed as comment                                     |
| **Comments @mentions**       | Tag users in comments                                                                 |
| **Global Search**            | `⌘K` / `Ctrl+K` – Search courses, lessons, events, posts, comments, @users, #hashtags |

---

#### 🤝 Affiliate System

**Core Features:**

- ✅ Accurate tracking and commission system
- 🛡️ **Revenue Leakage Protection** – Affiliates only receive commission from first occurrence (guards against lifetime recurring subscription leakage)
- 🔗 Referral Links with Analytics
- 💵 Commissions & Payout management
- 📊 Admin Management System – Analytics, approvals, payouts, commission rates per affiliate

**Affiliate Flow:**

```
1. User applies for affiliate program
2. Admin approval required
3. Unique shareable URL generated e.g. https://app.stg.experts.com.sa/events?ref=AHMED2024
4. User subscribes/registers/enrolls via affiliate link
5. Affiliate receives commission based on approved rate
6. Payout available when 100 SAR threshold reached
```

**Example Calculation:**

| Item               | Value      |
| ------------------ | ---------- |
| Course Price       | 1,499 SAR  |
| Commission Rate    | 15%        |
| Affiliate Earnings | 224.85 SAR |

---

#### 🔗 Important missing routes (admin/developer)

| Route                                                                | Description           | Status                |
| -------------------------------------------------------------------- | --------------------- | --------------------- |
| [/admin](https://app.stg.experts.com.sa/admin)                       | Admin dashboard       | Partially implemented |
| [/admin/users](https://app.stg.experts.com.sa/admin/users)           | Users management      | Not implemented       |
| [/admin/courses](https://app.stg.experts.com.sa/admin/courses)       | Courses management    | Not implemented       |
| [/admin/events](https://app.stg.experts.com.sa/admin/events)         | Events management     | Not implemented       |
| [/admin/posts](https://app.stg.experts.com.sa/admin/posts)           | Posts management      | Not implemented       |
| [/admin/comments](https://app.stg.experts.com.sa/admin/comments)     | Comments management   | Not implemented       |
| [/admin/settings](https://app.stg.experts.com.sa/admin/settings)     | Settings management   | Not implemented       |
| [/admin/affiliates](https://app.stg.experts.com.sa/admin/affiliates) | Affiliates management | Partially implemented |
| [/console](https://app.stg.experts.com.sa/console)                   | Diagnostics Stream    | Fully implemented     |
| [/console/status](https://app.stg.experts.com.sa/console/status)     | System Status         | Fully implemented     |

---

#### 📊 Under the hood

The system is built using TDD (Test Driven Development) approach. Where we write the tests first and then write the code to pass the tests. This approach helps us to build a robust and reliable system.

**What do we test, and how to decide what to test?**

- core functionality of the system.
- happy path and the edge cases.
- error cases.
- performance of the system.
- security of the system.
- scalability of the system.
- reliability of the system.
- usability of the system.

There are 3 types of tests:

- unit tests
- integration tests
- end to end tests

Edge case examples:

- User tries to enroll in a course with an invalid coupon code.
- User tries to enroll in a course with a valid coupon code but the coupon is expired.
- User tries to enroll in a course with a valid coupon code but the coupon is not valid for the course.
- User tries to enroll in a course with a valid coupon code but the coupon is not valid for the user.
- How the system handles payment errors.
- Etc...

A snippet result of a all tests:

```sh
 Test Files  51 passed (51)
      Tests  264 passed (264)
   Start at  02:45:35
   Duration  27.88s (transform 2.39s, setup 820ms, import 3.98s, tests 18.34s, environment 4ms)
```

[Full Suite Tests](https://gist.github.com/logix-inc/6f35809b47174c51f619592a90d6de47?permalink_comment_id=5946175#gistcomment-5946175) can be found here
