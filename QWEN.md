# QWEN.md - Hackathon Todo App

## Project Overview

This is a multi-phase todo application built using **Spec-Driven Development (SDD)** methodology. The project demonstrates progressive enhancement from a simple CLI to a cloud-native application. The project follows a systematic approach where each phase builds upon the previous work while maintaining backward compatibility and comprehensive specifications.

### Project Philosophy

- **Spec-First Development**: Complete specifications before implementation
- **Test-Driven**: Comprehensive test coverage for all features
- **Progressive Enhancement**: Each phase builds on previous work
- **Production Ready**: Focus on code quality, error handling, and user experience

## Current Status

### Phase I - In-Memory Python Console Todo App (Complete)

**Location**: `phase-1/`
**Tech Stack**: Python 3.13+, UV, questionary, rich, pyfiglet, pytest

A beautiful interactive CLI todo application with rich terminal UI and comprehensive task management features.

#### Features

- **Add Tasks** - Interactive prompts with validation
- **List Tasks** - Rich formatted table with sorting
- **Update Tasks** - Modify title, description, due date, or priority
- **Delete Tasks** - Confirmation-based deletion
- **Mark Complete/Incomplete** - Status tracking with timestamps
- **Due Dates** - Interactive date picker with overdue indicators
- **Priority Levels** - High (🔴), Medium (🟡), Low (🟢)
- **Help System** - Comprehensive command reference
- **Error Handling** - Graceful degradation with helpful tips

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

## Upcoming Phases

### Phase II - File Persistence & Data Export
- JSON/CSV file storage
- Import/export functionality
- Data migration tools
- Backup & restore

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

## Development Workflow

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

## Building and Running Phase I

### Prerequisites:
- Python 3.13 or higher
- [UV package manager](https://docs.astral.sh/uv/)

### Installation & Run:

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

## Development Conventions

### Code Quality Standards

**Python Standards:**
- Type hints on ALL functions, methods, and variables
- Docstrings for all public functions, classes, and modules
- Use `dataclasses` or `Pydantic` for data models
- PEP 8 naming conventions strictly enforced
- Single responsibility principle for all functions
- Maximum function length: 20 lines
- Maximum file length: 200 lines
- No global mutable state

### CLI User Experience Excellence

**Interaction Philosophy:**
- **Guided Input Over Free-Form:** Prefer dropdown/selection menus over typing when options are finite
- **Progressive Disclosure:** Show options only when relevant to current context
- **Immediate Feedback:** Confirm every action with clear success/error messages
- **Forgiving Input:** Accept partial matches, case-insensitive commands
- **Graceful Exit:** Allow user to cancel/go back at any prompt (Esc, Ctrl+C)
- **Visual Hierarchy:** Use colors, icons, and formatting to guide user attention

**Input Type Standards:**
- Command selection: Arrow-key menu OR typed command (both supported)
- Yes/No confirmation: Arrow-key selection between options
- Single selection from finite list: Arrow-key dropdown
- Task selection: Arrow-key list with task preview
- Free text (title, description): Standard text input with validation

**Visual Feedback Standards:**
- Success: Green ✓ with descriptive message
- Error: Red ✗ with helpful guidance and tips
- Warning: Yellow ⚠ with explanation
- Info: Blue ℹ for neutral information
- Tables: Rich formatted tables with borders

### Error Handling Philosophy
- Graceful handling of ALL invalid input
- Clear, user-friendly error messages with actionable guidance
- Never crash on bad input - always recover gracefully
- Validate all inputs before processing
- Provide helpful tips on how to fix errors

## Project Structure

```
hackathon-todo/
├── README.md                    # Project overview
├── .specify/                    # SpecKit Plus configuration
│   ├── memory/
│   │   └── constitution.md      # Project principles
│   ├── templates/               # Spec templates
│   └── scripts/                 # Automation scripts
├── specs/                       # Feature specifications
│   └── 001-phase1-todo-cli/     # Phase I specs
├── history/                     # Development history
│   ├── prompts/                 # Prompt History Records (PHRs)
│   └── adr/                     # Architecture Decision Records
├── phase-1/                     # Phase I implementation
├── phase-2/                     # (Coming soon)
└── .gitignore                   # Git ignore patterns
```

## Testing

Phase I has 25 tests with 100% pass rate:
- Core modules: 100% coverage (models, storage)
- Interactive modules: Tested with mocked prompts
- Overall coverage: 44% (with 100% for core modules)

## Key Design Patterns

- **Dependency Injection**: Storage instance passed to all command functions
- **Singleton Console**: Single rich.Console instance with custom theme
- **Dataclass with Factories**: Auto-generation of UUID and timestamps
- **Pattern Matching**: `match/case` for command routing in main loop
- **Union Types**: Modern Python 3.10+ syntax (`Task | None` instead of `Optional[Task]`)

## Important Constraints

- **No persistence**: In-memory storage only (data lost on exit)
- **No database**: Python dict storage, no SQLite/PostgreSQL
- **No web frameworks**: CLI application only
- **No file I/O**: No JSON/CSV export (Phase I scope)

## Security Principles

- Environment variables for ALL secrets - never hardcoded
- Input validation on all user inputs
- SQL injection prevention through ORM (no raw queries for future phases)
- XSS prevention in frontend (for future phases)
- CORS properly configured for allowed origins only (for future phases)

## Performance Principles

- API response time < 200ms for CRUD operations (for future phases)
- Frontend Time to Interactive < 3 seconds (for future phases)
- Database queries MUST use indexes for filtered columns (for future phases)
- Pagination required for all list endpoints (max 50 items) (for future phases)

## Review Criteria

All submissions will be evaluated on:

| Criteria | Weight | What's Evaluated |
|----------|--------|------------------|
| Spec Quality | 40% | Clarity, completeness, proper workflow, refinement evidence |
| Generated Code Quality | 30% | Clean, documented, follows standards, well-organized |
| Functionality | 20% | Features work correctly, proper error handling, good UX |
| Process Documentation | 10% | Preserved spec history, clear README/CLAUDE.md, iteration evidence |

## Constitution Principles

The project is governed by a strict constitution with the following key principles:

1. **Spec-Driven Development**: NO MANUAL CODE WRITING IS PERMITTED
2. **Mandatory Development Workflow**: Spec → Plan → Tasks → Implement → Validate → Refine
3. **Test-First Development**: Tests MUST be written BEFORE implementation specs
4. **Phase-Based Technology Governance**: Technologies are additive across phases
5. **CLI User Experience Excellence**: Professional CLI application standards
6. **Code Quality and Organization Standards**: Strict quality requirements
7. **Documentation and Traceability Requirements**: Complete documentation