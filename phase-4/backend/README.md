# Todo API Backend

FastAPI backend for Phase II Evolution of Todo.

## Setup

```bash
uv sync
cp .env.example .env
# Edit .env with your configuration
uv run alembic upgrade head
uv run uvicorn todo_api.main:app --reload
```

## Testing

```bash
uv run pytest
```
