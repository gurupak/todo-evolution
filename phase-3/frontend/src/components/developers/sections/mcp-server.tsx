import { CodeBlock } from "../code-block";

export function McpServerSection() {
  return (
    <section id="mcp-server" data-section className="mb-16">
      <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
        MCP Server
      </h2>
      <p className="text-gray-700 dark:text-gray-300 mb-8">
        The Model Context Protocol (MCP) server exposes task management tools that AI agents can use
        to interact with the todo system. Built with FastMCP, it provides a standardized interface
        for AI-powered task management.
      </p>

      {/* Overview */}
      <div id="mcp-overview" data-section className="mb-12">
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Overview</h3>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          The MCP server enables AI agents to manage tasks through a set of tools. Each tool requires
          a <code className="text-sm bg-gray-200 dark:bg-gray-800 px-2 py-1 rounded">user_id</code> parameter
          to ensure proper data isolation between users.
        </p>

        <div className="bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-6 mb-6">
          <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">Server Information</h4>
          <ul className="space-y-2 text-sm text-blue-700 dark:text-blue-300">
            <li><strong>Server Name:</strong> <code className="bg-blue-100 dark:bg-blue-900 px-2 py-0.5 rounded">todo-server</code></li>
            <li><strong>Framework:</strong> FastMCP (Python)</li>
            <li><strong>Protocol:</strong> Model Context Protocol (MCP)</li>
            <li><strong>Database:</strong> PostgreSQL via SQLModel</li>
            <li><strong>User Isolation:</strong> Enforced via user_id parameter</li>
          </ul>
        </div>
      </div>

      {/* Setup */}
      <div id="mcp-setup" data-section className="mb-12">
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Setup</h3>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          To connect an AI agent to the MCP server, configure your MCP client with the server details.
        </p>

        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
          Claude Desktop Configuration
        </h4>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
          Add the following to your Claude Desktop MCP settings (<code className="text-xs bg-gray-200 dark:bg-gray-800 px-1 py-0.5 rounded">claude_desktop_config.json</code>):
        </p>

        <CodeBlock
          language="json"
          code={`{
  "mcpServers": {
    "todo-server": {
      "command": "uvx",
      "args": [
        "fastmcp",
        "run",
        "path/to/todo_api/mcp/server.py"
      ],
      "env": {
        "DATABASE_URL": "postgresql://...",
        "PYTHONPATH": "path/to/backend/src"
      }
    }
  }
}`}
        />

        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 mt-6">
          Environment Variables
        </h4>
        <CodeBlock
          language="bash"
          code={`DATABASE_URL=postgresql://user:password@host:port/database
PYTHONPATH=/path/to/backend/src`}
        />
      </div>

      {/* Available Tools */}
      <div id="mcp-tools" data-section className="mb-12">
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Available Tools</h3>

        {/* list_tasks */}
        <div className="border-l-4 border-green-500 dark:border-green-400 pl-6 mb-8">
          <div className="mb-3">
            <span className="inline-block bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 px-3 py-1 rounded text-xs font-bold uppercase tracking-wide mb-2">
              MCP Tool
            </span>
            <h4 className="text-xl font-bold text-gray-900 dark:text-white">list_tasks</h4>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              List all tasks for a specific user, ordered by creation date (newest first).
            </p>
          </div>

          <h5 className="font-semibold text-gray-900 dark:text-white mb-2">Parameters</h5>
          <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 mb-4 border border-gray-200 dark:border-gray-800">
            <ul className="text-sm space-y-1 text-gray-700 dark:text-gray-300">
              <li><code className="text-xs bg-gray-200 dark:bg-gray-800 px-1 py-0.5 rounded">user_id</code>: <strong>Required.</strong> The ID of the user whose tasks to retrieve (string).</li>
            </ul>
          </div>

          <h5 className="font-semibold text-gray-900 dark:text-white mb-2">Returns</h5>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
            List of task dictionaries with all task fields.
          </p>
          <CodeBlock
            language="json"
            code={`[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user_123",
    "title": "Complete project documentation",
    "description": "Write comprehensive API docs",
    "priority": "high",
    "is_completed": false,
    "created_at": "2025-12-28T10:00:00",
    "updated_at": "2025-12-28T10:00:00"
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "user_id": "user_123",
    "title": "Review pull requests",
    "description": "",
    "priority": "medium",
    "is_completed": true,
    "created_at": "2025-12-27T14:00:00",
    "updated_at": "2025-12-28T09:30:00"
  }
]`}
          />

          <h5 className="font-semibold text-gray-900 dark:text-white mb-2 mt-4">Usage Example (Python)</h5>
          <CodeBlock
            language="python"
            code={`# In an MCP-enabled AI agent
tasks = await list_tasks(user_id="user_123")
print(f"Found {len(tasks)} tasks")
for task in tasks:
    print(f"- {task['title']} ({task['priority']})")`}
          />
        </div>

        {/* Future Tools Notice */}
        <div className="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6">
          <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
            🚧 Additional Tools Coming Soon
          </h4>
          <p className="text-sm text-gray-700 dark:text-gray-300 mb-3">
            The MCP server currently exposes <code className="text-xs bg-gray-200 dark:bg-gray-800 px-1 py-0.5 rounded">list_tasks</code>.
            Additional tools for creating, updating, and deleting tasks will be added in future releases.
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            <strong>Expected tools:</strong> create_task, update_task, toggle_task_complete, delete_task
          </p>
        </div>
      </div>

      {/* Integration Notes */}
      <div className="bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
        <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-3">
          Integration with Chat API
        </h4>
        <p className="text-sm text-blue-700 dark:text-blue-300">
          The Chat API uses these MCP tools internally when processing user requests through the
          OpenAI Agents SDK. When you send a chat message like "show me my tasks", the AI agent
          automatically calls the appropriate MCP tools and formats the response in natural language.
        </p>
      </div>
    </section>
  );
}
