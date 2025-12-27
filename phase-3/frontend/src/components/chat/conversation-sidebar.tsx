"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/hooks/use-auth";
import {
  getConversations,
  Conversation,
  ChatError,
  deleteConversation,
  updateConversation,
} from "@/lib/chat-api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  MessageSquare,
  Plus,
  Loader2,
  MoreVertical,
  Trash2,
  ExternalLink,
  Edit2,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

// ============================================================================
// Type Definitions
// ============================================================================

/**
 * Props for ConversationSidebar component
 */
export interface ConversationSidebarProps {
  /** Currently active conversation ID */
  activeConversationId?: string;
  /** Callback when user selects a conversation */
  onSelectConversation: (conversationId: string) => void;
  /** Callback when user starts a new conversation */
  onNewConversation: () => void;
  /** Custom CSS class name */
  className?: string;
}

// ============================================================================
// ConversationSidebar Component
// ============================================================================

/**
 * ConversationSidebar Component
 *
 * Displays list of user's conversation history in a sidebar.
 * Allows users to view, select, and resume previous conversations.
 *
 * Features:
 * - Fetches conversation list on mount and user change
 * - Displays conversations sorted by most recent first
 * - Highlights currently active conversation
 * - "New Chat" button to start fresh conversation
 * - Loading state while fetching data
 * - Error handling with toast notifications
 * - Formats timestamps in user-friendly format
 *
 * @example
 * ```tsx
 * <ConversationSidebar
 *   activeConversationId={currentConversationId}
 *   onSelectConversation={(id) => loadConversation(id)}
 *   onNewConversation={() => startNewChat()}
 * />
 * ```
 */
