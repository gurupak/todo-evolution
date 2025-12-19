# Storage Contract

**Module**: `todo.storage`  
**Purpose**: In-memory task storage and CRUD operations

---

## InMemoryStorage Class

```python
from uuid import UUID
from todo.models import Task

class InMemoryStorage:
    """In-memory task storage using dictionary."""
    
    def __init__(self) -> None:
        """Initialize empty task storage."""
        ...
    
    def add(self, task: Task) -> Task:
        """Add a new task to storage."""
        ...
    
    def get(self, task_id: UUID) -> Task | None:
        """Get a task by ID, or None if not found."""
        ...
    
    def get_all(self) -> list[Task]:
        """Get all tasks."""
        ...
    
    def update(self, task_id: UUID, **kwargs) -> Task | None:
        """Update a task's fields. Returns updated task or None if not found."""
        ...
    
    def delete(self, task_id: UUID) -> bool:
        """Delete a task. Returns True if deleted, False if not found."""
        ...
    
    def get_pending(self) -> list[Task]:
        """Get all incomplete tasks."""
        ...
    
    def get_completed(self) -> list[Task]:
        """Get all completed tasks."""
        ...
    
    def count(self) -> dict[str, int]:
        """Get task counts (total, completed, pending)."""
        ...
```

---

## Method Contracts

### `__init__() -> None`

**Purpose**: Initialize empty task storage

**Parameters**: None

**Returns**: None (constructor)

**Side Effects**: Initializes internal `_tasks` dictionary

**Example**:
```python
storage = InMemoryStorage()
assert len(storage.get_all()) == 0
```

---

### `add(task: Task) -> Task`

**Purpose**: Add a new task to storage

**Parameters**:
- `task: Task` - The task instance to add

**Returns**: `Task` - The same task instance (for chaining)

**Side Effects**: Stores task in internal dictionary using `task.id` as key

**Behavior**:
- If task with same ID exists, overwrites (idempotent)
- Task object is stored by reference (mutations affect stored task)

**Example**:
```python
task = Task(title="Buy milk")
added_task = storage.add(task)
assert added_task == task
assert storage.get(task.id) == task
```

---

### `get(task_id: UUID) -> Task | None`

**Purpose**: Retrieve a task by its ID

**Parameters**:
- `task_id: UUID` - The unique identifier of the task

**Returns**: 
- `Task` - The task object if found
- `None` - If no task with given ID exists

**Side Effects**: None (read-only operation)

**Example**:
```python
task = Task(title="Buy milk")
storage.add(task)

retrieved = storage.get(task.id)
assert retrieved == task

not_found = storage.get(uuid4())  # Random UUID
assert not_found is None
```

---

### `get_all() -> list[Task]`

**Purpose**: Retrieve all tasks in storage

**Parameters**: None

**Returns**: `list[Task]` - List of all task objects (may be empty)

**Side Effects**: None (read-only operation)

**Behavior**:
- Order is not guaranteed (dict values in arbitrary order)
- Returns empty list if no tasks exist
- Returns new list each call (not a reference to internal structure)

**Example**:
```python
storage.add(Task(title="Task 1"))
storage.add(Task(title="Task 2"))

all_tasks = storage.get_all()
assert len(all_tasks) == 2
```

---

### `update(task_id: UUID, **kwargs) -> Task | None`

**Purpose**: Update one or more fields of a task

**Parameters**:
- `task_id: UUID` - The ID of the task to update
- `**kwargs` - Field names and their new values

**Returns**:
- `Task` - The updated task object if found
- `None` - If no task with given ID exists

**Side Effects**: 
- Modifies the task object in storage
- Sets `updated_at` field to `datetime.now()`

**Behavior**:
- Only updates fields specified in kwargs
- Ignores kwargs for non-existent fields
- Always updates `updated_at` timestamp
- Special handling for `is_completed`:
  - If changed to `True`, sets `completed_at = datetime.now()`
  - If changed to `False`, sets `completed_at = None`

**Example**:
```python
task = Task(title="Buy milk")
storage.add(task)

updated = storage.update(
    task.id,
    title="Buy groceries",
    priority=Priority.HIGH
)
assert updated.title == "Buy groceries"
assert updated.priority == Priority.HIGH
assert updated.updated_at > task.created_at

# Task not found
not_found = storage.update(uuid4(), title="New")
assert not_found is None
```

---

### `delete(task_id: UUID) -> bool`

**Purpose**: Remove a task from storage

**Parameters**:
- `task_id: UUID` - The ID of the task to delete

**Returns**:
- `True` - If task was found and deleted
- `False` - If no task with given ID exists

**Side Effects**: Removes task from internal dictionary

**Example**:
```python
task = Task(title="Buy milk")
storage.add(task)

success = storage.delete(task.id)
assert success is True
assert storage.get(task.id) is None

# Already deleted
success_again = storage.delete(task.id)
assert success_again is False
```

