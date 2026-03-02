
from contextlib import asynccontextmanager
from contextvars import ContextVar
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config.database.connection_settings import get_engine_settings, get_session_factory_settings, \
    get_database_connection_string


engine = create_async_engine(
    get_database_connection_string(), **get_engine_settings()
)

SessionFactory = async_sessionmaker(
    bind=engine, class_=AsyncSession, **get_session_factory_settings()
)

async_session: ContextVar[AsyncSession | None] = ContextVar(
    "async_session", default=None
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession]:
    current_session = async_session.get()

    if current_session:
        yield current_session
    else:
        async with SessionFactory() as session:
            token = async_session.set(session)

            try:
                async with session.begin():
                    yield session
            finally:
                async_session.reset(token)


def get_current_session() -> AsyncSession:
    current_session = async_session.get()

    if current_session is None:
        raise RuntimeError("No active DB session in context")

    return current_session


async def dispose_engine() -> None:
    try:
        await engine.dispose()
    except Exception:
        pass
