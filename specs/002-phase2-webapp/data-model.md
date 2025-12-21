# Phase II Data Model

**Feature**: Phase II - Full-Stack Web Application  
**Date**: 2025-12-19  
**Purpose**: Define all entities, relationships, and database schema

---

## Overview

Phase II introduces persistent storage with PostgreSQL, managed by two systems:
- **Better Auth**: Manages user authentication tables (user, session, account)
- **FastAPI**: Manages application data tables (task)

Both systems share the same Neon PostgreSQL database but have separate responsibilities.

---

## Entity Relationship Diagram

```
┌─────────────────┐
│      User       │ (Better Auth)
│─────────────────│
│ id: UUID (PK)   │
│ email: VARCHAR  │◄────┐
│ name: VARCHAR   │     │
│ emailVerified:  │     │
│   BOOLEAN       │     │
│ image: VARCHAR? │     │
│ createdAt: TS   │     │
│ updatedAt: TS   │     │
└─────────────────┘     │
         │              │
         │              │
         │ 1:N          │ N:1
         ▼              │
┌─────────────────┐     │
│    Session      │     │
│─────────────────│     │
│ id: UUID (PK)   │     │
│ userId: UUID FK ├─────┘
│ token: VARCHAR  │
│ expiresAt: TS   │
│ createdAt: TS   │
│ updatedAt: TS   │
└─────────────────┘

┌─────────────────┐
│      Task       │ (FastAPI)
│─────────────────│
│ id: UUID (PK)   │
│ userId: UUID FK ├─────┐
│ title: VARCHAR  │     │
│ description: V? │     │ N:1
│ priority: ENUM  │     │
│ isCompleted: B  │     │
│ createdAt: TS   │     │
│ updatedAt: TS   │     │
│ completedAt: TS?│     │
└─────────────────┘     │
                        │
                        ▼
              ┌─────────────────┐
              │      User       │
              └─────────────────┘
```

---

## Entity Definitions

### 1. User (Managed by Better Auth)

**Purpose**: Represents a registered user account with authentication credentials.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique user identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User's email address (login identifier) |
| `name` | VARCHAR(100) | NOT NULL | User's display name |
| `emailVerified` | BOOLEAN | NOT NULL, DEFAULT false | Email verification status (Phase III+) |
| `image` | VARCHAR(500) | NULLABLE | Profile image URL (optional) |
| `createdAt` | TIMESTAMP | NOT NULL, DEFAULT now() | Account creation timestamp |
| `updatedAt` | TIMESTAMP | NOT NULL, DEFAULT now() | Last update timestamp |

