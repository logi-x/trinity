---
title: "Experts Lti Implementation Plan"
date: "2026-04-17"
tags: [plan, project/experts]
category: "plan"
---

Absolutely — below is a **step-by-step LTI implementation plan** written in the same spirit as your previous implementation guide, but adapted for **Experts** and structured so an **LLM can follow it incrementally**. I used the attached plan’s style as the reference shape.

---

# Experts LTI Implementation Plan

## Summary

Yes, this is doable, but it should be implemented in **phases**.

For **Experts**, LTI should be introduced first as a **clean integration boundary**, not as a deep rewrite of the platform. The goal is to allow external LMS platforms such as **Moodle, Blackboard, Canvas, or FutureX** to launch learning content from Experts, identify the learner securely, and optionally return progress or completion data.

Recommended direction:

- implement **LTI 1.3 Advantage only**
- treat LTI as a dedicated integration module, not scattered across existing course logic
- separate:
  - **platform registration**
  - **launch validation**
  - **user/session resolution**
  - **course access mapping**
  - **AGS/NRPS/deep-linking support**

- ship in stages:
  1. **basic launch**
  2. **user/course mapping**
  3. **grade/progress return**
  4. optional advanced services

Do **not** start with LTI 1.1 or custom ad-hoc LMS integrations.

---

# Primary Goal

Allow an external LMS to:

1. register Experts as an LTI tool
2. launch a course/lesson/activity inside Experts
3. authenticate the learner via signed LTI launch
4. create or resolve the local Experts user
5. enroll or map the learner correctly
6. optionally send progress / score / completion back to the LMS

---

# Scope Recommendation

## Phase 1 scope

Implement only:

- LTI 1.3 login initiation
- LTI 1.3 launch endpoint
- signed JWT validation
- platform registration model
- deployment/client configuration model
- learner resolution
- basic resource launch
- session creation inside Experts

## Phase 2 scope

Add:

- AGS (Assignment and Grade Services)
- score passback
- progress/completion sync
- launch context persistence
- instructor vs learner role handling

## Phase 3 scope

Optional:

- NRPS (Names and Roles Provisioning Services)
- Deep Linking
- multi-tenant institution-specific mapping
- admin UI for platform registration
- audit tools and diagnostics

---

# Architecture Direction

Use a dedicated module, for example:

```txt
apps/experts-app
  /app/api/lti/...
  /lib/lti/...
  /server/lti/...
```

Suggested internal layers:

- `LtiPlatformService`
- `LtiLaunchService`
- `LtiUserResolutionService`
- `LtiEnrollmentService`
- `LtiGradeService`
- `LtiTokenService`
- `LtiAuditService`

Do **not** bury this logic directly inside generic auth or course controllers.

---

# Data Model

Recommended tables/entities:

## `LtiPlatform`

Represents the external LMS or institution.

Fields:

- `id`
- `name`
- `issuer`
- `authLoginUrl`
- `authTokenUrl`
- `jwksUrl`
- `clientId`
- `deploymentId`
- `isActive`
- `createdAt`
- `updatedAt`

## `LtiPlatformKeyCache`

Optional local cache of platform public keys.

Fields:

- `id`
- `platformId`
- `kid`
- `jwk`
- `expiresAt`
- `createdAt`

## `LtiLaunch`

Stores each validated LTI launch.

Fields:

- `id`
- `platformId`
- `deploymentId`
- `messageType`
- `targetLinkUri`
- `resourceLinkId`
- `contextId`
- `contextTitle`
- `userSub`
- `userEmail`
- `userGivenName`
- `userFamilyName`
- `roles`
- `rawClaimsJson`
- `status`
- `launchedAt`

## `LtiUserLink`

Maps LMS user identity to local Experts user.

Fields:

- `id`
- `platformId`
- `userSub`
- `email`
- `userId`
- `lastLaunchAt`
- unique on `(platformId, userSub)`

## `LtiResourceLink`

Maps LMS resource links to Experts resources.

Fields:

- `id`
- `platformId`
- `resourceLinkId`
- `contextId`
- `courseId?`
- `lessonId?`
- `eventId?`
- `activityType`
- `createdAt`
- `updatedAt`

## `LtiEnrollmentLink`

Optional enrollment bridge.

Fields:

- `id`
- `platformId`
- `contextId`
- `userId`
- `courseId`
- `externalRole`
- `createdAt`

