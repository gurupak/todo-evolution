"use client";

import { TaskList, Task } from "./task-card";

export interface MessageContentProps {
  content: string;
  role: "user" | "assistant";
}

/**
 * Parse message content and extract task JSON blocks
 */
function parseTasksFromMessage(content: string): {
  tasks: Task[] | null;
  textContent: string;
} {
  // Look for JSON code blocks with tasks
  const jsonBlockRegex = /```json\s*(\{[\s\S]*?"tasks"[\s\S]*?\})\s*```/;
  const match = content.match(jsonBlockRegex);

  if (!match) {
    return { tasks: null, textContent: content };
  }

  try {
    const jsonData = JSON.parse(match[1]);
    if (jsonData.tasks && Array.isArray(jsonData.tasks)) {
      // Remove the JSON block from text content
      const textContent = content.replace(jsonBlockRegex, "").trim();
      return { tasks: jsonData.tasks, textContent };
    }
  } catch (e) {
    // JSON parsing failed, return original content
    console.error("Failed to parse tasks JSON:", e);
  }

  return { tasks: null, textContent: content };
}

/**
 * MessageContent Component
 * 
 * Renders message content with special handling for task lists.
 * Detects JSON task blocks and renders them as interactive cards.
 */
export function MessageContent({ content, role }: MessageContentProps) {
  const { tasks, textContent } = parseTasksFromMessage(content);

  return (
    <div className="space-y-4">
      {/* Regular text content */}
      {textContent && (
        <div className="prose prose-sm dark:prose-invert max-w-none">
          <p className="whitespace-pre-wrap">{textContent}</p>
        </div>
      )}

      {/* Task cards if detected */}
      {tasks && tasks.length > 0 && (
        <div className="mt-4">
          <TaskList tasks={tasks} />
        </div>
      )}
    </div>
  );
}
