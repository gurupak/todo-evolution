# Commands Contract

**Module**: `todo.commands`  
**Purpose**: User interaction and business logic for CLI commands

---

## Overview

All command functions:
- Accept `storage: InMemoryStorage` as parameter (dependency injection)
- Return `None` (side effects only)
- Handle user interaction via questionary
- Display output via display module functions
- Implement business logic and validation

---

## Function Signatures

```python
from todo.storage import InMemoryStorage

def add_task(storage: InMemoryStorage) -> None:
    """Add a new task through interactive prompts."""
    ...

def list_tasks(storage: InMemoryStorage) -> None:
    """Display all tasks in formatted table."""
    ...

def update_task(storage: InMemoryStorage) -> None:
    """Update an existing task's details."""
    ...

def delete_task(storage: InMemoryStorage) -> None:
    """Delete a task with confirmation."""
    ...

def mark_complete(storage: InMemoryStorage) -> None:
    """Mark an incomplete task as complete."""
    ...

def mark_incomplete(storage: InMemoryStorage) -> None:
    """Mark a complete task as incomplete."""
    ...

def show_help() -> None:
    """Display help screen with command reference."""
    ...
```

---

## Command Contracts

### `add_task(storage: InMemoryStorage) -> None`

**Purpose**: Add a new task through interactive prompts

**Parameters**:
- `storage: InMemoryStorage` - Storage instance for saving task

**Returns**: None

**User Flow**:
1. Prompt for title (required, validated)
2. Prompt for description (optional)
3. Prompt for priority (default MEDIUM, required selection)
4. Create Task object
5. Save to storage
6. Display success panel with task details

**Validation**:
- Title: 1-200 chars after trimming
- Description: Max 1000 chars after trimming
- Priority: Must select from enum (no skip)

**Cancellation**: If user presses Ctrl+C at any prompt, show cancellation message and return

**Success Output**:
```
╭─ ✓ Task Added ──────────────╮
│ Buy groceries               │
│ ID: a1b2c3d4                │
│ Priority: 🟡 Medium         │
│ Status: ○ Pending           │
╰─────────────────────────────╯
```

**Example**:
```python
storage = InMemoryStorage()
add_task(storage)  # Prompts user, adds task
```

---

### `list_tasks(storage: InMemoryStorage) -> None`

**Purpose**: Display all tasks in formatted table with statistics

**Parameters**:
- `storage: InMemoryStorage` - Storage instance for retrieving tasks

**Returns**: None

**User Flow**:
1. Retrieve all tasks from storage
2. If empty, show empty state panel
3. If has tasks, show formatted table (sorted newest first)
4. Show summary statistics

**Empty State**:
```
╭─────────────────────────╮
│   📭 No tasks yet!      │
│                         │
│ Get started by adding   │
│ your first task.        │
╰─────────────────────────╯
```

**Task Table**:
```
┌──────────┬───────────────┬──────────┬──────────┬────────────┐
│ ID       │ Title         │ Priority │ Status   │ Created    │
├──────────┼───────────────┼──────────┼──────────┼────────────┤
│ a1b2c3d4 │ Buy groceries │ 🟡 Medium│ ○ Pending│ 2 hours ago│
│ b2c3d4e5 │ Write report  │ 🔴 High  │ ✓ Complete│ 2025-01-10│
└──────────┴───────────────┴──────────┴──────────┴────────────┘

📊 Total: 2 tasks │ ✓ 1 complete │ ○ 1 pending
```

**Example**:
```python
list_tasks(storage)  # Displays table or empty state
```

---

### `update_task(storage: InMemoryStorage) -> None`

**Purpose**: Update an existing task's details

**Parameters**:
- `storage: InMemoryStorage` - Storage instance for updating task

**Returns**: None

**User Flow**:
1. Check if tasks exist (show warning if empty)
2. Prompt user to select task from list
3. Prompt user to select what to update (Title/Description/Priority/All)
4. Prompt for new value(s) based on selection
5. Update task in storage
6. Display before/after comparison

