---
title: "Testing Guide: Multi-Host Events UI"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/testing-multi-host-events"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Testing Guide: Multi-Host Events UI

## 🧪 API Endpoints to Test

### 1. Search for Instructors

**Endpoint:** `GET /api/v1/users/search?q={query}`

**Test Cases:**

```bash
# Search by username
curl http://localhost:3025/api/v1/users/search?q=john

# Search by email
curl --location 'http://localhost:3025/api/v1/users/search?q=ahmed@logi-x.org' \
--header 'Cookie: authjs.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiMFVzazdoME9iMGdTczA0Rm1KSjI3YzJHR21jeFBBX1N3VlJUaTZBb0NzQnVNN081UlJmQVhvcnRLeFRzOUstczZVa3dNNXJDaF83RHo5c1lFR2pzb3cifQ..Ds0VxaVZ8qm0LSflsZh5Pg.DTC91C1WEjR3othLCUit5yUgD_Zt390vrAfDZaXdmzPo2iL2n4rdRoSQ4OuBWGdbQMlEok-oowUQN3jKqz8DGMJ6Im20H_6YtlVWoxGtWGPJnPAmLfjVQ1miSukhfH79ZeVDoQVgaHYBBJu2-RHiTgGvy-ziMIP6OgsQmF4MjeovdV0ltEiEYCgfsTFSxGA3xdeNsHwr0FcDk2-UU7JEKiuLL0f7S3Et_I7NDMH8voaaJLwpVpjj-IAXJSeQnlIhkr_ntx3VW3aRit4WD4_o88LyzWkvsf0RBo5SrhRj5ESbqB5lc3kEco4x2WTAxKLMoQ3oXTK4KNKp3aEUXFXV55KmziVd8GbJPmgAuQ7jduUewI3rSWegx1gS2IhpZ9yrVqUmJWnvoPdniXfUsftGK5BmxK0_aE-J11mfM37X29p8djKz7Yc4Z32httgQ_JDTmUOxZ2V-JmJcnC9EmtxTHbspqtXlZFKpdih7pLBzbMGlZ7GuH7iFj8WldW8V3Z8y.5P2D31fW0bWeLJugDDCTa4qKWhyijeRuT3FM2LrIQls'

# Search by full name
curl --location 'http://localhost:3025/api/v1/users/search?q=ahmed' \
--header 'Cookie: authjs.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiMFVzazdoME9iMGdTczA0Rm1KSjI3YzJHR21jeFBBX1N3VlJUaTZBb0NzQnVNN081UlJmQVhvcnRLeFRzOUstczZVa3dNNXJDaF83RHo5c1lFR2pzb3cifQ..Ds0VxaVZ8qm0LSflsZh5Pg.DTC91C1WEjR3othLCUit5yUgD_Zt390vrAfDZaXdmzPo2iL2n4rdRoSQ4OuBWGdbQMlEok-oowUQN3jKqz8DGMJ6Im20H_6YtlVWoxGtWGPJnPAmLfjVQ1miSukhfH79ZeVDoQVgaHYBBJu2-RHiTgGvy-ziMIP6OgsQmF4MjeovdV0ltEiEYCgfsTFSxGA3xdeNsHwr0FcDk2-UU7JEKiuLL0f7S3Et_I7NDMH8voaaJLwpVpjj-IAXJSeQnlIhkr_ntx3VW3aRit4WD4_o88LyzWkvsf0RBo5SrhRj5ESbqB5lc3kEco4x2WTAxKLMoQ3oXTK4KNKp3aEUXFXV55KmziVd8GbJPmgAuQ7jduUewI3rSWegx1gS2IhpZ9yrVqUmJWnvoPdniXfUsftGK5BmxK0_aE-J11mfM37X29p8djKz7Yc4Z32httgQ_JDTmUOxZ2V-JmJcnC9EmtxTHbspqtXlZFKpdih7pLBzbMGlZ7GuH7iFj8WldW8V3Z8y.5P2D31fW0bWeLJugDDCTa4qKWhyijeRuT3FM2LrIQls'

# Empty query (should return empty array)
curl http://localhost:3025/api/v1/users/search?q=
```

