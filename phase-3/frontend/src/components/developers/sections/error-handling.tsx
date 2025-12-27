import { CodeBlock } from "../code-block";

export function ErrorHandlingSection() {
  return (
    <section id="error-handling" data-section className="mb-16">
      <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
        Error Handling
      </h2>
      <p className="text-gray-700 dark:text-gray-300 mb-8">
        The API uses standard HTTP status codes to indicate success or failure. All error responses
        include a JSON body with detailed error information.
      </p>

      {/* HTTP Status Codes */}
      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        HTTP Status Codes
      </h3>

      <div className="space-y-4 mb-8">
        {/* 2xx Success */}
        <div className="border border-gray-200 dark:border-gray-800 rounded-lg p-4">
          <div className="flex items-center justify-between mb-3">
            <h4 className="font-semibold text-gray-900 dark:text-white">2xx Success</h4>
            <span className="text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 px-2 py-1 rounded">
              Success
            </span>
          </div>
          <ul className="space-y-2 text-sm">
            <li className="flex items-start">
              <code className="font-mono text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded mr-3 mt-0.5">200</code>
              <span className="text-gray-700 dark:text-gray-300">OK - Request succeeded</span>
            </li>
            <li className="flex items-start">
              <code className="font-mono text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded mr-3 mt-0.5">201</code>
              <span className="text-gray-700 dark:text-gray-300">Created - Resource successfully created (POST requests)</span>
            </li>
            <li className="flex items-start">
              <code className="font-mono text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded mr-3 mt-0.5">204</code>
              <span className="text-gray-700 dark:text-gray-300">No Content - Request succeeded with no response body (DELETE requests)</span>
            </li>
          </ul>
        </div>

        {/* 4xx Client Errors */}
        <div className="border border-gray-200 dark:border-gray-800 rounded-lg p-4">
          <div className="flex items-center justify-between mb-3">
            <h4 className="font-semibold text-gray-900 dark:text-white">4xx Client Errors</h4>
            <span className="text-xs bg-yellow-100 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-300 px-2 py-1 rounded">
              Client Error
            </span>
          </div>
          <ul className="space-y-2 text-sm">
            <li className="flex items-start">
              <code className="font-mono text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded mr-3 mt-0.5">400</code>
              <span className="text-gray-700 dark:text-gray-300">Bad Request - Invalid request body or parameters</span>
            </li>
            <li className="flex items-start">
              <code className="font-mono text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded mr-3 mt-0.5">401</code>
              <span className="text-gray-700 dark:text-gray-300">Unauthorized - Missing or invalid JWT token</span>
            </li>
            <li className="flex items-start">
              <code className="font-mono text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded mr-3 mt-0.5">403</code>
              <span className="text-gray-700 dark:text-gray-300">Forbidden - user_id mismatch or guardrail blocked request</span>
            </li>
            <li className="flex items-start">
              <code className="font-mono text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded mr-3 mt-0.5">404</code>
              <span className="text-gray-700 dark:text-gray-300">Not Found - Resource doesn't exist or access denied</span>
            </li>
            <li className="flex items-start">
              <code className="font-mono text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded mr-3 mt-0.5">422</code>
              <span className="text-gray-700 dark:text-gray-300">Unprocessable Entity - Validation error (Pydantic schema failed)</span>
            </li>
            <li className="flex items-start">
              <code className="font-mono text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded mr-3 mt-0.5">429</code>
              <span className="text-gray-700 dark:text-gray-300">Too Many Requests - Rate limit exceeded (includes Retry-After header)</span>
            </li>
          </ul>
        </div>

        {/* 5xx Server Errors */}
        <div className="border border-gray-200 dark:border-gray-800 rounded-lg p-4">
          <div className="flex items-center justify-between mb-3">
            <h4 className="font-semibold text-gray-900 dark:text-white">5xx Server Errors</h4>
            <span className="text-xs bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 px-2 py-1 rounded">
              Server Error
            </span>
          </div>
          <ul className="space-y-2 text-sm">
            <li className="flex items-start">
              <code className="font-mono text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded mr-3 mt-0.5">500</code>
              <span className="text-gray-700 dark:text-gray-300">Internal Server Error - Unexpected server error</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Error Response Format */}
      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        Error Response Format
      </h3>
      <p className="text-gray-700 dark:text-gray-300 mb-4">
        All error responses follow a consistent JSON format with a <code className="text-sm bg-gray-200 dark:bg-gray-800 px-2 py-1 rounded">detail</code> field
        containing a human-readable error message.
      </p>

      <CodeBlock
        language="json"
        code={`{
  "detail": "Error message describing what went wrong"
}`}
      />

      {/* Common Error Examples */}
      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 mt-8">
        Common Error Examples
      </h3>

      <div className="space-y-6">
        {/* Validation Error */}
        <div>
          <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
            Validation Error (422)
          </h4>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
            When request body fails Pydantic validation (e.g., title too long, invalid priority value):
          </p>
          <CodeBlock
            language="json"
            code={`{
  "detail": [
    {
      "type": "string_too_long",
      "loc": ["body", "title"],
      "msg": "String should have at most 200 characters",
      "input": "Very long title that exceeds the maximum length...",
      "ctx": {
        "max_length": 200
      }
    }
  ]
}`}
          />
        </div>

        {/* Authentication Error */}
        <div>
          <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
            Authentication Error (401)
          </h4>
          <CodeBlock
            language="json"
            code={`{
  "detail": "Could not validate credentials"
}`}
          />
        </div>

        {/* Authorization Error */}
        <div>
          <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
            Authorization Error (403)
          </h4>
          <CodeBlock
            language="json"
            code={`{
  "detail": "User ID in URL does not match authenticated user"
}`}
          />
        </div>

        {/* Guardrail Block */}
        <div>
          <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
            Guardrail Block (403)
          </h4>
          <CodeBlock
            language="json"
            code={`{
  "detail": "I'm your todo assistant and can only help with task management. I can help you: add tasks, view tasks, mark complete, delete tasks, update details. What would you like to do?"
}`}
          />
        </div>

        {/* Rate Limit */}
        <div>
          <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
            Rate Limit (429)
          </h4>
          <CodeBlock
            language="json"
            code={`{
  "detail": "High demand. Please wait 30s and try again."
}`}
          />
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            Response includes <code className="text-xs bg-gray-200 dark:bg-gray-800 px-1 py-0.5 rounded">Retry-After: 30</code> header.
          </p>
        </div>

        {/* Not Found */}
        <div>
          <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
            Not Found (404)
          </h4>
          <CodeBlock
            language="json"
            code={`{
  "detail": "Task not found"
}`}
          />
        </div>
      </div>

      {/* Best Practices */}
      <div className="bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-6 mt-8">
        <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-3">
          Error Handling Best Practices
        </h4>
        <ul className="space-y-2 text-sm text-blue-700 dark:text-blue-300">
          <li className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Always check the HTTP status code before parsing the response body</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Handle 401/403 errors by redirecting users to sign in</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">✓</span>
            <span>For 429 errors, respect the Retry-After header and implement exponential backoff</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Display user-friendly error messages from the detail field</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Log full error responses for debugging but never expose internal details to users</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">✓</span>
            <span>Implement client-side validation matching server constraints to reduce 422 errors</span>
          </li>
        </ul>
      </div>

      {/* Example Error Handler */}
      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 mt-8">
        Example Error Handler
      </h3>
      <CodeBlock
        language="javascript"
        code={`async function apiRequest(url, options = {}) {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Authorization': \`Bearer \${getToken()}\`,
        'Content-Type': 'application/json',
        ...options.headers
      }
    });

    if (!response.ok) {
      const error = await response.json();

      switch (response.status) {
        case 401:
          // Redirect to login
          window.location.href = '/auth/signin';
          break;
        case 403:
          throw new Error(error.detail || 'Access denied');
        case 404:
          throw new Error('Resource not found');
        case 422:
          // Validation error - display specific field errors
          const fieldErrors = error.detail.map(e => e.msg).join(', ');
          throw new Error(\`Validation failed: \${fieldErrors}\`);
        case 429:
          const retryAfter = response.headers.get('Retry-After') || 30;
          throw new Error(\`Rate limit exceeded. Retry after \${retryAfter}s\`);
        default:
          throw new Error(error.detail || 'An error occurred');
      }
    }

    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

// Usage
try {
  const tasks = await apiRequest('/api/user_123/tasks');
  console.log('Tasks:', tasks);
} catch (error) {
  // Display error to user
  showErrorToast(error.message);
}`}
      />
    </section>
  );
}
