from typing import AsyncGenerator
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config.environment import settings
from app.core.config.message_broker import ensure_binding
from app.core.config.database.session import dispose_engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    await ensure_binding(
        bindings=[{
            "exchange": "articles", "routing_keys": [
                "article.created"
            ]
        }]
    )

    yield
    await dispose_engine()
