"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/use-auth";
import { ChatInterface } from "@/components/chat/chat-interface";
import { ConversationSidebar } from "@/components/chat/conversation-sidebar";
import { Header } from "@/components/layout/header";

/**
 * Chat page with AI assistant for natural language task management
 *
 * Features:
 * - Protected route (requires authentication)
 * - Full-height chat interface
 * - Integration with OpenAI ChatKit
 * - Natural language task management via AI agent
 * - MCP tools for database operations
 *
 * User Stories:
 * - US1: Start new conversation with AI assistant
 * - US2: Add tasks via natural language
 * - US3: View tasks via chat
 * - US4: Complete tasks via chat
 * - US5: Update tasks via chat
 * - US6: Delete tasks via chat
 *
 * @implements T051 - Create chat page with ChatKit integration
 * @implements T052 - Add protected route authentication to chat page
 */
export default function ChatPage() {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();
  const [selectedConversationId, setSelectedConversationId] = useState<
    string | undefined
  >();

  // Redirect to signin if not authenticated (after loading completes)
  useEffect(() => {
    if (!authLoading && !user) {
      console.log("User not authenticated, redirecting to signin...");
      router.replace("/auth/signin?callbackUrl=/chat");
    }
  }, [authLoading, user, router]);

  /**
   * Handle selecting a conversation from sidebar
   */
  const handleSelectConversation = (conversationId: string) => {
    setSelectedConversationId(conversationId);
  };

  /**
   * Handle starting a new conversation
   */
  const handleNewConversation = () => {
    setSelectedConversationId(undefined);
  };

  /**
   * Handle conversation ID changes from ChatInterface
   */
  const handleConversationChange = (conversationId: string) => {
    setSelectedConversationId(conversationId);
  };

  // Render loading state
  if (authLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Header user={null} />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-center h-64">
            <div className="text-gray-600 dark:text-gray-400">
              Loading authentication...
            </div>
          </div>
        </main>
      </div>
    );
  }

  // Render unauthenticated state
  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Header user={null} />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-center h-64">
            <div className="text-gray-600 dark:text-gray-400">
              Please sign in to continue
            </div>
          </div>
        </main>
      </div>
    );
  }

  // Render authenticated chat interface
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col">
      <Header user={user} />

      <main className="flex-1 w-full mx-auto">
        <div className="px-4 sm:px-6 lg:px-8 py-6 max-w-7xl mx-auto">
          <div className="mb-4">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              AI Task Assistant
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              Manage your tasks naturally with AI-powered chat
            </p>
          </div>
        </div>

        {/* Chat Interface with Sidebar - Full height container */}
        <div className="h-[calc(100vh-14rem)] px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm h-full flex overflow-hidden">
            {/* Conversation History Sidebar */}
            <ConversationSidebar
              activeConversationId={selectedConversationId}
              onSelectConversation={handleSelectConversation}
              onNewConversation={handleNewConversation}
            />

            {/* Chat Interface */}
            <div className="flex-1 overflow-hidden">
              <ChatInterface
                initialConversationId={selectedConversationId}
                onConversationChange={handleConversationChange}
                className="h-full"
              />
            </div>
          </div>
        </div>

        {/* Helper text */}
        <div className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto mt-4 text-sm text-gray-500 dark:text-gray-400">
          <p className="font-medium mb-2">Try asking:</p>
          <ul className="list-disc list-inside space-y-1">
            <li>&quot;Add task to buy groceries&quot;</li>
            <li>&quot;Show me my pending tasks&quot;</li>
            <li>&quot;Mark task 3 as complete&quot;</li>
            <li>&quot;Update task 1 to call mom&quot;</li>
            <li>&quot;Delete the meeting task&quot;</li>
          </ul>
        </div>
      </main>
    </div>
  );
}
