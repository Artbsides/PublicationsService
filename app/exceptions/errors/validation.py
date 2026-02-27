from fastapi import status
from pydantic import ValidationError as PydanticValidationError

from app.exceptions.errors.base import BaseError


class ValidationError(BaseError):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, exception: PydanticValidationError) -> None:
        self.args = exception.errors()
