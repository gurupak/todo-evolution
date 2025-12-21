# Phase II Quickstart Guide

**Feature**: Phase II - Full-Stack Web Application  
**Date**: 2025-12-19  
**Estimated Setup Time**: 15-20 minutes

---

## Prerequisites

Ensure you have the following installed:

- **Node.js**: 18.0.0 or higher
- **Python**: 3.13 or higher
- **UV**: Latest version (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Git**: For version control
- **Neon Account**: Free tier at https://neon.tech

---

## Step 1: Database Setup (Neon)

1. **Create Neon Account**:
   - Visit https://neon.tech and sign up
   - Create a new project named "todo-evolution"

2. **Get Connection String**:
   - Copy the connection string from Neon dashboard
   - It will look like: `postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/dbname`

3. **Enable Better Auth Tables**:
   - Better Auth will automatically create user/session/account tables
   - We'll create the task table via Alembic migration

---

## Step 2: Backend Setup

```bash
# Navigate to backend directory
cd phase-2/backend

# Install dependencies with UV
uv sync

# Create environment file
cp .env.example .env

# Edit .env and configure:
# DATABASE_URL=postgresql+asyncpg://user:pass@host.neon.tech/db?sslmode=require
# BETTER_AUTH_SECRET=your-random-32-char-secret-here
# FRONTEND_URL=http://localhost:3000

# Run database migrations
uv run alembic upgrade head

# Start development server
uv run uvicorn todo_api.main:app --reload --port 8000
```

**Verify Backend**:
- Visit http://localhost:8000/docs
- You should see FastAPI's auto-generated API documentation

---

## Step 3: Frontend Setup

```bash
# Open a new terminal
# Navigate to frontend directory
cd phase-2/frontend

# Install dependencies
npm install

# Initialize shadcn/ui (if not already done)
npx shadcn@latest init

# Create environment file
cp .env.local.example .env.local

# Edit .env.local and configure:
# BETTER_AUTH_SECRET=same-secret-as-backend
# DATABASE_URL=postgresql://user:pass@host.neon.tech/db?sslmode=require
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_APP_URL=http://localhost:3000

# Start development server
npm run dev
```

**Verify Frontend**:
- Visit http://localhost:3000
- You should see the landing page with sign up/sign in links

---

## Step 4: First-Time User Flow

1. **Register Account**:
   - Click "Sign Up"
   - Enter name, email, password
   - Click "Create Account"
   - You'll be redirected to the dashboard

2. **Create First Task**:
   - Click "Add Task" button
   - Enter title: "Test my todo app"
   - Select priority: High
   - Click "Create"
   - Task appears in the list

3. **Test Task Operations**:
   - Click checkbox to mark complete
   - Click task to view details
   - Click edit to update
   - Click delete to remove

---

## Environment Variables Reference

### Backend (.env)

| Variable | Example | Required | Purpose |
|----------|---------|----------|---------|
| DATABASE_URL | `postgresql+asyncpg://...` | Yes | Neon PostgreSQL connection |
| BETTER_AUTH_SECRET | `random-32-char-string` | Yes | JWT signing/verification |
| FRONTEND_URL | `http://localhost:3000` | Yes | CORS allowed origin |
| HOST | `0.0.0.0` | No | Server bind address (default: 0.0.0.0) |
| PORT | `8000` | No | Server port (default: 8000) |
| DEBUG | `true` | No | Enable debug logging |

### Frontend (.env.local)

| Variable | Example | Required | Purpose |
|----------|---------|----------|---------|
| BETTER_AUTH_SECRET | `same-as-backend` | Yes | Must match backend secret |
| DATABASE_URL | `postgresql://...` | Yes | Better Auth database |
| NEXT_PUBLIC_API_URL | `http://localhost:8000` | Yes | FastAPI backend URL |
| NEXT_PUBLIC_APP_URL | `http://localhost:3000` | Yes | Frontend base URL |

**Important**: `BETTER_AUTH_SECRET` MUST be identical in both backend and frontend!

---

## Common Commands

### Backend

```bash
# Install dependencies
uv sync

# Run migrations
uv run alembic upgrade head

# Create new migration
uv run alembic revision --autogenerate -m "description"

# Start server
uv run uvicorn todo_api.main:app --reload

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=todo_api --cov-report=html

# Type checking
uv run mypy src/

# Linting
uv run ruff check .

# Format code
uv run ruff format .
```

### Frontend

```bash
# Install dependencies
npm install

# Install shadcn component
npx shadcn@latest add button

# Start dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run tests
npm test

# Type checking
npm run type-check

# Linting
npm run lint
```

---

## Troubleshooting

### Backend Issues

**Error: "ModuleNotFoundError: No module named 'todo_api'"**
- Solution: Run `uv sync` to install dependencies

**Error: "Could not connect to database"**
- Check DATABASE_URL format includes `?sslmode=require`
- Verify Neon database is running
- Test connection with: `psql $DATABASE_URL`

**Error: "JWT verification failed"**
- Ensure BETTER_AUTH_SECRET matches between backend and frontend
- Secret must be at least 32 characters

### Frontend Issues

**Error: "Failed to fetch tasks"**
- Verify backend is running on http://localhost:8000
- Check NEXT_PUBLIC_API_URL is correct
- Check browser console for CORS errors

**Error: "Authentication failed"**
- Clear browser cookies and localStorage
- Verify BETTER_AUTH_SECRET matches backend
- Check DATABASE_URL for Better Auth

**Error: "shadcn component not found"**
- Run `npx shadcn@latest init` first
- Then install specific component: `npx shadcn@latest add button`

---

## Next Steps

After successful setup:

1. **Read the Specification**: Review `specs/002-phase2-webapp/spec.md`
2. **Understand the Plan**: Review `specs/002-phase2-webapp/plan.md`
3. **Explore Contracts**: Review `specs/002-phase2-webapp/contracts/`
4. **Run Tests**: Execute `uv run pytest` (backend) and `npm test` (frontend)
5. **Generate Tasks**: Run `/sp.tasks` to create implementation task breakdown
6. **Start Implementation**: Run `/sp.implement` to generate code from specs

---

## Development Workflow

```
┌─────────────────────────────────────────────────┐
│  1. Spec Written (✓ completed)                  │
│  2. Clarifications (✓ completed)                │
│  3. Plan Created (✓ completed)                  │
│  4. Tasks Generated (← you are here)            │
│  5. Implementation (via /sp.implement)          │
│  6. Testing (run tests)                         │
│  7. Refinement (update specs if needed)         │
└─────────────────────────────────────────────────┘
```

---

## Port Reference

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend | 8000 | http://localhost:8000 |
| Backend Docs | 8000 | http://localhost:8000/docs |
| Neon Database | 5432 | (via connection string) |

---

## Quick Health Check

Run these commands to verify everything is working:

```bash
# Backend health
curl http://localhost:8000/docs
# Should return FastAPI docs page

# Frontend health
curl http://localhost:3000
# Should return HTML

# Database connection
# (from backend directory)
uv run python -c "from todo_api.database import engine; import asyncio; asyncio.run(engine.connect())"
# Should connect without errors
```

---

## Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review error messages carefully
3. Verify all environment variables are set correctly
4. Ensure all prerequisites are installed
5. Check that ports 3000 and 8000 are not in use
6. Review the specification and plan documents

---

**Ready to start?** Follow steps 1-4 above to get your development environment running!
