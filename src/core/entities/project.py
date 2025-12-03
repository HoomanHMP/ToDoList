from datetime import datetime

class Project:
    def __init__(self, name: str, description: str):
        self.id = id(self)
        self.name = name
        self.description = description
        self.created_at = datetime.now()

    def __str__(self):
        return f"Project(ID: {self.id}, Name: '{self.name}')"

    def __repr__(self):
        return f"Project(id={self.id}, name='{self.name}')"