from fastapi import Depends

from app.confs.database.session import get_session
from app.modules.publications.dtos.publication import PublicationDto
from app.modules.publications.repository import PublicationRepository
from app.utils.bucket import upload


class PublicationService:
    def __init__(
        self, publication_repository: PublicationRepository = Depends()
    ) -> None:
        self.publication_repository = publication_repository

    async def create(self, data: PublicationDto.Create) -> None:
        storage_key = await upload(data.file)

        async with get_session():
            created_upload = await self.publication_repository.create(
                filename=data.file.filename,
                storage_key=storage_key
            )

        return created_upload
