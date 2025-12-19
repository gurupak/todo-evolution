# Data Model: Phase I - In-Memory Python Console Todo App

**Feature**: Phase I Todo CLI  
**Date**: 2025-12-18  
**Status**: Complete

## Overview

This document defines the data model for Phase I of the Todo application. The model consists of two core entities (Task, Priority) and one service entity (InMemoryStorage) managing the in-memory collection.

---

## Entity: Priority (Enum)

### Description
Enumeration defining the three task importance levels.

### Type
`enum.Enum`

### Values

| Value | String Representation | Display | Description |
|-------|----------------------|---------|-------------|
| `HIGH` | "high" | 🔴 High | Urgent or critical tasks |
| `MEDIUM` | "medium" | 🟡 Medium | Normal priority tasks (default) |
| `LOW` | "low" | 🟢 Low | Nice-to-have or low-urgency tasks |

### Implementation

```python
from enum import Enum

class Priority(Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
```

### Validation Rules
- MUST be one of the three defined values
- Default to MEDIUM when creating new tasks
- Cannot be None (required field)

### Display Format
- Console display: `{emoji} {name}` (e.g., "🔴 High", "🟡 Medium", "🟢 Low")
- Internal storage: enum value
- Serialization (if needed): `.value` property ("high", "medium", "low")

---

## Entity: Task (Dataclass)

### Description
Represents a single todo item with title, description, priority, completion status, and timestamps.

### Type
`@dataclass` (from `dataclasses` module)

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `UUID` | No | `uuid4()` | Unique task identifier (auto-generated) |
| `title` | `str` | Yes | N/A | Task name/summary (1-200 characters) |
| `description` | `str` | No | `""` | Detailed task description (max 1000 characters) |
| `priority` | `Priority` | No | `Priority.MEDIUM` | Task importance level |
| `is_completed` | `bool` | No | `False` | Completion status |
| `created_at` | `datetime` | No | `datetime.now()` | Task creation timestamp (auto-set) |
| `updated_at` | `datetime` | No | `datetime.now()` | Last modification timestamp (auto-updated) |
| `completed_at` | `datetime \| None` | No | `None` | Completion timestamp (set when marked complete) |

### Implementation

```python
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class Task:
    """Represents a todo task."""
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    is_completed: bool = False
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
```

### Field Details

#### `id: UUID`
- **Purpose**: Unique identifier for the task
- **Generation**: Auto-generated via `uuid4()` on instance creation
- **Immutable**: Should not be changed after creation
- **Display**: First 8 characters shown in UI (e.g., "a1b2c3d4")
- **Storage key**: Used as dictionary key in InMemoryStorage

#### `title: str`
- **Purpose**: Primary task description
- **Required**: Yes (must be provided on creation)
- **Validation**:
  - Length: 1-200 characters after trimming
  - Whitespace: Leading/trailing whitespace trimmed
  - Internal whitespace: Multiple spaces/newlines collapsed to single space
  - Characters: Allow all printable characters including emojis/unicode
  - Control characters: Stripped
- **Example**: "Buy groceries", "Complete project report 📝"

#### `description: str`
- **Purpose**: Additional task details
- **Required**: No (optional field)
- **Validation**:
  - Length: Max 1000 characters after trimming
  - Whitespace: Leading/trailing whitespace trimmed
  - Internal whitespace: Multiple spaces/newlines collapsed to single space
  - Characters: Allow all printable characters including emojis/unicode
  - Control characters: Stripped
- **Default**: Empty string `""`
- **Example**: "Milk, eggs, bread, cheese"

#### `priority: Priority`
- **Purpose**: Task importance level
- **Required**: No (defaults to MEDIUM)
- **Default**: `Priority.MEDIUM`
- **Validation**: Must be valid Priority enum value
- **Selection**: Required during creation (no skip option), user must explicitly choose

#### `is_completed: bool`
- **Purpose**: Completion status flag
- **Default**: `False` (new tasks are incomplete)
- **State changes**:
  - `False` → `True`: Mark complete (sets `completed_at`)
  - `True` → `False`: Mark incomplete (clears `completed_at`)

