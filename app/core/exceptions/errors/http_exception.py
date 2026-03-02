from fastapi import status
from starlette.exceptions import HTTPException

from app.core.exceptions.errors.base import BaseError
from app.core.exceptions.errors.not_found import NotFoundError
from app.core.exceptions.errors.internal_server import InternalServerError


class HTTPExceptionError(BaseError):
    def __new__(cls, exception: HTTPException) -> BaseError:
        if exception.status_code == status.HTTP_404_NOT_FOUND:
            return NotFoundError()

        raise InternalServerError(exception) from exception
