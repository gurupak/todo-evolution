# Implementation Plan: Phase III - Todo AI Chatbot

**Branch**: `003-todo-ai-chatbot` | **Date**: 2025-12-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-todo-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build an AI-powered chatbot interface that lets users manage todos through natural language conversation using MCP server architecture. The system will integrate FastMCP for exposing database tools, OpenAI Agents SDK for intelligent task management with guardrails, and OpenAI ChatKit for the frontend chat UI. The implementation extends Phase II by adding conversational AI capabilities while maintaining the existing task management foundation.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript/Next.js 15 (frontend)  
**Primary Dependencies**: FastAPI 0.115+, FastMCP (latest), OpenAI Agents SDK Python 0.2.9+, OpenAI ChatKit React 1.2.0+, SQLModel 0.0.22+, Better Auth (existing)  
**Storage**: Neon PostgreSQL (existing from Phase II) with new tables: conversation, message  
**Testing**: pytest 8.0+ with pytest-asyncio for backend, Jest/React Testing Library for frontend  
**Target Platform**: Web application (Linux/Windows server backend, modern browsers frontend)  
**Project Type**: Web application with backend API and frontend UI (extending Phase II)  
**Performance Goals**: <3s AI response time, <1s database operations, support 100 concurrent chat sessions  
**Constraints**: Stateless chat API design, conversation history truncation at 8000 tokens, guardrails must block off-topic requests, no real-time sync between chat and Phase II UI  
**Scale/Scope**: Multi-user system with conversation isolation, 5 MCP tools, 2 guardrails (input/output), single chat endpoint, ~15-20 new files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Note**: Constitution file is currently a template. Applying standard best practices for this feature.

### Design Principles Compliance

✅ **Test-First Development**: All MCP tools, guardrails, and chat endpoints will have unit tests written before implementation  
✅ **Simplicity**: Using established frameworks (FastMCP, OpenAI Agents SDK) rather than building custom solutions  
✅ **Security**: User data isolation enforced at database level, JWT authentication reused from Phase II, guardrails prevent off-topic abuse  
✅ **Modularity**: Clear separation between MCP tools, agent logic, guardrails, and API layer  
✅ **Observability**: Structured logging for tool calls, guardrail triggers, and AI errors  

### Architectural Constraints

✅ **Stateless Design**: No server-side session state; conversation history loaded from DB per request  
✅ **Database Schema**: Minimal additions (2 tables: conversation, message) extending existing Phase II schema  
✅ **Integration**: Builds on existing Phase II foundation without modifying core task management  
✅ **Performance**: Guardrails run before expensive AI calls to reduce latency and cost  

### No Violations Detected

All design decisions align with standard web application best practices. No complexity justification required.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
phase-3/
├── backend/
│   ├── src/todo_api/
│   │   ├── main.py              # Add chat router
│   │   ├── config.py            # Add OPENAI_API_KEY
│   │   ├── database.py          # Existing from Phase II
│   │   ├── models/
│   │   │   ├── task.py          # Existing from Phase II
│   │   │   ├── conversation.py  # NEW - Conversation model
│   │   │   └── message.py       # NEW - Message model
│   │   ├── routers/
│   │   │   ├── tasks.py         # Existing from Phase II
│   │   │   └── chat.py          # NEW - Chat endpoint
│   │   ├── services/
│   │   │   ├── task_service.py  # Existing from Phase II
│   │   │   └── chat_service.py  # NEW - Chat orchestration
│   │   ├── mcp/
│   │   │   ├── __init__.py
│   │   │   ├── server.py        # FastMCP server instance
│   │   │   └── tools.py         # 5 task management tools
│   │   └── agent/
│   │       ├── __init__.py
│   │       ├── todo_agent.py    # OpenAI Agents SDK setup
│   │       └── guardrails.py    # Input/output guardrails
│   ├── tests/
│   │   ├── test_mcp_tools.py    # MCP tool tests
│   │   ├── test_guardrails.py   # Guardrail tests
│   │   └── test_chat_api.py     # Chat endpoint tests
│   └── pyproject.toml           # Add fastmcp, openai-agents, openai
│
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── chat/
    │   │   │   └── page.tsx     # NEW - Chat page
    │   │   ├── dashboard/
    │   │   │   └── page.tsx     # Existing from Phase II
    │   │   └── layout.tsx       # Add chat navigation
    │   ├── components/
    │   │   ├── chat/            # NEW
    │   │   │   ├── chat-interface.tsx
    │   │   │   └── message-list.tsx
    │   │   └── tasks/           # Existing from Phase II
    │   └── lib/
    │       ├── chat-api.ts      # NEW - Chat API client
    │       └── api.ts           # Existing from Phase II
    └── package.json             # Add @openai/chatkit
```

**Structure Decision**: Web application architecture extending Phase II. Backend adds chat-specific modules (mcp/, agent/, chat router) while preserving existing task management. Frontend adds chat UI components and page using ChatKit. Phase 2 code is copied to phase-3/ and extended, not modified in place.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. This section is not applicable.