**Expected Response:**

```json
[
  {
    "id": "uuid",
    "username": "johndoe",
    "email": "john@example.com",
    "isVerified": true,
    "profile": {
      "fullName": "John Doe",
      "avatarUrl": "https://...",
      "bio": "..."
    }
  }
]
```

---

### 2. Get Event Hosts

**Endpoint:** `GET /api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d/hosts`

**Test Cases:**

```bash
# Get all hosts for an event
curl -H 'Cookie: authjs.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiMFVzazdoME9iMGdTczA0Rm1KSjI3YzJHR21jeFBBX1N3VlJUaTZBb0NzQnVNN081UlJmQVhvcnRLeFRzOUstczZVa3dNNXJDaF83RHo5c1lFR2pzb3cifQ..Ds0VxaVZ8qm0LSflsZh5Pg.DTC91C1WEjR3othLCUit5yUgD_Zt390vrAfDZaXdmzPo2iL2n4rdRoSQ4OuBWGdbQMlEok-oowUQN3jKqz8DGMJ6Im20H_6YtlVWoxGtWGPJnPAmLfjVQ1miSukhfH79ZeVDoQVgaHYBBJu2-RHiTgGvy-ziMIP6OgsQmF4MjeovdV0ltEiEYCgfsTFSxGA3xdeNsHwr0FcDk2-UU7JEKiuLL0f7S3Et_I7NDMH8voaaJLwpVpjj-IAXJSeQnlIhkr_ntx3VW3aRit4WD4_o88LyzWkvsf0RBo5SrhRj5ESbqB5lc3kEco4x2WTAxKLMoQ3oXTK4KNKp3aEUXFXV55KmziVd8GbJPmgAuQ7jduUewI3rSWegx1gS2IhpZ9yrVqUmJWnvoPdniXfUsftGK5BmxK0_aE-J11mfM37X29p8djKz7Yc4Z32httgQ_JDTmUOxZ2V-JmJcnC9EmtxTHbspqtXlZFKpdih7pLBzbMGlZ7GuH7iFj8WldW8V3Z8y.5P2D31fW0bWeLJugDDCTa4qKWhyijeRuT3FM2LrIQls' \
  http://localhost:3025/api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d/hosts | jq
```

**Expected Response:**

```json
[
  {
    "eventId": "uuid",
    "userId": "uuid",
    "role": "primary",
    "revenueShare": 60.0,
    "isVisible": true,
    "user": {
      "id": "uuid",
      "username": "johndoe",
      "email": "john@example.com",
      "isVerified": true,
      "profile": {
        "fullName": "John Doe",
        "avatarUrl": "https://...",
        "bio": "..."
      }
    }
  }
]
```

---

### 3. Add Host to Event

**Endpoint:** `POST /api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d/hosts`

**Test Cases:**

