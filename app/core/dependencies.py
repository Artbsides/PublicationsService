from dishka import Scope, AsyncContainer, make_async_container
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from dishka.integrations.fastapi import FastapiProvider

from app.core.config.dependencies import QueueProvider, DatabaseProvider
from app.modules.uploads.dependencies import UploadProvider
from app.modules.publications.dependencies import PublicationProvider


providers = (
    DatabaseProvider(),
    QueueProvider(),
    PublicationProvider(),
    UploadProvider(),
)


def build_container() -> AsyncContainer:
    return make_async_container(FastapiProvider(), *providers)


@asynccontextmanager
async def build_worker_container() -> AsyncGenerator[AsyncContainer]:
    async with make_async_container(*providers)(scope=Scope.REQUEST) as container:
        yield container
