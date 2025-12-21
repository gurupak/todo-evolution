---
description: "Task breakdown for Phase II - Full-Stack Web Application"
---

# Tasks: Phase II - Full-Stack Web Application

**Input**: Design documents from `/specs/002-phase2-webapp/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This is a web application with separate backend and frontend:
- Backend: `phase-2/backend/src/todo_api/`
- Frontend: `phase-2/frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both backend and frontend

- [X] T001 Create phase-2 directory structure per plan.md
- [X] T002 Initialize backend Python project with UV in phase-2/backend/
- [X] T003 [P] Initialize frontend Next.js project with TypeScript in phase-2/frontend/
- [X] T004 [P] Configure backend pyproject.toml with FastAPI, SQLModel, Alembic, pytest dependencies
- [X] T005 [P] Configure frontend package.json with Next.js 16, shadcn/ui, TanStack Query, Better Auth
- [X] T006 [P] Create backend .env.example with DATABASE_URL, BETTER_AUTH_SECRET, FRONTEND_URL
- [X] T007 [P] Create frontend .env.local.example with BETTER_AUTH_SECRET, DATABASE_URL, NEXT_PUBLIC_API_URL
- [X] T008 [P] Setup backend linting with ruff in phase-2/backend/
- [X] T009 [P] Setup frontend linting with ESLint and formatting with Prettier in phase-2/frontend/
- [X] T010 Create phase-2/README.md with setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [X] T011 Setup Neon PostgreSQL database and obtain connection string
- [X] T012 Create backend config.py with Pydantic Settings for environment variables in phase-2/backend/src/todo_api/config.py
- [X] T013 Create async database engine and session factory in phase-2/backend/src/todo_api/database.py
- [X] T014 Initialize Alembic for migrations in phase-2/backend/
- [X] T015 Create PriorityEnum in phase-2/backend/src/todo_api/models/__init__.py
- [X] T016 Create SQLModel Task model in phase-2/backend/src/todo_api/models/task.py
- [X] T017 Create Alembic migration for Task table with indexes and triggers in phase-2/backend/alembic/versions/001_create_task_table.py
- [X] T018 Run Alembic migration to create Task table in Neon database
- [X] T019 Create Pydantic schemas in phase-2/backend/src/todo_api/schemas/task.py (TaskCreateRequest, TaskUpdateRequest, TaskResponse, TaskListResponse)
- [X] T020 [P] Create common error schemas in phase-2/backend/src/todo_api/schemas/common.py (ErrorResponse)
- [X] T021 Create JWT verification middleware in phase-2/backend/src/todo_api/middleware/auth.py
- [X] T022 Create TaskService with CRUD operations in phase-2/backend/src/todo_api/services/task_service.py
- [X] T023 Create FastAPI app with CORS configuration in phase-2/backend/src/todo_api/main.py
- [X] T024 Create task router with dependency injection in phase-2/backend/src/todo_api/routers/tasks.py
- [X] T025 Register task router in main.py FastAPI app
- [X] T026 Create pytest conftest.py with async database fixtures in phase-2/backend/tests/conftest.py

### Frontend Foundation

- [X] T027 [P] Initialize shadcn/ui with components.json in phase-2/frontend/
- [X] T028 [P] Configure Tailwind CSS in phase-2/frontend/tailwind.config.ts
- [X] T029 [P] Setup Better Auth configuration in phase-2/frontend/src/lib/auth.ts
- [X] T030 [P] Create TypeScript types (Task, User, Session, Priority enum) in phase-2/frontend/src/types/task.ts and user.ts
- [X] T031 [P] Create API client with JWT injection in phase-2/frontend/src/lib/api-client.ts
- [X] T032 [P] Create utility functions (cn, etc.) in phase-2/frontend/src/lib/utils.ts
- [X] T033 [P] Create constants file in phase-2/frontend/src/lib/constants.ts
- [X] T034 [P] Setup TanStack Query provider in phase-2/frontend/src/app/layout.tsx
- [X] T035 [P] Create Next.js middleware for route protection in phase-2/frontend/src/middleware.ts
- [X] T036 [P] Install base shadcn/ui components (button, input, label, card, dialog, dropdown-menu, checkbox, badge, form, select, textarea, alert-dialog, skeleton, sheet)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: New users can register, login, and logout. Authenticated sessions are maintained via JWT tokens. This is the foundational authentication system.