```bash
# Add a guest host
curl -X POST \
  -H "Content-Type: application/json" \
  -H 'Cookie: authjs.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiMFVzazdoME9iMGdTczA0Rm1KSjI3YzJHR21jeFBBX1N3VlJUaTZBb0NzQnVNN081UlJmQVhvcnRLeFRzOUstczZVa3dNNXJDaF83RHo5c1lFR2pzb3cifQ..Ds0VxaVZ8qm0LSflsZh5Pg.DTC91C1WEjR3othLCUit5yUgD_Zt390vrAfDZaXdmzPo2iL2n4rdRoSQ4OuBWGdbQMlEok-oowUQN3jKqz8DGMJ6Im20H_6YtlVWoxGtWGPJnPAmLfjVQ1miSukhfH79ZeVDoQVgaHYBBJu2-RHiTgGvy-ziMIP6OgsQmF4MjeovdV0ltEiEYCgfsTFSxGA3xdeNsHwr0FcDk2-UU7JEKiuLL0f7S3Et_I7NDMH8voaaJLwpVpjj-IAXJSeQnlIhkr_ntx3VW3aRit4WD4_o88LyzWkvsf0RBo5SrhRj5ESbqB5lc3kEco4x2WTAxKLMoQ3oXTK4KNKp3aEUXFXV55KmziVd8GbJPmgAuQ7jduUewI3rSWegx1gS2IhpZ9yrVqUmJWnvoPdniXfUsftGK5BmxK0_aE-J11mfM37X29p8djKz7Yc4Z32httgQ_JDTmUOxZ2V-JmJcnC9EmtxTHbspqtXlZFKpdih7pLBzbMGlZ7GuH7iFj8WldW8V3Z8y.5P2D31fW0bWeLJugDDCTa4qKWhyijeRuT3FM2LrIQls' \
  -d '{
    "userId": "ff4b3a65-1d6b-4e81-94fd-899fb9a9f961",
    "role": "co",
    "revenueShare": null,
    "isVisible": true
  }' \
  http://localhost:3025/api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d/hosts | jq

# Add a co-host with revenue share
curl -X POST \
  -H "Content-Type: application/json" \
    -H "Cookie: authjs.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiMFVzazdoME9iMGdTczA0Rm1KSjI3YzJHR21jeFBBX1N3VlJUaTZBb0NzQnVNN081UlJmQVhvcnRLeFRzOUstczZVa3dNNXJDaF83RHo5c1lFR2pzb3cifQ..Ds0VxaVZ8qm0LSflsZh5Pg.DTC91C1WEjR3othLCUit5yUgD_Zt390vrAfDZaXdmzPo2iL2n4rdRoSQ4OuBWGdbQMlEok-oowUQN3jKqz8DGMJ6Im20H_6YtlVWoxGtWGPJnPAmLfjVQ1miSukhfH79ZeVDoQVgaHYBBJu2-RHiTgGvy-ziMIP6OgsQmF4MjeovdV0ltEiEYCgfsTFSxGA3xdeNsHwr0FcDk2-UU7JEKiuLL0f7S3Et_I7NDMH8voaaJLwpVpjj-IAXJSeQnlIhkr_ntx3VW3aRit4WD4_o88LyzWkvsf0RBo5SrhRj5ESbqB5lc3kEco4x2WTAxKLMoQ3oXTK4KNKp3aEUXFXV55KmziVd8GbJPmgAuQ7jduUewI3rSWegx1gS2IhpZ9yrVqUmJWnvoPdniXfUsftGK5BmxK0_aE-J11mfM37X29p8djKz7Yc4Z32httgQ_JDTmUOxZ2V-JmJcnC9EmtxTHbspqtXlZFKpdih7pLBzbMGlZ7GuH7iFj8WldW8V3Z8y.5P2D31fW0bWeLJugDDCTa4qKWhyijeRuT3FM2LrIQls" \
  -d '{
    "userId": "e81a705b-d817-4350-8b44-1f9d694d4ffa",
    "role": "co",
    "revenueShare": 30.00,
    "isVisible": true
  }' \
  http://localhost:3025/api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d/hosts | jq

# Try to add duplicate host (should fail)
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Cookie: authjs.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiMFVzazdoME9iMGdTczA0Rm1KSjI3YzJHR21jeFBBX1N3VlJUaTZBb0NzQnVNN081UlJmQVhvcnRLeFRzOUstczZVa3dNNXJDaF83RHo5c1lFR2pzb3cifQ..Ds0VxaVZ8qm0LSflsZh5Pg.DTC91C1WEjR3othLCUit5yUgD_Zt390vrAfDZaXdmzPo2iL2n4rdRoSQ4OuBWGdbQMlEok-oowUQN3jKqz8DGMJ6Im20H_6YtlVWoxGtWGPJnPAmLfjVQ1miSukhfH79ZeVDoQVgaHYBBJu2-RHiTgGvy-ziMIP6OgsQmF4MjeovdV0ltEiEYCgfsTFSxGA3xdeNsHwr0FcDk2-UU7JEKiuLL0f7S3Et_I7NDMH8voaaJLwpVpjj-IAXJSeQnlIhkr_ntx3VW3aRit4WD4_o88LyzWkvsf0RBo5SrhRj5ESbqB5lc3kEco4x2WTAxKLMoQ3oXTK4KNKp3aEUXFXV55KmziVd8GbJPmgAuQ7jduUewI3rSWegx1gS2IhpZ9yrVqUmJWnvoPdniXfUsftGK5BmxK0_aE-J11mfM37X29p8djKz7Yc4Z32httgQ_JDTmUOxZ2V-JmJcnC9EmtxTHbspqtXlZFKpdih7pLBzbMGlZ7GuH7iFj8WldW8V3Z8y.5P2D31fW0bWeLJugDDCTa4qKWhyijeRuT3FM2LrIQls" \
  -d '{
    "userId": "e81a705b-d817-4350-8b44-1f9d694d4ffa",
    "role": "guest"
  }' \
  http://localhost:3025/api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d/hosts
```