## `LtiLineItem`

For AGS support later.

Fields:

- `id`
- `platformId`
- `courseId`
- `lessonId?`
- `resourceLinkId`
- `lineItemUrl`
- `label`
- `scoreMaximum`
- `createdAt`

---

# Why separate LTI models

Do **not** try to overload your existing user/course/enrollment models with raw LMS metadata everywhere.

Reason:

- LTI claims are external-system specific
- identity mapping must be stable over time
- launch records are useful for debugging
- one user may come from several institutions/platforms
- AGS and deep linking introduce platform-specific data that should stay isolated

---

# Route Structure

Suggested endpoints:

## OIDC / Login

- `GET /api/lti/login`

Receives:

- `iss`
- `login_hint`
- `target_link_uri`
- `lti_message_hint`
- `client_id`

Purpose:

- validate the platform/client
- generate `state` and `nonce`
- redirect to the LMS authorization endpoint

---

## LTI Launch

- `POST /api/lti/launch`

Purpose:

- receive the `id_token`
- validate JWT and claims
- validate nonce/state
- resolve or create local user
- map resource
- create Experts session
- redirect learner into target Experts page

---

## JWKS

- `GET /api/lti/jwks`

Purpose:

- expose Experts public keys if needed for certain flows
- useful if Experts later acts as a platform in other scenarios

---

## AGS / Grade Sync

Phase 2:

- `POST /api/lti/ags/sync`
- or internal service job, not necessarily public

---

# Claims Validation Rules

On launch, validate at minimum:

- `iss` matches registered platform issuer
- `aud` contains Experts client ID
- `exp` is valid
- `nonce` matches stored nonce
- `deployment_id` matches allowed deployment
- `message_type` is supported
- `version` is LTI 1.3
- required LTI claims exist

Support these message types first:

- `LtiResourceLinkRequest`

Later:

- `LtiDeepLinkingRequest`

---

# User Resolution Strategy

Recommended order:

1. match existing `LtiUserLink` by `(platformId, userSub)`
2. else try email match if email is present and trusted
3. else create a new user stub/profile
4. create/update `LtiUserLink`

Important:

- do not rely only on email
- `sub` is the stable external identity key
- preserve the platform-to-user mapping permanently

---

# Role Mapping

Map external LTI roles into internal Experts roles.

Initial mapping:

- learner/student → learner
- instructor/faculty → instructor or staff access
- administrator → admin-like elevated context only if explicitly allowed

Do not automatically give full platform admin rights just because the external role says administrator.

Use a constrained mapping table.

---

# Resource Mapping

Decide what an LTI launch can open.

Recommended v1 target types:

- course landing page
- lesson page
- assessment page

Do not try to expose all internal Experts routes initially.

Use `LtiResourceLink` to map:

- external `resource_link.id`
- external `context.id`
- internal `courseId` / `lessonId`

Fallback behavior:

- if no mapping exists, route to a safe landing page or a “resource not configured” page

---

# Session Strategy

After successful launch:

1. validate launch
2. resolve/create local user
3. create Experts authenticated session
4. attach short-lived LTI launch context to session
5. redirect to the mapped Experts resource

Do **not** keep the full LTI payload in a browser-visible token.

Store sensitive claims server-side.

---

# AGS / Grade Return Plan

Phase 2 only.

When a learner completes an activity:

1. load linked `LtiLineItem`
2. obtain platform access token using OAuth client credentials / service flow as required
3. send score result to LMS
4. store sync result and timestamp
5. retry failures asynchronously if needed

Suggested sync events:

- quiz submission
- course completion
- lesson completion
- certification completion if applicable later

Do not implement score sync before launch/auth flow is stable.

---

# Deep Linking Plan

Phase 3 only.

Use deep linking if an LMS instructor wants to pick Experts content from inside their LMS.

Flow:

1. LMS sends deep-linking request
2. Experts shows content picker UI
3. instructor selects course/lesson/resource
4. Experts returns signed deep-link response
5. LMS stores the selected launchable resource

Skip this entirely for v1.

---

# Security Requirements

Must-have protections:

- signed JWT validation against platform JWKS
- nonce validation
- state validation
- issuer/client/deployment allowlist
- replay attack prevention
- audit logging for every failed launch
- secure secret/key storage
- HTTPS-only in all environments beyond local dev

Do not trust any unsigned or partially validated launch payload.

---

# Logging and Audit

