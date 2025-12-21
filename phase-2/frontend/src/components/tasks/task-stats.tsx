interface TaskStatsProps {
  total: number;
  completed: number;
  pending: number;
}

/**
 * Component displaying task statistics
 * Shows total, completed, and pending tasks (T080)
 */
export function TaskStats({ total, completed, pending }: TaskStatsProps) {
  const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;

  return (
    <div className="grid grid-cols-3 gap-4 mb-6">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
        <div className="text-2xl font-bold text-gray-900 dark:text-white">{total}</div>
        <div className="text-sm text-gray-600 dark:text-gray-400">Total Tasks</div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
        <div className="text-2xl font-bold text-green-600 dark:text-green-400">{completed}</div>
        <div className="text-sm text-gray-600 dark:text-gray-400">Completed</div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
        <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{pending}</div>
        <div className="text-sm text-gray-600 dark:text-gray-400">Pending</div>
      </div>

      {total > 0 && (
        <div className="col-span-3 bg-gray-100 dark:bg-gray-800 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Completion Rate
            </span>
            <span className="text-sm font-bold text-gray-900 dark:text-white">
              {completionRate}%
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className="bg-green-600 dark:bg-green-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${completionRate}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
