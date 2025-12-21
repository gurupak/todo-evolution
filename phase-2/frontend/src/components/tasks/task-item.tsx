"use client";

import { useState } from "react";
import { Task } from "@/types/task";
import { PriorityBadge } from "./priority-badge";
import { useToggleComplete, useDeleteTask } from "@/hooks/use-tasks";
import { toast } from "sonner";

interface TaskItemProps {
  task: Task;
  onEdit?: (task: Task) => void;
}

/**
 * Individual task item component with checkbox and actions
 * Displays title, description, priority, and completion status (T082)
 */
export function TaskItem({ task, onEdit }: TaskItemProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const toggleComplete = useToggleComplete();
  const deleteTask = useDeleteTask();

  const handleToggle = async () => {
    try {
      await toggleComplete.mutateAsync(task.id);
      toast.success(
        task.is_completed ? "Task marked as incomplete" : "Task completed!",
      );
    } catch (error) {
      toast.error("Failed to update task");
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this task?")) {
      return;
    }

    setIsDeleting(true);
    try {
      await deleteTask.mutateAsync(task.id);
      toast.success("Task deleted");
    } catch (error) {
      toast.error("Failed to delete task");
      setIsDeleting(false);
    }
  };

  return (
    <div
      className={`bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700 transition-opacity ${
        isDeleting ? "opacity-50" : ""
      }`}
    >
      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          checked={task.is_completed}
          onChange={handleToggle}
          disabled={toggleComplete.isPending || isDeleting}
          className="mt-1 h-5 w-5 text-blue-600 rounded border-gray-300 focus:ring-blue-500 focus:ring-2"
        />

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2 mb-1">
            <h3
              className={`text-lg font-medium ${
                task.is_completed
                  ? "line-through text-gray-500 dark:text-gray-500"
                  : "text-gray-900 dark:text-white"
              }`}
            >
              {task.title}
            </h3>
            <PriorityBadge priority={task.priority} />
          </div>

          {task.description && (
            <p
              className={`text-sm mb-2 ${
                task.is_completed
                  ? "text-gray-400 dark:text-gray-600"
                  : "text-gray-600 dark:text-gray-400"
              }`}
            >
              {task.description}
            </p>
          )}

          <div className="flex items-center gap-3 text-xs">
            <span className="text-gray-500 dark:text-gray-500">
              Created {new Date(task.created_at).toLocaleDateString()}
            </span>
            {task.target_completion_date &&
              !task.is_completed &&
              (() => {
                const dueDate = new Date(task.target_completion_date);
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                dueDate.setHours(0, 0, 0, 0);
                const isOverdue = dueDate < today;
                const isDueToday = dueDate.getTime() === today.getTime();

                return (
                  <span
                    className={`flex items-center gap-1 px-2 py-1 rounded-md font-medium ${
                      isOverdue
                        ? "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300"
                        : isDueToday
                          ? "bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300"
                          : "bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300"
                    }`}
                  >
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                      />
                    </svg>
                    {isOverdue ? "Overdue" : isDueToday ? "Due Today" : "Due"}{" "}
                    {new Date(task.target_completion_date).toLocaleDateString()}
                  </span>
                );
              })()}
            {task.completed_at && (
              <span>
                Completed {new Date(task.completed_at).toLocaleDateString()}
              </span>
            )}
          </div>
        </div>

        <div className="flex gap-2">
          {onEdit && !task.is_completed && (
            <button
              onClick={() => onEdit(task)}
              disabled={isDeleting}
              className="text-gray-600 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 transition-colors"
              title="Edit task"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                />
              </svg>
            </button>
          )}

          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="text-gray-600 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400 transition-colors disabled:opacity-50"
            title="Delete task"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
