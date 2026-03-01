import json

from aio_pika import DeliveryMode, Message
from aiormq.abc import ConfirmationFrameType
from app.confs.broker import get_channel


async def publish(routing_key: str, payload: dict) -> ConfirmationFrameType:
    async with get_channel() as channel:
        exchange = await channel.get_exchange("article")

        return await exchange.publish(
            Message(
                body=json.dumps(payload, ensure_ascii=False, default=str).encode(),
                content_type="application/json",
                delivery_mode=DeliveryMode.PERSISTENT,
            ),
            routing_key=routing_key,
        )
