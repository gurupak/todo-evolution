# Phase II: Full-Stack Web Todo Application

Multi-user web application with authentication, persistent storage, and responsive design.

## Tech Stack

**Frontend**: Next.js 16 (App Router), TypeScript, shadcn/ui, Tailwind CSS, TanStack Query, Better Auth  
**Backend**: FastAPI, Python 3.13+, SQLModel, Alembic, Neon PostgreSQL  
**Auth**: Better Auth (JWT tokens, 24-hour expiration)

## Quick Start

### Prerequisites
- Python 3.13+ with UV package manager
- Node.js 20+ with npm
- Neon PostgreSQL database (cloud)

### Backend Setup
```bash
cd phase-2/backend
uv sync
cp .env.example .env
# Edit .env with your DATABASE_URL and BETTER_AUTH_SECRET
uv run alembic upgrade head
uv run uvicorn todo_api.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd phase-2/frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with configuration
npm run dev
```

### First-Time User Flow
1. Navigate to http://localhost:3000
2. Click "Sign Up" and create an account
3. Add your first task from the dashboard

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Shared secret for JWT verification (must match frontend)
- `FRONTEND_URL`: Frontend URL for CORS (default: http://localhost:3000)

### Frontend (.env.local)
- `BETTER_AUTH_SECRET`: Shared secret (same as backend)
- `DATABASE_URL`: Neon PostgreSQL connection string (for Better Auth)
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## Development

### Run Tests
```bash
# Backend
cd phase-2/backend
uv run pytest

# Frontend
cd phase-2/frontend
npm test
```

### Linting
```bash
# Backend
cd phase-2/backend
uv run ruff check .
uv run ruff format .

# Frontend
cd phase-2/frontend
npm run lint
```

## Project Structure

```
phase-2/
├── backend/          # FastAPI application
│   ├── src/todo_api/
│   ├── tests/
│   ├── alembic/
│   └── pyproject.toml
└── frontend/         # Next.js application
    ├── src/app/
    ├── src/components/
    └── package.json
```

## Features

- ✅ User registration and authentication (Better Auth + JWT)
- ✅ Secure multi-user data isolation
- ✅ Create, view, edit, delete tasks
- ✅ Task completion tracking with timestamps
- ✅ Priority levels (high, medium, low)
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Real-time UI updates (optimistic updates)
- ✅ Comprehensive test coverage
- ✅ Production-ready error handling

## API Endpoints

- `POST /api/auth/signup` - Register new user
- `POST /api/auth/signin` - Login user
- `GET /api/{user_id}/tasks` - List all tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{task_id}` - Get task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle completion

## Documentation

See [specs/002-phase2-webapp/](../specs/002-phase2-webapp/) for detailed specifications.
