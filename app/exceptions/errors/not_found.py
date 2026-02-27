from typing import ClassVar
from fastapi import status

from app.exceptions.errors.base import BaseError


class NotFoundError(BaseError):
    args: ClassVar[dict[str, str]] = {
        "message": "Resource not found"
    }

    status_code = status.HTTP_404_NOT_FOUND
