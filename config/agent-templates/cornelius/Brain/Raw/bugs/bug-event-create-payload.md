---
title: "I'll be trying to fix all issues to prepare it for production"
status: open
resolution: unknown
tags: [bug, project/experts]
---

I'll be trying to fix all issues to prepare it for production

## Event Create Payload

```json
// payload for event create
{
  "title": "Solar Test 2",
  "description": "Solar Test 2",
  "content": "Solar Test 2 Solar Test 2",
  "categoryId": "e9ca6bfa-42b2-4b5d-9b08-8b3f0eed92bf",
  "thumbnailUrl": "https://cdn.experts.com.sa/assets/events/13f5b0b2-faf7-48ad-88e8-8d654090e95d/422da3df-e117-4bb8-ac2e-f4800b2f323e.png",
  "galleryImageUrls": [],
  "eventType": "workshop",
  "locationType": "in-person",
  "locationDetails": {
    "name": "7298 Sulaiman Al Ghunaim",
    "description": "",
    "address": "7298 Sulaiman Al Ghunaim, An Nahdah, Riyadh 13222, Saudi Arabia",
    "placeId": "Ei03Mjk4IFN1bGFpbWFuIEFsIEdodW5haW0sIFJpeWFkaCBTYXVkaSBBcmFiaWEiMRIvChQKEgm7wTt5fwAvPhG0gqhlg2gnVxCCOSoUChIJi053R38ALz4RsMGXC_T5Pm0",
    "state": "Riyadh Province",
    "postalCode": "13222",
    "city": "An Nahdah",
    "country": "Saudi Arabia",
    "latitude": 24.7621576,
    "longitude": 46.8249308
  },
  "meetingUrl": null,
  "price": 0,
  "isFree": true,
  "affiliatePromotionEnabled": false,
  "affiliateCommissionCap": null,
  "couponEnabled": false,
  "couponCode": null,
  "couponDiscountType": null,
  "couponDiscountValue": null,
  "maxAttendees": 2,
  "schedule": {
    "type": "single",
    "single": {
      "date": "2026-05-10",
      "startTime": "10:00",
      "endTime": "11:00"
    }
  },
  "agenda": [],
  "hosts": [
    {
      "userId": "ff4b3a65-1d6b-4e81-94fd-899fb9a9f961",
      "role": "guest"
    }
  ],
  "speakers": [],
  "requirements": [],
  "learnings": ["Solar Test 2", "Solar Test 3", "Solar Test 4"],
  "timezone": "Asia/Riyadh",
  "id": "13f5b0b2-faf7-48ad-88e8-8d654090e95d",
  "publishing": {
    "status": "published"
  }
}
```

## Event Create Preview (browser networks tab)

