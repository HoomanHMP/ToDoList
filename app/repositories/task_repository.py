from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.exceptions.repository_exceptions import EntityNotFoundException
from app.models.task import Task


class TaskRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Task]:
        stmt = select(Task).order_by(Task.created_at)
        result = self.session.execute(stmt)
        return list(result.scalars().all())

    def get_by_id(self, task_id: int) -> Optional[Task]:
        stmt = select(Task).where(Task.id == task_id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_project_id(self, project_id: int) -> List[Task]:
        stmt = select(Task).where(Task.project_id == project_id).order_by(Task.created_at)
        result = self.session.execute(stmt)
        return list(result.scalars().all())

    def count_by_project_id(self, project_id: int) -> int:
        return len(self.get_by_project_id(project_id))

    def get_overdue_tasks(self) -> List[Task]:
        now = datetime.now()
        stmt = select(Task).where(
            and_(
                Task.deadline.is_not(None),
                Task.deadline < now,
                Task.status != "done",
            )
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())

    def create(
        self,
        project_id: int,
        title: str,
        description: str,
        deadline: Optional[datetime] = None,
    ) -> Task:
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
        )
        self.session.add(task)
        self.session.flush()  # Get the ID
        return task

    def update_status(self, task_id: int, new_status: str) -> Task:
        task = self.get_by_id(task_id)
        if not task:
            raise EntityNotFoundException("Task", task_id)

        old_status = task.status
        task.status = new_status

        # If marking as done, set closed_at
        if new_status == "done" and old_status != "done":
            task.closed_at = datetime.now()

        return task

    def close_overdue_task(self, task: Task) -> Task:
        task.status = "done"
        task.closed_at = datetime.now()
        return task

    def delete(self, task_id: int) -> Task:
        task = self.get_by_id(task_id)
        if not task:
            raise EntityNotFoundException("Task", task_id)

        self.session.delete(task)
        return task