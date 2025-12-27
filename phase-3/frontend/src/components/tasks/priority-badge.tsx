import { Priority } from "@/types/task";

interface PriorityBadgeProps {
  priority: Priority;
}

/**
 * Badge component for displaying task priority
 * Color-coded: High (red), Medium (yellow), Low (green) (T079)
 */
export function PriorityBadge({ priority }: PriorityBadgeProps) {
  const colors = {
    [Priority.HIGH]: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400",
    [Priority.MEDIUM]: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400",
    [Priority.LOW]: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
  };

  const labels = {
    [Priority.HIGH]: "High",
    [Priority.MEDIUM]: "Medium",
    [Priority.LOW]: "Low",
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colors[priority]}`}
    >
      {labels[priority]}
    </span>
  );
}
