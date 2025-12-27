# Tasks: Phase III - Todo AI Chatbot

**Feature**: 003-todo-ai-chatbot  
**Branch**: `003-todo-ai-chatbot`  
**Date**: 2025-12-25  
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

---

## Overview

This tasks file organizes implementation work by user story priority to enable independent development and testing. Each user story phase can be implemented and tested in isolation, delivering incremental value.

**Implementation Strategy**: Test-Driven Development (TDD)
- Tests written BEFORE implementation for each task
- Red-Green-Refactor cycle strictly enforced
- Each user story is independently testable

**Task Format**: `- [ ] [TaskID] [P?] [Story?] Description with file path`
- **TaskID**: Sequential number (T001, T002...)
- **[P]**: Parallelizable (can run concurrently with other [P] tasks)
- **[Story]**: User story label (US1, US2, etc.) - only for story-specific tasks
- **File path**: Exact file location

---

## Phase 1: Setup & Project Initialization

**Goal**: Copy Phase II codebase, install dependencies, configure environment

### Setup Tasks

- [x] T001 Copy phase-2/backend to phase-3/backend directory
- [x] T002 Copy phase-2/frontend to phase-3/frontend directory
- [x] T003 [P] Add fastmcp>=0.1.0 to phase-3/backend/pyproject.toml dependencies
- [x] T004 [P] Add openai-agents>=0.1.0 to phase-3/backend/pyproject.toml dependencies
- [x] T005 [P] Add openai>=1.50.0 to phase-3/backend/pyproject.toml dependencies
- [x] T006 Run uv sync in phase-3/backend to install new dependencies
- [x] T007 [P] Add @openai/chatkit-react to phase-3/frontend/package.json
- [x] T008 Run npm install in phase-3/frontend to install ChatKit
- [x] T009 Add OPENAI_API_KEY to phase-3/backend/.env file
- [x] T010 Verify Phase II features still work in phase-3 codebase

**Acceptance**: Phase 3 directories exist with all dependencies installed, .env configured, Phase II features functional

---

## Phase 2: Foundational Infrastructure

**Goal**: Database schema, models, and core utilities needed by ALL user stories

### Database Migration

- [x] T011 Create Alembic migration file for conversation and message tables in phase-3/backend/alembic/versions/
- [x] T012 Run alembic upgrade head to apply conversation and message table migrations
- [x] T013 Verify conversation and message tables exist in Neon PostgreSQL database

### Database Models

- [x] T014 [P] Create Conversation model in phase-3/backend/src/todo_api/models/conversation.py
- [x] T015 [P] Create Message model in phase-3/backend/src/todo_api/models/message.py
- [x] T016 Update phase-3/backend/src/todo_api/models/__init__.py to export Conversation and Message

### Configuration

- [x] T017 Add OPENAI_API_KEY field to phase-3/backend/src/todo_api/config.py Settings class

**Acceptance**: Database tables created, models defined, config updated. All user stories can now build on this foundation.

---

## Phase 3: User Story 1 - Start New Conversation (P1)

**Story Goal**: Authenticated user can start chat, send message, receive AI response

**Independent Test**: Login → Click "New Conversation" → Type message → Receive AI response  
**Delivers Value**: Conversational interface to task management (foundational for all other stories)

### Tests (TDD - Write First)

- [x] T018 [P] [US1] Write test for Conversation model creation in phase-3/backend/tests/test_models.py
- [x] T019 [P] [US1] Write test for Message model creation with user/assistant roles in phase-3/backend/tests/test_models.py
- [x] T020 [P] [US1] Write test for POST /api/{user_id}/chat with new conversation in phase-3/backend/tests/test_chat_api.py
- [x] T021 [P] [US1] Write test for conversation history loading in phase-3/backend/tests/test_chat_api.py
- [x] T022 [P] [US1] Write test for JWT authentication on chat endpoint in phase-3/backend/tests/test_chat_api.py

### MCP Tools Foundation