```json
// response for event create
POST http://localhost:3025/api/v1/events
Content-Type: application/json
Request URL
http://localhost:3025/api/v1/events
Request Method
POST
Status Code
201 Created
Remote Address
127.0.0.1:3025
Referrer Policy
strict-origin-when-cross-origin

{
    "id": "13f5b0b2-faf7-48ad-88e8-8d654090e95d",
    "processingEntityId": "2d5b8f2a-0d8e-4d2c-9d8b-6c7f3b1f1a10",
    "categoryId": "e9ca6bfa-42b2-4b5d-9b08-8b3f0eed92bf",
    "title": "Solar Test 2",
    "description": "Solar Test 2",
    "content": "Solar Test 2 Solar Test 2",
    "thumbnailUrl": "https://cdn.experts.com.sa/assets/events/13f5b0b2-faf7-48ad-88e8-8d654090e95d/422da3df-e117-4bb8-ac2e-f4800b2f323e.png",
    "galleryImageUrls": [],
    "eventType": "workshop",
    "schedule": {
        "type": "single",
        "dates": [
            "2026-05-09T21:00:00.000Z"
        ],
        "daysOfWeek": [],
        "endDate": null
    },
    "occurrences": [
        {
            "id": "b088eca7-af89-4510-8de5-00f6a668b763",
            "startsAt": "2026-05-10T07:00:00.000Z",
            "endsAt": "2026-05-10T08:00:00.000Z",
            "timezone": "Asia/Riyadh",
            "capacity": null,
            "isCancelled": false
        }
    ],
    "timezone": "Asia/Riyadh",
    "locationType": "in-person",
    "locationDetails": {
        "name": "7298 Sulaiman Al Ghunaim",
        "description": "",
        "address": "7298 Sulaiman Al Ghunaim, An Nahdah, Riyadh 13222, Saudi Arabia",
        "placeId": "Ei03Mjk4IFN1bGFpbWFuIEFsIEdodW5haW0sIFJpeWFkaCBTYXVkaSBBcmFiaWEiMRIvChQKEgm7wTt5fwAvPhG0gqhlg2gnVxCCOSoUChIJi053R38ALz4RsMGXC_T5Pm0",
        "state": "Riyadh Province",
        "postalCode": "13222",
        "city": "An Nahdah",
        "country": "Saudi Arabia",
        "latitude": 24.7621576,
        "longitude": 46.8249308
    },
    "meetingUrl": null,
    "price": 0,
    "isFree": true,
    "isFeatured": false,
    "learningOutcomes": [
        "Solar Test 2",
        "Solar Test 3",
        "Solar Test 4"
    ],
    "requirements": null,
    "tags": [],
    "affiliatePromotionEnabled": false,
    "affiliateCommissionCap": null,
    "couponEnabled": false,
    "couponCode": null,
    "couponDiscountType": null,
    "couponDiscountValue": null,
    "publishedAt": "2026-05-09T11:53:39.660Z",
    "lastPriceChangedAt": null,
    "pricingLockedUntil": null,
    "hasActivePromotion": false,
    "maxAttendees": 2,
    "publishingStatus": "published",
    "category": {
        "id": "e9ca6bfa-42b2-4b5d-9b08-8b3f0eed92bf",
        "slug": "science-engineering",
        "name": "Science & Engineering",
        "description": "Physical sciences, engineering, and scientific research"
    },
    "hosts": [
        {
            "userId": "ff4b3a65-1d6b-4e81-94fd-899fb9a9f961",
            "role": "guest",
            "revenueShare": null,
            "isVisible": true,
            "user": {
                "id": "ff4b3a65-1d6b-4e81-94fd-899fb9a9f961",
                "email": "egrzahid@gmail.com",
                "username": "egrzahid",
                "isVerified": true,
                "status": "active",
                "deactivationReason": null,
                "profile": {
                    "fullName": "Ahmad Zahid",
                    "avatarUrl": "https://cdn.experts.com.sa/s/avatars/user/default.png",
                    "bio": "Engineer & Entrepreneur, co-founder and CFO of Experts LMS.",
                    "dateOfBirth": null
                },
                "createdAt": null,
                "updatedAt": null
            }
        }
    ],
    "agenda": [],
    "speakers": [],
    "registrationsCount": 0,
    "paidRegistrationCount": 0,
    "pendingRegistrationCount": 0,
    "refundedRegistrationCount": 0,
    "netRevenueTotal": 0,
    "grossRevenueTotal": 0,
    "refundedRevenueTotal": 0,
    "likesCount": 0,
    "isLiked": false,
    "ratingCount": 0,
    "averageRating": 0,
    "viewCount": 0,
    "shareCount": 0,
    "bookmarkCount": 0,
    "isRegistered": false,
    "createdAt": "2026-05-09T11:53:39.660Z",
    "updatedAt": "2026-05-09T11:53:39.660Z"
}
```

## Event Create Response (browser networks tab)

