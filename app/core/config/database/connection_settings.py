from typing import Any

from app.core.config.environment import settings


def get_engine_settings() -> dict[str, Any]:
    return {
        "echo": False,
        "pool_pre_ping": True,
        "pool_size": 10,
        "pool_timeout": 30,
        "pool_recycle": 1800,
        "max_overflow": 20,
    }


def get_session_factory_settings() -> dict[str, bool]:
    return {
        "autoflush": False,
        "expire_on_commit": True,
    }


def get_database_connection_string() -> str:
    uri = (
        f"{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@"
        f"{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/"
        f"{settings.DATABASE_NAME}"
    )

    return f"postgresql+psycopg://{uri}?{settings.DATABASE_PARAMETERS}"