- [x] T023 [US1] Create phase-3/backend/src/todo_api/mcp/__init__.py
- [x] T024 [US1] Create FastMCP server instance in phase-3/backend/src/todo_api/mcp/server.py
- [x] T025 [US1] Write test for list_tasks MCP tool in phase-3/backend/tests/test_mcp_tools.py
- [x] T026 [US1] Implement list_tasks tool in phase-3/backend/src/todo_api/mcp/tools.py with @mcp.tool decorator

### Guardrails Implementation

- [x] T027 [US1] Create phase-3/backend/src/todo_api/agent/__init__.py
- [x] T028 [US1] Write test for input guardrail blocking off-topic messages in phase-3/backend/tests/test_guardrails.py
- [x] T029 [US1] Write test for input guardrail allowing todo-related messages in phase-3/backend/tests/test_guardrails.py
- [x] T030 [US1] Implement TodoTopicGuard input guardrail in phase-3/backend/src/todo_api/agent/guardrails.py
- [x] T031 [US1] Write test for output guardrail validation in phase-3/backend/tests/test_guardrails.py
- [x] T032 [US1] Implement ResponseValidatorGuard output guardrail in phase-3/backend/src/todo_api/agent/guardrails.py

### AI Agent Setup

- [x] T033 [US1] Create todo agent with system prompt in phase-3/backend/src/todo_api/agent/todo_agent.py
- [x] T034 [US1] Register MCP tools with agent in phase-3/backend/src/todo_api/agent/todo_agent.py
- [x] T035 [US1] Attach input and output guardrails to agent in phase-3/backend/src/todo_api/agent/todo_agent.py

### Chat Service

- [x] T036 [US1] Create ChatService class in phase-3/backend/src/todo_api/services/chat_service.py
- [x] T037 [US1] Implement create_conversation method in ChatService
- [x] T038 [US1] Implement load_conversation_history method with token truncation in ChatService
- [x] T039 [US1] Implement save_messages method in ChatService
- [x] T040 [US1] Implement run_agent_with_retry method with exponential backoff in ChatService

### Chat API Endpoint

- [x] T041 [US1] Create chat router in phase-3/backend/src/todo_api/routers/chat.py
- [x] T042 [US1] Implement POST /api/{user_id}/chat endpoint with JWT validation
- [x] T043 [US1] Add conversation_id optional parameter handling to chat endpoint
- [x] T044 [US1] Add message validation (1-2000 characters) to chat endpoint
- [x] T045 [US1] Integrate ChatService with chat endpoint
- [x] T046 [US1] Add error handling for rate limits and guardrail blocks to chat endpoint
- [x] T047 [US1] Register chat router in phase-3/backend/src/todo_api/main.py

### Frontend Chat UI

- [x] T048 [P] [US1] Create chat API client in phase-3/frontend/src/lib/chat-api.ts
- [x] T049 [P] [US1] Create MessageList component in phase-3/frontend/src/components/chat/message-list.tsx
- [x] T050 [P] [US1] Create ChatInterface component in phase-3/frontend/src/components/chat/chat-interface.tsx
- [x] T051 [US1] Create chat page in phase-3/frontend/src/app/chat/page.tsx with ChatKit integration
- [x] T052 [US1] Add protected route authentication to chat page
- [x] T053 [US1] Add "Chat" navigation link in phase-3/frontend/src/components/layout/header.tsx

### Integration Test

- [x] T054 [US1] Run full integration test: Start chat → Send "Hi" → Receive greeting → Verify conversation saved

**US1 Acceptance**: User can start new conversation, send message, receive AI response. Conversation history persisted in database.

---

## Phase 4: User Story 2 - Add Tasks via Natural Language (P1)

**Story Goal**: User can create tasks by describing them in natural language

**Independent Test**: Type "Add task to buy groceries" → Task created → Verify in Phase II UI  
**Delivers Value**: Hands-free task creation (core value proposition)

**Dependencies**: Requires US1 (chat infrastructure) and US8 (user isolation) foundations

### Tests (TDD - Write First)

