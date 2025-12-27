/**
 * Chat API Client
 *
 * Provides functions for interacting with the Phase III AI chat API.
 * Handles conversation management and message sending with proper
 * authentication and error handling.
 */

import apiClient from "./api-client";

// ============================================================================
// Type Definitions
// ============================================================================

/**
 * Request payload for sending a chat message
 */
export interface ChatRequest {
  /** Existing conversation ID to resume (omit to start new conversation) */
  conversation_id?: string;
  /** User message content (1-2000 characters) */
  message: string;
}

/**
 * Response from chat API endpoint
 */
export interface ChatResponse {
  /** Conversation ID (new or existing) */
  conversation_id: string;
  /** AI assistant response */
  response: string;
  /** MCP tools invoked (if any) */
  tool_calls?: Record<string, unknown>;
}

/**
 * Conversation metadata
 */
export interface Conversation {
  /** Unique conversation ID */
  id: string;
  /** Optional custom title */
  title?: string | null;
  /** ISO timestamp when conversation was created */
  created_at: string;
  /** ISO timestamp when conversation was last updated */
  updated_at: string;
}

/**
 * Message within a conversation
 */
export interface ConversationMessage {
  /** Unique message ID */
  id: string;
  /** Message sender role */
  role: "user" | "assistant";
  /** Message text content */
  content: string;
  /** ISO timestamp when message was created */
  created_at: string;
  /** AI tool invocations (assistant messages only) */
  tool_calls?: Record<string, unknown>;
}

/**
 * Response from conversation list endpoint
 */
export interface ConversationListResponse {
  /** List of conversations */
  conversations: Conversation[];
}

/**
 * Response from conversation detail endpoint
 */
export interface ConversationDetailResponse {
  /** Conversation ID */
  id: string;
  /** ISO timestamp when conversation was created */
  created_at: string;
  /** ISO timestamp when conversation was last updated */
  updated_at: string;
  /** List of messages in chronological order */
  messages: ConversationMessage[];
}

/**
 * Error response from chat API
 */
export interface ChatError {
  /** HTTP status code */
  status: number;
  /** Error message */
  message: string;
  /** Additional error details */
  detail?: string;
}

// ============================================================================
// API Functions
// ============================================================================

/**
 * Send a message to the AI chat assistant
 *
 * @param userId - The authenticated user's ID
 * @param message - The message to send to the AI
 * @param conversationId - Optional conversation ID to resume existing conversation
 * @returns Promise resolving to the chat response
 * @throws ChatError if the request fails
 *
 * @example
 * ```typescript
 * // Start new conversation
 * const response = await sendChatMessage("user123", "Hello, add a task to buy milk");
 * console.log(response.conversation_id); // "550e8400-e29b-41d4-a716-446655440000"
 * console.log(response.response); // "I've added a task to buy milk..."
 *
 * // Resume existing conversation
 * const nextResponse = await sendChatMessage(
 *   "user123",
 *   "Show me my tasks",
 *   response.conversation_id
 * );
 * ```
 */
export async function sendChatMessage(
  userId: string,
  message: string,
  conversationId?: string,
): Promise<ChatResponse> {
  try {
    const requestBody: ChatRequest = {
      message,
      ...(conversationId && { conversation_id: conversationId }),
    };

    const response = await apiClient.post<ChatResponse>(
      `/${userId}/chat`,
      requestBody,
    );

    return response.data;
  } catch (error: unknown) {
    // Type guard for axios error
    if (error && typeof error === "object" && "response" in error) {
      const axiosError = error as {
        response?: {
          status: number;
          data?: { detail?: string };
        };
      };

      const status = axiosError.response?.status ?? 500;
      const detail = axiosError.response?.data?.detail ?? "Unknown error";

      // Map HTTP status codes to user-friendly messages
      let message: string;
      switch (status) {
        case 401:
          message = "Authentication required. Please sign in again.";
          break;
        case 403:
          if (detail.includes("todo assistant")) {
            message =
              "I can only help with task management. Please ask about your todos.";
          } else if (detail.includes("user_id mismatch")) {
            message =
              "Access denied. You can only access your own conversations.";
          } else {
            message = "Access denied.";
          }
          break;
        case 404:
          message = "Conversation not found. It may have been deleted.";
          break;
        case 429:
          message = "Too many requests. Please wait 30 seconds and try again.";
          break;
        case 500:
          if (detail.includes("Unable to generate valid response")) {
            message =
              "Unable to generate a valid response. Please try rephrasing your message.";
          } else if (detail.includes("High demand")) {
            message = "High demand. Please wait 30 seconds and try again.";
          } else {
            message =
              "An error occurred while processing your request. Please try again.";
          }
          break;
        default:
          message = `Request failed with status ${status}`;
      }

      const chatError: ChatError = {
        status,
        message,
        detail,
      };

      throw chatError;
    }

    // Handle non-axios errors
    throw {
      status: 500,
      message: "An unexpected error occurred",
      detail: error instanceof Error ? error.message : String(error),
    } as ChatError;
  }
}

