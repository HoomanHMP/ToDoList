from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions.repository_exceptions import (
    DuplicateEntityException,
    EntityNotFoundException,
)
from app.models.project import Project


class ProjectRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Project]:
        stmt = select(Project).order_by(Project.created_at)
        result = self.session.execute(stmt)
        return list(result.scalars().all())

    def get_by_id(self, project_id: int) -> Optional[Project]:
        stmt = select(Project).where(Project.id == project_id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_name(self, name: str) -> Optional[Project]:
        stmt = select(Project).where(Project.name == name)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def count(self) -> int:
        return len(self.get_all())

    def create(self, name: str, description: str) -> Project:
        # Check for duplicate name
        existing = self.get_by_name(name)
        if existing:
            raise DuplicateEntityException("Project", "name", name)

        project = Project(name=name, description=description)
        self.session.add(project)
        self.session.flush()  # Get the ID
        return project

    def delete(self, project_id: int) -> Project:
        project = self.get_by_id(project_id)
        if not project:
            raise EntityNotFoundException("Project", project_id)

        self.session.delete(project)
        return project
