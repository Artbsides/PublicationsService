from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.confs.broker import ensure_binding
from app.confs.database.session import dispose_engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    await ensure_binding(
        bindings=[
            {
                "exchange": "articles", "routing_keys": [
                    "article.created",
                ]
            }
        ],
    )

    yield
    await dispose_engine()
