import sys

from app.cli.console import ToDoListCLI
from app.db.session import SessionLocal


def main() -> None:
    session = SessionLocal()
    try:
        cli = ToDoListCLI(session)
        cli.run()
        session.commit()
    except KeyboardInterrupt:
        print("\nExiting...")
        session.rollback()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()
