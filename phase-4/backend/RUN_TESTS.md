# How to Run Tests - Phase III Backend

This project uses **UV** for Python package management. Follow the instructions below to run tests correctly.

---

## Quick Start

### Run Integration Test T054

```bash
cd phase-3/backend

# Method 1: Using UV (recommended)
uv run pytest tests/test_integration_t054.py -v

# Method 2: Run all integration tests
uv run pytest tests/test_integration_t054.py -v -m integration

# Method 3: Run with coverage
uv run pytest tests/test_integration_t054.py -v --cov=todo_api --cov-report=term
```

---

## Why `pytest` command not found?

**Problem**: Running `pytest tests/test_integration_t054.py -v` directly fails with:
```
bash: pytest: command not found
```

**Reason**: pytest is installed in UV's virtual environment, not globally. You need to either:
1. Use `uv run` to execute commands in the UV environment
2. Activate the virtual environment manually

---

## Methods to Run Tests

### Method 1: Using `uv run` (Recommended)

This is the **easiest and recommended** approach:

```bash
# Navigate to backend directory
cd /d/workspace/nextjs/hackathon-todo/phase-3/backend

# Run integration test T054
uv run pytest tests/test_integration_t054.py -v

# Run all tests
uv run pytest -v

# Run tests with markers
uv run pytest -v -m integration  # Only integration tests
uv run pytest -v -m "not integration"  # Skip integration tests
```

**Advantages**:
- No need to activate virtual environment
- Always uses correct Python version
- Automatically manages dependencies

### Method 2: Activate Virtual Environment

If you prefer to activate the environment once and run multiple commands:

```bash
# Navigate to backend directory
cd /d/workspace/nextjs/hackathon-todo/phase-3/backend

# Install dependencies (if not already done)
uv sync

# Activate virtual environment
# On Windows Git Bash:
source .venv/Scripts/activate

# On Linux/Mac:
source .venv/bin/activate

# Now you can run pytest directly
pytest tests/test_integration_t054.py -v

# Run all tests
pytest -v

# Deactivate when done
deactivate
```

**Advantages**:
- Can run multiple commands without `uv run` prefix
- Faster for repeated test runs

**Disadvantages**:
- Must remember to activate/deactivate
- Easy to forget which environment you're in

---

## Test Commands Reference

### Run Specific Test File

```bash
# Integration test T054
uv run pytest tests/test_integration_t054.py -v

# MCP tools tests
uv run pytest tests/test_mcp_tools.py -v

# Guardrails tests
uv run pytest tests/test_guardrails.py -v

# Chat API tests
uv run pytest tests/test_chat_api.py -v
```

### Run Tests by Marker

```bash
# Only integration tests
uv run pytest -v -m integration

# Only unit tests (non-integration)
uv run pytest -v -m "not integration"

# Specific user story tests (if tagged)
uv run pytest -v -m "user_story_1"
```

### Run Tests with Coverage

```bash
# Run with coverage report
uv run pytest tests/test_integration_t054.py -v --cov=todo_api --cov-report=term

# Coverage for all tests
uv run pytest -v --cov=todo_api --cov-report=html

# Open coverage report in browser
# Windows:
start htmlcov/index.html

# Linux/Mac:
open htmlcov/index.html
```

### Run Tests with Different Verbosity

```bash
# Quiet mode (minimal output)
uv run pytest tests/test_integration_t054.py -q

# Normal verbosity
uv run pytest tests/test_integration_t054.py

# Verbose mode (detailed output)
uv run pytest tests/test_integration_t054.py -v

# Very verbose (show test names)
uv run pytest tests/test_integration_t054.py -vv

# Show print statements
uv run pytest tests/test_integration_t054.py -v -s
```

### Run Tests with Output Capture

```bash
# Capture output (default)
uv run pytest tests/test_integration_t054.py -v

# Show print() statements and logging
uv run pytest tests/test_integration_t054.py -v -s

# Show stdout even for passing tests
uv run pytest tests/test_integration_t054.py -v --capture=no
```

---

## Troubleshooting

### Error: `command not found: pytest`

**Solution**: Use `uv run pytest` instead of `pytest`

```bash
# ❌ Wrong
pytest tests/test_integration_t054.py -v

# ✅ Correct
uv run pytest tests/test_integration_t054.py -v
```

### Error: `ModuleNotFoundError: No module named 'todo_api'`

**Solution**: Make sure you're in the backend directory and run `uv sync` first

```bash
cd phase-3/backend
uv sync
uv run pytest tests/test_integration_t054.py -v
```

### Error: `No tests ran`

**Possible causes**:
1. Test file doesn't match pytest's discovery pattern (must be `test_*.py` or `*_test.py`)
2. Test functions don't start with `test_`
3. Wrong directory

**Solution**: Verify file path and naming

```bash
# Check test file exists
ls tests/test_integration_t054.py

# Run from backend directory
pwd  # Should show: /d/workspace/nextjs/hackathon-todo/phase-3/backend
uv run pytest tests/test_integration_t054.py -v
```

### Error: `FAILED test_integration_t054.py::test_t054_full_chat_workflow`

**Possible causes**:
1. Backend server not running
2. Database not migrated
3. Environment variables not set
4. OpenAI API key invalid/missing

**Solution**: Follow prerequisites in INTEGRATION_TEST_T054.md

```bash
# 1. Check environment variables
cat .env

# 2. Run database migrations
uv run alembic upgrade head

# 3. Start backend server (in separate terminal)
uv run fastapi dev src/todo_api/main.py

# 4. Run tests
uv run pytest tests/test_integration_t054.py -v
```

---

## CI/CD Integration

For automated testing in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Install dependencies
  run: |
    cd phase-3/backend
    pip install uv
    uv sync

- name: Run integration tests
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    BETTER_AUTH_SECRET: ${{ secrets.BETTER_AUTH_SECRET }}
    BETTER_AUTH_URL: http://localhost:3000
  run: |
    cd phase-3/backend
    uv run pytest tests/test_integration_t054.py -v
```

---

## Best Practices

1. **Always use `uv run`** for consistency:
   ```bash
   uv run pytest tests/test_integration_t054.py -v
   ```

2. **Run tests before committing**:
   ```bash
   uv run pytest -v
   ```

3. **Check coverage periodically**:
   ```bash
   uv run pytest -v --cov=todo_api --cov-report=term
   ```

4. **Use markers for selective testing**:
   ```bash
   # Quick unit tests during development
   uv run pytest -v -m "not integration"
   
   # Full test suite before push
   uv run pytest -v
   ```

---

## Summary

**✅ Correct Command**:
```bash
cd phase-3/backend
uv run pytest tests/test_integration_t054.py -v
```

**❌ Incorrect Command**:
```bash
cd phase-3/backend
pytest tests/test_integration_t054.py -v  # Will fail with "command not found"
```

**Remember**: This project uses UV, so always prefix Python commands with `uv run` or activate the virtual environment first!
