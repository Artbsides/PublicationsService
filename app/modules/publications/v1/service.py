import boto3

from uuid import uuid4
from fastapi import Depends
from botocore.client import Config

from app.confs.database.session import get_session
from app.confs.environment import settings
from app.modules.publications.v1.dtos.publication import PublicationDto
from app.modules.publications.v1.repository import PublicationRepository


class PublicationService:
    def __init__(self, publication_repository: PublicationRepository = Depends()) -> None:
        self.s3 = boto3.client(
            "s3",
            endpoint_url=settings.BUCKET_HOST,
            aws_access_key_id=settings.BUCKET_USER,
            aws_secret_access_key=settings.BUCKET_PASSWORD,
            region_name="us-east-1",
            config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
        )

        self.publication_repository = publication_repository

    async def create(self, data: PublicationDto.Create) -> None:
        upload_id = uuid4()
        object_key = f"{upload_id}.zip"

        await data.file.seek(0)
        content = await data.file.read()

        self.s3.put_object(
            Bucket=settings.BUCKET_NAME,
            Key=object_key,
            Body=content,
            ContentType=data.file.content_type or "application/zip",
        )


        async with get_session(transactional=True):
            await self.publication_repository.create()
            await self.publication_repository.create_outbox()


        return {"upload_id": upload_id, "status": "pending"}

        return await self.publication_repository.create()

    async def read(self) -> None:
        return await self.publication_repository.read()

    async def read_one(self) -> None:
        return await self.publication_repository.read_one()
