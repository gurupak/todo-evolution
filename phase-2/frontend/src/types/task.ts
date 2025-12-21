export enum Priority {
  HIGH = "high",
  MEDIUM = "medium",
  LOW = "low",
}

export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string;
  priority: Priority;
  is_completed: boolean;
  target_completion_date: string | null;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
  priority?: Priority;
  target_completion_date?: string | null;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  priority?: Priority;
  target_completion_date?: string | null;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  completed: number;
  pending: number;
}