**Expected Responses:**

- Success: `201 Created` with host object
- Duplicate: `400 Bad Request` with error message
- Unauthorized: `401 Unauthorized`
- Forbidden: `403 Forbidden` (if not an instructor for the event)

---

### 4. Update Host

**Endpoint:** `PUT /api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d/hosts/{userId}`

**Test Cases:**

```bash
# Update host role
curl -X PUT \
  -H "Content-Type: application/json" \
  -H "Cookie: authjs.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiMFVzazdoME9iMGdTczA0Rm1KSjI3YzJHR21jeFBBX1N3VlJUaTZBb0NzQnVNN081UlJmQVhvcnRLeFRzOUstczZVa3dNNXJDaF83RHo5c1lFR2pzb3cifQ..Ds0VxaVZ8qm0LSflsZh5Pg.DTC91C1WEjR3othLCUit5yUgD_Zt390vrAfDZaXdmzPo2iL2n4rdRoSQ4OuBWGdbQMlEok-oowUQN3jKqz8DGMJ6Im20H_6YtlVWoxGtWGPJnPAmLfjVQ1miSukhfH79ZeVDoQVgaHYBBJu2-RHiTgGvy-ziMIP6OgsQmF4MjeovdV0ltEiEYCgfsTFSxGA3xdeNsHwr0FcDk2-UU7JEKiuLL0f7S3Et_I7NDMH8voaaJLwpVpjj-IAXJSeQnlIhkr_ntx3VW3aRit4WD4_o88LyzWkvsf0RBo5SrhRj5ESbqB5lc3kEco4x2WTAxKLMoQ3oXTK4KNKp3aEUXFXV55KmziVd8GbJPmgAuQ7jduUewI3rSWegx1gS2IhpZ9yrVqUmJWnvoPdniXfUsftGK5BmxK0_aE-J11mfM37X29p8djKz7Yc4Z32httgQ_JDTmUOxZ2V-JmJcnC9EmtxTHbspqtXlZFKpdih7pLBzbMGlZ7GuH7iFj8WldW8V3Z8y.5P2D31fW0bWeLJugDDCTa4qKWhyijeRuT3FM2LrIQls" \
  -d '{
    "role": "guest"
  }' \
  http://localhost:3025/api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d/hosts/e81a705b-d817-4350-8b44-1f9d694d4ffa | jq

# Update revenue share
curl -X PUT \
  -H "Content-Type: application/json" \
  -H "Cookie: authjs.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiMFVzazdoME9iMGdTczA0Rm1KSjI3YzJHR21jeFBBX1N3VlJUaTZBb0NzQnVNN081UlJmQVhvcnRLeFRzOUstczZVa3dNNXJDaF83RHo5c1lFR2pzb3cifQ..Ds0VxaVZ8qm0LSflsZh5Pg.DTC91C1WEjR3othLCUit5yUgD_Zt390vrAfDZaXdmzPo2iL2n4rdRoSQ4OuBWGdbQMlEok-oowUQN3jKqz8DGMJ6Im20H_6YtlVWoxGtWGPJnPAmLfjVQ1miSukhfH79ZeVDoQVgaHYBBJu2-RHiTgGvy-ziMIP6OgsQmF4MjeovdV0ltEiEYCgfsTFSxGA3xdeNsHwr0FcDk2-UU7JEKiuLL0f7S3Et_I7NDMH8voaaJLwpVpjj-IAXJSeQnlIhkr_ntx3VW3aRit4WD4_o88LyzWkvsf0RBo5SrhRj5ESbqB5lc3kEco4x2WTAxKLMoQ3oXTK4KNKp3aEUXFXV55KmziVd8GbJPmgAuQ7jduUewI3rSWegx1gS2IhpZ9yrVqUmJWnvoPdniXfUsftGK5BmxK0_aE-J11mfM37X29p8djKz7Yc4Z32httgQ_JDTmUOxZ2V-JmJcnC9EmtxTHbspqtXlZFKpdih7pLBzbMGlZ7GuH7iFj8WldW8V3Z8y.5P2D31fW0bWeLJugDDCTa4qKWhyijeRuT3FM2LrIQls" \
  -d '{
    "revenueShare": 40.00
  }' \
  http://localhost:3025/api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d/hosts/e81a705b-d817-4350-8b44-1f9d694d4ffa | jq

# Hide host
curl -X PUT \
  -H "Content-Type: application/json" \
  -H "Cookie: authjs.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiMFVzazdoME9iMGdTczA0Rm1KSjI3YzJHR21jeFBBX1N3VlJUaTZBb0NzQnVNN081UlJmQVhvcnRLeFRzOUstczZVa3dNNXJDaF83RHo5c1lFR2pzb3cifQ..Ds0VxaVZ8qm0LSflsZh5Pg.DTC91C1WEjR3othLCUit5yUgD_Zt390vrAfDZaXdmzPo2iL2n4rdRoSQ4OuBWGdbQMlEok-oowUQN3jKqz8DGMJ6Im20H_6YtlVWoxGtWGPJnPAmLfjVQ1miSukhfH79ZeVDoQVgaHYBBJu2-RHiTgGvy-ziMIP6OgsQmF4MjeovdV0ltEiEYCgfsTFSxGA3xdeNsHwr0FcDk2-UU7JEKiuLL0f7S3Et_I7NDMH8voaaJLwpVpjj-IAXJSeQnlIhkr_ntx3VW3aRit4WD4_o88LyzWkvsf0RBo5SrhRj5ESbqB5lc3kEco4x2WTAxKLMoQ3oXTK4KNKp3aEUXFXV55KmziVd8GbJPmgAuQ7jduUewI3rSWegx1gS2IhpZ9yrVqUmJWnvoPdniXfUsftGK5BmxK0_aE-J11mfM37X29p8djKz7Yc4Z32httgQ_JDTmUOxZ2V-JmJcnC9EmtxTHbspqtXlZFKpdih7pLBzbMGlZ7GuH7iFj8WldW8V3Z8y.5P2D31fW0bWeLJugDDCTa4qKWhyijeRuT3FM2LrIQls" \
  -d '{
    "isVisible": false
  }' \
  http://localhost:3025/api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d/hosts/e81a705b-d817-4350-8b44-1f9d694d4ffa | jq

# Update multiple fields
curl -X PUT \
  -H "Content-Type: application/json" \
  -H "Cookie: authjs.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiMFVzazdoME9iMGdTczA0Rm1KSjI3YzJHR21jeFBBX1N3VlJUaTZBb0NzQnVNN081UlJmQVhvcnRLeFRzOUstczZVa3dNNXJDaF83RHo5c1lFR2pzb3cifQ..Ds0VxaVZ8qm0LSflsZh5Pg.DTC91C1WEjR3othLCUit5yUgD_Zt390vrAfDZaXdmzPo2iL2n4rdRoSQ4OuBWGdbQMlEok-oowUQN3jKqz8DGMJ6Im20H_6YtlVWoxGtWGPJnPAmLfjVQ1miSukhfH79ZeVDoQVgaHYBBJu2-RHiTgGvy-ziMIP6OgsQmF4MjeovdV0ltEiEYCgfsTFSxGA3xdeNsHwr0FcDk2-UU7JEKiuLL0f7S3Et_I7NDMH8voaaJLwpVpjj-IAXJSeQnlIhkr_ntx3VW3aRit4WD4_o88LyzWkvsf0RBo5SrhRj5ESbqB5lc3kEco4x2WTAxKLMoQ3oXTK4KNKp3aEUXFXV55KmziVd8GbJPmgAuQ7jduUewI3rSWegx1gS2IhpZ9yrVqUmJWnvoPdniXfUsftGK5BmxK0_aE-J11mfM37X29p8djKz7Yc4Z32httgQ_JDTmUOxZ2V-JmJcnC9EmtxTHbspqtXlZFKpdih7pLBzbMGlZ7GuH7iFj8WldW8V3Z8y.5P2D31fW0bWeLJugDDCTa4qKWhyijeRuT3FM2LrIQls" \
  -d '{
    "role": "primary",
    "revenueShare": 50.00,
    "isVisible": true
  }' \
  http://localhost:3025/api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d/hosts/e81a705b-d817-4350-8b44-1f9d694d4ffa | jq
```

