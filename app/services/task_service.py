import os
from datetime import datetime
from typing import List, Optional, Tuple

from dotenv import load_dotenv

from app.exceptions import EntityNotFoundException
from app.models.task import Task
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository

load_dotenv()


class TaskService:

    def __init__(
        self,
        task_repository: TaskRepository,
        project_repository: ProjectRepository,
    ):
        self.task_repository = task_repository
        self.project_repository = project_repository
        self.max_tasks_per_project = int(
            os.getenv("MAX_NUMBER_OF_TASKS_PER_PROJECT", 100)
        )
        self.valid_statuses = ["todo", "doing", "done"]

    def add_task(
        self,
        project_id: int,
        title: str,
        description: str,
        deadline: Optional[datetime] = None,
    ) -> Tuple[bool, str]:
        if len(title) > 30:
            return False, "Error: Task title cannot exceed 30 characters."

        if len(description) > 150:
            return False, "Error: Task description cannot exceed 150 characters."

        project = self.project_repository.get_by_id(project_id)
        if not project:
            return False, "Error: Project with this ID not found."

        task_count = self.task_repository.count_by_project_id(project_id)
        if task_count >= self.max_tasks_per_project:
            return (
                False,
                f"Error: Maximum number of tasks per project ({self.max_tasks_per_project}) reached.",
            )

        task = self.task_repository.create(project_id, title, description, deadline)
        return True, f"Task '{title}' created successfully. (ID: {task.id})"

    def change_task_status(self, task_id: int, new_status: str) -> Tuple[bool, str]:
        if new_status not in self.valid_statuses:
            return (
                False,
                f"Error: Status '{new_status}' is invalid. Valid statuses: {', '.join(self.valid_statuses)}",
            )

        try:
            task = self.task_repository.get_by_id(task_id)
            if not task:
                return False, "Error: Task with this ID not found."

            old_status = task.status
            self.task_repository.update_status(task_id, new_status)
            return True, f"Task status changed from '{old_status}' to '{new_status}'."
        except EntityNotFoundException:
            return False, "Error: Task with this ID not found."

    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        return self.task_repository.get_by_project_id(project_id)

    def close_overdue_tasks(self) -> int:
        overdue_tasks = self.task_repository.get_overdue_tasks()
        for task in overdue_tasks:
            self.task_repository.close_overdue_task(task)
        return len(overdue_tasks)
