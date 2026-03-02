import json

from aio_pika import Message, DeliveryMode
from aiormq.abc import ConfirmationFrameType

from app.core.config.message_broker import get_channel


async def messaging_publish(exchange_name: str, routing_key: str, payload: dict) -> ConfirmationFrameType:
    async with get_channel() as channel:
        exchange = await channel.get_exchange(exchange_name)

        return await exchange.publish(
            Message(
                body=json.dumps(payload, ensure_ascii=False, default=str).encode(),
                content_type="application/json",
                delivery_mode=DeliveryMode.PERSISTENT,
            ),
            routing_key=routing_key,
        )
