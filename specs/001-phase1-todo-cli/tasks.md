# Implementation Tasks: Phase I - In-Memory Python Console Todo App

**Feature**: Phase I Todo CLI  
**Branch**: `001-phase1-todo-cli`  
**Date**: 2025-12-18  
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

---

## Task Summary

| Phase | User Story | Task Count | Can Run In Parallel |
|-------|------------|------------|---------------------|
| Phase 1 | Setup | 3 | No (sequential setup) |
| Phase 2 | Foundational | 3 | Yes (independent modules) |
| Phase 3 | US1: Add New Task (P1) | 4 | Partial (display before commands) |
| Phase 4 | US2: View Task List (P1) | 2 | Yes (after Phase 3 complete) |
| Phase 5 | US3: Update Task (P2) | 1 | Yes (after Phase 2 complete) |
| Phase 6 | US4: Delete Task (P2) | 1 | Yes (after Phase 2 complete) |
| Phase 7 | US5: Mark Complete/Incomplete (P2) | 2 | Yes (after Phase 2 complete) |
| Phase 8 | Integration & Polish | 3 | No (requires all features) |
| Phase 9 | Due Date Feature (Enhancement) | 9 | Yes (after Phase 2 complete) |
| **Total** | **5 User Stories + 1 Enhancement** | **28 Tasks** | **19 parallelizable** |

---

## Dependencies & Execution Order

### Critical Path (Must Complete First)
```
Phase 1 (Setup) → Phase 2 (Foundation) → Phase 3 (US1: Add Task) → Phase 4 (US2: List Tasks)
```

**Minimum Viable Product (MVP)**: Phase 1 + Phase 2 + Phase 3 + Phase 4 = User can add and view tasks

### Parallel Opportunities

**After Phase 2 Complete**:
- Phase 5 (Update), Phase 6 (Delete), Phase 7 (Mark Complete) can run in parallel
- All depend only on foundational modules (models, storage, display)
- Independent user stories with no cross-dependencies

**Phase 3 Internal Parallelization**:
- T007 (display functions) and T008 (add_task command) can run in parallel after T006 (storage) completes

---

## Phase 1: Project Setup

**Goal**: Initialize Phase I project structure with UV package manager and dependencies

**Prerequisites**: None

**Tasks**:

- [x] T001 Create phase-1 directory structure per plan.md (phase-1/src/todo/, phase-1/tests/)
- [x] T002 Create pyproject.toml with UV configuration, dependencies (questionary>=2.0.0, rich>=13.0.0, pyfiglet>=1.0.2), dev dependencies (pytest>=8.0.0, pytest-cov>=4.0.0, ruff>=0.8.0), and project metadata (name="todo-phase1", version="0.1.0") in phase-1/pyproject.toml
- [x] T003 Create phase-1/src/todo/__init__.py with __version__ = "0.1.0"

**Acceptance**: `uv sync` runs successfully and installs all dependencies without errors

---

## Phase 2: Foundational Modules

**Goal**: Implement core data structures and infrastructure needed by all user stories

**Prerequisites**: Phase 1 complete

**Independent Test**: All foundation modules can be tested independently without user-facing features

**Tasks**:

- [x] T004 [P] Implement Priority enum (HIGH, MEDIUM, LOW) and Task dataclass with all fields (id, title, description, priority, is_completed, created_at, updated_at, completed_at) using field factories for UUID and timestamps in phase-1/src/todo/models.py
- [x] T005 [P] Implement InMemoryStorage class with all CRUD methods (add, get, get_all, update, delete, get_pending, get_completed, count) using dict[UUID, Task] storage in phase-1/src/todo/storage.py
- [x] T006 [P] Create rich Console singleton with custom theme (success=green bold, error=red bold, warning=yellow bold, info=blue) in phase-1/src/todo/display.py

**Acceptance**: 
- `from todo.models import Task, Priority` works
- `storage = InMemoryStorage(); storage.add(Task(title="Test"))` works
- `from todo.display import console` works

---

## Phase 3: User Story 1 - Add New Task (P1)

**User Story**: As a user, I want to add a new task with title, description, and priority so that I can track things I need to do.

**Why P1**: Creating tasks is the foundational action - without this, no other features provide value. This is the minimum viable product.

