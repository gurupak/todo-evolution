# Quickstart: Todo AI Chatbot (Phase III)

**Feature**: 003-todo-ai-chatbot  
**Date**: 2025-12-25  
**Prerequisites**: Phase II completed and running

---

## Overview

This guide walks you through setting up the Phase III AI chatbot feature. You'll copy Phase II code, install new dependencies, run database migrations, configure OpenAI API, and test the chat interface.

**What You'll Build**:
- FastMCP server with 5 task management tools
- OpenAI Agents SDK agent with input/output guardrails
- Chat API endpoint (POST /api/{user_id}/chat)
- React ChatKit UI for natural language task management

**Time Estimate**: 30-45 minutes

---

## Prerequisites

### Required Software
- Python 3.13+
- Node.js 18+ and npm/pnpm
- PostgreSQL access (Neon account from Phase II)
- OpenAI API account with API key

### Completed Steps from Phase II
- ✅ Backend FastAPI server running
- ✅ Frontend Next.js app running
- ✅ Better Auth authentication configured
- ✅ Database schema with `task` and `user` tables
- ✅ JWT authentication working

### Environment Variables from Phase II
- `DATABASE_URL` - Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Better Auth secret key
- `BETTER_AUTH_URL` - Better Auth URL

---

## Step 1: Copy Phase II to Phase III

Create a new directory for Phase III and copy the Phase II codebase:

```bash
# From repository root
mkdir -p phase-3
cp -r phase-2/backend phase-3/backend
cp -r phase-2/frontend phase-3/frontend

cd phase-3
```

**Why copy instead of modify in place?**
- Preserves Phase II as a working baseline
- Allows side-by-side comparison
- Easier rollback if needed

---

## Step 2: Backend Setup

### 2.1 Install New Python Dependencies

```bash
cd phase-3/backend

# Add dependencies to pyproject.toml
# (manually edit file or run commands below)

uv add fastmcp
uv add openai-agents
uv add openai

# Sync environment
uv sync
```

**Updated `pyproject.toml` dependencies section**:
```toml
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.31.0",
    "sqlmodel>=0.0.22",
    "alembic>=1.14.0",
    "asyncpg>=0.29.0",
    "python-jose[cryptography]>=3.3.0",
    "pydantic-settings>=2.5.2",
    "python-multipart>=0.0.12",
    # NEW FOR PHASE III
    "fastmcp>=0.1.0",
    "openai-agents>=0.1.0",
    "openai>=1.50.0",
]
```

### 2.2 Add OpenAI API Key to Environment

Create or update `.env` file in `phase-3/backend/`:

```bash
# Existing from Phase II
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...
BETTER_AUTH_URL=http://localhost:3000

# NEW FOR PHASE III
OPENAI_API_KEY=sk-proj-...
```

**Get OpenAI API Key**:
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy and paste into `.env`

### 2.3 Run Database Migration

Create Alembic migration for new tables:

```bash
cd phase-3/backend

# Generate migration
uv run alembic revision --autogenerate -m "Add conversation and message tables"

# Review generated migration file in alembic/versions/

# Apply migration
uv run alembic upgrade head
```

**Expected output**:
```
INFO  [alembic.runtime.migration] Running upgrade <previous> -> <new>, Add conversation and message tables
```

**Verify tables created**:
```sql
-- Connect to your Neon database and run:
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('conversation', 'message');

-- Should return:
-- conversation
-- message
```

---

## Step 3: Frontend Setup

### 3.1 Install ChatKit Dependencies

```bash
cd phase-3/frontend

npm install @openai/chatkit-react
# or
pnpm add @openai/chatkit-react
```

**Updated `package.json`**:
```json
{
  "dependencies": {
    // ... existing dependencies from Phase II
    "@openai/chatkit-react": "^1.2.0"
  }
}
```

---

## Step 4: Verify Phase II Still Works

Before adding new code, confirm Phase II functionality works in the copied code:

### 4.1 Start Backend

```bash
cd phase-3/backend
uv run fastapi dev src/todo_api/main.py
```

**Expected**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 4.2 Start Frontend

```bash
cd phase-3/frontend
npm run dev
```

**Expected**:
```
Ready - started server on 0.0.0.0:3000
```

### 4.3 Test Phase II Features

1. Navigate to http://localhost:3000
2. Log in with existing account
3. Create a task in Phase II UI
4. Verify task appears in list
5. Mark task complete

**If Phase II features don't work**: Fix before proceeding to Phase III implementation.

---

## Step 5: Implementation Order

With setup complete, implement Phase III in this order:

### Backend (in dependency order)

1. **Models** (no dependencies):
   - `src/todo_api/models/conversation.py`
   - `src/todo_api/models/message.py`

