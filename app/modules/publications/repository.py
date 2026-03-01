from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload

from app.enums import SourceFileStatusEnum
from app.models import ArticleModel, PublicationModel, SourceFileModel
from app.modules.publications.entities.article import ArticleEntity
from app.modules.publications.entities.publication import PublicationEntity
from app.modules.publications.entities.source_file import SourceFileEntity
from app.utils.repository import BaseRepository


class PublicationRepository(BaseRepository):
    async def create(
        self, *, filename: str, storage_key: str
    ) -> SourceFileEntity:
        query = (
            insert(SourceFileModel).values(
                filename=filename, storage_key=storage_key
            )
            .returning(SourceFileModel)
        )

        return self.to_entity(
            SourceFileEntity, (await self.session.execute(query)).scalar_one()
        )

    async def read_one(
        self, *, source_file_id: UUID, filters: dict | None = None
    ) -> PublicationEntity:
        query = select(PublicationModel).where(PublicationModel.source_file_id == source_file_id)

        if filters:
            query = query.where(
                *self.to_filters(PublicationModel, filters)
            )

        return self.to_entity(
            PublicationEntity, (await self.session.execute(query)).scalar_one()
        )

    async def update(
        self, *, source_file_id: UUID, values: dict, filters: dict | None = None
    ) -> SourceFileEntity | None:
        query = update(SourceFileModel).where(SourceFileModel.id == source_file_id)

        if filters:
            query = query.where(
                *self.to_filters(SourceFileModel, filters)
            )

        query = query.values(values).returning(SourceFileModel)

        return self.to_entity(
            SourceFileEntity, (await self.session.execute(query)).scalar_one_or_none()
        )

    async def create_publication(
        self, *, source_file_id: UUID
    ) -> PublicationEntity:
        query = insert(PublicationModel).values(source_file_id=source_file_id).returning(PublicationModel)

        return self.to_entity(
            PublicationEntity, (await self.session.execute(query)).scalar_one()
        )

    async def create_article(
        self, *, publication_id: UUID, idempotency_key: UUID, data: dict
    ) -> ArticleEntity:
        query = (
            insert(ArticleModel).values(
                publication_id=publication_id, idempotency_key=idempotency_key, data=data
            )
            .returning(ArticleModel)
        )

        return self.to_entity(
            ArticleEntity, (await self.session.execute(query)).scalar_one()
        )

    async def retrieve_pubications(self) -> list[PublicationEntity]:
        query = select(PublicationModel).options(
            selectinload(PublicationModel.source_file)
        )

        return self.to_entities(
            PublicationEntity, (await self.session.execute(query)).scalars().all()
        )

    async def retrieve_pubication(self, *, id: UUID) -> PublicationEntity:
        query = (
            select(PublicationModel).options(
                selectinload(PublicationModel.source_file)
            )
            .where(
                PublicationModel.id == id
            )
        )

        return self.to_entity(
            PublicationEntity, (await self.session.execute(query)).scalar_one()
        )

    async def retrieve_articles(self, *, publication_id: UUID) -> list[ArticleEntity]:
        query = select(ArticleModel).where(
            ArticleModel.publication_id == publication_id
        )

        return self.to_entities(
            ArticleEntity, (await self.session.execute(query)).scalars().all()
        )
