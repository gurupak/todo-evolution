"use client";

import { Task } from "@/types/task";
import { TaskItem } from "./task-item";
import { TaskEmpty } from "./task-empty";

interface TaskListProps {
  tasks: Task[];
  isLoading?: boolean;
  error?: Error | null;
  onEdit?: (task: Task) => void;
}

/**
 * Task list component with loading and error states
 * Displays all tasks in a scrollable list (T083)
 */
export function TaskList({ tasks, isLoading, error, onEdit }: TaskListProps) {
  if (isLoading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700 animate-pulse"
          >
            <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2" />
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2" />
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 text-center">
        <div className="text-red-600 dark:text-red-400 text-lg font-semibold mb-2">
          Failed to load tasks
        </div>
        <div className="text-red-600 dark:text-red-400 text-sm">
          {error.message || "An error occurred"}
        </div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return <TaskEmpty />;
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} onEdit={onEdit} />
      ))}
    </div>
  );
}