2. **MCP Tools** (depends on: models):
   - `src/todo_api/mcp/__init__.py`
   - `src/todo_api/mcp/tools.py` (5 tools: add, list, complete, delete, update)
   - `src/todo_api/mcp/server.py` (FastMCP instance)

3. **Guardrails** (depends on: nothing):
   - `src/todo_api/agent/__init__.py`
   - `src/todo_api/agent/guardrails.py` (input + output guardrails)

4. **Agent** (depends on: guardrails, MCP tools):
   - `src/todo_api/agent/todo_agent.py` (OpenAI Agents SDK setup)

5. **Service** (depends on: agent, models):
   - `src/todo_api/services/chat_service.py` (orchestration logic)

6. **Router** (depends on: service):
   - `src/todo_api/routers/chat.py` (POST /api/{user_id}/chat)

7. **Main** (depends on: router):
   - Update `src/todo_api/main.py` (register chat router)
   - Update `src/todo_api/config.py` (add OPENAI_API_KEY)

### Frontend (in dependency order)

1. **API Client** (no dependencies):
   - `src/lib/chat-api.ts`

2. **Chat Components** (depends on: API client):
   - `src/components/chat/message-list.tsx`
   - `src/components/chat/chat-interface.tsx`

3. **Chat Page** (depends on: components):
   - `src/app/chat/page.tsx`

4. **Navigation** (depends on: nothing):
   - Update `src/app/layout.tsx` (add "Chat" link)

### Tests (implement after corresponding modules)

1. `tests/test_mcp_tools.py`
2. `tests/test_guardrails.py`
3. `tests/test_chat_api.py`

---

## Step 6: Development Workflow

### Test-Driven Development (TDD)

For each module, follow this cycle:

1. **Write test** (red):
   ```bash
   # Example for MCP tools
   cd phase-3/backend
   # Write tests/test_mcp_tools.py
   uv run pytest tests/test_mcp_tools.py -v
   # EXPECTED: FAIL (not implemented yet)
   ```

2. **Implement module** (green):
   ```bash
   # Write src/todo_api/mcp/tools.py
   uv run pytest tests/test_mcp_tools.py -v
   # EXPECTED: PASS
   ```

3. **Refactor** (clean):
   - Improve code quality
   - Run tests again to ensure still passing

### Manual Testing

After implementing chat endpoint:

```bash
# Test with curl
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer {jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add task to buy groceries"}'

# EXPECTED:
# {
#   "conversation_id": "...",
#   "response": "I've added the task 'Buy groceries' to your list.",
#   "tool_calls": [...]
# }
```

### Integration Testing

After implementing frontend chat UI:

1. Open http://localhost:3000/chat
2. Type: "Add task to buy groceries"
3. Verify AI responds with confirmation
4. Navigate to dashboard (Phase II UI)
5. Verify task appears in list
6. Return to chat
7. Type: "What are my pending tasks?"
8. Verify AI lists the task you just created

---

## Step 7: Guardrails Testing

Test that guardrails block off-topic requests:

### Test Cases

| User Message | Expected Behavior |
|--------------|-------------------|
| "Add task to buy milk" | ✅ Allowed → AI creates task |
| "Show my tasks" | ✅ Allowed → AI lists tasks |
| "What's the weather today?" | ❌ Blocked → Guardrail message |
| "Write me a poem" | ❌ Blocked → Guardrail message |
| "Help me with Python code" | ❌ Blocked → Guardrail message |
| "Hi there" | ✅ Allowed → AI greets user |

**Guardrail Message** (when blocked):
```
I'm your todo assistant and can only help with task management.

I can help you:
• Add new tasks
• View your task list
• Mark tasks complete
• Delete tasks
• Update task details

What would you like to do with your tasks?
```

---

## Step 8: Debugging Common Issues

### Issue: "OPENAI_API_KEY not found"

**Solution**:
```bash
# Verify .env file exists
cat phase-3/backend/.env

# Verify key is set
echo $OPENAI_API_KEY

# If empty, source .env
export $(cat .env | xargs)
```

### Issue: "Conversation not found"

**Cause**: Trying to resume conversation with invalid ID

**Solution**: Omit `conversation_id` to start new conversation:
```json
{
  "message": "Add task to buy groceries"
}
```

### Issue: "Guardrail blocked my task creation"

**Cause**: Guardrail misclassified intent

**Solution**: 
1. Check guardrail agent instructions
2. Add more examples to training
3. Use more explicit phrasing: "Create a task to buy groceries"

### Issue: "Tool not found: add_task"

**Cause**: MCP server not registered with agent

