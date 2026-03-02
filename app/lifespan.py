from fastapi import FastAPI
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from app.core.config.message_broker import ensure_binding
from app.core.config.database.session import dispose_engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    await ensure_binding(
        bindings=[{
            "exchange": "articles", "routing_keys": [
                "article.created"
            ]
        }]
    )

    yield
    await dispose_engine()
