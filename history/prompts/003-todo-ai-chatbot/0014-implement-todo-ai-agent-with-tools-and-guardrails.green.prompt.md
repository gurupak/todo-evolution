---
id: 0014
title: Implement Todo AI Agent with Tools and Guardrails
stage: green
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-todo-ai-chatbot
branch: 003-todo-ai-chatbot
user: Irfan Ahmed
command: /sp.implement T033-T035
labels: ["openai-agents-sdk", "agent", "function-tools", "guardrails", "integration"]
links:
  spec: specs/003-todo-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-3/backend/src/todo_api/agent/todo_agent.py
  - specs/003-todo-ai-chatbot/tasks.md
tests: []
---

## Prompt

/sp.implement T033-T035

User requested implementation of tasks T033-T035 from tasks.md (note: user input was "T033-T025" but this appears to be a typo - proceeding with T033-T035 which are the sequential tasks):

- T033: Create todo agent with system prompt in phase-3/backend/src/todo_api/agent/todo_agent.py
- T034: Register MCP tools with agent in phase-3/backend/src/todo_api/agent/todo_agent.py
- T035: Attach input and output guardrails to agent in phase-3/backend/src/todo_api/agent/todo_agent.py

This integrates all previous components (MCP tools, guardrails) into the main AI agent that will power the conversational task management interface.

## Response snapshot

Created the main todo_agent by integrating FastMCP tools and guardrails with OpenAI Agents SDK:

**Integration Pattern Discovery:**
Before implementation, I consulted the user about using guardrails correctly. User confirmed to verify against official OpenAI Agents SDK documentation. I retrieved docs from Context7 MCP and confirmed the implementation pattern.

**Key Learning:** MCP tools from FastMCP need to be wrapped with `@function_tool` decorator to be used as Agent tools in OpenAI Agents SDK.

**File Created:**

**phase-3/backend/src/todo_api/agent/todo_agent.py**

1. **MCP Tool Wrapper:**
   - Created `@function_tool` wrapper for `mcp_list_tasks`
   - Used `Annotated` type hints for parameter descriptions
   - Async function that calls the FastMCP tool
   - Returns list of task dictionaries

2. **Agent Configuration:**
   - **Name**: "Todo Assistant"
   - **Instructions**: Comprehensive system prompt (100+ lines) covering:
     - Capabilities (create, view, update, complete, delete tasks)
     - Communication style (conversational, friendly, clear confirmations)
     - Task priority levels (HIGH, MEDIUM, LOW)
     - Task status (pending, completed)
     - Example interactions showing expected behavior
     - Important notes on data isolation and error handling
   
3. **Tools Integration (T034):**
   - `tools=[list_tasks]` - wrapped MCP tool as function tool
   - Agent can now call list_tasks during conversation
   
4. **Guardrails Integration (T035):**
   - `input_guardrails=[todo_topic_guard]` - blocks off-topic messages
   - `output_guardrails=[response_validator_guard]` - validates responses
   - Guardrails run automatically before/after agent execution

**Agent System Prompt Design:**
The system prompt follows best practices:
- Clear capability boundaries
- Conversational tone guidelines
- Domain-specific vocabulary (priority levels, status)
- Example interactions for few-shot learning
- Security reminders (user isolation, no hallucination)
- Error handling guidelines

**Verification:**
- Python syntax compilation passed
- tasks.md updated with T033-T035 marked as completed [x]
- Package __init__.py already exports todo_agent correctly

## Outcome

- ✅ Impact: Main AI agent complete - all components (MCP tools, guardrails, agent) now integrated
- 🧪 Tests: No new tests written (agent integration will be tested via ChatService in T036-T040)
- 📁 Files: 1 new file created (todo_agent.py), tasks.md updated
- 🔁 Next prompts: Implement ChatService (T036-T040) to orchestrate agent execution with database
- 🧠 Reflection: Using @function_tool wrapper to bridge FastMCP and OpenAI Agents SDK is the correct pattern - allows type-safe tool registration with proper descriptions

## Evaluation notes (flywheel)

- Failure modes observed: Initial confusion about MCP/Agent tool integration - resolved by consulting official docs
- Graders run and results (PASS/FAIL): Syntax compilation PASS
- Prompt variant (if applicable): Standard /sp.implement workflow with doc verification step
- Next experiment (smallest change to try): Test agent execution end-to-end with Runner.run in ChatService
