from celery import Celery
from dishka import Scope, Provider, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.worker import get_application
from app.core.config.database.session import get_session


class DatabaseProvider(Provider):
    session = provide(
        source=staticmethod(get_session.__wrapped__), provides=AsyncSession, scope=Scope.REQUEST,
    )


class QueueProvider(Provider):
    publisher = provide(
        source=staticmethod(get_application), provides=Celery, scope=Scope.APP,
    )
