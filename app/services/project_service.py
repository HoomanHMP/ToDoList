import os
from typing import List, Optional, Tuple

from dotenv import load_dotenv

from app.exceptions import (
    DuplicateEntityException,
    EntityNotFoundException,
    MaxLimitReachedException,
    ValidationException,
)
from app.models.project import Project
from app.repositories.project_repository import ProjectRepository

load_dotenv()


class ProjectService:

    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository
        self.max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECTS", 10))

    def create_project(self, name: str, description: str) -> Tuple[bool, str]:
        if len(name) > 30:
            return False, "Error: Project name cannot exceed 30 characters."

        if len(description) > 150:
            return False, "Error: Project description cannot exceed 150 characters."

        if self.project_repository.count() >= self.max_projects:
            return (
                False,
                f"Error: Maximum number of projects ({self.max_projects}) reached.",
            )

        try:
            project = self.project_repository.create(name, description)
            return True, f"Project '{name}' created successfully. (ID: {project.id})"
        except DuplicateEntityException:
            return False, "Error: A project with this name already exists."

    def get_all_projects(self) -> List[Project]:
        return self.project_repository.get_all()

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        return self.project_repository.get_by_id(project_id)

    def delete_project(self, project_id: int) -> Tuple[bool, str]:
        try:
            project = self.project_repository.delete(project_id)
            return (
                True,
                f"Project '{project.name}' and all its tasks deleted successfully.",
            )
        except EntityNotFoundException:
            return False, "Error: Project with this ID not found."
