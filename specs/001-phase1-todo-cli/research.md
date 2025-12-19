# Phase 0: Research & Technology Validation

**Feature**: Phase I - In-Memory Python Console Todo App  
**Date**: 2025-12-18  
**Status**: Complete

## Overview

This document consolidates research findings for the five key technology areas required for Phase I implementation. All research validates technology choices align with project constitution and spec requirements.

---

## 1. UV Package Manager Best Practices

### Decision
Use UV as the Python package manager for Phase I and all subsequent phases.

### Rationale
- **Speed**: 10-100x faster than pip for dependency resolution and installation
- **Modern**: Built in Rust, designed for Python 3.8+ with current best practices
- **Unified**: Replaces pip, pip-tools, and virtualenv with single tool
- **Auto venv**: Automatically manages virtual environments (no manual activation)
- **Lock files**: Generates `uv.lock` for reproducible installs
- **Compatible**: Works with standard `pyproject.toml` (PEP 621)

### Key Usage Patterns

```bash
# Install UV (one-time setup)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize project (creates pyproject.toml)
uv init

# Add dependencies
uv add questionary rich pyfiglet

# Add dev dependencies
uv add --dev pytest pytest-cov ruff

# Install all dependencies (creates/updates venv automatically)
uv sync

# Run application
uv run todo

# Run any command in the venv
uv run pytest
uv run ruff check .
```

### Project Configuration (pyproject.toml)

```toml
[project]
name = "todo-phase1"
version = "0.1.0"
description = "Phase I: In-Memory Python Console Todo App"
requires-python = ">=3.13"
dependencies = [
    "questionary>=2.0.0",
    "rich>=13.0.0",
    "pyfiglet>=1.0.2",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.8.0",
]

[project.scripts]
todo = "todo.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Alternatives Considered
- **pip + venv**: Slower, requires manual venv management
- **Poetry**: Opinionated dependency format, slower than UV
- **pipenv**: Deprecated, not recommended for new projects

### References
- https://github.com/astral-sh/uv
- https://docs.astral.sh/uv/

---

## 2. questionary Library Patterns

### Decision
Use questionary >=2.0.0 for all interactive CLI prompts.

### Rationale
- **User-friendly**: Arrow-key navigation, visual menus, colored output
- **Validation**: Built-in input validation with custom error messages
- **Flexible**: Supports text, select, confirm, checkbox, password, and more
- **Keyboard interrupt handling**: Gracefully handles Ctrl+C (returns None)
- **Customizable**: Styling, formatting, custom validators

### Core Patterns

#### 1. Main Menu (Select with Icons)

```python
import questionary
from questionary import Choice, Separator

def prompt_main_menu() -> str | None:
    """Display main menu and return selected command."""
    choices = [
        Choice("➕ Add Task", value="add"),
        Choice("📋 List Tasks", value="list"),
        Choice("✏️  Update Task", value="update"),
        Choice("🗑️  Delete Task", value="delete"),
        Choice("✅ Mark Complete", value="done"),
        Choice("⬜ Mark Incomplete", value="undone"),
        Separator(),
        Choice("❓ Help", value="help"),
        Choice("🚪 Exit", value="exit"),
    ]
    
    return questionary.select(
        "What would you like to do?",
        choices=choices,
        instruction="(Use ↑↓ arrows or type command shortcut)",
    ).ask()
```

**Key Features**:
- Returns `None` if user presses Ctrl+C (graceful cancellation)
- `Choice(title, value)` separates display from internal value
- `Separator()` adds visual grouping
- Icons provide visual hierarchy

#### 2. Text Input with Validation

```python
def prompt_title() -> str | None:
    """Prompt for task title with validation."""
    def validate_title(text: str) -> bool | str:
        text = text.strip()
        if len(text) == 0:
            return "Title is required - Please enter a title for your task (1-200 characters)"
        if len(text) > 200:
            return f"Title too long - Maximum 200 characters allowed. You entered {len(text)}"
        return True
    
    return questionary.text(
        "Enter task title:",
        validate=validate_title,
    ).ask()
```

**Key Features**:
- Validator returns `True` (valid) or error message string
- Re-prompts automatically on validation failure
- Returns `None` on Ctrl+C

#### 3. Confirmation Prompts

```python
def prompt_confirm_delete(task_title: str) -> bool:
    """Confirm deletion with Yes/No selection."""
    choices = [
        Choice("Yes, delete it", value=True),
        Choice("No, keep it", value=False),
    ]
    
    result = questionary.select(
        f"Are you sure you want to delete '{task_title}'?",
        choices=choices,
    ).ask()
    
    return result if result is not None else False