---

### `get_pending() -> list[Task]`

**Purpose**: Retrieve all incomplete tasks

**Parameters**: None

**Returns**: `list[Task]` - List of tasks where `is_completed == False`

**Side Effects**: None (read-only operation)

**Filter Criteria**: `not task.is_completed`

**Example**:
```python
task1 = Task(title="Incomplete 1")
task2 = Task(title="Incomplete 2")
task3 = Task(title="Complete", is_completed=True)

storage.add(task1)
storage.add(task2)
storage.add(task3)

pending = storage.get_pending()
assert len(pending) == 2
assert task1 in pending
assert task2 in pending
assert task3 not in pending
```

---

### `get_completed() -> list[Task]`

**Purpose**: Retrieve all completed tasks

**Parameters**: None

**Returns**: `list[Task]` - List of tasks where `is_completed == True`

**Side Effects**: None (read-only operation)

**Filter Criteria**: `task.is_completed`

**Example**:
```python
task1 = Task(title="Incomplete")
task2 = Task(title="Complete 1", is_completed=True)
task3 = Task(title="Complete 2", is_completed=True)

storage.add(task1)
storage.add(task2)
storage.add(task3)

completed = storage.get_completed()
assert len(completed) == 2
assert task2 in completed
assert task3 in completed
assert task1 not in completed
```

---

### `count() -> dict[str, int]`

**Purpose**: Get task count statistics

**Parameters**: None

**Returns**: `dict[str, int]` with keys:
- `"total"`: Total number of tasks
- `"completed"`: Number of completed tasks (`is_completed == True`)
- `"pending"`: Number of incomplete tasks (`is_completed == False`)

**Side Effects**: None (read-only operation)

**Invariant**: `total == completed + pending`

**Example**:
```python
storage.add(Task(title="Pending 1"))
storage.add(Task(title="Pending 2"))
storage.add(Task(title="Complete", is_completed=True))

stats = storage.count()
assert stats == {
    "total": 3,
    "completed": 1,
    "pending": 2
}
```

---

## Internal State

### `_tasks: dict[UUID, Task]`

**Type**: Private attribute (not part of public API)

**Purpose**: Internal storage dictionary

**Key**: Task UUID  
**Value**: Task object

**Access**: Should only be accessed by InMemoryStorage methods

---

## Error Handling

### Not Found Scenarios

| Method | Behavior when Task Not Found |
|--------|------------------------------|
| `get(task_id)` | Returns `None` |
| `update(task_id, ...)` | Returns `None` |
| `delete(task_id)` | Returns `False` |

### Empty Storage Scenarios

| Method | Behavior when Storage Empty |
|--------|----------------------------|
| `get_all()` | Returns `[]` |
| `get_pending()` | Returns `[]` |
| `get_completed()` | Returns `[]` |
| `count()` | Returns `{"total": 0, "completed": 0, "pending": 0}` |

---

## Thread Safety

**Not Thread-Safe**: InMemoryStorage is designed for single-threaded CLI application.

**Concurrent Access**: Not supported. Do not use from multiple threads.

---

## Memory Management

**Persistence**: None - all data lost when storage object is garbage collected

**Capacity**: Limited by available RAM (practical limit ~100 tasks for target performance)

---

## Dependencies

```python
from uuid import UUID  # Standard library
from todo.models import Task  # Internal module
```

---

## Module Exports

```python
__all__ = ["InMemoryStorage"]

# Usage
from todo.storage import InMemoryStorage
```

---

## Testing Contract

```python
def test_add_and_get_task():
    storage = InMemoryStorage()
    task = Task(title="Test")
    storage.add(task)
    assert storage.get(task.id) == task

def test_get_nonexistent_task():
    storage = InMemoryStorage()
    assert storage.get(uuid4()) is None

def test_update_task():
    storage = InMemoryStorage()
    task = Task(title="Original")
    storage.add(task)
    
    updated = storage.update(task.id, title="Updated")
    assert updated.title == "Updated"
    assert updated.updated_at > task.created_at

def test_delete_task():
    storage = InMemoryStorage()
    task = Task(title="To Delete")
    storage.add(task)
    
    assert storage.delete(task.id) is True
    assert storage.get(task.id) is None

def test_filter_pending():
    storage = InMemoryStorage()
    storage.add(Task(title="Pending"))
    storage.add(Task(title="Complete", is_completed=True))
    
    pending = storage.get_pending()
    assert len(pending) == 1
    assert pending[0].title == "Pending"

def test_count():
    storage = InMemoryStorage()
    storage.add(Task(title="Task 1"))
    storage.add(Task(title="Task 2", is_completed=True))
    
    stats = storage.count()
    assert stats == {"total": 2, "completed": 1, "pending": 1}
```

---

## Version

**Contract Version**: 1.0.0  
**Last Updated**: 2025-12-18
