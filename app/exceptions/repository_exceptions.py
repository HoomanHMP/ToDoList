from app.exceptions.base import AppException


class RepositoryException(AppException):

    pass


class EntityNotFoundException(RepositoryException):

    def __init__(self, entity_type: str, entity_id: int):
        message = f"{entity_type} with ID {entity_id} not found."
        super().__init__(message)


class DuplicateEntityException(RepositoryException):

    def __init__(self, entity_type: str, field: str, value: str):
        message = f"A {entity_type} with {field} '{value}' already exists."
        super().__init__(message)