**Independent Test**: Launch app, select "Add Task", enter details, verify success panel displays with correct task information

**Prerequisites**: Phase 2 complete (models, storage, display foundation)

**Acceptance Criteria**:
1. ✓ Success panel displays task ID (first 8 chars), title, priority with emoji, status
2. ✓ Whitespace is trimmed from title/description
3. ✓ Title >200 chars shows error and re-prompts
4. ✓ Empty title shows error and re-prompts
5. ✓ Description can be skipped (empty string)
6. ✓ Priority selection shows emojis (🔴 High, 🟡 Medium, 🟢 Low)

**Tasks**:

- [x] T007 [P] [US1] Implement display functions for add task flow: show_success(title, message), show_banner() with pyfiglet ASCII art, format_priority(priority) returning emoji string in phase-1/src/todo/display.py
- [x] T008 [US1] Implement add_task(storage) command with questionary prompts for title (validated 1-200 chars), description (optional, max 1000 chars), priority (default MEDIUM, required selection), create Task, save to storage, display success panel in phase-1/src/todo/commands.py
- [x] T009 [US1] Implement main() entry point with storage initialization, show_banner(), main menu loop with questionary.select for command routing including "Add Task" option, KeyboardInterrupt handling in phase-1/src/todo/main.py
- [x] T010 [US1] Create tests for add_task flow: test task creation, test title validation (empty, too long, whitespace trimming), test description optional, test priority default in phase-1/tests/test_commands.py

**Test Command**: `uv run pytest tests/test_commands.py::test_add_task -v`

**Manual Test**: `uv run todo` → Select "Add Task" → Enter "Buy milk" → Skip description → Select Medium → Verify success panel

---

## Phase 4: User Story 2 - View Task List (P1)

**User Story**: As a user, I want to see all my tasks in a formatted table so that I can review what needs to be done.

**Why P1**: Viewing tasks is essential - users need to see what they've created. Together with Add Task, this forms the MVP.

**Independent Test**: Create 2-3 tasks with different priorities/statuses, select "List Tasks", verify table displays with all columns, correct sorting (newest first), and summary statistics

**Prerequisites**: Phase 3 complete (can create tasks to list)

**Acceptance Criteria**:
1. ✓ Table displays columns: ID (8 chars), Title (truncated), Priority (emoji), Status (icon), Created (relative/absolute)
2. ✓ Tasks sorted by created_at descending (newest first)
3. ✓ Summary shows "📊 Total: X tasks │ ✓ Y complete │ ○ Z pending"
4. ✓ Empty state shows "📭 No tasks yet!" with guidance
5. ✓ Priority column shows 🔴/🟡/🟢 emojis
6. ✓ Status column shows ✓ Complete or ○ Pending

**Tasks**:

- [x] T011 [US2] Implement show_task_table(tasks) with rich Table (columns: ID, Title, Priority, Status, Created), show_empty_state() panel, format_status(is_completed), format_created_date(dt) helper (relative <7 days, absolute >=7 days), truncate_title(title, max_width) helper in phase-1/src/todo/display.py
- [x] T012 [US2] Implement list_tasks(storage) command: retrieve all tasks, check empty (show empty state), sort by created_at desc, display table, show summary statistics using storage.count() in phase-1/src/todo/commands.py, add "List Tasks" option to main menu in phase-1/src/todo/main.py

**Test Command**: `uv run pytest tests/test_commands.py::test_list_tasks -v`

**Manual Test**: `uv run todo` → Add 2 tasks → Select "List Tasks" → Verify table with 2 rows and summary

---

## Phase 5: User Story 3 - Update Task Details (P2)

**User Story**: As a user, I want to modify an existing task's details so that I can correct or improve task information.

**Why P2**: Updating improves usability but isn't required for MVP. Users can still track tasks without this feature.

**Independent Test**: Create task, select "Update Task", choose task, select field to update, verify before/after comparison displays correctly

**Prerequisites**: Phase 2 complete (models, storage, display)

**Acceptance Criteria**:
1. ✓ Task selection menu shows all tasks with ID │ Title │ Priority │ Status
2. ✓ Update options: Title, Description, Priority, All fields
3. ✓ Current value shown as placeholder/default
4. ✓ Success panel shows before/after comparison
5. ✓ created_at unchanged, updated_at set to current time
6. ✓ Empty task list shows warning with tip

