from uuid import UUID

from sqlalchemy import insert, select, update

from app.enums import SourceFileStatusEnum
from app.models import SourceFileModel
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
        self, *, source_file_id: UUID, **kwargs
    ) -> SourceFileEntity:
        query = select(SourceFileModel).where(
            SourceFileModel.id == source_file_id, *self.to_filters(SourceFileModel, kwargs)
        )

        return self.to_entity(
            SourceFileEntity, (await self.session.execute(query)).scalar_one()
        )

    async def update(
        self, *, source_file_id: UUID, filters: dict, values: dict
    ) -> SourceFileEntity | None:
        query = (
            update(SourceFileModel).where(
                SourceFileModel.id == source_file_id, *self.to_filters(SourceFileModel, filters)
            )
            .values(values)
            .returning(SourceFileModel)
        )

        return self.to_entity(
            SourceFileEntity, (await self.session.execute(query)).scalar_one_or_none()
        )