/**
 * Update conversation (rename)
 *
 * @param userId - The authenticated user's ID
 * @param conversationId - The conversation ID to update
 * @param title - New conversation title
 * @returns Promise resolving to updated conversation data
 * @throws ChatError if the request fails
 *
 * @example
 * ```typescript
 * const updated = await updateConversation(
 *   "user123",
 *   "550e8400-e29b-41d4-a716-446655440000",
 *   "My Important Tasks"
 * );
 * console.log("Renamed to:", updated.title);
 * ```
 */
export async function updateConversation(
  userId: string,
  conversationId: string,
  title: string,
): Promise<Conversation> {
  try {
    const response = await apiClient.patch<Conversation>(
      `/${userId}/conversations/${conversationId}`,
      { title },
    );
    return response.data;
  } catch (error: unknown) {
    if (error && typeof error === "object" && "response" in error) {
      const axiosError = error as {
        response?: {
          status: number;
          data?: { detail?: string };
        };
      };

      const status = axiosError.response?.status ?? 500;
      const detail = axiosError.response?.data?.detail ?? "Unknown error";

      let message: string;
      switch (status) {
        case 401:
          message = "Authentication required. Please sign in again.";
          break;
        case 403:
          message =
            "Access denied. You can only rename your own conversations.";
          break;
        case 404:
          message = "Conversation not found.";
          break;
        default:
          message = "Failed to rename conversation.";
      }

      const chatError: ChatError = {
        status,
        message,
        detail,
      };

      throw chatError;
    }

    throw {
      status: 500,
      message: "An unexpected error occurred",
      detail: error instanceof Error ? error.message : String(error),
    } as ChatError;
  }
}

/**
 * Delete a conversation and all its messages
 *
 * @param userId - The authenticated user's ID
 * @param conversationId - The conversation ID to delete
 * @returns Promise resolving when deletion is complete
 * @throws ChatError if the request fails
 *
 * @example
 * ```typescript
 * await deleteConversation("user123", "550e8400-e29b-41d4-a716-446655440000");
 * console.log("Conversation deleted successfully");
 * ```
 */
export async function deleteConversation(
  userId: string,
  conversationId: string,
): Promise<void> {
  try {
    await apiClient.delete(`/${userId}/conversations/${conversationId}`);
  } catch (error: unknown) {
    if (error && typeof error === "object" && "response" in error) {
      const axiosError = error as {
        response?: {
          status: number;
          data?: { detail?: string };
        };
      };

      const status = axiosError.response?.status ?? 500;
      const detail = axiosError.response?.data?.detail ?? "Unknown error";

      let message: string;
      switch (status) {
        case 401:
          message = "Authentication required. Please sign in again.";
          break;
        case 403:
          message =
            "Access denied. You can only delete your own conversations.";
          break;
        case 404:
          message = "Conversation not found.";
          break;
        default:
          message = "Failed to delete conversation.";
      }

      const chatError: ChatError = {
        status,
        message,
        detail,
      };

      throw chatError;
    }

    throw {
      status: 500,
      message: "An unexpected error occurred",
      detail: error instanceof Error ? error.message : String(error),
    } as ChatError;
  }
}

