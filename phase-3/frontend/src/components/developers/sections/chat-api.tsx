import { CodeBlock } from "../code-block";
import { ApiEndpoint } from "../api-endpoint";

export function ChatApiSection() {
  return (
    <section id="chat-api" data-section className="mb-16">
      <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
        Chat API
      </h2>
      <p className="text-gray-700 dark:text-gray-300 mb-8">
        Interact with the AI-powered chat assistant. The assistant uses MCP tools to manage tasks
        through natural language conversations with built-in guardrails for task-focused interactions.
      </p>

      {/* Send Message */}
      <ApiEndpoint
        id="send-message"
        method="POST"
        path="/api/{user_id}/chat"
        title="Send Chat Message"
        description="Send a message to the AI assistant and receive a response. Supports both new and existing conversations."
      >
        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Request Body</h4>
        <CodeBlock
          language="json"
          code={`{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Create a high priority task to review the API documentation"
}`}
        />

        <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 mb-4 border border-gray-200 dark:border-gray-800">
          <h5 className="font-semibold text-sm text-gray-900 dark:text-white mb-2">Fields</h5>
          <ul className="text-sm space-y-1 text-gray-700 dark:text-gray-300">
            <li><code className="text-xs bg-gray-200 dark:bg-gray-800 px-1 py-0.5 rounded">conversation_id</code>: Optional UUID. Omit to start a new conversation, include to resume existing.</li>
            <li><code className="text-xs bg-gray-200 dark:bg-gray-800 px-1 py-0.5 rounded">message</code>: Required, 1-2000 characters. The user's message to the assistant.</li>
          </ul>
        </div>

        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Response</h4>
        <CodeBlock
          language="json"
          code={`{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "I've created a high priority task for you: 'Review the API documentation'. Would you like me to add any additional details or set a deadline?",
  "tool_calls": {
    "create_task": {
      "title": "Review the API documentation",
      "priority": "high",
      "user_id": "user_123"
    }
  }
}`}
        />

        <div className="bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mt-4">
          <p className="text-sm text-blue-700 dark:text-blue-300">
            <strong>Guardrails:</strong> The assistant is focused on task management. Off-topic messages
            receive a 403 Forbidden response with a helpful redirect message.
          </p>
        </div>

        <h4 className="font-semibold text-gray-900 dark:text-white mb-2 mt-6">Example Request</h4>
        <CodeBlock
          language="javascript"
          code={`const response = await fetch(
  'https://todo-evolution-backend.railway.app/api/user_123/chat',
  {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_JWT_TOKEN',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: 'Show me all my high priority tasks'
    })
  }
);
const { conversation_id, response, tool_calls } = await response.json();`}
        />

        <h4 className="font-semibold text-gray-900 dark:text-white mb-2 mt-6">Error Responses</h4>
        <div className="space-y-3">
          <div className="border border-gray-200 dark:border-gray-800 rounded-lg p-3">
            <div className="flex items-center justify-between mb-1">
              <span className="font-mono text-xs font-semibold text-gray-900 dark:text-white">403 Forbidden</span>
              <span className="text-xs bg-yellow-100 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-300 px-2 py-0.5 rounded">Guardrail Block</span>
            </div>
            <p className="text-xs text-gray-600 dark:text-gray-400">Off-topic message rejected by input guardrail.</p>
          </div>
          <div className="border border-gray-200 dark:border-gray-800 rounded-lg p-3">
            <div className="flex items-center justify-between mb-1">
              <span className="font-mono text-xs font-semibold text-gray-900 dark:text-white">404 Not Found</span>
              <span className="text-xs bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 px-2 py-0.5 rounded">Invalid Conversation</span>
            </div>
            <p className="text-xs text-gray-600 dark:text-gray-400">Conversation ID not found or access denied.</p>
          </div>
          <div className="border border-gray-200 dark:border-gray-800 rounded-lg p-3">
            <div className="flex items-center justify-between mb-1">
              <span className="font-mono text-xs font-semibold text-gray-900 dark:text-white">429 Too Many Requests</span>
              <span className="text-xs bg-orange-100 dark:bg-orange-900 text-orange-700 dark:text-orange-300 px-2 py-0.5 rounded">Rate Limit</span>
            </div>
            <p className="text-xs text-gray-600 dark:text-gray-400">OpenAI API rate limit exceeded. Retry after 30 seconds.</p>
          </div>
        </div>
      </ApiEndpoint>

      {/* List Conversations */}
      <ApiEndpoint
        id="list-conversations"
        method="GET"
        path="/api/{user_id}/conversations"
        title="List Conversations"
        description="Get all conversations for the authenticated user, sorted by most recently updated first."
      >
        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Response</h4>
        <CodeBlock
          language="json"
          code={`{
  "conversations": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Task Planning Session",
      "created_at": "2025-12-28T10:00:00Z",
      "updated_at": "2025-12-28T15:30:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "title": "New conversation",
      "created_at": "2025-12-27T14:00:00Z",
      "updated_at": "2025-12-27T14:15:00Z"
    }
  ]
}`}
        />
      </ApiEndpoint>

      {/* Get Conversation */}
      <ApiEndpoint
        id="get-conversation"
        method="GET"
        path="/api/{user_id}/conversations/{conversation_id}"
        title="Get Conversation"
        description="Retrieve a specific conversation with all messages. Supports pagination."
      >
        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Query Parameters</h4>
        <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 mb-4 border border-gray-200 dark:border-gray-800">
          <ul className="text-sm space-y-1 text-gray-700 dark:text-gray-300">
            <li><code className="text-xs bg-gray-200 dark:bg-gray-800 px-1 py-0.5 rounded">limit</code>: Optional, max 100 (default: 50). Number of messages to return.</li>
            <li><code className="text-xs bg-gray-200 dark:bg-gray-800 px-1 py-0.5 rounded">offset</code>: Optional (default: 0). Number of messages to skip for pagination.</li>
          </ul>
        </div>

        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Response</h4>
        <CodeBlock
          language="json"
          code={`{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-28T15:30:00Z",
  "messages": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "role": "user",
      "content": "Create a task to review documentation",
      "created_at": "2025-12-28T10:00:00Z",
      "tool_calls": null
    },
    {
      "id": "880e8400-e29b-41d4-a716-446655440003",
      "role": "assistant",
      "content": "I've created the task for you...",
      "created_at": "2025-12-28T10:00:05Z",
      "tool_calls": {
        "create_task": {
          "title": "Review documentation",
          "user_id": "user_123"
        }
      }
    }
  ]
}`}
        />

        <h4 className="font-semibold text-gray-900 dark:text-white mb-2 mt-4">Example with Pagination</h4>
        <CodeBlock
          language="bash"
          code={`curl "https://todo-evolution-backend.railway.app/api/user_123/conversations/550e8400-e29b-41d4-a716-446655440000?limit=20&offset=0" \\
  -H "Authorization: Bearer YOUR_JWT_TOKEN"`}
        />
      </ApiEndpoint>

      {/* Update Conversation */}
      <ApiEndpoint
        id="update-conversation"
        method="PATCH"
        path="/api/{user_id}/conversations/{conversation_id}"
        title="Update Conversation"
        description="Update conversation properties such as title."
      >
        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Request Body</h4>
        <CodeBlock
          language="json"
          code={`{
  "title": "Project Planning Discussion"
}`}
        />

        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Response</h4>
        <CodeBlock
          language="json"
          code={`{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Project Planning Discussion",
  "created_at": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-28T16:00:00Z"
}`}
        />
      </ApiEndpoint>

      {/* Delete Conversation */}
      <ApiEndpoint
        id="delete-conversation"
        method="DELETE"
        path="/api/{user_id}/conversations/{conversation_id}"
        title="Delete Conversation"
        description="Permanently delete a conversation and all its messages."
      >
        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Response</h4>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
          Returns <code className="text-xs bg-gray-200 dark:bg-gray-800 px-1 py-0.5 rounded">204 No Content</code> on success (no response body).
        </p>

        <div className="bg-yellow-50 dark:bg-yellow-950 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
          <p className="text-sm text-yellow-700 dark:text-yellow-300">
            <strong>Warning:</strong> This permanently deletes the conversation and all associated messages. This action cannot be undone.
          </p>
        </div>
      </ApiEndpoint>
    </section>
  );
}