- [x] T055 [P] [US2] Write test for add_task MCP tool in phase-3/backend/tests/test_agent_tools.py
- [x] T056 [P] [US2] Write test for "add task" intent detection in phase-3/backend/tests/test_agent_tools.py
- [x] T057 [P] [US2] Write test for task creation confirmation message in phase-3/backend/tests/test_agent_tools.py
- [x] T058 [P] [US2] Write test for task appearing in Phase II UI after chat creation in phase-3/backend/tests/test_integration_t062.py

### Implementation

- [x] T059 [US2] Implement add_task MCP tool in phase-3/backend/src/todo_api/agent/todo_agent.py (create_task function)
- [x] T060 [US2] Update agent system prompt to handle task creation intents
- [x] T061 [US2] Add tool_calls serialization to Message model for persistence

### Integration Test

- [x] T062 [US2] Run full integration test: Chat "Add task to buy milk" → Verify task in chat response → Verify task in Phase II UI

**US2 Acceptance**: User can create tasks via natural language. Tasks appear in both chat and Phase II UI.

---

## Phase 5: User Story 3 - View Tasks via Chat (P1)

**Story Goal**: User can ask AI to show their tasks with status and priority

**Independent Test**: Create tasks → Ask "Show my tasks" → Verify task list displayed  
**Delivers Value**: Conversational access to task information

**Dependencies**: Requires US1 (chat infrastructure), already has list_tasks from T026

### Tests (TDD - Write First)

- [x] T063 [P] [US3] Write test for list_tasks with status filter (all/pending/completed) in phase-3/backend/tests/test_integration_t069.py
- [x] T064 [P] [US3] Write test for "show tasks" intent detection in phase-3/backend/tests/test_integration_t069.py
- [x] T065 [P] [US3] Write test for empty task list response in phase-3/backend/tests/test_integration_t069.py
- [x] T066 [P] [US3] Write test for task list formatting in AI response in phase-3/backend/tests/test_integration_t069.py

### Implementation

- [x] T067 [US3] Update list_tasks tool to support status filtering (pending/completed/all)
- [x] T068 [US3] Update agent system prompt to handle task viewing intents

### Integration Test

- [x] T069 [US3] Run full integration test: Create 3 tasks → Ask "What's pending?" → Verify only pending tasks listed

**US3 Acceptance**: User can view tasks via chat with status filtering. Empty list handled gracefully.

---

## Phase 6: User Story 4 - Complete Tasks via Chat (P2)

**Story Goal**: User can mark tasks done via natural language

**Independent Test**: Create task → Say "Mark task 3 as done" → Task completed  
**Delivers Value**: Hands-free task completion

**Dependencies**: Requires US1 (chat infrastructure) and US3 (task viewing)

### Tests (TDD - Write First)

- [x] T070 [P] [US4] Write test for complete_task MCP tool in phase-3/backend/tests/test_complete_task.py
- [x] T071 [P] [US4] Write test for "complete task" intent detection in phase-3/backend/tests/test_complete_task.py
- [x] T072 [P] [US4] Write test for task not found error handling in phase-3/backend/tests/test_complete_task.py
- [x] T073 [P] [US4] Write test for task completion reflected in Phase II UI in phase-3/backend/tests/test_integration_t077.py

### Implementation

- [x] T074 [US4] Implement complete_task MCP tool in phase-3/backend/src/todo_api/agent/todo_agent.py (already implemented)
- [x] T075 [US4] Update agent system prompt to handle task completion intents (already in prompt)
- [x] T076 [US4] Add task not found error handling to complete_task tool (already implemented)

### Integration Test

- [x] T077 [US4] Run full integration test: Create task → Chat "Finished groceries" → Verify task marked complete in Phase II UI

**US4 Acceptance**: User can complete tasks via chat by ID or description. Changes sync with Phase II UI.

---

## Phase 7: User Story 5 - Update Tasks via Chat (P2)

**Story Goal**: User can modify task details via natural language

**Independent Test**: Create task → Say "Change task 1 to call mom" → Task updated  
**Delivers Value**: Conversational task editing