**Independent Test**: Create account → Sign in → Verify session → Sign out → Verify redirect to login

### Implementation for User Story 1

- [X] T037 [P] [US1] Setup Better Auth database schema (user, session, account tables) by running Better Auth migration
- [X] T038 [P] [US1] Create auth layout component in phase-2/frontend/src/components/auth/auth-layout.tsx
- [X] T039 [P] [US1] Create signup page with form validation in phase-2/frontend/src/app/auth/signup/page.tsx
- [X] T040 [P] [US1] Create signin page with form validation in phase-2/frontend/src/app/auth/signin/page.tsx
- [X] T041 [P] [US1] Create useAuth hook for Better Auth session management in phase-2/frontend/src/hooks/use-auth.ts
- [X] T042 [P] [US1] Create header component with branding in phase-2/frontend/src/components/layout/header.tsx
- [X] T043 [US1] Create user menu dropdown with logout in phase-2/frontend/src/components/layout/user-menu.tsx
- [X] T044 [US1] Create landing page with sign in/sign up links in phase-2/frontend/src/app/page.tsx
- [X] T045 [US1] Configure middleware to protect /dashboard routes in phase-2/frontend/src/middleware.ts
- [X] T046 [US1] Test registration flow (valid email, password validation, duplicate email error)
- [X] T047 [US1] Test login flow (valid credentials, invalid credentials, redirect to dashboard)
- [X] T048 [US1] Test logout flow (session cleared, redirect to login)
- [X] T049 [US1] Test protected route redirect (unauthenticated user redirected to login with return URL)

**Checkpoint**: At this point, User Story 1 should be fully functional - users can register, login, and logout

---

## Phase 4: User Story 6 - Multi-User Data Isolation (Priority: P1)

**Goal**: Ensure authenticated users can only access their own tasks. This is a critical security requirement that must be enforced before task creation.

**Independent Test**: Create two user accounts → Add tasks to each → Verify each user only sees their own tasks → Attempt direct URL access to other user's task → Verify 403 Forbidden

### Backend Tests for User Story 6

- [X] T050 [P] [US6] Write JWT middleware test for valid token in phase-2/backend/tests/test_auth.py
- [X] T051 [P] [US6] Write JWT middleware test for expired token in phase-2/backend/tests/test_auth.py
- [X] T052 [P] [US6] Write JWT middleware test for invalid token in phase-2/backend/tests/test_auth.py
- [X] T053 [P] [US6] Write JWT middleware test for missing token in phase-2/backend/tests/test_auth.py

### Implementation for User Story 6

- [X] T054 [US6] Implement JWT token verification logic in auth middleware in phase-2/backend/src/todo_api/middleware/auth.py
- [X] T055 [US6] Extract user_id from JWT claims in auth middleware
- [X] T056 [US6] Add user_id filtering to all TaskService methods in phase-2/backend/src/todo_api/services/task_service.py
- [X] T057 [US6] Add authorization check in task router to verify user_id in URL matches authenticated user in phase-2/backend/src/todo_api/routers/tasks.py
- [X] T058 [US6] Return 403 Forbidden when user_id mismatch
- [X] T059 [US6] Return 401 Unauthorized when JWT is missing or invalid

### Backend Tests for User Story 6 (Verification)

- [X] T060 [US6] Test TaskService filters tasks by user_id in phase-2/backend/tests/test_task_service.py
- [X] T061 [US6] Test API returns 403 when accessing other user's task in phase-2/backend/tests/test_task_api.py
- [X] T062 [US6] Test API returns 401 when JWT is missing in phase-2/backend/tests/test_task_api.py

