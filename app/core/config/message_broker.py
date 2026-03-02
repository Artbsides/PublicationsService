from aio_pika import ExchangeType, connect_robust
from contextlib import asynccontextmanager
from aio_pika.abc import AbstractChannel
from collections.abc import AsyncGenerator

from app.core.config.environment import settings


@asynccontextmanager
async def get_channel() -> AsyncGenerator[AbstractChannel]:
    uri = (
        f"{settings.MESSAGE_BROKER_USER}:{settings.MESSAGE_BROKER_PASSWORD}@"
        f"{settings.MESSAGE_BROKER_HOST}:{settings.MESSAGE_BROKER_PORT}//"
    )

    async with await connect_robust(f"amqp://{uri}") as connection:
        yield await connection.channel()


async def ensure_binding(bindings: list[dict]) -> None:
    async with get_channel() as channel:
        for bind in bindings:
            exchange = await channel.declare_exchange(
                name=bind["exchange"], type=ExchangeType.TOPIC, durable=True,
            )

            for routing_key in bind["routing_keys"]:
                queue = await channel.declare_queue(
                    name=f"{routing_key}.queue", durable=True,
                )

                await queue.bind(
                    exchange, routing_key=routing_key
                )
