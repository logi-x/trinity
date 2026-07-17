---
title: "Login cURL command"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/auth"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Login cURL command

## Command

```bash
curl -X POST  https://api.dev.experts.com.sa/v1/login -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Requested-With: XMLHttpRequest" -d '{"email":"admin@experts.com.sa","password":"password"}'


```

## Response

```json
{
  "status": "success",
  "user": {
    "id": 2,
    "uuid": "b9891fd1-4a0a-493b-aa2f-1a9013f0ce8a",
    "first_name": "Admin",
    "last_name": "Account",
    "name": "Admin Account",
    "email": "<admin@experts.com.sa>",
    "username": "admin",
    "avatar_url": null,
    "country_code": "+966",
    "phone": "530828155",
    "bio": null,
    "metadata": null,
    "dob": "1990-07-09 09:13:21",
    "email_verified_at": "2025-06-08T06:13:21.000000Z",
    "email_verified": true,
    "phone_verified": true,
    "is_verified": true,
    "created_at": "2025-06-08T06:13:21.000000Z",
    "updated_at": "2025-06-08T06:13:21.000000Z",
    "roles": [
      {
        "uuid": "01974e2c-1647-7390-8ffa-aa1734dd3d91",
        "name": "admin",
        "guard_name": "web",
        "created_at": "2025-06-08T06:13:21.000000Z",
        "updated_at": "2025-06-08T06:13:21.000000Z",
        "pivot": {
          "model_type": "App\\Domains\\Users\\Models\\User",
          "model_uuid": "2",
          "role_id": "01974e2c-1647-7390-8ffa-aa1734dd3d91"
        }
      }
    ]
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIwMTk3NGUyYy1mNGNmLTcyMWMtYTcxMC0xYzc1ODM1MDQyZmUiLCJqdGkiOiI0YWFjYTk2Mjg3YzUyOTI1NWFmYjIxYjk3ZTBhMzIwNDBkNTI3YjcyYWZiYTkzZDczODlkMjg3ZmNjNzE5YTUxM2Y2OTIzY2ExY2IxZjgwNiIsImlhdCI6MTc1MjE5MDA5Ny41NzUxMjUsIm5iZiI6MTc1MjE5MDA5Ny41NzUxMjcsImV4cCI6MTc4MzcyNjA5Ny41MDExNDgsInN1YiI6IjIiLCJzY29wZXMiOlsiYWRtaW4iXX0.AT2jiwsfcICe7TpuuCiKvtyT0l79fZkgfAQh-wv2tivh-VbtITh6lYGlSygZbk_WUFddkOvVyYiaJr6jCMRYMlXLIXUIFfEaS4Oydx-w414UE5D6XfxIYKrtAgoe94qahhsS0u7eEcC0YKpmECwKYSj62VxnOcynaDMrWlMdU-_yS4lDgzEAcp804eprePrP3n7ivGfb8-OS-v9Ymgv5jhC8caDyZQ-nrS6mUnjBS85q6Ph1xkol5eX20DefutGMkBkrbIUB7vcExS8EJgQl7mYwE0g6tWMB2GO6nlSIfpKyAOlnBTgBEbG-WwrMGhgtjysJI0K3kORMQ-JYxTJgEbxkVjrKUZDfo9ZHHBqHUwPno7OhkK_7XfS1PESGMxwK_vpNnlDzTsT8px21a-Y6lwketMDnh4sBr9qacvQZHVPRPPg5Z9VKn1RgNLDokZCC27kzqy5i2HO9tVLhSZT8-GqD_1BWfkfFqlF1RbFZCbLIbmwrecL2bMf1Sb30Y7VQRa1RgN38dsat4ob05ov2hRNddhlchsXoMIpGJBN3571d2Fccfd563_ONXnG8L998BMLMLsx3zLCP-LolXatnTo_HgAiCIVfYvKCuxpzX7PSxL6hsfRsFOjlByrzHXzaG25OtzRtk46XnILlMyrRwla0c9EplerBq4FOcKjFI5-g",
  "token_type": "Bearer",
  "message": "User logged in successfully.",
  "success": true
}
```
