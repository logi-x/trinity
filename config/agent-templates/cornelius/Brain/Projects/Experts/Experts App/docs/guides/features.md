---
title: "🎯 Experts Platform – Features & Reference Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/features"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🎯 Experts Platform – Features & Reference Guide

Staging Environment (<ins>**investor-presentable**</ins> with Mock Data): <https://app.stg.experts.com.sa/>

> [!NOTE]
> Staging uses mock data and is intended for product walkthroughs only.

---

## 🔐 Test Accounts

| Email                   | Password    |
| ----------------------- | ----------- |
| `a********gi@gmail.com` | `*********` |
| `e*****id@gmail.com`    | `*********` |

---

## 📋 Terminology Reference

### Content Types & Invoice Types

| Content Type | Invoice Type   |
| ------------ | -------------- |
| Course       | `service`      |
| Event        | `service`      |
| Subscription | `subscription` |

### Action Terminology

| Content Type | User Action  |
| ------------ | ------------ |
| Course       | Enrollment   |
| Event        | Registration |

### Color Theming

| Content Type | Color  | Hex Code  |
| ------------ | ------ | --------- |
| 🔵 Course    | Blue   | `#3b9df6` |
| 🟠 Event     | Amber  | `#fe9a00` |
| 🟣 Post      | Violet | `#8e51ff` |

---

## 💳 Test Payment Credentials

> [!TIP]
> Use the test card below for demo payments in staging.

| Field       | Value                 |
| ----------- | --------------------- |
| Card Number | `4242 4242 4242 4242` |
| CVV         | `123`                 |
| Expiry      | `01/28`               |

---

## ✨ Platform Features

### 🌐 Community & Social

| Feature                      | Description                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------------- |
| **Global Social Reactions**  | Like, comment, share functionality                                                    |
| **Comments Internal Embeds** | Copy/share course/event/post and embed as comment                                     |
| **Comments @mentions**       | Tag users in comments                                                                 |
| **Global Search**            | `⌘K` / `Ctrl+K` – Search courses, lessons, events, posts, comments, @users, #hashtags |
| **Presence Channels**        | Real-time online users indicator                                                      |

---

### 👤 User Features

| Feature                       | Description                                      |
| ----------------------------- | ------------------------------------------------ |
| **Activity Tracker/Timeline** | User activity history + progress tracking        |
| **Verified Status**           | User verification badge system                   |
| **Bio**                       | Short description (160 chars max)                |
| **About Section**             | Resume with Markdown support                     |
| **Follow System**             | Following/Followers with Follow/Unfollow actions |
| **Social Links**              | External profile links                           |
| **User Content**              | View Courses/Events per @user                    |
| **Reviews**                   | User's own ratings                               |
| **Bookmarks**                 | Save content for later                           |

---

### 📅 Events

| Feature              | Description                                          |
| -------------------- | ---------------------------------------------------- |
| **Speakers Support** | Main Host + Speakers (host, co-host, speaker, guest) |
| **Revenue Share**    | Percentage-based revenue sharing system              |
| **Event Modes**      | Online (Meeting URL) / In-Person (Location Map Pin)  |
| **Pricing**          | Paid/Free event options                              |
| **Hashtags**         | Searchable #hashtags support                         |
| **Date Flexibility** | Single/Multi/Recurring dates support                 |
| **Event Visibility** | Past & Upcoming events all visible                   |
| **Description**      | Detailed description with Markdown support           |
| **Agenda**           | Detailed agenda with speaker, topic, time            |
| **Metrics**          | Views/Ratings counters                               |

**Status:** MVP ready (CRUD in progress)

#### 🚧 Pending (Events)

- **[^P1] Full CRUD UI** for creators (create/edit/delete, drafts, publishing lifecycle)
- **[^P1] Occurrences editor** (date rules + timezones, multi/recurring validation)
- **[^P1] Registration management** (attendees list, capacity edits, cancellations)
- **[^P1] Host/speaker management** in the creator flow (roles + revenue share UI)
- **[^P2] Event assets** (thumbnail/cover, agenda polish, validation)
- **[^P2] Content uploads** (event assets, media)

#### 📌 Unified Event Types

```
lecture | webinar | workshop | research | conference
training | seminar | symposium | hackathon | other
```

---

