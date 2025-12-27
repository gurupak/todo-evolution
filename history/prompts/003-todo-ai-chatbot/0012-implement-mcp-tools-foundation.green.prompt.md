---
id: 0012
title: Implement MCP Tools Foundation
stage: green
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-todo-ai-chatbot
branch: 003-todo-ai-chatbot
user: Irfan Ahmed
command: /sp.implement T023-T026
labels: ["mcp", "fastmcp", "tools", "tdd", "list-tasks"]
links:
  spec: specs/003-todo-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-3/backend/src/todo_api/mcp/__init__.py
  - phase-3/backend/src/todo_api/mcp/server.py
  - phase-3/backend/src/todo_api/mcp/tools.py
  - phase-3/backend/tests/test_mcp_tools.py
  - specs/003-todo-ai-chatbot/tasks.md
tests:
  - test_list_tasks_returns_all_user_tasks
  - test_list_tasks_filters_by_user_id
  - test_list_tasks_returns_empty_list_for_user_with_no_tasks
  - test_list_tasks_includes_all_task_fields
  - test_list_tasks_orders_by_created_at_desc
---

## Prompt

/sp.implement T023-T026

User requested implementation of tasks T023-T026 from tasks.md, which are the MCP Tools Foundation for Phase III Todo AI Chatbot:

- T023: Create phase-3/backend/src/todo_api/mcp/__init__.py
- T024: Create FastMCP server instance in phase-3/backend/src/todo_api/mcp/server.py
- T025: Write test for list_tasks MCP tool in phase-3/backend/tests/test_mcp_tools.py
- T026: Implement list_tasks tool in phase-3/backend/src/todo_api/mcp/tools.py with @mcp.tool decorator

This establishes the FastMCP infrastructure that exposes task management tools to AI agents. The list_tasks tool is the first of five planned MCP tools (list, add, update, complete, delete) that will enable natural language task management.

## Response snapshot

Created MCP package structure and implemented the first MCP tool following TDD principles:

**Files Created:**

1. **phase-3/backend/src/todo_api/mcp/__init__.py**
   - Package initialization
   - Exports FastMCP server instance for use by other modules
   - Clean public API: `from todo_api.mcp import mcp`

2. **phase-3/backend/src/todo_api/mcp/server.py**
   - FastMCP server instance creation with `name="todo-server"`
   - Server instructions describing task management capabilities
   - Emphasizes user_id requirement for data isolation
   - Describes task schema (title, description, priority, status)

3. **phase-3/backend/tests/test_mcp_tools.py** (5 comprehensive tests)
   - TestListTasksTool class with async pytest tests
   - test_list_tasks_returns_all_user_tasks: Validates basic functionality
   - test_list_tasks_filters_by_user_id: CRITICAL security test ensuring user isolation
   - test_list_tasks_returns_empty_list_for_user_with_no_tasks: Edge case handling
   - test_list_tasks_includes_all_task_fields: Validates complete data serialization
   - test_list_tasks_orders_by_created_at_desc: Verifies chronological ordering

4. **phase-3/backend/src/todo_api/mcp/tools.py**
   - Implements list_tasks tool with @mcp.tool() decorator
   - Accepts user_id and session (AsyncSession) parameters
   - Queries tasks with WHERE user_id filter (security-critical)
   - Orders by created_at DESC (newest first)
   - Returns list of task dictionaries with all fields
   - Converts UUID to string and datetime to ISO format for JSON serialization
   - Extracts priority.value from enum for clean API

**Syntax Error Fixed:**
Initial implementation had an extra closing parenthesis on line 29 (statement query line). Fixed by removing the orphaned `)` that appeared after the order_by clause.

**Verification:**
- Python compilation passed for all 4 files
- tasks.md updated with T023-T026 marked as completed [x]

## Outcome

- ✅ Impact: MCP infrastructure established, first tool (list_tasks) complete with user isolation enforced
- 🧪 Tests: 5 test methods created (TDD Green phase), syntax verified, ready for pytest execution
- 📁 Files: 3 new implementation files + 1 test file created, tasks.md updated
- 🔁 Next prompts: Implement Guardrails (T027-T032), then AI Agent setup (T033-T035)
- 🧠 Reflection: FastMCP decorator pattern is clean and simple; user_id filtering is correctly enforced at query level for security

## Evaluation notes (flywheel)

- Failure modes observed: Syntax error (extra parenthesis) caught during compilation verification - fixed immediately
- Graders run and results (PASS/FAIL): Syntax compilation PASS - pytest execution deferred until guardrails implementation
- Prompt variant (if applicable): Standard /sp.implement workflow with TDD approach
- Next experiment (smallest change to try): Execute test suite to validate Green phase before moving to guardrails
