# Display Contract

**Module**: `todo.display`  
**Purpose**: Rich terminal output formatting and display functions

---

## Overview

All display functions:
- Use the shared `console` singleton
- Return `None` (output to terminal only)
- Handle formatting and styling via rich library
- Never raise exceptions (graceful degradation)

---

## Console Singleton

```python
from rich.console import Console
from rich.theme import Theme

theme = Theme({
    "success": "green bold",
    "error": "red bold",
    "warning": "yellow bold",
    "info": "blue",
    "dim": "dim",
})

console = Console(theme=theme)
```

**Purpose**: Single console instance for consistent output and buffering

---

## Display Functions

```python
from todo.models import Task, Priority

def show_banner() -> None:
    """Display application banner with ASCII art."""
    ...

def show_success(title: str, message: str) -> None:
    """Display success message in green panel."""
    ...

def show_error(message: str, tip: str | None = None) -> None:
    """Display error message in red panel with optional tip."""
    ...

def show_warning(message: str) -> None:
    """Display warning message in yellow panel."""
    ...

def show_info(message: str) -> None:
    """Display info message in blue panel."""
    ...

def show_task_table(tasks: list[Task]) -> None:
    """Display tasks in formatted table with statistics."""
    ...

def show_empty_state() -> None:
    """Display empty state when no tasks exist."""
    ...

def show_task_details(task: Task) -> None:
    """Display detailed task information panel."""
    ...

def show_help_screen() -> None:
    """Display help screen with command reference."""
    ...

def show_goodbye() -> None:
    """Display goodbye message on exit."""
    ...

def format_priority(priority: Priority) -> str:
    """Format priority with emoji indicator."""
    ...

def format_status(is_completed: bool) -> str:
    """Format status with icon indicator."""
    ...

def format_task_choice(task: Task) -> str:
    """Format task for selection menu display."""
    ...
```

---

## Function Contracts

### `show_banner() -> None`

**Purpose**: Display application banner with ASCII art and version

**Parameters**: None

**Returns**: None

**Output**:
```
╭────────────────────────────────────────╮
│       _______ ____  ____  ____         │
│      /_  __// __ \/ __ \/ __ \        │
│       / /  / / / / / / / / / /        │
│      / /  / /_/ / /_/ / /_/ /         │
│     /_/   \____/_____/\____/          │
│                                        │
│   ──────────────────────────────────   │
│   Phase I: In-Memory Console App       │
│   Version 0.1.0                        │
╰────────────────────────────────────────╯
```

**Dependencies**: Uses pyfiglet for ASCII art

**Example**:
```python
show_banner()  # Prints banner to console
```

---

### `show_success(title: str, message: str) -> None`

**Purpose**: Display success message in green panel

**Parameters**:
- `title: str` - Panel title (e.g., "Task Added")
- `message: str` - Success message content

**Returns**: None

**Output**:
```
╭─ ✓ Task Added ──────────────╮
│ Buy groceries               │
│ ID: a1b2c3d4                │
│ Priority: 🟡 Medium         │
│ Status: ○ Pending           │
╰─────────────────────────────╯
```

**Style**: Green border, green bold text, checkmark icon

**Example**:
```python
show_success(
    "Task Added",
    "Buy groceries\nID: a1b2c3d4\nPriority: 🟡 Medium"
)
```

---

### `show_error(message: str, tip: str | None = None) -> None`

**Purpose**: Display error message in red panel with optional tip

**Parameters**:
- `message: str` - Error message
- `tip: str | None` - Optional helpful tip (default: None)

**Returns**: None

**Output**:
```
╭─ Error ─────────────────────╮
│ ✗ Title is required         │
│                             │
│ 💡 Tip: Enter a task title  │
│ between 1-200 characters    │
╰─────────────────────────────╯
```

**Style**: Red border, red bold text, optional tip in blue

**Example**:
```python
show_error(
    "Title is required",
    "Enter a task title between 1-200 characters"
)
```

---

### `show_warning(message: str) -> None`

**Purpose**: Display warning message in yellow panel

**Parameters**:
- `message: str` - Warning message

**Returns**: None

**Output**:
```
╭─ Warning ───────────────────╮
│ ⚠ No tasks available to     │
│ update                      │
╰─────────────────────────────╯
```

**Style**: Yellow border, yellow bold text, warning icon

**Example**:
```python
show_warning("No tasks available to update")
```

---

### `show_info(message: str) -> None`

**Purpose**: Display info message in blue panel

**Parameters**:
- `message: str` - Info message

**Returns**: None

**Output**:
```
╭─ Info ──────────────────────╮
│ ℹ Operation cancelled.      │
│ Returning to main menu...   │
╰─────────────────────────────╯
```

**Style**: Blue border, blue text, info icon

**Example**:
```python
show_info("Operation cancelled. Returning to main menu...")
```

---

### `show_task_table(tasks: list[Task]) -> None`

**Purpose**: Display tasks in formatted table with statistics

**Parameters**:
- `tasks: list[Task]` - List of tasks to display

**Returns**: None

**Behavior**:
- Sorts tasks by `created_at` descending (newest first)
- Truncates long titles to fit terminal width
- Shows summary statistics after table

**Output**:
```
┌──────────┬───────────────┬──────────┬──────────┬────────────┐
│ ID       │ Title         │ Priority │ Status   │ Created    │
├──────────┼───────────────┼──────────┼──────────┼────────────┤
│ a1b2c3d4 │ Buy groceries │ 🟡 Medium│ ○ Pending│ 2 hours ago│
│ b2c3d4e5 │ Write report  │ 🔴 High  │ ✓ Complete│ 2025-01-10│
└──────────┴───────────────┴──────────┴──────────┴────────────┘

📊 Total: 2 tasks │ ✓ 1 complete │ ○ 1 pending
```