### 📚 Courses

| Feature               | Description                                    |
| --------------------- | ---------------------------------------------- |
| **Multi Instructors** | Collaboration support for multiple instructors |
| **Pricing**           | Paid/Free course options                       |
| **Metrics**           | Views/Ratings counters                         |
| **Hashtags**          | Searchable #hashtags support                   |
| **Certificates**      | Course completion certificate system           |

**Status:** MVP ready (CRUD in progress)

#### 🚧 Pending (Courses)

- **[^P1] Full CRUD UI** for creators (create/edit/delete, drafts, publishing lifecycle)
- **[^P1] Module/lesson builder** (ordering, visibility, lock/preview rules)
- **[^P1] Enrollment rules** (free/paid, prerequisites, access checks)
- **[^P1] Progress tracking + resume** per lesson
- **[^P1] Assessment/quiz hooks** (if required for completion)
- **[^P2] Content uploads** (course thumbnails, lesson media, large files/video storage)

---

### 🎬 Creator Studio

A comprehensive dashboard for content creators:

- 📊 **Overview & Stats** – Platform performance at a glance
- 📖 **Course Management** – Publish and manage courses
- 📅 **Event Management** – Publish and manage events
- 📈 **Analytics** – Performance metrics, revenue tracking

**Status:** Partially complete (Courses/Events CRUD wired, analytics + insights pending)

#### 🚧 Pending (Creator Studio)

- **[^P1] Dashboard insights** still rely on mock activity/reviews/quick actions
- **[^P1] Analytics** data sources are minimal (needs dedicated creator analytics APIs)
- **[^P2] Event creation flow** has multiple legacy variants (needs consolidation)
- **[^P2] Scheduling UI** still missing some single‑schedule enhancements

---

### 🔑 Authentication

| Feature            | Description                                               |
| ------------------ | --------------------------------------------------------- |
| **Social Logins**  | Login/Register via social providers                       |
| **Multi Profiles** | Multiple profiles per account _(not fully supported yet)_ |

**Status:** Core login/registration ready (password reset + email verification pending)

#### 🚧 Pending (Authentication)

- **[^P1] Password reset emails** (API + token flow)
- **[^P1] Email verification / OTP flow** (API + enforcement)
- **[^P2] Account linking UX** (beyond API readiness)

---

## ✉️ Emailing System

| Feature              | Description                                     |
| -------------------- | ----------------------------------------------- |
| **Provider**         | Mailtrap integration (via `lib/mail`)           |
| **Support Requests** | Support email template + internal send endpoint |

**Status:** Support email ready (transactional emails pending)

#### 🚧 Pending (Emailing)

- **[^P1] Transactional email templates** (reset password, verification, receipts)
- **[^P1] Outbound email API routing** (environment-based provider switching)
- **[^P2] Email delivery audit/logs** (basic observability + retries)

---

## 💰 Monetization

### 🤝 Affiliate System

**Core Features:**

- ✅ Accurate tracking and commission system
- 🛡️ **Revenue Leakage Protection** – Affiliates only receive commission from first occurrence (guards against lifetime recurring subscription leakage)
- 🔗 Referral Links with Analytics
- 💵 Commissions & Payout management
- 📊 Admin Management System – Analytics, approvals, payouts, commission rates per affiliate

**Status:** Core tracking + admin workflows ready (payout automation pending)

#### 🚧 Pending (Affiliate)

- **[^P1] Automated payout execution** (currently admin marks payouts manually)
- **[^P1] Payout method validation** (bank details/PayPal/Stripe verification)
- **[^P2] Notification hooks** for payout status changes (affiliate + admin)

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

### 📋 Plans & Subscriptions

| Feature               | Description                           |
| --------------------- | ------------------------------------- |
| **Plan Limits**       | Enforcement of plan restrictions      |
| **Recurring Billing** | Automatic processing (monthly/yearly) |

**Status:** Core flows ready (renewals + downgrade/upgrade UX pending)

#### 🚧 Pending (Plans & Subscriptions)

- **[^P1] Automated renewals** per gateway (recurring billing lifecycle)
- **[^P1] Upgrade/downgrade UX polish** (billing proration + messaging)
- **[^P2] Production Stripe (KSA)** readiness

---

### 💳 Payment Gateways

