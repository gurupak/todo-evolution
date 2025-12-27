import { CodeBlock } from "../code-block";

export function QuickStartSection() {
  return (
    <section id="quick-start" data-section className="mb-16">
      <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
        Quick Start
      </h2>
      <p className="text-gray-700 dark:text-gray-300 mb-6">
        Get started with the Todo Evolution API in minutes. Our REST API provides programmatic access
        to task management, and our MCP server enables AI agents to interact with your tasks.
      </p>

      <div className="bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-2">
          Base URL
        </h3>
        <code className="text-sm text-blue-700 dark:text-blue-300 font-mono">
          https://todo-evolution-backend.railway.app
        </code>
      </div>

      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        Making Your First Request
      </h3>
      <p className="text-gray-700 dark:text-gray-300 mb-4">
        All API requests require JWT authentication. Here's a simple example:
      </p>

      <CodeBlock
        language="bash"
        code={`curl -X GET "https://todo-evolution-backend.railway.app/api/{user_id}/tasks" \\
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \\
  -H "Content-Type: application/json"`}
      />

      <CodeBlock
        language="javascript"
        code={`// Using fetch API
const response = await fetch(
  'https://todo-evolution-backend.railway.app/api/{user_id}/tasks',
  {
    headers: {
      'Authorization': 'Bearer YOUR_JWT_TOKEN',
      'Content-Type': 'application/json'
    }
  }
);
const data = await response.json();
console.log(data);`}
      />

      <CodeBlock
        language="python"
        code={`# Using requests library
import requests

headers = {
    "Authorization": "Bearer YOUR_JWT_TOKEN",
    "Content-Type": "application/json"
}

response = requests.get(
    "https://todo-evolution-backend.railway.app/api/{user_id}/tasks",
    headers=headers
)
data = response.json()
print(data)`}
      />
    </section>
  );
}
