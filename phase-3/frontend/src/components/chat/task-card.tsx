"use client";

import { CheckCircle2, Clock, AlertCircle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

// ============================================================================
// Type Definitions
// ============================================================================

export interface Task {
  id: string;
  title: string;
  description?: string;
  priority: "HIGH" | "MEDIUM" | "LOW";
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCardProps {
  task: Task;
  index: number;
}

// ============================================================================
// Priority Colors & Icons
// ============================================================================

const priorityConfig = {
  HIGH: {
    badge: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
    card: "border-l-4 border-l-red-500",
    icon: AlertCircle,
  },
  MEDIUM: {
    badge:
      "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
    card: "border-l-4 border-l-yellow-500",
    icon: Clock,
  },
  LOW: {
    badge: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
    card: "border-l-4 border-l-blue-500",
    icon: Clock,
  },
};

const completedConfig = {
  card: "border-l-4 border-l-green-500 bg-green-50 dark:bg-green-950",
  badge: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200",
};

// ============================================================================
// TaskCard Component
// ============================================================================

export function TaskCard({ task, index }: TaskCardProps) {
  // Normalize priority (handle both "HIGH" and "PriorityEnum.HIGH" formats)
  const normalizedPriority = task.priority
    ?.toString()
    .replace(/PriorityEnum\./gi, "")
    .toUpperCase() as "HIGH" | "MEDIUM" | "LOW";
  const priority =
    normalizedPriority in priorityConfig ? normalizedPriority : "MEDIUM";

  const config = task.is_completed ? completedConfig : priorityConfig[priority];
  const PriorityIcon = task.is_completed
    ? CheckCircle2
    : priorityConfig[priority].icon;

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.RelativeTimeFormat("en", { numeric: "auto" }).format(
      Math.ceil((date.getTime() - Date.now()) / (1000 * 60 * 60 * 24)),
      "day",
    );
  };

  return (
    <Card
      className={cn(
        "transition-all hover:shadow-md",
        config.card,
        task.is_completed && "opacity-75",
      )}
    >
      <CardContent className="p-4">
        <div className="flex items-start gap-3">
          {/* Icon */}
          <div className="mt-0.5">
            <PriorityIcon
              className={cn(
                "h-5 w-5",
                task.is_completed
                  ? "text-green-600 dark:text-green-400"
                  : priority === "HIGH"
                    ? "text-red-600 dark:text-red-400"
                    : priority === "MEDIUM"
                      ? "text-yellow-600 dark:text-yellow-400"
                      : "text-blue-600 dark:text-blue-400",
              )}
            />
          </div>

          {/* Content */}
          <div className="flex-1 space-y-2">
            {/* Title & Priority Badge */}
            <div className="flex items-start justify-between gap-2">
              <h4
                className={cn(
                  "font-semibold text-sm",
                  task.is_completed && "line-through text-muted-foreground",
                )}
              >
                {index}. {task.title}
              </h4>
              <Badge
                variant="secondary"
                className={cn(
                  "text-xs font-medium shrink-0",
                  task.is_completed ? completedConfig.badge : config.badge,
                )}
              >
                {task.is_completed ? "Completed" : priority}
              </Badge>
            </div>

            {/* Description */}
            {task.description && (
              <p className="text-sm text-muted-foreground">
                {task.description}
              </p>
            )}

            {/* Metadata */}
            <div className="flex items-center gap-3 text-xs text-muted-foreground">
              <span>Created {formatDate(task.created_at)}</span>
              {task.updated_at !== task.created_at && (
                <span>• Updated {formatDate(task.updated_at)}</span>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

// ============================================================================
// TaskList Component
// ============================================================================

export interface TaskListProps {
  tasks: Task[];
}

export function TaskList({ tasks }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <p>No tasks found. Start by adding a new task!</p>
      </div>
    );
  }

  // Sort: incomplete first, then by priority (HIGH > MEDIUM > LOW)
  const sortedTasks = [...tasks].sort((a, b) => {
    if (a.is_completed !== b.is_completed) {
      return a.is_completed ? 1 : -1;
    }
    const priorityOrder = { HIGH: 0, MEDIUM: 1, LOW: 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Your Tasks</h3>
        <div className="text-sm text-muted-foreground">
          {tasks.filter((t) => !t.is_completed).length} pending,{" "}
          {tasks.filter((t) => t.is_completed).length} completed
        </div>
      </div>
      {sortedTasks.map((task, index) => (
        <TaskCard key={task.id} task={task} index={index + 1} />
      ))}
    </div>
  );
}
