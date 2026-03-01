import io
from uuid import NAMESPACE_DNS, UUID, uuid5
import zipfile
from fastapi import Depends
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from app.confs.broker import get_channel
from app.confs.database.session import get_session
from app.confs.workers import get_application
from app.enums import SourceFileStatusEnum
from app.models import SourceFileModel
from app.modules.publications.dtos.publication import PublicationDto
from app.modules.publications.repository import PublicationRepository
from app.utils.broker import publish
from app.utils.bucket import download, upload
from app.utils.xml import generate_hash, parse_xml


class PublicationService:
    def __init__(
        self, publication_repository: PublicationRepository = Depends()
    ) -> None:
        self.publication_repository = publication_repository

    async def create(self, data: PublicationDto.Create) -> None:
        async with get_session():
            source_file = await self.publication_repository.create(
                filename=data.file.filename, storage_key=upload(data.file)
            )

        get_application().send_task(
            "process_uploaded_file", args=[source_file.id]
        )

        return source_file

    async def process_source_file(self, source_file_id: UUID, is_last_retry: bool = False) -> None:
        async with get_session():
            source_file = await self.publication_repository.update(
                source_file_id=source_file_id, filters={"status": SourceFileStatusEnum.PENDING}, values={
                    "status": SourceFileStatusEnum.PROCESSING
                }
            )

        if source_file:
            try:
                compressed_file = download(source_file.storage_key)

                
                try:
                    async with get_session():
                        publication = await self.publication_repository.create_publication(
                            source_file_id=source_file.id
                        )
                except IntegrityError as exception:
                    if not isinstance(exception.orig, UniqueViolation):
                        raise exception

                    async with get_session():
                        publication = await self.publication_repository.read_one(
                            source_file_id=source_file.id
                        )

                with zipfile.ZipFile(io.BytesIO(compressed_file)) as folder:
                    xmls = [
                        filename for filename in folder.namelist() if filename.lower().endswith(".xml")
                    ]

                    for filename in xmls:
                        data = parse_xml(
                            folder.read(filename), filename
                        )

                        idempotency_key = uuid5(
                            NAMESPACE_DNS, f"{publication.id}:{generate_hash(data)}"
                        )

                        try:
                            async with get_session():
                                article = await self.publication_repository.create_article(
                                    publication_id=publication.id, idempotency_key=idempotency_key, data=data
                                )

                            await publish("article.created", article.data)
                        except IntegrityError as exception:
                            if not isinstance(exception.orig, UniqueViolation):
                                raise exception

                async with get_session():
                    await self.publication_repository.update(
                        source_file_id=source_file.id, values={"status": SourceFileStatusEnum.COMPLETED}
                    )

                raise Exception

            except Exception as exception:
                async with get_session():
                    await self.publication_repository.update(
                        source_file_id=source_file.id, values={
                            "status": SourceFileStatusEnum.FAILED if is_last_retry else SourceFileStatusEnum.PENDING
                        }
                    )

                raise exception
