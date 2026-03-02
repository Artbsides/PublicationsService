import io
import zipfile

from uuid import NAMESPACE_DNS, uuid5
from fastapi import Depends
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from app.utils.xml import parse_xml, generate_hash
from app.core.storage import storage_download
from app.core.message_broker import messaging_publish
from app.modules.uploads.service import UploadService
from app.core.config.database.session import get_session
from app.modules.uploads.schemas.dtos import UploadDto
from app.modules.uploads.schemas.enums import UploadStatusEnum
from app.modules.publications.repository import PublicationRepository
from app.modules.publications.schemas.dtos import ArticleDto, PublicationDto
from app.modules.publications.schemas.entities import ArticleEntity, PublicationEntity


class PublicationService:
    def __init__(
        self,
        upload_service: UploadService = Depends(),
        publication_repository: PublicationRepository = Depends()
    ) -> None:
        self.upload_service = upload_service
        self.publication_repository = publication_repository

    async def create_publication(
        self, data: PublicationDto.Create, is_last_retry: bool | None = None
    ) -> None:
        async with get_session():
            upload = await self.upload_service.update_upload(
                filters=UploadDto.Read(
                    id=data.upload_id, status=UploadStatusEnum.PENDING
                ),
                data=UploadDto.Update(
                    status=UploadStatusEnum.PROCESSING
                )
            )

        if upload:
            try:
                compressed_file = storage_download(upload.storage_key)

                try:
                    async with get_session():
                        publication = await self.publication_repository.create_publication(
                            data=PublicationDto.Create(upload_id=upload.id)
                        )
                except IntegrityError as exception:
                    if not isinstance(exception.orig, UniqueViolation):
                        raise exception

                    async with get_session():
                        publication = await self.publication_repository.retrieve_publication(
                            filters=PublicationDto.Read(upload_id=upload.id)
                        )

                with zipfile.ZipFile(io.BytesIO(compressed_file)) as folder:
                    xmls = [
                        filename for filename in folder.namelist() if filename.lower().endswith(".xml")
                    ]

                    for filename in xmls:
                        parsed_xml = parse_xml(
                            folder.read(filename), filename
                        )

                        idempotency_key = uuid5(
                            NAMESPACE_DNS, f"{publication.id}:{generate_hash(parsed_xml)}"
                        )

                        try:
                            async with get_session():
                                article = await self.publication_repository.create_article(
                                    data=ArticleDto.Create(
                                        publication_id=publication.id, idempotency_key=idempotency_key, data=parsed_xml
                                    )
                                )

                            await messaging_publish(
                                "articles", "article.created", article.data
                            )
                        except IntegrityError as exception:
                            if not isinstance(exception.orig, UniqueViolation):
                                raise exception

                async with get_session():
                    await self.upload_service.update_upload(
                        filters=UploadDto.ReadOne(id=upload.id), data=UploadDto.Update(
                            status=UploadStatusEnum.COMPLETED
                        )
                    )

            except Exception:
                async with get_session():
                    await self.upload_service.update_upload(
                        filters=UploadDto.ReadOne(id=upload.id), data=UploadDto.Update(
                            status=UploadStatusEnum.FAILED if is_last_retry else UploadStatusEnum.PENDING
                        )
                    )

                raise

    async def retrieve_publications(self) -> list[PublicationEntity]:
        async with get_session():
            return await self.publication_repository.retrieve_publications()

    async def retrieve_publication(self, parameters: PublicationDto.ReadOne) -> PublicationEntity:
        async with get_session():
            return await self.publication_repository.retrieve_publication(
                filters=parameters
            )

    async def retrieve_articles(self, parameters: ArticleDto.Read) -> list[ArticleEntity]:
        async with get_session():
            return await self.publication_repository.retrieve_articles(
                filters=parameters
            )

    async def retrieve_article(self, parameters: ArticleDto.Read) -> ArticleEntity:
        async with get_session():
            return await self.publication_repository.retrieve_article(
                filters=parameters
            )
