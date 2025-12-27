---
id: "0021"
title: "Fix Config Import Error"
stage: "refactor"
date: 2025-12-26
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "003-todo-ai-chatbot"
branch: "003-todo-ai-chatbot"
user: "agent"
command: "/sp.implement"
labels: ["bugfix", "import-error", "configuration", "refactor"]
links:
  spec: "specs/003-todo-ai-chatbot/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - phase-3/backend/src/todo_api/dependencies.py
tests:
  - None
---

## Prompt

```text
Irfan Ahmed@Gurupak MINGW64 /d/workspace/nextjs/hackathon-todo/phase-3/backend (003-todo-ai-chatbot)
$ uv run pytest tests/test_integration_t054.py -v -m integration
ImportError while loading conftest 'D:\workspace\nextjs\hackathon-todo\phase-3\backend\tests\conftest.py'.
tests\conftest.py:13: in <module>
    from todo_api.main import app
src\todo_api\main.py:7: in <module>
    from .routers import chat, tasks
src\todo_api\routers\chat.py:16: in <module>
    from todo_api.dependencies import get_current_user
src\todo_api\dependencies.py:11: in <module>
    from todo_api.config import get_settings
E   ImportError: cannot import name 'get_settings' from 'todo_api.config' (D:\workspace\nextjs\hackathon-todo\phase-3\backend\src\todo_api\config.py)
```

User encountered an ImportError when trying to run integration tests. The error showed that `dependencies.py` was trying to import `get_settings` function from `config.py`, but that function doesn't exist.

## Response snapshot

**Problem Identified**: Import mismatch between `dependencies.py` and `config.py`

**Root Cause**:
- `config.py` exports a global `settings` instance (line 28: `settings = Settings()`)
- `dependencies.py` was trying to import `get_settings()` function that doesn't exist
- This causes ImportError when loading the application

**Analysis**:
Checked `config.py` structure:
```python
class Settings(BaseSettings):
    # Configuration fields...
    
# Global settings instance
settings = Settings()
```

The config module exports the `settings` instance directly, not a `get_settings()` function.

**Fix Applied**:
Changed import in `dependencies.py` from:
```python
from todo_api.config import get_settings

async def get_current_user(...):
    settings = get_settings()  # Function call
    token = credentials.credentials
```

To:
```python
from todo_api.config import settings

async def get_current_user(...):
    token = credentials.credentials  # Use module-level settings directly
```

**Why This Works**:
- The `settings` instance is created once when the module loads
- It reads environment variables from `.env` file automatically
- No need for a function to create/return settings
- Simpler and more efficient (singleton pattern)

**Verification**:
- Searched codebase for other occurrences of `get_settings` import: None found
- This was the only file with the incorrect import

**Files Modified**:
- `phase-3/backend/src/todo_api/dependencies.py` (changed import statement, removed unnecessary local variable)

## Outcome

- ✅ Impact: Fixed ImportError blocking all test execution. Application can now start properly.
- 🧪 Tests: No new tests created (bugfix for existing code)
- 📁 Files: 1 modified (dependencies.py)
- 🔁 Next prompts: User should re-run `uv run pytest tests/test_integration_t054.py -v -m integration` to execute tests
- 🧠 Reflection: This was a simple import error from inconsistent naming between config module and its usage. The fix aligns with FastAPI best practices (global settings instance rather than dependency injection for settings). The module-level singleton pattern is more efficient than calling a function on every request.

## Evaluation notes (flywheel)

- Failure modes observed: Import mismatch between module export and usage. Likely occurred during implementation when different patterns were used.
- Graders run and results (PASS/FAIL): N/A (bugfix, tests should now be runnable)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): User should run `cd phase-3/backend && uv run pytest tests/test_integration_t054.py -v -m integration` to verify tests execute without import errors
