import boto3

from mypy_boto3_s3 import S3Client

from app.confs.environment import settings
from botocore.client import Config


def get_client() -> S3Client:
    return boto3.client(
        service_name=settings.BUCKET_SERVICE_NAME,
        endpoint_url=settings.BUCKET_HOST,
        aws_access_key_id=settings.BUCKET_USER,
        aws_secret_access_key=settings.BUCKET_PASSWORD,
    )
