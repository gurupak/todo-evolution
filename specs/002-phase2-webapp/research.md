# Phase II Technology Research

**Feature**: Phase II - Full-Stack Web Application  
**Date**: 2025-12-19  
**Purpose**: Research and validate technology choices for multi-user web application

---

## 1. Better Auth + FastAPI JWT Integration

### Research Question
How does Better Auth's JWT plugin integrate with FastAPI for token verification?

### Decision
Use Better Auth in Next.js for authentication and session management, with FastAPI backend verifying JWT tokens using a shared secret.

### Implementation Pattern

**Better Auth Configuration (Frontend)**:
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL!,
  },
  plugins: [
    jwt({
      issuer: "todo-app",
      expiresIn: "24h", // From clarification
    }),
  ],
  secret: process.env.BETTER_AUTH_SECRET!,
});
```

**FastAPI JWT Verification (Backend)**:
```python
# middleware/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import JWTError, jwt
from pydantic import BaseModel
from config import settings

security = HTTPBearer()

class TokenData(BaseModel):
    sub: str  # user_id
    email: str

async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security)
) -> TokenData:
    """Verify JWT token and extract user data."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"],
        )
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        
        return TokenData(sub=user_id, email=email)
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
```

### Token Structure
```json
{
  "sub": "uuid-user-id",
  "email": "user@example.com",
  "iss": "todo-app",
  "exp": 1234567890,
  "iat": 1234567890
}
```

### Shared Secret
- Environment variable: `BETTER_AUTH_SECRET`
- Must be identical in both frontend and backend
- Minimum 32 characters, cryptographically random
- Never commit to version control

### Rationale
- Better Auth handles complex auth flows (registration, login, session)
- FastAPI focuses on business logic, not auth implementation
- JWT enables stateless authentication (no backend session storage)
- Shared secret approach is simple and sufficient for Phase II

### Alternatives Considered
- **NextAuth.js**: Similar but less modern, more complex configuration
- **Passport.js backend**: Would require Node.js backend, inconsistent with FastAPI choice
- **Custom JWT implementation**: Reinventing the wheel, higher security risk

---

## 2. Neon PostgreSQL Async Integration

### Research Question
Best practices for using Neon with SQLModel and async SQLAlchemy?

### Decision
Use asyncpg driver with async SQLAlchemy engine, configured for Neon's serverless environment.

### Implementation Pattern

**Database Configuration**:
```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel
from config import settings

# Async engine for Neon
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
    pool_size=5,         # Smaller pool for serverless
    max_overflow=10,
)

# Session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncSession:
    """Dependency for FastAPI routes."""
    async with async_session() as session:
        yield session

async def create_db_and_tables():
    """Create all tables (development only)."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

**Connection String Format**:
```
postgresql+asyncpg://user:password@ep-xxx-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require
```

### Neon-Specific Optimizations
- **Connection Pooling**: Small pool size (5) + overflow (10) for serverless
- **SSL Required**: All connections must use SSL (`?sslmode=require`)
- **Pool Pre-Ping**: Validate connections before use (handles serverless cold starts)
- **Pool Recycle**: Recycle connections after 1 hour (prevents stale connections)

### Alembic Migration Pattern
```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from todo_api.models import SQLModel  # Import all models
from todo_api.config import settings

# Run async migrations
async def run_async_migrations():
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
```

### Rationale
- Neon optimized for async connections (better performance)
- asyncpg is fastest PostgreSQL driver for Python
- SQLModel provides type safety + ORM convenience
- Alembic handles schema migrations reliably

### Alternatives Considered
- **Synchronous SQLAlchemy**: Slower, doesn't leverage Neon's async capabilities
- **Raw asyncpg**: More verbose, no ORM benefits
- **Prisma**: TypeScript-only, doesn't work with Python backend

---

## 3. TanStack Query Patterns for Task Management

### Research Question
Optimal patterns for CRUD operations with TanStack Query?

### Decision
Use TanStack Query (React Query v5) with separate hooks for each operation, cache invalidation on mutations, and optional optimistic updates.

### Implementation Pattern

**Query Hooks** (`hooks/use-tasks.ts`):
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { Task, TaskCreateRequest, TaskUpdateRequest } from '@/types/task';

// Query keys
export const taskKeys = {
  all: ['tasks'] as const,
  lists: () => [...taskKeys.all, 'list'] as const,
  list: (userId: string) => [...taskKeys.lists(), userId] as const,
  details: () => [...taskKeys.all, 'detail'] as const,
  detail: (userId: string, taskId: string) => 
    [...taskKeys.details(), userId, taskId] as const,
};

// Fetch all tasks for user
export function useTasks(userId: string) {
  return useQuery({
    queryKey: taskKeys.list(userId),
    queryFn: () => apiClient.get<Task[]>(`/api/${userId}/tasks`),
    staleTime: 30000, // 30 seconds
  });
}