Create structured audit logs for:

- unknown issuer
- invalid audience
- expired token
- nonce mismatch
- unsupported message type
- resource mapping failure
- user resolution fallback
- score sync failure

Suggested log fields:

- `platformId`
- `issuer`
- `clientId`
- `deploymentId`
- `userSub`
- `contextId`
- `resourceLinkId`
- `eventType`
- `status`
- `errorCode`

This will save a huge amount of time during FutureX or university integration.

---

# Admin Configuration Plan

Do not hardcode all platforms forever.

Recommended v1:

- config via database + seeded admin records
- manual creation through Prisma seed or protected internal script

Recommended later:

- internal admin UI to manage:
  - platform issuer
  - client ID
  - deployment ID
  - auth URL
  - token URL
  - JWKS URL
  - active/inactive status

---

# Step-by-Step Implementation Plan

## Step 1 — Introduce the LTI module skeleton

Create the directory structure and services:

- `/lib/lti/types.ts`
- `/lib/lti/constants.ts`
- `/server/lti/platform-service.ts`
- `/server/lti/launch-service.ts`
- `/server/lti/user-resolution-service.ts`
- `/server/lti/claim-validator.ts`
- `/server/lti/audit-service.ts`

Goal:

- isolate LTI logic from the start

---

## Step 2 — Add the database schema

Create Prisma models for:

- `LtiPlatform`
- `LtiLaunch`
- `LtiUserLink`
- `LtiResourceLink`
- optional `LtiLineItem`

Goal:

- establish the integration boundary cleanly

Deliverable:

- migration created and applied
- indexes/uniques added
- seed script for one test LMS platform

---

## Step 3 — Implement platform registration lookup

Create `LtiPlatformService` with methods like:

- `findByIssuerAndClientId`
- `findByIssuer`
- `assertDeploymentAllowed`

Goal:

- validate that launches only come from known platforms

---

## Step 4 — Implement OIDC login initiation endpoint

Build `GET /api/lti/login`

Tasks:

- validate incoming platform/client
- generate `state` and `nonce`
- persist them temporarily
- redirect to LMS auth endpoint

Goal:

- complete the first half of the LTI 1.3 login flow

---

## Step 5 — Implement JWKS fetch and cache

Create helper to fetch platform public keys from `jwksUrl`.

Tasks:

- fetch JWKS
- cache by `kid`
- refresh on expiry/miss
- validate token signatures using matching key

Goal:

- robust JWT verification

---

## Step 6 — Implement launch endpoint

Build `POST /api/lti/launch`

Tasks:

- parse `id_token`
- validate JWT signature
- validate standard claims
- validate nonce/state
- normalize claims into internal DTO
- persist `LtiLaunch`

Goal:

- accept only trusted, valid LTI launches

---

## Step 7 — Build claim normalization

Create a normalized launch object, for example:

```ts
type NormalizedLtiLaunch = {
  platformId: string;
  deploymentId: string;
  messageType: string;
  user: {
    sub: string;
    email?: string | null;
    givenName?: string | null;
    familyName?: string | null;
  };
  context?: {
    id?: string | null;
    title?: string | null;
  };
  resource?: {
    resourceLinkId?: string | null;
    targetLinkUri?: string | null;
  };
  roles: string[];
};
```

Goal:

- avoid spreading raw claim access throughout the codebase

---

## Step 8 — Implement user resolution

Create `LtiUserResolutionService`.

Tasks:

- resolve by existing `LtiUserLink`
- fallback to email
- create local Experts user if needed
- upsert mapping

Goal:

- stable external-to-local identity linkage

---

## Step 9 — Implement resource resolution

Create `LtiResourceResolver`.

Tasks:

- map `resource_link.id` + `context.id` to internal resource
- support course/lesson launch
- fail gracefully if not mapped

Goal:

- route learners to the correct Experts page

---

## Step 10 — Create Experts session after launch

After validation and mapping:

- create auth session
- attach short-lived launch context
- redirect to resolved page

Goal:

- user lands inside Experts already authenticated

---

## Step 11 — Add learner enrollment behavior

Define v1 policy:

Option A:

- launch only if already enrolled

Option B:

- auto-enroll if allowed for that LTI platform/context

Recommended:

- support configurable behavior per platform

Goal:

- avoid accidental unauthorized course access

---

## Step 12 — Add instructor/role-aware behavior

Use role mapping to decide:

- learner access
- instructor preview access
- content management restrictions

Goal:

- keep permissions predictable and safe

---

## Step 13 — Add failure pages and diagnostics

Create clear internal pages for:

- invalid launch
- unknown platform
- unmapped resource
- inactive deployment
- unsupported message type

Goal:

- easier debugging for integrators and internal team

---

## Step 14 — Add AGS foundation

Add `LtiLineItem` model and service scaffolding.

Tasks:

- store line item metadata
- prepare token acquisition
- define outbound score DTOs

Goal:

- prepare for score passback without coupling it too early

---

## Step 15 — Implement score sync

On supported graded activities:

- calculate normalized score
- call AGS endpoint
- store response/audit result
- retry failed syncs

Goal:

- complete the bidirectional integration loop

---

## Step 16 — Add test harness and sandbox platform

Prepare one known working LMS integration target.

Best options:

- Moodle test instance
- Canvas dev instance
- FutureX sandbox later if available

Goal:

- have a repeatable real integration environment

---

## Step 17 — Add admin/internal tooling

Build internal tools to:

- inspect launches
- inspect user links
- inspect platform config
- re-run grade sync manually
- test resource mappings

Goal:

- operational support without raw DB digging every time

---

## Step 18 — Optional deep linking support

Only after basic launch is stable.

Tasks:

- accept deep-link request
- render content picker
- return signed deep-link response

Goal:

- LMS instructors can embed Experts content directly

---

# API / DTO Changes

Do not directly expose raw LTI claims to the rest of the app.

Instead, use normalized DTOs:

- `NormalizedLtiLaunch`
- `ResolvedLtiUser`
- `ResolvedLtiResource`
- `LtiGradeSyncPayload`

This keeps the rest of Experts independent of LMS-specific details.

---

# Rollout Strategy

## Release 1

- schema
- platform config
- login initiation
- launch validation
- user mapping
- session creation
- manual resource mapping

## Release 2

- enrollment policies
- instructor role handling
- AGS score sync
- improved diagnostics

## Release 3

- deep linking
- NRPS
- admin UI
- institution self-service config

---

# Test Plan

## Unit tests

- issuer/client/deployment validation
- nonce/state validation
- JWT claim normalization
- user resolution logic
- role mapping logic
- resource resolution logic

## Integration tests

- successful login + launch flow
- launch with unknown issuer
- expired token
- invalid audience
- nonce mismatch
- missing resource mapping
- new user auto-creation
- existing user match via `LtiUserLink`

## AGS tests

- successful score sync
- retry on temporary failure
- invalid line item handling

## End-to-end tests

- Moodle/Canvas launch enters Experts correctly
- learner lands on expected lesson/course
- completion triggers grade sync

---

# Assumptions

- Experts remains the source of truth for its internal content and progression logic
- LTI is an interoperability layer, not a replacement for Experts auth model
- v1 supports launch into selected content, not full LMS parity
- email may be missing or unreliable, so `sub` must be primary
- LTI 1.3 only; no LTI 1.1 support
- FutureX or universities may require only a subset at first, especially launch + learner tracking

---

# Recommended Constraints

For v1, intentionally limit:

- one institution/platform config at a time if needed
- resource launch only, no deep linking
- learner role only, instructor later
- manual resource mapping
- no broad automatic role escalation
- no generic “map any route” behavior

This keeps the first implementation safer and much easier to validate.

---

# Suggested Deliverables for the LLM

Ask the LLM to complete the work in this order:

1. add Prisma models and migration
2. add LTI constants and claim types
3. build platform config service
4. implement login initiation route
5. implement JWKS fetch + signature validation
6. implement launch validation route
7. implement normalized claim parser
8. implement user linking
9. implement resource mapping
10. create session + redirect flow
11. add audit logging
12. add AGS scaffolding
13. add tests

---

# Final Recommendation

For Experts, the best path is:

- **start with LTI 1.3 launch only**
- keep it **modular and isolated**
- store **all external LMS identity/mapping in dedicated tables**
- add **AGS later**
- treat **FutureX integration as a future consumer of this module**

That way, you are not building “just for FutureX”; you are building a reusable **institution/LMS interoperability layer** for Experts.

If you want, I can turn this into a **copy-paste markdown spec file** in the exact style of your previous planning docs, or make it more concrete for **Next.js + Prisma + PostgreSQL** with proposed Prisma schema models and route skeletons.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