/**
 * Validate message length before sending
 *
 * @param message - The message to validate
 * @returns true if valid, false otherwise
 *
 * @example
 * ```typescript
 * if (validateMessage(userInput)) {
 *   await sendChatMessage(userId, userInput);
 * } else {
 *   console.error("Message must be between 1 and 2000 characters");
 * }
 * ```
 */
export function validateMessage(message: string): boolean {
  return message.length >= 1 && message.length <= 2000;
}

/**
 * Get user-friendly error message from ChatError
 *
 * @param error - The ChatError object
 * @returns User-friendly error message
 *
 * @example
 * ```typescript
 * try {
 *   await sendChatMessage(userId, message);
 * } catch (error) {
 *   const errorMessage = getErrorMessage(error as ChatError);
 *   showNotification(errorMessage, "error");
 * }
 * ```
 */
export function getErrorMessage(error: ChatError): string {
  return error.message;
}

/**
 * Get list of user's conversations
 *
 * @param userId - The authenticated user's ID
 * @returns Promise resolving to list of conversations (sorted by most recent)
 * @throws ChatError if the request fails
 *
 * @example
 * ```typescript
 * const { conversations } = await getConversations("user123");
 * conversations.forEach(conv => {
 *   console.log(`Conversation ${conv.id} updated at ${conv.updated_at}`);
 * });
 * ```
 */
export async function getConversations(
  userId: string,
): Promise<ConversationListResponse> {
  try {
    const response = await apiClient.get<ConversationListResponse>(
      `/${userId}/conversations`,
    );
    return response.data;
  } catch (error: unknown) {
    if (error && typeof error === "object" && "response" in error) {
      const axiosError = error as {
        response?: {
          status: number;
          data?: { detail?: string };
        };
      };

      const status = axiosError.response?.status ?? 500;
      const detail = axiosError.response?.data?.detail ?? "Unknown error";

      const chatError: ChatError = {
        status,
        message:
          status === 401
            ? "Authentication required. Please sign in again."
            : "Failed to load conversation history.",
        detail,
      };

      throw chatError;
    }

    throw {
      status: 500,
      message: "An unexpected error occurred",
      detail: error instanceof Error ? error.message : String(error),
    } as ChatError;
  }
}

/**
 * Get specific conversation with messages
 *
 * @param userId - The authenticated user's ID
 * @param conversationId - The conversation ID to retrieve
 * @param limit - Maximum number of messages to return (default: 50, max: 100)
 * @param offset - Number of messages to skip (default: 0)
 * @returns Promise resolving to conversation with messages
 * @throws ChatError if the request fails
 *
 * @example
 * ```typescript
 * const conversation = await getConversationById(
 *   "user123",
 *   "550e8400-e29b-41d4-a716-446655440000"
 * );
 * console.log(`Loaded ${conversation.messages.length} messages`);
 * ```
 */
export async function getConversationById(
  userId: string,
  conversationId: string,
  limit: number = 50,
  offset: number = 0,
): Promise<ConversationDetailResponse> {
  try {
    const response = await apiClient.get<ConversationDetailResponse>(
      `/${userId}/conversations/${conversationId}`,
      {
        params: { limit, offset },
      },
    );
    return response.data;
  } catch (error: unknown) {
    if (error && typeof error === "object" && "response" in error) {
      const axiosError = error as {
        response?: {
          status: number;
          data?: { detail?: string };
        };
      };

      const status = axiosError.response?.status ?? 500;
      const detail = axiosError.response?.data?.detail ?? "Unknown error";

      let message: string;
      switch (status) {
        case 401:
          message = "Authentication required. Please sign in again.";
          break;
        case 403:
          message =
            "Access denied. You can only access your own conversations.";
          break;
        case 404:
          message = "Conversation not found.";
          break;
        default:
          message = "Failed to load conversation.";
      }

      const chatError: ChatError = {
        status,
        message,
        detail,
      };

      throw chatError;
    }

    throw {
      status: 500,
      message: "An unexpected error occurred",
      detail: error instanceof Error ? error.message : String(error),
    } as ChatError;
  }
}
