---
title: "Backend Integration Summary: Authentication, Users & Organizations"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/backend-integration-summary"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Backend Integration Summary: Authentication, Users & Organizations

## Overview

This document outlines the comprehensive integration between the Authentication, Users, and Organizations domains in the Experts API backend. The system has been designed with a domain-driven architecture that provides robust user management, organization membership, and role-based access control.

## Architecture Overview

### Domain Structure

```
app/Domains/
├── Users/
│   ├── Controllers/
│   │   ├── UserController.php
│   │   └── PlanController.php
│   ├── Models/
│   │   ├── User.php
│   │   ├── UserEntitlement.php
│   │   ├── Plan.php
│   │   ├── Role.php
│   │   └── Permission.php
│   └── Resources/
│       ├── UserResource.php
│       └── PlanResource.php
└── Organizations/
    ├── Controllers/
    │   └── OrganizationController.php
    ├── Models/
    │   └── Organization.php
    └── Resources/
        └── OrganizationResource.php
```

## Key Features Implemented

### 1. Enhanced User Model

The `User` model has been extended with comprehensive organization management capabilities:

**New Relationships:**

- `organizationMemberships()` - All user's organization memberships
- `activeOrganizationMemberships()` - Only active memberships
- `entitlement()` - User's plan entitlement
- `courses()` - User's courses (for instructors)

**New Methods:**

- `joinOrganization($organizationId, $role, $permissions)` - Join an organization with specified role
- `leaveOrganization($organizationId)` - Leave an organization
- `getRoleInOrganization($organizationId)` - Get user's role in specific organization
- `hasPermissionInOrganization($organizationId, $permission)` - Check permissions in organization
- `isOrganizationMember($organizationId)` - Check membership status

### 2. Comprehensive API Routes

#### Authentication Routes (`/v1/auth.php`)

- `POST /login` - User authentication with token generation
- `POST /register` - User registration with role assignment
- `POST /logout` - Token revocation and logout
- `POST /forgot-password` - Password reset initiation
- `POST /reset-password` - Password reset completion
- Email verification endpoints

#### User Management Routes (`/v1/users/`)

- `GET /` - List all users (permission: view users)
- `POST /` - Create new user (permission: create users)
- `GET /{user}` - Get user profile
- `PUT /{user}` - Update user (permission: edit users)
- `DELETE /{user}` - Delete user (permission: delete users)

#### Organization Management Routes (`/v1/organizations/`)

- `GET /` - List organizations (public)
- `GET /{organization}` - View organization details (public)
- `POST /` - Create organization (authenticated)
- `PUT /{organization}` - Update organization (owner/admin)
- `DELETE /{organization}` - Delete organization (owner)

#### Organization Membership Routes

- `GET /users/{user}/organization-memberships` - User's memberships
- `POST /users/{user}/organization-memberships` - Join organization
- `PUT /users/{user}/organization-memberships/{membership}` - Update membership
- `DELETE /users/{user}/organization-memberships/{membership}` - Leave organization

#### Organization Member Management Routes

- `GET /organizations/{organization}/members` - List organization members
- `POST /organizations/{organization}/members/invite` - Invite user to organization
- `DELETE /organizations/{organization}/members/{membership}` - Remove member

#### Plan Management Routes (`/v1/plans/`)

- `GET /` - List available plans
- `GET /comparison` - Plan comparison data
- `GET /recommendations` - Personalized plan recommendations
- `GET /current` - Current user's plan and usage
- `GET /{slug}` - Specific plan details
- `POST /assign` - Assign plan to user
- `POST /upgrade` - Upgrade user plan
- `POST /downgrade` - Downgrade user plan

### 3. Advanced Features

#### Role-Based Access Control

- Spatie permissions integration
- Organization-specific roles (student, instructor, admin)
- Permission inheritance and management
- Route-level permission middleware

#### Plan Management System

- Flexible plan structure with limits and features
- Usage tracking and enforcement
- Automatic plan recommendations
- Upgrade/downgrade workflows with data validation

#### Organization Membership System

- Multi-organization support for users
- Role-based permissions within organizations
- Membership lifecycle management (join, leave, change role)
- Organization-specific permission checks

## Database Relationships

### User-Organization Relationship

```sql
OrganizationMembership:
- user_id (UUID, references users.uuid)
- organization_id (UUID, references users.uuid for organization accounts)
- role_in_org (enum: student, instructor, admin)
- permissions (JSON array)
- is_active (boolean)
- joined_at, left_at (timestamps)
```

### User-Plan Relationship

```sql
UserEntitlement:
- user_id (UUID, references users.uuid)
- plan_type (string, references plans.slug)
- course_limit, student_limit (integers, nullable for unlimited)
- features (JSON array)
- expires_at (timestamp, nullable for lifetime plans)
```

## Authentication Flow

### Registration Process

1. User submits registration data
2. AuthController validates and creates user
3. User assigned default 'user' role
4. API token generated with 'student' scope
5. UserResource returned with user data and token

### Login Process

1. Credentials validated against database
2. API token created with appropriate scopes
3. User loaded with roles, permissions, and relationships
4. Comprehensive user data returned

### Organization Creation

1. User can create organization during registration or separately
2. Organization owner automatically gets 'admin' role
3. Organization-specific permissions assigned
4. Membership record created linking user to organization

## Security Considerations

### Authentication

- Laravel Passport for OAuth2 token management
- Rate limiting on authentication endpoints (10 requests/minute)
- Secure token revocation on logout

### Authorization

- Role-based access control using Spatie permissions
- Organization-specific permission checks
- Route-level middleware protection
- UUID-based model binding for security

### Data Protection

- Password hashing with bcrypt
- Email verification workflow
- Secure file upload through Vault system
- Input validation and sanitization

## API Response Format

All API responses follow a consistent format:

```json
{
  "status": "success|error",
  "data": { ... },
  "message": "Human readable message",
  "meta": { ... } // For paginated responses
}
```

## Testing Support

The system includes comprehensive test coverage:

- Authentication tests (login, logout, registration)
- Permission-based access tests
- Organization membership workflow tests
- Plan management tests

## Usage Examples

### Creating an Organization

```bash
POST /v1/organizations
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Tech Academy",
  "description": "A leading technology education provider",
  "type": "academy",
  "website": "https://techacademy.com"
}
```

### Joining an Organization

```bash
POST /v1/users/{user_uuid}/organization-memberships
Authorization: Bearer {token}
Content-Type: application/json

{
  "organization_id": "org-uuid",
  "role": "student",
  "permissions": ["view_courses", "enroll_in_courses"]
}
```

### Checking Current User

```bash
GET /v1/user
Authorization: Bearer {token}

# Returns user with roles, permissions, entitlements, and organization memberships
```

## Future Enhancements

### Planned Features

1. Multi-tenancy support for organizations
2. Advanced analytics and reporting
3. Integration with payment systems for plan billing
4. Advanced permission granularity
5. Organization-specific branding and customization

### API Versioning

The current implementation uses `/v1/` prefix for all routes, allowing for future API versioning without breaking existing integrations.

## Conclusion

This backend integration provides a robust foundation for a multi-tenant educational platform with sophisticated user management, organization hierarchies, and flexible plan structures. The domain-driven architecture ensures maintainability and scalability while the comprehensive API coverage supports diverse frontend applications and third-party integrations.
