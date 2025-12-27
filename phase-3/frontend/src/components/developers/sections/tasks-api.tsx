import { CodeBlock } from "../code-block";
import { ApiEndpoint } from "../api-endpoint";

export function TasksApiSection() {
  return (
    <section id="tasks-api" data-section className="mb-16">
      <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
        Tasks API
      </h2>
      <p className="text-gray-700 dark:text-gray-300 mb-8">
        Manage tasks programmatically with full CRUD operations. All endpoints require JWT authentication
        and enforce user data isolation.
      </p>

      {/* List Tasks */}
      <ApiEndpoint
        id="list-tasks"
        method="GET"
        path="/api/{user_id}/tasks"
        title="List Tasks"
        description="Retrieve all tasks for the authenticated user with statistics."
      >
        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Response</h4>
        <CodeBlock
          language="json"
          code={`{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "user_123",
      "title": "Complete project documentation",
      "description": "Write comprehensive API docs",
      "priority": "high",
      "is_completed": false,
      "target_completion_date": "2025-12-31T23:59:59Z",
      "created_at": "2025-12-28T10:00:00Z",
      "updated_at": "2025-12-28T10:00:00Z",
      "completed_at": null
    }
  ],
  "total": 15,
  "completed": 7,
  "pending": 8
}`}
        />

        <h4 className="font-semibold text-gray-900 dark:text-white mb-2 mt-4">Example Request</h4>
        <CodeBlock
          language="javascript"
          code={`const response = await fetch(
  'https://todo-evolution-backend.railway.app/api/user_123/tasks',
  {
    headers: {
      'Authorization': 'Bearer YOUR_JWT_TOKEN'
    }
  }
);
const { tasks, total, completed, pending } = await response.json();`}
        />
      </ApiEndpoint>

      {/* Create Task */}
      <ApiEndpoint
        id="create-task"
        method="POST"
        path="/api/{user_id}/tasks"
        title="Create Task"
        description="Create a new task for the authenticated user."
      >
        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Request Body</h4>
        <CodeBlock
          language="json"
          code={`{
  "title": "Review pull requests",
  "description": "Review and merge pending PRs",
  "priority": "high",
  "target_completion_date": "2025-12-30T17:00:00Z"
}`}
        />

        <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 mb-4 border border-gray-200 dark:border-gray-800">
          <h5 className="font-semibold text-sm text-gray-900 dark:text-white mb-2">Field Constraints</h5>
          <ul className="text-sm space-y-1 text-gray-700 dark:text-gray-300">
            <li><code className="text-xs bg-gray-200 dark:bg-gray-800 px-1 py-0.5 rounded">title</code>: Required, 1-200 characters</li>
            <li><code className="text-xs bg-gray-200 dark:bg-gray-800 px-1 py-0.5 rounded">description</code>: Optional, max 1000 characters (default: "")</li>
            <li><code className="text-xs bg-gray-200 dark:bg-gray-800 px-1 py-0.5 rounded">priority</code>: Optional, one of "high", "medium", "low" (default: "medium")</li>
            <li><code className="text-xs bg-gray-200 dark:bg-gray-800 px-1 py-0.5 rounded">target_completion_date</code>: Optional, ISO 8601 datetime</li>
          </ul>
        </div>

        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Response</h4>
        <CodeBlock
          language="json"
          code={`{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "user_123",
  "title": "Review pull requests",
  "description": "Review and merge pending PRs",
  "priority": "high",
  "is_completed": false,
  "target_completion_date": "2025-12-30T17:00:00Z",
  "created_at": "2025-12-28T14:30:00Z",
  "updated_at": "2025-12-28T14:30:00Z",
  "completed_at": null
}`}
        />

        <h4 className="font-semibold text-gray-900 dark:text-white mb-2 mt-4">Example Request</h4>
        <CodeBlock
          language="javascript"
          code={`const response = await fetch(
  'https://todo-evolution-backend.railway.app/api/user_123/tasks',
  {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_JWT_TOKEN',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title: 'Review pull requests',
      description: 'Review and merge pending PRs',
      priority: 'high',
      target_completion_date: '2025-12-30T17:00:00Z'
    })
  }
);
const task = await response.json();`}
        />
      </ApiEndpoint>

      {/* Get Task */}
      <ApiEndpoint
        id="get-task"
        method="GET"
        path="/api/{user_id}/tasks/{task_id}"
        title="Get Task"
        description="Retrieve a specific task by ID."
      >
        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Response</h4>
        <CodeBlock
          language="json"
          code={`{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user_123",
  "title": "Complete project documentation",
  "description": "Write comprehensive API docs",
  "priority": "high",
  "is_completed": false,
  "target_completion_date": "2025-12-31T23:59:59Z",
  "created_at": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-28T10:00:00Z",
  "completed_at": null
}`}
        />

        <div className="bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg p-4 mt-4">
          <p className="text-sm text-red-700 dark:text-red-300">
            <strong>404 Not Found:</strong> Returns if task doesn't exist or belongs to another user.
          </p>
        </div>
      </ApiEndpoint>

      {/* Update Task */}
      <ApiEndpoint
        id="update-task"
        method="PUT"
        path="/api/{user_id}/tasks/{task_id}"
        title="Update Task"
        description="Update one or more fields of an existing task."
      >
        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Request Body</h4>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
          All fields are optional. Only include fields you want to update.
        </p>
        <CodeBlock
          language="json"
          code={`{
  "title": "Updated task title",
  "description": "Updated description",
  "priority": "medium",
  "target_completion_date": "2025-12-31T23:59:59Z"
}`}
        />

        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Response</h4>
        <CodeBlock
          language="json"
          code={`{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user_123",
  "title": "Updated task title",
  "description": "Updated description",
  "priority": "medium",
  "is_completed": false,
  "target_completion_date": "2025-12-31T23:59:59Z",
  "created_at": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-28T15:30:00Z",
  "completed_at": null
}`}
        />
      </ApiEndpoint>

      {/* Toggle Complete */}
      <ApiEndpoint
        id="toggle-complete"
        method="PATCH"
        path="/api/{user_id}/tasks/{task_id}/complete"
        title="Toggle Complete"
        description="Toggle the completion status of a task. Sets completed_at timestamp when marking complete."
      >
        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Response</h4>
        <CodeBlock
          language="json"
          code={`{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user_123",
  "title": "Complete project documentation",
  "description": "Write comprehensive API docs",
  "priority": "high",
  "is_completed": true,
  "target_completion_date": "2025-12-31T23:59:59Z",
  "created_at": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-28T16:45:00Z",
  "completed_at": "2025-12-28T16:45:00Z"
}`}
        />

        <div className="bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mt-4">
          <p className="text-sm text-blue-700 dark:text-blue-300">
            <strong>Note:</strong> Calling this endpoint again will toggle back to incomplete and set completed_at to null.
          </p>
        </div>
      </ApiEndpoint>

      {/* Delete Task */}
      <ApiEndpoint
        id="delete-task"
        method="DELETE"
        path="/api/{user_id}/tasks/{task_id}"
        title="Delete Task"
        description="Permanently delete a task. This action cannot be undone."
      >
        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Response</h4>
        <CodeBlock
          language="json"
          code={`{
  "message": "Task deleted successfully",
  "id": "550e8400-e29b-41d4-a716-446655440000"
}`}
        />

        <div className="bg-yellow-50 dark:bg-yellow-950 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 mt-4">
          <p className="text-sm text-yellow-700 dark:text-yellow-300">
            <strong>Warning:</strong> This operation is permanent and cannot be reversed.
          </p>
        </div>
      </ApiEndpoint>
    </section>
  );
}
