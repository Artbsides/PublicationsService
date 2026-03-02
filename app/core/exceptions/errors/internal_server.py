from typing import ClassVar
from fastapi import status

from app.core.exceptions.errors.base import BaseError


class InternalServerError(BaseError):
    args: ClassVar[dict[str, str]] = {
        "message": "An internal error occurred"
    }

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