**Checkpoint**: Security layer complete - all API requests are authenticated and authorized

---

## Phase 5: User Story 2 - Create and View Tasks (Priority: P1) 🎯 MVP Extension

**Goal**: Authenticated users can create tasks with title, description, and priority, then view all their tasks in a sorted list. This is the core value proposition.

**Independent Test**: Login → Create task with high priority → Create task with low priority → Verify both appear in list sorted by creation date → Verify empty state when no tasks

### Backend Tests for User Story 2

- [X] T063 [P] [US2] Write TaskService.create test in phase-2/backend/tests/test_task_service.py
- [X] T064 [P] [US2] Write TaskService.get_all test with user_id filtering in phase-2/backend/tests/test_task_service.py
- [X] T065 [P] [US2] Write TaskService.get_by_id test in phase-2/backend/tests/test_task_service.py
- [X] T066 [P] [US2] Write API POST /tasks endpoint test in phase-2/backend/tests/test_task_api.py
- [X] T067 [P] [US2] Write API GET /tasks endpoint test in phase-2/backend/tests/test_task_api.py
- [X] T068 [P] [US2] Write API GET /tasks/{id} endpoint test in phase-2/backend/tests/test_task_api.py
- [X] T069 [P] [US2] Write validation error test (empty title) in phase-2/backend/tests/test_task_api.py

### Backend Implementation for User Story 2

- [X] T070 [US2] Implement TaskService.create method in phase-2/backend/src/todo_api/services/task_service.py
- [X] T071 [US2] Implement TaskService.get_all method with user_id filter and sorting in phase-2/backend/src/todo_api/services/task_service.py
- [X] T072 [US2] Implement TaskService.get_by_id method with user_id verification in phase-2/backend/src/todo_api/services/task_service.py
- [X] T073 [US2] Implement POST /api/{user_id}/tasks endpoint in phase-2/backend/src/todo_api/routers/tasks.py
- [X] T074 [US2] Implement GET /api/{user_id}/tasks endpoint in phase-2/backend/src/todo_api/routers/tasks.py
- [X] T075 [US2] Implement GET /api/{user_id}/tasks/{task_id} endpoint in phase-2/backend/src/todo_api/routers/tasks.py
- [X] T076 [US2] Add validation error handling with field-level errors in task router

### Frontend Implementation for User Story 2

- [X] T077 [P] [US2] Create useTasks hook with TanStack Query for list query in phase-2/frontend/src/hooks/use-tasks.ts
- [X] T078 [P] [US2] Create useCreateTask mutation hook in phase-2/frontend/src/hooks/use-tasks.ts
- [X] T079 [P] [US2] Create priority badge component in phase-2/frontend/src/components/tasks/priority-badge.tsx
- [X] T080 [P] [US2] Create task stats component in phase-2/frontend/src/components/tasks/task-stats.tsx
- [X] T081 [P] [US2] Create task empty state component in phase-2/frontend/src/components/tasks/task-empty.tsx
- [X] T082 [P] [US2] Create task item component with checkbox in phase-2/frontend/src/components/tasks/task-item.tsx
- [X] T083 [US2] Create task list component with loading and error states in phase-2/frontend/src/components/tasks/task-list.tsx
- [X] T084 [US2] Create task form component with React Hook Form and Zod validation in phase-2/frontend/src/components/tasks/task-form.tsx
- [X] T085 [US2] Create dashboard page with task list and stats in phase-2/frontend/src/app/dashboard/page.tsx
- [X] T086 [US2] Add "Add Task" dialog with task form to dashboard
- [X] T087 [US2] Implement toast notifications with Sonner for success/error messages
- [X] T088 [US2] Test create task flow (valid input, validation errors, success message)
- [X] T089 [US2] Test view tasks flow (list display, empty state, sorting by creation date)