**Expected Response:**

```json
{
  "eventId": "uuid",
  "userId": "uuid",
  "role": "primary",
  "revenueShare": 50.00,
  "isVisible": true,
  "user": { ... }
}
```

---

### 5. Remove Host

**Endpoint:** `DELETE /api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d/hosts/{userId}`

**Test Cases:**

```bash
# Remove a guest or co-host
curl -X DELETE \
  -H "Cookie: authjs.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiMFVzazdoME9iMGdTczA0Rm1KSjI3YzJHR21jeFBBX1N3VlJUaTZBb0NzQnVNN081UlJmQVhvcnRLeFRzOUstczZVa3dNNXJDaF83RHo5c1lFR2pzb3cifQ..Ds0VxaVZ8qm0LSflsZh5Pg.DTC91C1WEjR3othLCUit5yUgD_Zt390vrAfDZaXdmzPo2iL2n4rdRoSQ4OuBWGdbQMlEok-oowUQN3jKqz8DGMJ6Im20H_6YtlVWoxGtWGPJnPAmLfjVQ1miSukhfH79ZeVDoQVgaHYBBJu2-RHiTgGvy-ziMIP6OgsQmF4MjeovdV0ltEiEYCgfsTFSxGA3xdeNsHwr0FcDk2-UU7JEKiuLL0f7S3Et_I7NDMH8voaaJLwpVpjj-IAXJSeQnlIhkr_ntx3VW3aRit4WD4_o88LyzWkvsf0RBo5SrhRj5ESbqB5lc3kEco4x2WTAxKLMoQ3oXTK4KNKp3aEUXFXV55KmziVd8GbJPmgAuQ7jduUewI3rSWegx1gS2IhpZ9yrVqUmJWnvoPdniXfUsftGK5BmxK0_aE-J11mfM37X29p8djKz7Yc4Z32httgQ_JDTmUOxZ2V-JmJcnC9EmtxTHbspqtXlZFKpdih7pLBzbMGlZ7GuH7iFj8WldW8V3Z8y.5P2D31fW0bWeLJugDDCTa4qKWhyijeRuT3FM2LrIQls" \
  http://localhost:3025/api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d/hosts/{userId}

# Try to remove last primary host (should fail)
curl -X DELETE \
  -H "Cookie: authjs.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiMFVzazdoME9iMGdTczA0Rm1KSjI3YzJHR21jeFBBX1N3VlJUaTZBb0NzQnVNN081UlJmQVhvcnRLeFRzOUstczZVa3dNNXJDaF83RHo5c1lFR2pzb3cifQ..Ds0VxaVZ8qm0LSflsZh5Pg.DTC91C1WEjR3othLCUit5yUgD_Zt390vrAfDZaXdmzPo2iL2n4rdRoSQ4OuBWGdbQMlEok-oowUQN3jKqz8DGMJ6Im20H_6YtlVWoxGtWGPJnPAmLfjVQ1miSukhfH79ZeVDoQVgaHYBBJu2-RHiTgGvy-ziMIP6OgsQmF4MjeovdV0ltEiEYCgfsTFSxGA3xdeNsHwr0FcDk2-UU7JEKiuLL0f7S3Et_I7NDMH8voaaJLwpVpjj-IAXJSeQnlIhkr_ntx3VW3aRit4WD4_o88LyzWkvsf0RBo5SrhRj5ESbqB5lc3kEco4x2WTAxKLMoQ3oXTK4KNKp3aEUXFXV55KmziVd8GbJPmgAuQ7jduUewI3rSWegx1gS2IhpZ9yrVqUmJWnvoPdniXfUsftGK5BmxK0_aE-J11mfM37X29p8djKz7Yc4Z32httgQ_JDTmUOxZ2V-JmJcnC9EmtxTHbspqtXlZFKpdih7pLBzbMGlZ7GuH7iFj8WldW8V3Z8y.5P2D31fW0bWeLJugDDCTa4qKWhyijeRuT3FM2LrIQls" \
  http://localhost:3025/api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d/hosts/{primaryHostUserId}
```

