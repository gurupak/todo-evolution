# Phase I Specification: In-Memory Python Console Todo App

## Overview

**Phase:** I of V  
**Objective:** Build an interactive command-line todo application that stores tasks in memory  
**Purpose:** Establish foundation and demonstrate mastery of Spec-Driven Development  
**Level:** Basic Level Functionality (all 5 core features)

This is the starting point of the Evolution of Todo project. A simple, elegant CLI app that will later evolve into a full-stack web application, AI-powered chatbot, and cloud-native distributed system.

## User Stories

### US-1: Add Task

**As a** user  
**I want to** add a new task with title, description, and priority  
**So that** I can track things I need to do

**Acceptance Criteria:**

- Interactive prompt for title (required, 1-200 characters)
- Interactive prompt for description (optional, max 1000 characters)
- Arrow-key dropdown for priority selection (High/Medium/Low)
- Auto-generate UUID for task ID
- Auto-set created_at timestamp
- Default status: incomplete
- Display success confirmation with task details
- Show shortened task ID (first 8 characters)

**Flow:**

```
? Enter task title: Buy groceries
? Enter description (optional): Milk, eggs, bread from Costco
? Select priority: (Use arrow keys)
  🔴 High
❯ 🟡 Medium  
  🟢 Low

╭─ ✓ Task Created ─────────────────────────╮
│  ID:       a1b2c3d4                      │
│  Title:    Buy groceries                 │
│  Priority: 🟡 Medium                     │
│  Status:   ○ Pending                     │
╰──────────────────────────────────────────╯
```

---

### US-2: View Task List

**As a** user  
**I want to** see all my tasks in a formatted table  
**So that** I can review what needs to be done

**Acceptance Criteria:**

- Display tasks in rich formatted table
- Columns: ID (8 chars), Title, Priority (with emoji), Status (with icon), Created
- Status indicators: ✓ for complete, ○ for incomplete
- Priority indicators: 🔴 High, 🟡 Medium, 🟢 Low
- Show helpful message when list is empty
- Display summary: total tasks, complete count, pending count
- Sort by created_at descending (newest first)

**Flow - With Tasks:**

```
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ ID       ┃ Title                ┃ Priority ┃ Status     ┃ Created      ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ a1b2c3d4 │ Buy groceries        │ 🔴 High  │ ○ Pending  │ Dec 17, 2025 │
│ b2c3d4e5 │ Call mom             │ 🟡 Medium│ ✓ Complete │ Dec 16, 2025 │
│ c3d4e5f6 │ Finish report        │ 🟢 Low   │ ○ Pending  │ Dec 15, 2025 │
└──────────┴──────────────────────┴──────────┴────────────┴──────────────┘

📊 Total: 3 tasks │ ✓ 1 complete │ ○ 2 pending
```

**Flow - Empty State:**

```
╭─────────────────────────────────────────────────╮
│  📭 No tasks yet!                               │
│                                                 │
│  Get started by selecting "Add Task" or         │
│  type 'add' to create your first task.          │
╰─────────────────────────────────────────────────╯
```

---

### US-3: Update Task

**As a** user  
**I want to** modify an existing task's details  
**So that** I can correct or improve task information

**Acceptance Criteria:**

- Arrow-key selection to choose task from list
- Arrow-key selection for what to update (Title/Description/Priority/All)
- Show current value as placeholder/default
- Validate task exists
- Preserve original created_at timestamp
- Update the updated_at timestamp
- Show before/after comparison on success

**Flow:**

```
? Select task to update: (Use arrow keys)
❯ a1b2c3d4 │ Buy groceries │ 🔴 High │ ○ Pending
  b2c3d4e5 │ Call mom │ 🟡 Medium │ ✓ Complete
  c3d4e5f6 │ Finish report │ 🟢 Low │ ○ Pending

? What would you like to update? (Use arrow keys)
❯ Title
  Description
  Priority
  All fields

? New title (current: Buy groceries): Get groceries from Costco

╭─ ✓ Task Updated ─────────────────────────╮
│  Before: Buy groceries                   │
│  After:  Get groceries from Costco       │
╰──────────────────────────────────────────╯
```

**Error - No Tasks:**

```
╭─ ⚠ Cannot Update ────────────────────────╮
│  No tasks available to update.           │
│                                          │
│  💡 Create a task first using 'add'      │
╰──────────────────────────────────────────╯
```

