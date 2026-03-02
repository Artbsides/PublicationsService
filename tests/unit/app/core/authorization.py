import jwt
import pytest

from fastapi import Request, status
from datetime import datetime, timezone, timedelta
from unittest import mock

from app.core.authorization import Authorization
from app.core.config.environment import settings
from app.core.exceptions.errors.unauthorized_token import UnauthorizedTokenError


class TestAuthorization:
    token = jwt.encode(
        key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM, payload={
            "exp": (datetime.now(timezone.utc) + timedelta(seconds=30)).timestamp()
        }
    )

    @mock.patch("app.core.authorization.Request")
    async def authorization_successful_test(self, request: Request) -> None:
        request.headers = {
            "Authorization": f"Bearer {self.token}"
        }

        assert await Authorization().__call__(request) is None

    @mock.patch("app.core.authorization.Request")
    async def authorization_failure_test(self, request: Request) -> None:
        request.headers = {
            "Authorization": "Bearer invalid_token"
        }

        with pytest.raises(UnauthorizedTokenError) as exception:
            await Authorization().__call__(request)

        assert exception.value.args is not None
        assert exception.value.status_code is status.HTTP_401_UNAUTHORIZED