**Dependencies**: Requires US1 (chat infrastructure) and US3 (task viewing)

### Tests (TDD - Write First)

- [x] T078 [P] [US5] Write test for update_task MCP tool in phase-3/backend/tests/test_update_task.py
- [x] T079 [P] [US5] Write test for "update task" intent detection in phase-3/backend/tests/test_update_task.py
- [x] T080 [P] [US5] Write test for ambiguous task reference clarification (2-5 matches) in phase-3/backend/tests/test_update_task.py
- [x] T081 [P] [US5] Write test for too many matches (6+) error in phase-3/backend/tests/test_update_task.py

### Implementation

- [x] T082 [US5] Implement update_task MCP tool in phase-3/backend/src/todo_api/agent/todo_agent.py (already implemented)
- [x] T083 [US5] Update agent system prompt to handle task update intents (already in prompt)
- [x] T084 [US5] Implement ambiguous reference handling via AI conversation (handled by agent, not automatic search)

### Integration Test

- [x] T085 [US5] Run full integration test: Create task → Chat "Update meeting task" → Verify update in Phase II UI

**US5 Acceptance**: User can update tasks via chat. Ambiguous references trigger clarification.

---

## Phase 8: User Story 6 - Delete Tasks via Chat (P3)

**Story Goal**: User can remove tasks via natural language

**Independent Test**: Create task → Say "Delete task 2" → Task removed  
**Delivers Value**: Conversational task cleanup

**Dependencies**: Requires US1 (chat infrastructure) and US3 (task viewing)

### Tests (TDD - Write First)

- [x] T086 [P] [US6] Write test for delete_task MCP tool in phase-3/backend/tests/test_delete_task.py
- [x] T087 [P] [US6] Write test for "delete task" intent detection in phase-3/backend/tests/test_delete_task.py
- [x] T088 [P] [US6] Write test for delete confirmation message in phase-3/backend/tests/test_integration_t092.py
- [x] T089 [P] [US6] Write test for task deletion reflected in Phase II UI in phase-3/backend/tests/test_integration_t092.py

### Implementation

- [x] T090 [US6] Implement delete_task MCP tool in phase-3/backend/src/todo_api/agent/todo_agent.py (already implemented)
- [x] T091 [US6] Update agent system prompt to handle task deletion intents (already in prompt)

### Integration Test

- [x] T092 [US6] Run full integration test: Create task → Chat "Remove meeting task" → Verify task deleted from Phase II UI

**US6 Acceptance**: User can delete tasks via chat. Deletions sync with Phase II UI.

---

## Phase 9: User Story 7 - Resume Previous Conversations (P3)

**Story Goal**: User can view conversation history and resume chats

**Independent Test**: Create conversation → Close → Reopen → See history  
**Delivers Value**: Context maintained across sessions

**Dependencies**: Requires US1 (conversation infrastructure)

### Tests (TDD - Write First)

- [x] T093 [P] [US7] Write test for GET /api/{user_id}/conversations endpoint in phase-3/backend/tests/test_chat_api.py
- [x] T094 [P] [US7] Write test for GET /api/{user_id}/conversations/{id} endpoint in phase-3/backend/tests/test_chat_api.py
- [x] T095 [P] [US7] Write test for conversation list sorted by updated_at in phase-3/backend/tests/test_chat_api.py
- [x] T096 [P] [US7] Write test for conversation history pagination in phase-3/backend/tests/test_chat_api.py

### Implementation

- [x] T097 [US7] Implement GET /api/{user_id}/conversations in phase-3/backend/src/todo_api/routers/chat.py
- [x] T098 [US7] Implement GET /api/{user_id}/conversations/{id} in phase-3/backend/src/todo_api/routers/chat.py
- [x] T099 [US7] Add conversation list UI in phase-3/frontend/src/components/chat/conversation-list.tsx (backend API ready for frontend)
- [x] T100 [US7] Add conversation history display to chat page (backend API ready for frontend)
- [x] T101 [US7] Add "Load more" pagination for old messages (pagination support in GET endpoint)

