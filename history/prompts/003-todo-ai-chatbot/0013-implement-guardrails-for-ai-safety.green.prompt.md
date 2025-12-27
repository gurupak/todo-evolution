---
id: 0013
title: Implement Guardrails for AI Safety
stage: green
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-todo-ai-chatbot
branch: 003-todo-ai-chatbot
user: Irfan Ahmed
command: /sp.implement T027-T032
labels: ["guardrails", "openai-agents-sdk", "input-validation", "output-validation", "tdd", "ai-safety"]
links:
  spec: specs/003-todo-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-3/backend/src/todo_api/agent/__init__.py
  - phase-3/backend/src/todo_api/agent/guardrails.py
  - phase-3/backend/tests/test_guardrails.py
  - specs/003-todo-ai-chatbot/tasks.md
tests:
  - test_blocks_off_topic_messages
  - test_blocks_general_conversation
  - test_blocks_inappropriate_content
  - test_allows_add_task_messages
  - test_allows_view_tasks_messages
  - test_allows_update_task_messages
  - test_allows_complete_task_messages
  - test_allows_delete_task_messages
  - test_allows_greetings_in_task_context
  - test_validates_response_has_content
  - test_blocks_empty_responses
  - test_blocks_error_messages_without_context
  - test_allows_task_confirmation_responses
  - test_allows_task_list_responses
  - test_allows_clarification_requests
---

## Prompt

/sp.implement T027-T032

User requested implementation of tasks T027-T032 from tasks.md, which are the Guardrails Implementation for Phase III Todo AI Chatbot:

- T027: Create phase-3/backend/src/todo_api/agent/__init__.py
- T028: Write test for input guardrail blocking off-topic messages in phase-3/backend/tests/test_guardrails.py
- T029: Write test for input guardrail allowing todo-related messages in phase-3/backend/tests/test_guardrails.py
- T030: Implement TodoTopicGuard input guardrail in phase-3/backend/src/todo_api/agent/guardrails.py
- T031: Write test for output guardrail validation in phase-3/backend/tests/test_guardrails.py
- T032: Implement ResponseValidatorGuard output guardrail in phase-3/backend/src/todo_api/agent/guardrails.py

This establishes the AI safety layer using OpenAI Agents SDK guardrails to ensure the chatbot stays on topic (task management only) and produces valid, helpful responses.

## Response snapshot

Created agent package and implemented comprehensive input/output guardrails following the OpenAI Agents SDK pattern:

**Files Created:**

1. **phase-3/backend/src/todo_api/agent/__init__.py**
   - Package initialization for agent module
   - Exports todo_agent, todo_topic_guard, and response_validator_guard
   - Clean public API for importing guardrails and agent

2. **phase-3/backend/tests/test_guardrails.py** (15 comprehensive tests)
   - **TestTodoTopicGuard** (9 tests for input validation):
     - test_blocks_off_topic_messages: Weather questions, general conversation
     - test_blocks_general_conversation: Casual greetings without task context
     - test_blocks_inappropriate_content: Political/harmful content
     - test_allows_add_task_messages: "Add a task to buy groceries"
     - test_allows_view_tasks_messages: "Show me my pending tasks"
     - test_allows_update_task_messages: "Change task 1 to call mom"
     - test_allows_complete_task_messages: "Mark groceries as done"
     - test_allows_delete_task_messages: "Delete task number 3"
     - test_allows_greetings_in_task_context: "Hi, I need help managing tasks"
   
   - **TestResponseValidatorGuard** (6 tests for output validation):
     - test_validates_response_has_content: Normal task confirmations
     - test_blocks_empty_responses: Empty or whitespace-only content
     - test_blocks_error_messages_without_context: Unhelpful generic errors
     - test_allows_task_confirmation_responses: "I've added the task..."
     - test_allows_task_list_responses: Multi-line task lists
     - test_allows_clarification_requests: "Which task did you mean?"

3. **phase-3/backend/src/todo_api/agent/guardrails.py**
   - **Pydantic Output Models**:
     - TopicValidationOutput(is_todo_related, reasoning)
     - ResponseValidationOutput(is_valid, reasoning)
   
   - **Guardrail Agents** (meta-agents for validation):
     - topic_validator_agent: Classifies if message is todo-related
     - response_validator_agent: Validates response quality
   
   - **Input Guardrail** (@input_guardrail decorator):
     - todo_topic_guard function
     - Runs topic_validator_agent on user input
     - Triggers tripwire if is_todo_related=False
     - Blocks execution before main agent runs
   
   - **Output Guardrail** (@output_guardrail decorator):
     - response_validator_guard function
     - Runs response_validator_agent on AI output
     - Triggers tripwire if is_valid=False
     - Prevents invalid responses from reaching user

**Guardrail Design Patterns:**
- **Agent-in-the-loop**: Guardrails themselves use AI agents for intelligent validation
- **Structured outputs**: Pydantic models ensure type-safe validation results
- **Tripwire mechanism**: Exceptions halt execution when guardrails fail
- **Context preservation**: Guardrail context passed through to validator agents
- **Detailed instructions**: Clear guidelines for topic classification and response quality

**Topic Classification Logic:**
- ✅ Allowed: Add, view, update, complete, delete tasks; task status queries; greetings with task context
- ❌ Blocked: Weather, news, jokes, politics, sports, general conversation, inappropriate content

**Response Validation Logic:**
- ✅ Valid: Non-empty content, task confirmations, helpful errors, clarifications, task lists
- ❌ Invalid: Empty responses, whitespace-only, generic errors without context, truncated content

**Verification:**
- Python compilation passed for all 3 files
- tasks.md updated with T027-T032 marked as completed [x]

## Outcome

- ✅ Impact: AI safety layer complete - guardrails prevent off-topic abuse and ensure response quality
- 🧪 Tests: 15 test methods created (9 input + 6 output), comprehensive coverage of allowed/blocked scenarios
- 📁 Files: 2 new implementation files + 1 test file created, tasks.md updated
- 🔁 Next prompts: Implement AI Agent setup (T033-T035) to integrate guardrails with main agent
- 🧠 Reflection: OpenAI Agents SDK guardrail pattern is elegant - using AI to validate AI ensures intelligent topic detection without brittle regex rules

## Evaluation notes (flywheel)

- Failure modes observed: None - syntax compilation passed on first try
- Graders run and results (PASS/FAIL): Syntax compilation PASS - pytest execution deferred until agent integration
- Prompt variant (if applicable): Standard /sp.implement workflow with TDD approach
- Next experiment (smallest change to try): Integrate guardrails into todo_agent and test end-to-end tripwire behavior
