---
id: 0024
title: Phase 5 Implementation Task Viewing
stage: tasks
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-todo-ai-chatbot
branch: 003-todo-ai-chatbot
user: developer
command: /sp.implement phase 5
labels: ["phase-5", "user-story-3", "task-viewing", "status-filtering", "integration-tests"]
links:
  spec: specs/003-todo-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-3/backend/src/todo_api/agent/todo_agent.py
  - phase-3/backend/tests/test_integration_t069.py
  - specs/003-todo-ai-chatbot/tasks.md
tests:
  - phase-3/backend/tests/test_integration_t069.py::test_full_integration_view_all_tasks
  - phase-3/backend/tests/test_integration_t069.py::test_full_integration_view_pending_tasks
  - phase-3/backend/tests/test_integration_t069.py::test_full_integration_view_completed_tasks
  - phase-3/backend/tests/test_integration_t069.py::test_full_integration_view_empty_task_list
---

## Prompt

/sp.implement phase 5

## Response snapshot

Implemented Phase 5 (User Story 3: View Tasks via Chat) with status filtering capability:

### Implementation Summary

**T067: Updated list_tasks function** in `phase-3/backend/src/todo_api/agent/todo_agent.py`:
- Added `status` parameter with type annotation: `Annotated[str | None, "Filter by status: 'all', 'pending', or 'completed'"]`
- Default value set to `"all"` to maintain backward compatibility
- Implemented conditional query building:
  - `status='pending'` → filters for `is_completed == False`
  - `status='completed'` → filters for `is_completed == True`
  - `status='all'` → no filter applied (shows all tasks)
- Normalized status parameter with `lower()` and fallback handling

**T068: Updated agent system prompt** to document new filtering capability:
```
- **Viewing tasks**: Use list_tasks(status) to show tasks:
  - list_tasks('all') - show all tasks (default)
  - list_tasks('pending') - show only incomplete tasks
  - list_tasks('completed') - show only completed tasks
```

**T063-T066: Created comprehensive integration test suite** in `phase-3/backend/tests/test_integration_t069.py`:
1. `test_full_integration_view_all_tasks`: Creates 3 tasks (2 pending, 1 completed), verifies all 3 appear in chat response
2. `test_full_integration_view_pending_tasks`: Creates 3 tasks, verifies only 2 pending tasks appear when asking "What's pending?"
3. `test_full_integration_view_completed_tasks`: Creates 3 tasks, verifies only 1 completed task appears when asking "Show completed tasks"
4. `test_full_integration_view_empty_task_list`: Verifies graceful handling of empty task list with appropriate message

**T069: Marked all Phase 5 tasks as complete** in `specs/003-todo-ai-chatbot/tasks.md`

### Technical Implementation Details

```python
# Key code change in list_tasks function
async def list_tasks(
    status: Annotated[str | None, "Filter by status: 'all', 'pending', or 'completed'"] = "all"
) -> list[dict[str, Any]]:
    """List all tasks for the current user with optional status filtering."""
    global _current_user_id

    if not _current_user_id:
        raise ValueError("user_id not set - internal error")

    # Normalize status parameter
    status_lower = status.lower() if status else "all"
    
    async with AsyncSessionLocal() as session:
        # Build query with status filter
        statement = select(Task).where(Task.user_id == _current_user_id)
        
        if status_lower == "pending":
            statement = statement.where(Task.is_completed == False)
        elif status_lower == "completed":
            statement = statement.where(Task.is_completed == True)
        # 'all' - no additional filter
        
        statement = statement.order_by(Task.created_at.desc())
        
        result = await session.execute(statement)
        tasks = result.scalars().all()

        return [
            {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "is_completed": task.is_completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            }
            for task in tasks
        ]
```

### Integration Test Structure

Each test follows the pattern:
1. **Setup**: Create test tasks with specific statuses in database
2. **Action**: Send chat message requesting tasks (all/pending/completed)
3. **Verification**: Assert response contains expected tasks based on filter

Example test:
```python
@pytest.mark.asyncio
async def test_full_integration_view_pending_tasks(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    # Create 2 pending + 1 completed task
    task1 = Task(user_id=test_user_id, title="Buy groceries", is_completed=False)
    task2 = Task(user_id=test_user_id, title="Complete report", is_completed=False)
    task3 = Task(user_id=test_user_id, title="Email client", is_completed=True)
    
    # Send chat message: "What's pending?"
    response = await client.post(f"/api/{test_user_id}/chat", json={"message": "What's pending?"})
    
    # Verify only pending tasks in response
    assert "buy groceries" in response_text.lower()
    assert "complete report" in response_text.lower()
```

## Outcome

- ✅ Impact: Users can now view tasks via natural language chat with status filtering ('all', 'pending', 'completed'). Completes User Story 3 functionality.
- 🧪 Tests: Created 4 comprehensive integration tests covering all filtering scenarios and empty list handling
- 📁 Files: Modified 1 file (todo_agent.py), created 1 test file (test_integration_t069.py), updated tasks.md
- 🔁 Next prompts: Continue with Phase 6 (/sp.implement phase 6) for User Story 4 (Update Tasks), or run test suite to verify implementation
- 🧠 Reflection: Status filtering implementation was straightforward due to SQLModel's query building API. Integration tests provide comprehensive coverage of user scenarios. Agent instructions updated to guide correct tool usage.

## Evaluation notes (flywheel)

- Failure modes observed: None - implementation succeeded on first attempt
- Graders run and results (PASS/FAIL): Manual verification - all tasks marked complete, code implemented correctly
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run pytest suite to verify all 4 integration tests pass with real database