#### `created_at: datetime`
- **Purpose**: Task creation timestamp
- **Generation**: Auto-set to current time via `datetime.now()` on creation
- **Immutable**: Never updated after creation
- **Display format**:
  - Relative: `<7 days` → "2 hours ago", "3 days ago"
  - Absolute: `>=7 days` → "2025-01-15" (YYYY-MM-DD)

#### `updated_at: datetime`
- **Purpose**: Last modification timestamp
- **Generation**: Auto-set to current time on creation
- **Mutable**: Updated to `datetime.now()` whenever task is modified (title, description, priority, completion status)
- **Use case**: Track when task was last changed

#### `completed_at: datetime | None`
- **Purpose**: Completion timestamp
- **Default**: `None` (incomplete tasks)
- **State changes**:
  - Set to `datetime.now()` when `is_completed` changes from `False` to `True`
  - Set to `None` when `is_completed` changes from `True` to `False`
- **Nullable**: Can be `None` (incomplete) or `datetime` (completed)

### Validation Rules

#### Creation Validation
1. **Title required**: Non-empty after trimming, 1-200 characters
2. **Description optional**: If provided, max 1000 characters
3. **Text normalization**: All text fields trimmed, internal whitespace collapsed, control characters stripped
4. **Priority explicit**: User must select (defaults to MEDIUM but requires confirmation)
5. **Auto-fields**: `id`, `created_at`, `updated_at` set automatically

#### Update Validation
1. **Title**: Same rules as creation
2. **Description**: Same rules as creation
3. **Priority**: Must be valid enum value
4. **Timestamps**:
   - `created_at`: Never changed
   - `updated_at`: Always set to current time on any update
   - `completed_at`: Set/cleared based on `is_completed` change

#### State Transition: Mark Complete
```
Precondition: is_completed == False
Action: Mark complete
Postcondition:
  - is_completed = True
  - completed_at = datetime.now()
  - updated_at = datetime.now()
```

#### State Transition: Mark Incomplete
```
Precondition: is_completed == True
Action: Mark incomplete
Postcondition:
  - is_completed = False
  - completed_at = None
  - updated_at = datetime.now()
```

### Invariants

1. **UUID uniqueness**: Each task has a globally unique `id`
2. **Timestamp ordering**: `created_at` <= `updated_at` always
3. **Completion consistency**: `is_completed == True` ⟺ `completed_at is not None`
4. **Text validity**: `title` is never empty string after validation
5. **Priority validity**: `priority` is always a valid `Priority` enum value

---

## Entity: InMemoryStorage (Service)

### Description
Service class managing the in-memory collection of tasks. Wraps a dictionary providing CRUD operations and filtering helpers.

### Type
Class (service/repository pattern)

### Internal State

| Attribute | Type | Description |
|-----------|------|-------------|
| `_tasks` | `dict[UUID, Task]` | Private dictionary mapping task IDs to Task objects |

### Implementation

```python
from uuid import UUID
from todo.models import Task

class InMemoryStorage:
    """In-memory task storage using dictionary."""
    
    def __init__(self) -> None:
        """Initialize empty task storage."""
        self._tasks: dict[UUID, Task] = {}
```

### Methods

#### `add(task: Task) -> Task`
- **Purpose**: Add a new task to storage
- **Parameters**: `task` - Task instance to add
- **Returns**: The added task
- **Side effects**: Stores task in `_tasks` dict using `task.id` as key
- **Idempotency**: Overwrites if task with same ID exists (though IDs are unique)
- **Example**:
  ```python
  task = Task(title="Buy milk")
  storage.add(task)
  ```

#### `get(task_id: UUID) -> Task | None`
- **Purpose**: Retrieve a task by ID
- **Parameters**: `task_id` - UUID of task to retrieve
- **Returns**: Task object if found, `None` if not found
- **Side effects**: None (read-only)
- **Example**:
  ```python
  task = storage.get(some_uuid)
  if task is None:
      print("Task not found")
  ```

#### `get_all() -> list[Task]`
- **Purpose**: Retrieve all tasks
- **Returns**: List of all Task objects
- **Side effects**: None (read-only)
- **Order**: Unordered (dict values in arbitrary order)
- **Example**:
  ```python
  all_tasks = storage.get_all()
  ```

#### `update(task_id: UUID, **kwargs) -> Task | None`
- **Purpose**: Update a task's fields
- **Parameters**: 
  - `task_id` - UUID of task to update
  - `**kwargs` - Field names and new values
