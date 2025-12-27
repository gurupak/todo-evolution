# Feature Specification: Phase III - Todo AI Chatbot

**Feature Branch**: `003-todo-ai-chatbot`  
**Created**: 2025-12-24  
**Status**: Draft  
**Input**: User description: "Build an AI-powered chatbot interface that lets users manage their todos through natural language conversation using MCP server architecture."

## Clarifications

### Session 2025-12-24

- Q: How should the system handle conversations that exceed the AI model's context window? → A: Truncate oldest messages when total exceeds 8000 tokens, keeping most recent context plus conversation summary
- Q: When the AI service (OpenAI API) returns rate limit errors, how should the system respond to the user? → A: Automatically retry with exponential backoff (3 attempts), then show "High demand. Please wait 30s"
- Q: When a user refers to a task by description and multiple tasks match, how many matches should trigger the clarification question? → A: Ask for clarification when 2-5 tasks match; if 6+ matches, ask user to be more specific
- Q: When a user updates a task in the Phase II web UI while viewing the same task in chat, how should the chat interface reflect the change? → A: No automatic sync; user must refresh conversation or send new message to see updated task data
- Q: When an MCP tool fails (e.g., database error when creating a task), how should the AI agent communicate this to the user? → A: Show specific error like "I couldn't create the task due to a system error. Please try again"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start New Conversation with AI Assistant (Priority: P1)

An authenticated user can initiate a new conversation with the AI chatbot to manage their todos through natural language. The chat interface displays messages with the assistant on the left and user messages on the right.

**Why this priority**: Starting a conversation is the foundational capability that enables all AI-powered task management features. Without this, users cannot interact with the assistant.

**Independent Test**: Can be fully tested by logging in, clicking "New Conversation", typing a message, and receiving an AI response. Delivers value by providing conversational interface to task management.

**Acceptance Scenarios**:

1. **Given** an authenticated user on dashboard, **When** they click "New Conversation", **Then** a new empty chat interface appears
2. **Given** a user in a new conversation, **When** they type a message and press send, **Then** message appears on right side and AI response appears on left
3. **Given** a user sending a message, **When** AI is processing, **Then** loading indicator appears
4. **Given** a user with empty chat, **When** conversation loads, **Then** they see welcome message from AI assistant

---

### User Story 2 - Add Tasks via Natural Language (Priority: P1)

An authenticated user can create new tasks by describing them in natural language to the AI assistant. The assistant understands the intent and creates the task with appropriate title and description.

**Why this priority**: Creating tasks through conversation is the core value proposition of the AI chatbot. This demonstrates the primary benefit over the Phase II UI.

**Independent Test**: Can be fully tested by typing "Add task to buy groceries" and verifying the task appears in both chat confirmation and Phase II task list. Delivers immediate value by enabling hands-free task creation.

**Acceptance Scenarios**:

1. **Given** a user in chat, **When** they say "Add task to buy groceries", **Then** AI creates task and confirms with task details
2. **Given** a user in chat, **When** they say "Remind me to call mom tonight", **Then** AI creates task with title "Call mom tonight" and confirms
3. **Given** a user in chat, **When** they say "Add high priority task to finish report", **Then** AI creates task with high priority and confirms
4. **Given** a user after creating task via chat, **When** they check Phase II web UI, **Then** the new task appears in their task list

---

### User Story 3 - View Tasks via Chat (Priority: P1)

An authenticated user can ask the AI assistant to show their tasks, and the assistant retrieves and displays current task list with status and priority information.

**Why this priority**: Viewing tasks is essential for users to know what needs to be done. This completes the basic CRUD cycle along with task creation.

**Independent Test**: Can be fully tested by creating tasks and asking "Show my tasks" or "What's pending?". Delivers value by providing conversational access to task information.

**Acceptance Scenarios**:

1. **Given** a user with existing tasks, **When** they ask "Show my tasks", **Then** AI lists all tasks with titles and completion status
2. **Given** a user with mixed tasks, **When** they ask "What's pending?", **Then** AI lists only incomplete tasks
3. **Given** a user with no tasks, **When** they ask "Show my tasks", **Then** AI responds "You have no tasks"
4. **Given** a user with tasks, **When** they ask "List my completed tasks", **Then** AI shows only completed tasks

---

### User Story 4 - Complete Tasks via Chat (Priority: P2)

An authenticated user can mark tasks as done by telling the AI assistant using natural language, such as referencing task ID or task content.

**Why this priority**: Completion tracking via chat enhances usability but requires the foundational create/view capabilities to exist first.

**Independent Test**: Can be fully tested by creating a task, then saying "Mark task 3 as done" or "Finished groceries". Delivers value by allowing hands-free task completion.

**Acceptance Scenarios**:

1. **Given** a user with task ID 5, **When** they say "Mark task 5 as done", **Then** AI marks task complete and confirms with task title
2. **Given** a user with pending grocery task, **When** they say "Finished groceries", **Then** AI identifies the task, marks it complete, and confirms
3. **Given** a user completing task via chat, **When** they check Phase II UI, **Then** task shows as completed with timestamp
4. **Given** a user referencing non-existent task, **When** they say "Complete task 999", **Then** AI responds "Task not found"

---

### User Story 5 - Update Tasks via Chat (Priority: P2)

An authenticated user can modify existing tasks by describing the changes in natural language, and the AI assistant updates the appropriate task fields.

**Why this priority**: Editing enhances flexibility but is secondary to core create/view/complete operations.

**Independent Test**: Can be fully tested by creating a task and saying "Change task 1 to call mom tonight". Delivers value by allowing conversational task updates.

**Acceptance Scenarios**:

1. **Given** a user with task ID 3, **When** they say "Change task 3 to call mom tonight", **Then** AI updates task title and confirms
2. **Given** a user with meeting task, **When** they say "Update meeting task description to include agenda", **Then** AI updates description and confirms
3. **Given** a user updating task via chat, **When** they check Phase II UI, **Then** changes are reflected with updated timestamp
4. **Given** a user referencing ambiguous task, **When** AI finds multiple matches, **Then** AI asks "Which task: 1) [title1] or 2) [title2]?"

---

### User Story 6 - Delete Tasks via Chat (Priority: P3)

An authenticated user can remove tasks by asking the AI assistant to delete them, either by ID or description. The assistant confirms before deletion.

**Why this priority**: Deletion is useful for long-term task management but not critical for initial value delivery.

**Independent Test**: Can be fully tested by creating a task and saying "Delete task 2" or "Remove meeting task". Delivers value by allowing conversational task cleanup.

**Acceptance Scenarios**:

1. **Given** a user with task ID 7, **When** they say "Delete task 7", **Then** AI removes task and confirms deletion
2. **Given** a user with meeting task, **When** they say "Remove meeting task", **Then** AI identifies task, deletes it, and confirms
3. **Given** a user deleting task via chat, **When** they check Phase II UI, **Then** task no longer appears in list
4. **Given** a user requesting deletion of non-existent task, **When** they say "Delete task 999", **Then** AI responds "Task not found"

---

### User Story 7 - Resume Previous Conversations (Priority: P3)

An authenticated user can view their conversation history and resume previous chats with full context, allowing them to continue where they left off.

**Why this priority**: Conversation history improves user experience but is not essential for basic functionality.

**Independent Test**: Can be fully tested by creating a conversation, closing it, then reopening to see previous messages. Delivers value by maintaining context across sessions.

**Acceptance Scenarios**:

1. **Given** a user with past conversations, **When** they open conversations list, **Then** they see all conversations with last message preview and timestamp
2. **Given** a user clicking a past conversation, **When** it loads, **Then** full message history appears in chronological order
3. **Given** a user in resumed conversation, **When** they send new message, **Then** AI has context from previous messages
4. **Given** a user with many conversations, **When** viewing list, **Then** conversations are sorted by most recent activity

---

### User Story 8 - Multi-User Conversation Isolation (Priority: P1)

Each authenticated user can only access their own conversations and the AI assistant can only operate on their tasks, ensuring privacy and data security.

**Why this priority**: Data isolation is critical for security and privacy in a multi-user system. This must be enforced from day one.

**Independent Test**: Can be fully tested by creating two user accounts, having each start conversations and create tasks via chat, then verifying users cannot access each other's conversations or tasks. Delivers value by ensuring user privacy.

**Acceptance Scenarios**:

1. **Given** two different users, **When** each creates conversations, **Then** each user sees only their own conversations
2. **Given** user A with tasks, **When** user B asks AI "Show my tasks", **Then** AI returns only user B's tasks, not user A's
3. **Given** a user, **When** they try to access another user's conversation URL directly, **Then** they receive 403 Forbidden error
4. **Given** user A creating task via chat, **When** user B views Phase II UI, **Then** user A's task is not visible to user B

---

### Edge Cases

