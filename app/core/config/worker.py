import asyncio

from celery import Celery
from functools import lru_cache
from celery.signals import worker_process_init, worker_process_shutdown
from collections.abc import Coroutine
from dishka.integrations.celery import setup_dishka

from app.core.config.environment import settings


loop: asyncio.AbstractEventLoop | None = None


@worker_process_init.connect
def worker_init(**_) -> None:
    global loop

    asyncio.set_event_loop(
        loop := asyncio.new_event_loop()
    )


@worker_process_shutdown.connect
def worker_shutdown(**_) -> None:
    if loop and not loop.is_closed():
        loop.close()


def run_async(coroutine: Coroutine) -> None:
    if loop is None:
        raise RuntimeError("Event loop not initialized. Is the worker running?")

    loop.run_until_complete(coroutine)


@lru_cache
def get_application() -> Celery:
    from app.core.dependencies import build_worker_container

    uri = (
        f"{settings.MESSAGE_BROKER_USER}:{settings.MESSAGE_BROKER_PASSWORD}@"
        f"{settings.MESSAGE_BROKER_HOST}:{settings.MESSAGE_BROKER_PORT}"
    )

    app = Celery(
        "publications-service", broker=f"amqp://{uri}//"
    )

    setup_dishka(
        build_worker_container(), app
    )

    return app