```

**Key Features**:
- Boolean return via Choice value
- Explicit yes/no wording (avoid ambiguous "OK/Cancel")
- Default to False if cancelled

#### 4. Task Selection from List

```python
from todo.models import Task

def prompt_select_task(tasks: list[Task], message: str) -> Task | None:
    """Display task list and return selected task."""
    if not tasks:
        return None
    
    choices = [
        Choice(
            f"{str(task.id)[:8]} │ {task.title[:40]} │ {format_priority(task.priority)}",
            value=task
        )
        for task in tasks
    ]
    
    return questionary.select(
        message,
        choices=choices,
    ).ask()
```

**Key Features**:
- Choice value is the actual Task object (not ID string)
- Formatted display with ID | Title | Priority
- Returns `None` if list empty or cancelled

#### 5. Priority Selection

```python
from todo.models import Priority

def prompt_priority(default: Priority = Priority.MEDIUM) -> Priority | None:
    """Prompt for priority level with default."""
    choices = [
        Choice("🔴 High", value=Priority.HIGH),
        Choice("🟡 Medium", value=Priority.MEDIUM),
        Choice("🟢 Low", value=Priority.LOW),
    ]
    
    # Find index of default for initial cursor position
    default_idx = next(i for i, c in enumerate(choices) if c.value == default)
    
    return questionary.select(
        "Select priority:",
        choices=choices,
        default=choices[default_idx],
    ).ask()
```

**Key Features**:
- Enum values as Choice values (type-safe)
- Visual priority indicators (colored circles)
- Default cursor position

### Keyboard Interrupt Handling

All questionary prompts return `None` when user presses Ctrl+C. Handle this consistently:

```python
choice = prompt_main_menu()
if choice is None:  # User pressed Ctrl+C
    display.show_info("ℹ Operation cancelled. Returning to main menu...")
    continue
```

### Alternatives Considered
- **click.prompt**: Less interactive, no arrow-key menus
- **inquirer**: Similar but less actively maintained
- **prompttoolkit**: Lower-level, more complex API

### References
- https://github.com/tmbo/questionary
- https://questionary.readthedocs.io/

---

## 3. rich Library Best Practices

### Decision
Use rich >=13.0.0 for all terminal output formatting.

### Rationale
- **Beautiful output**: Tables, panels, progress bars, syntax highlighting
- **Cross-platform**: Works on Windows, macOS, Linux with proper encoding
- **Theme support**: Custom color schemes and styles
- **Console singleton**: Centralized output control
- **Auto-detection**: Detects terminal capabilities (colors, width, etc.)

### Core Patterns

#### 1. Console Singleton with Theme

```python
# display.py
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

**Why Singleton**: All output uses same console instance for consistent formatting and buffering.

#### 2. Success Panel

```python
from rich.panel import Panel
from rich.text import Text

def show_success(title: str, message: str) -> None:
    """Display success message in green panel."""
    panel = Panel(
        Text(message, style="success"),
        title=f"✓ {title}",
        border_style="green",
        padding=(1, 2),
    )
    console.print(panel)
```

**Output Example**:
```
╭─ ✓ Task Added ──────────────────────────────╮
│                                              │
│  Buy groceries                               │
│  ID: a1b2c3d4                                │
│  Priority: 🟡 Medium                         │
│  Status: ○ Pending                           │
│                                              │
╰──────────────────────────────────────────────╯
```

#### 3. Error Panel with Tip

```python
def show_error(message: str, tip: str | None = None) -> None:
    """Display error message with optional tip."""
    content = Text()
    content.append("✗ ", style="error")
    content.append(message, style="error")
    
    if tip:
        content.append("\n\n")
        content.append("💡 Tip: ", style="info")
        content.append(tip, style="dim")
    
    panel = Panel(
        content,
        border_style="red",
        padding=(1, 2),
    )
    console.print(panel)
```

#### 4. Task Table

