# Business Logic Contract

## TaskService

```python
class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository
    
    async def create_task(
        self, 
        user_id: UUID, 
        data: TaskCreateRequest
    ) -> TaskResponse:
        """Create task with automatic retry on DB failure."""
        
    async def list_tasks(self, user_id: UUID) -> TaskListResponse:
        """List all user tasks with stats."""
        
    async def get_task(
        self, 
        user_id: UUID, 
        task_id: UUID
    ) -> TaskResponse:
        """Get single task, raise 404 if not found."""
        
    async def update_task(
        self,
        user_id: UUID,
        task_id: UUID,
        data: TaskUpdateRequest
    ) -> TaskResponse:
        """Update task (last-write-wins strategy)."""
        
    async def delete_task(
        self,
        user_id: UUID,
        task_id: UUID
    ) -> None:
        """Delete task, raise 404 if not found."""
        
    async def toggle_complete(
        self,
        user_id: UUID,
        task_id: UUID
    ) -> TaskResponse:
        """Toggle task completion status."""
```

## Business Rules

1. All operations filter by user_id (data isolation)
2. Title/description trimmed before save
3. Database failures trigger single automatic retry
4. Concurrent edits use last-write-wins
