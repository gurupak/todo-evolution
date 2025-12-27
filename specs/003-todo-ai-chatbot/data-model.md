# Data Model: Todo AI Chatbot

**Feature**: 003-todo-ai-chatbot  
**Date**: 2025-12-25  
**Status**: Phase 1 Design

---

## Overview

Phase III extends the Phase II database schema with two new tables to support conversational AI chat functionality. The existing `task` and `user` tables remain unchanged. All new tables integrate with existing user authentication and maintain strict user data isolation.

---

## Entity Relationship Diagram

```
┌─────────────────┐
│      User       │ (existing from Phase II)
│─────────────────│
│ id (PK)         │
│ email           │
│ ...             │
└────────┬────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────────────┐
│    Conversation         │ (NEW)
│─────────────────────────│
│ id (PK)                 │
│ user_id (FK → User)     │
│ created_at              │
│ updated_at              │
└───────────┬─────────────┘
            │
            │ 1:N
            │
            ▼
┌─────────────────────────────────┐
│         Message                 │ (NEW)
│─────────────────────────────────│
│ id (PK)                         │
│ conversation_id (FK → Convo)    │
│ user_id (FK → User)             │
│ role (user | assistant)         │
│ content (text)                  │
│ tool_calls (JSON, nullable)     │
│ created_at                      │
└─────────────────────────────────┘

         ┌─────────────────┐
         │      Task       │ (existing from Phase II)
         │─────────────────│
         │ id (PK)         │
         │ user_id (FK)    │
         │ title           │
         │ ...             │
         └─────────────────┘
         (modified by MCP tools, no direct FK to message)
```

---

## New Entities

### 1. Conversation

Represents a chat session between a user and the AI assistant. Each conversation contains an ordered sequence of messages.

**Purpose**: Group related messages together, enable conversation resumption, support multi-conversation history.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL, Default: uuid4() | Unique identifier |
| user_id | UUID | FK (user.id), NOT NULL, Index | Owner of conversation |
| created_at | TIMESTAMP | NOT NULL, Default: now() | When conversation started |
| updated_at | TIMESTAMP | NOT NULL, Default: now() | Last message timestamp |

**Indexes**:
- Primary: `id`
- Foreign Key: `user_id → user.id` (ON DELETE CASCADE)
- Query Index: `(user_id, updated_at DESC)` for "recent conversations" query

**Validation Rules**:
- `user_id` must exist in user table
- `updated_at` >= `created_at`
- Soft delete: Not implemented in Phase III (delete removes all messages via CASCADE)