**Expected Responses:**

- Success: `200 OK` with `{"success": true}`
- Last primary host: `400 Bad Request` with error message
- Not found: `404 Not Found`

---

### 6. Get Event with Hosts

**Endpoint:** `GET /api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d`

**Test Cases:**

```bash
# Get event details (should include hosts array)
curl http://localhost:3025/api/v1/events/06245481-0cab-483d-9a26-030b3ff57d5d
```

**Expected Response:**

```json
{
  "id": "uuid",
  "title": "Event Title",
  "host": { ... }, // Primary host (backward compatibility)
  "hosts": [       // All visible hosts
    {
      "userId": "uuid",
      "role": "primary",
      "revenueShare": 60.00,
      "isVisible": true,
      "user": { ... }
    },
    {
      "userId": "uuid",
      "role": "co",
      "revenueShare": 40.00,
      "isVisible": true,
      "user": { ... }
    }
  ],
  ...
}
```

---

## 🖥️ UI Pages to Test

### 1. Event Edit Page

**URL:** `/creator/events/06245481-0cab-483d-9a26-030b3ff57d5d/edit`

**Test Scenarios:**

1. **View Existing Hosts**
   - Navigate to event edit page
   - Scroll to "Event Hosts" section
   - Verify all existing hosts are displayed
   - Check roles, revenue shares, and visibility badges

