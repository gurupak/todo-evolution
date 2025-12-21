# Implementation Plan: Phase II - Full-Stack Web Application

**Branch**: `002-phase2-webapp` | **Date**: 2025-12-19 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/002-phase2-webapp/spec.md`

## Summary

Transform the Phase I in-memory Python CLI todo application into a production-ready, multi-user web application with authentication, persistent storage, and responsive design. The system will use Next.js (frontend) + FastAPI (backend) + Neon PostgreSQL (database) with Better Auth handling authentication via JWT tokens. This phase demonstrates full-stack development capabilities while maintaining backward compatibility with Phase I.

## Technical Context

**Frontend Stack**:
- **Language/Version**: TypeScript 5.x with strict mode, Next.js 16+ (App Router)
- **Primary Dependencies**: shadcn/ui, Tailwind CSS, TanStack Query 5.x, React Hook Form, Zod, Better Auth 1.x with JWT plugin, Sonner (toasts)
- **Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
- **Performance Goals**: Task list renders <2s, UI updates <500ms, 95% operation success rate
- **Constraints**: Responsive design (320px minimum width), touch-friendly (44px tap targets), no offline mode

**Backend Stack**:
- **Language/Version**: Python 3.13+ (managed by UV package manager)
- **Primary Dependencies**: FastAPI 0.115+, SQLModel 0.0.22+, Alembic 1.14+, python-jose (JWT verification), asyncpg (PostgreSQL driver), pydantic-settings
- **Storage**: Neon Serverless PostgreSQL with async connections
- **Testing**: pytest 8.0+, pytest-asyncio for async tests
- **Target Platform**: ASGI server (Uvicorn) on Linux/macOS/Windows
- **Performance Goals**: API responses <1s, concurrent users 10,000, 99% uptime
- **Constraints**: Stateless backend (JWT-based auth), async-only database operations

**Shared**:
- **Authentication**: Better Auth (frontend) + JWT verification (backend) with shared secret
- **Database Schema**: Better Auth manages user/session/account tables; FastAPI manages task table
- **Project Type**: Web application (separate frontend + backend)
- **Scale/Scope**: Multi-user system, ~5 API endpoints, ~10 UI components, 7 pages/routes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Initial Check (Before Phase 0 Research)

✅ **Phase II Technology Requirements (from Constitution)**:
- Next.js 16+ with App Router exclusively ✓
- TypeScript strict mode ✓
- shadcn/ui ✓
- Tailwind CSS ✓
- FastAPI with async endpoints ✓
- SQLModel ORM ✓
- Pydantic validation ✓
- Dependency injection ✓
- Neon PostgreSQL (serverless) ✓
- Proper migrations (Alembic) ✓

✅ **Spec-Driven Development Compliance**:
- Specification created via `/sp.specify` ✓
- Clarifications completed via `/sp.clarify` ✓
- Plan being created via `/sp.plan` ✓
- Next step: `/sp.tasks` for task breakdown ✓
- Implementation via `/sp.implement` (no manual coding) ✓

✅ **Test-First Development**:
- Test specifications will be written before implementation specs ✓
- Minimum 80% coverage for business logic ✓
- Integration tests prioritized ✓
- All user-facing features must have tests ✓

✅ **Code Quality Standards**:
- Type hints on all functions/methods ✓
- Docstrings for public APIs ✓
- Pydantic models for data validation ✓
- PEP 8 naming conventions ✓
- Maximum function length: 20 lines ✓
- No global mutable state ✓
- TypeScript strict mode ✓
- No `any` type without justification ✓
- Server Components by default ✓
- shadcn/ui components exclusively ✓
- Tailwind CSS only ✓

✅ **Additive Phase Compliance**:
- Phase I CLI application remains functional ✓
- No modifications to `phase-1/` directory ✓
- Phase II exists in separate `phase-2/` directory ✓
- Independent package management (phase-1: UV, phase-2: UV + npm) ✓

**INITIAL GATE RESULT**: ✅ **PASS** - All constitution requirements met, no violations to justify

---

### Post-Design Check (After Phase 1 Artifacts)

**Artifacts Reviewed**:
- ✅ research.md (Phase 0 output)
- ✅ data-model.md (Phase 1.1 output)
- ✅ contracts/README.md, models.md, storage.md, commands.md, display.md (Phase 1.2 output)
- ✅ quickstart.md (Phase 1.3 output)
- ✅ Agent context updated via update-agent-context.sh (Phase 1.4 output)

**Technology Stack Validation**:

✅ **Data Model Compliance (data-model.md)**:
- SQLModel used for Task entity ✓
- Pydantic validation enforced ✓
- Type hints on all fields ✓
- Database triggers for updated_at and completed_at ✓
- Foreign key constraints with CASCADE delete ✓
- Proper indexing strategy for performance ✓
- Alembic migration defined ✓
- No soft deletes needed (hard deletes acceptable for Phase II) ✓

✅ **API Contract Compliance (contracts/)**:
- RESTful endpoint design ✓
- Pydantic request/response schemas ✓
- Proper error handling with status codes ✓
- JWT authentication flow documented ✓
- Type-safe TypeScript types matching Python schemas ✓
- No manual code writing - contracts specify behavior only ✓

✅ **Architecture Compliance**:
- Separation of concerns: models → storage → commands → display ✓
- Dependency injection planned for FastAPI ✓
- Async database operations specified ✓
- TanStack Query for frontend state management ✓
- Better Auth for authentication (no manual auth code) ✓

✅ **Security Standards**:
- JWT verification middleware specified ✓
- User ID filtering enforced in service layer ✓
- bcrypt password hashing (managed by Better Auth) ✓
- No hardcoded secrets (environment variables) ✓
- CORS configuration planned ✓
- Input validation at multiple layers ✓

✅ **Performance Standards**:
- Database indexes for all filtered columns ✓
- Composite index for user_id + is_completed ✓
- Async queries specified ✓
- TanStack Query caching planned ✓
- Optimistic updates specified ✓

✅ **Testing Strategy**:
- Integration tests prioritized ✓
- JWT middleware: 100% coverage target ✓
- Business logic: 90%+ coverage target ✓
- Component tests: 70%+ coverage target ✓
- Test specifications included in contracts ✓

**Constitution Violations Found**: NONE

**FINAL GATE RESULT**: ✅ **PASS** - All design artifacts align with constitution principles. Ready to proceed to `/sp.tasks`.

## Project Structure

### Documentation (this feature)

```text
specs/002-phase2-webapp/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (already created)
├── checklists/
│   └── requirements.md  # Specification quality checklist
├── research.md          # Phase 0 output (technology research)
├── data-model.md        # Phase 1 output (entity schemas)
├── quickstart.md        # Phase 1 output (setup guide)
├── contracts/           # Phase 1 output (API contracts)
│   ├── README.md        # Contract overview
│   ├── models.md        # Data model contracts
│   ├── storage.md       # Database contracts
│   ├── commands.md      # Business logic contracts
│   └── display.md       # UI contracts
└── tasks.md             # Phase 2 output (/sp.tasks - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
phase-2/
├── backend/
│   ├── src/
│   │   └── todo_api/
│   │       ├── __init__.py
│   │       ├── main.py           # FastAPI app, CORS, routers
│   │       ├── config.py         # Pydantic settings (env vars)
│   │       ├── database.py       # Async engine, session factory
│   │       ├── models/
│   │       │   ├── __init__.py
│   │       │   └── task.py       # SQLModel Task table
│   │       ├── schemas/
│   │       │   ├── __init__.py
│   │       │   ├── task.py       # Pydantic request/response schemas
│   │       │   └── common.py     # Shared schemas (error responses)
│   │       ├── routers/
│   │       │   ├── __init__.py
│   │       │   └── tasks.py      # Task API endpoints
│   │       ├── services/
│   │       │   ├── __init__.py
│   │       │   └── task_service.py  # Business logic
│   │       └── middleware/
│   │           ├── __init__.py
│   │           └── auth.py       # JWT verification, user_id extraction
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/             # Migration files
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py           # Pytest fixtures
│   │   ├── test_auth.py          # JWT middleware tests
│   │   ├── test_task_service.py  # Business logic tests
│   │   └── test_task_api.py      # API endpoint tests
│   ├── pyproject.toml            # UV project config
│   ├── alembic.ini               # Alembic config
│   ├── .env.example              # Environment variable template
│   └── README.md                 # Backend setup instructions
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx        # Root layout
│   │   │   ├── page.tsx          # Landing page (/)
│   │   │   ├── auth/
│   │   │   │   ├── signin/
│   │   │   │   │   └── page.tsx  # Login page
│   │   │   │   └── signup/
│   │   │   │       └── page.tsx  # Registration page
│   │   │   └── dashboard/
│   │   │       └── page.tsx      # Task list (protected)
│   │   ├── components/
│   │   │   ├── ui/               # shadcn/ui components
│   │   │   ├── tasks/
│   │   │   │   ├── task-list.tsx
│   │   │   │   ├── task-item.tsx
│   │   │   │   ├── task-form.tsx
│   │   │   │   ├── task-detail.tsx
│   │   │   │   ├── task-empty.tsx
│   │   │   │   ├── task-stats.tsx
│   │   │   │   └── priority-badge.tsx
│   │   │   ├── layout/
│   │   │   │   ├── header.tsx
│   │   │   │   └── user-menu.tsx
│   │   │   └── auth/
│   │   │       ├── auth-layout.tsx
│   │   │       └── protected-route.tsx
│   │   ├── lib/
│   │   │   ├── auth.ts           # Better Auth config
│   │   │   ├── api-client.ts     # Axios/fetch with JWT injection
│   │   │   ├── utils.ts          # Helper functions (cn, etc.)
│   │   │   └── constants.ts      # App-wide constants
│   │   ├── hooks/
│   │   │   ├── use-tasks.ts      # TanStack Query hooks for tasks
│   │   │   ├── use-auth.ts       # Better Auth session hooks
│   │   │   └── use-toast.ts      # Toast notification hook
│   │   ├── types/
│   │   │   ├── task.ts           # Task type definitions
│   │   │   ├── user.ts           # User type definitions
│   │   │   └── api.ts            # API response types
│   │   └── middleware.ts         # Next.js middleware (route protection)
│   ├── public/                   # Static assets
│   ├── tests/
│   │   └── __tests__/
│   ├── package.json
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── components.json           # shadcn/ui config
│   ├── .env.local.example
│   └── README.md                 # Frontend setup instructions
│
└── README.md                     # Phase II overview
```

**Structure Decision**: Web application structure with separate frontend and backend directories. This aligns with the constitution's Phase II requirements and supports independent deployment of frontend (static hosting/Vercel) and backend (API server). Both use modern package managers (UV for Python, npm for Node.js) and follow best practices for their respective ecosystems.

## Complexity Tracking

No constitution violations - this section is not applicable.

---

## Phase 0: Research & Technology Validation

### Research Tasks

The user has provided a comprehensive technical plan. I will validate and document the key technology choices:

#### 1. Better Auth + FastAPI JWT Integration

**Research Question**: How does Better Auth's JWT plugin integrate with FastAPI for token verification?

**Key Points to Research**:
- JWT token structure (claims: sub, email, exp)
- Shared secret configuration (BETTER_AUTH_SECRET)
- Token verification in FastAPI using python-jose
- User ID extraction from token claims
- Error handling for expired/invalid tokens

#### 2. Neon PostgreSQL Async Integration

**Research Question**: Best practices for using Neon with SQLModel and async SQLAlchemy?

**Key Points to Research**:
- Connection string format for Neon
- Async engine configuration
- Session management with async context managers
- Migration strategy with Alembic
- Connection pooling for serverless environment

#### 3. TanStack Query Patterns for Task Management

**Research Question**: Optimal patterns for CRUD operations with TanStack Query?

**Key Points to Research**:
- Query key structure for task lists and individual tasks
- Mutation patterns for create/update/delete
- Optimistic updates for task completion
- Cache invalidation strategy
- Error handling and retry logic

#### 4. Next.js 16 App Router Authentication

**Research Question**: How to implement route protection with Better Auth in Next.js 16 App Router?

**Key Points to Research**:
- Middleware.ts configuration for protected routes
- Session validation in Server Components
- Redirect behavior for unauthenticated users
- Return URL preservation for post-login redirect

#### 5. Responsive Design with shadcn/ui

**Research Question**: Best practices for mobile-first responsive design using shadcn/ui components?

**Key Points to Research**:
- Mobile breakpoints (320px, 640px, 1024px)
- Touch-friendly component sizing
- Sheet vs Dialog for mobile modals
- Responsive table/list patterns

**Output**: `research.md` documenting all findings with code examples and architectural decisions

---

## Phase 1: Design & Contracts

### Phase 1.1: Data Model Design

**Objective**: Define all entities, relationships, and database schema

**Deliverable**: `data-model.md`

**Content Structure**:

1. **Entity Definitions**
   - User (managed by Better Auth)
   - Session (managed by Better Auth)
   - Task (managed by FastAPI)

2. **Database Schema**
   - Task table DDL
   - Indexes for performance
   - Foreign key constraints
   - Default values and triggers

3. **Validation Rules**
   - Field constraints from FR-001 to FR-047
   - Enum definitions (priority: high/medium/low)
   - Unique constraints (user email)

4. **State Transitions**
   - Task completion state machine
   - Timestamp management (created_at, updated_at, completed_at)

### Phase 1.2: API Contract Generation

**Objective**: Define all API endpoints with request/response schemas

**Deliverable**: `contracts/` directory

**Files to Generate**:

1. **contracts/README.md**: Overview of contract structure
2. **contracts/models.md**: Pydantic models and SQLModel definitions
3. **contracts/storage.md**: Database operations and queries
4. **contracts/commands.md**: Business logic service contracts
5. **contracts/display.md**: Frontend component contracts

**API Endpoints** (from spec):

| Method | Endpoint | Request | Response | Status Codes |
|--------|----------|---------|----------|--------------|
| GET | `/api/{user_id}/tasks` | Headers: Authorization | TaskListResponse | 200, 401, 403 |
| POST | `/api/{user_id}/tasks` | TaskCreateRequest | TaskResponse | 201, 400, 401, 403 |
| GET | `/api/{user_id}/tasks/{task_id}` | Headers: Authorization | TaskResponse | 200, 401, 403, 404 |
| PUT | `/api/{user_id}/tasks/{task_id}` | TaskUpdateRequest | TaskResponse | 200, 400, 401, 403, 404 |
| DELETE | `/api/{user_id}/tasks/{task_id}` | Headers: Authorization | DeleteResponse | 200, 401, 403, 404 |
| PATCH | `/api/{user_id}/tasks/{task_id}/complete` | Headers: Authorization | TaskResponse | 200, 401, 403, 404 |

### Phase 1.3: Quickstart Guide

**Objective**: Create step-by-step setup instructions

**Deliverable**: `quickstart.md`

**Content Structure**:

1. **Prerequisites**
   - Node.js 18+, Python 3.13+, UV, Neon account

2. **Backend Setup**
   ```bash
   cd phase-2/backend
   uv sync
   cp .env.example .env
   # Configure DATABASE_URL and BETTER_AUTH_SECRET
   uv run alembic upgrade head
   uv run uvicorn todo_api.main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd phase-2/frontend
   npm install
   npx shadcn@latest init
   cp .env.local.example .env.local
   # Configure NEXT_PUBLIC_API_URL and BETTER_AUTH_SECRET
   npm run dev
   ```

4. **First-Time User Flow**
   - Navigate to http://localhost:3000
   - Click "Sign Up"
   - Create account and add first task

### Phase 1.4: Agent Context Update

**Objective**: Update Claude Code's context with Phase II technologies

**Action**: Run `.specify/scripts/bash/update-agent-context.sh claude`

**Technologies to Add**:
- Next.js 16 App Router patterns
- Better Auth JWT configuration
- FastAPI async endpoint patterns
- SQLModel with Neon PostgreSQL
- TanStack Query mutation patterns

---

## Phase 2: Task Decomposition

**Note**: This phase is handled by `/sp.tasks` command - NOT part of `/sp.plan` output.

The `/sp.tasks` command will generate `tasks.md` with:
- Atomic, testable tasks derived from this plan
- Dependency ordering
- Acceptance criteria for each task
- Test specifications per task

---

## Implementation Sequence

### Stage 1: Backend Foundation (Tasks 1-8)

1. **Backend Project Setup**
   - Initialize UV project with pyproject.toml
   - Configure Pydantic settings for environment variables
   - Set up async database engine and session factory

2. **Database Models**
   - Define Task SQLModel with all fields from spec
   - Create Alembic migration for task table
   - Add indexes for user_id and performance

3. **JWT Middleware**
   - Implement JWT verification using python-jose
   - Extract user_id from token claims
   - Handle expired/invalid token errors

4. **Task Service Layer**
   - Implement business logic for CRUD operations
   - Enforce user_id filtering on all queries
   - Handle last-write-wins for concurrent edits
   - Implement automatic retry logic for database failures

5. **Pydantic Schemas**
   - Define request/response schemas
   - Add validation rules from spec
   - Create error response schemas

6. **Task Router**
   - Implement all 6 API endpoints
   - Add dependency injection for auth and database
   - Configure CORS for frontend origin

7. **FastAPI Main App**
   - Configure application with middleware
   - Register routers
   - Add error handlers

8. **Backend Tests**
   - JWT middleware tests
   - Task service tests (business logic)
   - API endpoint integration tests

### Stage 2: Frontend Foundation (Tasks 9-16)

9. **Frontend Project Setup**
   - Initialize Next.js 16 with TypeScript
   - Configure shadcn/ui and Tailwind
   - Set up Better Auth with JWT plugin

10. **Better Auth Configuration**
    - Configure database connection
    - Enable JWT plugin with 24-hour expiration
    - Set up email/password credentials provider

11. **API Client**
    - Create axios/fetch client with JWT injection
    - Implement automatic token refresh (if needed)
    - Handle 401/403 errors with redirect

12. **TypeScript Types**
    - Define Task, User, and API response types
    - Create validation schemas with Zod

13. **TanStack Query Hooks**
    - useTasks (list query)
    - useTask (single task query)
    - useCreateTask (mutation)
    - useUpdateTask (mutation)
    - useDeleteTask (mutation)
    - useToggleComplete (mutation)

14. **Base shadcn/ui Components**
    - Install: button, input, label, card, dialog, dropdown-menu, checkbox, badge, table, form, select, textarea, alert-dialog, avatar, skeleton, sheet

15. **Next.js Middleware**
    - Implement route protection for /dashboard
    - Redirect unauthenticated users to /auth/signin
    - Preserve return URL for post-login redirect

16. **Frontend Tests Setup**
    - Configure Jest/Vitest
    - Set up React Testing Library
    - Create test utilities and mocks

### Stage 3: Authentication UI (Tasks 17-20)

17. **Auth Layout Component**
    - Centered card layout for auth pages
    - Responsive design

18. **Sign Up Page**
    - Registration form with validation
    - Error handling and toast notifications
    - Redirect to dashboard on success

19. **Sign In Page**
    - Login form with validation
    - "Remember me" checkbox
    - Redirect to dashboard or return URL

20. **Header & User Menu**
    - Logo and navigation
    - User profile dropdown with logout

### Stage 4: Task Management UI (Tasks 21-30)

21. **Priority Badge Component**
    - Red (high), Yellow (medium), Green (low)
    - Icon + text display

22. **Task Stats Component**
    - Total, Completed, Pending counts
    - Real-time updates

23. **Task Empty State**
    - "No tasks yet" message
    - "Add Task" CTA button

24. **Task Item Component**
    - Checkbox for completion toggle
    - Title with strikethrough when complete
    - Priority badge
    - Action dropdown (edit, delete)

25. **Task List Component**
    - TanStack Query integration
    - Loading skeleton state
    - Error boundary

26. **Task Form Component**
    - Create/edit mode
    - React Hook Form + Zod validation
    - Title, description, priority fields
    - Cancel and submit buttons

27. **Task Detail Component**
    - Full task display in sheet/dialog
    - All metadata (timestamps, priority, status)
    - Edit and delete buttons

28. **Task Create Dialog**
    - "Add Task" button in header
    - Dialog with TaskForm component
    - Success toast on creation

29. **Task Edit Flow**
    - Click edit from detail view
    - Pre-populate form with current values
    - Success toast on update

30. **Task Delete Confirmation**
    - Alert dialog with task title
    - Confirm/cancel buttons
    - Success toast on deletion

### Stage 5: Dashboard & Polish (Tasks 31-35)

31. **Landing Page**
    - Welcome message
    - Sign in / Sign up links
    - Feature overview

32. **Dashboard Page**
    - Task stats at top
    - Task list with all components
    - Add task button
    - Protected route enforcement

33. **Responsive Design**
    - Mobile breakpoint styles
    - Touch-friendly tap targets (44px min)
    - Bottom sheet for mobile modals

34. **Error Handling**
    - Network error messages
    - Validation error display
    - Generic error fallback

35. **End-to-End Testing**
    - User registration flow
    - Create, edit, complete, delete task flow
    - Session expiration handling
    - Multi-user data isolation

---

## Testing Strategy

### Backend Tests (pytest)

**Test Coverage Requirements**:
- JWT middleware: 100% (critical security component)
- Task service: 90%+ (business logic)
- API endpoints: 85%+ (integration tests)

**Test Categories**:

1. **Unit Tests** (`test_task_service.py`):
   - CRUD operations
   - User ID filtering
   - Validation rules
   - Error handling

2. **Integration Tests** (`test_task_api.py`):
   - Full request/response cycle
   - Authentication enforcement
   - Authorization checks (user_id matching)
   - Error responses (400, 401, 403, 404)

3. **Security Tests** (`test_auth.py`):
   - JWT verification
   - Expired token handling
   - Invalid token handling
   - User ID extraction

**Test Fixtures** (`conftest.py`):
- Async database session
- Test user with JWT token
- Sample task data
- API client with auth

### Frontend Tests (Jest/Vitest + React Testing Library)

**Test Coverage Requirements**:
- Components: 70%+
- Hooks: 80%+
- Pages: 60%+

**Test Categories**:

1. **Component Tests**:
   - TaskList renders tasks correctly
   - TaskForm validates input
   - PriorityBadge displays correct colors
   - TaskItem toggles completion

2. **Hook Tests**:
   - useTasks fetches and caches data
   - useCreateTask mutation works
   - useToggleComplete optimistic update

3. **Integration Tests**:
   - User can sign up and log in
   - User can create and view tasks
   - User can complete and delete tasks
   - Session expiration redirects to login

---

## Environment Configuration

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host.neon.tech/db?sslmode=require

# Auth
BETTER_AUTH_SECRET=your-shared-secret-here  # Must match frontend

# CORS
FRONTEND_URL=http://localhost:3000

# Server
HOST=0.0.0.0
PORT=8000
```