// Fetch single task
export function useTask(userId: string, taskId: string) {
  return useQuery({
    queryKey: taskKeys.detail(userId, taskId),
    queryFn: () => apiClient.get<Task>(`/api/${userId}/tasks/${taskId}`),
  });
}

// Create task mutation
export function useCreateTask(userId: string) {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: TaskCreateRequest) =>
      apiClient.post<Task>(`/api/${userId}/tasks`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: taskKeys.list(userId) });
    },
  });
}

// Toggle completion mutation
export function useToggleComplete(userId: string, taskId: string) {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: () =>
      apiClient.patch<Task>(`/api/${userId}/tasks/${taskId}/complete`),
    onMutate: async () => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: taskKeys.detail(userId, taskId) });
      
      const previousTask = queryClient.getQueryData<Task>(
        taskKeys.detail(userId, taskId)
      );
      
      if (previousTask) {
        queryClient.setQueryData<Task>(
          taskKeys.detail(userId, taskId),
          { ...previousTask, is_completed: !previousTask.is_completed }
        );
      }
      
      return { previousTask };
    },
    onError: (err, variables, context) => {
      // Rollback on error
      if (context?.previousTask) {
        queryClient.setQueryData(
          taskKeys.detail(userId, taskId),
          context.previousTask
        );
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: taskKeys.list(userId) });
      queryClient.invalidateQueries({ queryKey: taskKeys.detail(userId, taskId) });
    },
  });
}
```

### Cache Invalidation Strategy
- **Create/Update/Delete**: Invalidate list query
- **Complete Toggle**: Optimistic update + invalidate on settle
- **Stale Time**: 30 seconds (balance freshness vs requests)

### Rationale
- Structured query keys enable targeted invalidation
- Optimistic updates provide instant feedback
- Automatic retry (3 attempts) handles transient failures
- DevTools help debug caching issues

### Alternatives Considered
- **SWR**: Similar but less features, smaller community
- **Apollo Client**: GraphQL-focused, overkill for REST API
- **Redux Toolkit Query**: More boilerplate, tighter coupling

---

## 4. Next.js 16 App Router Authentication

### Research Question
How to implement route protection with Better Auth in Next.js 16 App Router?

### Decision
Use Next.js middleware.ts for route-level protection, Better Auth hooks for session state, and Server Components for server-side session checks.

### Implementation Pattern

**Middleware** (`middleware.ts`):
```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { auth } from './lib/auth';

export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  const isAuthPage = request.nextUrl.pathname.startsWith('/auth');
  const isProtectedPage = request.nextUrl.pathname.startsWith('/dashboard');

  // Redirect authenticated users away from auth pages
  if (isAuthPage && session) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // Redirect unauthenticated users to login with return URL
  if (isProtectedPage && !session) {
    const loginUrl = new URL('/auth/signin', request.url);
    loginUrl.searchParams.set('callbackUrl', request.nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/auth/:path*'],
};
```

**Server Component Session Check**:
```typescript
// app/dashboard/page.tsx
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    redirect('/auth/signin');
  }

  return <TaskList userId={session.user.id} />;
}
```

**Client Component Session Hook**:
```typescript
// components/tasks/task-list.tsx
'use client';

import { useSession } from '@/lib/auth-client';

export function TaskList({ userId }: { userId: string }) {
  const { data: session } = useSession();
  
  if (!session) {
    return null; // Middleware handles redirect
  }
  
  // Use session data
  return <div>{session.user.email}</div>;
}
```

### Return URL Preservation
```typescript
// app/auth/signin/page.tsx
'use client';

import { useSearchParams } from 'next/navigation';
import { signIn } from '@/lib/auth-client';