**Table Columns**:
- ID: First 8 characters of UUID
- Title: Smart truncated with ellipsis
- Priority: Emoji + name (🔴/🟡/🟢)
- Status: Icon + text (✓/○)
- Created: Relative (<7 days) or absolute (>=7 days)

**Example**:
```python
tasks = storage.get_all()
show_task_table(tasks)
```

---

### `show_empty_state() -> None`

**Purpose**: Display empty state when no tasks exist

**Parameters**: None

**Returns**: None

**Output**:
```
╭─────────────────────────╮
│   📭 No tasks yet!      │
│                         │
│ Get started by adding   │
│ your first task.        │
╰─────────────────────────╯
```

**Style**: Blue border, centered text, mailbox icon

**Example**:
```python
if not tasks:
    show_empty_state()
```

---

### `show_task_details(task: Task) -> None`

**Purpose**: Display detailed task information panel

**Parameters**:
- `task: Task` - Task to display

**Returns**: None

**Output**:
```
╭─ Task Details ──────────────╮
│ ID: a1b2c3d4                │
│ Title: Buy groceries        │
│ Description: Milk, eggs     │
│ Priority: 🟡 Medium         │
│ Status: ○ Pending           │
│ Created: 2 hours ago        │
╰─────────────────────────────╯
```

**Usage**: Used before delete confirmation

**Example**:
```python
show_task_details(task)
```

---

### `show_help_screen() -> None`

**Purpose**: Display help screen with command reference

**Parameters**: None

**Returns**: None

**Output**:
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

**Content**:
- Command list with shortcuts
- Navigation tips
- 2-3 usage examples

**Example**:
```python
show_help_screen()
```

---

### `show_goodbye() -> None`

**Purpose**: Display goodbye message on exit

**Parameters**: None

**Returns**: None

**Output**:
```
╭─ Goodbye! ──────────────────╮
│ Your tasks were stored in   │
│ memory and will be lost.    │
│ See you next time!          │
╰─────────────────────────────╯
```

**Example**:
```python
show_goodbye()
```

---

## Formatting Functions

### `format_priority(priority: Priority) -> str`

**Purpose**: Format priority with emoji indicator

**Parameters**:
- `priority: Priority` - Priority enum value

**Returns**: `str` - Formatted priority string

**Output**:
- `Priority.HIGH` → "🔴 High"
- `Priority.MEDIUM` → "🟡 Medium"
- `Priority.LOW` → "🟢 Low"

**Example**:
```python
formatted = format_priority(task.priority)
# "🟡 Medium"
```

---

### `format_status(is_completed: bool) -> str`

**Purpose**: Format status with icon indicator

**Parameters**:
- `is_completed: bool` - Completion status

**Returns**: `str` - Formatted status string

**Output**:
- `True` → "✓ Complete"
- `False` → "○ Pending"

**Example**:
```python
formatted = format_status(task.is_completed)
# "○ Pending"
```

---

### `format_task_choice(task: Task) -> str`

**Purpose**: Format task for selection menu display

**Parameters**:
- `task: Task` - Task to format

**Returns**: `str` - Formatted choice string

**Output**: `"{id[:8]} │ {title[:40]} │ {priority} │ {status}"`

**Example**:
```python
formatted = format_task_choice(task)
# "a1b2c3d4 │ Buy groceries │ 🟡 Medium │ ○ Pending"
```

---

## Helper Functions (Internal)

```python
def format_created_date(dt: datetime) -> str:
    """Format created timestamp (relative <7 days, absolute >=7 days)."""
    # Returns "2 hours ago", "3 days ago", or "2025-01-15"
    ...

def truncate_title(title: str, max_width: int) -> str:
    """Smart truncate title with ellipsis."""
    # Returns "Very long title..." if exceeds max_width
    ...
```

---

## Dependencies

```python
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from pyfiglet import Figlet
from datetime import datetime, timedelta

from todo.models import Task, Priority
```

---

## Module Exports

```python
__all__ = [
    "console",
    "show_banner",
    "show_success",
    "show_error",
    "show_warning",
    "show_info",
    "show_task_table",
    "show_empty_state",
    "show_task_details",
    "show_help_screen",
    "show_goodbye",
    "format_priority",
    "format_status",
    "format_task_choice",
]

# Usage
from todo import display
display.show_success("Title", "Message")
```

---

## Testing Strategy

Display functions are hard to unit test (visual output). Testing approach:

### 1. Integration Tests
Test that functions don't raise exceptions:
```python
def test_show_success_no_error():
    # Should not raise
    show_success("Test", "Message")
```

### 2. Format Function Tests
Test formatting functions return expected strings:
```python
def test_format_priority():
    assert format_priority(Priority.HIGH) == "🔴 High"
    assert format_priority(Priority.MEDIUM) == "🟡 Medium"
    assert format_priority(Priority.LOW) == "🟢 Low"

def test_format_status():
    assert format_status(True) == "✓ Complete"
    assert format_status(False) == "○ Pending"
```

### 3. Manual Testing
Visual validation in actual terminal:
- Check alignment
- Verify colors display correctly
- Confirm icons render properly
- Test with various terminal widths

---

## Terminal Compatibility

- **Colors**: Fallback to no-color if terminal doesn't support
- **Emojis**: Use unicode emojis (may not render on all terminals)
- **Width**: Rich auto-detects terminal width and adjusts tables
- **Encoding**: UTF-8 required for emoji support

---

## Version

**Contract Version**: 1.0.0  
**Last Updated**: 2025-12-18