---

### US-4: Delete Task

**As a** user  
**I want to** remove a task from my list  
**So that** I can clean up completed or cancelled items

**Acceptance Criteria:**

- Arrow-key selection to choose task from list
- Show task details before confirmation
- Arrow-key Yes/No confirmation (not typing)
- Delete only on explicit confirmation
- Show deletion success message
- Handle empty list gracefully

**Flow:**

```
? Select task to delete: (Use arrow keys)
❯ a1b2c3d4 │ Buy groceries │ 🔴 High │ ○ Pending
  b2c3d4e5 │ Call mom │ 🟡 Medium │ ✓ Complete

╭─ Task Details ───────────────────────────╮
│  ID:          a1b2c3d4                   │
│  Title:       Buy groceries              │
│  Description: Milk, eggs, bread          │
│  Priority:    🔴 High                    │
│  Status:      ○ Pending                  │
│  Created:     Dec 17, 2025 10:30 AM      │
╰──────────────────────────────────────────╯

? Are you sure you want to delete this task? (Use arrow keys)
❯ Yes, delete it
  No, keep it

╭─ ✓ Task Deleted ─────────────────────────╮
│  "Buy groceries" has been removed.       │
╰──────────────────────────────────────────╯
```

**Flow - Cancelled:**

```
? Are you sure you want to delete this task? (Use arrow keys)
  Yes, delete it
❯ No, keep it

ℹ Deletion cancelled. Task was not removed.
```

---

### US-5: Mark Complete / Incomplete

**As a** user  
**I want to** toggle a task's completion status  
**So that** I can track my progress

**Acceptance Criteria:**

- Arrow-key selection showing current status
- Only show relevant tasks (incomplete for "done", complete for "undone")
- Toggle: incomplete → complete sets completed_at
- Toggle: complete → incomplete clears completed_at
- Show status change confirmation with visual feedback
- Handle empty/no-matching-tasks gracefully

**Flow - Mark Complete:**

```
? Select task to mark complete: (Use arrow keys)
❯ ○ a1b2c3d4 │ Buy groceries │ 🔴 High
  ○ c3d4e5f6 │ Finish report │ 🟢 Low

╭─ ✓ Task Completed ───────────────────────╮
│  "Buy groceries" marked as complete!     │
│                                          │
│  ○ Pending  →  ✓ Complete                │
╰──────────────────────────────────────────╯
```

**Flow - Mark Incomplete:**

```
? Select task to mark incomplete: (Use arrow keys)
❯ ✓ b2c3d4e5 │ Call mom │ 🟡 Medium

╭─ ✓ Task Reopened ────────────────────────╮
│  "Call mom" marked as incomplete.        │
│                                          │
│  ✓ Complete  →  ○ Pending                │
╰──────────────────────────────────────────╯
```

**Error - No Tasks to Complete:**

```
╭─ ℹ No Pending Tasks ─────────────────────╮
│  All tasks are already complete!         │
│                                          │
│  💡 Add new tasks or mark some as        │
│     incomplete using 'undone'            │
╰──────────────────────────────────────────╯
```

---

