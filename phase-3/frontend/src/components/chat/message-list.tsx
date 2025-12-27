"use client";

import { useEffect, useRef } from "react";
import { MessageContent } from "./message-content";

// ============================================================================
// Type Definitions
// ============================================================================

/**
 * Represents a single chat message
 */
export interface Message {
  /** Unique message identifier */
  id: string;
  /** Message role: 'user' or 'assistant' */
  role: "user" | "assistant";
  /** Message content/text */
  content: string;
  /** Timestamp when message was created */
  timestamp: Date;
}

/**
 * Props for MessageList component
 */
export interface MessageListProps {
  /** Array of messages to display */
  messages: Message[];
  /** Whether messages are currently loading */
  isLoading?: boolean;
  /** Custom CSS class name */
  className?: string;
}

// ============================================================================
// MessageList Component
// ============================================================================

/**
 * MessageList Component
 *
 * Displays a scrollable list of chat messages with automatic scroll to bottom.
 * Supports both user and assistant messages with distinct styling.
 *
 * Features:
 * - Auto-scroll to latest message
 * - Distinct styling for user vs assistant messages
 * - Loading indicator support
 * - Timestamp display
 * - Responsive layout
 *
 * @example
 * ```tsx
 * const messages = [
 *   { id: '1', role: 'user', content: 'Hello', timestamp: new Date() },
 *   { id: '2', role: 'assistant', content: 'Hi there!', timestamp: new Date() }
 * ];
 *
 * <MessageList messages={messages} isLoading={false} />
 * ```
 */
export function MessageList({
  messages,
  isLoading = false,
  className = "",
}: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  /**
   * Format timestamp to user-friendly time string
   */
  const formatTime = (date: Date): string => {
    return new Intl.DateTimeFormat("en-US", {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    }).format(date);
  };

  return (
    <div
      ref={containerRef}
      className={`flex-1 overflow-y-auto px-4 py-6 space-y-4 ${className}`}
    >
      {messages.length === 0 && !isLoading ? (
        <div className="flex flex-col items-center justify-center h-full text-center">
          <div className="max-w-md space-y-3">
            <div className="text-4xl">💬</div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Start a conversation
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Ask me to add, view, update, or complete your tasks. I'm here to
              help manage your todos through natural conversation!
            </p>
            <div className="mt-4 space-y-2 text-left">
              <p className="text-xs text-gray-500 dark:text-gray-500">
                Try saying:
              </p>
              <ul className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                <li>• "Add a task to buy groceries"</li>
                <li>• "Show me my pending tasks"</li>
                <li>• "Mark task 3 as complete"</li>
                <li>• "Update my meeting task"</li>
              </ul>
            </div>
          </div>
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-3 ${
                  message.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 border border-gray-200 dark:border-gray-700"
                }`}
              >
                {/* Message Content */}
                <MessageContent content={message.content} role={message.role} />

                {/* Timestamp */}
                <div
                  className={`mt-2 text-xs ${
                    message.role === "user"
                      ? "text-blue-100"
                      : "text-gray-500 dark:text-gray-400"
                  }`}
                >
                  {formatTime(message.timestamp)}
                </div>
              </div>
            </div>
          ))}

          {/* Loading Indicator */}
          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-[80%] rounded-lg px-4 py-3 bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                <div className="flex items-center space-x-2">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div
                      className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.1s" }}
                    ></div>
                    <div
                      className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.2s" }}
                    ></div>
                  </div>
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    Thinking...
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Scroll anchor */}
          <div ref={messagesEndRef} />
        </>
      )}
    </div>
  );
}