**Checkpoint**: Core task management functional - users can create and view tasks

---

## Phase 6: User Story 3 - Task Completion Tracking (Priority: P2)

**Goal**: Users can toggle task completion status with a checkbox. Completed tasks show strikethrough styling and timestamps. Dashboard stats update in real-time.

**Independent Test**: Login → Create task → Mark as complete → Verify strikethrough and timestamp → Mark as incomplete → Verify styling removed → Verify stats update

### Backend Tests for User Story 3

- [X] T090 [P] [US3] Write TaskService.toggle_complete test in phase-2/backend/tests/test_task_service.py
- [X] T091 [P] [US3] Write API PATCH /tasks/{id}/complete endpoint test in phase-2/backend/tests/test_task_api.py
- [X] T092 [P] [US3] Write test for completed_at timestamp setting in phase-2/backend/tests/test_task_service.py
- [X] T093 [P] [US3] Write test for completed_at clearing when toggled back in phase-2/backend/tests/test_task_service.py

### Backend Implementation for User Story 3

- [X] T094 [US3] Implement TaskService.toggle_complete method in phase-2/backend/src/todo_api/services/task_service.py
- [X] T095 [US3] Implement PATCH /api/{user_id}/tasks/{task_id}/complete endpoint in phase-2/backend/src/todo_api/routers/tasks.py
- [X] T096 [US3] Add database trigger logic validation for completed_at timestamp

### Frontend Implementation for User Story 3

- [X] T097 [P] [US3] Create useToggleComplete mutation hook with optimistic update in phase-2/frontend/src/hooks/use-tasks.ts
- [X] T098 [US3] Add completion checkbox to task item component with strikethrough styling in phase-2/frontend/src/components/tasks/task-item.tsx
- [X] T099 [US3] Update task stats to calculate completed/pending counts in phase-2/frontend/src/components/tasks/task-stats.tsx
- [X] T100 [US3] Add completion timestamp display to task detail view
- [X] T101 [US3] Test toggle completion flow (checkbox click, optimistic update, strikethrough styling)
- [X] T102 [US3] Test stats update (completed count increases, pending count decreases)

**Checkpoint**: Task completion tracking functional with real-time UI updates

---

## Phase 7: User Story 4 - Task Details and Editing (Priority: P2)

**Goal**: Users can view full task details including all metadata, and edit task fields (title, description, priority). Changes reflect immediately without page refresh.

**Independent Test**: Login → Create task → Click task to view details → Click edit → Update fields → Save → Verify changes in list → Cancel edit → Verify no changes

### Backend Tests for User Story 4

- [ ] T103 [P] [US4] Write TaskService.update test in phase-2/backend/tests/test_task_service.py
- [ ] T104 [P] [US4] Write API PUT /tasks/{id} endpoint test in phase-2/backend/tests/test_task_api.py
- [ ] T105 [P] [US4] Write partial update test (only title changed) in phase-2/backend/tests/test_task_service.py
- [ ] T106 [P] [US4] Write updated_at timestamp test in phase-2/backend/tests/test_task_service.py

### Backend Implementation for User Story 4

- [ ] T107 [US4] Implement TaskService.update method in phase-2/backend/src/todo_api/services/task_service.py
- [ ] T108 [US4] Implement PUT /api/{user_id}/tasks/{task_id} endpoint in phase-2/backend/src/todo_api/routers/tasks.py
- [ ] T109 [US4] Add validation for partial updates (null fields ignored)

### Frontend Implementation for User Story 4