## Data Model

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class Priority(Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    """Represents a todo task."""
    id: UUID = field(default_factory=uuid4)
    title: str = ""                                    # Required, 1-200 characters
    description: str = ""                              # Optional, max 1000 characters
    priority: Priority = Priority.MEDIUM               # Default: MEDIUM
    is_completed: bool = False                         # Default: False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None               # Set when marked complete
```

---

## Main Menu Interface

```
╭──────────────────────────────────────────╮
│         📝 TODO APP - Phase I            │
│         ─────────────────────            │
│         In-Memory Console App            │
╰──────────────────────────────────────────╯

? What would you like to do? (Use arrow keys)
❯ ➕ Add Task
  📋 List Tasks
  ✏️  Update Task
  🗑️  Delete Task
  ✅ Mark Complete
  ⬜ Mark Incomplete
  ❓ Help
  🚪 Exit

Alternative: Type command directly (add, list, update, delete, done, undone, help, exit)
```

---

## Help Screen

```
╭─ 📖 Help ────────────────────────────────────────────────────╮
│                                                              │
│  Commands:                                                   │
│  ─────────                                                   │
│  add      ➕  Create a new task                              │
│  list     📋  View all tasks                                 │
│  update   ✏️   Modify an existing task                       │
│  delete   🗑️   Remove a task                                 │
│  done     ✅  Mark a task as complete                        │
│  undone   ⬜  Mark a task as incomplete                      │
│  help     ❓  Show this help message                         │
│  exit     🚪  Exit the application                           │
│                                                              │
│  Navigation:                                                 │
│  ───────────                                                 │
│  ↑/↓       Navigate options                                  │
│  Enter     Select option                                     │
│  Ctrl+C    Cancel current operation                          │
│  Esc       Return to main menu                               │
│                                                              │
│  💡 Tip: You can type commands directly or use arrow keys    │
│                                                              │
╰──────────────────────────────────────────────────────────────╯
```

---

## Exit Flow

```
? Are you sure you want to exit? (Use arrow keys)
❯ Yes, exit
  No, stay

╭──────────────────────────────────────────╮
│  👋 Goodbye!                             │
│                                          │
│  Your tasks were stored in memory and    │
│  will be lost. See you next time!        │
╰──────────────────────────────────────────╯
```

---

## Module Structure

```
phase-1/
├── src/
│   └── todo/
│       ├── __init__.py      # Package initialization, version
│       ├── main.py          # Entry point, main menu loop ONLY
│       ├── models.py        # Task dataclass, Priority enum
│       ├── storage.py       # InMemoryStorage class (dict-based)
│       ├── commands.py      # Command handlers (add, list, update, delete, done, undone)
│       └── display.py       # Rich formatting utilities (tables, panels, prompts)
├── tests/
│   ├── __init__.py
│   ├── test_models.py       # Task creation, validation tests
│   ├── test_storage.py      # Storage CRUD operation tests
│   ├── test_commands.py     # Command handler tests
│   └── conftest.py          # Pytest fixtures
├── pyproject.toml           # UV project configuration
└── README.md                # Phase I specific instructions
```

---

## Module Responsibilities

### main.py

- Application entry point
- Display welcome banner
- Main menu loop
- Command routing to handlers
- Graceful exit handling
- NO business logic in this file

### models.py

- Task dataclass definition
- Priority enum with HIGH, MEDIUM, LOW
- Model validation helper functions
- Timestamp generation utilities

### storage.py

- InMemoryStorage class implementation
- Internal dict storage: `{task_id: Task}`
- Methods:
  - `add(task: Task) -> Task`
  - `get(task_id: UUID) -> Task | None`
  - `get_all() -> list[Task]`
  - `update(task_id: UUID, **kwargs) -> Task | None`
  - `delete(task_id: UUID) -> bool`
  - `get_pending() -> list[Task]`
  - `get_completed() -> list[Task]`
  - `count() -> dict` (returns total, completed, pending counts)

### commands.py

- `add_task(storage: InMemoryStorage) -> None` - Interactive task creation
- `list_tasks(storage: InMemoryStorage) -> None` - Display task table
- `update_task(storage: InMemoryStorage) -> None` - Interactive update flow
- `delete_task(storage: InMemoryStorage) -> None` - Interactive delete with confirmation
- `mark_complete(storage: InMemoryStorage) -> None` - Mark task as done
- `mark_incomplete(storage: InMemoryStorage) -> None` - Mark task as not done
- `show_help() -> None` - Display help screen

### display.py

- Rich Console instance (singleton)
- `show_banner() -> None` - Display app header
- `show_success(message: str) -> None` - Green success panel
- `show_error(message: str, tip: str = None) -> None` - Red error panel
- `show_info(message: str) -> None` - Blue info panel
- `show_warning(message: str) -> None` - Yellow warning panel
- `show_task_table(tasks: list[Task]) -> None` - Formatted task table
- `show_empty_state() -> None` - No tasks message
- `show_task_details(task: Task) -> None` - Single task detail panel
- `format_priority(priority: Priority) -> str` - Priority with emoji
- `format_status(is_completed: bool) -> str` - Status with icon
- `format_task_choice(task: Task) -> str` - Task as selection option

---

## Dependencies

```toml
# pyproject.toml
[project]
name = "todo-phase1"
version = "0.1.0"
description = "Phase I: In-Memory Python Console Todo App"
requires-python = ">=3.13"
dependencies = [
    "questionary>=2.0.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
]

[project.scripts]
todo = "todo.main:main"
```

---

## Example Session

```
╭──────────────────────────────────────────╮
│         📝 TODO APP - Phase I            │
│         ─────────────────────            │
│         In-Memory Console App            │
╰──────────────────────────────────────────╯

? What would you like to do? Add Task

? Enter task title: Buy groceries
? Enter description (optional): Milk, eggs, bread
? Select priority: Medium

╭─ ✓ Task Created ─────────────────────────╮
│  ID:       a1b2c3d4                      │
│  Title:    Buy groceries                 │
│  Priority: 🟡 Medium                     │
│  Status:   ○ Pending                     │
╰──────────────────────────────────────────╯

? What would you like to do? Add Task

? Enter task title: Call mom
? Enter description (optional): 
? Select priority: High

╭─ ✓ Task Created ─────────────────────────╮
│  ID:       b2c3d4e5                      │
│  Title:    Call mom                      │
│  Priority: 🔴 High                       │
│  Status:   ○ Pending                     │
╰──────────────────────────────────────────╯

? What would you like to do? List Tasks

┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ ID       ┃ Title          ┃ Priority ┃ Status     ┃ Created      ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ b2c3d4e5 │ Call mom       │ 🔴 High  │ ○ Pending  │ Dec 17, 2025 │
│ a1b2c3d4 │ Buy groceries  │ 🟡 Medium│ ○ Pending  │ Dec 17, 2025 │
└──────────┴────────────────┴──────────┴────────────┴──────────────┘

📊 Total: 2 tasks │ ✓ 0 complete │ ○ 2 pending

? What would you like to do? Mark Complete

? Select task to mark complete: b2c3d4e5 │ Call mom │ 🔴 High

╭─ ✓ Task Completed ───────────────────────╮
│  "Call mom" marked as complete!          │
│                                          │
│  ○ Pending  →  ✓ Complete                │
╰──────────────────────────────────────────╯

? What would you like to do? Exit

? Are you sure you want to exit? Yes, exit

╭──────────────────────────────────────────╮
│  👋 Goodbye!                             │
│                                          │
│  Your tasks were stored in memory and    │
│  will be lost. See you next time!        │
╰──────────────────────────────────────────╯
```

---

## Validation Rules

### Title Validation

- Required (cannot be empty or whitespace only)
- Minimum length: 1 character
- Maximum length: 200 characters
- Trim leading/trailing whitespace

### Description Validation

- Optional (can be empty)
- Maximum length: 1000 characters
- Trim leading/trailing whitespace

### Task ID Validation

- Must be valid UUID format
- Must exist in storage for update/delete/done/undone operations

---

## Error Handling

### Invalid Title

```
✗ Error: Title is required
  Please enter a title for your task (1-200 characters)
```

### Title Too Long

```
✗ Error: Title too long
  Maximum 200 characters allowed. You entered 250.
```

### Task Not Found

```
✗ Error: Task not found
  No task exists with ID "xyz12345"
  
  💡 Tip: Use 'list' to see all available tasks
```

### No Tasks Available

```
╭─ ⚠ No Tasks ─────────────────────────────╮
│  There are no tasks to [action].         │
│                                          │
│  💡 Create a task first using 'add'      │
╰──────────────────────────────────────────╯
```

### Keyboard Interrupt (Ctrl+C)

```
ℹ Operation cancelled. Returning to main menu...
```

---

## Deliverables Checklist

### GitHub Repository Must Contain:

- [ ] `.specify/memory/constitution.md` - Generated constitution file
- [ ] `.specify/specs/phase-1/001-basic-todo-cli/` - All spec files (spec.md, plan.md, tasks.md)
- [ ] `phase-1/src/todo/` - All Python source files
- [ ] `phase-1/tests/` - Test files with pytest
- [ ] `phase-1/pyproject.toml` - UV project configuration
- [ ] `phase-1/README.md` - Phase I specific documentation
- [ ] `CLAUDE.md` - Claude Code instructions (root level)
- [ ] `README.md` - Project overview (root level)

### Working Application Must Demonstrate:

- [ ] Add tasks with title, description, and priority (interactive)
- [ ] List all tasks in formatted table with status indicators
- [ ] Update task title, description, or priority (interactive selection)
- [ ] Delete tasks with confirmation (interactive selection)
- [ ] Toggle task completion status (interactive selection)
- [ ] Proper error handling for all edge cases
- [ ] Beautiful CLI output with rich formatting
