import pytest

from fastapi import status
from starlette.exceptions import HTTPException

from app.core.exceptions.errors.http_exception import HTTPExceptionError
from app.core.exceptions.errors.internal_server import InternalServerError


class TestHTTPExceptionError:
    def http_exception_mapped_error_successful_test(self) -> None:
        exception = HTTPExceptionError(
            HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        )

        assert exception.args is not None
        assert exception.status_code is status.HTTP_404_NOT_FOUND

    def http_exception_not_mapped_error_successful_test(self) -> None:
        with pytest.raises(InternalServerError) as exception:
            HTTPExceptionError(
                HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            )

        assert exception.value.args is not None
        assert exception.value.status_code is status.HTTP_500_INTERNAL_SERVER_ERROR
