---
id: "0020"
title: "Fix Pytest Command Issue"
stage: "misc"
date: 2025-12-26
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "003-todo-ai-chatbot"
branch: "003-todo-ai-chatbot"
user: "agent"
command: "/sp.implement"
labels: ["troubleshooting", "pytest", "uv", "testing", "documentation"]
links:
  spec: "specs/003-todo-ai-chatbot/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - phase-3/backend/RUN_TESTS.md
  - phase-3/backend/run-test-t054.sh
tests:
  - None
---

## Prompt

```text
Irfan Ahmed@Gurupak MINGW64 /d/workspace/nextjs/hackathon-todo/phase-3/backend (003-todo-ai-chatbot)
$ pytest tests/test_integration_t054.py -v
bash: pytest: command not found
```

User encountered error when trying to run the integration test T054. The command `pytest` was not found in the shell.

## Response snapshot

**Problem Identified**: User tried to run `pytest` directly, but it's not in the PATH because the project uses UV for Python package management.

**Root Cause**: 
- This project uses UV (modern Python package manager)
- pytest is installed in UV's virtual environment (`.venv/`)
- Running `pytest` directly fails because it's not globally installed
- Need to use `uv run pytest` to execute commands in the UV environment

**Solutions Provided**:

1. **Comprehensive Testing Guide** (`RUN_TESTS.md`):
   - Explained why `pytest` command fails
   - Documented two methods to run tests:
     - **Method 1**: `uv run pytest` (recommended, no environment activation needed)
     - **Method 2**: Activate virtual environment first, then run pytest
   - Provided command reference for different test scenarios
   - Added troubleshooting section for common errors
   - Included CI/CD integration examples
   - Best practices for testing workflow

2. **Quick Test Script** (`run-test-t054.sh`):
   - Bash script to run T054 with one command
   - Automatic prerequisite checks (.env file, pyproject.toml)
   - Dependency sync with `uv sync`
   - Runs test with verbose output
   - Color-coded success/failure messages
   - Helpful next steps and troubleshooting tips
   - Exit code propagation for CI/CD

**Correct Commands**:

```bash
# Method 1: Using UV (recommended)
cd phase-3/backend
uv run pytest tests/test_integration_t054.py -v

# Method 2: Using shell script
cd phase-3/backend
./run-test-t054.sh

# Method 3: Activate virtual environment
cd phase-3/backend
uv sync
source .venv/Scripts/activate  # Windows Git Bash
pytest tests/test_integration_t054.py -v
```

**Documentation Highlights**:

- **Quick Start**: Immediate solution at top of RUN_TESTS.md
- **Why Section**: Explains the error for learning
- **Methods Comparison**: Pros/cons of each approach
- **Command Reference**: Organized by use case (specific file, markers, coverage, verbosity)
- **Troubleshooting**: 4 common errors with solutions
- **CI/CD Examples**: GitHub Actions workflow snippet
- **Best Practices**: Recommended workflow patterns

**Files Created**:
- `phase-3/backend/RUN_TESTS.md` (comprehensive guide, 350+ lines)
- `phase-3/backend/run-test-t054.sh` (convenience script, 75 lines)

## Outcome

- ✅ Impact: User can now run integration tests correctly using UV. Comprehensive documentation prevents future confusion.
- 🧪 Tests: No new tests created (troubleshooting task)
- 📁 Files: 2 created (RUN_TESTS.md, run-test-t054.sh)
- 🔁 Next prompts: User should run `uv run pytest tests/test_integration_t054.py -v` or `./run-test-t054.sh` to execute tests
- 🧠 Reflection: Common issue when using UV-managed projects. Creating both comprehensive documentation and convenience script addresses immediate need and prevents future issues. The shell script provides guardrails (checks for .env, pyproject.toml) and helpful error messages.

## Evaluation notes (flywheel)

- Failure modes observed: User unfamiliar with UV package manager, attempted to run pytest directly
- Graders run and results (PASS/FAIL): N/A (documentation task)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): User should run `cd phase-3/backend && uv run pytest tests/test_integration_t054.py -v` to verify tests execute correctly
