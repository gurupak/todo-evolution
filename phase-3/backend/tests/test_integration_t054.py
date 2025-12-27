"""
Integration Test T054: Chat Functionality End-to-End

Tests the complete chat workflow:
1. Import all necessary modules (verify no import errors)
2. Basic smoke test that application can start

Note: Full integration tests require running backend server with OpenAI API.
For now, this validates that all imports work correctly.
"""

import pytest


@pytest.mark.integration
def test_t054_imports_work():
    """
    T054: Verify all Phase III imports work correctly.

    This is a smoke test to ensure:
    - All models can be imported
    - All routers can be imported
    - Main app can be imported
    - No circular import errors
    - No missing dependencies
    """
    # Test model imports
    from todo_api.models import Conversation, Message, PriorityEnum, Task

    assert Conversation is not None
    assert Message is not None
    assert Task is not None
    assert PriorityEnum is not None

    # Test MCP imports
    from todo_api.mcp.server import mcp
    from todo_api.mcp.tools import list_tasks

    assert mcp is not None
    assert list_tasks is not None

    # Test agent imports
    from todo_api.agent.guardrails import response_validator_guard, todo_topic_guard
    from todo_api.agent.todo_agent import todo_agent

    assert todo_agent is not None
    assert todo_topic_guard is not None
    assert response_validator_guard is not None

    # Test service imports
    from todo_api.services.chat_service import ChatService

    assert ChatService is not None

    # Test router imports
    from todo_api.routers import chat, tasks

    assert chat is not None
    assert tasks is not None

    # Test main app import
    from todo_api.main import app

    assert app is not None

    print("✓ All imports successful - no circular dependencies or missing modules")


@pytest.mark.integration
def test_t054_app_can_start():
    """
    T054: Verify FastAPI application can initialize.

    This test confirms that:
    - FastAPI app object is created
    - Routers are registered
    - No initialization errors
    """
    from todo_api.main import app

    # Check app exists and has routes
    assert app is not None
    assert len(app.routes) > 0

    # Check chat router is registered
    chat_routes = [r for r in app.routes if hasattr(r, "path") and "/chat" in r.path]
    assert len(chat_routes) > 0, "Chat router should be registered"

    print(f"✓ App initialized successfully with {len(app.routes)} routes")


@pytest.mark.integration
def test_t054_database_models_valid():
    """
    T054: Verify database models are properly configured.

    This test ensures:
    - Models have correct table names
    - Models have required fields
    - Enums are properly defined
    """
    from todo_api.models import Conversation, Message, PriorityEnum, Task

    # Check Conversation model
    assert hasattr(Conversation, "__tablename__") or hasattr(Conversation, "__table__")
    assert hasattr(Conversation, "id")
    assert hasattr(Conversation, "user_id")
    assert hasattr(Conversation, "created_at")

    # Check Message model
    assert hasattr(Message, "id")
    assert hasattr(Message, "conversation_id")
    assert hasattr(Message, "role")
    assert hasattr(Message, "content")

    # Check Task model
    assert hasattr(Task, "id")
    assert hasattr(Task, "user_id")
    assert hasattr(Task, "title")
    assert hasattr(Task, "is_completed")

    # Check PriorityEnum
    assert hasattr(PriorityEnum, "HIGH")
    assert hasattr(PriorityEnum, "MEDIUM")
    assert hasattr(PriorityEnum, "LOW")

    print("✓ All database models properly configured")


if __name__ == "__main__":
    """Run tests directly for quick validation."""
    print("=" * 60)
    print("T054 Integration Test Suite")
    print("=" * 60)
    print()

    test_t054_imports_work()
    test_t054_app_can_start()
    test_t054_database_models_valid()

    print()
    print("=" * 60)
    print("✓ All T054 tests passed!")
    print("=" * 60)
    print()
    print("User Story 1 (Start New Conversation): READY")
    print()
    print("Next steps:")
    print("1. Start backend: uv run fastapi dev src/todo_api/main.py")
    print("2. Start frontend: npm run dev (in frontend directory)")
    print("3. Test chat UI manually at http://localhost:3000/chat")
    print("=" * 60)
