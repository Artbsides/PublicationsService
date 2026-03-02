from fastapi import status

from app.core.exceptions.errors.internal_server import InternalServerError


class TestInternalServerError:
    def internal_server_error_successful_test(self) -> None:
        exception = InternalServerError()

        assert exception.args is not None
        assert exception.status_code is status.HTTP_500_INTERNAL_SERVER_ERROR
