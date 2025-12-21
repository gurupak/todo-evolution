# API Contracts - Phase II

**Feature**: Phase II - Full-Stack Web Application  
**Date**: 2025-12-19  
**Purpose**: Define all API contracts, schemas, and component interfaces

---

## Overview

This directory contains the complete API contract definitions for Phase II, organized by layer:

| File | Layer | Purpose |
|------|-------|---------|
| `models.md` | Data Layer | Pydantic schemas, SQLModel definitions, TypeScript types |
| `storage.md` | Storage Layer | Database operations, queries, repository patterns |
| `commands.md` | Business Logic | Service layer contracts, business rules |
| `display.md` | Presentation Layer | React component interfaces, props, events |

---

## Contract Philosophy

**Contracts Define Behavior, Not Implementation**

Each contract specifies:
- **Input**: What data goes in (parameters, request bodies)
- **Output**: What data comes out (return types, response bodies)
- **Errors**: What can go wrong (error codes, messages)
- **Side Effects**: What changes in the system (database updates, cache invalidation)

Contracts do NOT specify:
- Implementation details (algorithms, optimizations)
- Technology choices (already defined in plan.md)
- UI styling (handled by Tailwind/shadcn)

---

## API Endpoint Summary

### Task Endpoints

| Method | Endpoint | Request | Response | Auth | Purpose |
|--------|----------|---------|----------|------|---------|
| GET | `/api/{user_id}/tasks` | Query params | TaskListResponse | Required | List all user's tasks |
| POST | `/api/{user_id}/tasks` | TaskCreateRequest | TaskResponse | Required | Create new task |
| GET | `/api/{user_id}/tasks/{task_id}` | - | TaskResponse | Required | Get single task |
| PUT | `/api/{user_id}/tasks/{task_id}` | TaskUpdateRequest | TaskResponse | Required | Update task |
| DELETE | `/api/{user_id}/tasks/{task_id}` | - | DeleteResponse | Required | Delete task |
| PATCH | `/api/{user_id}/tasks/{task_id}/complete` | - | TaskResponse | Required | Toggle completion |

### Authentication Endpoints (Better Auth)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/signin` | Login user |
| POST | `/api/auth/signout` | Logout user |
| GET | `/api/auth/session` | Get current session |

*Note: Auth endpoints are handled by Better Auth and follow its contract specifications.*

---

## Status Codes

### Success Codes

| Code | Meaning | Used For |
|------|---------|----------|
| 200 | OK | Successful GET, PUT, PATCH, DELETE |
| 201 | Created | Successful POST (task creation) |

### Error Codes

| Code | Meaning | Used For |
|------|---------|----------|
| 400 | Bad Request | Validation errors (invalid input) |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | Valid token but insufficient permissions |
| 404 | Not Found | Task doesn't exist |
| 500 | Internal Server Error | Unexpected server errors |

---

## Error Response Format

All error responses follow this structure:

```typescript
interface ErrorResponse {
  detail: string;  // Human-readable error message
  errors?: Array<{
    field: string;  // Field name that failed validation
    message: string;  // Specific validation error
  }>;
}
```

**Examples**:

```json
// 400 Bad Request (Validation Error)
{
  "detail": "Validation error",
  "errors": [
    {"field": "title", "message": "Title is required"},
    {"field": "priority", "message": "Priority must be one of: high, medium, low"}
  ]
}

// 401 Unauthorized
{
  "detail": "Not authenticated"
}

// 403 Forbidden
{
  "detail": "Not authorized to access this resource"
}

// 404 Not Found
{
  "detail": "Task not found"
}

// 500 Internal Server Error
{
  "detail": "Internal server error"
}
```

---

## Authentication Flow

### 1. User Registration

```
Frontend                Better Auth              Database
   │                         │                      │
   │──── POST /auth/signup ──>│                      │
   │     {email, password}    │                      │
   │                          │──── INSERT user ────>│
   │                          │<──── user record ────│
   │                          │──── INSERT session ──>│
   │                          │<──── session + JWT ──│
   │<─── 200 {session, JWT} ──│                      │
```

### 2. User Login

```
Frontend                Better Auth              Database
   │                         │                      │
   │──── POST /auth/signin ──>│                      │
   │     {email, password}    │                      │
   │                          │──── SELECT user ────>│
   │                          │<──── user record ────│
   │                          │   (verify password)  │
   │                          │──── INSERT session ──>│
   │                          │<──── session + JWT ──│
   │<─── 200 {session, JWT} ──│                      │
```

### 3. Authenticated API Request

```
Frontend                FastAPI                 Database
   │                         │                      │
   │─── GET /api/user/tasks ─>│                      │
   │  Header: Bearer {JWT}    │                      │
   │                          │  (verify JWT)        │
   │                          │  (extract user_id)   │
   │                          │──── SELECT tasks ───>│
   │                          │<──── task records ───│
   │<───── 200 {tasks} ───────│                      │
```

---

## Data Flow Patterns

### Create Operation

```
Component → Hook → API Client → FastAPI Router → Service → Database
    │         │         │              │             │         │
    └─────────┴─────────┴──────────────┴─────────────┴─────────┘
                     Request Flow →
                     
    ┌─────────┬─────────┬──────────────┬─────────────┬─────────┐
    │         │         │              │             │         │
Component ← Hook ← API Client ← FastAPI Router ← Service ← Database
                     ← Response Flow
```

### Query Operation

```
Component → Hook (cache check)
    │            │
    └────────────┴─── Cache Hit → Return cached data
                 │
                 └─── Cache Miss → API Request → Database
```

---

## Contract Versioning

**Phase II**: All contracts are version 1.0 (implicit)

Future phases may introduce:
- API versioning via URL (`/api/v2/...`)
- Schema versioning via headers (`Accept: application/vnd.api+json; version=2`)
- Backward compatibility requirements

---

## Testing Contracts

Each contract file includes test specifications:

1. **models.md**: Schema validation tests
2. **storage.md**: Database operation tests
3. **commands.md**: Business logic tests
4. **display.md**: Component rendering tests

All tests follow the pattern:
```
Given [precondition]
When [action]
Then [expected outcome]
```

---

## Next Steps

After reading this overview:

1. Read `models.md` for data schema definitions
2. Read `storage.md` for database operation contracts
3. Read `commands.md` for business logic contracts
4. Read `display.md` for UI component contracts
5. Refer to `plan.md` for implementation sequence

---

## Contract Change Process

**Important**: Contracts define the specification. If generated code doesn't match:

1. ❌ Do NOT edit the generated code manually
2. ✅ DO update the contract specification
3. ✅ DO re-run `/sp.implement` to regenerate code

This ensures the specification remains the single source of truth.