**Tasks**:

- [x] T013 [US3] Implement update_task(storage) command with task selection, update field selection (Title/Description/Priority/All), prompts with current values as defaults, storage.update() call, before/after comparison display, empty state handling in phase-1/src/todo/commands.py, implement show_warning(message) and format_task_choice(task) in phase-1/src/todo/display.py, add "Update Task" to main menu in phase-1/src/todo/main.py

**Test Command**: `uv run pytest tests/test_commands.py::test_update_task -v`

**Manual Test**: `uv run todo` → Add task → Select "Update Task" → Change title → Verify before/after shown

---

## Phase 6: User Story 4 - Delete Task (P2)

**User Story**: As a user, I want to remove a task from my list so that I can clean up completed or cancelled items.

**Why P2**: Deletion helps maintain clean list but isn't essential for core functionality.

**Independent Test**: Create task, select "Delete Task", view task details, confirm deletion, verify task removed from list

**Prerequisites**: Phase 2 complete (models, storage, display)

**Acceptance Criteria**:
1. ✓ Task selection shows all tasks with ID │ Title │ Priority │ Status
2. ✓ Confirmation panel shows full task details (ID, Title, Description, Priority, Status, Created)
3. ✓ "Yes, delete it" removes task with success message showing title
4. ✓ "No, keep it" shows cancellation message, task remains
5. ✓ Empty task list shows warning
6. ✓ Deleted task no longer in list

**Tasks**:

- [x] T014 [US4] Implement delete_task(storage) command with task selection, show_task_details(task) confirmation panel, yes/no confirmation prompt, storage.delete() call, success/cancellation messages, empty state handling in phase-1/src/todo/commands.py, implement show_task_details(task) in phase-1/src/todo/display.py, add "Delete Task" to main menu in phase-1/src/todo/main.py

**Test Command**: `uv run pytest tests/test_commands.py::test_delete_task -v`

**Manual Test**: `uv run todo` → Add task → Select "Delete Task" → Confirm → Verify task gone

---

## Phase 7: User Story 5 - Mark Complete/Incomplete (P2)

**User Story**: As a user, I want to toggle a task's completion status so that I can track my progress.

**Why P2**: Tracking completion is valuable but not essential for MVP.

**Independent Test**: Create 2 incomplete tasks, mark one complete, verify status change, mark it incomplete, verify reverse operation

**Prerequisites**: Phase 2 complete (models, storage, display)

**Acceptance Criteria**:
1. ✓ Mark Complete shows only incomplete tasks (○ prefix)
2. ✓ Marking complete sets is_completed=True, completed_at=now(), shows "○ Pending → ✓ Complete"
3. ✓ Mark Incomplete shows only completed tasks (✓ prefix)
4. ✓ Marking incomplete sets is_completed=False, completed_at=None, shows "✓ Complete → ○ Pending"
5. ✓ All complete shows info "All tasks are already complete!"
6. ✓ No complete tasks shows info "No completed tasks to mark incomplete"

**Tasks**:

- [x] T015 [P] [US5] Implement mark_complete(storage) command with get_pending() filter, task selection from incomplete tasks, storage.update(is_completed=True, completed_at=now()), status change confirmation "○ → ✓", all-complete info message in phase-1/src/todo/commands.py, add "Mark Complete" to main menu in phase-1/src/todo/main.py
- [x] T016 [P] [US5] Implement mark_incomplete(storage) command with get_completed() filter, task selection from complete tasks, storage.update(is_completed=False, completed_at=None), status change confirmation "✓ → ○", no-complete info message in phase-1/src/todo/commands.py, add "Mark Incomplete" to main menu in phase-1/src/todo/main.py

**Test Command**: `uv run pytest tests/test_commands.py::test_mark_complete tests/test_commands.py::test_mark_incomplete -v`

**Manual Test**: `uv run todo` → Add task → Mark Complete → Verify ✓ → Mark Incomplete → Verify ○

---

## Phase 8: Integration & Polish

**Goal**: Complete remaining UI features, help system, exit confirmation, and comprehensive testing