export default function SignInPage() {
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get('callbackUrl') || '/dashboard';

  const handleSubmit = async (data: FormData) => {
    await signIn.email({
      email: data.get('email'),
      password: data.get('password'),
      callbackURL: callbackUrl, // Redirect after login
    });
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

### Rationale
- Middleware runs before page render (fast redirect)
- Server Components provide server-side session validation
- Client hooks enable reactive UI based on session state
- Return URL ensures seamless UX after login

### Alternatives Considered
- **Client-only protection**: Flashes protected content, security risk
- **Higher-order components**: More boilerplate, less type-safe
- **Custom session provider**: Reinventing Better Auth's built-in solution

---

## 5. Responsive Design with shadcn/ui

### Research Question
Best practices for mobile-first responsive design using shadcn/ui components?

### Decision
Use Tailwind's mobile-first breakpoints with shadcn/ui responsive variants, Sheet component for mobile modals, and touch-friendly sizing.

### Implementation Pattern

**Responsive Breakpoints** (Tailwind Config):
```typescript
// tailwind.config.ts
export default {
  theme: {
    screens: {
      'sm': '640px',   // Tablet
      'md': '768px',
      'lg': '1024px',  // Desktop
      'xl': '1280px',
      '2xl': '1536px',
    },
  },
};
```

**Mobile-First Component**:
```typescript
// components/tasks/task-list.tsx
export function TaskList() {
  return (
    <div className="
      w-full
      px-4 sm:px-6 lg:px-8
      py-4 sm:py-6
    ">
      {/* Mobile: Single column, Desktop: Two columns */}
      <div className="
        grid
        grid-cols-1 lg:grid-cols-2
        gap-4
      ">
        <TaskItem />
      </div>
    </div>
  );
}
```

**Mobile Modal Pattern** (Sheet vs Dialog):
```typescript
// components/tasks/task-form-modal.tsx
'use client';

import { useMediaQuery } from '@/hooks/use-media-query';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from '@/components/ui/sheet';

export function TaskFormModal({ open, onOpenChange, children }) {
  const isDesktop = useMediaQuery('(min-width: 768px)');

  if (isDesktop) {
    return (
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Add Task</DialogTitle>
          </DialogHeader>
          {children}
        </DialogContent>
      </Dialog>
    );
  }

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent side="bottom" className="h-[90vh]">
        <SheetHeader>
          <SheetTitle>Add Task</SheetTitle>
        </SheetHeader>
        {children}
      </SheetContent>
    </Sheet>
  );
}
```

**Touch-Friendly Sizing**:
```typescript
// components/ui/button.tsx (shadcn default)
const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",    // 40px = touch-friendly
        icon: "h-9 w-9",                // 36px = acceptable for icons
      },
    },
  }
);
```

**Responsive Table Pattern**:
```typescript
// Mobile: Card layout, Desktop: Table
export function TaskTable({ tasks }) {
  return (
    <>
      {/* Mobile cards */}
      <div className="lg:hidden space-y-4">
        {tasks.map(task => (
          <Card key={task.id}>
            <CardContent className="p-4">
              <div className="flex items-start justify-between">
                <Checkbox className="mt-1" />
                <div className="flex-1 ml-3">
                  <h3 className="font-medium">{task.title}</h3>
                  <PriorityBadge priority={task.priority} />
                </div>
                <DropdownMenu />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Desktop table */}
      <Table className="hidden lg:table">
        <TableHeader>
          <TableRow>
            <TableHead className="w-12">Status</TableHead>
            <TableHead>Title</TableHead>
            <TableHead>Priority</TableHead>
            <TableHead className="w-24">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {tasks.map(task => (
            <TableRow key={task.id}>
              <TableCell><Checkbox /></TableCell>
              <TableCell>{task.title}</TableCell>
              <TableCell><PriorityBadge priority={task.priority} /></TableCell>
              <TableCell><DropdownMenu /></TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>
  );
}
```

### Mobile UX Guidelines
| Element | Mobile | Desktop |
|---------|--------|---------|
| Modals | Sheet (bottom) | Dialog (center) |
| Tables | Card list | Table |
| Navigation | Hamburger menu | Full header |
| Forms | Stacked fields | Grid layout |
| Buttons | min-height: 44px | min-height: 36px |

### Rationale
- Mobile-first approach ensures base experience works everywhere
- Progressive enhancement adds features for larger screens
- shadcn/ui components have built-in responsive variants
- Touch targets ≥44px follow WCAG accessibility guidelines

### Alternatives Considered
- **Separate mobile/desktop components**: Code duplication, harder to maintain
- **CSS Grid only**: Less semantic, harder to reason about
- **Custom breakpoints**: Inconsistent with Tailwind defaults

---

## Summary of Decisions

| Area | Technology | Version | Rationale |
|------|-----------|---------|-----------|
| Frontend Framework | Next.js (App Router) | 16+ | Modern React patterns, Server Components, excellent DX |
| UI Components | shadcn/ui + Tailwind | Latest | Customizable, accessible, beautiful defaults |
| State Management | TanStack Query | 5.x | Best caching, optimistic updates, minimal boilerplate |
| Forms | React Hook Form + Zod | Latest | Type-safe validation, excellent performance |
| Backend Framework | FastAPI | 0.115+ | Async-first, auto-docs, high performance, Pydantic integration |
| ORM | SQLModel | 0.0.22+ | Type-safe, async support, Alembic migrations |
| Database | Neon PostgreSQL | - | Serverless, async-optimized, generous free tier |
| Auth | Better Auth + JWT | 1.x | Modern, Next.js native, JWT support out of the box |
| Testing (Backend) | pytest + pytest-asyncio | Latest | Async support, excellent fixtures, widely adopted |
| Testing (Frontend) | Jest/Vitest + RTL | Latest | Fast, component testing, TypeScript support |

All technology choices align with the constitution's Phase II requirements and prioritize:
1. Type safety (TypeScript, Pydantic, SQLModel)
2. Async operations (FastAPI, asyncpg, TanStack Query)
3. Developer experience (shadcn/ui, Better Auth, TanStack Query)
4. Performance (Neon serverless, optimistic updates, caching)
5. Maintainability (clear separation of concerns, minimal boilerplate)

**All NEEDS CLARIFICATION items from plan.md have been resolved.**
