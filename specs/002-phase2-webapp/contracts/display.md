# UI Component Contract

## Component Interfaces

### TaskList
```typescript
interface TaskListProps {
  userId: string;
}
// Fetches and displays all tasks with TanStack Query
```

### TaskItem
```typescript
interface TaskItemProps {
  task: Task;
  onToggle: (taskId: string) => void;
  onEdit: (taskId: string) => void;
  onDelete: (taskId: string) => void;
}
```

### TaskForm
```typescript
interface TaskFormProps {
  mode: 'create' | 'edit';
  task?: Task;
  onSubmit: (data: TaskCreateRequest | TaskUpdateRequest) => Promise<void>;
  onCancel: () => void;
}
```

### PriorityBadge
```typescript
interface PriorityBadgeProps {
  priority: 'high' | 'medium' | 'low';
}
// Red for high, yellow for medium, green for low
```

### TaskStats
```typescript
interface TaskStatsProps {
  total: number;
  completed: number;
  pending: number;
}
```

## Component Hierarchy

```
DashboardPage
├── TaskStats
├── AddTaskButton → TaskForm (dialog)
└── TaskList
    └── TaskItem (multiple)
        ├── Checkbox (toggle complete)
        ├── PriorityBadge
        └── DropdownMenu (edit/delete)
            ├── TaskForm (edit dialog)
            └── AlertDialog (delete confirm)
```
