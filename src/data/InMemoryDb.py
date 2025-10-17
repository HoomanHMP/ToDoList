class InMemoryDB:
    def __init__(self):
        """سازنده کلاس InMemoryDB. لیست‌های خالی را مقداردهی اولیه می‌کند."""
        self.projects = []
        self.tasks = []

database = InMemoryDB()