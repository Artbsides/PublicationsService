from uuid import uuid4
from fastapi import UploadFile
from pathlib import Path

from app.core.config.storage import get_client
from app.core.config.environment import settings


def storage_upload(file: UploadFile) -> str:
    storage_key = f"{uuid4()}.{Path(file.filename or "").suffix.lower().lstrip(".")}"

    get_client().put_object(
        Key=storage_key,
        Bucket=settings.STORAGE_NAME,
        Body=file.file,
        ContentType=file.content_type
    )

    return storage_key

def storage_download(storage_key: str) -> bytes:
    response = get_client().get_object(
        Bucket=settings.STORAGE_NAME, Key=storage_key
    )

    return response["Body"].read()