**Prerequisites**: All user stories (Phases 3-7) complete

**Tasks**:

- [x] T017 Implement show_help() command displaying help panel with command list (shortcuts), navigation tips (arrows, Ctrl+C), 2-3 usage examples in phase-1/src/todo/commands.py, implement show_help_screen() in phase-1/src/todo/display.py, add "Help" and "Exit" options to main menu in phase-1/src/todo/main.py with exit confirmation prompt and show_goodbye() panel
- [x] T018 Implement show_info(message) and show_error(message, tip) display functions with Panel formatting in phase-1/src/todo/display.py, update all commands to use show_info() for Ctrl+C cancellations and show_error() for validation failures
- [x] T019 Create comprehensive test suite: phase-1/tests/conftest.py with fixtures (empty_storage, storage_with_tasks, sample_task), phase-1/tests/test_models.py (Task creation, Priority enum), phase-1/tests/test_storage.py (all CRUD ops, filtering, counting), run full test suite with coverage report

**Test Command**: `uv run pytest --cov=todo --cov-report=term-missing`

**Acceptance**: 
- ✓ All 19 tasks complete
- ✓ Help screen displays correctly
- ✓ Exit confirmation works
- ✓ Ctrl+C handled gracefully in all flows
- ✓ All error messages user-friendly with tips
- ✓ Test coverage ≥80% for models and storage

---

## Phase 9: Due Date Feature (Enhancement)

**Goal**: Add optional due date field to tasks with validation and display

**Prerequisites**: Phase 2 (Foundation) complete

**Tasks**:

- [ ] T020 Update Task dataclass in phase-1/src/todo/models.py to add `due_date: date | None = None` field, import date from datetime
- [ ] T021 Add due date prompt in add_task() command before priority selection in phase-1/src/todo/commands.py: prompt for optional date (YYYY-MM-DD format), validate format, validate not in past, allow skip with Enter, normalize and store as date object
- [ ] T022 Add due date validation helper function _validate_due_date(date_str: str) -> date | None in phase-1/src/todo/commands.py: parse YYYY-MM-DD format, validate not in past, return date object or None if invalid with error message
- [ ] T023 Update show_task_table() in phase-1/src/todo/display.py to add "Due Date" column showing date in YYYY-MM-DD format or "-" if None, add visual indicator (🔴) for overdue tasks
- [ ] T024 Update show_task_details() in phase-1/src/todo/display.py to display due date with overdue indicator if applicable
- [ ] T025 Add due date to update_task() command options in phase-1/src/todo/commands.py: add "Due Date" option to update menu, prompt with current value as default
- [ ] T026 Update test fixtures in phase-1/tests/conftest.py to include tasks with and without due dates
- [ ] T027 Add tests for due date validation in phase-1/tests/test_commands.py: test valid date, invalid format, past date, skip/optional, overdue detection
- [ ] T028 Update show_success() display for add_task in phase-1/src/todo/display.py to show due date in task creation confirmation panel

**Test Command**: `uv run pytest tests/test_commands.py -k due_date -v`

**Acceptance**:
- ✓ Users can optionally provide due date when creating tasks
- ✓ Due date format validated as YYYY-MM-DD
- ✓ Past dates rejected with error message
- ✓ Due date displayed in task list with overdue indicator
- ✓ Due date can be updated via update command
- ✓ Empty due date (press Enter to skip) works correctly
- ✓ Tests pass with due date scenarios

---

## Task Execution Strategy

### MVP-First Approach (Recommended)

**Week 1 - MVP**: Phases 1-4 only
- Day 1: Phase 1 (Setup) + Phase 2 (Foundation)
- Day 2: Phase 3 (Add Task - US1)
- Day 3: Phase 4 (List Tasks - US2)
- **Deliverable**: Working todo app where users can add and view tasks

**Week 2 - Full Feature Set**: Phases 5-8
- Day 4: Phase 5 (Update - US3) + Phase 6 (Delete - US4) in parallel
- Day 5: Phase 7 (Mark Complete - US5) + Phase 8 (Polish)
- **Deliverable**: Complete Phase I with all 5 user stories

### Parallel Execution Example

