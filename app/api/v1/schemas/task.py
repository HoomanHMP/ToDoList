from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):

    title: str = Field(..., min_length=1, max_length=30, description="Task title")
    description: str = Field(
        ..., min_length=1, max_length=150, description="Task description"
    )


class TaskCreate(TaskBase):

    deadline: Optional[datetime] = Field(
        None, description="Task deadline (ISO 8601 format)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Complete Phase 3",
                "description": "Implement FastAPI endpoints for the ToDoList",
                "deadline": "2025-12-31T23:59:59",
            }
        }
    )


class TaskUpdate(BaseModel):

    title: Optional[str] = Field(
        None, min_length=1, max_length=30, description="Task title"
    )
    description: Optional[str] = Field(
        None, min_length=1, max_length=150, description="Task description"
    )
    deadline: Optional[datetime] = Field(
        None, description="Task deadline (ISO 8601 format)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Updated task title",
                "description": "Updated task description",
                "deadline": "2025-12-31T23:59:59",
            }
        }
    )


class TaskStatusUpdate(BaseModel):

    status: str = Field(
        ..., pattern="^(todo|doing|done)$", description="Task status"
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"status": "doing"}}
    )


class TaskResponse(TaskBase):

    id: int = Field(..., description="Task ID")
    project_id: int = Field(..., description="Associated project ID")
    status: str = Field(..., description="Task status (todo, doing, done)")
    deadline: Optional[datetime] = Field(None, description="Task deadline")
    closed_at: Optional[datetime] = Field(None, description="Task close timestamp")
    created_at: datetime = Field(..., description="Task creation timestamp")

    model_config = ConfigDict(from_attributes=True)
