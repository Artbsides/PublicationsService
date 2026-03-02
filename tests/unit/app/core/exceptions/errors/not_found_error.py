from fastapi import status

from app.core.exceptions.errors.not_found import NotFoundError


class TestNotFound:
    def not_found_error_successful_test(self) -> None:
        exception = NotFoundError()

        assert exception.args is not None
        assert exception.status_code is status.HTTP_404_NOT_FOUND
