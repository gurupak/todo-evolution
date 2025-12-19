# Implementation Plan: Phase I - In-Memory Python Console Todo App

**Branch**: `001-phase1-todo-cli` | **Date**: 2025-12-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase1-todo-cli/spec.md`

## Summary

Build an interactive CLI todo application with 5 core features (add, list, update, delete, mark complete/incomplete) using Python 3.13+, questionary for interactive prompts, and rich for beautiful terminal UI. All data stored in-memory with no persistence. Focus on excellent user experience through guided interactions, visual feedback, and graceful error handling.

## Technical Context

**Language/Version**: Python 3.13+  
**Package Manager**: UV (modern, fast Python package manager)  
**Primary Dependencies**: questionary >=2.0.0 (interactive CLI), rich >=13.0.0 (formatted output), pyfiglet >=1.0.2 (ASCII banners)  
**Storage**: In-memory only (Python dict: {UUID: Task})  
**Testing**: pytest >=8.0.0, pytest-cov >=4.0.0  
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)  
**Project Type**: Single project (Python package)  
**Performance Goals**: <1 second list display for 100 tasks, <30 seconds to create a task  
**Constraints**: No external databases, no file persistence, no web frameworks  
**Scale/Scope**: Single-user local app, up to 100 tasks in memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase I Technology Requirements (from constitution.md:173-179)

✅ **PASS** - **UV Package Manager**: Using UV as specified  
✅ **PASS** - **Python 3.13+**: Specified in requirements  
✅ **PASS** - **In-memory storage only**: Using Python dict, no external DB  
✅ **PASS** - **questionary for CLI prompts**: Included in dependencies  
✅ **PASS** - **rich for formatted output**: Included in dependencies  
✅ **PASS** - **Standard Library Only**: Using dataclasses, datetime, uuid, typing, enum  
✅ **PASS** - **No Prohibited Technologies**: No external databases, web frameworks, file persistence, third-party task management libraries, or GUI frameworks

### Spec-Driven Development Workflow (from constitution.md:37-49)

✅ **PASS** - Spec created first (spec.md exists with detailed requirements)  
✅ **PASS** - Planning phase in progress (/sp.plan command)  
⏳ **PENDING** - Task decomposition (/sp.tasks - next step)  
⏳ **PENDING** - Implementation via Claude Code (/sp.implement - future step)  
⏳ **PENDING** - Validation against spec (future step)

### CLI User Experience Standards (from constitution.md:192-227)

✅ **PASS** - **Guided Input**: Using arrow-key menus for selections  
✅ **PASS** - **Progressive Disclosure**: Context-specific options  
✅ **PASS** - **Immediate Feedback**: Success/error panels for all actions  
✅ **PASS** - **Forgiving Input**: Partial prefix matching for command shortcuts  
✅ **PASS** - **Graceful Exit**: Ctrl+C handling, cancellation support  
✅ **PASS** - **Visual Hierarchy**: Colors (green=success, red=error, yellow=warning, blue=info)  
✅ **PASS** - **questionary for prompts**: Required library  
✅ **PASS** - **rich for output**: Required library

### Code Quality Standards (from constitution.md:229-261)

✅ **PASS** - **Type hints**: Planned for all functions and methods  
✅ **PASS** - **Docstrings**: Planned for all public functions/classes  
✅ **PASS** - **Data models**: Using dataclasses for Task model  
✅ **PASS** - **PEP 8**: Will be enforced via ruff  
✅ **PASS** - **Single responsibility**: Module organization follows SoC  
✅ **PASS** - **Function length**: Target max 20 lines  
✅ **PASS** - **File length**: Target max 200 lines  
✅ **PASS** - **No global mutable state**: Storage injected via dependency injection  
✅ **PASS** - **Graceful error handling**: Defined in spec (FR-016, FR-016a)  
✅ **PASS** - **Clear error messages**: Specified in requirements  
✅ **PASS** - **Input validation**: All inputs validated before processing  
✅ **PASS** - **Separation of concerns**: Models, storage, commands, display separated

### Test-First Development (from constitution.md:69-85)

⏳ **PENDING** - Test specifications to be written before implementation  
⏳ **PENDING** - Minimum 80% coverage target  
⏳ **PENDING** - Integration tests priority  
⏳ **PENDING** - All user flows tested  
⏳ **PENDING** - All error paths tested  
⏳ **PENDING** - Edge cases tested

**GATE RESULT**: ✅ **PASS** - All mandatory requirements satisfied. No constitution violations. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-phase1-todo-cli/
├── spec.md              # Feature specification (COMPLETE)
├── plan.md              # This file (IN PROGRESS)
├── research.md          # Phase 0 output (TO BE CREATED)
├── data-model.md        # Phase 1 output (TO BE CREATED)
├── quickstart.md        # Phase 1 output (TO BE CREATED)
├── contracts/           # Phase 1 output (TO BE CREATED - N/A for CLI)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
phase-1/
├── src/
│   └── todo/
│       ├── __init__.py      # Package init, __version__ = "0.1.0"
│       ├── main.py          # Entry point, CLI loop, command routing
│       ├── models.py        # Task dataclass, Priority enum
│       ├── storage.py       # InMemoryStorage class
│       ├── commands.py      # Command handler functions
│       └── display.py       # Rich output formatting
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_models.py       # Task and Priority tests
│   ├── test_storage.py      # InMemoryStorage tests
│   └── test_commands.py     # Command integration tests
├── pyproject.toml           # UV project configuration
├── README.md                # Phase I documentation
└── .gitignore
```