| Gateway         | Status                                                               |
| --------------- | -------------------------------------------------------------------- |
| **Noon**        | ✅ Active                                                            |
| **Tabby**       | ✅ Active                                                            |
| **Stripe**      | 🧪 Testing only (not supported in SA yet, not for production in KSA) |
| _More gateways_ | 🔌 Extendable architecture                                           |

**Status:** Noon/Tabby live, Stripe testing only

> [!WARNING]
> Stripe is for testing only and not approved for production in KSA.

#### 🚧 Pending (Payment Gateways)

- **[^P1] Unified refund/cancel flows** across providers
- **[^P2] Additional gateways** (as needed)

---

### ⚖️ Legal & Compliance

| Feature                     | Description                                                               |
| --------------------------- | ------------------------------------------------------------------------- |
| **ZATCA Compliance**        | Fully compliant with Saudi tax authority                                  |
| **Multi Business Entities** | Registered entities can issue invoices, process payments, report to ZATCA |

**Status:** ZATCA pipeline ready, multi‑entity supported

#### 🚧 Pending (Legal & Compliance)

- **[^P1] Multi‑entity routing UI** (admin configuration)
- **[^P1] Operational monitoring** for failures/retries

---

### 🧾 Invoicing

| Feature              | Description                                                                |
| -------------------- | -------------------------------------------------------------------------- |
| **Branded Invoices** | Multi-entity support with custom logo, primary color, Arabic/English fonts |
| **Auto Sequencing**  | Invoice numbers: `INV-2026-000001` / Credit notes: `CRN-2026-000001`       |

**Status:** PDF invoices + ZATCA reporting ready

#### 🚧 Pending (Invoicing)

- **[^P1] Invoice emailing** (automated delivery)
- **[^P2] Bulk export/download** tools
- **[^P2] Template QA** (localization + edge cases)

---

## 🗄️ Storage

| Feature          | Description                               |
| ---------------- | ----------------------------------------- |
| **Cloud CDN**    | Content Delivery Network buckets          |
| **Availability** | Long-lived storage with high availability |
| **Invoices**     | Private R2 storage for PDF invoices       |

**Status:** Invoice storage ready

#### 🚧 Pending (Storage)

- **[^P1] Course/event media uploads** (large files, streaming assets)
- **[^P2] CDN optimization** rules per asset type

---

## 🌍 Global Platform Features

### Core Functionality

| Feature                 | Description                                                         |
| ----------------------- | ------------------------------------------------------------------- |
| **Views Counters**      | Accurate tracking for all content types (once per user per content) |
| **Rating System**       | Comprehensive ratings across the platform                           |
| **Sign In to ...**      | Guest action/content protected                                      |
| **SEO Optimized**       | Full SEO search engines optimization                                |
| **Access Restrictions** | Role-based access level enforcement                                 |
| **Markdown Support**    | Global Markdown rendering                                           |
| **Skeleton Loading**    | Unified loading states                                              |
| **RTL Support**         | Full Right-to-Left support for Arabic                               |
| **Theming**             | Consistent Dark/Light theme                                         |
| **Filtering System**    | Comprehensive unified filters across the app                        |
| **Categories**          | Fixed unified category system                                       |
| **Notifications**       | In-app notifications (@mentions, follows, comments, etc.)           |
| **Live Updates**        | Real-time content updates without page refresh                      |

### Naming Conventions

| Action                            | Content Type    |
| --------------------------------- | --------------- |
| **Register**                      | Event           |
| **Enroll**                        | Course          |
| **Instructor(s)**                 | Course creators |
| **Host/Speaker(s)**               | Event creators  |
| **Instructor(s)/Host/Speaker(s)** | creator         |

### Themed Accents

| Content    | Theme  | Applied To                |
| ---------- | ------ | ------------------------- |
| 🔵 Courses | Blue   | Shadows, buttons, borders |
| 🟠 Events  | Amber  | Shadows, buttons, borders |
| 🟣 Posts   | Violet | Shadows, buttons, borders |

---

## 🖼️ Default Illustrations

### Avatar Defaults

