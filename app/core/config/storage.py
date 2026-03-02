import boto3

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client

from app.core.config.environment import settings


def get_client() -> S3Client:
    return boto3.client(
        service_name=settings.STORAGE_SERVICE_NAME,
        endpoint_url=settings.STORAGE_HOST,
        aws_access_key_id=settings.STORAGE_USER,
        aws_secret_access_key=settings.STORAGE_PASSWORD,
    )
