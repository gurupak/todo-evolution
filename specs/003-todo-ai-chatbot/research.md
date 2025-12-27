# Phase 0 Research: Todo AI Chatbot

**Feature**: 003-todo-ai-chatbot  
**Date**: 2025-12-25  
**Purpose**: Technology evaluation and best practices for MCP server, AI agent, and chat UI integration

---

## Research Questions Resolved

### 1. FastMCP for MCP Server Implementation

**Question**: How to build MCP server with database tools using FastMCP?

**Decision**: Use FastMCP (Python) as the MCP server framework

**Rationale**:
- FastMCP provides decorator-based tool registration (`@mcp.tool`) with automatic schema generation from type hints
- Built-in support for database operations through tool functions
- Integrates seamlessly with FastAPI (already used in Phase II)
- Supports both synchronous and asynchronous database operations
- Provides structured response handling for tool results

**Alternatives Considered**:
- Official MCP Python SDK: More low-level, requires manual schema definition
- Custom MCP implementation: Unnecessary complexity, reinventing the wheel

**Implementation Pattern** (from documentation):
```python
from fastmcp import FastMCP

mcp = FastMCP("Todo Tools")

@mcp.tool
def add_task(user_id: str, title: str, description: str = "") -> dict:
    """Add a new task for the user."""
    # Database operation here
    return {"success": True, "task_id": "..."}
```

**Key Features Used**:
- Tool decorator for automatic registration
- Type hints for parameter validation
- Docstrings for tool descriptions
- Structured dict responses

**Reference**: 
- Library ID: `/jlowin/fastmcp` (1749 code snippets, High reputation, Score: 78)
- Documentation: https://gofastmcp.com

---

### 2. OpenAI Agents SDK for AI Agent with Guardrails

**Question**: How to implement input/output guardrails in OpenAI Agents SDK?

**Decision**: Use OpenAI Agents SDK Python with guardrail decorators

**Rationale**:
- Built-in guardrail system with `@input_guardrail` and `@output_guardrail` decorators
- Guardrails can run dedicated AI agents for validation (agent-in-the-loop pattern)
- Tripwire mechanism stops execution when guardrail triggers
- Pydantic models for structured validation outputs
- Supports async operations for non-blocking validation

**Alternatives Considered**:
- Manual validation with if/else: Fragile, hard to maintain topic detection logic
- Separate validation service: Adds latency and complexity
- LangChain guardrails: Different ecosystem, less integrated with OpenAI models

**Implementation Pattern** (from documentation):
```python
from agents import Agent, input_guardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel

class TopicOutput(BaseModel):
    is_todo_related: bool
    reasoning: str

guardrail_agent = Agent(
    name="Topic Validator",
    instructions="Check if user message is about todo management.",
    output_type=TopicOutput
)

@input_guardrail
async def todo_topic_guard(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    output = result.final_output_as(TopicOutput)
    return GuardrailFunctionOutput(
        output_info=output,
        tripwire_triggered=not output.is_todo_related
    )

main_agent = Agent(
    name="Todo Assistant",
    instructions="Help users manage tasks.",
    input_guardrails=[todo_topic_guard]
)
```

**Key Features Used**:
- Input guardrails run before agent execution
- Output guardrails run after agent execution
- Tripwire mechanism raises exceptions (InputGuardrailTripwireTriggered)
- Guardrail agents use structured Pydantic outputs
- Context preserved across guardrail and main agent

**Exception Handling**:
```python
try:
    result = await Runner.run(agent, user_message)
except InputGuardrailTripwireTriggered:
    return {"response": "I can only help with todo management..."}
```

**Reference**:
- Library ID: `/openai/openai-agents-python` (251 code snippets, High reputation, Score: 90.9)
- Version: v0.2.9
- Documentation: https://openai.github.io/openai-agents-python

---

### 3. ChatKit for React Chat UI

**Question**: How to integrate OpenAI ChatKit into Next.js frontend?

**Decision**: Use `@openai/chatkit-react` npm package (version 1.2.0)

**Rationale**:
- Official OpenAI React component library
- Provides pre-built chat UI with message rendering, input field, and send button
- Supports streaming responses from AI
- Handles conversation state management
- Built-in message alignment (user right, assistant left)
- Customizable through themes and props

**Alternatives Considered**:
- Custom chat UI with React: Time-consuming, risk of UX bugs
- Third-party chat libraries (react-chat-ui, chatscope): Not optimized for AI conversations
- shadcn/ui chat components: Would require significant assembly work

