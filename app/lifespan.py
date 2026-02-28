from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.confs.database.session import dispose_engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await dispose_engine()
