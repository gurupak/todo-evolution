# 📋 Hackathon Todo App

A multi-phase todo application built using **Spec-Driven Development (SDD)** methodology. This project demonstrates progressive enhancement from a simple CLI to a cloud-native application.

## 🎯 Project Overview

This project implements a todo management system across multiple phases, with each phase adding new capabilities while maintaining backward compatibility and comprehensive specifications.

### Project Philosophy

- **Spec-First Development**: Complete specifications before implementation
- **Test-Driven**: Comprehensive test coverage for all features
- **Progressive Enhancement**: Each phase builds on previous work
- **Production Ready**: Focus on code quality, error handling, and user experience

## 📦 Current Status

### ✅ Phase I - In-Memory Python Console Todo App

**Status**: Complete  
**Location**: `phase-1/`  
**Tech Stack**: Python 3.13+, UV, questionary, rich, pyfiglet, pytest

A beautiful interactive CLI todo application with rich terminal UI and comprehensive task management features.

#### Features

- ✅ **Add Tasks** - Interactive prompts with validation
- ✅ **List Tasks** - Rich formatted table with sorting
- ✅ **Update Tasks** - Modify title, description, due date, or priority
- ✅ **Delete Tasks** - Confirmation-based deletion
- ✅ **Mark Complete/Incomplete** - Status tracking with timestamps
- ✅ **Due Dates** - Interactive date picker with overdue indicators
- ✅ **Priority Levels** - High (🔴), Medium (🟡), Low (🟢)
- ✅ **Help System** - Comprehensive command reference
- ✅ **Error Handling** - Graceful degradation with helpful tips

#### Quick Start

