from sqlalchemy import insert, select

from app.core.models import ArticleModel, PublicationModel
from app.core.database import BaseRepository
from app.modules.publications.schemas.dtos import ArticleDto, PublicationDto
from app.modules.publications.schemas.entities import ArticleEntity, PublicationEntity


class PublicationRepository(BaseRepository):
    async def create_publication(
        self, *, data: PublicationDto.Create
    ) -> PublicationEntity:
        query = (
            insert(PublicationModel).values(
                data.model_dump(exclude_unset=True)
            )
            .returning(PublicationModel)
        )

        return self.to_entity(
            PublicationEntity, (await self.session.execute(query)).scalar_one()
        )

    async def retrieve_publications(self) -> list[PublicationEntity]:
        query = select(PublicationModel)

        return self.to_entities(
            PublicationEntity, (await self.session.execute(query)).scalars().all()
        )

    async def retrieve_publication(
        self, *, filters: PublicationDto.ReadOne
    ) -> PublicationEntity:
        query = select(PublicationModel).where(
            *self.to_filters(PublicationModel, filters)
        )

        return self.to_entity(
            PublicationEntity, (await self.session.execute(query)).scalar_one()
        )

    async def create_article(
        self, *, data: ArticleDto.Create
    ) -> ArticleEntity:
        query = (
            insert(ArticleModel).values(
                data.model_dump(exclude_unset=True)
            )
            .returning(ArticleModel)
        )

        return self.to_entity(
            ArticleEntity, (await self.session.execute(query)).scalar_one()
        )

    async def retrieve_articles(
        self, *, filters: ArticleDto.Read
    ) -> list[ArticleEntity]:
        query = select(ArticleModel).where(
            *self.to_filters(ArticleModel, filters)
        )

        return self.to_entities(
            ArticleEntity, (await self.session.execute(query)).scalars().all()
        )

    async def retrieve_article(
        self, *, filters: ArticleDto.ReadOne
    ) -> ArticleEntity:
        query = select(ArticleModel).where(
            *self.to_filters(ArticleModel, filters)
        )

        return self.to_entity(
            ArticleEntity, (await self.session.execute(query)).scalar_one()
        )
