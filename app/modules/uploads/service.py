from app.core.storage import storage_upload
from app.core.config.worker import get_application
from app.modules.uploads.repository import UploadRepository
from app.core.config.database.session import get_session
from app.modules.uploads.schemas.dtos import UploadDto
from app.modules.uploads.schemas.entities import UploadEntity


class UploadService:
    def __init__(self, upload_repository: UploadRepository) -> None:
        self.upload_repository = upload_repository

    async def create_upload(
        self, data: UploadDto.Upload
    ) -> UploadEntity:
        async with get_session():
            upload = await self.upload_repository.create_upload(
                data=UploadDto.Create(
                    filename=data.file.filename, storage_key=storage_upload(data.file)
                )
            )

        get_application().send_task("create_publication", args=[upload.id])

        return upload

    async def update_upload(self, filters: UploadDto.Read, data: UploadDto.Update) -> UploadEntity:
        async with get_session():
            return await self.upload_repository.update_upload(
                filters=filters, data=data
            )

    async def retrieve_uploads(self) -> list[UploadEntity]:
        async with get_session():
            return await self.upload_repository.retrieve_uploads()

    async def retrieve_upload(self, parameters: UploadDto.ReadOne) -> UploadEntity:
        async with get_session():
            return await self.upload_repository.retrieve_upload(
                filters=parameters
            )