- What happens when a user asks to complete a task but multiple tasks match the description? → If 2-5 tasks match: AI asks clarifying question listing matching tasks with IDs. If 6+ tasks match: AI asks user to provide more specific description or use task ID
- How does the system handle AI errors or API failures? → For rate limit errors: automatically retry with exponential backoff (3 attempts), then show "High demand. Please wait 30s". For other errors: display "Unable to process request. Please try again" and log error for debugging
- What happens when a user sends message while previous message is still processing? → System queues the message and shows "Please wait for current response to complete"
- How does the system respond when database connection is lost during chat operation? → System shows error message, retries once automatically, then displays "Unable to connect" if retry fails
- What happens when a user references a task ID that doesn't exist? → AI responds with friendly "I couldn't find that task. Could you provide the task ID or description?"
- How does the system handle messages exceeding reasonable length (> 2000 characters)? → System shows validation error "Message too long (max 2000 characters)"
- What happens when AI cannot determine user intent from message? → AI asks clarifying question: "I'm not sure what you'd like me to do. Could you rephrase that?"
- How does the system behave when conversation history becomes very long (> 50 messages)? → System loads most recent 50 messages initially, with "Load more" option for older messages
- What happens when a user's JWT expires during active chat? → System redirects to login with return URL to current conversation

## Requirements *(mandatory)*

### Functional Requirements

**Chat Interface**

- **FR-001**: System MUST provide chat interface with message input field and send button
- **FR-002**: System MUST display user messages aligned to the right side
- **FR-003**: System MUST display assistant messages aligned to the left side
- **FR-004**: System MUST show loading indicator while AI processes message
- **FR-005**: System MUST display messages in chronological order (oldest first)
- **FR-006**: System MUST allow users to start new conversations via "New Conversation" button
- **FR-007**: System MUST scroll to newest message when new message arrives
- **FR-008**: System MUST validate message input as required with max 2000 characters

**Conversation Management**

- **FR-009**: System MUST create new conversation record on first message
- **FR-010**: System MUST return conversation_id with first response
- **FR-011**: System MUST allow users to resume conversations by providing conversation_id
- **FR-012**: System MUST display list of user's past conversations with preview and timestamp
- **FR-013**: System MUST sort conversations by most recent activity (updated_at)
- **FR-014**: System MUST load conversation history from database on resume
- **FR-015**: System MUST support paginated loading of old messages (50 messages per page)

**AI Chat API**

- **FR-016**: System MUST provide single endpoint POST /api/{user_id}/chat
- **FR-017**: System MUST accept conversation_id as optional parameter
- **FR-018**: System MUST accept message as required parameter (1-2000 characters)
- **FR-019**: System MUST return conversation_id in response
- **FR-020**: System MUST return AI assistant response in response
- **FR-021**: System MUST return tool_calls made by AI in response
- **FR-022**: System MUST operate statelessly (load/save conversation each request)
- **FR-023**: System MUST verify user_id in URL matches authenticated user's JWT
- **FR-064**: System MUST truncate conversation history when total exceeds 8000 tokens, keeping most recent messages plus conversation summary

**MCP Server Tools**

- **FR-024**: System MUST provide add_task tool that accepts user_id, title, description
- **FR-025**: System MUST provide list_tasks tool that accepts user_id, status (all/pending/completed)
- **FR-026**: System MUST provide complete_task tool that accepts user_id, task_id
- **FR-027**: System MUST provide delete_task tool that accepts user_id, task_id
- **FR-028**: System MUST provide update_task tool that accepts user_id, task_id, title, description
- **FR-029**: All MCP tools MUST operate on same task table as Phase II
- **FR-030**: All MCP tools MUST enforce user data isolation (user can only access own tasks)
- **FR-031**: All MCP tools MUST return structured responses with success status and data
- **FR-070**: All MCP tools MUST return specific error messages indicating which operation failed and why

**AI Agent Behavior**

- **FR-032**: AI agent MUST understand "add task" intent and call add_task tool
- **FR-033**: AI agent MUST understand "show tasks" intent and call list_tasks tool
- **FR-034**: AI agent MUST understand "complete task" intent and call complete_task tool
- **FR-035**: AI agent MUST understand "delete task" intent and call delete_task tool
- **FR-036**: AI agent MUST understand "update task" intent and call update_task tool
- **FR-037**: AI agent MUST confirm all actions with friendly natural language response
- **FR-038**: AI agent MUST include task details in confirmation messages
- **FR-039**: AI agent MUST handle "task not found" errors gracefully
- **FR-040**: AI agent MUST ask clarifying questions when task reference is ambiguous
- **FR-041**: AI agent MUST respond helpfully when unable to determine user intent
- **FR-067**: AI agent MUST list matching tasks (with IDs) when 2-5 tasks match user's description
- **FR-068**: AI agent MUST ask for more specific description when 6+ tasks match user's description
- **FR-071**: AI agent MUST communicate MCP tool failures with specific operation-focused error messages (e.g., "I couldn't create the task due to a system error. Please try again")

**Message Persistence**

- **FR-042**: System MUST save user message to database before AI processing
- **FR-043**: System MUST save assistant response to database after AI processing
- **FR-044**: System MUST record message role (user/assistant) for each message
- **FR-045**: System MUST record tool_calls JSON for assistant messages
- **FR-046**: System MUST automatically set created_at timestamp on messages
- **FR-047**: System MUST associate messages with conversation_id and user_id

