from fastapi import Request, HTTPException, status
from unittest.mock import patch
from fastapi.responses import JSONResponse

from app.core.exceptions.exception_handler import ExceptionHandler


class TestExceptionHandler:
    @patch("app.core.exceptions.exception_handler.Request")
    async def throw_mapped_error_successful_test(self, request: Request) -> None:
        handler = ExceptionHandler.throw(
            request, HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        )

        assert handler.status_code is status.HTTP_404_NOT_FOUND

        assert handler.body is not None
        assert isinstance(handler, JSONResponse)

    @patch("app.core.exceptions.exception_handler.Request")
    async def throw_not_mapped_error_successful_test(self, request: Request) -> None:
        handler = ExceptionHandler.throw(
            request, AttributeError()
        )

        assert handler.status_code is status.HTTP_500_INTERNAL_SERVER_ERROR

        assert handler.body is not None
        assert isinstance(handler, JSONResponse)