```python
from rich.table import Table

def show_task_table(tasks: list[Task]) -> None:
    """Display tasks in formatted table."""
    table = Table(
        title="📋 Your Tasks",
        header_style="bold cyan",
        border_style="dim",
        show_lines=False,
    )
    
    table.add_column("ID", width=10, style="dim")
    table.add_column("Title", min_width=20, max_width=50)
    table.add_column("Priority", justify="center", width=10)
    table.add_column("Status", justify="center", width=12)
    table.add_column("Created", width=14, style="dim")
    
    # Sort by created_at descending (newest first)
    sorted_tasks = sorted(tasks, key=lambda t: t.created_at, reverse=True)
    
    for task in sorted_tasks:
        table.add_row(
            str(task.id)[:8],
            truncate_title(task.title, 50),
            format_priority(task.priority),
            format_status(task.is_completed),
            format_created_date(task.created_at),
        )
    
    console.print(table)
    
    # Summary statistics
    stats = storage.count()
    summary = Text()
    summary.append("📊 Total: ", style="bold")
    summary.append(f"{stats['total']} tasks", style="cyan")
    summary.append(" │ ", style="dim")
    summary.append("✓ ", style="green")
    summary.append(f"{stats['completed']} complete", style="green")
    summary.append(" │ ", style="dim")
    summary.append("○ ", style="yellow")
    summary.append(f"{stats['pending']} pending", style="yellow")
    
    console.print(summary)
```

#### 5. ASCII Art Banner (with pyfiglet)

```python
from pyfiglet import Figlet
from rich.align import Align

def show_banner() -> None:
    """Display application banner with ASCII art."""
    f = Figlet(font="slant")
    ascii_art = f.renderText("TODO")
    
    content = Text()
    content.append(ascii_art.rstrip(), style="cyan bold")
    content.append("\n")
    content.append("─" * 40, style="dim")
    content.append("\n")
    content.append("Phase I: In-Memory Console App", style="dim italic")
    content.append("\n")
    content.append("Version 0.1.0", style="dim")
    
    panel = Panel(
        Align.center(content),
        border_style="cyan",
        padding=(0, 2),
    )
    console.print(panel)
    console.print()  # Blank line after banner
```

#### 6. Empty State

```python
def show_empty_state() -> None:
    """Display message when no tasks exist."""
    content = Text()
    content.append("📭 No tasks yet!\n\n", style="info", justify="center")
    content.append("Get started by adding your first task.", style="dim")
    
    panel = Panel(
        Align.center(content),
        border_style="blue",
        padding=(2, 4),
    )
    console.print(panel)
```

### Helper Functions

```python
from datetime import datetime, timedelta
from todo.models import Priority

def format_priority(priority: Priority) -> str:
    """Format priority with emoji indicator."""
    match priority:
        case Priority.HIGH:
            return "🔴 High"
        case Priority.MEDIUM:
            return "🟡 Medium"
        case Priority.LOW:
            return "🟢 Low"

def format_status(is_completed: bool) -> str:
    """Format status with icon indicator."""
    return "✓ Complete" if is_completed else "○ Pending"

def format_created_date(dt: datetime) -> str:
    """Format created timestamp (relative < 7 days, absolute >= 7 days)."""
    now = datetime.now()
    delta = now - dt
    
    if delta < timedelta(days=7):
        # Relative format
        if delta < timedelta(hours=1):
            minutes = int(delta.total_seconds() / 60)
            return f"{minutes}m ago"
        elif delta < timedelta(days=1):
            hours = int(delta.total_seconds() / 3600)
            return f"{hours}h ago"
        else:
            days = delta.days
            return f"{days}d ago"
    else:
        # Absolute format (YYYY-MM-DD)
        return dt.strftime("%Y-%m-%d")

def truncate_title(title: str, max_width: int) -> str:
    """Smart truncate title with ellipsis."""
    if len(title) <= max_width:
        return title
    return title[:max_width - 3] + "..."
```

### Alternatives Considered
- **colorama**: Color only, no tables/panels
- **tabulate**: Tables only, limited formatting
- **prettytable**: Older, less feature-rich
- **texttable**: Limited styling options

### References
- https://github.com/Textualize/rich
- https://rich.readthedocs.io/

---

## 4. In-Memory Storage Patterns

### Decision
Use dictionary with UUID keys for in-memory task storage.

### Rationale
- **Fast lookups**: O(1) access by UUID
- **Type-safe**: UUID type prevents string/int confusion
- **Standard library**: No external dependencies
- **Simple**: Minimal abstraction over dict
- **Testable**: Easy to mock and verify

### Implementation Pattern

