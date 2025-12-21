# Storage Layer Contract

## Database Operations

### TaskRepository

```python
class TaskRepository:
    async def create(self, user_id: UUID, data: TaskCreateRequest) -> Task
    async def get_by_id(self, user_id: UUID, task_id: UUID) -> Task | None
    async def list_by_user(self, user_id: UUID) -> list[Task]
    async def update(self, user_id: UUID, task_id: UUID, data: TaskUpdateRequest) -> Task | None
    async def delete(self, user_id: UUID, task_id: UUID) -> bool
    async def toggle_complete(self, user_id: UUID, task_id: UUID) -> Task | None
```

### Query Patterns

```python
# List tasks (sorted by created_at DESC)
SELECT * FROM task 
WHERE user_id = $1 
ORDER BY created_at DESC

# Get stats
SELECT 
  COUNT(*) as total,
  SUM(CASE WHEN is_completed THEN 1 ELSE 0 END) as completed,
  SUM(CASE WHEN NOT is_completed THEN 1 ELSE 0 END) as pending
FROM task
WHERE user_id = $1
```