**Structure Decision**: Single project structure selected. This is a standalone CLI application with no frontend/backend split. All code resides in `phase-1/` directory with standard Python package layout under `src/todo/`. Tests mirror the source structure.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations to justify** - All constitution requirements are met.

## Phase 0: Research & Technology Validation

### Research Topics

1. **UV Package Manager Best Practices**
   - Installation and setup
   - Dependency management vs pip/poetry
   - Running scripts with `uv run`
   - Development workflow

2. **questionary Library Patterns**
   - Interactive menu navigation
   - Text input with validation
   - Confirmation prompts
   - Task selection from lists
   - Keyboard interrupt handling

3. **rich Library Best Practices**
   - Panel components for messages
   - Table formatting for task lists
   - Theme customization
   - Console singleton pattern
   - Color schemes

4. **In-Memory Storage Patterns**
   - Dict-based storage strategies
   - UUID as dictionary keys
   - CRUD operation implementations
   - Filtering and counting helpers

5. **Python 3.13+ Features**
   - Type hints with union types (|)
   - dataclass field factories
   - datetime handling
   - Pattern matching (match/case)

**Output**: `research.md` with findings and recommendations

## Phase 1: Design & Contracts

### Data Model

**Entities**:
1. **Task** - Core entity representing a todo item
2. **Priority** - Enum for task importance levels
3. **InMemoryStorage** - Service managing task collection

**Output**: `data-model.md` with entity definitions, relationships, validation rules

### API Contracts

**Note**: CLI applications don't have HTTP APIs. This section documents the **public function signatures** that form the application's internal contract.

**Command Functions** (commands.py):
- `add_task(storage: InMemoryStorage) -> None`
- `list_tasks(storage: InMemoryStorage) -> None`
- `update_task(storage: InMemoryStorage) -> None`
- `delete_task(storage: InMemoryStorage) -> None`
- `mark_complete(storage: InMemoryStorage) -> None`
- `mark_incomplete(storage: InMemoryStorage) -> None`
- `show_help() -> None`

**Storage Functions** (storage.py):
- `add(task: Task) -> Task`
- `get(task_id: UUID) -> Task | None`
- `get_all() -> list[Task]`
- `update(task_id: UUID, **kwargs) -> Task | None`
- `delete(task_id: UUID) -> bool`
- `get_pending() -> list[Task]`
- `get_completed() -> list[Task]`
- `count() -> dict[str, int]`

**Display Functions** (display.py):
- `show_banner() -> None`
- `show_success(title: str, message: str) -> None`
- `show_error(message: str, tip: str | None = None) -> None`
- `show_warning(message: str) -> None`
- `show_info(message: str) -> None`
- `show_task_table(tasks: list[Task]) -> None`
- `show_empty_state() -> None`
- `show_task_details(task: Task) -> None`
- `show_help_screen() -> None`
- `show_goodbye() -> None`
- `format_priority(priority: Priority) -> str`
- `format_status(is_completed: bool) -> str`
- `format_task_choice(task: Task) -> str`

**Output**: Contract documentation in `contracts/` directory (function signatures, type contracts)

### Quickstart Guide

**Output**: `quickstart.md` with:
- Installation steps (UV setup)
- Running the application (`uv run todo`)
- Basic usage flow
- Development commands (test, lint, format)

## Module Dependencies & Build Order

### Dependency Graph

```
main.py
  ├─> commands.py
  │     ├─> storage.py
  │     │     └─> models.py
  │     └─> display.py
  │           └─> models.py
  └─> display.py
        └─> models.py

models.py (no dependencies - foundation)
```

### File Generation Order

Files must be generated in dependency order:

1. `pyproject.toml` - Project configuration
2. `src/todo/__init__.py` - Package init
3. `src/todo/models.py` - Data structures (no deps)
4. `src/todo/storage.py` - Storage class (depends on models)
5. `src/todo/display.py` - Output formatting (depends on models)
6. `src/todo/commands.py` - Business logic (depends on storage, display)
7. `src/todo/main.py` - Entry point (depends on commands, display)
8. `tests/conftest.py` - Test fixtures
9. `tests/test_models.py` - Model tests
10. `tests/test_storage.py` - Storage tests
11. `tests/test_commands.py` - Command tests
12. `README.md` - Documentation

## Implementation Strategy

### Separation of Concerns

| Module | Responsibility | Dependencies | Lines (est.) |
|--------|---------------|--------------|--------------|
| `models.py` | Data structures only (Task, Priority) | stdlib (dataclasses, datetime, enum, uuid) | ~50 |
| `storage.py` | CRUD operations on in-memory dict | models | ~80 |
| `display.py` | All Rich formatting and output | rich, models | ~150 |
| `commands.py` | User interaction flows, business logic | questionary, storage, display | ~200 |
| `main.py` | Entry point, main loop, command routing | commands, display | ~60 |

### Key Design Patterns

1. **Dependency Injection**: Storage instance injected into all command functions
2. **Singleton Console**: Single Rich console instance with custom theme
3. **Enum for Priority**: Type-safe priority levels
4. **Dataclass for Task**: Immutable data with defaults
5. **Pure Functions**: Commands are side-effect functions (void return)
6. **Validation at Boundary**: Input validation in prompts before processing

### Error Handling Strategy

**User Input Errors**:
- Invalid title/description: Questionary validators re-prompt with message
- Task not found: Display warning panel with actionable tip
- Empty task list: Display empty state panel with guidance
- Ambiguous command shortcut: Display error with valid options

**System Errors**:
- `KeyboardInterrupt` (Ctrl+C): Catch, display info message, continue loop
- Unexpected exceptions: Catch, display error panel with technical details logged, return to main menu

**Validation Rules**:
- **Title**: Required, 1-200 chars, trim whitespace, normalize internal whitespace, allow unicode/emojis, strip control chars
- **Description**: Optional, max 1000 chars, trim whitespace, normalize internal whitespace, allow unicode/emojis, strip control chars
- **Priority**: Must be valid enum (HIGH, MEDIUM, LOW), default MEDIUM, required selection
- **Task ID**: Must exist in storage for update/delete/mark operations

## Testing Strategy

### Test Structure

```
tests/
├── conftest.py          # Shared fixtures (empty_storage, storage_with_tasks, sample_task)
├── test_models.py       # Task creation, defaults, Priority enum
├── test_storage.py      # All CRUD operations, filtering, counting
└── test_commands.py     # Command handler integration tests (with mocked questionary)
```

### Test Coverage Goals

| Module | Target Coverage | Focus Areas |
|--------|----------------|-------------|
| models.py | 100% | Task creation, field defaults, Priority enum values |
| storage.py | 100% | CRUD operations, edge cases, filtering, counting |
| commands.py | 80% | User flow integration, error handling (mocked input) |
| display.py | 60% | Format functions (visual output testing limited) |
| main.py | 40% | Main loop integration (minimal - hard to test interactively) |

### Testing Commands

```bash
# Run all tests
uv run pytest

# With coverage report
uv run pytest --cov=todo --cov-report=term-missing --cov-report=html

# Specific test file
uv run pytest tests/test_storage.py -v

# Watch mode (requires pytest-watch)
uv run ptw
```

## Development Workflow

### Setup

```bash
# Clone repository and navigate to phase-1
cd phase-1

# Install dependencies (UV handles venv automatically)
uv sync

# Run application
uv run todo

# Run tests
uv run pytest

# Lint code
uv run ruff check .

# Format code
uv run ruff format .
```

### Daily Development

1. Write/update specs first
2. Generate tests from acceptance criteria
3. Generate implementation via Claude Code
4. Run tests: `uv run pytest --cov=todo`
5. Lint: `uv run ruff check .`
6. Format: `uv run ruff format .`
7. Manual testing in CLI
8. Refine spec if needed (never edit code manually)

## Next Steps

1. ✅ Complete this plan.md
2. ⏳ Generate research.md (Phase 0)
3. ⏳ Generate data-model.md (Phase 1)
4. ⏳ Generate contracts/ (Phase 1)
5. ⏳ Generate quickstart.md (Phase 1)
6. ⏳ Update agent context (CLAUDE.md)
7. ⏳ Run /sp.tasks to generate tasks.md
8. ⏳ Run /sp.implement to generate code