```python
from uuid import UUID
from todo.models import Task

class InMemoryStorage:
    """In-memory task storage using dictionary."""
    
    def __init__(self) -> None:
        """Initialize empty task storage."""
        self._tasks: dict[UUID, Task] = {}
    
    def add(self, task: Task) -> Task:
        """Add a new task to storage."""
        self._tasks[task.id] = task
        return task
    
    def get(self, task_id: UUID) -> Task | None:
        """Get a task by ID, or None if not found."""
        return self._tasks.get(task_id)
    
    def get_all(self) -> list[Task]:
        """Get all tasks."""
        return list(self._tasks.values())
    
    def update(self, task_id: UUID, **kwargs) -> Task | None:
        """Update a task's fields. Returns updated task or None if not found."""
        task = self._tasks.get(task_id)
        if task is None:
            return None
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        # Always update updated_at timestamp
        task.updated_at = datetime.now()
        
        return task
    
    def delete(self, task_id: UUID) -> bool:
        """Delete a task. Returns True if deleted, False if not found."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def get_pending(self) -> list[Task]:
        """Get all incomplete tasks."""
        return [task for task in self._tasks.values() if not task.is_completed]
    
    def get_completed(self) -> list[Task]:
        """Get all completed tasks."""
        return [task for task in self._tasks.values() if task.is_completed]
    
    def count(self) -> dict[str, int]:
        """Get task counts."""
        completed = sum(1 for task in self._tasks.values() if task.is_completed)
        total = len(self._tasks)
        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
        }
```

### Testing Strategy

```python
# tests/test_storage.py
import pytest
from uuid import uuid4
from todo.models import Task, Priority
from todo.storage import InMemoryStorage

def test_add_task(empty_storage):
    task = Task(title="Test Task")
    added = empty_storage.add(task)
    assert added.id == task.id
    assert empty_storage.get(task.id) == task

def test_get_nonexistent_task(empty_storage):
    assert empty_storage.get(uuid4()) is None

def test_update_task(empty_storage):
    task = Task(title="Original")
    empty_storage.add(task)
    
    updated = empty_storage.update(task.id, title="Updated")
    assert updated.title == "Updated"
    assert updated.updated_at > task.created_at

def test_delete_task(empty_storage):
    task = Task(title="To Delete")
    empty_storage.add(task)
    
    assert empty_storage.delete(task.id) is True
    assert empty_storage.get(task.id) is None

def test_get_pending(storage_with_tasks):
    pending = storage_with_tasks.get_pending()
    assert all(not task.is_completed for task in pending)

def test_count(storage_with_tasks):
    counts = storage_with_tasks.count()
    assert counts["total"] == 3
    assert counts["completed"] == 1
    assert counts["pending"] == 2
```

### Alternatives Considered
- **List-based storage**: O(n) lookups, slower
- **SQLite in-memory**: Overkill for Phase I, violates "no database" constraint
- **Third-party libs**: Against constitution (stdlib only for storage)

---

## 5. Python 3.13+ Features

### Decision
Require Python 3.13+ and leverage modern type hints and features.

### Rationale
- **Union types (|)**: Cleaner than `Union[...]` or `Optional[...]`
- **Pattern matching**: More readable than if/elif chains
- **Performance**: CPython 3.13 includes JIT compiler for faster execution
- **Type safety**: Stricter type checking in mypy/pyright

### Key Features to Use

#### 1. Union Type Syntax (PEP 604)

```python
# ✓ Modern (Python 3.10+)
def get_task(task_id: UUID) -> Task | None:
    ...

# ✗ Old style (avoid)
def get_task(task_id: UUID) -> Optional[Task]:
    ...
```

#### 2. Pattern Matching (PEP 634)

```python
# Main menu routing
match choice:
    case "add":
        commands.add_task(storage)
    case "list":
        commands.list_tasks(storage)
    case "update":
        commands.update_task(storage)
    case "delete":
        commands.delete_task(storage)
    case "done":
        commands.mark_complete(storage)
    case "undone":
        commands.mark_incomplete(storage)
    case "help":
        commands.show_help()
    case "exit":
        if prompt_confirm_exit():
            display.show_goodbye()
            break
    case _:
        display.show_error("Unknown command")
```

#### 3. Dataclass with Field Factories

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
    id: UUID = field(default_factory=uuid4)  # Auto-generate UUID
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
```

**Why field factories**: Ensure each instance gets unique UUID and timestamp, not shared across all instances.

#### 4. Enum for Type Safety

```python
from enum import Enum

class Priority(Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Usage
task = Task(title="Buy milk", priority=Priority.HIGH)
```

### Type Checking Configuration

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py313"
select = ["E", "F", "I", "N", "UP", "ANN"]  # Enable type hint checks

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["ANN"]  # Relax annotation rules in tests
```

### Alternatives Considered
- **Python 3.11**: Missing some type hint improvements
- **Python 3.12**: Good, but 3.13 has JIT for better performance
- **Backward compatibility**: Not needed - this is greenfield project

---

## Summary

All technology choices validated and aligned with:
- ✅ Project constitution Phase I requirements
- ✅ Feature specification (spec.md)
- ✅ Code quality standards
- ✅ Best practices for modern Python development

**Ready to proceed to Phase 1: Design & Contracts**
