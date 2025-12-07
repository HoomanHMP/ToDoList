from app.exceptions.base import AppException


class ServiceException(AppException):

    pass


class ValidationException(ServiceException):

    pass


class MaxLimitReachedException(ServiceException):

    def __init__(self, entity_type: str, limit: int):
        message = f"Maximum number of {entity_type} ({limit}) reached."
        super().__init__(message)
