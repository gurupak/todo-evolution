# Models Contract

**Module**: `todo.models`  
**Purpose**: Data structures for Task and Priority

---

## Priority (Enum)

```python
from enum import Enum

class Priority(Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
```

### Enum Values

| Value | String | Description |
|-------|--------|-------------|
| `Priority.HIGH` | "high" | Urgent or critical tasks |
| `Priority.MEDIUM` | "medium" | Normal priority tasks (default) |
| `Priority.LOW` | "low" | Nice-to-have tasks |

### Usage

```python
# Create with enum
task = Task(title="Buy milk", priority=Priority.HIGH)

# Access string value
priority_str = task.priority.value  # "high"

# Compare
if task.priority == Priority.HIGH:
    print("Urgent!")
```

---

## Task (Dataclass)

```python
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class Task:
    """Represents a todo task."""
    
    # Required fields
    title: str
    
    # Optional fields with defaults
    description: str = ""
    priority: Priority = Priority.MEDIUM
    is_completed: bool = False
    
    # Auto-generated fields
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
```

### Field Specifications

#### Required Fields

**`title: str`**
- **Purpose**: Task name/summary
- **Required**: Yes (must provide on creation)
- **Constraints**: 1-200 characters after normalization
- **Validation**: Performed by questionary before Task creation

#### Optional Fields

**`description: str`**
- **Purpose**: Detailed task information
- **Default**: `""`
- **Constraints**: Max 1000 characters after normalization

**`priority: Priority`**
- **Purpose**: Task importance level
- **Default**: `Priority.MEDIUM`
- **Constraints**: Must be valid Priority enum value

**`is_completed: bool`**
- **Purpose**: Completion status flag
- **Default**: `False`
- **Constraints**: None

#### Auto-Generated Fields

**`id: UUID`**
- **Purpose**: Unique task identifier
- **Generation**: `uuid4()` called on instance creation
- **Type**: UUID object (not string)
- **Immutable**: Should not be changed after creation

**`created_at: datetime`**
- **Purpose**: Task creation timestamp
- **Generation**: `datetime.now()` called on instance creation
- **Immutable**: Never updated after creation

**`updated_at: datetime`**
- **Purpose**: Last modification timestamp
- **Generation**: `datetime.now()` called on instance creation
- **Mutable**: Updated on any task modification

**`completed_at: datetime | None`**
- **Purpose**: Completion timestamp
- **Default**: `None`
- **State**: Set to `datetime.now()` when marked complete, cleared when marked incomplete

### Constructor Examples

```python
# Minimal (required fields only)
task = Task(title="Buy milk")
# Result: Task with default priority=MEDIUM, description="", is_completed=False

# With optional fields
task = Task(
    title="Buy milk",
    description="Whole milk, 2 gallons",
    priority=Priority.HIGH
)

# Full specification (unusual - auto fields typically not provided)
task = Task(
    title="Buy milk",
    description="Whole milk, 2 gallons",
    priority=Priority.HIGH,
    is_completed=False,
    id=uuid4(),  # Explicit UUID (rare)
    created_at=datetime.now(),
    updated_at=datetime.now(),
    completed_at=None
)
```

### Dataclass Features

#### Automatic Methods

```python
# Equality (compares all fields)
task1 == task2  # True if all fields equal

# String representation
str(task)  # "Task(title='Buy milk', ...)"
repr(task)  # Same as str()

# Field access
task.title  # "Buy milk"
task.priority  # Priority.MEDIUM
```

#### Field Mutation

```python
# Direct field assignment (allowed but discouraged)
task.title = "Buy groceries"
task.is_completed = True

# Preferred: Use InMemoryStorage.update() for managed updates
storage.update(task.id, title="Buy groceries", is_completed=True)
```

### Type Annotations

```python
# Type hints for clarity
task_id: UUID = task.id
title: str = task.title
priority: Priority = task.priority
completed: bool = task.is_completed
created: datetime = task.created_at
completed_time: datetime | None = task.completed_at
```

---

## Module Exports

```python
# Public API
__all__ = ["Task", "Priority"]

# Usage
from todo.models import Task, Priority
```

---

## Dependencies

- `dataclasses` - Standard library
- `datetime` - Standard library
- `uuid` - Standard library
- `enum` - Standard library

**No external dependencies**

---

## Testing Contract

### Task Creation Tests

```python
def test_task_minimal_creation():
    """Task can be created with just title."""
    task = Task(title="Test")
    assert task.title == "Test"
    assert task.description == ""
    assert task.priority == Priority.MEDIUM
    assert task.is_completed is False
    assert task.id is not None
    assert task.created_at is not None
    assert task.updated_at is not None
    assert task.completed_at is None

def test_task_full_creation():
    """Task can be created with all optional fields."""
    task = Task(
        title="Test",
        description="Description",
        priority=Priority.HIGH,
        is_completed=True
    )
    assert task.title == "Test"
    assert task.description == "Description"
    assert task.priority == Priority.HIGH
    assert task.is_completed is True

def test_task_unique_ids():
    """Each task gets unique UUID."""
    task1 = Task(title="Task 1")
    task2 = Task(title="Task 2")
    assert task1.id != task2.id
```

### Priority Enum Tests

```python
def test_priority_values():
    """Priority enum has expected values."""
    assert Priority.HIGH.value == "high"
    assert Priority.MEDIUM.value == "medium"
    assert Priority.LOW.value == "low"

def test_priority_comparison():
    """Priority enum values can be compared."""
    task = Task(title="Test", priority=Priority.HIGH)
    assert task.priority == Priority.HIGH
    assert task.priority != Priority.LOW
```

---

## Version

**Contract Version**: 1.0.0  
**Last Updated**: 2025-12-18
