# Quickstart Guide: Phase I Todo CLI

**Feature**: Phase I - In-Memory Python Console Todo App  
**Date**: 2025-12-18  
**Status**: Ready for Implementation

---

## Prerequisites

### Required Software

| Software | Version | Purpose | Installation |
|----------|---------|---------|--------------|
| **Python** | 3.13+ | Runtime environment | https://www.python.org/downloads/ |
| **UV** | Latest | Package manager | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Git** | Any | Version control | https://git-scm.com/downloads |

### Verify Installation

```bash
# Check Python version (must be 3.13+)
python --version

# Check UV installation
uv --version

# Check Git
git --version
```

---

## Project Setup

### 1. Navigate to Project Directory

```bash
cd phase-1
```

### 2. Initialize UV Project (First Time Only)

If `pyproject.toml` doesn't exist:

```bash
uv init
```

### 3. Install Dependencies

```bash
# Install all dependencies (creates/updates venv automatically)
uv sync

# This installs:
# - questionary (interactive CLI)
# - rich (formatted output)
# - pyfiglet (ASCII art)
# - pytest (testing)
# - pytest-cov (coverage)
# - ruff (linting)
```

**Note**: UV automatically creates and manages the virtual environment. No manual `venv` activation needed!

---

## Running the Application

### Basic Usage

```bash
# Run the todo application
uv run todo
```

**What happens**:
1. ASCII art banner displays
2. Main menu appears with options
3. Navigate with arrow keys OR type command shortcuts
4. Select an action to perform

### Interactive Flow Example

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

? What would you like to do? (Use ↑↓ arrows or type command shortcut)
  ➕ Add Task
  📋 List Tasks
  ✏️  Update Task
  🗑️  Delete Task
  ✅ Mark Complete
  ⬜ Mark Incomplete
  ───────────────
  ❓ Help
  🚪 Exit
```

---

## Basic Workflows

### Workflow 1: Add Your First Task

```bash
# 1. Start application
uv run todo

# 2. Select "Add Task" (or type "add")

# 3. Enter task title
? Enter task title: Buy groceries

# 4. Enter description (optional, press Enter to skip)
? Enter task description: Milk, eggs, bread

# 5. Select priority (use arrows)
? Select priority:
  🔴 High
> 🟡 Medium
  🟢 Low

# 6. Success confirmation appears
╭─ ✓ Task Added ──────────────╮
│ Buy groceries               │
│ ID: a1b2c3d4                │
│ Priority: 🟡 Medium         │
│ Status: ○ Pending           │
╰─────────────────────────────╯
```

### Workflow 2: View All Tasks

```bash
# Select "List Tasks" (or type "list")

# Table displays all tasks
┌──────────┬───────────────┬──────────┬──────────┬────────────┐
│ ID       │ Title         │ Priority │ Status   │ Created    │
├──────────┼───────────────┼──────────┼──────────┼────────────┤
│ a1b2c3d4 │ Buy groceries │ 🟡 Medium│ ○ Pending│ 2 hours ago│
└──────────┴───────────────┴──────────┴──────────┴────────────┘

📊 Total: 1 task │ ✓ 0 complete │ ○ 1 pending
```

### Workflow 3: Mark Task Complete

```bash
# Select "Mark Complete" (or type "done")

# Select task from list
? Select task to mark complete:
> a1b2c3d4 │ Buy groceries │ 🟡 Medium │ ○ Pending

# Confirmation appears
╭─ ✓ Task Completed ──────────╮
│ Buy groceries               │
│ ○ Pending → ✓ Complete      │
╰─────────────────────────────╯
```

### Workflow 4: Update Task

```bash
# Select "Update Task" (or type "update")

# Select task
? Select task to update:
> a1b2c3d4 │ Buy groceries │ 🟡 Medium │ ✓ Complete

# Choose what to update
? What would you like to update?
  Title
> Priority
  Description
  All fields

# Update selected field(s)
? Select priority:
  🔴 High
> 🟡 Medium
  🟢 Low

# Before/after comparison
╭─ ✓ Task Updated ────────────╮
│ Priority: 🟡 Medium → 🔴 High│
╰─────────────────────────────╯
```

### Workflow 5: Delete Task

```bash
# Select "Delete Task" (or type "delete")

# Select task
? Select task to delete:
> a1b2c3d4 │ Buy groceries │ 🔴 High │ ✓ Complete

# Task details shown
╭─ Confirm Deletion ──────────╮
│ ID: a1b2c3d4                │
│ Title: Buy groceries        │
│ Description: Milk, eggs     │
│ Priority: 🔴 High           │
│ Status: ✓ Complete          │
│ Created: 2 hours ago        │
╰─────────────────────────────╯

# Confirm deletion
? Are you sure?
> Yes, delete it
  No, keep it

