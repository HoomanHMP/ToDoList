import os
from dotenv import load_dotenv
from src.core.entities.project import Project
from src.core.entities.task import Task
from src.data.in_memory_db import database

load_dotenv()

class TaskService:
    def __init__(self):
        self.max_tasks_per_project = int(os.getenv("MAX_NUMBER_OF_TASKS_PER_PROJECT", 100))
        self.valid_statuses = ["todo", "doing", "done"]

    def add_task(self, project_id: int, title: str, description: str, deadline=None) -> tuple[bool, str]:
        if len(title) > 30:
            return False, "Error: Task title cannot exceed 30 characters."
        if len(description) > 150:
            return False, "Error: Task description cannot exceed 150 characters."

        project_exists = False
        for project in database.projects:
            if project.id == project_id:
                project_exists = True
                break
        if not project_exists:
            return False, "Error: Project with this ID not found."

        task_count_in_project = sum(1 for task in database.tasks if task.project_id == project_id)
        if task_count_in_project >= self.max_tasks_per_project:
            return False, f"Error: Maximum number of tasks per project ({self.max_tasks_per_project}) reached."

        new_task = Task(project_id, title, description, deadline)
        database.tasks.append(new_task)

        return True, f"Task '{title}' created successfully. (ID: {new_task.id})"

    def change_task_status(self, task_id: int, new_status: str) -> tuple[bool, str]:
        if new_status not in self.valid_statuses:
            return False, f"Error: Status '{new_status}' is invalid. Valid statuses: {', '.join(self.valid_statuses)}"

        task_to_update = None
        for task in database.tasks:
            if task.id == task_id:
                task_to_update = task
                break

        if task_to_update is None:
            return False, "Error: Task with this ID not found."

        old_status = task_to_update.status
        task_to_update.status = new_status

        return True, f"Task status changed from '{old_status}' to '{new_status}'."

    def get_tasks_by_project(self, project_id: int) -> list[Task]:
        return [task for task in database.tasks if task.project_id == project_id]