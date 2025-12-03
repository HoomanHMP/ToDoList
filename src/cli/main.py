from src.core.services.project_service import ProjectService
from src.core.services.task_service import TaskService


class ToDoListCLI:
    def __init__(self):
        self.project_service = ProjectService()
        self.task_service = TaskService()

    def display_menu(self):
        print("\n\n\n\n\n")
        print("-"*50)
        print("          ToDoList System (Python OOP)")
        print("="*50)
        print("1. List all projects")
        print("2. Create new project")
        print("3. Delete project")
        print("4. Show tasks in a project")
        print("5. Add task to project")
        print("6. Change task status")
        print("0. Exit")
        print("-"*50)

    def run(self):
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

    def _list_all_projects(self):
        projects = self.project_service.get_all_projects()
        if not projects:
            print(">>> No projects found.")
            return

        print("\n>>> All Projects:")
        for i, project in enumerate(projects, 1):
            print(f"  {i}. {project} - Description: {project.description}")

    def _create_project(self):
        print("\n>>> Create New Project:")
        name = input("Project name: ").strip()
        description = input("Project description: ").strip()

        success, message = self.project_service.create_project(name, description)
        print(f">>> {message}")

    def _delete_project(self):
        print("\n>>> Delete Project:")
        try:
            project_id = int(input("Project ID to delete: ").strip())
        except ValueError:
            print(">>> Error: ID must be a number.")
            return

        success, message = self.project_service.delete_project(project_id)
        print(f">>> {message}")

    def _list_project_tasks(self):
        print("\n>>> Show Project Tasks:")
        try:
            project_id = int(input("Project ID: ").strip())
        except ValueError:
            print(">>> Error: ID must be a number.")
            return

        if(not any(proj.id == project_id for proj in self.project_service.get_all_projects())):
            print(">>> Error: Project with this ID not found.")
            return

        tasks = self.task_service.get_tasks_by_project(project_id)
        if not tasks:
            print(">>> This project has no tasks.")
            return

        print(f">>> Tasks in Project (ID: {project_id}):")
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. {task} - Description: {task.description}")

    def _add_task(self):
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

    def _change_task_status(self):
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

def main():
    cli = ToDoListCLI()
    cli.run()

if __name__ == "__main__":
    main()