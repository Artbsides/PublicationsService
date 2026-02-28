
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.confs.database.connection_settings import get_database_connection_string, get_engine_settings, get_session_factory_settings


engine = create_async_engine(
    get_database_connection_string(), **get_engine_settings()
)


SessionFactory = async_sessionmaker(
    bind=engine, class_=AsyncSession, **get_session_factory_settings()
)


_current_session: ContextVar[AsyncSession | None] = ContextVar(
    "current_session", default=None
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    current_session = _current_session.get()

    if current_session:
        yield current_session
    else:
        async with SessionFactory() as session:
            token = _current_session.set(session)

            try:
                async with session.begin():
                    yield session
            finally:
                _current_session.reset(token)


def get_current_session() -> AsyncSession:
    session = _current_session.get()

    if session is None:
        raise RuntimeError("No active DB session in context")

    return session


async def dispose_engine() -> None:
    try:
        await engine.dispose()
    except Exception:
        pass
