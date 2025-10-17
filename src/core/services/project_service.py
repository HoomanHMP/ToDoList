import os
from dotenv import load_dotenv
from src.core.entities.project import Project
from src.data.in_memory_db import database

load_dotenv()

class ProjectService:
    def __init__(self):
        self.max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECTS", 10))

    def create_project(self, name: str, description: str) -> tuple[bool, str]:
        if len(name) > 30:
            return False, "Error: Project name cannot exceed 30 characters."
        if len(description) > 150:
            return False, "Error: Project description cannot exceed 150 characters."
        if len(database.projects) >= self.max_projects:
            return False, f"Error: Maximum number of projects ({self.max_projects}) reached."

        for project in database.projects:
            if project.name == name:
                return False, "Error: A project with this name already exists."

        new_project = Project(name, description)
        database.projects.append(new_project)

        return True, f"Project '{name}' created successfully. (ID: {new_project.id})"

    def get_all_projects(self) -> list[Project]:
        return sorted(database.projects, key = lambda p: p.created_at)

    def delete_project(self, project_id: int) -> tuple[bool, str]:
        project_to_delete = None
        for project in database.projects:
            if project.id == project_id:
                project_to_delete = project
                break

        if project_to_delete is None:
            return False, "Error: Project with this ID not found."

        database.tasks = [task for task in database.tasks if task.project_id != project_id]
        database.projects.remove(project_to_delete)

        return True, f"Project '{project_to_delete.name}' and all its tasks deleted successfully."