**Empty State**: Show warning panel with tip to add task first

**Update Options**:
- Title only
- Description only
- Priority only
- All fields

**Success Output**:
```
╭─ ✓ Task Updated ────────────╮
│ Before: Buy milk            │
│ After:  Buy groceries       │
│                             │
│ Priority: 🟡 Medium → 🔴 High│
╰─────────────────────────────╯
```

**Cancellation**: If user cancels at any prompt, show cancellation message and return

**Example**:
```python
update_task(storage)  # Prompts user, updates selected task
```

---

### `delete_task(storage: InMemoryStorage) -> None`

**Purpose**: Delete a task with confirmation

**Parameters**:
- `storage: InMemoryStorage` - Storage instance for deleting task

**Returns**: None

**User Flow**:
1. Check if tasks exist (show warning if empty)
2. Prompt user to select task from list
3. Display task details panel
4. Prompt for confirmation (Yes/No)
5. If confirmed, delete from storage and show success
6. If cancelled, show cancellation message

**Confirmation Panel**:
```
╭─ Confirm Deletion ──────────╮
│ ID: a1b2c3d4                │
│ Title: Buy groceries        │
│ Description: Milk, eggs     │
│ Priority: 🟡 Medium         │
│ Status: ○ Pending           │
│ Created: 2 hours ago        │
│                             │
│ Are you sure?               │
│ > Yes, delete it            │
│   No, keep it               │
╰─────────────────────────────╯
```

**Success Output**:
```
╭─ ✓ Task Deleted ────────────╮
│ 'Buy groceries' has been    │
│ removed                     │
╰─────────────────────────────╯
```

**Cancellation Output**:
```
╭─ ℹ Deletion Cancelled ──────╮
│ Task was not removed        │
╰─────────────────────────────╯
```

**Example**:
```python
delete_task(storage)  # Prompts user, deletes if confirmed
```

---

### `mark_complete(storage: InMemoryStorage) -> None`

**Purpose**: Mark an incomplete task as complete

**Parameters**:
- `storage: InMemoryStorage` - Storage instance for updating task

**Returns**: None

**User Flow**:
1. Retrieve all pending tasks
2. If none, show info panel
3. Prompt user to select task from pending list
4. Update task: `is_completed=True`, `completed_at=datetime.now()`
5. Display status change confirmation

**All Complete Info**:
```
╭─ ℹ All Tasks Complete ──────╮
│ All tasks are already       │
│ complete!                   │
│                             │
│ 💡 Tip: Add new tasks or    │
│ mark some incomplete        │
╰─────────────────────────────╯
```

**Success Output**:
```
╭─ ✓ Task Completed ──────────╮
│ Buy groceries               │
│ ○ Pending → ✓ Complete      │
╰─────────────────────────────╯
```

**Example**:
```python
mark_complete(storage)  # Prompts user, marks selected task complete
```

---

### `mark_incomplete(storage: InMemoryStorage) -> None`

**Purpose**: Mark a complete task as incomplete

**Parameters**:
- `storage: InMemoryStorage` - Storage instance for updating task

**Returns**: None

**User Flow**:
1. Retrieve all completed tasks
2. If none, show info panel
3. Prompt user to select task from completed list
4. Update task: `is_completed=False`, `completed_at=None`
5. Display status change confirmation

**No Complete Tasks Info**:
```
╭─ ℹ No Completed Tasks ──────╮
│ No completed tasks to mark  │
│ incomplete                  │
╰─────────────────────────────╯
```

**Success Output**:
```
╭─ ✓ Task Marked Incomplete ──╮
│ Buy groceries               │
│ ✓ Complete → ○ Pending      │
╰─────────────────────────────╯
```

**Example**:
```python
mark_incomplete(storage)  # Prompts user, marks selected task incomplete
```

---

### `show_help() -> None`

**Purpose**: Display help screen with command reference and navigation tips