**State Transitions**: None (conversations don't have status)

**Example**:
```python
from sqlmodel import Field, SQLModel
from datetime import datetime
from uuid import UUID, uuid4

class Conversation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

---

### 2. Message

Represents a single message within a conversation. Messages alternate between user and assistant, maintaining full dialogue history.

**Purpose**: Store conversation history for context loading, display message history in UI, enable conversation resumption.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL, Default: uuid4() | Unique identifier |
| conversation_id | UUID | FK (conversation.id), NOT NULL, Index | Parent conversation |
| user_id | UUID | FK (user.id), NOT NULL | Message owner (for isolation) |
| role | VARCHAR(20) | NOT NULL, CHECK IN ('user', 'assistant') | Message sender |
| content | TEXT | NOT NULL | Message text content |
| tool_calls | JSONB | NULLABLE | AI tool invocations (assistant only) |
| created_at | TIMESTAMP | NOT NULL, Default: now() | Message timestamp |

**Indexes**:
- Primary: `id`
- Foreign Keys:
  - `conversation_id → conversation.id` (ON DELETE CASCADE)
  - `user_id → user.id` (ON DELETE CASCADE)
- Query Index: `(conversation_id, created_at ASC)` for chronological message loading

**Validation Rules**:
- `role` must be exactly "user" or "assistant"
- `content` must not be empty string
- `tool_calls` only allowed when `role = 'assistant'` (application-level validation)
- `user_id` must match `conversation.user_id` (application-level validation for data integrity)

**Content Constraints**:
- Maximum content length: 2000 characters (validated at API level)
- tool_calls format: Array of `{tool_name: str, arguments: dict, result: any}`

**Example**:
```python
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import JSON
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversation.id", nullable=False, index=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    role: str = Field(nullable=False, max_length=20)  # 'user' or 'assistant'
    content: str = Field(nullable=False, sa_column=Column("content", sqlalchemy.Text))
    tool_calls: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    class Config:
        validate_assignment = True
```

**tool_calls JSON Structure** (when present):
```json
[
  {
    "tool": "add_task",
    "arguments": {
      "user_id": "uuid-here",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread"
    },
    "result": {
      "success": true,
      "task": { "id": "task-uuid", "title": "Buy groceries", ... }
    }
  }
]
```

---

## Existing Entities (No Changes)

### Task (from Phase II)

**No modifications required**. MCP tools operate on existing task table.

**Current Fields**:
- id: UUID (PK)
- user_id: UUID (FK)
- title: VARCHAR
- description: TEXT (nullable)
- is_completed: BOOLEAN
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

**Usage in Phase III**: MCP tools create/read/update/delete tasks. No direct foreign key to message table (indirect relationship through user_id).

### User (from Phase II)

**No modifications required**. Existing Better Auth user table.

**Current Fields**: As defined by Better Auth schema

**Usage in Phase III**: JWT authentication validates user_id, which is passed to MCP tools and stored in conversation/message tables.

---

## Database Migration

**Alembic Migration File**: `add_conversation_tables`

**Up Migration**:
```sql
-- Create conversation table
CREATE TABLE conversation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_conversation_user_updated 
    ON conversation(user_id, updated_at DESC);

-- Create message table
CREATE TABLE message (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    tool_calls JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT message_content_not_empty CHECK (length(content) > 0)
);

CREATE INDEX idx_message_conversation_created 
    ON message(conversation_id, created_at ASC);
```

**Down Migration**:
```sql
DROP TABLE IF EXISTS message CASCADE;
DROP TABLE IF EXISTS conversation CASCADE;
```

---

## Query Patterns

### 1. Create New Conversation

```sql
INSERT INTO conversation (user_id) 
VALUES (:user_id) 
RETURNING id, created_at, updated_at;
```

### 2. Load Conversation History

```sql
SELECT id, role, content, tool_calls, created_at 
FROM message 
WHERE conversation_id = :conversation_id 
  AND user_id = :user_id  -- security: verify ownership
ORDER BY created_at ASC
LIMIT 50;  -- pagination
```

### 3. Save User Message

```sql
INSERT INTO message (conversation_id, user_id, role, content) 
VALUES (:conversation_id, :user_id, 'user', :content) 
RETURNING id, created_at;

-- Update conversation timestamp
UPDATE conversation 
SET updated_at = NOW() 
WHERE id = :conversation_id;
```

### 4. Save Assistant Message with Tool Calls

```sql
INSERT INTO message (conversation_id, user_id, role, content, tool_calls) 
VALUES (:conversation_id, :user_id, 'assistant', :content, :tool_calls::jsonb) 
RETURNING id, created_at;

UPDATE conversation 
SET updated_at = NOW() 
WHERE id = :conversation_id;
```

### 5. List User's Conversations (Most Recent First)

```sql
SELECT c.id, c.created_at, c.updated_at,
       (SELECT content FROM message 
        WHERE conversation_id = c.id 
        ORDER BY created_at DESC 
        LIMIT 1) AS last_message
FROM conversation c
WHERE c.user_id = :user_id
ORDER BY c.updated_at DESC
LIMIT 20;
```

### 6. Delete Conversation (with CASCADE)

```sql
DELETE FROM conversation 
WHERE id = :conversation_id 
  AND user_id = :user_id;  -- security: verify ownership
-- CASCADE automatically deletes all messages
```

---

## Data Integrity Rules

### User Isolation
- Every query MUST filter by `user_id` from JWT
- User can only access conversations where `conversation.user_id = authenticated_user_id`
- User can only access messages where `message.user_id = authenticated_user_id`
- MCP tools receive `user_id` parameter and filter tasks accordingly

### Referential Integrity
- CASCADE deletes: Deleting conversation deletes all messages
- CASCADE deletes: Deleting user deletes all conversations and messages
- Foreign key constraints enforced at database level

### Temporal Integrity
- `message.created_at` is immutable (no updates)
- `conversation.updated_at` = max(message.created_at) for that conversation
- Messages ordered by `created_at ASC` for chronological display

### Content Integrity
- `content` cannot be empty string (CHECK constraint)
- `role` must be 'user' or 'assistant' (CHECK constraint)
- `tool_calls` only present for assistant messages (application-level)

---

## Token Counting and Truncation

**Problem**: Conversation history may exceed model context window (e.g., 8000 tokens).

**Solution**: Truncate oldest messages when loading history.

**Algorithm**:
```python
def load_conversation_with_truncation(conversation_id: str, user_id: str, max_tokens: int = 8000):
    # Load all messages
    messages = db.query(Message)\
        .filter(Message.conversation_id == conversation_id)\
        .filter(Message.user_id == user_id)\
        .order_by(Message.created_at.asc())\
        .all()
    
    # Count tokens (using tiktoken or similar)
    total_tokens = sum(count_tokens(msg.content) for msg in messages)
    
    # Truncate from beginning if over limit
    while total_tokens > max_tokens and len(messages) > 1:
        removed = messages.pop(0)
        total_tokens -= count_tokens(removed.content)
    
    return messages
```

**Future Enhancement**: Generate conversation summary for truncated messages.

---

## Scalability Considerations

### Pagination
- Load messages in batches (50 messages per page)
- Frontend requests older messages with `offset` parameter
- Index on `(conversation_id, created_at)` ensures fast pagination

### Archival
- Conversations older than 90 days could be archived (future feature)
- Archive table: `conversation_archive`, `message_archive`

### Cleanup
- Cron job to delete empty conversations (no messages)
- Soft delete option for user-requested conversation deletion

---

## Security Considerations

### SQL Injection Prevention
- Use parameterized queries (SQLModel/SQLAlchemy handles this)
- Never construct SQL with string interpolation

### User Data Isolation
- Always filter by `user_id` from JWT
- Verify `conversation.user_id == jwt.user_id` before loading messages
- Verify `message.user_id == jwt.user_id` when accessing individual messages

### Content Sanitization
- Validate message content length (<= 2000 chars) at API level
- Escape HTML in content when displaying in UI
- tool_calls JSON validated against schema before storage

---

## Testing Strategy

### Unit Tests
- Test Conversation model creation with valid/invalid user_id
- Test Message model with valid/invalid role values
- Test content length validation
- Test tool_calls JSON schema validation

### Integration Tests
- Test CASCADE delete: deleting conversation removes messages
- Test user isolation: user A cannot access user B's conversations
- Test conversation history loading with truncation
- Test message ordering (chronological)

### Data Migration Tests
- Test migration up: tables created with correct schema
- Test migration down: tables dropped cleanly
- Test existing data unaffected (task, user tables)

---

## Example Usage

### Creating a Conversation with Messages

```python
from sqlmodel import Session, select

# 1. Create conversation
conversation = Conversation(user_id=user_id)
session.add(conversation)
session.commit()
session.refresh(conversation)

# 2. Add user message
user_msg = Message(
    conversation_id=conversation.id,
    user_id=user_id,
    role="user",
    content="Add task to buy groceries"
)
session.add(user_msg)
session.commit()

# 3. Add assistant message with tool calls
assistant_msg = Message(
    conversation_id=conversation.id,
    user_id=user_id,
    role="assistant",
    content="I've added the task 'Buy groceries' to your list.",
    tool_calls=[{
        "tool": "add_task",
        "arguments": {"user_id": str(user_id), "title": "Buy groceries"},
        "result": {"success": True, "task_id": "..."}
    }]
)
session.add(assistant_msg)
session.commit()

# 4. Update conversation timestamp
conversation.updated_at = datetime.utcnow()
session.add(conversation)
session.commit()
```

---

## Summary

**New Tables**: 2 (conversation, message)  
**Modified Tables**: 0  
**Foreign Keys**: 3 (conversation.user_id, message.conversation_id, message.user_id)  
**Indexes**: 2 additional (for query performance)  
**Data Isolation**: Enforced via user_id filtering  
**Migration**: Alembic migration file required  

**Ready for**: API contract design (Phase 1, next step)