# Success message
╭─ ✓ Task Deleted ────────────╮
│ 'Buy groceries' has been    │
│ removed                     │
╰─────────────────────────────╯
```

---

## Command Reference

### Main Menu Commands

| Command | Shortcut | Description |
|---------|----------|-------------|
| ➕ Add Task | `add` | Add a new task with title, description, priority |
| 📋 List Tasks | `list` | View all tasks in formatted table |
| ✏️  Update Task | `update` | Modify task title, description, or priority |
| 🗑️  Delete Task | `delete` | Remove a task (with confirmation) |
| ✅ Mark Complete | `done` | Mark an incomplete task as complete |
| ⬜ Mark Incomplete | `undone` | Mark a complete task as incomplete |
| ❓ Help | `help` | Show help screen |
| 🚪 Exit | `exit` | Exit application (with confirmation) |

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑` / `↓` | Navigate menu options |
| `Enter` | Select current option |
| `Ctrl+C` | Cancel current operation / Go back |
| Type command | Jump to command (e.g., typing "add" selects Add Task) |

### Command Shortcuts (Partial Matching)

You can type partial commands:
- `a` or `ad` or `add` → Add Task
- `l` or `li` or `list` → List Tasks
- `u` or `up` or `update` → Update Task
- `d` or `de` or `delete` → Delete Task
- `h` or `he` or `help` → Help
- `e` or `ex` or `exit` → Exit

**Note**: Ambiguous shortcuts (e.g., "d" for both "done" and "delete") will show an error with valid options.

---

## Development Commands

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=todo --cov-report=term-missing

# Run with HTML coverage report
uv run pytest --cov=todo --cov-report=html
# Open htmlcov/index.html in browser

# Run specific test file
uv run pytest tests/test_storage.py -v

# Run specific test
uv run pytest tests/test_storage.py::test_add_task -v
```

### Code Quality

```bash
# Lint code (check for issues)
uv run ruff check .

# Lint with auto-fix
uv run ruff check . --fix

# Format code
uv run ruff format .

# Check formatting without changing
uv run ruff format . --check
```

### Development Workflow

```bash
# 1. Make changes to code

# 2. Format code
uv run ruff format .

# 3. Run linter
uv run ruff check .

# 4. Run tests
uv run pytest --cov=todo

# 5. Run application manually
uv run todo
```

---

## Project Structure

```
phase-1/
├── src/
│   └── todo/
│       ├── __init__.py      # Package init (__version__ = "0.1.0")
│       ├── main.py          # Entry point, main loop
│       ├── models.py        # Task, Priority data structures
│       ├── storage.py       # InMemoryStorage service
│       ├── commands.py      # Command handlers
│       └── display.py       # Rich output formatting
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_models.py
│   ├── test_storage.py
│   └── test_commands.py
├── pyproject.toml           # Project configuration
├── README.md                # Project documentation
└── .gitignore
```

---

## Troubleshooting

### Issue: "Command not found: uv"

**Solution**: Install UV package manager

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# Verify installation
uv --version
```

### Issue: "Python version not supported"

**Solution**: Install Python 3.13+

```bash
# Check current version
python --version

# Install Python 3.13+ from https://www.python.org/downloads/
# Or use pyenv:
pyenv install 3.13.0
pyenv local 3.13.0
```

### Issue: "Module not found" errors

**Solution**: Reinstall dependencies

```bash
# Remove existing environment
rm -rf .venv

# Reinstall all dependencies
uv sync
```

### Issue: Emojis not displaying correctly

**Solution**: Ensure terminal supports UTF-8 encoding

```bash
# Check locale
locale

# Set UTF-8 (Linux/macOS)
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# For Windows: Use Windows Terminal or PowerShell 7+
```

### Issue: Colors not showing

**Solution**: Check terminal color support

```bash
# Most modern terminals support colors
# If using Windows CMD, switch to PowerShell or Windows Terminal

# Disable colors (if needed)
export NO_COLOR=1
uv run todo
```

### Issue: Application crashes on Ctrl+C

**Solution**: This is a bug. The application should handle Ctrl+C gracefully. Check implementation of KeyboardInterrupt handling in main loop.

---

## Important Notes

### Data Persistence

⚠️ **WARNING**: All tasks are stored **in-memory only**.

- Tasks are **lost when you exit** the application
- No file persistence in Phase I
- No database storage in Phase I
- Expected behavior per requirements

### Performance

- Target: <1 second to display up to 100 tasks
- Target: <30 seconds to create a task (including all prompts)
- Practical limit: ~100 tasks for optimal performance

### Validation Rules

**Title**:
- Required (cannot be empty)
- Length: 1-200 characters after trimming
- Allows unicode/emojis
- Internal whitespace collapsed to single space

**Description**:
- Optional (can skip)
- Max 1000 characters after trimming
- Allows unicode/emojis
- Internal whitespace collapsed to single space

**Priority**:
- Required selection (defaults to MEDIUM)
- Must choose: HIGH, MEDIUM, or LOW
- Cannot skip priority prompt

---

## Next Steps

1. ✅ Setup complete - Dependencies installed
2. ⏳ Run `/sp.tasks` to generate task breakdown
3. ⏳ Run `/sp.implement` to generate code from specs
4. ⏳ Test the application with `uv run todo`
5. ⏳ Run tests with `uv run pytest --cov=todo`

---

## Support

For issues or questions:
1. Check this quickstart guide
2. Review the [specification](./spec.md)
3. Check the [implementation plan](./plan.md)
4. Review [data model](./data-model.md) and [contracts](./contracts/)

---

## Version

**Quickstart Version**: 1.0.0  
**Application Version**: 0.1.0 (Phase I)  
**Last Updated**: 2025-12-18