2. **Search and Add Host**
   - Type in search box (e.g., "john")
   - Wait for search results (debounced 300ms)
   - Verify only instructors appear
   - Verify already-added hosts are filtered out
   - Click "Add" button on a user
   - Verify host appears in list
   - Verify search box clears

3. **Update Host Role**
   - Select different role from dropdown (primary/co/guest)
   - Verify role badge updates
   - Verify API call succeeds

4. **Update Revenue Share**
   - Enter percentage in revenue share input
   - Verify total revenue share updates
   - Verify warning if sum ≠ 100%
   - Verify green indicator when sum = 100%

5. **Hide/Show Host**
   - Toggle visibility (if implemented)
   - Verify host disappears from public view

6. **Remove Host**
   - Click trash icon on a guest/co-host
   - Confirm deletion
   - Verify host is removed
   - Try to remove last primary host
   - Verify error message appears

7. **Revenue Share Validation**
   - Add multiple hosts with revenue shares
   - Verify total shows at bottom
   - Verify warning when sum ≠ 100%
   - Verify green indicator when sum = 100%

---

### 2. Event Detail Page

**URL:** `/events/06245481-0cab-483d-9a26-030b3ff57d5d`

**Test Scenarios:**

1. **View Multiple Hosts**
   - Navigate to event detail page
   - Verify all visible hosts are displayed
   - Check avatars show correctly
   - Verify "+N" indicator for more than 3 hosts

---

### 3. Event Cards (Listings)

**URLs:**

- `/events` (event listing)
- `/events/calendar` (calendar view)
- `/dashboard` (user dashboard)

**Test Scenarios:**

1. **Multiple Hosts Display**
   - View event cards in listings
   - Verify multiple host avatars show (up to 3)
   - Verify "+N" indicator for more hosts
   - Verify host count text ("2 hosts", "3 hosts", etc.)