export function ConversationSidebar({
  activeConversationId,
  onSelectConversation,
  onNewConversation,
  className = "",
}: ConversationSidebarProps) {
  const { user } = useAuth();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [conversationToDelete, setConversationToDelete] = useState<
    string | null
  >(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [renameDialogOpen, setRenameDialogOpen] = useState(false);
  const [conversationToRename, setConversationToRename] = useState<
    string | null
  >(null);
  const [newTitle, setNewTitle] = useState("");
  const [isRenaming, setIsRenaming] = useState(false);

  /**
   * Fetch conversation list from API
   */
  useEffect(() => {
    async function fetchConversations() {
      if (!user?.id) {
        setIsLoading(false);
        return;
      }

      try {
        setIsLoading(true);
        const response = await getConversations(user.id);
        setConversations(response.conversations);
      } catch (error) {
        const chatError = error as ChatError;
        toast.error(chatError.message);
        setConversations([]);
      } finally {
        setIsLoading(false);
      }
    }

    fetchConversations();
  }, [user?.id]);

  /**
   * Format timestamp to relative time (e.g., "2 hours ago", "Yesterday")
   */
  function formatTimestamp(isoString: string): string {
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays}d ago`;

    // Format as date for older conversations
    return date.toLocaleDateString(undefined, {
      month: "short",
      day: "numeric",
    });
  }

  /**
   * Refresh conversation list (called after sending new message)
   */
  const refreshConversations = async () => {
    if (!user?.id) return;

    try {
      const response = await getConversations(user.id);
      setConversations(response.conversations);
    } catch (error) {
      // Silent fail on refresh
      console.error("Failed to refresh conversations:", error);
    }
  };

  // Expose refresh function to parent (optional)
  useEffect(() => {
    if (activeConversationId && conversations.length > 0) {
      // Refresh when active conversation changes
      refreshConversations();
    }
  }, [activeConversationId]);

  /**
   * Handle rename conversation click
   */
  const handleRenameClick = (
    conversationId: string,
    currentTitle: string | null,
    e: React.MouseEvent,
  ) => {
    e.stopPropagation();
    setConversationToRename(conversationId);
    setNewTitle(currentTitle || "");
    setRenameDialogOpen(true);
  };

  /**
   * Perform conversation rename
   */
  const handleRenameConfirm = async () => {
    if (!conversationToRename || !user?.id || !newTitle.trim()) return;

    try {
      setIsRenaming(true);
      const updated = await updateConversation(
        user.id,
        conversationToRename,
        newTitle.trim(),
      );

      // Update local state
      setConversations((prev) =>
        prev.map((conv) =>
          conv.id === conversationToRename
            ? { ...conv, title: updated.title }
            : conv,
        ),
      );

      toast.success("Conversation renamed successfully");
      setRenameDialogOpen(false);
    } catch (error) {
      const chatError = error as ChatError;
      toast.error(chatError.message);
    } finally {
      setIsRenaming(false);
      setConversationToRename(null);
      setNewTitle("");
    }
  };

  /**
   * Handle delete conversation confirmation
   */
  const handleDeleteClick = (conversationId: string, e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent conversation selection
    setConversationToDelete(conversationId);
    setDeleteDialogOpen(true);
  };

  /**
   * Perform conversation deletion
   */
  const handleDeleteConfirm = async () => {
    if (!conversationToDelete || !user?.id) return;

    try {
      setDeletingId(conversationToDelete);
      await deleteConversation(user.id, conversationToDelete);

      // Remove from local state
      setConversations((prev) =>
        prev.filter((conv) => conv.id !== conversationToDelete),
      );

      // If deleted conversation was active, start new conversation
      if (conversationToDelete === activeConversationId) {
        onNewConversation();
      }

      toast.success("Conversation deleted successfully");
      setDeleteDialogOpen(false);
    } catch (error) {
      const chatError = error as ChatError;
      toast.error(chatError.message);
    } finally {
      setDeletingId(null);
      setConversationToDelete(null);
    }
  };

  return (
    <div
      className={cn(
        "flex h-full w-64 flex-col border-r bg-muted/30",
        className,
      )}
    >
      {/* Header */}
      <div className="border-b p-4">
        <Button
          onClick={onNewConversation}
          className="w-full"
          variant="default"
          size="sm"
        >
          <Plus className="mr-2 h-4 w-4" />
          New Chat
        </Button>
      </div>

      {/* Conversation List */}
      <ScrollArea className="flex-1">
        {isLoading ? (
          <div className="flex items-center justify-center p-8">
            <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
          </div>
        ) : conversations.length === 0 ? (
          <div className="p-4 text-center text-sm text-muted-foreground">
            <MessageSquare className="mx-auto mb-2 h-8 w-8 opacity-50" />
            <p>No conversations yet</p>
            <p className="mt-1 text-xs">Start chatting to create history</p>
          </div>
        ) : (
          <div className="space-y-1 p-2">
            {conversations.map((conversation) => {
              const isActive = conversation.id === activeConversationId;

              return (
                <div
                  key={conversation.id}
                  className={cn(
                    "group relative w-full rounded-lg transition-colors",
                    "hover:bg-muted",
                    isActive && "bg-muted",
                  )}
                >
                  <div className="flex items-start justify-between p-3">
                    {/* Clickable conversation area */}
                    <button
                      onClick={() => onSelectConversation(conversation.id)}
                      className="flex items-center space-x-2 flex-1 min-w-0 pr-2 text-left"
                    >
                      {deletingId === conversation.id ? (
                        <Loader2 className="h-4 w-4 flex-shrink-0 animate-spin text-muted-foreground" />
                      ) : (
                        <MessageSquare className="h-4 w-4 flex-shrink-0 text-muted-foreground" />
                      )}
                      <div className="min-w-0 flex-1">
                        <p
                          className={cn(
                            "truncate text-sm",
                            isActive && "font-medium",
                          )}
                        >
                          {conversation.title || "Conversation"}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {formatTimestamp(conversation.updated_at)}
                        </p>
                      </div>
                    </button>

                    {/* Three-dot menu */}
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-8 w-8 p-0 opacity-0 group-hover:opacity-100 focus:opacity-100"
                          onClick={(e) => e.stopPropagation()}
                          disabled={deletingId === conversation.id}
                        >
                          <MoreVertical className="h-4 w-4" />
                          <span className="sr-only">Open menu</span>
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem
                          onClick={() => onSelectConversation(conversation.id)}
                        >
                          <ExternalLink className="mr-2 h-4 w-4" />
                          Open history
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          onClick={(e) =>
                            handleRenameClick(
                              conversation.id,
                              conversation.title ?? null,
                              e,
                            )
                          }
                        >
                          <Edit2 className="mr-2 h-4 w-4" />
                          Rename
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          onClick={(e) => handleDeleteClick(conversation.id, e)}
                          className="text-destructive focus:text-destructive"
                        >
                          <Trash2 className="mr-2 h-4 w-4" />
                          Delete history
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </ScrollArea>

      {/* Footer Info */}
      <div className="border-t p-3 text-center text-xs text-muted-foreground">
        {conversations.length > 0 && (
          <p>
            {conversations.length} conversation
            {conversations.length !== 1 ? "s" : ""}
          </p>
        )}
      </div>

      {/* Rename Dialog */}
      <Dialog open={renameDialogOpen} onOpenChange={setRenameDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Rename conversation</DialogTitle>
            <DialogDescription>
              Enter a new name for this conversation to help identify it later.
            </DialogDescription>
          </DialogHeader>
          <div className="py-4">
            <Input
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="Conversation title"
              maxLength={200}
              disabled={isRenaming}
              onKeyDown={(e) => {
                if (e.key === "Enter" && newTitle.trim()) {
                  handleRenameConfirm();
                }
              }}
            />
          </div>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => {
                setRenameDialogOpen(false);
                setConversationToRename(null);
                setNewTitle("");
              }}
              disabled={isRenaming}
            >
              Cancel
            </Button>
            <Button
              onClick={handleRenameConfirm}
              disabled={!newTitle.trim() || isRenaming}
            >
              {isRenaming ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Renaming...
                </>
              ) : (
                "Rename"
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete conversation?</AlertDialogTitle>
            <AlertDialogDescription>
              This will permanently delete this conversation and all its
              messages. This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel
              onClick={() => setConversationToDelete(null)}
              disabled={deletingId !== null}
            >
              Cancel
            </AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDeleteConfirm}
              disabled={deletingId !== null}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              {deletingId ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Deleting...
                </>
              ) : (
                "Delete"
              )}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
