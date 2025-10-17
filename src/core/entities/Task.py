from datetime import datetime

class Task:
    def __init__(self, project_id: int, title: str, description: str, deadline = None):
        self.id = id(self)
        self.project_id = project_id
        self.title = title
        self.description = description
        self.status = "todo"
        self.deadline = deadline

    def __str__(self):
        return f"Task(ID: {self.id}, Title: '{self.title}', Status: '{self.status}')"

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"