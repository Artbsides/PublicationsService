from sqlalchemy import insert

from app.enums import SourceFileStatusEnum
from app.models import SourceFileModel
from app.modules.publications.entities.source_file import SourceFileEntity
from app.utils.repository import BaseRepository


class PublicationRepository(BaseRepository):
    async def create(
        self, *, filename: str, storage_key: str
    ) -> None:
        query = (
            insert(SourceFileModel).values(
                filename=filename, storage_key=storage_key
            )
            .returning(SourceFileModel)
        )

        return self.to_entity(
            SourceFileEntity, (await self.session.execute(query)).scalar_one()
        )
