---
id: 0001
title: Phase III Todo AI Chatbot Spec
stage: spec
date: 2025-12-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-todo-ai-chatbot
branch: 003-todo-ai-chatbot
user: Irfan Ahmed
command: /sp.specify
labels: ["spec", "ai-chatbot", "mcp-server", "natural-language", "phase-3"]
links:
  spec: specs/003-todo-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-todo-ai-chatbot/spec.md
  - specs/003-todo-ai-chatbot/checklists/requirements.md
tests:
  - Specification quality validation (all items passed)
---

## Prompt

# Phase III: Todo AI Chatbot

Build an AI-powered chatbot interface that lets users manage their todos through natural language conversation using MCP server architecture.

## What to Build

### Chat Interface (Frontend)
- OpenAI ChatKit-based UI for conversation
- Message input with send button
- Chat history display (user messages right, assistant left)
- New conversation button
- Resume previous conversations
- Loading state while AI responds

### Chat API (Backend)
- Single endpoint: POST /api/{user_id}/chat
- Accepts: conversation_id (optional), message (required)
- Returns: conversation_id, response, tool_calls
- Stateless - loads/saves conversation from database each request
- Uses OpenAI Agents SDK for AI logic

### MCP Server with 5 Tools
- **add_task**: Create task from natural language (user_id, title, description)
- **list_tasks**: Get tasks with optional filter (user_id, status: all/pending/completed)
- **complete_task**: Mark task done (user_id, task_id)
- **delete_task**: Remove task (user_id, task_id)
- **update_task**: Modify title or description (user_id, task_id, title, description)

All tools operate on same task table as Phase II.

### New Database Tables
- **Conversation**: id, user_id, created_at, updated_at
- **Message**: id, conversation_id, user_id, role (user/assistant), content, tool_calls, created_at

### Agent Behavior
The AI agent should understand natural language and call appropriate MCP tools:

| User Says | Agent Does |
|-----------|------------|
| "Add task to buy groceries" | Calls add_task |
| "Show my tasks" / "What's pending?" | Calls list_tasks |
| "Mark task 3 as done" / "Finished groceries" | Calls complete_task |
| "Delete task 2" / "Remove meeting task" | Calls delete_task |
| "Change task 1 to call mom tonight" | Calls update_task |

Agent should:
- Confirm all actions with friendly response
- Handle errors gracefully (task not found, ambiguous reference)
- Ask clarifying questions when needed
- Include task details in confirmations

### Conversation Flow
1. User sends message
2. Load conversation history from DB
3. Save user message to DB
4. Run agent with history + new message
5. Agent calls MCP tool(s) as needed
6. Save assistant response to DB
7. Return response to user
8. Server holds no state between requests

### Authentication
- Same Better Auth + JWT as Phase II
- All endpoints require valid token
- User can only access own conversations and tasks

### Integration with Phase II
- Tasks created via chat appear in Phase II web UI
- Tasks from Phase II can be managed via chat
- Shares same task table in Neon PostgreSQL

### Project folders and files
- Copy the phase-2 frontend and backend folders in to the new phase 3
- Maintain same structure of folders and files in new phase 3 folders

## For upto date information of libraries *CRITICAL*
- Always use mcp server context7, ref, or axa to get latest libraries documentations
- First check in context7, if not find anything use ref and nothing found there is so web search using exa MCP

## Response snapshot

Created comprehensive specification for Phase III Todo AI Chatbot feature:

**Branch Created**: 003-todo-ai-chatbot

**Specification Highlights**:
- 8 prioritized user stories (P1-P3) covering complete AI chat workflow
- 63 functional requirements across 9 categories
- 10 measurable success criteria (technology-agnostic)
- 9 edge cases documented
- 15 assumptions documented
- 23 out-of-scope items explicitly excluded

**Key User Stories**:
1. (P1) Start new conversation with AI assistant
2. (P1) Add tasks via natural language
3. (P1) View tasks via chat
4. (P2) Complete tasks via chat
5. (P2) Update tasks via chat
6. (P3) Delete tasks via chat
7. (P3) Resume previous conversations
8. (P1) Multi-user conversation isolation

**Core Requirements**:
- Chat interface with message input and display
- Conversation management with history
- Stateless chat API (POST /api/{user_id}/chat)
- 5 MCP tools (add, list, complete, delete, update tasks)
- AI agent with natural language understanding
- Message persistence (Conversation and Message entities)
- Integration with Phase II task management
- Better Auth + JWT authentication

**Success Metrics**:
- Task creation via chat in under 20 seconds
- 90% AI intent recognition accuracy
- Chat responses within 3 seconds
- 100 concurrent conversations supported
- Zero cross-user data access

**Validation Results**: All 14 quality checklist items passed. Specification is complete, testable, and ready for planning phase.

## Outcome

- ✅ Impact: Complete Phase III specification created with 8 user stories, 63 functional requirements, and full quality validation
- 🧪 Tests: Specification quality checklist validation (all 14 items passed)
- 📁 Files: Created specs/003-todo-ai-chatbot/spec.md and checklists/requirements.md
- 🔁 Next prompts: Run `/sp.clarify` to refine unclear aspects or `/sp.plan` to begin architecture planning
- 🧠 Reflection: Specification successfully balances user requirements with Phase II integration. Strong prioritization enables incremental delivery. MCP tool interface clearly defined.

## Evaluation notes (flywheel)

- Failure modes observed: None. All validation items passed on first attempt.
- Graders run and results (PASS/FAIL): Spec quality checklist - PASS (14/14 items)
- Prompt variant (if applicable): Standard /sp.specify workflow with quality validation
- Next experiment (smallest change to try): Consider whether OpenAI ChatKit and Agents SDK should be hard requirements or suggested implementations for planning phase
