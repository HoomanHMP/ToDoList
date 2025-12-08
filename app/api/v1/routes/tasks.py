import re
from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.api.v1.schemas import TaskCreate, TaskResponse, TaskUpdate, TaskStatusUpdate
from app.db.session import get_db
from app.exceptions import EntityNotFoundException
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    return TaskService(task_repo, project_repo)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task in a project. Maximum 100 tasks per project allowed.",
)
def create_task(
    project_id: int,
    task: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    success, message = service.add_task(
        project_id, task.title, task.description, task.deadline
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    
    match = re.search(r'\(ID: (\d+)\)', message)
    if match:
        task_id = int(match.group(1))
        created_task = service.task_repository.get_by_id(task_id)
        return created_task
    
    tasks = service.get_tasks_by_project(project_id)
    created_task = tasks[-1] if tasks else None
    return created_task


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="List all tasks in a project",
    description="Retrieve all tasks for a specific project.",
)
def list_tasks(
    project_id: int, service: TaskService = Depends(get_task_service)
):
    try:
        tasks = service.get_tasks_by_project(project_id)
        return tasks
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
    description="Retrieve a specific task by its ID.",
)
def get_task(
    project_id: int, task_id: int, service: TaskService = Depends(get_task_service)
):
    try:
        task = service.task_repository.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        if task.project_id != project_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found in this project",
            )
        return task
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse,
    summary="Update task status",
    description="Update the status of a task (todo, doing, done).",
)
def update_task_status(
    project_id: int,
    task_id: int,
    status_update: TaskStatusUpdate,
    service: TaskService = Depends(get_task_service),
):
    task = service.task_repository.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    if task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found in this project",
        )
    
    success, result = service.change_task_status(task_id, status_update.status)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result)
    
    updated_task = service.task_repository.get_by_id(task_id)
    return updated_task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a specific task.",
)
def delete_task(
    project_id: int, task_id: int, service: TaskService = Depends(get_task_service)
):
    task = service.task_repository.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    if task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found in this project",
        )
    
    success, message = service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
