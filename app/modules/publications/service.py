import io
from uuid import UUID
import zipfile
from fastapi import Depends

from app.confs.database.session import get_session
from app.confs.workers import get_application
from app.enums import SourceFileStatusEnum
from app.models import SourceFileModel
from app.modules.publications.dtos.publication import PublicationDto
from app.modules.publications.repository import PublicationRepository
from app.utils.bucket import download, upload
from app.utils.xml import parse_xml


class PublicationService:
    def __init__(
        self, publication_repository: PublicationRepository = Depends()
    ) -> None:
        self.publication_repository = publication_repository

    async def create(self, data: PublicationDto.Create) -> None:
        storage_key = upload(data.file)

        async with get_session():
            source_file = await self.publication_repository.create(
                filename=data.file.filename,
                storage_key=storage_key
            )

        get_application().send_task(
            "process_uploaded_file", args=[source_file.id]
        )

        return source_file

    async def process_source_file(self, source_file_id: UUID) -> None:
        async with get_session():
            source_file = await self.publication_repository.update(
                source_file_id = source_file_id, filters = { "status": SourceFileStatusEnum.PENDING }, values = {
                    "status": SourceFileStatusEnum.PROCESSING
                }
            )

        if source_file:
            try:
                compressed_file = download(source_file.storage_key)

                with zipfile.ZipFile(io.BytesIO(compressed_file)) as folder:
                    xmls = [
                        filename for filename in folder.namelist() if filename.lower().endswith(".xml")
                    ]

                    for filename in xmls:
                        data = parse_xml(folder.read(filename), filename)

            except Exception as exception:
                source_file = await self.publication_repository.update(
                    source_file_id = source_file_id, values = { "status": SourceFileStatusEnum.PENDING }
                )

                raise exception

        return None