**Parameters**: None

**Returns**: None

**Output**: Help panel with:
- Command list with shortcuts
- Navigation tips (arrow keys, Ctrl+C)
- 2-3 usage examples

**Help Screen**:
```
╭─ ❓ Help ───────────────────────────────╮
│ COMMANDS                                 │
│ ➕ add      - Add a new task            │
│ 📋 list     - View all tasks            │
│ ✏️  update   - Update a task            │
│ 🗑️  delete   - Delete a task            │
│ ✅ done     - Mark task complete        │
│ ⬜ undone   - Mark task incomplete      │
│ ❓ help     - Show this help            │
│ 🚪 exit     - Exit application          │
│                                          │
│ NAVIGATION                               │
│ • Use ↑↓ arrows to select options       │
│ • Type command shortcuts (e.g., "add")  │
│ • Press Ctrl+C to cancel/go back        │
│                                          │
│ EXAMPLES                                 │
│ 1. Type "add" or select "➕ Add Task"   │
│ 2. Enter task details when prompted     │
│ 3. View tasks with "list" command       │
╰──────────────────────────────────────────╯
```

**Example**:
```python
show_help()  # Displays help screen
```

---

## Helper Functions (Internal)

These functions are used internally by commands but not part of public API:

```python
def prompt_title(current: str = "") -> str | None:
    """Prompt for task title with validation."""
    ...

def prompt_description(current: str = "") -> str | None:
    """Prompt for task description."""
    ...

def prompt_priority(current: Priority = Priority.MEDIUM) -> Priority | None:
    """Prompt for priority selection."""
    ...

def prompt_select_task(tasks: list[Task], message: str) -> Task | None:
    """Prompt user to select a task from list."""
    ...

def prompt_confirm(message: str) -> bool:
    """Prompt for yes/no confirmation."""
    ...
```

---

## Error Handling

### Empty Storage

| Command | Behavior |
|---------|----------|
| `list_tasks` | Show empty state panel |
| `update_task` | Show warning: "No tasks available to update" |
| `delete_task` | Show warning: "No tasks available" |
| `mark_complete` | Show info: "All tasks are already complete!" (if all complete) |
| `mark_incomplete` | Show info: "No completed tasks to mark incomplete" |

### User Cancellation (Ctrl+C)

All commands handle `None` return from questionary prompts:
```python
choice = prompt_something()
if choice is None:
    display.show_info("ℹ Operation cancelled. Returning to main menu...")
    return
```

### Invalid Input

Validation happens at prompt level (questionary validators), so commands receive valid input only.

---

## Dependencies

```python
import questionary
from questionary import Choice, Separator
from datetime import datetime

from todo.storage import InMemoryStorage
from todo.models import Task, Priority
from todo import display
```

---

## Module Exports

```python
__all__ = [
    "add_task",
    "list_tasks",
    "update_task",
    "delete_task",
    "mark_complete",
    "mark_incomplete",
    "show_help",
]

# Usage
from todo.commands import add_task, list_tasks, ...
```

---

## Testing Strategy

Commands are tested using mocked questionary and storage:

```python
from unittest.mock import Mock, patch

@patch('todo.commands.questionary')
def test_add_task(mock_questionary):
    # Mock user input
    mock_questionary.text.return_value.ask.return_value = "Buy milk"
    mock_questionary.select.return_value.ask.return_value = Priority.MEDIUM
    
    storage = InMemoryStorage()
    add_task(storage)
    
    tasks = storage.get_all()
    assert len(tasks) == 1
    assert tasks[0].title == "Buy milk"

@patch('todo.commands.questionary')
def test_add_task_cancelled(mock_questionary):
    # User cancels (Ctrl+C)
    mock_questionary.text.return_value.ask.return_value = None
    
    storage = InMemoryStorage()
    add_task(storage)
    
    assert len(storage.get_all()) == 0
```

---

## Version

**Contract Version**: 1.0.0  
**Last Updated**: 2025-12-18