**Validation Rules** (from spec FR-001, FR-002, FR-003):
- Email must be valid format (RFC 5322)
- Email must be unique (enforced by database constraint)
- Name must be 1-100 characters
- Password minimum 8 characters (hashed with bcrypt, stored in Better Auth's internal tables)

**Indexes**:
```sql
CREATE UNIQUE INDEX idx_user_email ON "user"(email);
CREATE INDEX idx_user_created_at ON "user"(createdAt);
```

**Managed By**: Better Auth (automatically created during setup)

---

### 2. Session (Managed by Better Auth)

**Purpose**: Represents an authenticated user session with JWT token.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique session identifier |
| `userId` | UUID | FOREIGN KEY (user.id), NOT NULL, ON DELETE CASCADE | Reference to user |
| `token` | VARCHAR(500) | NOT NULL | JWT token string |
| `expiresAt` | TIMESTAMP | NOT NULL | Token expiration time (24 hours from creation) |
| `createdAt` | TIMESTAMP | NOT NULL, DEFAULT now() | Session creation timestamp |
| `updatedAt` | TIMESTAMP | NOT NULL, DEFAULT now() | Last update timestamp |

**Validation Rules** (from clarifications):
- Token expires after 24 hours
- Token contains claims: `sub` (userId), `email`, `iss`, `exp`, `iat`
- Token signed with `BETTER_AUTH_SECRET` using HS256

**Indexes**:
```sql
CREATE INDEX idx_session_user_id ON "session"(userId);
CREATE INDEX idx_session_token ON "session"(token);
CREATE INDEX idx_session_expires_at ON "session"(expiresAt);
```

**Managed By**: Better Auth (automatically created during setup)

---

### 3. Task (Managed by FastAPI)

**Purpose**: Represents a todo item with title, description, priority, and completion status.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique task identifier |
| `user_id` | UUID | FOREIGN KEY (user.id), NOT NULL, ON DELETE CASCADE | Owner of the task |
| `title` | VARCHAR(200) | NOT NULL | Task title |
| `description` | VARCHAR(1000) | NOT NULL, DEFAULT '' | Task description |
| `priority` | priority_enum | NOT NULL, DEFAULT 'medium' | Task priority (high/medium/low) |
| `is_completed` | BOOLEAN | NOT NULL, DEFAULT false | Completion status |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT now() | Task creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT now() | Last update timestamp |
| `completed_at` | TIMESTAMP | NULLABLE | Completion timestamp (set when is_completed becomes true) |

**Validation Rules** (from spec FR-010 to FR-022):
- Title: Required, 1-200 characters, trimmed whitespace
- Description: Optional, max 1000 characters, trimmed whitespace, defaults to empty string
- Priority: Must be one of 'high', 'medium', 'low'; defaults to 'medium'
- is_completed: Boolean, defaults to false
- completed_at: Set automatically when is_completed changes to true, cleared when set to false
- updated_at: Automatically updated on any field change (database trigger)

**Indexes**:
```sql
CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_created_at ON task(created_at DESC);
CREATE INDEX idx_task_is_completed ON task(is_completed);
CREATE INDEX idx_task_user_completed ON task(user_id, is_completed);
```

**Index Rationale**:
- `idx_task_user_id`: Primary filter (all queries filter by user_id)
- `idx_task_created_at`: Default sort order (newest first)
- `idx_task_is_completed`: Filter completed vs pending tasks
- `idx_task_user_completed`: Composite index for user's task stats query

**Managed By**: FastAPI (created via Alembic migration)

---

## Custom Types

### Priority Enum

```sql
CREATE TYPE priority_enum AS ENUM ('high', 'medium', 'low');
```

**Purpose**: Enforce valid priority values at database level.

**Values**:
- `high`: Urgent/important tasks (displayed with red badge)
- `medium`: Normal priority tasks (displayed with yellow badge, default)
- `low`: Low priority tasks (displayed with green badge)

---

## Relationships

### User ↔ Task (One-to-Many)

**Relationship**: One user can have many tasks, each task belongs to exactly one user.

**Enforcement**:
```sql
ALTER TABLE task
  ADD CONSTRAINT fk_task_user
  FOREIGN KEY (user_id)
  REFERENCES "user"(id)
  ON DELETE CASCADE;
```

**Business Rules**:
- User can only access their own tasks (enforced in FastAPI service layer)
- Deleting a user deletes all their tasks (CASCADE)
- Task creation requires valid user_id from JWT token

### User ↔ Session (One-to-Many)

**Relationship**: One user can have multiple active sessions (different devices).

**Enforcement**:
```sql
ALTER TABLE "session"
  ADD CONSTRAINT fk_session_user
  FOREIGN KEY (userId)
  REFERENCES "user"(id)
  ON DELETE CASCADE;
```

**Business Rules**:
- Deleting a user deletes all their sessions (CASCADE)
- Sessions expire after 24 hours
- Better Auth handles session cleanup automatically

---

## State Transitions

### Task Completion Lifecycle

```
┌─────────────┐
│   Created   │ (is_completed = false, completed_at = NULL)
└──────┬──────┘
       │
       │ PATCH /tasks/{id}/complete
       ▼
┌─────────────┐
│  Completed  │ (is_completed = true, completed_at = now())
└──────┬──────┘
       │
       │ PATCH /tasks/{id}/complete (toggle)
       ▼
┌─────────────┐
│   Active    │ (is_completed = false, completed_at = NULL)
└─────────────┘
```

**Transition Rules**:
1. When `is_completed` changes from `false` to `true`:
   - Set `completed_at = now()`
   - Set `updated_at = now()`
   
2. When `is_completed` changes from `true` to `false`:
   - Set `completed_at = NULL`
   - Set `updated_at = now()`

3. When task is updated (title, description, priority):
   - Set `updated_at = now()`
   - Do NOT change `is_completed` or `completed_at`

---

## Database Schema (DDL)

### Task Table

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create priority enum
CREATE TYPE priority_enum AS ENUM ('high', 'medium', 'low');

-- Create task table
CREATE TABLE task (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000) NOT NULL DEFAULT '',
    priority priority_enum NOT NULL DEFAULT 'medium',
    is_completed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
    completed_at TIMESTAMP,
    
    CONSTRAINT fk_task_user
        FOREIGN KEY (user_id)
        REFERENCES "user"(id)
        ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_created_at ON task(created_at DESC);
CREATE INDEX idx_task_is_completed ON task(is_completed);
CREATE INDEX idx_task_user_completed ON task(user_id, is_completed);

-- Create trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_task_updated_at
    BEFORE UPDATE ON task
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create trigger for completed_at
CREATE OR REPLACE FUNCTION update_completed_at_column()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_completed = true AND OLD.is_completed = false THEN
        NEW.completed_at = now();
    ELSIF NEW.is_completed = false AND OLD.is_completed = true THEN
        NEW.completed_at = NULL;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_task_completed_at
    BEFORE UPDATE ON task
    FOR EACH ROW
    EXECUTE FUNCTION update_completed_at_column();
```

---

## SQLModel Definition (Python)

```python
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class PriorityEnum(str, Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task(SQLModel, table=True):
    """Task model for persistent storage."""
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    class Config:
        """SQLModel configuration."""
        use_enum_values = True  # Store enum as string
```

---

## TypeScript Types (Frontend)

```typescript
export enum Priority {
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low',
}

export interface Task {
  id: string;  // UUID
  user_id: string;  // UUID
  title: string;
  description: string;
  priority: Priority;
  is_completed: boolean;
  created_at: string;  // ISO 8601
  updated_at: string;  // ISO 8601
  completed_at: string | null;  // ISO 8601 or null
}

export interface User {
  id: string;  // UUID
  email: string;
  name: string;
  emailVerified: boolean;
  image?: string;
  createdAt: string;
  updatedAt: string;
}

export interface Session {
  user: User;
  session: {
    token: string;
    expiresAt: string;
  };
}
```

---

## Data Volume Estimates

**Phase II Scale** (from spec assumptions):
- **Users**: ~1,000 users
- **Tasks per user**: ~100 tasks average
- **Total tasks**: ~100,000 tasks
- **Sessions**: ~500 active sessions (concurrent users)

**Storage Estimates**:
- User record: ~300 bytes
- Task record: ~500 bytes
- Session record: ~700 bytes

**Total Storage**:
- Users: 1,000 × 300 bytes = 0.3 MB
- Tasks: 100,000 × 500 bytes = 50 MB
- Sessions: 500 × 700 bytes = 0.35 MB
- **Total: ~51 MB** (well within Neon free tier: 10 GB)

**Query Performance Targets** (from spec SC-004):
- List 100 tasks: <2 seconds
- Single task fetch: <500ms
- Create/update/delete: <1 second

---

## Migration Strategy

### Initial Migration (Alembic)

```python
# alembic/versions/001_create_task_table.py
"""Create task table

Revision ID: 001
Create Date: 2025-12-19
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Create enum
    op.execute("CREATE TYPE priority_enum AS ENUM ('high', 'medium', 'low')")
    
    # Create table
    op.create_table(
        'task',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.String(1000), nullable=False, server_default=''),
        sa.Column('priority', sa.Enum('high', 'medium', 'low', name='priority_enum'), 
                  nullable=False, server_default='medium'),
        sa.Column('is_completed', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column('completed_at', sa.TIMESTAMP, nullable=True),
    )
    
    # Create foreign key
    op.create_foreign_key(
        'fk_task_user',
        'task', 'user',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )
    
    # Create indexes
    op.create_index('idx_task_user_id', 'task', ['user_id'])
    op.create_index('idx_task_created_at', 'task', ['created_at'], postgresql_ops={'created_at': 'DESC'})
    op.create_index('idx_task_is_completed', 'task', ['is_completed'])
    op.create_index('idx_task_user_completed', 'task', ['user_id', 'is_completed'])

def downgrade():
    op.drop_table('task')
    op.execute('DROP TYPE priority_enum')
```

---

## Data Integrity Rules

### Referential Integrity

1. **Task → User**:
   - Every task MUST have a valid user_id
   - Foreign key constraint enforces this at database level
   - CASCADE delete: deleting user deletes all their tasks

2. **Session → User**:
   - Every session MUST have a valid userId
   - Managed by Better Auth automatically

### Data Validation

1. **Application Level** (FastAPI):
   - Pydantic schemas validate all inputs before database operations
   - SQLModel enforces field types and constraints
   - Business logic in service layer validates user ownership

2. **Database Level**:
   - NOT NULL constraints prevent missing required fields
   - UNIQUE constraint on user.email prevents duplicate accounts
   - ENUM constraint on task.priority enforces valid values
   - CHECK constraints (if needed) for additional validation

### Concurrency Control

**Strategy**: Last-write-wins (from clarifications)

- No optimistic locking (no version field)
- No pessimistic locking (no row-level locks)
- `updated_at` timestamp shows when last modification occurred
- Database triggers ensure timestamp accuracy

**Rationale**: Acceptable for single-user editing own tasks (no collaboration in Phase II)

---

## Summary

**Total Tables**: 4
- `user` (Better Auth)
- `session` (Better Auth)
- `account` (Better Auth, for future OAuth)
- `task` (FastAPI)

**Total Custom Types**: 1
- `priority_enum`

**Total Indexes**: 9
- 3 on user (email, id, created_at)
- 3 on session (userId, token, expiresAt)
- 4 on task (user_id, created_at, is_completed, composite)

**Total Relationships**: 2
- User → Task (1:N)
- User → Session (1:N)

All definitions align with the specification's functional requirements (FR-001 to FR-047) and support the measurable success criteria (SC-001 to SC-010).
