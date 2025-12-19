# Feature Specification: Phase I - In-Memory Python Console Todo App

**Feature Branch**: `001-phase1-todo-cli`  
**Created**: 2025-12-18  
**Status**: Draft  
**Input**: User description: "Phase I: In-Memory Python Console Todo App - Build an interactive CLI todo application with 5 core features (add, list, update, delete, mark complete/incomplete) using Python 3.13+, questionary, and rich libraries for beautiful terminal UI"

## Clarifications

### Session 2025-12-18

- Q: The specification mentions both arrow-key menu navigation and direct command typing (FR-002), but the interaction model is unclear. → A: Main menu shows options, user can navigate with arrows OR type command shortcuts (e.g., typing "add" while menu is visible jumps to Add task)
- Q: The Created timestamp display format is not specified (FR-011 mentions "Created (formatted date)" but doesn't define the format). → A: Relative format for recent tasks (e.g., "2 hours ago", "3 days ago"), absolute date for older (e.g., "2025-01-15") with threshold at 7 days
- Q: The Title field truncation behavior for the table display is not specified. Long titles could break table formatting. → A: Smart truncate based on terminal width: allocate proportional space to Title column, truncate with ellipsis if exceeds available space
- Q: The spec mentions "version" in the welcome banner (FR-021) but doesn't specify versioning strategy or initial version number. → A: Semantic versioning starting at 0.1.0 (phase 1 = 0.1.0, future phases increment minor version)
- Q: The Help screen content structure (FR-022) is mentioned but not defined. What information should it include? → A: Comprehensive: command list with shortcuts, navigation tips (arrow keys, Ctrl+C), and 2-3 usage examples
- Q: The spec describes command shortcuts (e.g., typing "add" while menu is visible) but doesn't specify the exact matching behavior. → A: Partial prefix matching (e.g., "a" → "add", "l" → "list", "u" → "update") with error on ambiguous matches
- Q: The specification mentions handling Ctrl+C gracefully (FR-016), but doesn't specify behavior for unexpected errors or exceptions during task operations. → A: Graceful degradation: catch exceptions, display user-friendly error panel, log technical details to console, return to main menu
- Q: The spec doesn't specify the default priority when creating tasks through the interactive prompts. → A: Default to MEDIUM priority with explicit selection required (no skip option)
- Q: The spec defines validation for title (1-200 chars) and description (max 1000 chars), but doesn't specify handling for special characters, newlines, or control characters. → A: Allow all printable characters including emojis/unicode, normalize whitespace (collapse multiple spaces/newlines to single space), strip control characters
- Q: The spec mentions displaying success/error/info/warning messages with colored output (FR-023), but doesn't specify the visual presentation format. → A: Rich panels with icons, colored borders, and formatted text (e.g., ✓ Success in green panel with border)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add New Task (Priority: P1)

As a user, I want to add a new task with title, description, and priority so that I can track things I need to do.

**Why this priority**: Creating tasks is the foundational action - without the ability to add tasks, no other features can be tested or provide value. This is the minimum viable product.

**Independent Test**: Can be fully tested by launching the app, selecting "Add Task", entering task details through interactive prompts, and verifying the success confirmation displays correct task information. Delivers immediate value as users can start capturing tasks.

**Acceptance Scenarios**:

1. **Given** the main menu is displayed, **When** I select "Add Task" and enter title "Buy groceries", description "Milk, eggs, bread", and priority "Medium", **Then** a success panel displays showing task ID (first 8 chars), title, priority with emoji (🟡 Medium), and status (○ Pending)
2. **Given** the add task flow is active, **When** I enter a title with leading/trailing whitespace "  Meeting notes  ", **Then** the system trims whitespace and stores "Meeting notes"
3. **Given** the title prompt is displayed, **When** I enter a title longer than 200 characters, **Then** an error displays "Title too long - Maximum 200 characters allowed. You entered [count]"
4. **Given** the title prompt is displayed, **When** I enter only whitespace or leave it empty, **Then** an error displays "Title is required - Please enter a title for your task (1-200 characters)"
5. **Given** the description prompt is displayed, **When** I skip the description (press Enter), **Then** the task is created with an empty description
6. **Given** the priority selection is displayed, **When** I use arrow keys to select "High", **Then** the priority is set to HIGH and displays with 🔴 emoji

---

### User Story 2 - View Task List (Priority: P1)

As a user, I want to see all my tasks in a formatted table so that I can review what needs to be done.

**Why this priority**: Viewing tasks is essential to make the app useful - users need to see what they've created. Together with P1 Add Task, this forms the minimal viable product.

**Independent Test**: Can be fully tested by creating 2-3 tasks with different priorities and statuses, then selecting "List Tasks" to verify the rich formatted table displays correctly with all columns, proper sorting (newest first), and summary statistics.

**Acceptance Scenarios**:

1. **Given** I have 3 tasks in the system, **When** I select "List Tasks", **Then** a formatted table displays with columns: ID (8 chars), Title, Priority (with emoji), Status (with icon), Created (formatted date)
2. **Given** I have tasks with different creation times, **When** I list tasks, **Then** they are sorted by created_at descending (newest first)
3. **Given** I have 2 complete and 3 pending tasks, **When** I list tasks, **Then** the summary shows "📊 Total: 5 tasks │ ✓ 2 complete │ ○ 3 pending"
4. **Given** I have no tasks in the system, **When** I select "List Tasks", **Then** an empty state panel displays "📭 No tasks yet!" with helpful guidance to add first task
5. **Given** tasks are displayed, **When** I view the Priority column, **Then** High shows 🔴, Medium shows 🟡, Low shows 🟢
6. **Given** tasks are displayed, **When** I view the Status column, **Then** complete tasks show ✓ Complete and incomplete show ○ Pending

---

### User Story 3 - Update Task Details (Priority: P2)

As a user, I want to modify an existing task's details so that I can correct or improve task information.

**Why this priority**: Updating tasks is important for maintaining accurate information but isn't required for the minimal viable product. Users can still track tasks without this feature, though it improves usability.

**Independent Test**: Can be fully tested by creating a task, selecting "Update Task", choosing the task from arrow-key menu, selecting what to update (Title/Description/Priority/All), and verifying the before/after comparison shows the change correctly.

**Acceptance Scenarios**:

1. **Given** I have tasks in the system, **When** I select "Update Task" and choose a task via arrow keys, **Then** I see options: Title, Description, Priority, All fields
2. **Given** I'm updating a task's title, **When** the prompt displays, **Then** the current title is shown as placeholder/default
3. **Given** I update a task's title from "Buy groceries" to "Get groceries from Costco", **When** the update completes, **Then** a success panel shows "Before: Buy groceries" and "After: Get groceries from Costco"
4. **Given** I update a task, **When** the update is saved, **Then** the created_at timestamp remains unchanged and updated_at is set to current time
5. **Given** I have no tasks, **When** I select "Update Task", **Then** a warning panel displays "No tasks available to update" with tip "Create a task first using 'add'"
6. **Given** I'm updating all fields, **When** I complete the flow, **Then** I'm prompted for title, description, and priority in sequence

---

### User Story 4 - Delete Task (Priority: P2)

As a user, I want to remove a task from my list so that I can clean up completed or cancelled items.

**Why this priority**: Deletion helps maintain a clean task list but isn't essential for the core todo functionality. Users can still manage tasks without deletion, though the list may become cluttered over time.

**Independent Test**: Can be fully tested by creating a task, selecting "Delete Task", choosing the task via arrow keys, viewing the task details confirmation panel, selecting "Yes, delete it", and verifying the deletion success message displays with the task removed from the list.

**Acceptance Scenarios**:

1. **Given** I have tasks in the system, **When** I select "Delete Task", **Then** an arrow-key selection menu shows all tasks with format: ID │ Title │ Priority │ Status
2. **Given** I've selected a task to delete, **When** the confirmation displays, **Then** I see full task details: ID, Title, Description, Priority, Status, Created timestamp
3. **Given** the confirmation is displayed, **When** I select "Yes, delete it", **Then** the task is removed and success message shows "'{Title}' has been removed"
4. **Given** the confirmation is displayed, **When** I select "No, keep it", **Then** an info message displays "Deletion cancelled. Task was not removed" and task remains
5. **Given** I have no tasks, **When** I select "Delete Task", **Then** a warning panel displays "No tasks available" with guidance to add tasks first
6. **Given** I delete a task, **When** the deletion completes, **Then** the task no longer appears in the task list

---

### User Story 5 - Mark Complete/Incomplete (Priority: P2)

As a user, I want to toggle a task's completion status so that I can track my progress.

**Why this priority**: Tracking completion is valuable for productivity but not essential for the minimal viable product. Users can track tasks even without status toggling, though it's less useful for managing ongoing work.

**Independent Test**: Can be fully tested by creating 2 incomplete tasks, selecting "Mark Complete", choosing one task, verifying the status change confirmation, then selecting "Mark Incomplete" to test the reverse operation.

**Acceptance Scenarios**:

1. **Given** I have incomplete tasks, **When** I select "Mark Complete", **Then** only incomplete tasks are shown in the selection menu with ○ prefix
2. **Given** I mark a task complete, **When** the status changes, **Then** is_completed becomes True, completed_at is set to current timestamp, and success shows "○ Pending → ✓ Complete"
3. **Given** I have completed tasks, **When** I select "Mark Incomplete", **Then** only completed tasks are shown in the selection menu with ✓ prefix
4. **Given** I mark a task incomplete, **When** the status changes, **Then** is_completed becomes False, completed_at is cleared (None), and success shows "✓ Complete → ○ Pending"
5. **Given** all tasks are complete, **When** I select "Mark Complete", **Then** an info panel displays "All tasks are already complete!" with tip to add new tasks or mark some incomplete
6. **Given** all tasks are incomplete, **When** I select "Mark Incomplete", **Then** an info panel displays "No completed tasks to mark incomplete"

---

### Edge Cases

- What happens when a user presses Ctrl+C during an interactive prompt? System displays "ℹ Operation cancelled. Returning to main menu..." and returns to main menu without making changes
- What happens when a user enters a 201-character title? System displays validation error: "✗ Error: Title too long - Maximum 200 characters allowed. You entered 201" and re-prompts
- What happens when a user tries to update a task but provides no changes? System accepts the "no change" state and updates the updated_at timestamp
- How does the system handle empty task list for operations requiring task selection? Display helpful error panel with guidance: "No tasks available to [action]. Create a task first using 'add'"
- What happens when a user selects "Exit" from main menu? System displays confirmation prompt "Are you sure you want to exit?" with arrow-key Yes/No options
- What happens when user confirms exit? Goodbye panel displays with message: "Your tasks were stored in memory and will be lost. See you next time!"
- How does the system handle rapid navigation with arrow keys? questionary library handles debouncing and smooth navigation without lag
- What happens when terminal window is too small for rich table? Table adjusts to terminal width or wraps content appropriately using rich library's responsive behavior

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an interactive main menu with options: Add Task, List Tasks, Update Task, Delete Task, Mark Complete, Mark Incomplete, Help, Exit
- **FR-002**: System MUST support both arrow-key menu navigation AND direct command typing where users can type shortcuts (add, list, update, delete, done, undone, help, exit) while the menu is displayed to jump directly to that action. Shortcuts use partial prefix matching (e.g., "a" → "add", "l" → "list") with error messages on ambiguous matches
- **FR-003**: System MUST store all tasks in memory using Python data structures (no external databases, no file persistence)
- **FR-004**: System MUST auto-generate UUID for each task ID and display first 8 characters in UI
- **FR-005**: System MUST validate task title as required (1-200 characters), trim leading/trailing whitespace, allow all printable characters including emojis/unicode, normalize internal whitespace (collapse multiple spaces/newlines to single space), and strip control characters
- **FR-006**: System MUST validate task description as optional (max 1000 characters), trim leading/trailing whitespace, allow all printable characters including emojis/unicode, normalize internal whitespace (collapse multiple spaces/newlines to single space), and strip control characters
- **FR-007**: System MUST prompt for optional due date before priority selection. Users can skip by pressing Enter. If provided, validate format as YYYY-MM-DD and ensure date is not in the past. Display due dates in task lists with visual indicators for overdue tasks
- **FR-007a**: System MUST support three priority levels: High (🔴), Medium (🟡), Low (🟢) with arrow-key selection. Priority selection is required (no skip option) and defaults to MEDIUM
- **FR-008**: System MUST auto-set created_at timestamp when task is created using datetime.now()
- **FR-009**: System MUST update updated_at timestamp whenever task is modified
- **FR-010**: System MUST set completed_at timestamp when task is marked complete and clear it when marked incomplete
- **FR-011**: System MUST display tasks in rich formatted table with columns: ID (8 chars), Title (smart truncated with ellipsis based on terminal width), Priority, Status, Created (relative format for tasks < 7 days old: "2 hours ago", "3 days ago"; absolute YYYY-MM-DD format for older tasks)
- **FR-012**: System MUST sort task list by created_at descending (newest first)
- **FR-013**: System MUST display task summary statistics: total count, completed count, pending count
- **FR-014**: System MUST show empty state message when no tasks exist: "📭 No tasks yet!" with guidance
- **FR-015**: System MUST require explicit confirmation for destructive operations (delete, exit)
- **FR-016**: System MUST handle keyboard interrupt (Ctrl+C) gracefully with cancellation message and return to main menu
- **FR-016a**: System MUST implement graceful error handling for unexpected exceptions: catch errors, display user-friendly error panel with actionable message, log technical details to console for debugging, and return to main menu without crashing
- **FR-017**: System MUST display task details panel before delete confirmation
- **FR-018**: System MUST show before/after comparison when task is updated
- **FR-019**: System MUST filter tasks by completion status for Mark Complete (show only incomplete) and Mark Incomplete (show only complete)
- **FR-020**: System MUST provide helpful error messages with actionable tips for all error conditions
- **FR-021**: System MUST display welcome banner on startup with app title and version (semantic versioning: 0.1.0 for Phase 1)
- **FR-022**: System MUST display help screen with command reference and navigation tips
- **FR-023**: System MUST use colored output for visual hierarchy: green for success, red for errors, yellow for warnings, blue for info. Messages MUST be displayed using rich Panel components with icons, colored borders, and formatted text (e.g., ✓ Success in green panel with border)
- **FR-024**: System MUST format priority with emoji indicators in all views
- **FR-025**: System MUST format status with icon indicators: ✓ for complete, ○ for pending

### Key Entities

- **Task**: Represents a todo item with attributes:
  - id (UUID): Unique identifier, auto-generated
  - title (string): Task name, required, 1-200 characters
  - description (string): Optional details, max 1000 characters
  - due_date (date or None): Optional due date in YYYY-MM-DD format, must not be in the past
  - priority (enum): HIGH, MEDIUM, or LOW
  - is_completed (boolean): Completion status, default False
  - created_at (datetime): Task creation timestamp, auto-set
  - updated_at (datetime): Last modification timestamp, auto-updated
  - completed_at (datetime or None): Completion timestamp, set when marked complete

- **Priority**: Enumeration defining task importance levels:
  - HIGH: Urgent or critical tasks
  - MEDIUM: Normal priority tasks (default when creating new tasks)
  - LOW: Nice-to-have or low-urgency tasks

- **InMemoryStorage**: Manages task collection with operations:
  - Stores tasks in dict structure {task_id: Task}
  - Provides methods: add, get, get_all, update, delete, get_pending, get_completed, count
  - No persistence - data lost when application exits

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a new task in under 30 seconds including all prompts (title, description, priority selection)
- **SC-002**: Users can view their complete task list instantly (under 1 second for up to 100 tasks)
- **SC-003**: Users successfully complete primary flows (add task, view list, mark complete) on first attempt without errors or confusion
- **SC-004**: All interactive prompts respond to arrow-key navigation without lag or missed keystrokes
- **SC-005**: Error messages provide clear actionable guidance that allows users to correct mistakes without external help
- **SC-006**: Task list displays correctly formatted with all visual elements (emojis, colors, tables) in standard terminal environments
- **SC-007**: Application handles 100+ tasks without performance degradation (list displays in under 1 second)
- **SC-008**: Users can cancel any operation at any time using Ctrl+C without crashing the application
- **SC-009**: All task data persists in memory throughout application session until user exits
- **SC-010**: Application provides consistent visual feedback for all user actions (success, error, info, warning states)
