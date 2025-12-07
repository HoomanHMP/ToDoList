from datetime import datetime

from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


def autoclose_overdue_command() -> int:
    session = SessionLocal()
    try:
        project_repository = ProjectRepository(session)
        task_repository = TaskRepository(session)
        task_service = TaskService(task_repository, project_repository)

        closed_count = task_service.close_overdue_tasks()
        session.commit()

        if closed_count > 0:
            print(
                f"[{datetime.now().isoformat()}] Closed {closed_count} overdue task(s)."
            )
        else:
            print(f"[{datetime.now().isoformat()}] No overdue tasks found.")

        return closed_count
    except Exception as e:
        session.rollback()
        print(f"[{datetime.now().isoformat()}] Error: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    autoclose_overdue_command()