- [ ] T110 [P] [US4] Create useUpdateTask mutation hook in phase-2/frontend/src/hooks/use-tasks.ts
- [ ] T111 [P] [US4] Create task detail component with all metadata in phase-2/frontend/src/components/tasks/task-detail.tsx
- [ ] T112 [US4] Add click handler to task item to open detail view
- [ ] T113 [US4] Add edit mode to task form component (pre-populate fields)
- [ ] T114 [US4] Add edit button to task detail component that opens form in edit mode
- [ ] T115 [US4] Implement save changes with optimistic update
- [ ] T116 [US4] Implement cancel edit to discard changes
- [ ] T117 [US4] Test edit task flow (open detail, click edit, update fields, save, verify list update)
- [ ] T118 [US4] Test cancel edit (changes discarded, modal closes)

**Checkpoint**: Task editing functional with immediate UI feedback

---

## Phase 8: User Story 5 - Task Deletion (Priority: P3)

**Goal**: Users can delete tasks after confirmation. Deleted tasks are removed from the list and stats are updated immediately.

**Independent Test**: Login → Create task → Click delete → See confirmation with task title → Confirm → Verify task removed → Verify stats updated

### Backend Tests for User Story 5

- [ ] T119 [P] [US5] Write TaskService.delete test in phase-2/backend/tests/test_task_service.py
- [ ] T120 [P] [US5] Write API DELETE /tasks/{id} endpoint test in phase-2/backend/tests/test_task_api.py
- [ ] T121 [P] [US5] Write test for 404 when deleting non-existent task in phase-2/backend/tests/test_task_api.py

### Backend Implementation for User Story 5

- [ ] T122 [US5] Implement TaskService.delete method in phase-2/backend/src/todo_api/services/task_service.py
- [ ] T123 [US5] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in phase-2/backend/src/todo_api/routers/tasks.py
- [ ] T124 [US5] Return 404 when task not found for deletion

### Frontend Implementation for User Story 5

- [ ] T125 [P] [US5] Create useDeleteTask mutation hook with cache invalidation in phase-2/frontend/src/hooks/use-tasks.ts
- [ ] T126 [US5] Add delete button to task detail component
- [ ] T127 [US5] Create delete confirmation alert dialog with task title
- [ ] T128 [US5] Implement delete on confirm with optimistic update
- [ ] T129 [US5] Update stats after deletion
- [ ] T130 [US5] Test delete task flow (click delete, see confirmation, confirm, verify removal)
- [ ] T131 [US5] Test cancel deletion (dialog closes, task remains)

**Checkpoint**: All core CRUD operations complete for tasks

---

## Phase 9: User Story 7 - Responsive Design (Priority: P2)

**Goal**: Application works on mobile (320px+), tablet (640-1024px), and desktop (1024px+) with appropriate layouts and touch-friendly targets.

**Independent Test**: Open app on mobile device → Verify single-column layout → Verify 44px+ tap targets → Test on tablet → Verify two-column layout → Test on desktop → Verify full layout

### Implementation for User Story 7

- [ ] T132 [P] [US7] Add responsive breakpoints to Tailwind config in phase-2/frontend/tailwind.config.ts
- [ ] T133 [P] [US7] Implement mobile-first styles for task list in phase-2/frontend/src/components/tasks/task-list.tsx
- [ ] T134 [P] [US7] Implement mobile-first styles for task item with 44px+ tap targets in phase-2/frontend/src/components/tasks/task-item.tsx
- [ ] T135 [P] [US7] Implement responsive header in phase-2/frontend/src/components/layout/header.tsx
- [ ] T136 [P] [US7] Replace dialog with bottom sheet for mobile modals in phase-2/frontend/src/components/tasks/task-detail.tsx
- [ ] T137 [P] [US7] Add responsive dashboard layout in phase-2/frontend/src/app/dashboard/page.tsx
- [ ] T138 [US7] Test mobile layout (320px width, single column, touch targets)
- [ ] T139 [US7] Test tablet layout (640-1024px, two columns)
- [ ] T140 [US7] Test desktop layout (1024px+, full layout)

**Checkpoint**: Application is fully responsive across all device sizes

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, error handling, and documentation

### Error Handling & Resilience