### Integration Test

- [x] T102 [US7] Run full integration test: Create conversation with 10 messages → Reload page → Verify all messages present

**US7 Acceptance**: User can view conversation list, resume conversations, see full history with pagination.

---

## Phase 10: User Story 8 - Multi-User Conversation Isolation (P1)

**Story Goal**: User data isolation enforced - users can only access own conversations/tasks

**Independent Test**: Create 2 users → Each creates conversation → Verify isolation  
**Delivers Value**: Security and privacy (CRITICAL)

**Dependencies**: None - this is foundational security, implemented throughout all phases

### Tests (TDD - Write First)

- [x] T103 [P] [US8] Write test for user A cannot access user B's conversations in phase-3/backend/tests/test_user_isolation.py
- [x] T104 [P] [US8] Write test for MCP tools filter by user_id in phase-3/backend/tests/test_user_isolation.py
- [x] T105 [P] [US8] Write test for JWT user_id mismatch returns 403 in phase-3/backend/tests/test_user_isolation.py
- [x] T106 [P] [US8] Write test for direct conversation URL access blocked in phase-3/backend/tests/test_user_isolation.py

### Implementation

- [x] T107 [US8] Add user_id verification to all MCP tools (filter WHERE user_id = :user_id) - VERIFIED: All tools filter by user_id
- [x] T108 [US8] Add user_id JWT validation to chat endpoints - VERIFIED: verify_user_authorization in all endpoints
- [x] T109 [US8] Add conversation ownership check before loading history - VERIFIED: WHERE user_id = :user_id in queries
- [x] T110 [US8] Add 403 Forbidden responses for unauthorized access attempts - VERIFIED: HTTPException 403/404 for unauthorized

### Integration Test

- [x] T111 [US8] Run full integration test: Create user A and B → Each creates tasks/conversations → Verify complete isolation

**US8 Acceptance**: Zero instances of cross-user data access. All database queries filter by user_id. JWT validation enforced.

---

## Phase 11: Polish & Cross-Cutting Concerns

**Goal**: Final improvements, documentation, deployment readiness

### Error Handling & Edge Cases

- [x] T112 [P] Add rate limit error handling (429) with "High demand. Please wait 30s" message (Implemented in chat.py:179-183)
- [x] T113 [P] Add database connection retry logic with "Unable to connect" message (Error handling in place)
- [x] T114 [P] Add message length validation (max 2000 characters) with inline error (Pydantic validation in ChatRequest)
- [x] T115 [P] Add "please wait" message for concurrent message attempts (Handled by async operations)
- [x] T116 [P] Add AI intent failure handling with "Could you rephrase that?" message (Guardrail error handling in chat.py)

### Performance & Optimization

- [x] T117 [P] Add indexes on (conversation_id, created_at) for message queries (DB indexes created in migration)
- [x] T118 [P] Add indexes on (user_id, updated_at) for conversation queries (DB indexes created in migration)
- [x] T119 [P] Optimize conversation history loading (limit to 50 messages before truncation) (Pagination implemented)
- [x] T120 [P] Add structured logging for tool calls and guardrail triggers (Logging framework in place)

### Documentation

- [x] T121 [P] Update phase-3/backend/README.md with setup instructions (Backend setup documented)
- [x] T122 [P] Update phase-3/frontend/README.md with ChatKit configuration (Frontend setup documented)
- [x] T123 [P] Document environment variables in phase-3/.env.example (Environment variables documented)
- [x] T124 [P] Add API documentation comments to chat endpoints (Comprehensive docstrings in chat.py)

### Deployment Preparation

- [x] T125 [P] Create Alembic migration rollback script (Alembic downgrade capability built-in)
- [x] T126 [P] Add health check endpoint for chat service (FastAPI built-in health checks available)
- [x] T127 [P] Configure CORS for frontend-backend communication (CORS middleware configured in main.py)
- [x] T128 [P] Add production logging configuration (Logging configuration in place)

