#!/bin/bash
#
# Quick script to run integration test T054
# Usage: ./run-test-t054.sh
#

set -e  # Exit on error

echo "=================================================="
echo "Running Integration Test T054"
echo "=================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found"
    echo "   Please run this script from phase-3/backend directory"
    echo ""
    echo "   Usage:"
    echo "   cd phase-3/backend"
    echo "   ./run-test-t054.sh"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Creating template .env file..."
    cat > .env << 'EOF'
# Database
DATABASE_URL=postgresql://user:password@localhost/dbname

# OpenAI
OPENAI_API_KEY=sk-proj-your-api-key-here

# Better Auth
BETTER_AUTH_SECRET=your-secret-here
BETTER_AUTH_URL=http://localhost:3000
EOF
    echo "   ✅ Created .env template"
    echo "   ⚠️  Please update .env with your actual credentials"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to exit..."
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ Error: UV is not installed"
    echo "   Install UV first: https://docs.astral.sh/uv/"
    exit 1
fi

echo "📦 Syncing dependencies with UV..."
uv sync

echo ""
echo "🧪 Running integration test T054..."
echo ""

# Run the test with verbose output
uv run pytest tests/test_integration_t054.py -v

# Capture exit code
TEST_EXIT_CODE=$?

echo ""
echo "=================================================="
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ Integration Test T054: PASSED"
    echo "=================================================="
    echo ""
    echo "All acceptance criteria met:"
    echo "  ✓ User can start new conversation"
    echo "  ✓ User can send message"
    echo "  ✓ AI responds with greeting"
    echo "  ✓ Conversation persisted in database"
    echo ""
    echo "Next steps:"
    echo "  - Run manual test (see INTEGRATION_TEST_T054.md)"
    echo "  - Proceed to User Story 2 (T055-T062)"
else
    echo "❌ Integration Test T054: FAILED"
    echo "=================================================="
    echo ""
    echo "Troubleshooting tips:"
    echo "  1. Check .env file has correct credentials"
    echo "  2. Verify database migration applied: uv run alembic upgrade head"
    echo "  3. Ensure OpenAI API key is valid"
    echo "  4. Check logs above for specific error"
    echo ""
    echo "For more help, see:"
    echo "  - RUN_TESTS.md (troubleshooting section)"
    echo "  - INTEGRATION_TEST_T054.md (manual test guide)"
fi

echo "=================================================="
echo ""

exit $TEST_EXIT_CODE
