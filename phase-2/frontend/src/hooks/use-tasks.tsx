"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "src/lib/api-client";
import { useAuth } from "./use-auth";
import type { Task, TaskListResponse, Priority } from "@/types/task";

interface CreateTaskData {
  title: string;
  description: string;
  priority: Priority;
  target_completion_date?: string | null;
}

interface UpdateTaskData {
  title?: string;
  description?: string;
  priority?: Priority;
  target_completion_date?: string | null;
}

/**
 * Hook for fetching all tasks for the authenticated user
 * Uses TanStack Query for caching and automatic refetching (T077)
 */
export function useTasks() {
  const { user } = useAuth();
  const userId = user?.id;

  return useQuery<TaskListResponse>({
    queryKey: ["tasks", userId],
    queryFn: async () => {
      if (!userId) throw new Error("User not authenticated");
      const response = await apiClient.get(`/${userId}/tasks`);
      return response.data;
    },
    enabled: !!userId,
    staleTime: 30 * 1000, // 30 seconds
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    refetchOnReconnect: false,
  });
}

/**
 * Hook for creating a new task
 * Automatically refetches task list on success (T078)
 */
export function useCreateTask() {
  const { user } = useAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateTaskData) => {
      if (!user?.id) throw new Error("User not authenticated");
      const response = await apiClient.post(`/${user.id}/tasks`, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks", user?.id] });
    },
  });
}

/**
 * Hook for updating a task
 * Automatically refetches task list on success
 */
export function useUpdateTask() {
  const { user } = useAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      taskId,
      data,
    }: {
      taskId: string;
      data: UpdateTaskData;
    }) => {
      if (!user?.id) throw new Error("User not authenticated");
      const response = await apiClient.put(`/${user.id}/tasks/${taskId}`, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks", user?.id] });
    },
  });
}

/**
 * Hook for toggling task completion status
 * Automatically refetches task list on success
 */
export function useToggleComplete() {
  const { user } = useAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (taskId: string) => {
      if (!user?.id) throw new Error("User not authenticated");
      const response = await apiClient.patch(
        `/${user.id}/tasks/${taskId}/complete`,
      );
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks", user?.id] });
    },
  });
}

/**
 * Hook for deleting a task
 * Automatically refetches task list on success
 */
export function useDeleteTask() {
  const { user } = useAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (taskId: string) => {
      if (!user?.id) throw new Error("User not authenticated");
      const response = await apiClient.delete(`/${user.id}/tasks/${taskId}`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks", user?.id] });
    },
  });
}
