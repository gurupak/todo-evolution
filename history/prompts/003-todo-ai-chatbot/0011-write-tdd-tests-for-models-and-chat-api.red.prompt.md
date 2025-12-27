---
id: 0011
title: Write TDD Tests for Models and Chat API
stage: red
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-todo-ai-chatbot
branch: 003-todo-ai-chatbot
user: Irfan Ahmed
command: /sp.implement T018 - T022
labels: ["tdd", "testing", "models", "chat-api", "pytest"]
links:
  spec: specs/003-todo-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-3/backend/tests/test_models.py
  - phase-3/backend/tests/test_chat_api.py
  - specs/003-todo-ai-chatbot/tasks.md
tests:
  - test_conversation_model_creation
  - test_conversation_model_requires_user_id
  - test_conversation_auto_sets_timestamps
  - test_message_model_with_user_role
  - test_message_model_with_assistant_role
  - test_message_model_requires_fields
  - test_message_content_cannot_be_empty
  - test_message_auto_sets_created_at
  - test_post_chat_creates_new_conversation
  - test_post_chat_validates_message_length
  - test_post_chat_loads_conversation_history
  - test_post_chat_returns_404_for_invalid_conversation
  - test_post_chat_requires_jwt_token
  - test_post_chat_validates_user_id_matches_jwt
  - test_post_chat_rejects_invalid_jwt
---

## Prompt

/sp.implement T018 - T022

User requested implementation of tasks T018-T022 from tasks.md, which are the TDD test cases for Phase III Todo AI Chatbot infrastructure:

- T018: Test Conversation model creation
- T019: Test Message model creation  
- T020: Test POST /api/{user_id}/chat endpoint
- T021: Test conversation history loading
- T022: Test JWT authentication

This follows the "Red" phase of TDD - writing tests before implementation. The tests validate the database models (Conversation, Message) and the chat API endpoint functionality that will be built in subsequent tasks.

## Response snapshot

Created comprehensive TDD test suite following pytest and pytest-asyncio patterns:

**Test Files Created:**

1. **phase-3/backend/tests/test_models.py** (8 test methods)
   - TestConversationModel class:
     - test_conversation_model_creation: Validates UUID generation, user_id association, timestamp creation
     - test_conversation_model_requires_user_id: Ensures user_id is required field
     - test_conversation_auto_sets_timestamps: Verifies created_at and updated_at auto-generation
   
   - TestMessageModel class:
     - test_message_model_with_user_role: Tests message creation with role="user"
     - test_message_model_with_assistant_role: Tests message with role="assistant" and tool_calls JSON storage
     - test_message_model_requires_fields: Validates required fields (conversation_id, user_id, role, content)
     - test_message_content_cannot_be_empty: Ensures content field is non-empty
     - test_message_auto_sets_created_at: Verifies timestamp auto-generation

2. **phase-3/backend/tests/test_chat_api.py** (9 test methods across 3 classes)
   - TestChatEndpointNewConversation:
     - test_post_chat_creates_new_conversation: Validates POST /api/{user_id}/chat creates new conversation
     - test_post_chat_validates_message_length: Ensures 1-2000 character constraint
   
   - TestChatEndpointConversationHistory:
     - test_post_chat_loads_conversation_history: Tests loading existing conversation by ID
     - test_post_chat_returns_404_for_invalid_conversation: Validates error handling
   
   - TestChatEndpointAuthentication:
     - test_post_chat_requires_jwt_token: Returns 401 if Authorization header missing
     - test_post_chat_validates_user_id_matches_jwt: Returns 403 if user_id doesn't match JWT
     - test_post_chat_rejects_invalid_jwt: Validates token verification

**Fixtures Implemented:**
- test_user_id: Returns string user ID compatible with Better Auth
- test_jwt_token: Generates valid JWT token for authentication tests
- session: Async database session with automatic transaction rollback
- client: AsyncClient for FastAPI testing with HTTPX

**Verification:**
- Python syntax compilation passed for both test files
- Tasks.md updated with T018-T022 marked as completed [x]

## Outcome

- ✅ Impact: Comprehensive TDD test coverage for User Story 1 (AI Chat Interface) foundation
- 🧪 Tests: 17 test methods created (8 model tests + 9 API tests), syntax verified, ready for TDD Red phase
- 📁 Files: 2 new test files created (test_models.py, test_chat_api.py), tasks.md updated
- 🔁 Next prompts: Implement MCP tools foundation (T023-T026), then Guardrails (T027-T032)
- 🧠 Reflection: TDD approach establishes clear acceptance criteria before implementation begins

## Evaluation notes (flywheel)

- Failure modes observed: None - tests compile successfully, fixtures properly structured for async operations
- Graders run and results (PASS/FAIL): Syntax compilation PASS - runtime execution deferred until implementation phase
- Prompt variant (if applicable): Standard /sp.implement workflow
- Next experiment (smallest change to try): Execute test suite to validate Red phase (all tests should fail initially per TDD)