**Solution**: Verify in `todo_agent.py`:
```python
from todo_api.mcp.server import mcp

agent = Agent(
    name="Todo Assistant",
    tools=mcp.get_tools(),  # Make sure this line exists
    ...
)
```

### Issue: "Database error: conversation_id not found"

**Cause**: Migration not applied

**Solution**:
```bash
cd phase-3/backend
uv run alembic current  # Check current revision
uv run alembic upgrade head  # Apply pending migrations
```

---

## Step 9: Verify Complete Implementation

### Backend Checklist

- [ ] MCP tools callable from FastMCP server
- [ ] Guardrails block off-topic messages
- [ ] Agent responds to task creation requests
- [ ] Chat endpoint returns conversation_id and response
- [ ] Conversation history saves to database
- [ ] JWT authentication enforces user isolation

### Frontend Checklist

- [ ] Chat page loads without errors
- [ ] Message input and send button work
- [ ] Messages display in correct order
- [ ] User messages align right
- [ ] Assistant messages align left
- [ ] Navigation link to chat page exists

### Integration Checklist

- [ ] Task created via chat appears in Phase II UI
- [ ] Task completed in Phase II UI affects chat responses
- [ ] User A cannot see User B's conversations
- [ ] Rate limit errors show user-friendly message
- [ ] Off-topic messages blocked with helpful redirect

---

## Step 10: Next Steps

After successful implementation:

1. **Deploy to production**:
   - Update environment variables in production
   - Run migrations on production database
   - Test with production OpenAI API key

2. **Monitor usage**:
   - Track OpenAI API costs
   - Monitor guardrail trigger rate
   - Analyze common user intents

3. **Iterate based on feedback**:
   - Refine guardrail instructions
   - Add more MCP tools (e.g., set priority, add due dates)
   - Improve conversation summary for long histories

---

## Troubleshooting

### Get Help

- **Backend errors**: Check `phase-3/backend/logs/` (if logging configured)
- **Frontend errors**: Check browser console (F12)
- **Database errors**: Check Neon dashboard query logs
- **OpenAI API errors**: Check https://platform.openai.com/usage

### Reset to Clean State

If things break badly:

```bash
# Reset database (WARNING: deletes all conversations)
cd phase-3/backend
uv run alembic downgrade -1  # Undo last migration
uv run alembic upgrade head   # Reapply migration

# Or manually:
# Connect to database and run:
# DROP TABLE message CASCADE;
# DROP TABLE conversation CASCADE;
# Then rerun migration
```

---

## Summary

**What You Built**:
- ✅ MCP server with 5 task management tools
- ✅ AI agent with guardrails for topic validation
- ✅ Stateless chat API with conversation history
- ✅ React ChatKit UI for natural language interaction
- ✅ Database schema for conversation/message storage

**Files Created**: ~15-20 new files
**Lines of Code**: ~800-1000 (backend), ~300-400 (frontend)
**Time to Implement**: 4-6 hours

**Key Learnings**:
- FastMCP simplifies MCP server creation with decorators
- OpenAI Agents SDK provides robust guardrail system
- Stateless design enables horizontal scaling
- ChatKit accelerates frontend chat UI development

---

## Appendix: File Structure Reference

```
phase-3/
├── backend/
│   ├── src/todo_api/
│   │   ├── models/
│   │   │   ├── conversation.py          ← NEW
│   │   │   └── message.py               ← NEW
│   │   ├── mcp/
│   │   │   ├── __init__.py              ← NEW
│   │   │   ├── server.py                ← NEW
│   │   │   └── tools.py                 ← NEW
│   │   ├── agent/
│   │   │   ├── __init__.py              ← NEW
│   │   │   ├── guardrails.py            ← NEW
│   │   │   └── todo_agent.py            ← NEW
│   │   ├── routers/
│   │   │   └── chat.py                  ← NEW
│   │   ├── services/
│   │   │   └── chat_service.py          ← NEW
│   │   ├── config.py                    ← UPDATED
│   │   └── main.py                      ← UPDATED
│   ├── tests/
│   │   ├── test_mcp_tools.py            ← NEW
│   │   ├── test_guardrails.py           ← NEW
│   │   └── test_chat_api.py             ← NEW
│   ├── .env                             ← UPDATED
│   └── pyproject.toml                   ← UPDATED
│
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── chat/
    │   │   │   └── page.tsx             ← NEW
    │   │   └── layout.tsx               ← UPDATED
    │   ├── components/
    │   │   └── chat/
    │   │       ├── chat-interface.tsx   ← NEW
    │   │       └── message-list.tsx     ← NEW
    │   └── lib/
    │       └── chat-api.ts              ← NEW
    └── package.json                     ← UPDATED
```

---

**Ready to implement?** Start with Step 5 and follow the dependency order!
