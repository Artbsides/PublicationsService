from celery import Celery
from app.confs.environment import settings


def get_application():
    uri = (
        f"{settings.MESSAGE_BROKER_USER}:{settings.MESSAGE_BROKER_PASSWORD}@"
        f"{settings.MESSAGE_BROKER_HOST}:{settings.MESSAGE_BROKER_PORT}"
    )

    return Celery(
        "XMLParserWorker", broker=f"amqp://{uri}", backend="rpc://",
    )
