from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProjectBase(BaseModel):

    name: str = Field(..., min_length=1, max_length=30, description="Project name")
    description: str = Field(
        ..., min_length=1, max_length=150, description="Project description"
    )


class ProjectCreate(ProjectBase):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "My Project",
                "description": "A detailed description of my project",
            }
        }
    )


class ProjectUpdate(BaseModel):

    name: Optional[str] = Field(
        None, min_length=1, max_length=30, description="Project name"
    )
    description: Optional[str] = Field(
        None, min_length=1, max_length=150, description="Project description"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Project Name",
                "description": "Updated project description",
            }
        }
    )


class ProjectResponse(ProjectBase):

    id: int = Field(..., description="Project ID")
    created_at: datetime = Field(..., description="Project creation timestamp")

    model_config = ConfigDict(from_attributes=True)
