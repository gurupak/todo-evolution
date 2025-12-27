import { CodeBlock } from "../code-block";

export function AuthenticationSection() {
  return (
    <section id="authentication" data-section className="mb-16">
      <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
        Authentication
      </h2>
      <p className="text-gray-700 dark:text-gray-300 mb-6">
        Todo Evolution uses JWT (JSON Web Tokens) for authentication. All API requests must include
        a valid JWT token in the Authorization header.
      </p>

      <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-6 mb-6 border border-gray-200 dark:border-gray-800">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
          How It Works
        </h3>
        <ol className="list-decimal list-inside space-y-2 text-gray-700 dark:text-gray-300">
          <li>Sign up or sign in through the web interface at <code className="text-sm bg-gray-200 dark:bg-gray-800 px-2 py-1 rounded">/auth/signup</code> or <code className="text-sm bg-gray-200 dark:bg-gray-800 px-2 py-1 rounded">/auth/signin</code></li>
          <li>The JWT token is automatically stored in an HTTP-only cookie</li>
          <li>Include the cookie in subsequent API requests</li>
          <li>The API validates the JWT and extracts the <code className="text-sm bg-gray-200 dark:bg-gray-800 px-2 py-1 rounded">user_id</code></li>
        </ol>
      </div>

      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        Authorization Header Format
      </h3>
      <CodeBlock
        language="http"
        code={`Authorization: Bearer <your_jwt_token>`}
      />

      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 mt-6">
        User ID Validation
      </h3>
      <p className="text-gray-700 dark:text-gray-300 mb-4">
        All endpoints include a <code className="text-sm bg-gray-200 dark:bg-gray-800 px-2 py-1 rounded">user_id</code> path parameter.
        The API verifies that the <code className="text-sm bg-gray-200 dark:bg-gray-800 px-2 py-1 rounded">user_id</code> in the URL matches
        the <code className="text-sm bg-gray-200 dark:bg-gray-800 px-2 py-1 rounded">user_id</code> from the JWT token.
      </p>

      <div className="bg-yellow-50 dark:bg-yellow-950 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 mb-6">
        <div className="flex items-start">
          <span className="text-yellow-600 dark:text-yellow-400 font-semibold mr-2">⚠️</span>
          <div>
            <p className="text-yellow-800 dark:text-yellow-200 font-semibold mb-1">
              Security Note
            </p>
            <p className="text-yellow-700 dark:text-yellow-300 text-sm">
              If the URL <code className="text-xs bg-yellow-100 dark:bg-yellow-900 px-1 py-0.5 rounded">user_id</code> doesn't
              match the JWT <code className="text-xs bg-yellow-100 dark:bg-yellow-900 px-1 py-0.5 rounded">user_id</code>, the
              API returns a <code className="text-xs bg-yellow-100 dark:bg-yellow-900 px-1 py-0.5 rounded">403 Forbidden</code> error.
              This prevents users from accessing other users' data.
            </p>
          </div>
        </div>
      </div>

      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        Authentication Errors
      </h3>
      <div className="space-y-4">
        <div className="border border-gray-200 dark:border-gray-800 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="font-mono text-sm font-semibold text-gray-900 dark:text-white">
              401 Unauthorized
            </span>
            <span className="text-xs bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 px-2 py-1 rounded">
              Missing or Invalid Token
            </span>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            The request is missing an Authorization header or the JWT token is invalid/expired.
          </p>
        </div>

        <div className="border border-gray-200 dark:border-gray-800 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="font-mono text-sm font-semibold text-gray-900 dark:text-white">
              403 Forbidden
            </span>
            <span className="text-xs bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 px-2 py-1 rounded">
              User ID Mismatch
            </span>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            The user_id in the URL doesn't match the user_id from the JWT token.
          </p>
        </div>
      </div>
    </section>
  );
}
