interface ApiEndpointProps {
  id: string;
  method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  path: string;
  title: string;
  description: string;
  children: React.ReactNode;
}

const methodColors = {
  GET: "bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300",
  POST: "bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300",
  PUT: "bg-yellow-100 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-300",
  PATCH: "bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300",
  DELETE: "bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300",
};

export function ApiEndpoint({ id, method, path, title, description, children }: ApiEndpointProps) {
  return (
    <div id={id} data-section className="mb-12 scroll-mt-24">
      <div className="border-l-4 border-blue-500 dark:border-blue-400 pl-6 mb-4">
        <div className="flex items-center gap-3 mb-2">
          <span
            className={`px-3 py-1 rounded text-xs font-bold uppercase tracking-wide ${methodColors[method]}`}
          >
            {method}
          </span>
          <code className="text-sm font-mono text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded">
            {path}
          </code>
        </div>
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">{title}</h3>
        <p className="text-gray-600 dark:text-gray-400">{description}</p>
      </div>
      <div className="pl-6">{children}</div>
    </div>
  );
}