**After Phase 2 Complete** (Foundation Ready):
```bash
# Developer A
git checkout -b feature/update-task
# Implement T013 (Update Task)

# Developer B (parallel)
git checkout -b feature/delete-task
# Implement T014 (Delete Task)

# Developer C (parallel)
git checkout -b feature/mark-complete
# Implement T015 + T016 (Mark Complete/Incomplete)
```

All three can work simultaneously - no code conflicts (separate functions in commands.py).

### Sequential Dependencies

**MUST Complete in Order**:
1. T001-T003 (Setup) → T004-T006 (Foundation) → T007-T010 (Add Task) → T011-T012 (List Tasks)

**After Foundation (T004-T006)**:
- T013-T016 can run in parallel (independent user stories)

**After All Features (T007-T016)**:
- T017-T019 (Integration & Polish)

---

## Validation Checklist

Before marking Phase complete:

### Phase 1 (Setup)
- [ ] `uv sync` runs without errors
- [ ] `uv run python -c "import todo"` works
- [ ] Directory structure matches plan.md

### Phase 2 (Foundation)
- [ ] `from todo.models import Task, Priority` succeeds
- [ ] `storage = InMemoryStorage(); storage.add(Task(title="Test"))` works
- [ ] `from todo.display import console` succeeds

### Phase 3 (US1: Add Task)
- [ ] `uv run todo` launches and shows banner
- [ ] Can add task with all fields
- [ ] Title validation works (empty, too long, trimming)
- [ ] Success panel displays correctly

### Phase 4 (US2: List Tasks)
- [ ] Empty state displays when no tasks
- [ ] Table displays with all columns
- [ ] Tasks sorted newest first
- [ ] Summary statistics correct

### Phase 5-7 (US3-5: Update/Delete/Complete)
- [ ] Each feature works independently
- [ ] Empty state handling correct
- [ ] Confirmation prompts work
- [ ] Status change messages display

### Phase 8 (Polish)
- [ ] Help screen comprehensive
- [ ] Exit confirmation works
- [ ] Ctrl+C handled in all flows
- [ ] All tests pass with ≥80% coverage

---

## Testing Strategy

### Unit Tests (phase-1/tests/)

**test_models.py**:
- Task creation with required/optional fields
- UUID auto-generation
- Timestamp auto-setting
- Priority enum values

**test_storage.py**:
- CRUD operations (add, get, update, delete)
- Filtering (get_pending, get_completed)
- Counting (total, completed, pending)
- Edge cases (not found, empty storage)

**test_commands.py** (mocked questionary):
- add_task with valid/invalid input
- list_tasks with empty/populated storage
- update_task field updates
- delete_task with confirmation
- mark_complete/incomplete status changes

### Integration Tests

**Manual Testing Checklist**:
1. Add 3 tasks with different priorities
2. List tasks - verify table and summary
3. Update a task's title
4. Mark a task complete
5. Delete a task with confirmation
6. Try to update with no tasks (verify warning)
7. Press Ctrl+C during add (verify cancellation)
8. View help screen
9. Exit with confirmation

### Coverage Goals

| Module | Target Coverage |
|--------|----------------|
| models.py | 100% |
| storage.py | 100% |
| display.py | 60% (visual functions hard to test) |
| commands.py | 80% |
| main.py | 40% (integration testing preferred) |

**Run Coverage**: `uv run pytest --cov=todo --cov-report=html`

---

## Next Steps

1. ✅ Tasks.md generated (this file)
2. ⏳ Run `/sp.implement` to generate code from tasks
3. ⏳ Execute tasks in order (T001 → T019)
4. ⏳ Run tests after each phase
5. ⏳ Manual testing for user flows
6. ⏳ Coverage report validation

---

## Summary

**Total Tasks**: 19  
**Parallelizable**: 10 tasks (53%)  
**User Stories**: 5 (2 P1, 3 P2)  
**MVP Scope**: Phases 1-4 (9 tasks) = Add + List Tasks  
**Full Feature Set**: All 8 phases (19 tasks)  

**Estimated Effort**:
- Setup & Foundation: 2-3 hours
- MVP (US1 + US2): 4-6 hours
- Additional Features (US3-5): 3-4 hours
- Polish & Testing: 2-3 hours
- **Total**: 11-16 hours for complete Phase I

**Ready for implementation** ✅
