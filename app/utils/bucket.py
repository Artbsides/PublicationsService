from uuid import uuid4
from pathlib import Path

from fastapi import UploadFile

from app.confs.environment import settings
from app.confs.bucket import get_client


def upload(file: UploadFile) -> str:
    storage_key = f"{uuid4()}.{Path(file.filename or "").suffix.lower().lstrip(".")}"

    get_client().put_object(
        Key=storage_key,
        Bucket=settings.BUCKET_NAME,
        Body=file.file,
        ContentType=file.content_type
    )

    return storage_key

def download(storage_key: str) -> bytes:
    response = get_client().get_object(
        Bucket=settings.BUCKET_NAME, Key=storage_key
    )

    return response["Body"].read()