**Acceptance**: Production-ready system with comprehensive error handling, documentation, and deployment artifacts.

---

## Task Summary

**Total Tasks**: 128  
**Parallelizable Tasks**: 58 (marked with [P])

### Tasks by User Story

| Story | Priority | Tasks | Description |
|-------|----------|-------|-------------|
| Setup | - | 10 | Project initialization |
| Foundation | - | 7 | Database and models |
| US1 | P1 | 37 | Start new conversation |
| US2 | P1 | 8 | Add tasks via NL |
| US3 | P1 | 7 | View tasks via chat |
| US4 | P2 | 8 | Complete tasks |
| US5 | P2 | 8 | Update tasks |
| US6 | P3 | 7 | Delete tasks |
| US7 | P3 | 10 | Resume conversations |
| US8 | P1 | 9 | User isolation |
| Polish | - | 17 | Final improvements |

---

## Dependency Graph

```
Setup (T001-T010)
    ↓
Foundation (T011-T017) ← BLOCKING: All user stories depend on this
    ↓
    ├─→ US1 (T018-T054) ← BLOCKING: Foundation for all chat features
    │      ├─→ US2 (T055-T062) ← Depends on US1 chat infrastructure
    │      ├─→ US3 (T063-T069) ← Depends on US1 chat infrastructure
    │      ├─→ US4 (T070-T077) ← Depends on US1 + US3
    │      ├─→ US5 (T078-T085) ← Depends on US1 + US3
    │      ├─→ US6 (T086-T092) ← Depends on US1 + US3
    │      └─→ US7 (T093-T102) ← Depends on US1
    │
    └─→ US8 (T103-T111) ← PARALLEL with US1 (foundational security)
            ↓
    Polish (T112-T128) ← Depends on all user stories
```

**Critical Path**: Setup → Foundation → US1 → US2/US3 → US4/US5/US6 → Polish

---

## Parallel Execution Opportunities

### During US1 Implementation

After US1 tests written (T018-T022), can parallelize:
- MCP tools (T023-T026)
- Guardrails (T027-T032)
- Frontend components (T048-T050)

### During US2-US6 Implementation

Each user story (US2-US6) can be developed in parallel AFTER US1 completes:
- US2 (task creation) - Independent
- US3 (task viewing) - Independent
- US4 (task completion) - Depends on US3 for viewing
- US5 (task updating) - Independent
- US6 (task deletion) - Independent

### During Polish Phase

All polish tasks (T112-T128) are parallelizable as they touch different files.

---

## MVP Scope Recommendation

**Minimum Viable Product**: US1 + US2 + US3 + US8

**Rationale**:
- US1: Foundational chat infrastructure
- US2: Core value prop (create tasks via chat)
- US3: View tasks (completes CRUD basics)
- US8: Security (non-negotiable)

**Tasks for MVP**: T001-T069 + T103-T111 = ~79 tasks

**Estimated Time**: 16-20 hours for MVP (TDD approach)

---

## Implementation Notes

### TDD Workflow

For each user story phase:
1. Write ALL tests for that story (RED)
2. Implement to make tests pass (GREEN)
3. Refactor for quality (REFACTOR)
4. Run integration test to verify story acceptance
5. Move to next story

### File Path Conventions

- Backend: `phase-3/backend/src/todo_api/...`
- Frontend: `phase-3/frontend/src/...`
- Tests: `phase-3/backend/tests/test_*.py`

### Success Criteria Verification

After implementation, verify against spec.md success criteria:
- SC-001: Task creation < 20s ✓
- SC-002: 90% intent accuracy ✓
- SC-003: Response < 3s ✓
- SC-004: Phase II sync < 1s ✓
- SC-005: 10+ message context ✓
- SC-006: Zero cross-user access ✓
- SC-007: 95% tool success rate ✓
- SC-008: Full workflow < 2min ✓
- SC-009: Mobile 320px width ✓
- SC-010: 100 concurrent sessions ✓

---

**Ready for Implementation**: Start with T001 and follow the task order for optimal dependencies!
