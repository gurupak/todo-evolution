"use client";

import { useState, useEffect } from "react";
import { Priority, Task } from "@/types/task";
import { useCreateTask, useUpdateTask } from "@/hooks/use-tasks";
import { toast } from "sonner";
import DatePickerWithPresets from "@/components/DatePickerWithPresets";

interface TaskFormProps {
  task?: Task;
  onSuccess?: () => void;
  onCancel?: () => void;
}

/**
 * Task form component with validation
 * Supports both creating and editing tasks (T084)
 */
export function TaskForm({ task, onSuccess, onCancel }: TaskFormProps) {
  const [title, setTitle] = useState(task?.title || "");
  const [description, setDescription] = useState(task?.description || "");
  const [priority, setPriority] = useState<Priority>(
    task?.priority || Priority.MEDIUM,
  );
  const [targetCompletionDate, setTargetCompletionDate] = useState<Date | null>(
    task?.target_completion_date ? new Date(task.target_completion_date) : null,
  );
  const [errors, setErrors] = useState<Record<string, string>>({});

  const createTask = useCreateTask();
  const updateTask = useUpdateTask();

  const isEditing = !!task;
  const mutation = isEditing ? updateTask : createTask;

  // Update form state when task prop changes (for editing)
  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description);
      setPriority(task.priority);
      setTargetCompletionDate(
        task.target_completion_date
          ? new Date(task.target_completion_date)
          : null,
      );
    } else {
      // Reset form for new task
      setTitle("");
      setDescription("");
      setPriority(Priority.MEDIUM);
      setTargetCompletionDate(null);
    }
  }, [task]);

  const validate = () => {
    const newErrors: Record<string, string> = {};

    if (!title.trim()) {
      newErrors.title = "Title is required";
    } else if (title.trim().length > 200) {
      newErrors.title = "Title must be 200 characters or less";
    }

    if (description.length > 1000) {
      newErrors.description = "Description must be 1000 characters or less";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    try {
      if (isEditing) {
        await updateTask.mutateAsync({
          taskId: task.id,
          data: {
            title: title.trim(),
            description: description.trim(),
            priority,
            target_completion_date: targetCompletionDate?.toISOString() || null,
          },
        });
        toast.success("Task updated successfully");
      } else {
        await createTask.mutateAsync({
          title: title.trim(),
          description: description.trim(),
          priority,
          target_completion_date: targetCompletionDate?.toISOString() || null,
        });
        toast.success("Task created successfully");
      }

      onSuccess?.();
    } catch (error: any) {
      const message = error.response?.data?.detail || "Failed to save task";
      toast.error(message);
    }
  };

  const handleTitleChange = (value: string) => {
    setTitle(value);
    if (errors.title) {
      setErrors((prev) => ({ ...prev, title: "" }));
    }
  };

  const handleDescriptionChange = (value: string) => {
    setDescription(value);
    if (errors.description) {
      setErrors((prev) => ({ ...prev, description: "" }));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label
          htmlFor="title"
          className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
        >
          Title *
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => handleTitleChange(e.target.value)}
          className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white ${
            errors.title
              ? "border-red-500 dark:border-red-500"
              : "border-gray-300 dark:border-gray-600"
          }`}
          placeholder="Enter task title"
          disabled={mutation.isPending}
        />
        {errors.title && (
          <p className="mt-1 text-sm text-red-600 dark:text-red-400">
            {errors.title}
          </p>
        )}
      </div>

      <div>
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
        >
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => handleDescriptionChange(e.target.value)}
          rows={3}
          className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white ${
            errors.description
              ? "border-red-500 dark:border-red-500"
              : "border-gray-300 dark:border-gray-600"
          }`}
          placeholder="Enter task description (optional)"
          disabled={mutation.isPending}
        />
        {errors.description && (
          <p className="mt-1 text-sm text-red-600 dark:text-red-400">
            {errors.description}
          </p>
        )}
      </div>

      <div>
        <label
          htmlFor="priority"
          className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
        >
          Priority
        </label>
        <select
          id="priority"
          value={priority}
          onChange={(e) => setPriority(e.target.value as Priority)}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
          disabled={mutation.isPending}
        >
          <option value={Priority.LOW}>Low</option>
          <option value={Priority.MEDIUM}>Medium</option>
          <option value={Priority.HIGH}>High</option>
        </select>
      </div>

      <DatePickerWithPresets
        selected={targetCompletionDate}
        onChange={setTargetCompletionDate}
      />

      <div className="flex gap-3 justify-end">
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={mutation.isPending}
            className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
          >
            Cancel
          </button>
        )}
        <button
          type="submit"
          disabled={mutation.isPending}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {mutation.isPending
            ? "Saving..."
            : isEditing
              ? "Update Task"
              : "Create Task"}
        </button>
      </div>
    </form>
  );
}
