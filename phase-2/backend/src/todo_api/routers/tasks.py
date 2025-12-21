"""Task API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..middleware.auth import get_current_user_id, verify_user_authorization
from ..schemas.common import DeleteResponse
from ..schemas.task import TaskCreateRequest, TaskListResponse, TaskResponse, TaskUpdateRequest
from ..services.task_service import TaskService

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    user_id: str = Path(...),
    token_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskListResponse:
    """List all tasks for the authenticated user."""
    # Verify authorization
    authorized_user_id = verify_user_authorization(user_id, token_user_id)
    service = TaskService(session)
    return await service.get_all(authorized_user_id)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreateRequest,
    user_id: str = Path(...),
    token_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Create a new task."""
    authorized_user_id = verify_user_authorization(user_id, token_user_id)
    service = TaskService(session)
    task = await service.create(authorized_user_id, data)
    return TaskResponse.from_orm(task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    user_id: str = Path(...),
    token_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Get a specific task by ID."""
    authorized_user_id = verify_user_authorization(user_id, token_user_id)
    service = TaskService(session)
    task = await service.get_by_id(task_id, authorized_user_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskResponse.from_orm(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    data: TaskUpdateRequest,
    user_id: str = Path(...),
    token_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Update a task."""
    authorized_user_id = verify_user_authorization(user_id, token_user_id)
    service = TaskService(session)
    task = await service.update(task_id, authorized_user_id, data)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskResponse.from_orm(task)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    task_id: str,
    user_id: str = Path(...),
    token_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Toggle task completion status."""
    authorized_user_id = verify_user_authorization(user_id, token_user_id)
    service = TaskService(session)
    task = await service.toggle_complete(task_id, authorized_user_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskResponse.from_orm(task)


@router.delete("/{task_id}", response_model=DeleteResponse)
async def delete_task(
    task_id: str,
    user_id: str = Path(...),
    token_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> DeleteResponse:
    """Delete a task."""
    authorized_user_id = verify_user_authorization(user_id, token_user_id)
    service = TaskService(session)
    deleted = await service.delete(task_id, authorized_user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return DeleteResponse(message="Task deleted successfully", id=str(task_id))
