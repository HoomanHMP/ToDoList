import warnings
from sqlalchemy.orm import Session

from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService


class ToDoListCLI:

    def __init__(self, session: Session):
        # Dependency Injection: inject repositories into services
        self.session = session
        project_repository = ProjectRepository(session)
        task_repository = TaskRepository(session)

        self.project_service = ProjectService(project_repository)
        self.task_service = TaskService(task_repository, project_repository)

    def display_menu(self) -> None:
        print("\n\n\n\n\n")
        print("-" * 50)
        print("          ToDoList System (Python OOP)")
        print("=" * 50)
        print("1. List all projects")
        print("2. Create new project")
        print("3. Delete project")
        print("4. Show tasks in a project")
        print("5. Add task to project")
        print("6. Change task status")
        print("0. Exit")
        print("-" * 50)

    def run(self) -> None:
        warnings.warn(
            "\n" + "=" * 70 + "\n"
            "DEPRECATION WARNING: This CLI is deprecated!\n"
            "The CLI interface will be removed in a future version.\n"
            "Please migrate to the REST API:\n"
            "  1. Start API: uvicorn app.api.app:app --reload\n"
            "  2. Visit: http://localhost:8000/docs\n"
            "New features will only be added to the API.\n"
            + "=" * 70,
            DeprecationWarning,
            stacklevel=2,
        )
        print("\n" + "!" * 70)
        print("WARNING: This CLI is DEPRECATED!")
        print("Please use the REST API instead.")
        print("Start API with: uvicorn app.api.app:app --reload")
        print("Documentation at: http://localhost:8000/docs")
        print("!" * 70)
        
        while True:
            self.display_menu()
            choice = input("Please enter your choice: ").strip()

            if choice == "1":
                self._list_all_projects()
            elif choice == "2":
                self._create_project()
            elif choice == "3":
                self._delete_project()
            elif choice == "4":
                self._list_project_tasks()
            elif choice == "5":
                self._add_task()
            elif choice == "6":
                self._change_task_status()
            elif choice == "0":
                print("Thank you for using ToDoList. Goodbye!")
                break
            else:
                print("Error: Invalid choice.")

    def _list_all_projects(self) -> None:
        projects = self.project_service.get_all_projects()
        if not projects:
            print(">>> No projects found.")
            return

        print("\n>>> All Projects:")
        for i, project in enumerate(projects, 1):
            print(f"  {i}. {project} - Description: {project.description}")

    def _create_project(self) -> None:
        print("\n>>> Create New Project:")
        name = input("Project name: ").strip()
        description = input("Project description: ").strip()

        success, message = self.project_service.create_project(name, description)
        print(f">>> {message}")

    def _delete_project(self) -> None:
        print("\n>>> Delete Project:")
        try:
            project_id = int(input("Project ID to delete: ").strip())
        except ValueError:
            print(">>> Error: ID must be a number.")
            return

        success, message = self.project_service.delete_project(project_id)
        print(f">>> {message}")

    def _list_project_tasks(self) -> None:
        print("\n>>> Show Project Tasks:")
        try:
            project_id = int(input("Project ID: ").strip())
        except ValueError:
            print(">>> Error: ID must be a number.")
            return

        project = self.project_service.get_project_by_id(project_id)
        if not project:
            print(">>> Error: Project with this ID not found.")
            return

        tasks = self.task_service.get_tasks_by_project(project_id)
        if not tasks:
            print(">>> This project has no tasks.")
            return

        print(f">>> Tasks in Project (ID: {project_id}):")
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. {task} - Description: {task.description}")

    def _add_task(self) -> None:
        print("\n>>> Add New Task:")
        try:
            project_id = int(input("Project ID: ").strip())
            title = input("Task title: ").strip()
            description = input("Task description: ").strip()
        except ValueError:
            print(">>> Error: Project ID must be a number.")
            return

        success, message = self.task_service.add_task(project_id, title, description)
        print(f">>> {message}")

    def _change_task_status(self) -> None:
        print("\n>>> Change Task Status:")
        try:
            task_id = int(input("Task ID: ").strip())
            print("Valid statuses: todo, doing, done")
            new_status = input("New status: ").strip().lower()
        except ValueError:
            print(">>> Error: Task ID must be a number.")
            return

        success, message = self.task_service.change_task_status(task_id, new_status)
        print(f">>> {message}")