- [ ] T141 [P] Add automatic retry logic for database operations in phase-2/backend/src/todo_api/services/task_service.py
- [ ] T142 [P] Add network error handling with toast notifications in phase-2/frontend/src/lib/api-client.ts
- [ ] T143 [P] Add session expiration handling with redirect to login in phase-2/frontend/src/middleware.ts
- [ ] T144 [P] Add 404 error page in phase-2/frontend/src/app/not-found.tsx
- [ ] T145 [P] Add error boundary for React components in phase-2/frontend/src/app/error.tsx

### Performance Optimization

- [ ] T146 [P] Verify database indexes are created for task queries
- [ ] T147 [P] Add loading skeletons for task list in phase-2/frontend/src/components/tasks/task-list.tsx
- [ ] T148 [P] Implement TanStack Query caching strategy with staleTime

### Documentation

- [ ] T149 [P] Create backend README.md with setup instructions in phase-2/backend/README.md
- [ ] T150 [P] Create frontend README.md with setup instructions in phase-2/frontend/README.md
- [ ] T151 [P] Update phase-2/README.md with quickstart guide
- [ ] T152 [P] Add inline code comments for complex business logic
- [ ] T153 [P] Document environment variables in .env.example files

### Security Hardening

- [ ] T154 Verify CORS is configured correctly for production domains in phase-2/backend/src/todo_api/main.py
- [ ] T155 Verify JWT secret is strong and documented
- [ ] T156 Add rate limiting to API endpoints (optional for Phase II)
- [ ] T157 Verify all user inputs are validated on backend

### Final Validation

- [ ] T158 Run backend tests and verify 80%+ coverage
- [ ] T159 Run frontend build and verify no TypeScript errors
- [ ] T160 Run linting on backend (ruff) and frontend (ESLint)
- [ ] T161 Test complete user workflow from quickstart.md
- [ ] T162 Verify Phase I CLI application still works (additive phase compliance)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - BLOCKS all user stories
- **Phase 3 (US1 - Auth)**: Depends on Phase 2 completion
- **Phase 4 (US6 - Security)**: Depends on Phase 3 completion (needs auth to test authorization)
- **Phase 5 (US2 - Create/View)**: Depends on Phase 4 completion (needs security layer)
- **Phase 6 (US3 - Completion)**: Depends on Phase 5 completion (needs tasks to exist)
- **Phase 7 (US4 - Edit)**: Depends on Phase 5 completion (needs tasks to exist)
- **Phase 8 (US5 - Delete)**: Depends on Phase 5 completion (needs tasks to exist)
- **Phase 9 (US7 - Responsive)**: Can start after Phase 5 or run in parallel with Phases 6-8
- **Phase 10 (Polish)**: Depends on all desired user stories being complete

### User Story Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ← CRITICAL BLOCKER
    ↓
Phase 3 (US1: Auth) ← Must complete first
    ↓
Phase 4 (US6: Security) ← Must complete second
    ↓
Phase 5 (US2: Create/View) ← MVP Core
    ↓
    ├─→ Phase 6 (US3: Completion)
    ├─→ Phase 7 (US4: Edit)
    └─→ Phase 8 (US5: Delete)
    
Phase 9 (US7: Responsive) ← Can run parallel with 6-8
    ↓
Phase 10 (Polish) ← Final
```

### Parallel Opportunities

**Within Phase 1 (Setup)**:
- T003, T005, T006, T007, T008, T009 can all run in parallel

**Within Phase 2 (Foundational)**:
- Backend foundation tasks (T011-T026) run sequentially due to dependencies
- Frontend foundation tasks (T027-T036) can run in parallel
- Backend and Frontend foundations can run in parallel with each other

**Within User Stories**:
- Test tasks within a story can run in parallel (marked with [P])
- Model/component tasks within a story can run in parallel (marked with [P])
- Different user stories (Phases 6, 7, 8) can run in parallel after Phase 5 completes

**Phase 9 (Responsive)**: All T132-T137 tasks can run in parallel

**Phase 10 (Polish)**: Most tasks can run in parallel (marked with [P])

---

## Parallel Example: Phase 2 Foundational

```bash
# Backend foundation (sequential due to dependencies):
Task T011 → T012 → T013 → ... → T026

