from typing import ClassVar
from fastapi import status

from app.exceptions.errors.base import BaseError


class UnauthorizedTokenError(BaseError):
    args: ClassVar[dict[str, str]] = {
        "message": "Check your bearer token, you might not be authorized"
    }

    status_code = status.HTTP_401_UNAUTHORIZED