```json
{
  "id": "13f5b0b2-faf7-48ad-88e8-8d654090e95d",
  "processingEntityId": "2d5b8f2a-0d8e-4d2c-9d8b-6c7f3b1f1a10",
  "categoryId": "e9ca6bfa-42b2-4b5d-9b08-8b3f0eed92bf",
  "title": "Solar Test 2",
  "description": "Solar Test 2",
  "content": "Solar Test 2 Solar Test 2",
  "thumbnailUrl": "https://cdn.experts.com.sa/assets/events/13f5b0b2-faf7-48ad-88e8-8d654090e95d/422da3df-e117-4bb8-ac2e-f4800b2f323e.png",
  "galleryImageUrls": [],
  "eventType": "workshop",
  "schedule": {
    "type": "single",
    "dates": ["2026-05-09T21:00:00.000Z"],
    "daysOfWeek": [],
    "endDate": null
  },
  "occurrences": [
    {
      "id": "b088eca7-af89-4510-8de5-00f6a668b763",
      "startsAt": "2026-05-10T07:00:00.000Z",
      "endsAt": "2026-05-10T08:00:00.000Z",
      "timezone": "Asia/Riyadh",
      "capacity": null,
      "isCancelled": false
    }
  ],
  "timezone": "Asia/Riyadh",
  "locationType": "in-person",
  "locationDetails": {
    "name": "7298 Sulaiman Al Ghunaim",
    "description": "",
    "address": "7298 Sulaiman Al Ghunaim, An Nahdah, Riyadh 13222, Saudi Arabia",
    "placeId": "Ei03Mjk4IFN1bGFpbWFuIEFsIEdodW5haW0sIFJpeWFkaCBTYXVkaSBBcmFiaWEiMRIvChQKEgm7wTt5fwAvPhG0gqhlg2gnVxCCOSoUChIJi053R38ALz4RsMGXC_T5Pm0",
    "state": "Riyadh Province",
    "postalCode": "13222",
    "city": "An Nahdah",
    "country": "Saudi Arabia",
    "latitude": 24.7621576,
    "longitude": 46.8249308
  },
  "meetingUrl": null,
  "price": 0,
  "isFree": true,
  "isFeatured": false,
  "learningOutcomes": ["Solar Test 2", "Solar Test 3", "Solar Test 4"],
  "requirements": null,
  "tags": [],
  "affiliatePromotionEnabled": false,
  "affiliateCommissionCap": null,
  "couponEnabled": false,
  "couponCode": null,
  "couponDiscountType": null,
  "couponDiscountValue": null,
  "publishedAt": "2026-05-09T11:53:39.660Z",
  "lastPriceChangedAt": null,
  "pricingLockedUntil": null,
  "hasActivePromotion": false,
  "maxAttendees": 2,
  "publishingStatus": "published",
  "category": {
    "id": "e9ca6bfa-42b2-4b5d-9b08-8b3f0eed92bf",
    "slug": "science-engineering",
    "name": "Science & Engineering",
    "description": "Physical sciences, engineering, and scientific research"
  },
  "hosts": [
    {
      "userId": "ff4b3a65-1d6b-4e81-94fd-899fb9a9f961",
      "role": "guest",
      "revenueShare": null,
      "isVisible": true,
      "user": {
        "id": "ff4b3a65-1d6b-4e81-94fd-899fb9a9f961",
        "email": "egrzahid@gmail.com",
        "username": "egrzahid",
        "isVerified": true,
        "status": "active",
        "deactivationReason": null,
        "profile": {
          "fullName": "Ahmad Zahid",
          "avatarUrl": "https://cdn.experts.com.sa/s/avatars/user/default.png",
          "bio": "Engineer & Entrepreneur, co-founder and CFO of Experts LMS.",
          "dateOfBirth": null
        },
        "createdAt": null,
        "updatedAt": null
      }
    }
  ],
  "agenda": [],
  "speakers": [],
  "registrationsCount": 0,
  "paidRegistrationCount": 0,
  "pendingRegistrationCount": 0,
  "refundedRegistrationCount": 0,
  "netRevenueTotal": 0,
  "grossRevenueTotal": 0,
  "refundedRevenueTotal": 0,
  "likesCount": 0,
  "isLiked": false,
  "ratingCount": 0,
  "averageRating": 0,
  "viewCount": 0,
  "shareCount": 0,
  "bookmarkCount": 0,
  "isRegistered": false,
  "createdAt": "2026-05-09T11:53:39.660Z",
  "updatedAt": "2026-05-09T11:53:39.660Z"
}
```

the issue is for this specific payload, the event not found when visiting the event page
`[DEV]  GET /api/v1/creator/events/13f5b0b2-faf7-48ad-88e8-8d654090e95d 404 in 138ms (next.js: 104ms, proxy.ts: 3ms, application-code: 31ms)`

I tried to narrow it down to what might be causing the issue, it's most likely "Hosts & Speakers" section, when I remove it, the event is created successfully.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
