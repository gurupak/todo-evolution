/**
 * Empty state component shown when user has no tasks
 * Friendly message encouraging task creation (T081)
 */
export function TaskEmpty() {
  return (
    <div className="text-center py-12">
      <div className="text-6xl mb-4">📝</div>
      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        No tasks yet
      </h3>
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        Get started by creating your first task
      </p>
    </div>
  );
}