**Implementation Pattern** (from web research):
```tsx
import { ChatKit } from '@openai/chatkit-react'

export function ChatInterface() {
  return (
    <ChatKit
      apiEndpoint="/api/chat"
      authToken={jwtToken}
      onMessage={(message) => console.log('Sent:', message)}
      onResponse={(response) => console.log('Received:', response)}
    />
  )
}
```

**Key Features Used**:
- Built-in UI components (no styling needed initially)
- API integration through endpoint configuration
- JWT authentication support
- Message history rendering
- Loading states and error handling

**Reference**:
- Package: `@openai/chatkit-react@1.2.0`
- Published: 2025-10-27 (very recent)
- Documentation: https://platform.openai.com/docs/guides/chatkit

---

### 4. Stateless Chat API Design with Conversation History

**Question**: How to maintain conversation context without server-side state?

**Decision**: Load full conversation history from database on each request

**Rationale**:
- Enables horizontal scaling (any server can handle any request)
- Simplifies deployment (no sticky sessions or state synchronization)
- Database is source of truth for conversation history
- Conversation ID passed from frontend identifies which history to load
- History truncation happens at 8000 tokens to fit model context window

**Alternatives Considered**:
- In-memory session storage: Doesn't scale, loses data on restart
- Redis/Memcached caching: Adds complexity, eventual consistency issues
- Client-side state only: Can't resume conversations across devices

**Implementation Pattern**:
```python
async def handle_chat(conversation_id: str, new_message: str, user_id: str):
    # 1. Load conversation history from DB
    messages = await db.get_messages(conversation_id, user_id)
    
    # 2. Truncate if over 8000 tokens
    if count_tokens(messages) > 8000:
        messages = truncate_oldest(messages, max_tokens=8000)
    
    # 3. Add new user message
    messages.append({"role": "user", "content": new_message})
    
    # 4. Run agent with full history
    result = await Runner.run(agent, messages)
    
    # 5. Save user message + assistant response to DB
    await db.save_message(conversation_id, "user", new_message)
    await db.save_message(conversation_id, "assistant", result.final_output)
    
    return result
```

**Performance Optimization**:
- Index on (conversation_id, created_at) for fast message retrieval
- Limit query to most recent N messages (e.g., 50) before token counting
- Consider conversation summary for very long histories (future enhancement)

---

### 5. Database Tools with User Isolation

**Question**: How to ensure MCP tools only access user's own tasks?

**Decision**: Pass user_id as required parameter to all MCP tools

**Rationale**:
- Every tool function receives user_id from chat endpoint
- All database queries filter by user_id: `WHERE user_id = :user_id`
- Prevents cross-user data leakage
- Enforced at database query level, not just application logic
- Uses existing Phase II user authentication

**Implementation Pattern**:
```python
@mcp.tool
def list_tasks(user_id: str, status: str = "all") -> dict:
    """List tasks for the authenticated user."""
    with Session(engine) as session:
        query = select(Task).where(Task.user_id == user_id)
        
        if status == "pending":
            query = query.where(Task.is_completed == False)
        elif status == "completed":
            query = query.where(Task.is_completed == True)
        
        tasks = session.exec(query).all()
        
        return {
            "success": True,
            "count": len(tasks),
            "tasks": [task.model_dump() for task in tasks]
        }
```

**Security Considerations**:
- JWT validation extracts user_id before calling MCP tools
- No tool accepts task_id without user_id verification
- Foreign key constraints prevent orphaned data
- Audit logging for all tool executions (who, what, when)

---

### 6. PostgreSQL Integration with FastMCP

**Question**: How to connect FastMCP tools to existing PostgreSQL database?

**Decision**: Reuse Phase II database connection, inject session into tools

**Rationale**:
- Phase II already has SQLModel + asyncpg setup with Neon PostgreSQL
- MCP tools are synchronous functions that can use sync SQLModel sessions
- Connection pooling handled by existing database.py module
- No need for separate MCP database connection

**Implementation Pattern**:
```python
# In mcp/tools.py
from todo_api.database import engine
from sqlmodel import Session, select

@mcp.tool
def add_task(user_id: str, title: str, description: str = "") -> dict:
    """Create a new task."""
    with Session(engine) as session:
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            is_completed=False
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "success": True,
            "task": task.model_dump()
        }
```

**Database Schema Additions**:
- Reuse existing `task` table (no changes)
- Add `conversation` table (id, user_id, created_at, updated_at)
- Add `message` table (id, conversation_id, user_id, role, content, tool_calls, created_at)

**Migration Strategy**:
- Use Alembic (already in Phase II) for schema migrations
- New migration file: `add_conversation_tables.py`

---

### 7. Guardrail Topic Detection

**Question**: How to detect if user message is about todo management vs off-topic?

