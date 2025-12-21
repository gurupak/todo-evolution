# Data Models Contract

## Pydantic Schemas (Backend)

### TaskCreateRequest
```python
class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
```

### TaskUpdateRequest
```python
class TaskUpdateRequest(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    priority: PriorityEnum | None = None
```

### TaskResponse
```python
class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str
    priority: PriorityEnum
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
```

### TaskListResponse
```python
class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
    completed: int
    pending: int
```

## TypeScript Types (Frontend)

```typescript
export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  is_completed: boolean;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
  priority?: 'high' | 'medium' | 'low';
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  priority?: 'high' | 'medium' | 'low';
}
```