### Frontend (.env.local)

```bash
# Better Auth
BETTER_AUTH_SECRET=your-shared-secret-here  # Must match backend
DATABASE_URL=postgresql://user:pass@host.neon.tech/db?sslmode=require

# API
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## Deployment Checklist

**Pre-Deployment**:
- [ ] All tests passing (backend + frontend)
- [ ] No TypeScript errors (`npm run build`)
- [ ] No Python type errors (`mypy src/`)
- [ ] Environment variables documented
- [ ] Database migrations tested
- [ ] CORS configured for production domain
- [ ] JWT secret is strong and secure
- [ ] README.md updated with setup instructions

**Production Considerations** (future phases):
- Frontend: Deploy to Vercel/Netlify
- Backend: Deploy to Railway/Render/DigitalOcean
- Database: Neon production tier
- SSL/TLS for all connections
- Rate limiting on API endpoints
- Monitoring and logging

---

## Success Criteria Alignment

| Success Criterion | Implementation |
|-------------------|----------------|
| SC-001: Registration <90s | Simple form, minimal required fields |
| SC-002: Create task <30s | Quick "Add Task" dialog with defaults |
| SC-003: Updates <500ms | Optimistic UI updates with TanStack Query |
| SC-004: Load tasks <2s | Database indexing, async queries |
| SC-005: 95% success rate | Automatic retry, comprehensive error handling |
| SC-006: Zero data leakage | JWT verification, user_id filtering, authorization checks |
| SC-007: Mobile 320px+ | Responsive Tailwind, mobile-first design |
| SC-008: Core flow <3min | Streamlined UX, clear CTAs |
| SC-009: 99% uptime | Neon serverless, FastAPI reliability, error recovery |
| SC-010: Auth <1s | JWT verification, indexed queries |

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Better Auth + FastAPI integration complexity | Thorough research phase, test JWT flow early |
| Neon connection pooling in serverless | Use async connections, test under load |
| JWT token expiration UX | Clear error messages, return URL preservation |
| Mobile responsiveness issues | Mobile-first design, test on real devices |
| Database migration failures | Test migrations locally, backup strategy |
| CORS configuration errors | Test cross-origin requests early |
| Type safety between frontend/backend | Generate TypeScript types from Pydantic schemas |

---

## Next Steps

1. **Complete Phase 0**: Run research tasks to validate all technology choices
2. **Complete Phase 1**: Generate data-model.md, contracts/, and quickstart.md
3. **Update Agent Context**: Run update-agent-context.sh script
4. **Generate Tasks**: Run `/sp.tasks` to create atomic task breakdown
5. **Begin Implementation**: Run `/sp.implement` following task order
6. **Iterate**: Refine specs (never code) if generated output doesn't match requirements

---

## Appendix: Technology Justifications

### Why Better Auth?

- Native Next.js integration with App Router
- Built-in JWT plugin for token-based auth
- Handles complex flows (session management, email verification in future)
- Type-safe TypeScript API
- Extensible for future OAuth providers (Phase II+)

### Why FastAPI?

- Async-first design (optimal for Neon)
- Automatic OpenAPI documentation
- Pydantic validation (type-safe)
- High performance (comparable to Node.js)
- Easy dependency injection
- Excellent WebSocket support (future phases)

### Why SQLModel?

- Combines SQLAlchemy (ORM) + Pydantic (validation)
- Type hints for editor support
- Async support out of the box
- Alembic integration for migrations
- Simpler than raw SQLAlchemy

### Why TanStack Query?

- Best-in-class caching and synchronization
- Optimistic updates for great UX
- Automatic retry and error handling
- DevTools for debugging
- TypeScript support

### Why Neon PostgreSQL?

- Serverless (scales to zero, cost-effective)
- Branching for dev/staging/prod
- Built-in connection pooling
- Excellent async support
- Generous free tier for development