**Decision**: Use lightweight AI-based classification with keyword fallback

**Rationale**:
- AI guardrail agent provides nuanced topic detection
- Handles variations in phrasing ("remind me" = todo creation)
- Fast execution (<500ms) with small model
- Fallback to keyword matching for common patterns

**Topic Classification**:

| Intent | Keywords | Examples |
|--------|----------|----------|
| todo_create | add, create, remind, remember, need to | "Add task to buy milk" |
| todo_list | show, list, what, tasks, pending | "What are my tasks?" |
| todo_complete | done, finished, complete, mark | "Mark task 3 as done" |
| todo_delete | delete, remove, cancel | "Delete task 5" |
| todo_update | change, update, rename, edit | "Change task title" |
| greeting | hi, hello, hey, thanks, help | "Hi there" |
| off_topic | *everything else* | "What's the weather?" |

**Guardrail Agent Instructions**:
```
You are a topic classifier for a todo management chatbot.

Analyze the user's message and determine if it is related to task management.

Task-related topics include:
- Creating, adding, or remembering tasks
- Viewing, listing, or showing tasks
- Completing, finishing, or marking tasks done
- Deleting, removing, or canceling tasks
- Updating, editing, or changing task details
- Asking for help with todo features
- Greetings and pleasantries

Off-topic includes:
- General knowledge questions
- Weather, news, sports
- Coding or programming help
- Creative writing or stories
- Math calculations (unless counting tasks)
- Personal advice

Return true if the message is task-related, false otherwise.
```

---

### 8. Error Handling and Retry Logic

**Question**: How to handle AI API rate limits and errors?

**Decision**: Exponential backoff with 3 retries, then user-friendly error

**Rationale**:
- OpenAI API can return rate limit errors during high traffic
- Automatic retry gives system chance to recover
- Exponential backoff prevents thundering herd
- User sees one of two messages: success or graceful failure

**Implementation Pattern**:
```python
import asyncio
from openai import RateLimitError

async def run_agent_with_retry(agent, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = await Runner.run(agent, messages)
            return result
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                await asyncio.sleep(wait_time)
            else:
                raise
    
    # If all retries exhausted
    raise Exception("Rate limit exceeded after retries")

# In chat endpoint
try:
    result = await run_agent_with_retry(agent, messages)
    return {"response": result.final_output}
except RateLimitError:
    return {
        "error": "High demand. Please wait 30s and try again.",
        "retry_after": 30
    }
except Exception as e:
    logger.error(f"Agent error: {e}")
    return {
        "error": "Unable to process request. Please try again."
    }
```

---

## Technology Stack Summary

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| MCP Server | FastMCP | Latest | Expose task database tools to AI |
| AI Agent | OpenAI Agents SDK Python | 0.2.9+ | Orchestrate todo management with guardrails |
| Chat UI | @openai/chatkit-react | 1.2.0+ | React components for chat interface |
| Backend API | FastAPI | 0.115+ | REST API for chat endpoint (existing) |
| Database | PostgreSQL (Neon) | - | Conversation + message storage (existing) |
| ORM | SQLModel | 0.0.22+ | Database models (existing) |
| Auth | Better Auth + JWT | - | User authentication (existing from Phase II) |
| AI Provider | OpenAI API | - | GPT model for agent and guardrails |

---

## Key Implementation Insights

### 1. Guardrails Before Agent
Running guardrails before the main agent saves API costs and reduces latency when blocking off-topic requests.

### 2. Tool Results in Context
Include tool execution results in conversation history so the agent can reference what was created/modified.

### 3. Conversation Truncation Strategy
Truncate oldest messages first, but keep conversation summary and most recent N messages for continuity.

### 4. Stateless = Scalable
Loading history from DB on each request enables horizontal scaling without sticky sessions.

### 5. User Isolation at DB Level
Filter by user_id in SQL queries, not just application logic, for defense in depth.

---

## Open Questions for Phase 1

1. Should conversation summary be generated for histories >50 messages?
2. Should tool call history be included in message display or hidden from user?
3. What's the optimal token limit for truncation (currently 8000)?
4. Should guardrail agent use same model as main agent or smaller/faster model?
5. How to handle ambiguous task references (e.g., "complete the meeting task" when there are 3)?

---

## Next Steps (Phase 1)

1. Generate data-model.md for Conversation and Message entities
2. Design API contracts for POST /api/{user_id}/chat endpoint
3. Define OpenAPI schema for request/response
4. Create quickstart.md for development setup
5. Update agent context file with new technology stack

---

**Research Status**: ✅ Complete  
**All unknowns resolved**: Yes  
**Ready for Phase 1 design**: Yes