- **Returns**: Updated task if found, `None` if not found
- **Side effects**: 
  - Modifies task fields specified in kwargs
  - Sets `updated_at` to current time
- **Example**:
  ```python
  updated = storage.update(task_id, title="New title", priority=Priority.HIGH)
  ```

#### `delete(task_id: UUID) -> bool`
- **Purpose**: Remove a task from storage
- **Parameters**: `task_id` - UUID of task to delete
- **Returns**: `True` if task was deleted, `False` if not found
- **Side effects**: Removes task from `_tasks` dict
- **Example**:
  ```python
  success = storage.delete(task_id)
  ```

#### `get_pending() -> list[Task]`
- **Purpose**: Retrieve all incomplete tasks
- **Returns**: List of tasks where `is_completed == False`
- **Side effects**: None (read-only)
- **Filter**: `[task for task in tasks if not task.is_completed]`
- **Example**:
  ```python
  pending = storage.get_pending()
  ```

#### `get_completed() -> list[Task]`
- **Purpose**: Retrieve all completed tasks
- **Returns**: List of tasks where `is_completed == True`
- **Side effects**: None (read-only)
- **Filter**: `[task for task in tasks if task.is_completed]`
- **Example**:
  ```python
  done = storage.get_completed()
  ```

#### `count() -> dict[str, int]`
- **Purpose**: Get task count statistics
- **Returns**: Dictionary with keys `total`, `completed`, `pending`
- **Side effects**: None (read-only)
- **Example**:
  ```python
  stats = storage.count()
  # {"total": 10, "completed": 3, "pending": 7}
  ```

### Storage Characteristics

| Characteristic | Value | Rationale |
|----------------|-------|-----------|
| **Persistence** | None (in-memory only) | Phase I requirement - no file/DB persistence |
| **Capacity** | Limited by available RAM | Practical limit ~100 tasks for performance target |
| **Lookup complexity** | O(1) by ID | Dict key lookup is constant time |
| **Scan complexity** | O(n) for filters | Must iterate all tasks for filtering |
| **Thread safety** | Not thread-safe | Single-threaded CLI application |
| **Data loss** | On application exit | Expected behavior - no persistence |

### Relationships

```
InMemoryStorage
    │
    ├─── manages ───> {UUID: Task}
    │
    └─── provides operations on ───> Task collection
```

**Storage owns Tasks**: Tasks are stored and managed by InMemoryStorage. No other component directly accesses the internal `_tasks` dict.

---

## Entity Relationships Diagram

```
┌─────────────────────┐
│     Priority        │
│     (Enum)          │
├─────────────────────┤
│ + HIGH              │
│ + MEDIUM            │
│ + LOW               │
└─────────────────────┘
          △
          │
          │ has
          │
┌─────────────────────────────────────────┐
│              Task                       │
│           (Dataclass)                   │
├─────────────────────────────────────────┤
│ + id: UUID                              │
│ + title: str                            │
│ + description: str                      │
│ + priority: Priority                    │
│ + is_completed: bool                    │
│ + created_at: datetime                  │
│ + updated_at: datetime                  │
│ + completed_at: datetime | None         │
└─────────────────────────────────────────┘
          △
          │
          │ manages collection of
          │
┌─────────────────────────────────────────┐
│         InMemoryStorage                 │
│            (Service)                    │
├─────────────────────────────────────────┤
│ - _tasks: dict[UUID, Task]              │
├─────────────────────────────────────────┤
│ + add(task: Task) -> Task               │
│ + get(id: UUID) -> Task | None          │
│ + get_all() -> list[Task]               │
│ + update(id: UUID, **kw) -> Task | None │
│ + delete(id: UUID) -> bool              │
│ + get_pending() -> list[Task]           │
│ + get_completed() -> list[Task]         │
│ + count() -> dict[str, int]             │
└─────────────────────────────────────────┘
```

---

## Data Flow

### Task Creation Flow