# Frontend foundation (all parallel):
Task T027, T028, T029, T030, T031, T032, T033, T034, T035, T036

# Backend and Frontend can run in parallel with each other
```

---

## Parallel Example: User Story 2

```bash
# Backend tests (all parallel):
Task T063, T064, T065, T066, T067, T068, T069

# Frontend components (all parallel):
Task T077, T078, T079, T080, T081, T082
```

---

## Implementation Strategy

### MVP First (Minimal Viable Product)

**MVP Scope**: User Story 1 (Auth) + User Story 6 (Security) + User Story 2 (Create/View Tasks)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 6 (Multi-User Security)
5. Complete Phase 5: User Story 2 (Create/View Tasks)
6. **STOP and VALIDATE**: Test end-to-end flow (register → login → create task → view tasks)
7. Deploy/demo if ready

**MVP Value**: Users can register, login, create tasks, and view their task list - core value delivered!

### Incremental Delivery

After MVP:

1. **Iteration 2**: Add Phase 6 (Task Completion) → Users can mark tasks complete
2. **Iteration 3**: Add Phase 7 (Task Editing) → Users can update task details
3. **Iteration 4**: Add Phase 8 (Task Deletion) → Users can remove tasks
4. **Iteration 5**: Add Phase 9 (Responsive Design) → Mobile users can access the app
5. **Final Polish**: Complete Phase 10 (Error handling, docs, optimization)

Each iteration adds value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers:

1. **Together**: Complete Phase 1 (Setup) and Phase 2 (Foundational)
2. **Together**: Complete Phase 3 (Auth) and Phase 4 (Security) - sequential, security-critical
3. **Developer A**: Phase 5 (Create/View Tasks)
4. **Developer B**: Phase 9 (Responsive Design) - can start after Phase 5 structure is in place
5. **Once Phase 5 complete, parallel work**:
   - Developer A: Phase 6 (Completion Tracking)
   - Developer B: Phase 7 (Task Editing)
   - Developer C: Phase 8 (Task Deletion)
6. **Together**: Phase 10 (Polish & Testing)

---

## Task Summary

- **Total Tasks**: 162
- **Setup Tasks**: 10 (Phase 1)
- **Foundational Tasks**: 26 (Phase 2)
- **User Story 1 (Auth)**: 13 tasks (Phase 3)
- **User Story 6 (Security)**: 13 tasks (Phase 4)
- **User Story 2 (Create/View)**: 27 tasks (Phase 5)
- **User Story 3 (Completion)**: 13 tasks (Phase 6)
- **User Story 4 (Editing)**: 16 tasks (Phase 7)
- **User Story 5 (Deletion)**: 13 tasks (Phase 8)
- **User Story 7 (Responsive)**: 9 tasks (Phase 9)
- **Polish & Cross-Cutting**: 22 tasks (Phase 10)

**Parallel Opportunities**: 47 tasks marked [P] can run in parallel within their phases

**MVP Scope**: 76 tasks (Phases 1-5) deliver core value

**Suggested First Milestone**: Complete through Phase 5 (US2) for working MVP

---

## Notes

- All tasks follow the required format: `- [ ] [ID] [P?] [Story?] Description with file path`
- [P] tasks target different files and have no dependencies on incomplete tasks
- [Story] labels map tasks to user stories for traceability
- Each user story phase is independently testable
- Tests are written first and must fail before implementation
- Backend tests achieve 80%+ coverage target
- Frontend components use shadcn/ui exclusively
- All security requirements (US6) enforced before task creation (US2)
- Responsive design (US7) can be added incrementally or in parallel
- Phase I CLI application must remain functional (additive phase compliance)
