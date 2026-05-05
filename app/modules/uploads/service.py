from celery import Celery

from app.core.storage import storage_upload
from app.modules.uploads.repository import UploadRepository
from app.modules.uploads.schemas.dtos import UploadDto
from app.modules.uploads.schemas.entities import UploadEntity


class UploadService:
    def __init__(
        self,
        upload_repository: UploadRepository,
        queue: Celery,
    ) -> None:
        self.queue = queue
        self.upload_repository = upload_repository

    async def create_upload(
        self, data: UploadDto.Upload
    ) -> UploadEntity:
        upload = await self.upload_repository.create_upload(
            data=UploadDto.Create(
                filename=data.file.filename, storage_key=storage_upload(data.file)
            )
        )

        self.queue.send_task(
            "create_publication", args=[upload.id]
        )

        return upload

    async def update_upload(self, filters: UploadDto.Read, data: UploadDto.Update) -> UploadEntity:
        return await self.upload_repository.update_upload(
            filters=filters, data=data
        )

    async def retrieve_uploads(self) -> list[UploadEntity]:
        return await self.upload_repository.retrieve_uploads()

    async def retrieve_upload(self, parameters: UploadDto.ReadOne) -> UploadEntity:
        return await self.upload_repository.retrieve_upload(
            filters=parameters
        )