```
User Input (questionary)
    │
    ├─> title: str (validated: 1-200 chars, trimmed, normalized)
    ├─> description: str (validated: max 1000 chars, trimmed, normalized)
    └─> priority: Priority (selected from enum, default MEDIUM)
    │
    ▼
Task Constructor
    │
    ├─> Auto-generate: id = uuid4()
    ├─> Auto-set: created_at = datetime.now()
    ├─> Auto-set: updated_at = datetime.now()
    ├─> Default: is_completed = False
    └─> Default: completed_at = None
    │
    ▼
InMemoryStorage.add(task)
    │
    └─> Store in _tasks[task.id] = task
    │
    ▼
Display success message (rich Panel)
```

### Task Update Flow

```
User selects task (questionary)
    │
    ▼
User updates fields (questionary)
    │
    ├─> title (optional)
    ├─> description (optional)
    └─> priority (optional)
    │
    ▼
InMemoryStorage.update(task_id, **kwargs)
    │
    ├─> Validate task exists
    ├─> Update specified fields
    └─> Set updated_at = datetime.now()
    │
    ▼
Display before/after comparison (rich Panel)
```

### Mark Complete Flow

```
User selects incomplete task (questionary)
    │
    ▼
InMemoryStorage.update(task_id,
                       is_completed=True,
                       completed_at=datetime.now())
    │
    └─> Set updated_at = datetime.now()
    │
    ▼
Display status change: ○ Pending → ✓ Complete (rich Panel)
```

---

## Validation Summary

### Input Validation (Pre-Storage)

| Field | Validator | Error Message |
|-------|-----------|---------------|
| Title (empty) | `len(title.strip()) == 0` | "Title is required - Please enter a title for your task (1-200 characters)" |
| Title (too long) | `len(title.strip()) > 200` | "Title too long - Maximum 200 characters allowed. You entered {count}" |
| Description (too long) | `len(description.strip()) > 1000` | "Description too long - Maximum 1000 characters allowed. You entered {count}" |
| Priority (invalid) | `priority not in Priority` | (Prevented by questionary enum choices) |

### Business Rules Validation (Storage)

| Rule | Check | Action |
|------|-------|--------|
| Task exists | `task_id in _tasks` | Return `None` or `False` if not found |
| Completion consistency | `is_completed == True` | Set `completed_at = datetime.now()` |
| Incompletion consistency | `is_completed == False` | Set `completed_at = None` |
| Update timestamp | Any field modified | Set `updated_at = datetime.now()` |
| Creation timestamp | Task created | Set `created_at = datetime.now()` (immutable) |

---

## Testing Checklist

### Task Entity Tests
- ✓ Task creation with required title
- ✓ Task creation with all optional fields
- ✓ Auto-generation of id, created_at, updated_at
- ✓ Default values for description, priority, is_completed, completed_at
- ✓ Priority enum values (HIGH, MEDIUM, LOW)

### InMemoryStorage Tests
- ✓ Add task and retrieve by ID
- ✓ Get non-existent task returns None
- ✓ Get all tasks returns list
- ✓ Update task fields and verify updated_at changed
- ✓ Update non-existent task returns None
- ✓ Delete task and verify removed
- ✓ Delete non-existent task returns False
- ✓ Get pending tasks filters correctly
- ✓ Get completed tasks filters correctly
- ✓ Count returns correct statistics

### State Transition Tests
- ✓ Mark incomplete task complete (is_completed, completed_at, updated_at)
- ✓ Mark complete task incomplete (is_completed, completed_at cleared, updated_at)
- ✓ Timestamp invariants (created_at <= updated_at)
- ✓ Completion consistency (is_completed ⟺ completed_at not None)

---

## Summary

The data model for Phase I consists of:

1. **Priority** - Simple enum with 3 values (HIGH, MEDIUM, LOW)
2. **Task** - Rich dataclass with 8 fields, automatic ID/timestamp generation, validation rules
3. **InMemoryStorage** - Service providing 8 CRUD/filter operations on task collection

**Key Design Decisions**:
- ✅ UUID for unique task identification (not auto-incrementing integers)
- ✅ Dataclass for simple, immutable-like Task structure
- ✅ Field factories for auto-generation (uuid4, datetime.now)
- ✅ Dict-based storage for O(1) lookups
- ✅ No persistence (in-memory only per Phase I requirements)
- ✅ Explicit validation rules for all user input
- ✅ State transition rules for completion status
- ✅ Timestamp tracking (created, updated, completed)

**Ready to proceed to: Generate contracts/ and quickstart.md**
