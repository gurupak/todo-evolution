"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/use-auth";
import { useTasks } from "@/hooks/use-tasks";
import { TaskStats } from "@/components/tasks/task-stats";
import { TaskList } from "@/components/tasks/task-list";
import { TaskForm } from "@/components/tasks/task-form";
import { Header } from "@/components/layout/header";
import type { Task } from "@/types/task";

/**
 * Dashboard page with full task management
 * Create, view, edit, delete, and complete tasks (T085, T086)
 */
export default function DashboardPage() {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();
  const { data, isLoading: tasksLoading, error } = useTasks();
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Redirect to signin if not authenticated (after loading completes)
  useEffect(() => {
    if (!authLoading && !user) {
      console.log("User not authenticated, redirecting to signin...");
      router.replace("/auth/signin?callbackUrl=/dashboard");
    }
  }, [authLoading, user, router]);

  // Always render the layout with header
  const renderContent = () => {
    if (authLoading) {
      return (
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-600 dark:text-gray-400">
            Loading authentication...
          </div>
        </div>
      );
    }

    if (!user) {
      return (
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-600 dark:text-gray-400">
            Please sign in to continue
          </div>
        </div>
      );
    }

    if (tasksLoading) {
      return (
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-600 dark:text-gray-400">
            Loading tasks...
          </div>
        </div>
      );
    }

    return (
      <>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              My Tasks
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              Welcome back, {user?.name || "User"}!
            </p>
          </div>

          <button
            onClick={() => setIsDialogOpen(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors flex items-center gap-2"
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
                d="M12 4v16m8-8H4"
              />
            </svg>
            Add Task
          </button>
        </div>

        <TaskStats {...stats} />

        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
          <TaskList
            tasks={tasks}
            isLoading={tasksLoading}
            error={error}
            onEdit={handleEdit}
          />
        </div>
      </>
    );
  };

  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setIsDialogOpen(true);
  };

  const handleClose = () => {
    setIsDialogOpen(false);
    setEditingTask(null);
  };

  const tasks = data?.tasks || [];
  const stats = {
    total: data?.total || 0,
    completed: data?.completed || 0,
    pending: data?.pending || 0,
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header user={user || { id: "", email: "Loading...", name: "" }} />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {renderContent()}

        {/* Task Dialog */}
        {isDialogOpen && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <div
              className="bg-white dark:bg-gray-800 rounded-lg max-w-lg w-full p-6"
              onClick={(e) => e.stopPropagation()}
            >
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                {editingTask ? "Edit Task" : "Create New Task"}
              </h2>
              <TaskForm
                task={editingTask || undefined}
                onSuccess={handleClose}
                onCancel={handleClose}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