2. **Single Host Fallback**
   - View events with only one host
   - Verify single host displays correctly
   - Verify backward compatibility with old `host` field

---

## ✅ Test Checklist

### API Endpoints

- [ ] Search users by username
- [ ] Search users by email
- [ ] Search users by full name
- [ ] Get all hosts for an event
- [ ] Add guest host
- [ ] Add co-host with revenue share
- [ ] Add primary host
- [ ] Prevent duplicate host addition
- [ ] Update host role
- [ ] Update revenue share
- [ ] Update visibility
- [ ] Remove guest/co-host
- [ ] Prevent removing last primary host
- [ ] Unauthorized access returns 401
- [ ] Non-instructor access returns 403

### UI Components

- [ ] EventHostManager displays existing hosts
- [ ] Search functionality works (debounced)
- [ ] Search filters out existing hosts
- [ ] Add host button works
- [ ] Role dropdown updates correctly
- [ ] Revenue share input updates correctly
- [ ] Revenue share total calculates correctly
- [ ] Warning shows when sum ≠ 100%
- [ ] Green indicator shows when sum = 100%
- [ ] Remove button works (except last primary)
- [ ] Error messages display correctly
- [ ] Success toasts appear

### Event Display

- [ ] Event cards show multiple hosts
- [ ] Event detail page shows all hosts
- [ ] Avatars display correctly
- [ ] "+N" indicator works for >3 hosts
- [ ] Host count text displays correctly
- [ ] Backward compatibility with single host

### Edge Cases

- [ ] Event with no hosts
- [ ] Event with 1 host
- [ ] Event with 3 hosts
- [ ] Event with 5+ hosts
- [ ] Hidden hosts don't appear in public view
- [ ] Revenue shares sum to exactly 100%
- [ ] Revenue shares sum to 99.99% (should warn)
- [ ] Revenue shares sum to 100.01% (should warn)

---

## 🐛 Common Issues to Watch For

1. **Search not working**
   - Check debounce delay (300ms)
   - Verify API endpoint returns results
   - Check network tab for errors

2. **Hosts not displaying**
   - Verify API returns `hosts` array
   - Check if hosts are filtered by `isVisible`
   - Verify event has hosts in database

3. **Revenue share validation**
   - Check if validation runs on publish
   - Verify Decimal precision handling
   - Check tolerance (0.01%)

4. **Permission errors**
   - Verify user is instructor for event
   - Check session/authentication
   - Verify `isContentInstructor` function

---

## 📝 Manual Testing Steps

1. **Create a test event** (if needed)

   ```bash
   # Use the create event page or API
   POST /api/v1/events
   ```

2. **Add yourself as primary host** (if not already)
   - Go to event edit page
   - Search for your username
   - Add yourself as primary host

3. **Add multiple hosts**
   - Search for other instructors
   - Add them as co-hosts or guests
   - Set revenue shares

4. **Test revenue share validation**
   - Set shares that don't sum to 100%
   - Verify warning appears
   - Adjust to sum to 100%
   - Verify green indicator

5. **Test removal**
   - Try removing guest hosts
   - Try removing co-hosts
   - Try removing last primary (should fail)

6. **View public pages**
   - Check event detail page
   - Check event listings
   - Verify hosts display correctly

---

## 🔗 Related Files

- **API Routes:**
  - `app/api/v1/events/[id]/hosts/route.ts`
  - `app/api/v1/events/[id]/hosts/[userId]/route.ts`
  - `app/api/v1/users/search/route.ts`
  - `app/api/v1/events/[id]/route.ts`

- **Components:**
  - `src/components/events/EventHostManager.tsx`
  - `src/components/events/EventCard.tsx`

- **Pages:**
  - `app/creator/events/[id]/edit/page.tsx`
  - `app/events/[id]/page.tsx`
  - `app/events/page.tsx`

- **Hooks:**
  - `src/hooks/use-events.ts`

- **Services:**
  - `src/modules/permissions/permissions.service.ts`
