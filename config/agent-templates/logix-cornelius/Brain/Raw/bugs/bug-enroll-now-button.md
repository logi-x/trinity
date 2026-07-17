---
title: Enroll Now Button
date: 2026-05-13
status: open
resolution: unknown
tags: [bug, enroll-now-button, project/experts]
---

# Enroll Now Button

The Enroll Now button is not working as expected.

## Steps to Reproduce

1. Go to the course page `http://localhost:3025/en/courses/bb0ef8d0-1af6-4170-99e8-ba3111dd83b2`
2. Click on the "Enroll Now - Free" button

```json
// payload for enroll now button
{
    "userId": "ff4b3a65-1d6b-4e81-94fd-899fb9a9f961",
    "courseId": "bb0ef8d0-1af6-4170-99e8-ba3111dd83b2",
    "course": {
        "title": "Solar Solution Basic",
        "price": 0,
        "isFree": true
    },
    "provider": "stripe",
    "locale": "en",
    "baseUrl": "http://localhost:3025"
}
// response for enroll now button
{
    "free": true,
    "enrollment": {
        "id": "f28298fb-ae75-4bf2-8808-0796c8c30cc7",
        "enrolledAt": "2026-05-20T01:08:36.247Z",
        "progress": 0,
        "completedAt": null,
        "lastLessonId": null,
        "lastLessonAt": null,
        "provider": "free",
        "providerRef": null,
        "status": "completed",
        "course": {
            "id": "bb0ef8d0-1af6-4170-99e8-ba3111dd83b2",
            "title": "Solar Solution Basic",
            "description": "Learn the basic of solar solution",
            "thumbnailUrl": "",
            "category": "Science & Engineering",
            "level": "Beginner",
            "duration": 90,
            "totalLessons": 4,
            "price": 0,
            "isFree": true,
            "averageRating": 0,
            "ratingCount": 0,
            "viewCount": 0,
            "instructor": {
                "id": "ff4b3a65-1d6b-4e81-94fd-899fb9a9f961",
                "username": "egrzahid",
                "isVerified": true,
                "profile": {
                    "fullName": "Ahmad Zahid",
                    "avatarUrl": "https://cdn.experts.com.sa/s/avatars/user/default.png"
                }
            }
        }
    }
},

```

As shown, all work well but when I click on the Enroll Now button, it stays "Enroll Now - Free" instead of "Start learning".

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