**Prerequisites:**
- Python 3.13 or higher
- [UV package manager](https://docs.astral.sh/uv/)

**Installation & Run:**

```bash
# Navigate to Phase I directory
cd phase-1

# Install dependencies (UV auto-creates virtual environment)
uv sync

# Run the application
uv run todo

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=todo --cov-report=term-missing
```

#### Usage Examples

**Adding a Task:**
```
? Enter task title: Complete project documentation
? Enter task description (optional): Write README and API docs
? Select due date:
  ❯ Tomorrow (2025-12-20)
? Select priority:
  ❯ 🟡 Medium

✓ Task Added
  Complete project documentation
  ID: a1b2c3d4
  Due Date: 2025-12-20
  Priority: 🟡 Medium
  Status: ○ Pending
```

**Listing Tasks:**
```
📋 Your Tasks
┌──────────┬─────────────────┬──────────────┬──────────┬────────┬──────────────┐
│ ID       │ Title           │ Due Date     │ Priority │ Status │ Created      │
├──────────┼─────────────────┼──────────────┼──────────┼────────┼──────────────┤
│ a1b2c3d4 │ Complete docs   │ 2025-12-20   │ 🟡 Medium│ ○ Pend │ 5 mins ago   │
│ b2c3d4e5 │ Review PR #123  │ 🔴 2025-12-19│ 🔴 High  │ ○ Pend │ 1 hour ago   │
│ c3d4e5f6 │ Update tests    │ -            │ 🟢 Low   │ ✓ Comp │ 2025-12-15   │
└──────────┴─────────────────┴──────────────┴──────────┴────────┴──────────────┘

📊 Total: 3 tasks │ ✓ 1 complete │ ○ 2 pending
```

**Interactive Date Picker:**
```
? Select due date:
    No due date
  ❯ Today (2025-12-19)
    Tomorrow (2025-12-20)
    End of this week (2025-12-22)
    Next week (2025-12-26)
    In 1 month (2026-01-18)
    Custom date (enter manually)
```

#### Architecture

**Directory Structure:**
```
phase-1/
├── src/todo/
│   ├── __init__.py       # Package version
│   ├── models.py         # Task & Priority dataclasses
│   ├── storage.py        # InMemoryStorage (CRUD operations)
│   ├── display.py        # Rich UI formatting
│   ├── commands.py       # Command handlers
│   └── main.py           # Entry point & main loop
├── tests/
│   ├── conftest.py       # Test fixtures
│   ├── test_models.py    # Model tests
│   ├── test_storage.py   # Storage tests
│   └── test_commands.py  # Command tests
└── pyproject.toml        # UV project configuration
```

**Key Design Patterns:**
- **Dependency Injection**: Storage passed to all commands
- **Singleton Pattern**: Single Console instance with custom theme
- **Field Factories**: Auto-generation of UUIDs and timestamps
- **Pattern Matching**: Modern Python `match/case` for routing

**Test Coverage:**
- 25 tests, 100% pass rate
- Core modules: 100% coverage (models, storage)
- Interactive modules: Tested with mocked prompts

#### Documentation

- **Specification**: [`specs/001-phase1-todo-cli/spec.md`](specs/001-phase1-todo-cli/spec.md)
- **Plan**: [`specs/001-phase1-todo-cli/plan.md`](specs/001-phase1-todo-cli/plan.md)
- **Tasks**: [`specs/001-phase1-todo-cli/tasks.md`](specs/001-phase1-todo-cli/tasks.md)
- **Data Model**: [`specs/001-phase1-todo-cli/data-model.md`](specs/001-phase1-todo-cli/data-model.md)
- **Quickstart Guide**: [`specs/001-phase1-todo-cli/quickstart.md`](specs/001-phase1-todo-cli/quickstart.md)

#### Known Limitations

- **In-Memory Only**: Data lost when application exits
- **Single User**: No multi-user support
- **No Persistence**: Tasks not saved to disk
- **Local Only**: No network/sync capabilities

## 📦 Current Status

### ✅ Phase II - Full-Stack Web Application

**Status**: Complete
**Location**: `phase-2/`
**Tech Stack**: Next.js 15+, FastAPI, PostgreSQL, Better Auth, shadcn/ui, Tailwind CSS

A modern full-stack web application with user authentication, persistent storage, and responsive UI.

#### Features

- ✅ **User Authentication** - Email/password sign up and sign in with Better Auth
- ✅ **Multi-User Support** - Each user has isolated task data
- ✅ **Create Tasks** - Add tasks with title, description, priority, and due dates
- ✅ **List Tasks** - View all tasks with sorting and filtering
- ✅ **Update Tasks** - Modify task details after creation
- ✅ **Delete Tasks** - Remove tasks with confirmation modal
- ✅ **Mark Complete/Incomplete** - Toggle task completion status
- ✅ **Priority Levels** - High (🔴), Medium (🟡), Low (🟢)
- ✅ **Due Date Tracking** - Visual indicators for due and overdue tasks
- ✅ **Responsive Design** - Works on mobile, tablet, and desktop
- ✅ **Secure Session Management** - Proper authentication and authorization

#### Quick Start

**Prerequisites:**
- Node.js 18+
- Python 3.13+
- PostgreSQL database

**Backend Setup:**

```bash
# Navigate to Phase II backend directory
cd phase-2/backend

# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL and auth secret

# Run database migrations
uv run alembic upgrade head

# Start the backend server
uv run dev
```

**Frontend Setup:**

```bash
# Navigate to Phase II frontend directory
cd phase-2/frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local
# Edit .env.local with your backend URL and auth secret

# Start the development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

#### Architecture

**Directory Structure:**
```
phase-2/
├── backend/                    # FastAPI backend
│   ├── src/todo_api/
│   │   ├── models/            # SQLModel database models
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── routers/           # API route handlers
│   │   ├── services/          # Business logic
│   │   ├── middleware/        # Auth and other middleware
│   │   ├── database.py        # Database configuration
│   │   └── main.py            # FastAPI application
│   ├── alembic/               # Database migration scripts
│   └── pyproject.toml         # Backend dependencies
├── frontend/                   # Next.js frontend
│   ├── src/
│   │   ├── app/               # Next.js 13+ App Router pages
│   │   ├── components/        # Reusable UI components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── lib/               # Utilities and configuration
│   │   └── types/             # TypeScript type definitions
│   ├── package.json           # Frontend dependencies
│   └── next.config.ts         # Next.js configuration
└── README.md                  # Phase II documentation
```

**Key Design Patterns:**
- **Next.js App Router**: Modern file-based routing system
- **Server Components**: Data fetching and rendering on the server
- **TanStack Query**: Client-side state management and caching
- **SQLModel**: Type-safe database models and queries
- **Better Auth**: Secure authentication and session management

**Database Schema:**
- **users**: User account information
- **tasks**: Task data with user relationships
- **sessions**: Authentication session storage
- **accounts**: OAuth account linking (future use)

#### Documentation

- **Specification**: [`specs/002-phase2-webapp/spec.md`](specs/002-phase2-webapp/spec.md)
- **Plan**: [`specs/002-phase2-webapp/plan.md`](specs/002-phase2-webapp/plan.md)
- **Tasks**: [`specs/002-phase2-webapp/tasks.md`](specs/002-phase2-webapp/tasks.md)
- **Data Model**: [`specs/002-phase2-webapp/data-model.md`](specs/002-phase2-webapp/data-model.md)
- **Quickstart Guide**: [`specs/002-phase2-webapp/quickstart.md`](specs/002-phase2-webapp/quickstart.md)

#### Known Limitations

- **No File Attachments**: Tasks cannot include file uploads
- **Basic Notifications**: No email or push notifications
- **Simple Search**: No advanced search or filtering capabilities
- **Single Language**: English only interface

*(These will be addressed in future phases)*

## 📚 Project Structure

```
hackathon-todo/
├── README.md                    # This file
├── .specify/                    # SpecKit Plus configuration
│   ├── memory/
│   │   └── constitution.md      # Project principles
│   ├── templates/               # Spec templates
│   └── scripts/                 # Automation scripts
├── specs/                       # Feature specifications
│   ├── 001-phase1-todo-cli/     # Phase I specs
│   └── 002-phase2-webapp/       # Phase II specs
├── history/                     # Development history
│   ├── prompts/                 # Prompt History Records (PHRs)
│   └── adr/                     # Architecture Decision Records
├── phase-1/                     # Phase I implementation
├── phase-2/                     # Phase II implementation
└── .gitignore                   # Git ignore patterns
```
*(These will be addressed in future phases)*

## 🚀 Upcoming Phases

### Phase III - MCP Tools for AI Agents
- Model Context Protocol integration
- AI-invokable todo operations
- Agent-friendly APIs

### Phase IV - Cloud-Native Deployment
- Docker containerization
- Kubernetes deployment
- Helm charts
- Cloud infrastructure

### Phase V - Multi-User & Web UI
- REST API
- Web frontend
- User authentication
- Real-time sync

## 🛠️ Development Workflow

This project follows **Spec-Driven Development**:

1. **Specify** - Create detailed feature specifications
2. **Plan** - Design architecture and implementation strategy
3. **Task** - Decompose into actionable tasks
4. **Implement** - Execute tasks with TDD approach
5. **Validate** - Comprehensive testing and review
6. **Document** - Create PHRs and ADRs

### Key Commands

```bash
# Create/update specification
/sp.specify

# Generate implementation plan
/sp.plan

# Generate task breakdown
/sp.tasks

# Execute implementation
/sp.implement

# Record development session
/sp.phr
```

## 📊 Metrics

### Phase I Statistics

- **Lines of Code**: 1,027 (738 source + 289 tests)
- **Test Coverage**: 44% overall (100% for core modules)
- **Test Pass Rate**: 100% (25/25 tests passing)
- **Test Duration**: ~0.5 seconds
- **User Stories**: 5 (2 P1, 3 P2)
- **Tasks Completed**: 28/28

### Phase II Statistics

- **Lines of Code**: ~3,500 (Backend: ~1,500, Frontend: ~2,000)
- **Test Coverage**: Unit tests for core business logic
- **Test Pass Rate**: 100% for critical path operations
- **User Stories**: 7 (3 P1, 3 P2, 1 P3)
- **Tasks Completed**: 42/42
- **Database Models**: 4 (users, tasks, sessions, accounts)
- **API Endpoints**: 6 (CRUD operations for tasks)

## 🤝 Contributing

This is a personal learning project demonstrating Spec-Driven Development methodology. While not currently accepting external contributions, feel free to:

- ⭐ Star the repository
- 🐛 Report issues
- 💡 Suggest features for future phases
- 📖 Learn from the specifications and code

## 📝 License

This project is created for educational and demonstration purposes.

## 🙏 Acknowledgments

- **SpecKit Plus** - Specification-driven development toolkit
- **UV** - Fast Python package manager
- **questionary** - Interactive CLI prompts
- **rich** - Beautiful terminal formatting
- **pytest** - Testing framework

---

**Built with ❤️ using Spec-Driven Development**

*Last Updated: 2025-12-19*
