import time
from datetime import datetime

import schedule

from app.commands.autoclose_overdue import autoclose_overdue_command


def setup_scheduler() -> None:
    schedule.every(15).minutes.do(autoclose_overdue_command)

def run_scheduler() -> None:
    setup_scheduler()

    print(f"[{datetime.now().isoformat()}] Scheduler started.")
    print("Press Ctrl+C to stop.")

    autoclose_overdue_command()

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    run_scheduler()