**Authentication & Authorization**

- **FR-048**: System MUST use same Better Auth + JWT as Phase II
- **FR-049**: System MUST require valid JWT token for all chat endpoints
- **FR-050**: System MUST reject requests without valid token with 401 Unauthorized
- **FR-051**: System MUST verify user can only access own conversations
- **FR-052**: System MUST verify user can only access own tasks via MCP tools
- **FR-053**: System MUST redirect users with expired JWT to login with return URL

**Integration with Phase II**

- **FR-054**: Tasks created via chat MUST appear in Phase II web UI task list
- **FR-055**: Tasks created in Phase II MUST be accessible via chat
- **FR-056**: Task updates via chat MUST reflect in Phase II UI without page refresh
- **FR-057**: Task updates in Phase II MUST be visible when listed via chat (user initiates refresh by sending message)
- **FR-058**: System MUST share same Neon PostgreSQL database as Phase II
- **FR-069**: Chat interface MUST NOT automatically sync task changes from Phase II (no real-time updates required)

**Error Handling**

- **FR-059**: System MUST display user-friendly error messages for AI failures
- **FR-060**: System MUST display "Unable to connect" message for network errors after retry
- **FR-061**: System MUST display inline validation errors for message input
- **FR-062**: System MUST automatically retry failed AI requests once before showing error
- **FR-063**: System MUST prevent sending new message while previous is processing
- **FR-065**: System MUST handle AI rate limit errors with exponential backoff retry (3 attempts max)
- **FR-066**: System MUST display "High demand. Please wait 30s" when rate limit retries exhausted

### Key Entities

- **Conversation**: Represents a chat session between user and AI assistant with id, user_id, created_at, updated_at. Conversations contain messages and maintain chat context.

- **Message**: Represents a single message in a conversation with id, conversation_id, user_id, role (user/assistant), content, tool_calls (JSON), created_at. Messages track full dialogue history.

- **Task** (existing from Phase II): Tasks created/modified through MCP tools are the same entities as Phase II, ensuring seamless integration.

- **User** (existing from Phase II): Same user accounts from Phase II authenticate to chat interface.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a task via chat in under 20 seconds (faster than Phase II UI)
- **SC-002**: AI correctly identifies user intent in 90% of task management requests
- **SC-003**: Chat responses appear within 3 seconds of user message send
- **SC-004**: Tasks created via chat appear in Phase II UI within 1 second
- **SC-005**: System maintains conversation context across 10+ message exchanges
- **SC-006**: Zero instances of users accessing other users' conversations or tasks
- **SC-007**: 95% of AI tool calls succeed on first attempt
- **SC-008**: Users can complete workflow (start chat → create task → view task → complete task) in under 2 minutes
- **SC-009**: Chat interface is functional on mobile devices with screen width as low as 320px
- **SC-010**: System handles 100 concurrent chat conversations without degradation

## Assumptions

1. Users have access to OpenAI API key or compatible AI service for agent functionality
2. Users have completed Phase II setup (database, authentication working)
3. MCP server will run on same backend as Phase II API
4. AI responses are generated using OpenAI Agents SDK with function calling
5. Conversation history is truncated at 8000 tokens (oldest messages removed first, with summary retained)
6. Users interact with one conversation at a time (no concurrent message sending)
7. AI model used supports function/tool calling (e.g., GPT-4, GPT-3.5-turbo)
8. Chat interface uses OpenAI ChatKit or similar React component library
9. System supports English language only for AI interactions
10. Task priority can be inferred from natural language (e.g., "urgent" → high priority)
11. Tool call responses are included in conversation history for AI context
12. WebSocket or real-time updates are not required (polling or manual refresh acceptable)
13. Voice input is not supported in Phase III
14. Image/file attachments in chat are not supported in Phase III
15. Conversation search functionality is deferred to later phase

## Out of Scope

The following are explicitly excluded from Phase III:

- Voice or speech input/output
- Image or file attachments in chat messages
- Conversation search or filtering
- Conversation export or archiving
- Conversation sharing with other users
- Multi-language support (non-English)
- Custom AI model selection by user
- Fine-tuned AI models for specific domains
- Real-time typing indicators
- Message reactions or emojis
- Message editing or deletion by user
- Conversation renaming or labeling
- AI personality customization
- Integration with external calendar or reminder systems
- Email or push notifications for chat messages
- Offline chat functionality
- Mobile native chat applications
- Rich text formatting in messages (bold, italic, links)
- Code syntax highlighting in chat
- Chat analytics or usage tracking
- Rate limiting beyond basic API throttling
- Chat moderation or content filtering
- Multi-turn task workflows (e.g., "what else?", "do that again")
