"use client";

import { useState, useCallback, FormEvent, useEffect } from "react";
import { MessageList, Message } from "./message-list";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/hooks/use-auth";
import {
  sendChatMessage,
  validateMessage,
  getErrorMessage,
  ChatError,
  getConversationById,
} from "@/lib/chat-api";
import { toast } from "sonner";

// ============================================================================
// Type Definitions
// ============================================================================

/**
 * Props for ChatInterface component
 */
export interface ChatInterfaceProps {
  /** Optional initial conversation ID to resume */
  initialConversationId?: string;
  /** Custom CSS class name */
  className?: string;
  /** Callback when conversation ID changes (for sidebar sync) */
  onConversationChange?: (conversationId: string) => void;
}

// ============================================================================
// ChatInterface Component
// ============================================================================

/**
 * ChatInterface Component
 *
 * Main chat interface that combines message list and input.
 * Handles message sending, conversation management, and error handling.
 *
 * Features:
 * - Message input with validation (1-2000 characters)
 * - Send button with loading state
 * - Automatic conversation creation
 * - Error handling with user-friendly messages
 * - Authentication integration
 * - Toast notifications for errors
 *
 * @example
 * ```tsx
 * // Start new conversation
 * <ChatInterface />
 *
 * // Resume existing conversation
 * <ChatInterface initialConversationId="550e8400-e29b-41d4-a716-446655440000" />
 * ```
 */
export function ChatInterface({
  initialConversationId,
  className = "",
  onConversationChange,
}: ChatInterfaceProps) {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>(
    initialConversationId,
  );
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);

  /**
   * Load existing conversation when initialConversationId changes
   */
  useEffect(() => {
    async function loadConversation() {
      if (!initialConversationId || !user?.id) {
        // Clear messages if no conversation selected
        if (!initialConversationId) {
          setMessages([]);
          setConversationId(undefined);
        }
        return;
      }

      try {
        setIsLoadingHistory(true);
        const conversation = await getConversationById(
          user.id,
          initialConversationId,
        );

        // Convert API messages to UI message format
        const loadedMessages: Message[] = conversation.messages.map((msg) => ({
          id: msg.id,
          role: msg.role,
          content: msg.content,
          timestamp: new Date(msg.created_at),
        }));

        setMessages(loadedMessages);
        setConversationId(initialConversationId);
      } catch (error) {
        const chatError = error as ChatError;
        toast.error(chatError.message);
        setMessages([]);
        setConversationId(undefined);
      } finally {
        setIsLoadingHistory(false);
      }
    }

    loadConversation();
  }, [initialConversationId, user?.id]);

  /**
   * Handle predefined message click
   */
  const handlePredefinedMessage = useCallback((message: string) => {
    setInputMessage(message);
  }, []);

  /**
   * Handle sending a message to the AI assistant
   */
  const handleSendMessage = useCallback(
    async (e: FormEvent) => {
      e.preventDefault();

      // Validate message
      if (!inputMessage.trim()) {
        toast.error("Please enter a message");
        return;
      }

      if (!validateMessage(inputMessage)) {
        toast.error("Message must be between 1 and 2000 characters");
        return;
      }

      // Validate authentication
      if (!user?.id) {
        toast.error("You must be signed in to chat");
        return;
      }

      // Add user message to UI immediately
      const userMessage: Message = {
        id: `temp-user-${Date.now()}`,
        role: "user",
        content: inputMessage,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setInputMessage("");
      setIsLoading(true);

      try {
        // Send message to API
        const response = await sendChatMessage(
          user.id,
          inputMessage,
          conversationId,
        );

        // Update conversation ID if this is a new conversation
        if (!conversationId) {
          setConversationId(response.conversation_id);
          // Notify parent component of new conversation
          if (onConversationChange) {
            onConversationChange(response.conversation_id);
          }
        }

        // Add assistant response to UI
        const assistantMessage: Message = {
          id: `assistant-${Date.now()}`,
          role: "assistant",
          content: response.response,
          timestamp: new Date(),
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch (error) {
        // Remove the optimistic user message on error
        setMessages((prev) => prev.filter((msg) => msg.id !== userMessage.id));

        // Show user-friendly error message
        const chatError = error as ChatError;
        const errorMessage = getErrorMessage(chatError);
        toast.error(errorMessage);

        // Restore input on error
        setInputMessage(userMessage.content);

        // Special handling for authentication errors
        if (chatError.status === 401) {
          // User should be redirected to login
          console.error("Authentication error:", chatError);
        }
      } finally {
        setIsLoading(false);
      }
    },
    [inputMessage, user, conversationId],
  );

  /**
   * Handle input change with character limit
   */
  const handleInputChange = useCallback((value: string) => {
    // Enforce max length on input
    if (value.length <= 2000) {
      setInputMessage(value);
    } else {
      toast.error("Message cannot exceed 2000 characters");
    }
  }, []);

  return (
    <div
      className={`flex flex-col h-full bg-white dark:bg-gray-900 ${className}`}
    >
      {/* Messages Container */}
      <MessageList
        messages={messages}
        isLoading={isLoading || isLoadingHistory}
      />

      {/* Input Area */}
      <div className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
        {/* Predefined Messages */}
        <div className="px-4 pt-3 pb-2 flex flex-wrap gap-2">
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => handlePredefinedMessage("Show me all my tasks")}
            disabled={isLoading}
            className="text-xs"
          >
            📋 Show all tasks
          </Button>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => handlePredefinedMessage("List my pending tasks")}
            disabled={isLoading}
            className="text-xs"
          >
            ⏳ Pending tasks
          </Button>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => handlePredefinedMessage("Show completed tasks")}
            disabled={isLoading}
            className="text-xs"
          >
            ✅ Completed tasks
          </Button>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => handlePredefinedMessage("Show high priority tasks")}
            disabled={isLoading}
            className="text-xs"
          >
            �� High priority
          </Button>
        </div>

        <form onSubmit={handleSendMessage} className="p-4 pt-0">
          <div className="flex gap-2">
            {/* Message Input */}
            <Input
              type="text"
              value={inputMessage}
              onChange={(e) => handleInputChange(e.target.value)}
              placeholder="Ask me to add, view, or update tasks..."
              disabled={isLoading}
              className="flex-1"
              aria-label="Chat message input"
              maxLength={2000}
            />

            {/* Send Button */}
            <Button
              type="submit"
              disabled={isLoading || !inputMessage.trim()}
              className="px-6"
              aria-label="Send message"
            >
              {isLoading ? (
                <span className="flex items-center gap-2">
                  <svg
                    className="animate-spin h-4 w-4"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Sending...
                </span>
              ) : (
                "Send"
              )}
            </Button>
          </div>

          {/* Character Counter */}
          <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 text-right">
            {inputMessage.length} / 2000
          </div>
        </form>
      </div>
    </div>
  );
}