| Type       | URL                                                                                                                        |
| ---------- | -------------------------------------------------------------------------------------------------------------------------- |
| User       | [https://cdn.experts.com.sa/s/avatars/user/default.png](https://cdn.experts.com.sa/s/avatars/user/default.png)             |
| Post       | [https://cdn.experts.com.sa/s/avatars/post/default.png](https://cdn.experts.com.sa/s/avatars/post/default.png)             |
| Comment    | [https://cdn.experts.com.sa/s/avatars/comment/default.png](https://cdn.experts.com.sa/s/avatars/comment/default.png)       |
| Course     | [https://cdn.experts.com.sa/s/avatars/course/default.png](https://cdn.experts.com.sa/s/avatars/course/default.png)         |
| Event      | [https://cdn.experts.com.sa/s/avatars/event/default.png](https://cdn.experts.com.sa/s/avatars/event/default.png)           |
| Instructor | [https://cdn.experts.com.sa/s/avatars/instructor/default.png](https://cdn.experts.com.sa/s/avatars/instructor/default.png) |
| AI         | [https://cdn.experts.com.sa/s/avatars/ai/default.png](https://cdn.experts.com.sa/s/avatars/ai/default.png)                 |

### Error Pages

| Error                 | URL                                                                                    |
| --------------------- | -------------------------------------------------------------------------------------- |
| 404 Not Found         | [https://cdn.experts.com.sa/images/404.png](https://cdn.experts.com.sa/images/404.png) |
| 403 Forbidden         | [https://cdn.experts.com.sa/images/403.png](https://cdn.experts.com.sa/images/403.png) |
| 500 Server Error      | [https://cdn.experts.com.sa/images/500.png](https://cdn.experts.com.sa/images/500.png) |
| 429 Too Many Requests | [https://cdn.experts.com.sa/images/429.png](https://cdn.experts.com.sa/images/429.png) |

---

## 💓 System Heartbeat

### Diagnostics Stream

Real-time visibility into platform events, warnings, and failures with filterable feed.

> [!IMPORTANT]
> Diagnostics stream is internal/admin only.

**Tracked Events:**

- Gateway Payment Captured
- Event/Course Invoice Created
- User Account Created
- And more...

### Example Payload

```json
{
  "type": "REGISTRATION",
  "level": "INFO",
  "timestamp": "2026-01-03T10:27:25.268Z",
  "event": "user.registration.created",
  "payload": {
    "email": "ahmed@logi-x.org",
    "userId": "0d36c184-9242-40fa-b665-283fbb977ff4",
    "fullName": "Logix Inc.",
    "provider": "github",
    "providerAccountId": "185935600"
  }
}
```

---

## 📝 TODOs

- [ ] Finish coupon system globally (per affiliate/creator)
- [ ] Complete Events CRUD + publishing flow
- [ ] Complete Courses CRUD + module/lesson builder
- [ ] Learner enrollment UX (Start → Progress → Certificate)
- [ ] _Additional items to be added_

---

## ⏱️ Estimated Completion (Events/Courses + Enrollment UX)

**Estimates below focus on pending Events + Courses only.** The rest of the platform remains as documented.

| Area                                               | Estimate               | Notes                                                                                         |
| -------------------------------------------------- | ---------------------- | --------------------------------------------------------------------------------------------- |
| **Events CRUD[^1]**                                | **5–7 working days**   | Builder UI, occurrences editor, host management, validation, publish workflow                 |
| **Courses CRUD**                                   | **7–10 working days**  | Module/lesson builder, visibility rules, basic assessments                                    |
| **Enrollment UX (Start → Progress → Certificate)** | **10–14 working days** | Most complex area: player UX, progress state, resuming, completion logic, certificate trigger |

**Most complex portion:** Course enrollment UX (learner flow) because it spans player state, progress persistence, completion rules, quiz gating, and certificate issuance.

### ✅ Assumptions

- Existing backend flows (payments, subscriptions, ZATCA, storage) remain unchanged.
- No new payment gateway integrations required for this scope.
- Design system and UI patterns are reused (no new redesigns).

### 🔗 Dependencies

- **Lesson player** exists but needs hardening (content delivery, error states, UX polish).
- **Progress tracking** exists (lesson completion + resume), but needs validation and edge‑case coverage.
- **Certificates** API exists; certificate template + issuance rules still need final alignment.

[^1]: Create, Read, Update, Delete operations

[^P1]: High Priority

[^P2]: Low Priority
